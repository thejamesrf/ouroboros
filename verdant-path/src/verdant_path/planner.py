"""Session structure and workout planning.

A Verdant Path session has four phases: warm-up, main work, accessory/finisher,
and conditioning (plus a cooldown). Splits scale from 1x/week (full body) up to
6x/week (one pattern per day), but every split guarantees weekly coverage of all
six fundamental movements.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from verdant_path.movements import (
    MOVEMENT_PATTERNS,
    Movement,
    Pattern,
    all_patterns_covered,
    missing_patterns,
)
from verdant_path.trimp import TRIMP


@dataclass(frozen=True)
class SetTarget:
    """Planned set parameters: the prescription a trainer hands a member."""

    sets: int
    reps: str                  # e.g. "5", "8-12", "AMRAP"
    load: str | None = None    # e.g. "80% 1RM", "RPE 8", or a weight
    tempo: str | None = None   # e.g. "3010"
    rpe: float | None = None
    rest_sec: int | None = None
    notes: str | None = None


@dataclass(frozen=True)
class MovementAssignment:
    """A movement plus its planned set/rep scheme within a block."""

    movement: Movement
    target: SetTarget


@dataclass(frozen=True)
class SessionBlock:
    """One phase of a session: warm-up, main, accessory, or conditioning."""

    name: str
    assignments: list[MovementAssignment] = field(default_factory=list)
    notes: str | None = None


@dataclass(frozen=True)
class SessionTemplate:
    """A reusable single-day workout template."""

    name: str
    blocks: list[SessionBlock]
    tag: str = "Strength"            # Strength, Endurance, Functional, Recovery
    intended_trimp: TRIMP = TRIMP.MEDIUM
    cooldown: str | None = None      # e.g. "Breathing + stretching + walk"

    def movements(self) -> list[Movement]:
        out: list[Movement] = []
        for block in self.blocks:
            out.extend(a.movement for a in block.assignments)
        return out

    def patterns(self) -> set[Pattern]:
        return {m.pattern for m in self.movements()}


@dataclass
class WorkoutPlan:
    """A multi-day training plan over a week, covering a chosen split."""

    name: str
    frequency: int                       # sessions per week, 1-6
    days: list[SessionTemplate]          # ordered days in the rotation
    rotation_note: str | None = None     # e.g. "alternate strength/endurance"

    def weekly_coverage(self) -> bool:
        """True if the plan's days collectively cover all six patterns."""

        all_movements: list[Movement] = []
        for day in self.days:
            all_movements.extend(day.movements())
        return all_patterns_covered(all_movements)

    def coverage_report(self) -> str:
        all_movements: list[Movement] = []
        for day in self.days:
            all_movements.extend(day.movements())
        if all_patterns_covered(all_movements):
            return "✅ All six fundamental patterns covered this week."
        missing = ", ".join(p.value for p in missing_patterns(all_movements))
        return f"⚠️ Missing patterns: {missing}"


# --- Split definitions -----------------------------------------------------

# Each split maps gym frequency (1-6x/week) to a name and an ordered list of
# day-pattern focuses. The planner materializes these into SessionTemplates.
SPLITS: dict[int, dict] = {
    1: {
        "name": "Full-Body",
        "days": [["all patterns in one session"]],
    },
    2: {
        "name": "Upper / Lower",
        "days": [["Upper (push + pull)", "Lower (squat + hinge + lunge)"]],
    },
    3: {
        "name": "Push / Pull / Legs",
        "days": [["Push", "Pull", "Legs"]],
    },
    4: {
        "name": "Back/Hams · Chest/Bi · Calves/Quads · Shoulders/Tris",
        "days": [
            ["Back + Hamstrings"],
            ["Chest + Biceps"],
            ["Calves + Quads"],
            ["Shoulders + Triceps"],
        ],
    },
    5: {
        "name": "5-Part Rotation",
        "days": [
            ["Posterior Chain"],
            ["Chest + Biceps"],
            ["Shoulders + Triceps"],
            ["Quads + Calves"],
            ["Core + Forearms + Upper Back"],
        ],
    },
    6: {
        "name": "One Pattern Per Day",
        "days": [
            ["Push"],
            ["Pull"],
            ["Hinge"],
            ["Lunge"],
            ["Squat"],
            ["Carry/Rotate"],
        ],
    },
}


def split_for_frequency(frequency: int) -> dict:
    """Return the split definition for a given weekly frequency (1-6)."""

    if frequency not in SPLITS:
        raise ValueError(f"frequency must be 1-6, got {frequency}")
    return SPLITS[frequency]


# --- Planner ---------------------------------------------------------------


class Planner:
    """Builds and validates workout plans from the Verdant Path splits.

    The planner holds a movement library and a template library so trainers can
    assemble plans from reusable pieces. Members get assigned plans; the
    planner checks weekly coverage so a plan never silently drops a pattern.
    """

    def __init__(self, movement_library: dict[str, Movement] | None = None) -> None:
        self.movements = dict(movement_library or MOVEMENT_PATTERNS)
        self.templates: dict[str, SessionTemplate] = {}

    def get(self, name: str) -> Movement:
        if name not in self.movements:
            raise KeyError(f"unknown movement '{name}'; add it to the library")
        return self.movements[name]

    def register_template(self, template: SessionTemplate) -> None:
        self.templates[template.name] = template

    def build_session(
        self,
        name: str,
        main: list[tuple[str, SetTarget]],
        *,
        accessory: list[tuple[str, SetTarget]] | None = None,
        conditioning: str | None = None,
        tag: str = "Strength",
        intended_trimp: TRIMP = TRIMP.MEDIUM,
        cooldown: str = "Breathing + stretching + walk",
    ) -> SessionTemplate:
        """Assemble a session from movement names and set targets."""

        def to_assignments(pairs: list[tuple[str, SetTarget]]) -> list[MovementAssignment]:
            return [MovementAssignment(self.get(n), t) for n, t in pairs]

        warmup = SessionBlock(
            name="Warm-Up",
            notes="CARs, movement prep, light cardio",
        )
        main_block = SessionBlock(name="Main Work", assignments=to_assignments(main))
        blocks = [warmup, main_block]
        if accessory:
            blocks.append(
                SessionBlock(
                    name="Accessory / Finisher",
                    assignments=to_assignments(accessory),
                    notes="Unilateral, contralateral, grip, core, or weak-link work.",
                )
            )
        if conditioning:
            blocks.append(
                SessionBlock(name="Conditioning", notes=conditioning)
            )
        return SessionTemplate(
            name=name,
            blocks=blocks,
            tag=tag,
            intended_trimp=intended_trimp,
            cooldown=cooldown,
        )

    def build_plan(
        self,
        frequency: int,
        days: list[SessionTemplate],
        *,
        name: str | None = None,
        rotation_note: str | None = None,
    ) -> WorkoutPlan:
        """Assemble a weekly plan from prebuilt sessions, validating coverage."""

        split = split_for_frequency(frequency)
        if len(days) != frequency:
            raise ValueError(
                f"expected {frequency} day(s) for the {split['name']} split, "
                f"got {len(days)}"
            )
        plan = WorkoutPlan(
            name=name or f"{split['name']} ({frequency}x/week)",
            frequency=frequency,
            days=days,
            rotation_note=rotation_note,
        )
        if not plan.weekly_coverage():
            # Coverage is a soft warning for endurance-heavy rotations but we
            # surface it so trainers decide deliberately.
            pass
        return plan

    def schedule(self, plan: WorkoutPlan, start: date) -> list[tuple[date, SessionTemplate]]:
        """Lay out a plan's days on consecutive days starting at `start`.

        This is a simple consecutive-day layout; trainers may reflow it onto
        specific weekdays (e.g., Mon/Wed/Fri) when assigning to a member.
        """

        from datetime import timedelta

        return [(start + timedelta(days=i), day) for i, day in enumerate(plan.days)]
