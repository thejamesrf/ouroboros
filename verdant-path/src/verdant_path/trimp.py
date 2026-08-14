"""TRIMP — Training Impulse scoring on a subjective 1-3 scale.

TRIMP is Verdant Path's unit of training stress. A foundation week targets
8-12 TRIMP. The scale intentionally coarse-grained to stay grounded in embodied
awareness rather than false precision:

    1 (Low)    — recovery / Zone 2 (walking, mobility)
    2 (Medium) — moderate training (normal gym session)
    3 (High)   — heavy / CNS-demanding (HIIT, heavy lifts)
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum

# Foundation weekly TRIMP range — the floor of sustainable resilience work.
FOUNDATION_WEEKLY_TRIMP_RANGE = (8, 12)


class TRIMP(IntEnum):
    """Subjective training-stress levels."""

    LOW = 1      # recovery / Zone 2
    MEDIUM = 2   # moderate training
    HIGH = 3     # heavy / CNS-demanding

    @property
    def label(self) -> str:
        return {1: "Low", 2: "Medium", 3: "High"}[int(self)]


def trimp_level(value: int) -> TRIMP:
    """Coerce an integer (1-3) into a TRIMP level.

    Values below 1 clamp to LOW; values above 3 clamp to HIGH. This keeps
    accidental out-of-range entries from crashing a training log.
    """

    if value <= 1:
        return TRIMP.LOW
    if value >= 3:
        return TRIMP.HIGH
    return TRIMP.MEDIUM


@dataclass(frozen=True)
class SetLog:  # noqa: F811 — re-exported from tracker for convenience
    """A single logged set: the raw unit of a training session."""

    load: float | None = None
    reps: int | None = None
    tempo: str | None = None       # e.g. "3010"
    rpe: float | None = None       # 1-10 perceived exertion
    rest_sec: int | None = None
    notes: str | None = None


def trimp_for_session(sets: list[SetLog], assigned_level: TRIMP | None = None) -> TRIMP:
    """Estimate a session's TRIMP from logged sets, with an explicit override.

    Trainers often assign an intended TRIMP level when planning; members can
    override it after training based on how the body actually responded
    (embodied awareness over prescribed intent). If no override is given, we
    estimate from the heaviest RPE recorded.
    """

    if assigned_level is not None:
        return assigned_level

    if not sets:
        return TRIMP.LOW

    peak_rpe = max((s.rpe for s in sets if s.rpe is not None), default=0.0)
    if peak_rpe >= 8.5:
        return TRIMP.HIGH
    if peak_rpe >= 6.0:
        return TRIMP.MEDIUM
    return TRIMP.LOW


def weekly_trimp(levels: list[TRIMP]) -> int:
    """Sum TRIMP levels across a week's sessions."""

    return sum(int(level) for level in levels)


def weekly_trimp_status(total: int) -> str:
    """Human-readable status for a weekly TRIMP total."""

    low, high = FOUNDATION_WEEKLY_TRIMP_RANGE
    if total < low:
        return f"under-foundation ({total}/{low}-{high}): consider a bit more volume"
    if total <= high:
        return f"foundation range ({total}/{low}-{high}): sustainable"
    return f"above foundation ({total}/{low}-{high}): watch recovery cues"
