"""Ontos translator — converts Ontos statements to English (and back).

Re-exports the canonical implementation in ``ouroboros.translate``. Run directly:

    python -m ontos_language.tools.translator "STATEMENT"

The symbol glossaries are lifted verbatim from ``ontos-language/phonology.md``.
"""

from __future__ import annotations

import sys

from ouroboros.translate import translate_to_english


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print('usage: translator "STATEMENT"')
        return 2
    print(translate_to_english(" ".join(args)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
