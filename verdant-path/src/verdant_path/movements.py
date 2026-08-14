"""The six fundamental movement patterns.

Every Verdant Path program hits all six at least weekly, regardless of training
frequency. These are the non-negotiable movement roots of the system.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Pattern(str, Enum):
    """The six fundamental movement patterns."""

    PUSH = "push"
    PULL = "pull"
    HINGE = "hinge"
    LUNGE = "lunge"
    SQUAT = "squat"
    CARRY_ROTATE = "carry/rotate/anti-rotate"

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Movement:
    """A named exercise tagged with its primary movement pattern.

    The pattern drives weekly coverage checks; the movement is the concrete
    expression (e.g., a deadlift expresses the hinge pattern).
    """

    name: str
    pattern: Pattern
    # Accessory/finisher movements target weak links: unilateral, contralateral,
    # grip, core, or movement-specific support work.
    is_accessory: bool = False

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("movement name must not be empty")


# A working library of movements keyed by name. Trainers can extend this freely;
# these seed the template library with the lifts referenced in the spec.
MOVEMENT_PATTERNS: dict[str, Movement] = {
    # Push
    "bench_press": Movement("Bench Press", Pattern.PUSH),
    "overhead_press": Movement("Overhead Press", Pattern.PUSH),
    "dips": Movement("Dips", Pattern.PUSH),
    "lateral_raise": Movement("Lateral Raises", Pattern.PUSH, is_accessory=True),
    "push_up": Movement("Push-Up", Pattern.PUSH),
    # Pull
    "pull_up": Movement("Pull-Up", Pattern.PULL),
    "barbell_row": Movement("Barbell Row", Pattern.PULL),
    "cable_row": Movement("Cable Row", Pattern.PULL),
    "biceps_curl": Movement("Biceps Curl", Pattern.PULL, is_accessory=True),
    "face_pull": Movement("Face Pull", Pattern.PULL, is_accessory=True),
    # Hinge
    "deadlift": Movement("Deadlift", Pattern.HINGE),
    "romanian_deadlift": Movement("Romanian Deadlift", Pattern.HINGE),
    "back_extension": Movement("Back Extension", Pattern.HINGE, is_accessory=True),
    "kettlebell_swing": Movement("Kettlebell Swing", Pattern.HINGE),
    # Lunge
    "walking_lunge": Movement("Walking Lunge", Pattern.LUNGE),
    "bulgarian_split_squat": Movement("Bulgarian Split Squat", Pattern.LUNGE),
    "step_up": Movement("Step-Up", Pattern.LUNGE),
    # Squat
    "back_squat": Movement("Back Squat", Pattern.SQUAT),
    "front_squat": Movement("Front Squat", Pattern.SQUAT),
    "goblet_squat": Movement("Goblet Squat", Pattern.SQUAT),
    "leg_press": Movement("Leg Press", Pattern.SQUAT),
    "calf_raise": Movement("Calf Raise", Pattern.SQUAT, is_accessory=True),
    # Carry / rotate / anti-rotate
    "farmers_carry": Movement("Farmer's Carry", Pattern.CARRY_ROTATE),
    "suitcase_carry": Movement("Suitcase Carry", Pattern.CARRY_ROTATE),
    "pallof_press": Movement("Pallof Press", Pattern.CARRY_ROTATE, is_accessory=True),
    "plank": Movement("Plank", Pattern.CARRY_ROTATE, is_accessory=True),
    "hanging_leg_raise": Movement("Hanging Leg Raise", Pattern.CARRY_ROTATE, is_accessory=True),
    "forearm_curl": Movement("Forearm Curl", Pattern.CARRY_ROTATE, is_accessory=True),
}


def all_patterns_covered(movements: list[Movement]) -> bool:
    """Return True if every fundamental pattern appears at least once.

    This is the weekly-coverage invariant: a Verdant Path week that omits a
    pattern is incomplete by definition.
    """

    covered = {m.pattern for m in movements}
    return all(p in covered for p in Pattern)


def missing_patterns(movements: list[Movement]) -> list[Pattern]:
    """Patterns not yet hit by the given movements — for trainer feedback."""

    covered = {m.pattern for m in movements}
    return [p for p in Pattern if p not in covered]
