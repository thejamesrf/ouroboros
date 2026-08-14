#!/usr/bin/env python3
"""Ontos statement validator.

Checks Ontos statements for the structural rules described in
``grammar.md`` and ``phonology.md``:

- Non-atomic operations are explicitly grouped with parentheses.
- Every variable is bound by a quantifier (``forall``/``exists``) or a
  ``Let`` binding.
- No raw self-reference without the meta-symbol ``⣸`` (U+2378).

This is a deliberately minimal scaffold. It is *not* a complete parser; it
catches the most common violations and is meant to grow alongside the
language spec. See ``../grammar.md`` and ``../phonology.md`` for the rules.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field

# Symbols referenced throughout the language docs.
IMPLIES = "→"          # logical implication
AND = "∧"
OR = "∨"
NOT = "¬"
IFF = "↔"
FORALL = "∀"
EXISTS = "∃"
SELF_REF = "⣸"         # meta-symbol: marked self-reference
META_SYMBOLS = {"⢺", "⣽", "⣾", "⣸"}  # unknown, incomplete, paradox, self-ref

# Infix operators that, when used without surrounding parentheses, create
# ambiguity (per grammar.md Rule 1 and Rule 2).
INFIX_OPERATORS = (IMPLIES, AND, OR, IFF)


@dataclass
class ValidationResult:
    """Outcome of validating one or more Ontos statements."""

    valid: bool
    errors: list[str] = field(default_factory=list)


def _parentheses_balanced(statement: str) -> bool:
    """Return True if every ``(`` has a matching ``)``."""
    depth = 0
    for char in statement:
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def _explicit_grouping(statement: str) -> list[str]:
    """Flag statements with multiple infix operators and no parentheses.

    Per grammar.md, ``A ∧ B → C`` is ambiguous and invalid because it is
    unclear whether ``→`` applies to ``A`` or ``A ∧ B``.
    """
    errors: list[str] = []
    operator_count = sum(statement.count(op) for op in INFIX_OPERATORS)
    has_parens = "(" in statement or "[" in statement
    if operator_count > 1 and not has_parens:
        errors.append(
            "Ambiguous: multiple infix operators without explicit "
            "parentheses. Use parentheses to clarify grouping, e.g. "
            "'(A ∧ B) → C' rather than 'A ∧ B → C'."
        )
    return errors


def _variables_bound(statement: str) -> list[str]:
    """Flag free (unbound) lowercase variables.

    Variables must be bound by a quantifier (``∀``/``∃``) or a ``Let``
    binding. Single uppercase letters are treated as constants, not
    variables, following the convention in the examples.
    """
    errors: list[str] = []
    # Find all bare lowercase variable uses like `x` or `y`.
    tokens = re.findall(r"\b([a-z])\b", statement)
    bound: set[str] = set()
    for quantifier in (FORALL, EXISTS):
        for match in re.finditer(re.escape(quantifier) + r"\s*([a-z])", statement):
            bound.add(match.group(1))
    for match in re.finditer(r"Let\s+([a-z])\s*=", statement, re.IGNORECASE):
        bound.add(match.group(1))
    for token in tokens:
        if token not in bound:
            errors.append(
                f"Unbound variable '{token}': all variables must be bound "
                f"by a quantifier (∀/∃) or a 'Let' binding."
            )
    return errors


def _no_raw_self_reference(statement: str) -> list[str]:
    """Flag self-referential patterns not marked with the ``⣸`` symbol.

    A naive literal self-reference like ``A = A`` is allowed (it is not
    truly self-referential); genuine self-reference must use ``⣸``.
    """
    errors: list[str] = []
    # Heuristic: a token appearing as both sides of an assignment to itself
    # in a way that *isn't* a trivial identity is not enforced here; this
    # scaffold simply confirms the meta-symbol exists when needed.
    if "this statement" in statement.lower() and SELF_REF not in statement:
        errors.append(
            "Raw self-reference detected without the meta-symbol '⣸'. "
            "Mark self-referential statements explicitly, e.g. '⣸(A) = A'."
        )
    return errors


def validate(statement: str) -> ValidationResult:
    """Validate a single Ontos statement.

    Returns a :class:`ValidationResult` with ``valid=False`` and a list of
    human-readable errors if any rule is violated.
    """
    statement = statement.strip()
    errors: list[str] = []

    if not statement:
        return ValidationResult(valid=False, errors=["Empty statement."])

    if not _parentheses_balanced(statement):
        errors.append("Unbalanced parentheses: every '(' must have a matching ')'.")

    errors.extend(_explicit_grouping(statement))
    errors.extend(_variables_bound(statement))
    errors.extend(_no_raw_self_reference(statement))

    return ValidationResult(valid=not errors, errors=errors)


def main(argv: list[str] | None = None) -> int:
    """CLI entry point: validate statements passed as arguments or stdin."""
    args = argv if argv is not None else sys.argv[1:]
    statements = args or [line.strip() for line in sys.stdin if line.strip()]
    exit_code = 0
    for statement in statements:
        result = validate(statement)
        status = "✓ valid" if result.valid else "✗ invalid"
        print(f"{status}: {statement}")
        for error in result.errors:
            print(f"    - {error}")
        if not result.valid:
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
