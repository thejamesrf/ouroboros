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
