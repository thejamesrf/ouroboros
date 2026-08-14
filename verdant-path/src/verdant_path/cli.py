"""Verdant Path command-line interface.

    verdant split 5            show the split for a given weekly frequency
    verdant checkin ...       log a daily check-in, get the fatigue cue
    verdant fatigue-check     interactive-ish readiness adjustment
    verdant weekly ...        build a weekly review from logged data
    verdant habits            list the 90-day foundational habits
    verdant demo              run the spec's example workflow end-to-end
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, timedelta

from verdant_path.fatigue import fatigue_cue, readiness_adjustment
from verdant_path.habits import BUILDUP_PHASES, NINETY_DAY_PROGRAM, habit_score
from verdant_path.metrics import weekly_review
from verdant_path.planner import SPLITS
from verdant_path.templates import default_planner
from verdant_path.tracker import CheckIn, JournalEntry, SetLog, WorkoutLog
from verdant_path.trimp import TRIMP, weekly_trimp_status


def _bar(pct: float, width: int = 20) -> str:
    filled = int(round(pct / 100 * width))
    return "[" + "█" * filled + "·" * (width - filled) + f"] {pct:0.1f}%"


def cmd_split(args: argparse.Namespace) -> int:
    freq = args.frequency
    if freq not in SPLITS:
        print(f"frequency must be 1-6, got {freq}")
        return 2
    split = SPLITS[freq]
    print(f"🌿 {split['name']}  ({freq}x/week)")
    for i, day in enumerate(split["days"], start=1):
        print(f"  Day {i}: {', '.join(day)}")
    return 0


def cmd_checkin(args: argparse.Namespace) -> int:
    from verdant_path.fatigue import fatigue_from_checkin

    pct = fatigue_from_checkin(
        args.energy, args.mood, args.soreness, args.sleep, args.hrv,
        hrv_baseline=args.hrv_baseline,
    )
    cue = fatigue_cue(pct)
    adj = readiness_adjustment(pct)
    print("🌿 Daily Check-In")
    print(f"  Energy={args.energy}/5  Mood={args.mood}/5  Soreness={args.soreness}/5")
    print(f"  Sleep={args.sleep}h  HRV={args.hrv}ms (baseline {args.hrv_baseline})")
    print(f"\n  Fatigue {_bar(pct)}")
    print(f"  Cue: {cue}  -> {cue.guidance}")
    print(f"  Suggested: {adj.note}")
    if adj.volume_change or adj.intensity_change:
        vol = adj.volume_change
        inten = adj.intensity_change
        vol_txt = f"reduce {-vol:.0%}" if vol < 0 else (f"increase {vol:.0%}" if vol > 0 else "hold")
        inten_txt = f"reduce {-inten:.0%}" if inten < 0 else (f"increase {inten:.0%}" if inten > 0 else "hold")
        print(f"  Volume: {vol_txt}   Intensity: {inten_txt}")
    return 0


def cmd_habits(args: argparse.Namespace) -> int:
    print("🌱 90-Day Foundational Habits Program\n")
    for group in NINETY_DAY_PROGRAM:
        print(f"## {group.name}")
        for h in group.habits:
            print(f"  • {h.name}" + (f" — {h.description}" if h.description else ""))
        print()

    # Demo a daily score from a sample completion set.
    sample = {
        "Meditation 10+ min": True,
        "Drink a glass of water": True,
        "Brush teeth": True,
        "Make a to-do list": True,
        "Write goals": True,
        "Drink 1 gallon of water": True,
        "4-Day Holistic Wellness Cycle": True,
        "Follow one diet (Kauffmann/Paleo/Whole30), minimize processed foods": True,
        "No phone/social media in bed": False,
        "Review to-do list": True,
        "Read a real book 15 min (alternate fiction/non-fiction)": True,
        "Wind-down or tapping meditation": False,
    }
    print("Example daily score (one day):")
    print(f"  {_bar(habit_score(sample))}")
    print("\n📅 Gradual Buildup")
    for phase in BUILDUP_PHASES:
        print(f"  {phase.weeks}: {phase.focus}")
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    """Run the spec's example workflow end-to-end."""

    print("=" * 64)
    print("🌿 Ouroboros Verdant Path — Example Workflow")
    print("=" * 64)

    # 1. Trainer builds a 5x/week resistance split.
    print("\n[1] Trainer builds a 5x/week plan")
    planner = default_planner()
    plan = planner.build_plan(
        frequency=5,
        days=[
            planner.templates["Posterior Chain"],
            planner.templates["LISS Run"],
            planner.templates["Chest + Biceps"],
            planner.templates["HIIT / Work-Capacity"],
            planner.templates["Shoulders + Triceps"],
        ],
        rotation_note="Mon/Wed/Fri resistance · Tue/Thu endurance · Sat active recovery",
    )
    print(f"  Plan: {plan.name}")
    print(f"  Rotation: {plan.rotation_note}")
    print(f"  {plan.coverage_report()}")
    for i, day in enumerate(plan.days):
        print(f"    Day {i+1}: {day.name}  [{day.tag}, TRIMP {int(day.intended_trimp)}]")

    # 2. Member checks in Monday AM and gets a fatigue cue.
    print("\n[2] Member Monday AM check-in")
    monday = date(2025, 1, 6)
    ci = CheckIn(monday, energy=4, mood=3, soreness=2, sleep_hours=7, hrv=55)
    pct = ci.fatigue_percent()
    adj = readiness_adjustment(pct)
    print(f"  Energy=4 Mood=3 Soreness=2 Sleep=7h HRV=55 → fatigue {_bar(pct)}")
    print(f"  Cue: {ci.cue()}  -> {adj.note}")

    # 3. Member adjusts, logs the session (TRIMP=2), journals.
    print("\n[3] Member logs the session and journals")
    deadlift = planner.get("deadlift")
    log = WorkoutLog(
        day=monday,
        movement=deadlift,
        sets=[
            SetLog(load=180, reps=3, rpe=8, tempo="3010", rest_sec=180),
            SetLog(load=190, reps=3, rpe=8.5, tempo="3010", rest_sec=180),
            SetLog(load=190, reps=3, rpe=9, tempo="3010", rest_sec=180),
        ],
        trimp=TRIMP.MEDIUM,
        notes="Reduced deadlift volume ~20% per readiness cue.",
    )
    journal = JournalEntry(
        monday,
        "Lower back tight — need more hip mobility.",
        tags=["#recovery", "#soreness"],
    )
    print(f"  {log.movement.name}: {len(log.sets)} sets, "
          f"TRIMP={int(log.session_trimp())} ({log.session_trimp().label})")
    print(f"  Journal: {journal.text}  tags={journal.tags}")

    # 4. End of week review.
    print("\n[4] End-of-week review")
    week_logs = [log]  # one logged session for the demo
    prior = [9, 10, 8]  # prior weeks' TRIMP totals
    summary = weekly_review(
        monday, [ci], week_logs, prior_weeks_trimp=prior, hrv_trend_down=True,
    )
    print(f"  Week of {summary.week_start} → {summary.week_end}")
    print(f"  Total TRIMP={summary.total_trimp}  ({summary.trimp_status})")
    print(f"  Avg HRV={summary.avg_hrv:0.0f}ms  Avg sleep={summary.avg_sleep:0.1f}h")
    print(f"  Avg fatigue={summary.avg_fatigue_percent:0.1f}%  cue={summary.fatigue_cue}")
    print(f"  ACWR={summary.acwr:.2f}" if summary.acwr else "  ACWR=n/a")
    print(f"  Suggestion: {summary.suggestion}")

    print("\n" + "=" * 64)
    print("🌿 Verdant Path: creation as connection > mechanics.")
    print("=" * 64)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="verdant",
        description="Ouroboros Verdant Path — resilience-focused training & wellness.",
    )
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("split", help="Show the training split for a weekly frequency.")
    s.add_argument("frequency", type=int, help="gym days per week (1-6)")
    s.set_defaults(func=cmd_split)

    c = sub.add_parser("checkin", help="Log a daily check-in and get the fatigue cue.")
    c.add_argument("--energy", type=float, required=True, help="1-5")
    c.add_argument("--mood", type=float, required=True, help="1-5")
    c.add_argument("--soreness", type=float, required=True, help="1-5 (5=very sore)")
    c.add_argument("--sleep", type=float, required=True, help="hours")
    c.add_argument("--hrv", type=float, required=True, help="ms")
    c.add_argument("--hrv-baseline", type=float, default=50.0, help="personal HRV baseline (ms)")
    c.set_defaults(func=cmd_checkin)

    h = sub.add_parser("habits", help="List the 90-day foundational habits program.")
    h.set_defaults(func=cmd_habits)

    d = sub.add_parser("demo", help="Run the example workflow end-to-end.")
    d.set_defaults(func=cmd_demo)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
