"""Ontos — a validator, parser, and generator for the precision language.

Ontos is *strictly hierarchical, unambiguous, and context-free*. This module
encodes the rules documented in ``ontos-language/grammar.md`` and
``ontos-language/phonology.md`` so that an Ontos statement can be checked by
software rather than by eye.

The grammar in one breath:

* Every non-atomic operation **must** be wrapped in parentheses.
* There is **no operator precedence** — `A ∧ B → C` is ambiguous and invalid.
* Variables must be **bound** by a quantifier (``∀``/``∃``) or a ``Let`` binding.
* Raw self-reference (``A = A``) is forbidden unless wrapped with ``⍶``.
* Layer scopes ``[λ_Debug] ( ... )`` and layer shifts ``(λ_Debug → λ_Dream)(A)``
  are recognized as first-class constructs.

The validator returns a :class:`ValidationResult` with structured errors so the
CLI (and future editor integrations) can point at exactly what went wrong.
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass, field
from enum import Enum

# --------------------------------------------------------------------------- #
# Symbol tables — lifted verbatim from phonology.md / grammar.md.
# --------------------------------------------------------------------------- #

# Logical operators. ⊥ (contradiction) is intentionally absent: the spec calls it
# "Invalid in Ontos."
LOGICAL_OPS = {"¬", "∧", "∨", "→", "↔"}
BINARY_OPS = {"∧", "∨", "→", "↔"}
QUANTIFIERS = {"∀", "∃"}
META_SYMBOLS = {"⏄", "⏅", "⏆", "⍶"}  # unknown, incomplete, paradox, self-ref
LAYER_PREFIX = "λ"
ENTITY_PREFIXES = {"𝒢", "𝒩", "𝒫", "⚡", "⚢"}  # god, npc, player, anomaly (doc glyphs)
TRUTH_SYMBOLS = {"⊤"}

# The marked-self-reference operator. Without it, a name equalling itself is a
# forbidden raw self-reference (see grammar.md Rule 5).
SELF_REF = "⍶"


# --------------------------------------------------------------------------- #
# Public result types.
# --------------------------------------------------------------------------- #


class TokenKind(str, Enum):
    """The lexical categories an Ontos source string breaks into."""

    CONSTANT = "constant"          # 𝒢_Architect, λ_Debug, ⚢_EchoingDoor, ⊤
    VARIABLE = "variable"          # x, y, z (lowercase identifiers)
    OP = "op"                      # ¬ ∧ ∨ → ↔
    EQUALITY = "equality"          # = ≠ < > ≤ ≥ + − × ÷
    QUANTIFIER = "quantifier"      # ∀ ∃
    META = "meta"                  # ⏄ ⏅ ⏆ ⍶
    LPAREN = "lparen"              # ( )
    RPAREN = "rparen"
    LBRACKET = "lbracket"          # [ ]  (layer scope)
    RBRACKET = "rbracket"
    ARROW = "arrow"                # → when used as a layer shift
    LET = "let"                    # Let X = ...
    COMMA = "comma"


@dataclass(frozen=True)
class Token:
    """A single lexical token with its source position for error reporting."""

    kind: TokenKind
    text: str
    pos: int

    def __str__(self) -> str:
        return self.text


@dataclass
class ValidationError(ValueError):
    """One problem found while validating an Ontos statement.

    Subclasses ``ValueError`` so it can be raised *and* stored in a result list,
    letting the lexer signal fatal errors while the parser accumulates the rest.
    """

    rule: str
    message: str
    position: int = -1


@dataclass
class ValidationResult:
    """Outcome of validating a statement (or several)."""

    valid: bool
    errors: list[ValidationError] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def __bool__(self) -> bool:
        return self.valid


# --------------------------------------------------------------------------- #
# Golden cases — the exact valid/invalid pairs from grammar.md. These double as
# the validator's acceptance contract and the unit-test fixtures.
# --------------------------------------------------------------------------- #

GOLDEN_CASES: dict[str, bool] = {
    # Rule 1 & 2 — parentheses mandatory, no precedence.
    "(A ∧ B) → C": True,
    "A ∧ B → C": False,
    "(A → B) → C": True,
    "(A ∧ B) ∨ C": True,
    "A ∧ B ∨ C": False,
    "(A → B) ∧ (A → C)": True,
    "A → B ∧ C": False,
    "(A ↔ B) ∧ (B ↔ C)": True,
    # Rule 4 — variables must be bound.
    "∀x (x ∈ λ_Debug)": True,
    "x ∈ λ_Debug": False,
    "Let X = 𝒢_Architect → (X → ⚢_NewAnomaly)": True,
    # Rule 5 — marked vs raw self-reference.
    "⍶(A) = A": True,
    "A = A": False,
    # Layer scope & shift.
    "[λ_Debug] (A → B)": True,
    "(λ_Debug → λ_Dream) (A)": True,
    # Complex sentences from grammar.md.
    "∀x ((x ∈ λ_Debug) → (∃y (y = ⚢_EchoingDoor)))": True,
    "[λ_Debug] (𝒩_Alice → (⚡_EchoingDoor → (𝒢_Architect → ⚢_NewAnomaly)))": True,
    # Gödelian statement.
    "⏅(Ontos) ∧ (Ontos → ⏄)": True,
}


# --------------------------------------------------------------------------- #
# Lexer.
# --------------------------------------------------------------------------- #

_EQUALITY_CHARS = set("=≠<≥")  # < > ≤ are handled below; these are unambiguous
_MULTI_CHAR_HINTS = {"≤", "≥"}

# A constant looks like: a leading glyph (𝒢/𝒩/↯/λ/⊤) optionally followed by
# _Name, OR a bare uppercase identifier (A, B, Ontos).
_CONSTANT_RE = re.compile(
    r"(?:[\U0001D4A2\U0001D4A9\U0001D4AB\u26A1\u26A2\u03bb\u22a4\u23c5\u23c4\u23c6\u2378A-Z])[A-Za-z0-9_\u2080-\u2089]*"
)
_VARIABLE_RE = re.compile(r"[a-z][a-z0-9_]*")


def _is_const_start(ch: str) -> bool:
    return ch in ENTITY_PREFIXES or ch == LAYER_PREFIX or ch in TRUTH_SYMBOLS or ch.isupper()


def tokenize(source: str) -> list[Token]:
    """Break an Ontos source string into tokens.

    Whitespace is skipped. Raises :class:`ValidationError` (with a position) on
    an unrecognizable character so callers get a precise pointer.
    """

    tokens: list[Token] = []
    i = 0
    n = len(source)
    while i < n:
        ch = source[i]

        if ch.isspace():
            i += 1
            continue

        if ch == "(":
            tokens.append(Token(TokenKind.LPAREN, ch, i)); i += 1; continue
        if ch == ")":
            tokens.append(Token(TokenKind.RPAREN, ch, i)); i += 1; continue
        if ch == "[":
            tokens.append(Token(TokenKind.LBRACKET, ch, i)); i += 1; continue
        if ch == "]":
            tokens.append(Token(TokenKind.RBRACKET, ch, i)); i += 1; continue
        if ch == ",":
            tokens.append(Token(TokenKind.COMMA, ch, i)); i += 1; continue

        # Quantifiers and meta symbols are single glyphs.
        if ch in QUANTIFIERS:
            tokens.append(Token(TokenKind.QUANTIFIER, ch, i)); i += 1; continue
        if ch in META_SYMBOLS:
            tokens.append(Token(TokenKind.META, ch, i)); i += 1; continue

        # The arrow → is overloaded: a binary op (implication) *or* part of a
        # layer-shift. We emit it as OP; the parser disambiguates by context.
        if ch == "→":
            tokens.append(Token(TokenKind.OP, ch, i)); i += 1; continue
        if ch in BINARY_OPS - {"→"}:  # ∧ ∨ ↔
            tokens.append(Token(TokenKind.OP, ch, i)); i += 1; continue
        if ch == "¬":
            tokens.append(Token(TokenKind.OP, ch, i)); i += 1; continue

        # Membership / equality family.
        if ch == "∈":
            tokens.append(Token(TokenKind.EQUALITY, ch, i)); i += 1; continue
        if ch in _EQUALITY_CHARS or ch in {"<", ">", "≤", "≥", "+", "−", "×", "÷", "="}:
            tokens.append(Token(TokenKind.EQUALITY, ch, i)); i += 1; continue

        # `Let` binding keyword (case-insensitive, word-bounded).
        if ch in "Ll":
            m = re.match(r"[Ll]et\b", source[i:])
            if m:
                tokens.append(Token(TokenKind.LET, m.group(0), i))
                i += m.end()
                continue

        # Constants start with a glyph or uppercase letter.
        if _is_const_start(ch):
            m = _CONSTANT_RE.match(source, i)
            if m:
                tokens.append(Token(TokenKind.CONSTANT, m.group(0), i))
                i = m.end()
                continue

        # Variables: lowercase identifiers (but not the 'let' keyword).
        if ch.islower():
            m = _VARIABLE_RE.match(source, i)
            if m:
                tokens.append(Token(TokenKind.VARIABLE, m.group(0), i))
                i = m.end()
                continue

        raise ValidationError(
            rule="lex",
            message=f"unrecognized character {ch!r}",
            position=i,
        )

    return tokens


# --------------------------------------------------------------------------- #
# Parser / validator.
# --------------------------------------------------------------------------- #


class _Parser:
    """Recursive-descent validator over a token list.

    Grammar model (matching grammar.md Rules 1-5):

    A statement is a *chain* of operands joined by binary operators or
    relations::

        statement  := operand ( (BINOP | REL) operand )*

    where an ``operand`` is one of::

        operand := atom
                 | "(" statement ")"          # parenthesized group
                 | quantifier var "(" statement ")"
                 | "[" layer "]" "(" statement ")"
                 | "(layer → layer)" "(" atom ")"
                 | "⍶" "(" atom ")"
                 | "¬" operand                 # unary negation
                 | meta "(" atom ")"

    Rule 1 (mandatory parentheses): only the *outermost* binary operation may go
    unparenthesized. Any nested binary form must be wrapped. We enforce this by
    tracking whether the operand we just parsed is "compound" (it was itself a
    binary chain). If a binary operator follows a compound operand that was not
    wrapped in parens, the statement is ambiguous and invalid.
    """

    def __init__(self, tokens: list[Token]) -> None:
        self.toks = tokens
        self.i = 0
        self.errors: list[ValidationError] = []
        # Bound-variable stack. A variable is in scope while inside its
        # quantifier's parentheses or its Let binding.
        self._bound: set[str] = set()

    @property
    def cur(self) -> Token | None:
        return self.toks[self.i] if self.i < len(self.toks) else None

    def _advance(self) -> Token | None:
        t = self.cur
        self.i += 1
        return t

    def _expect(self, kind: TokenKind, rule: str, what: str) -> Token | None:
        if self.cur is None or self.cur.kind != kind:
            got = "end of input" if self.cur is None else repr(self.cur.text)
            self.errors.append(ValidationError(
                rule=rule,
                message=f"expected {what}, got {got}",
                position=self.cur.pos if self.cur else -1,
            ))
            return None
        return self._advance()

    # -- entry point -------------------------------------------------------- #

    def parse_statement(self) -> None:
        """Parse one top-level statement (a Let binding or an expression chain)."""

        if self.cur and self.cur.kind == TokenKind.LET:
            self._parse_let()
            return
        self._parse_chain(top=True)

    def _parse_let(self) -> None:
        self._expect(TokenKind.LET, "let", "\'Let\'")
        name = self.cur
        if name is None or name.kind not in (TokenKind.VARIABLE, TokenKind.CONSTANT):
            self.errors.append(ValidationError(
                rule="let",
                message="\'Let\' must bind a variable name",
                position=name.pos if name else -1,
            ))
            return
        self._advance()
        self._bound.add(name.text)
        self._expect(TokenKind.EQUALITY, "let", "\'=\'")
        self._parse_chain(top=True)

    def _is_binary_op(self, tok: Token | None) -> bool:
        return tok is not None and tok.kind == TokenKind.OP and tok.text in BINARY_OPS

    def _is_relation(self, tok: Token | None) -> bool:
        return tok is not None and tok.kind == TokenKind.EQUALITY

    def _parse_chain(self, *, top: bool = False) -> None:
        """Parse: operand ( (BINOP|REL) operand )* with Rule-1 enforcement.

        Rule 1 (grammar.md): only the *outermost* binary operation may go
        unparenthesized. A chain of two or more binary operators at the same
        level is ambiguous — the inner ones must be wrapped. So at the top
        level exactly one binary op is permitted; a second is an error. Inside
        parens the same rule applies recursively (top=False), where even one
        compound operand followed by an op is ambiguous.
        """

        op_count = 0
        self._parse_operand()
        while self._is_binary_op(self.cur) or self._is_relation(self.cur):
            op_tok = self._advance()
            op_count += 1
            # Rule 1: only one binary op is permitted at this level. A second
            # means the first operand should have been parenthesized.
            if op_count >= 2:
                self.errors.append(ValidationError(
                    rule="grouping",
                    message=(
                        "ambiguous: nested binary operation must be "
                        "parenthesized (wrap the left operand)"
                    ),
                    position=op_tok.pos,
                ))
            self._parse_operand()

    def _parse_operand(self) -> bool:
        """Parse a single operand. Return True if it was *compound* (a binary
        chain), False if atomic (atom / paren group / quantified / etc.).

        A parenthesized group counts as atomic for Rule-1 purposes because the
        parens have already disambiguated it.
        """

        t = self.cur
        if t is None:
            self.errors.append(ValidationError(
                rule="syntax", message="unexpected end of input", position=-1,
            ))
            return False

        # Layer scope:  [λ_Debug] ( ... )
        if t.kind == TokenKind.LBRACKET:
            self._parse_layer_scope()
            return False

        # Layer shift:  (λ_Debug → λ_Dream) (A)
        if t.kind == TokenKind.LPAREN and self._is_layer_shift_ahead():
            self._parse_layer_shift()
            return False

        # Quantified:  ∀x ( ... )
        if t.kind == TokenKind.QUANTIFIER:
            self._parse_quantified()
            return False

        # Unary negation:  ¬A
        if t.kind == TokenKind.OP and t.text == "¬":
            self._advance()
            self._parse_operand()
            return False

        # Meta symbols: either applied as ⍶(A)/⏅(Ontos), or bare as
        # a noun (e.g. "Ontos → ⏄" where ⏄ is "the unknown").
        if t.kind == TokenKind.META:
            nxt = self.toks[self.i + 1] if self.i + 1 < len(self.toks) else None
            if nxt is not None and nxt.kind == TokenKind.LPAREN:
                return self._parse_meta_operand()
            # Bare meta symbol used as a constant.
            self._advance()
            return False

        # Parenthesized sub-expression — atomic, fully disambiguated.
        if t.kind == TokenKind.LPAREN:
            self._parse_parens()
            return False

        # Bare constant or bound variable.
        if t.kind in (TokenKind.CONSTANT, TokenKind.VARIABLE):
            self._parse_atom()
            return False

        # A binary op or relation with no left operand.
        if t.kind in (TokenKind.OP, TokenKind.EQUALITY):
            self.errors.append(ValidationError(
                rule="grouping",
                message="binary operator with no left operand",
                position=t.pos,
            ))
            self._advance()
            self._parse_operand()
            return False

        # Unexpected token.
        self.errors.append(ValidationError(
            rule="syntax",
            message=f"unexpected token {t.text!r}",
            position=t.pos,
        ))
        self._advance()
        return False

    def _parse_atom(self) -> None:
        t = self.cur
        if t is None:
            self.errors.append(ValidationError(
                rule="syntax", message="unexpected end of input", position=-1,
            ))
            return
        if t.kind == TokenKind.CONSTANT:
            self._advance()
            return
        if t.kind == TokenKind.VARIABLE:
            if t.text not in self._bound:
                self.errors.append(ValidationError(
                    rule="unbound",
                    message=f"variable {t.text!r} is not bound by a quantifier or Let",
                    position=t.pos,
                ))
            self._advance()
            return
        self.errors.append(ValidationError(
            rule="syntax",
            message=f"expected a constant or variable, got {t.text!r}",
            position=t.pos,
        ))
        self._advance()

    def _parse_parens(self) -> None:
        self._expect(TokenKind.LPAREN, "grouping", "\'(\'")
        # Inside parens a full chain is legal: (A ∧ B)
        self._parse_chain()
        self._expect(TokenKind.RPAREN, "grouping", "\')\'")

    def _parse_meta_operand(self) -> bool:
        self._expect(TokenKind.META, "meta", "meta symbol")
        self._expect(TokenKind.LPAREN, "meta", "\'(\' after meta symbol")
        self._parse_atom()
        self._expect(TokenKind.RPAREN, "meta", "\')\'")
        # Optional trailing relation: ⍶(A) = A
        if self._is_relation(self.cur):
            self._advance()
            self._parse_atom()
        return False

    def _parse_quantified(self) -> None:
        self._expect(TokenKind.QUANTIFIER, "quantifier", "quantifier (∀ or ∃)")
        var = self.cur
        if var is None or var.kind != TokenKind.VARIABLE:
            self.errors.append(ValidationError(
                rule="quantifier",
                message="quantifier must bind a lowercase variable",
                position=var.pos if var else -1,
            ))
            return
        self._advance()
        prev_bound = set(self._bound)
        self._bound.add(var.text)
        self._expect(TokenKind.LPAREN, "quantifier", "\'(\' to open the quantified scope")
        self._parse_chain()
        self._expect(TokenKind.RPAREN, "quantifier", "\')\' to close the quantified scope")
        self._bound = prev_bound

    def _parse_layer_scope(self) -> None:
        self._expect(TokenKind.LBRACKET, "layer-scope", "\'[\'")
        if self.cur and self.cur.kind == TokenKind.CONSTANT and self.cur.text.startswith(LAYER_PREFIX):
            self._advance()
        elif self.cur is not None:
            self.errors.append(ValidationError(
                rule="layer-scope",
                message=f"expected a layer constant (λ_…), got {self.cur.text!r}",
                position=self.cur.pos,
            ))
        self._expect(TokenKind.RBRACKET, "layer-scope", "\']\'")
        if self.cur and self.cur.kind == TokenKind.LPAREN:
            self._parse_parens()

    def _is_layer_shift_ahead(self) -> bool:
        """Heuristic: is this `(` the start of `(λ_Debug → λ_Dream)`?"""
        if self.i + 2 >= len(self.toks):
            return False
        second = self.toks[self.i + 1]
        third = self.toks[self.i + 2]
        if second.kind != TokenKind.CONSTANT or not second.text.startswith(LAYER_PREFIX):
            return False
        return third.kind == TokenKind.OP and third.text == "→"

    def _parse_layer_shift(self) -> None:
        self._expect(TokenKind.LPAREN, "layer-shift", "\'(\'")
        if self.cur and self.cur.kind == TokenKind.CONSTANT:
            self._advance()
        self._expect(TokenKind.OP, "layer-shift", "\'→\'")
        if self.cur and self.cur.kind == TokenKind.CONSTANT:
            self._advance()
        self._expect(TokenKind.RPAREN, "layer-shift", "\')\'")
        self._expect(TokenKind.LPAREN, "layer-shift", "\'(\' for the shifted argument")
        self._parse_atom()
        self._expect(TokenKind.RPAREN, "layer-shift", "\')\'")


def validate_statement(source: str) -> ValidationResult:
    """Validate a single Ontos statement.

    Returns a :class:`ValidationResult` whose ``errors`` explain every rule
    violation found (lexer errors are raised as ``ValidationError`` by
    :func:`tokenize`).
    """

    source = source.strip()
    if not source:
        return ValidationResult(valid=False, errors=[
            ValidationError(rule="empty", message="statement is empty"),
        ])

    try:
        tokens = tokenize(source)
    except ValidationError as e:
        return ValidationResult(valid=False, errors=[e])

    parser = _Parser(tokens)
    parser.parse_statement()

    # Anything left unparsed is a structural error.
    if parser.i != len(tokens):
        leftover = parser.cur
        parser.errors.append(ValidationError(
            rule="syntax",
            message=f"unexpected trailing tokens starting at {leftover.text!r}",
            position=leftover.pos if leftover else -1,
        ))

    # Rule 5: raw self-reference. `A = A` (same constant both sides) is only
    # allowed when wrapped in ⍶. We detect the bare form lexically; run it
    # regardless of other errors so the specific self-ref rule is reported too.
    _check_raw_self_reference(source, parser.errors)

    return ValidationResult(
        valid=not parser.errors,
        errors=parser.errors,
    )


def _check_raw_self_reference(source: str, errors: list[ValidationError]) -> None:
    """Flag ``X = X`` where X is the same bare constant on both sides.

    The marked form ``⍶(X) = X`` is explicitly permitted, so we skip any
    statement whose source begins with the self-reference glyph.
    """

    if source.startswith(SELF_REF):
        return
    # Match `Name = Name` with identical names and no surrounding parentheses.
    m = re.match(r"^([A-Za-z𝒢𝒩↯][\w]*)\s*=\s*\1\s*$", source)
    if m:
        errors.append(ValidationError(
            rule="self-reference",
            message=(
                "raw self-reference is forbidden; wrap with ⍶, e.g. "
                f"⍶({m.group(1)}) = {m.group(1)}"
            ),
            position=0,
        ))


def validate_many(sources: list[str]) -> list[ValidationResult]:
    """Validate several statements at once (one result each)."""

    return [validate_statement(s) for s in sources]


# --------------------------------------------------------------------------- #
# Generator — build valid Ontos statements from a small grammar fragment.
# --------------------------------------------------------------------------- #

# A tiny vocabulary aligned with the Hidden Gods simulation. Kept minimal so the
# output is always grammatical and readable.
_SAMPLE_GODS = ["𝒢_Architect", "𝒢_Debugger", "𝒢_Dreamer", "𝒢_Engineer"]
_SAMPLE_ANOMALIES = ["⚡_EchoingDoor", "⚡_Flicker", "⚡_LoopRoom", "⚡_NewAnomaly"]
_SAMPLE_PLAYERS = ["𝒫_Alice", "𝒫_Brett", "𝒫_Cleo"]
_SAMPLE_LAYERS = ["λ_Debug", "λ_Dream", "λ_Machine", "λ₀"]
_BINARY = ["∧", "∨", "→", "↔"]


def generate_statement(rng: random.Random | None = None) -> str:
    """Produce one valid, randomized Ontos statement.

    The generator only ever emits fully-parenthesized forms, so its output is
    guaranteed to pass :func:`validate_statement`. Useful for seeding sessions
    or fuzz-testing the validator itself.
    """

    rng = rng or random.Random()
    template = rng.choice(("quantified", "layer_scope", "godelian", "binary"))

    if template == "quantified":
        layer = rng.choice(_SAMPLE_LAYERS)
        anomaly = rng.choice(_SAMPLE_ANOMALIES)
        return f"∀x ((x ∈ {layer}) → (∃y (y = {anomaly})))"

    if template == "layer_scope":
        layer = rng.choice(_SAMPLE_LAYERS)
        player = rng.choice(_SAMPLE_PLAYERS)
        anomaly = rng.choice(_SAMPLE_ANOMALIES)
        god = rng.choice(_SAMPLE_GODS)
        new = rng.choice(_SAMPLE_ANOMALIES)
        return f"[{layer}] ({player} → ({anomaly} → ({god} → {new})))"

    if template == "godelian":
        return "⏅(Ontos) ∧ (Ontos → ⏄)"

    # binary: two random atoms joined with a binary op, fully parenthesized.
    a = rng.choice(_SAMPLE_GODS + _SAMPLE_ANOMALIES)
    b = rng.choice(_SAMPLE_GODS + _SAMPLE_ANOMALIES)
    op = rng.choice(_BINARY)
    return f"({a} {op} {b})"


def generate_batch(n: int, seed: int | None = None) -> list[str]:
    """Generate ``n`` valid Ontos statements, optionally seeded for reproducibility."""

    rng = random.Random(seed)
    return [generate_statement(rng) for _ in range(n)]
