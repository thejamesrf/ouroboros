"""The 90-Day Foundational Habits Program.

A structured habit-stacking program that builds the lifestyle foundation under
the training: morning/evening routines, daily movement, nutrition, and a gradual
buildup from one to two movement sessions per day. The 90 days close with a
daily progress photo and a 48-hour fast.

Habits are scored per day (0-100%) as a weighted average of habit completion.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Habit:
    """A single habit with a display name and scoring weight."""

    name: str
    weight: float = 1.0          # relative weight in the daily score
    description: str | None = None


@dataclass(frozen=True)
class HabitGroup:
    """A named cluster of habits (e.g. the morning routine)."""

    name: str
    habits: list[Habit]


# --- Morning routine (minimum) -------------------------------------------

MORNING_ROUTINE = HabitGroup(
    name="Morning Routine (Minimum)",
    habits=[
        Habit("Meditation 10+ min", weight=1.5, description="Sit, breathe, settle."),
        Habit("Drink a glass of water"),
        Habit("Brush teeth"),
        Habit("Make a to-do list"),
        Habit("Write goals"),
    ],
)

# --- Daily habits ---------------------------------------------------------

DAILY_HABITS = HabitGroup(
    name="Daily Habits",
    habits=[
        Habit("Drink 1 gallon of water", weight=1.5),
        Habit(
            "4-Day Holistic Wellness Cycle",
            weight=2.0,
            description=(
                "2x movement sessions/day: 1x 30+ min, 1x 45+ min outdoors, "
                "Zone 2 or RPE 8+. Day 1 resistance (6 fundamentals, splittable), "
                "Day 2 cardio (LISS→threshold→LISS→fartlek), Day 3 active recovery, "
                "Day 4 explosive/ballistic/functional/bodyweight/outdoor."
            ),
        ),
        Habit("Follow one diet (Kauffmann/Paleo/Whole30), minimize processed foods", weight=1.5),
        Habit("No phone/social media in bed"),
    ],
)

# --- Evening routine (minimum) -------------------------------------------

EVENING_ROUTINE = HabitGroup(
    name="Evening Routine (Minimum)",
    habits=[
        Habit("Review to-do list"),
        Habit("Write goals"),
        Habit("Read a real book 15 min (alternate fiction/non-fiction)"),
        Habit("Wind-down or tapping meditation", weight=1.5),
    ],
)

# --- The full program -----------------------------------------------------

NINETY_DAY_PROGRAM: list[HabitGroup] = [
    MORNING_ROUTINE,
    DAILY_HABITS,
    EVENING_ROUTINE,
]


def all_habits() -> list[Habit]:
    """Flat list of every habit in the 90-day program."""

    out: list[Habit] = []
    for group in NINETY_DAY_PROGRAM:
        out.extend(group.habits)
    return out


def habit_score(completed: dict[str, bool]) -> float:
    """Daily score (0-100%) as a weighted average of habit completion.

    `completed` maps a habit name to whether it was done today. Unknown names
    are ignored so members can log a subset.
    """

    habits = all_habits()
    total_weight = sum(h.weight for h in habits)
    if total_weight <= 0:
        return 0.0
    earned = sum(h.weight for h in habits if completed.get(h.name, False))
    return earned / total_weight * 100.0


def habit_streak(daily_scores: list[float], *, threshold: float = 80.0) -> int:
    """Current streak of days scoring at or above `threshold`."""

    streak = 0
    for score in reversed(daily_scores):
        if score >= threshold:
            streak += 1
        else:
            break
    return streak


# --- Gradual buildup guidance ---------------------------------------------

@dataclass(frozen=True)
class BuildupPhase:
    """A phase of the gradual buildup from 1 to 2 movement sessions/day."""

    weeks: str
    focus: str
    sessions_per_day: int


BUILDUP_PHASES: list[BuildupPhase] = [
    BuildupPhase(
        weeks="Weeks 1-4",
        focus="1 movement session/day (30+ min primary focus).",
        sessions_per_day=1,
    ),
    BuildupPhase(
        weeks="Weeks 5-8",
        focus="Add a second session (15-20 min Zone 2 or mobility) as capacity improves.",
        sessions_per_day=2,
    ),
    BuildupPhase(
        weeks="Weeks 9-12",
        focus="Full 2-session days; scale habits incrementally. Daily progress photo.",
        sessions_per_day=2,
    ),
    BuildupPhase(
        weeks="End of 90 Days",
        focus="Complete a 48-hour fast to close the program.",
        sessions_per_day=2,
    ),
]
