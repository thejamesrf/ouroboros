"""Example: build and inspect a 5x/week Verdant Path plan.

Run with:  python examples/five_day_plan.py
"""

from datetime import date

from verdant_path import Planner, split_for_frequency
from verdant_path.templates import default_planner


def main() -> None:
    planner = default_planner()

    # Show the split definition for 5x/week.
    split = split_for_frequency(5)
    print(f"🌿 {split['name']} (5x/week)\n")

    # Assemble a plan from the default templates.
    plan = planner.build_plan(
        frequency=5,
        days=[
            planner.templates["Posterior Chain"],
            planner.templates["LISS Run"],
            planner.templates["Chest + Biceps"],
            planner.templates["HIIT / Work-Capacity"],
            planner.templates["Shoulders + Triceps"],
        ],
        rotation_note="Mon/Wed/Fri resistance · Tue/Thu endurance",
    )

    print(f"Plan: {plan.name}")
    print(f"Rotation: {plan.rotation_note}")
    print(plan.coverage_report())
    print()

    # Lay it out on consecutive days.
    for day, session in planner.schedule(plan, date(2025, 1, 6)):
        print(f"  {day}  {session.name}  [{session.tag}, TRIMP {int(session.intended_trimp)}]")
        for block in session.blocks:
            if block.assignments:
                names = ", ".join(a.movement.name for a in block.assignments)
                print(f"      {block.name}: {names}")
            elif block.notes:
                print(f"      {block.name}: {block.notes}")


if __name__ == "__main__":
    main()
