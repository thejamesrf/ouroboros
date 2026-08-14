"""Ontos generator — creates random Ontos statements and Hidden Gods content.

Re-exports the canonical implementation in ``ouroboros.ontos``. Run directly:

    python -m ontos_language.tools.generator [-n N] [--seed S]

Output is always grammatical and passes the validator.
"""

from __future__ import annotations

import argparse
import sys

from ouroboros.ontos import generate_batch


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Generate random valid Ontos statements.")
    p.add_argument("-n", "--count", type=int, default=1, help="how many statements")
    p.add_argument("--seed", type=int, default=None, help="seed for reproducibility")
    args = p.parse_args(argv)
    for stmt in generate_batch(args.count, seed=args.seed):
        print(stmt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
