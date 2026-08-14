"""The Ouroboros command-line interface.

    ouroboros validate "STATEMENT"       check an Ontos statement's validity
    ouroboros golden                     run the grammar.md golden test cases
    ouroboros translate "STATEMENT"      gloss an Ontos statement into English
    ouroboros anomaly [--layer L] [-n N] forge anomalies for a session
    ouroboros realm                      print the canonical Labyrinth of Eternity
    ouroboros demo                       run everything end-to-end
"""

from __future__ import annotations

import argparse
import sys

from ouroboros.anomalies import LAYERS, generate_batch, canonical_anomaly
from ouroboros.ontos import GOLDEN_CASES, generate_statement, validate_statement
from ouroboros.realms import canonical_realm
from ouroboros.translate import translate_to_english


def cmd_validate(args: argparse.Namespace) -> int:
    result = validate_statement(args.statement)
    status = "✅ VALID" if result.valid else "❌ INVALID"
    print(f"{status}  {args.statement}")
    for e in result.errors:
        loc = f" (pos {e.position})" if e.position >= 0 else ""
        print(f"  [{e.rule}] {e.message}{loc}")
    for w in result.warnings:
        print(f"  ⚠️  {w}")
    return 0 if result.valid else 1


def cmd_golden(args: argparse.Namespace) -> int:
    """Run every golden case from grammar.md and report pass/fail."""

    failures = 0
    for statement, expected in GOLDEN_CASES.items():
        result = validate_statement(statement)
        ok = result.valid == expected
        mark = "✅" if ok else "❌"
        verdict = "valid" if result.valid else "invalid"
        print(f"{mark} expected={'valid' if expected else 'invalid'} got={verdict:>7}  {statement}")
        if not ok:
            failures += 1
            for e in result.errors:
                print(f"     [{e.rule}] {e.message}")
    print(f"\n{len(GOLDEN_CASES) - failures}/{len(GOLDEN_CASES)} golden cases passed")
    return 1 if failures else 0


def cmd_translate(args: argparse.Namespace) -> int:
    print(translate_to_english(args.statement))
    return 0


def cmd_anomaly(args: argparse.Namespace) -> int:
    if args.canonical:
        print(canonical_anomaly().render())
        return 0
    anomalies = generate_batch(n=args.count, layer=args.layer, seed=args.seed)
    for a in anomalies:
        print(a.render())
    return 0


def cmd_realm(args: argparse.Namespace) -> int:
    realm = canonical_realm()
    print(realm.to_json())
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    """Run the whole stack end-to-end."""

    print("=" * 64)
    print("🜲 The Ouroboros Project — toolchain demo")
    print("=" * 64)

    # 1. Ontos validation against the grammar's golden cases.
    print("\n[1] Ontos validator — golden cases from grammar.md")
    sample = "∀x ((x ∈ λ_Debug) → (∃y (y = ⚡_EchoingDoor)))"
    r = validate_statement(sample)
    print(f"  {sample}")
    print(f"  -> {'valid' if r else 'invalid'}")

    # 2. Generate a guaranteed-valid statement and validate it.
    print("\n[2] Ontos generator — one fresh statement, self-validated")
    stmt = generate_statement()
    print(f"  generated: {stmt}")
    print(f"  validates: {bool(validate_statement(stmt))}")

    # 3. Translate the canonical Hidden-Gods Ontos scenario to English.
    print("\n[3] Ontos → English translator")
    scenario = "[λ_Debug] (𝒫_Alice → (⚡_EchoingDoor → (𝒢_Architect → ⚡_NewAnomaly)))"
    print(f"  {scenario}")
    print(f"  -> {translate_to_english(scenario)}")

    # 4. Anomaly Forge.
    print("\n[4] Anomaly Forge — two anomalies, Debug layer")
    for a in generate_batch(n=2, layer="Debug", seed=7):
        print(a.render(), end="")

    # 5. Realm loader.
    print("\n[5] Realm loader — The Labyrinth of Eternity")
    realm = canonical_realm()
    print(f"  {realm.name} ({realm.type})")
    print(f"  location: {realm.location.realm} — {realm.location.coordinates}")
    print(f"  purpose:  {realm.purpose.function}")
    print(f"  language: {realm.essence.primary_language}")

    print("\n" + "=" * 64)
    print("🜲 Creation as connection > mechanics.")
    print("=" * 64)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="ouroboros",
        description="The Ouroboros Project — Ontos, anomalies, and realms.",
    )
    sub = p.add_subparsers(dest="command", required=True)

    v = sub.add_parser("validate", help="Validate a single Ontos statement.")
    v.add_argument("statement", help="the Ontos statement to check")
    v.set_defaults(func=cmd_validate)

    g = sub.add_parser("golden", help="Run the grammar.md golden test cases.")
    g.set_defaults(func=cmd_golden)

    t = sub.add_parser("translate", help="Gloss an Ontos statement into English.")
    t.add_argument("statement", help="the Ontos statement to translate")
    t.set_defaults(func=cmd_translate)

    a = sub.add_parser("anomaly", help="Forge anomalies for a Hidden Gods session.")
    a.add_argument("--layer", default=None, help=f"layer name: {list(LAYERS)}")
    a.add_argument("-n", "--count", type=int, default=1, help="how many anomalies to forge")
    a.add_argument("--seed", type=int, default=None, help="seed for reproducibility")
    a.add_argument("--canonical", action="store_true", help="print the README reference anomaly")
    a.set_defaults(func=cmd_anomaly)

    r = sub.add_parser("realm", help="Print the canonical Labyrinth of Eternity realm.")
    r.set_defaults(func=cmd_realm)

    d = sub.add_parser("demo", help="Run the whole toolchain end-to-end.")
    d.set_defaults(func=cmd_demo)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
