"""Ontos ↔ English translation.

A faithful, dictionary-driven translator built directly from the symbol tables
in ``ontos-language/phonology.md`` and the sentence-structure table in
``ontos-language/grammar.md``. Ontos is a precision language, so a literal,
compositional gloss is exactly right: unambiguous and a little wooden.
"""

from __future__ import annotations

import re

# --------------------------------------------------------------------------- #
# Symbol glossaries — one meaning per symbol, per phonology.md.
# --------------------------------------------------------------------------- #

# Logical symbols (phonology.md §1). ⊥ is "Invalid in Ontos," so it is absent.
LOGICAL_GLOSSES: dict[str, str] = {
    "⊤": "True",
    "¬": "not",
    "∧": "and",
    "∨": "or",
    "→": "implies",
    "↔": "if and only if",
    "∀": "for all",
    "∃": "there exists",
}

# Meta symbols (grammar.md §3 operators table). ⍶ is self-reference.
META_GLOSSES: dict[str, str] = {
    "⏄": "the unknown",          # used as a noun: "Ontos implies the unknown"
    "⏅": "is incomplete",          # applied: ⏅(Ontos) -> "Ontos is incomplete"
    "⏆": "is paradoxical",
    "⍶": "refers to itself",
}

# Entity / anomaly / player / NPC prefixes. The leading glyph is the category
# marker; the trailing name is kept verbatim. Three distinct script capitals per
# phonology.md: 𝒢 (God), 𝒩 (NPC), 𝒫 (Player); ⚡/⚡ mark anomalies.
ENTITY_GLYPHS: dict[str, str] = {
    "\U0001D4A2": "the Hidden God",   # script G
    "\u26A1": "the anomaly",           # lightning (README form)
    "\u26A2": "the anomaly",           # doubled-female (grammar.md form)
    "\U0001D4A9": "NPC",              # script N
    "\U0001D4AB": "Player",           # script P
}

LAYER_GLYPH = "λ"

RELATION_GLOSSES: dict[str, str] = {
    "=": "equals",
    "≠": "does not equal",
    "∈": "is in",
    "<": "is less than",
    ">": "is greater than",
    "≤": "is at most",
    "≥": "is at least",
    "+": "plus",
    "−": "minus",
    "×": "times",
    "÷": "divided by",
}

LET_GLOSS = "Let"

# Operators that can join two operands in a binary chain.
_ALL_OPS = set(LOGICAL_GLOSSES) | set(RELATION_GLOSSES) - {"⊤"}


def _gloss_constant(text: str) -> str:
    """Translate a constant token to its English gloss.

    Constants are category-glyph + name (``𝒢_Architect``) or bare identifiers
    (``A``, ``Ontos``). Layers get a friendly reading. Bare meta symbols
    (e.g. ``⏄`` used as a noun) gloss directly.
    """

    text = text.strip()
    if text in LOGICAL_GLOSSES:
        return LOGICAL_GLOSSES[text]
    if text in META_GLOSSES:
        return META_GLOSSES[text]

    # Layer: λ_Debug -> "the Debug Layer". λ₀ -> "Base Reality".
    if text.startswith(LAYER_GLYPH):
        rest = text[1:]
        if rest in ("₀", "0"):
            return "Base Reality"
        name = rest.lstrip("_")
        return f"the {name} Layer"

    # Entity / anomaly / player — look up by leading glyph.
    if text and text[0] in ENTITY_GLYPHS:
        category = ENTITY_GLYPHS[text[0]]
        name = text[1:].lstrip("_")
        return f"{category} {name}".strip()

    # Bare uppercase identifier (A, B, Ontos) — pass through.
    return text


def _is_atom(token: str) -> bool:
    """True if ``token`` is a single constant/variable with no operator or
    grouping inside. A parenthesized or meta-applied form is *not* an atom."""

    token = token.strip()
    if not token or " " in token or "(" in token or ")" in token:
        return False
    return not any(op in token for op in _ALL_OPS if op != "⊤")


def _split_top_binary(source: str) -> tuple[str, str | None, str]:
    """Split ``A op B`` at the top-level (depth-0) binary operator.

    Returns ``(left, op_or_None, right)``. The first depth-0 operator wins,
    matching left-to-right reading.
    """

    depth = 0
    i = 0
    while i < len(source):
        ch = source[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif depth == 0 and ch in _ALL_OPS:
            return source[:i].strip(), ch, source[i + 1:].strip()
        i += 1
    return source.strip(), None, ""


def _split_outer(source: str) -> tuple[str | None, tuple[str, str] | None]:
    """If ``source`` is ``( … ) [op tail]`` return inner text and optional
    ``(op, tail)``. Returns ``(None, None)`` when not parenthesized."""

    s = source.strip()
    if not s.startswith("("):
        return None, None
    depth = 0
    for idx, ch in enumerate(s):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                inner = s[1:idx]
                rest = s[idx + 1:].strip()
                if rest and rest[0] in _ALL_OPS:
                    return inner, (rest[0], rest[1:].strip())
                return inner, None
    return s[1:], None  # unterminated; best effort


def translate_to_english(source: str) -> str:
    """Render an Ontos statement as an English gloss.

    Compositional and literal: operators read infix, quantifiers prefix their
    body, layer scopes read as "In the X Layer, …", and meta-applications such
    as ``⏅(Ontos)`` read as "Ontos is incomplete". Unknown tokens pass through
    so a partial translation stays useful.
    """

    source = source.strip()
    if not source:
        return ""

    # Layer scope:  [λ_Debug] ( <body> )
    m = re.match(r"^\[(λ[₀-₉\w]*)\]\s*\((.*)\)\s*$", source, re.DOTALL)
    if m:
        layer = _gloss_constant(m.group(1))
        return f"In {layer}, {_chain_to_english(m.group(2))}"

    # Layer shift:  (λ_Debug → λ_Dream)(A)
    m = re.match(r"^\((λ[₀-₉\w]*)\s*→\s*(λ[₀-₉\w]*)\)\s*\((.+?)\)\s*$", source, re.DOTALL)
    if m:
        frm = _gloss_constant(m.group(1))
        to = _gloss_constant(m.group(2))
        arg = _gloss_constant(m.group(3).strip())
        return f"{arg} transitions from {frm} to {to}"

    # Let binding.
    m = re.match(r"^Let\s+([A-Za-z]\w*)\s*=\s*(.+)$", source, re.DOTALL | re.IGNORECASE)
    if m:
        return f"{LET_GLOSS} {m.group(1)} equal {translate_to_english(m.group(2))}"

    return _chain_to_english(source)


def _chain_to_english(source: str) -> str:
    """Translate a (possibly unparenthesized) binary chain or single form."""

    source = source.strip()
    if not source:
        return ""

    # Marked self-reference:  ⍶(A) = A
    m = re.match(r"^⍶\((.+?)\)\s*=\s*(.+?)\s*$", source, re.DOTALL)
    if m:
        a = _gloss_constant(m.group(1).strip())
        b = _gloss_constant(m.group(2).strip())
        return f"{a} refers to itself and equals {b}"

    # Meta-application:  ⏅(Ontos)  -> "Ontos is incomplete".
    # Only matches a single, non-nested group so that
    # "⏅(Ontos) ∧ (Ontos → ⏄)" falls through to the binary-chain handler.
    m = re.match(r"^([⏄⏅⏆])\(([^()]+)\)\s*$", source)
    if m:
        meta = META_GLOSSES.get(m.group(1), m.group(1))
        arg = _gloss_constant(m.group(2).strip())
        return f"{arg} {meta}"

    # Quantified:  ∀x ( <body> )
    m = re.match(r"^([∀∃])([a-z]\w*)\s*\((.*)\)\s*$", source, re.DOTALL)
    if m:
        quant = LOGICAL_GLOSSES.get(m.group(1), m.group(1))
        return f"{quant} {m.group(2)}, {_chain_to_english(m.group(3))}"

    # Parenthesized binary:  (A ∧ B) [op tail]
    if source.startswith("("):
        inner, trailing = _split_outer(source)
        if inner is not None:
            gloss = _chain_to_english(inner)
            if trailing:
                op, tail = trailing
                gloss += f" {LOGICAL_GLOSSES.get(op, op)} {_chain_to_english(tail)}"
            return gloss

    # Unparenthesized binary chain:  A ∧ B  or  A = B  (single op only).
    left, op, right = _split_top_binary(source)
    if op is not None:
        left_g = _gloss_constant(left) if _is_atom(left) else _chain_to_english(left)
        right_g = _gloss_constant(right) if _is_atom(right) else _chain_to_english(right)
        connector = LOGICAL_GLOSSES.get(op) or RELATION_GLOSSES.get(op, op)
        return f"{left_g} {connector} {right_g}"

    # Bare atom.
    return _gloss_constant(source)


# --------------------------------------------------------------------------- #
# English -> Ontos (the Navigator direction).
# --------------------------------------------------------------------------- #
#
# The reverse direction is intentionally a *sketch*: natural language is
# ambiguous, so we extract a best-effort Ontos rendering by spotting entity
# categories, layer names, and relational verbs in the prose. The output is
# always valid Ontos (fully parenthesized), which the validator confirms.

import re as _re
from dataclasses import dataclass, field

# Keyword -> Ontos glyph. Order matters: check longer phrases first.
_ENTITY_KEYWORDS: list[tuple[str, str]] = [
    # Gods (by name or role).
    ("architect", "𝒢_Architect"),
    ("debugger", "𝒢_Debugger"),
    ("dreamer", "𝒢_Dreamer"),
    ("engineer", "𝒢_Engineer"),
    ("god", "𝒢_God"),
    # Players (by role or "player X").
    ("player", "𝒫_Player"),
    ("alice", "𝒫_Alice"),
    ("brett", "𝒫_Brett"),
    ("cleo", "𝒫_Cleo"),
    # NPCs.
    ("guide", "𝒩_Guide"),
    ("npc", "𝒩_NPC"),
]

_LAYER_KEYWORDS: list[tuple[str, str]] = [
    ("base reality", "λ₀"),       # Base Reality
    ("debug", "λ_Debug"),
    ("dream", "λ_Dream"),
    ("machine", "λ_Machine"),
]

# Verbs that imply an implication (A -> B).
_IMPLY_VERBS = {"implies", "causes", "leads to", "creates", "reveals", "opens", "triggers"}
# Verbs that imply conjunction (A and B).
_AND_VERBS = {"and", "with", "alongside"}
# Verbs that imply a relation (A = B, or A is-in layer).
_REL_VERBS = {"is", "equals", "resides in", "lives in", "enters", "in"}


@dataclass
class NavigatorOutput:
    """Structured summary of a story, in Ontos terms.

    The 'Navigator' is the conceptual bridge between natural-language lore and
    the precision language: it reads a story, extracts the actors/layers/anomalies
    and the relations between them, and emits valid Ontos statements plus a
    human-readable summary.
    """

    entities: list[str] = field(default_factory=list)
    layers: list[str] = field(default_factory=list)
    anomalies: list[str] = field(default_factory=list)
    statements: list[str] = field(default_factory=list)
    summary: str = ""

    def render(self) -> str:
        """Pretty-print the Navigator output for display."""

        lines = ["🧭 Navigator Output", "=" * 40]
        if self.entities:
            lines.append("Actors:  " + ", ".join(self.entities))
        if self.layers:
            lines.append("Layers:  " + ", ".join(self.layers))
        if self.anomalies:
            lines.append("Anomalies: " + ", ".join(self.anomalies))
        if self.statements:
            lines.append("")
            lines.append("Ontos statements:")
            for s in self.statements:
                lines.append(f"  {s}")
        if self.summary:
            lines.append("")
            lines.append(f"Summary: {self.summary}")
        return "\n".join(lines)


def _find_anomalies(text: str) -> list[str]:
    """Heuristically spot anomaly references in prose."""

    anomalies: list[str] = []
    # "the echoing door", "a glitch", "an anomaly", "the flicker", etc.
    anomaly_names = {
        "echoing door": "⚡_EchoingDoor",
        "flicker": "⚡_Flicker",
        "loop room": "⚡_LoopRoom",
        "glitch": "⚡_Glitch",
        "anomaly": "⚡_Anomaly",
        "null pointer": "⚡_NullPointer",
    }
    lower = text.lower()
    for phrase, glyph in anomaly_names.items():
        if phrase in lower:
            if glyph not in anomalies:
                anomalies.append(glyph)
    return anomalies


def translate_from_english(text: str) -> str:
    """Render an English sentence as a best-effort Ontos statement.

    This is a sketch translator: it spots entities, layers, and relational
    verbs, then composes a fully-parenthesized Ontos expression. The output is
    always grammatical; when the input is too vague to map, it returns a
    Gödelian acknowledgement.
    """

    text = text.strip()
    if not text:
        return ""

    lower = text.lower()

    # Gather entities mentioned.
    entities: list[str] = []
    for kw, glyph in _ENTITY_KEYWORDS:
        if kw in lower and glyph not in entities:
            entities.append(glyph)

    # Gather layers mentioned.
    layers: list[str] = []
    for kw, glyph in _LAYER_KEYWORDS:
        if kw in lower and glyph not in layers:
            layers.append(glyph)

    # Gather anomalies.
    anomalies = _find_anomalies(text)

    # Decide the operator from verbs.
    op = "→"  # default: implies
    for verb in _IMPLY_VERBS:
        if verb in lower:
            op = "→"
            break
    else:
        for verb in _AND_VERBS:
            if verb in lower:
                op = "∧"
                break

    # Compose. Prefer: [layer] (entity -> anomaly -> entity ...)
    atoms = entities + anomalies
    if not atoms:
        # Nothing recognizable -> Gödelian acknowledgement.
        return "⏅(Ontos) ∧ (Ontos → ⏄)"

    # Build a left-folded implication chain, fully parenthesized.
    if len(atoms) == 1:
        body = atoms[0]
    else:
        body = atoms[0]
        for nxt in atoms[1:]:
            body = f"({body} {op} {nxt})"

    if layers:
        # Scope under the first layer mentioned.
        return f"[{layers[0]}] ({body})"
    return body


def summarize_story(text: str) -> NavigatorOutput:
    """Read a story summary and emit Ontos statements + a Navigator report.

    This is the 'Navigator' bridge: it takes free-form English prose (a story
    beat, a session recap, a lore fragment) and distills it into the precision
    language. Each sentence becomes a best-effort Ontos statement; the whole
    text yields a structured :class:`NavigatorOutput`.
    """

    text = text.strip()
    if not text:
        return NavigatorOutput(summary="(empty input)")

    # Split into sentences on . ! ?
    sentences = [s.strip() for s in _re.split(r"[.!?]+", text) if s.strip()]

    out = NavigatorOutput()
    seen_entities: set[str] = set()
    seen_layers: set[str] = set()
    seen_anomalies: set[str] = set()

    for sentence in sentences:
        # Collect entities/layers/anomalies across the whole text.
        for kw, glyph in _ENTITY_KEYWORDS:
            if kw in sentence.lower() and glyph not in seen_entities:
                seen_entities.add(glyph)
                out.entities.append(glyph)
        for kw, glyph in _LAYER_KEYWORDS:
            if kw in sentence.lower() and glyph not in seen_layers:
                seen_layers.add(glyph)
                out.layers.append(glyph)
        for a in _find_anomalies(sentence):
            if a not in seen_anomalies:
                seen_anomalies.add(a)
                out.anomalies.append(a)

        stmt = translate_from_english(sentence)
        if stmt:
            out.statements.append(stmt)

    # Compose a one-line summary.
    parts = []
    if out.entities:
        parts.append(", ".join(out.entities))
    if out.layers:
        parts.append("in " + " / ".join(out.layers))
    if out.anomalies:
        parts.append("encountering " + ", ".join(out.anomalies))
    out.summary = " — ".join(parts) if parts else "no recognizable actors or layers found"

    return out
