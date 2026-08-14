"""Ontos validator — checks Ontos statements for contradictions or invalid syntax.

This is a thin, dependency-free entry point that re-exports the canonical
implementation in the installed ``ouroboros`` package. Run it directly:

    python -m ontos_language.tools.validator "STATEMENT"
    python -m ontos_language.tools.validator --golden

The grammar rules enforced live in ``ouroboros.ontos`` and are documented in
``ontos-language/grammar.md``.
"""

from __future__ import annotations

import sys

from ouroboros.ontos import GOLDEN_CASES, validate_statement


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print('usage: validator "STATEMENT"  |  --golden')
        return 2
    if args[0] == "--golden":
        passed = 0
        for statement, expected in GOLDEN_CASES.items():
            result = validate_statement(statement)
            ok = result.valid == expected
            print(f"{'✅' if ok else '❌'} {statement}")
            passed += ok
        print(f"\n{passed}/{len(GOLDEN_CASES)} golden cases passed")
        return 0 if passed == len(GOLDEN_CASES) else 1
    result = validate_statement(" ".join(args))
    print("✅ valid" if result.valid else "❌ invalid")
    for e in result.errors:
        print(f"  [{e.rule}] {e.message}")
    return 0 if result.valid else 1


if __name__ == "__main__":
    sys.exit(main())
