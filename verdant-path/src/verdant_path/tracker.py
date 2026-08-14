"""Daily check-ins, workout logs, and journal entries.

These are the member-facing records: what they did, how they felt, and what they
noticed. They feed fatigue scoring, TRIMP totals, and weekly reviews.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from verdant_path.fatigue import fatigue_cue, fatigue_from_checkin
from verdant_path.movements import Movement
from verdant_path.trimp import TRIMP, trimp_for_session


@dataclass(frozen=True)
class SetLog:
    """A single logged set: the raw unit of a training session."""

    load: float | None = None
    reps: int | None = None
    tempo: str | None = None       # e.g. "3010"
    rpe: float | None = None       # 1-10 perceived exertion
    rest_sec: int | None = None
    notes: str | None = None


@dataclass
class WorkoutLog:
    """A member's completed session: movements, sets, and resulting TRIMP."""

    day: date
    movement: Movement
    sets: list[SetLog] = field(default_factory=list)
    trimp: TRIMP | None = None          # explicit override after the session
    notes: str | None = None

    def session_trimp(self, assigned_level: TRIMP | None = None) -> TRIMP:
        """Resolve the session's TRIMP: explicit override, else estimate."""

        if self.trimp is not None:
            return self.trimp
        return trimp_for_session(self.sets, assigned_level=assigned_level)


@dataclass
class CheckIn:
    """A daily check-in: the five signals that produce a fatigue score."""

    day: date
    energy: float          # 1-5
    mood: float            # 1-5
    soreness: float        # 1-5 (5 = very sore)
    sleep_hours: float     # hours
    hrv: float             # ms
    hrv_baseline: float = 50.0

    def fatigue_percent(self) -> float:
        return fatigue_from_checkin(
            self.energy,
            self.mood,
            self.soreness,
            self.sleep_hours,
            self.hrv,
            hrv_baseline=self.hrv_baseline,
        )

    def cue(self):
        return fatigue_cue(self.fatigue_percent())


@dataclass
class JournalEntry:
    """A free-form reflective note: pain, energy, mood, insights.

    Journaling is introspection — the embodied-awareness layer that gives the
    metrics their meaning. Tags keep entries retrievable over time.
    """

    day: date
    text: str
    tags: list[str] = field(default_factory=list)
    photo: str | None = None          # path or URI to a progress photo

    def __post_init__(self) -> None:
        # Normalize tags on construction so callers can pass "#Recovery" etc.
        normalized: list[str] = []
        for tag in self.tags:
            clean = tag.strip().lstrip("#").lower()
            if clean and clean not in normalized:
                normalized.append(clean)
        self.tags = normalized

    def add_tag(self, tag: str) -> None:
        clean = tag.strip().lstrip("#").lower()
        if clean and clean not in self.tags:
            self.tags.append(clean)
