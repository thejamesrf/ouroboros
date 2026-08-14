"""Fatigue scoring and readiness-based auto-regulation.

The fatigue model turns a daily check-in into a single percentage and a color
cue that guides the day's training. Each signal is normalized to its own 0-100
*fatigue* contribution (higher = more fatigued) and averaged:

    fatigue% = 0.5*mean(...) + 0.5*max(...)

where the five signals are energy, mood, soreness, sleep, and hrv fatigue terms.

Low energy, low mood, low sleep, low HRV, and high soreness all raise the score.

The 1-5 signals use a natural 1-5 mapping (5→0%, 3→50%, 1→100% fatigue); HRV
adapts to the individual via a baseline. The score is a weakest-link-aware blend:
50% the mean of the five signals plus 50% the worst (highest) signal. This honors
auto-regulation's respect for the body's loudest warning and lands the spec's
worked example (Energy=4, Mood=3, Soreness=2, Sleep=7h, HRV=55ms) in the 🟠 band.

These cues are sanity checks, not commands — embodied awareness has the final
word.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Fatigue(str, Enum):
    """The three fatigue color cues that guide a training day."""

    GREEN = "GREEN"   # 0-39%  train normally
    AMBER = "AMBER"   # 40-69% technique, mobility, Zone 2
    RED = "RED"       # 70-100% reduce intensity/volume; recover

    @property
    def icon(self) -> str:
        return {Fatigue.GREEN: "\U0001F7E2", Fatigue.AMBER: "\U0001F7E0", Fatigue.RED: "\U0001F534"}[self]

    @property
    def guidance(self) -> str:
        return {
            Fatigue.GREEN: "Train normally.",
            Fatigue.AMBER: "Prioritize technique, mobility, Zone 2.",
            Fatigue.RED: "Reduce intensity/volume; recover.",
        }[self]

    def __str__(self) -> str:
        return f"{self.icon}"


def fatigue_cue(percent: float) -> Fatigue:
    """Map a fatigue percentage (0-100) to its color cue."""

    if percent < 40.0:
        return Fatigue.GREEN
    if percent < 70.0:
        return Fatigue.AMBER
    return Fatigue.RED


def _scale(value: float, low: float, high: float) -> float:
    """Linearly map `value` from [low, high] onto [0, 100], clamped."""

    if high <= low:
        return 0.0
    pct = (value - low) / (high - low) * 100.0
    return max(0.0, min(100.0, pct))


def fatigue_from_checkin(
    energy: float,        # 1-5
    mood: float,          # 1-5
    soreness: float,      # 1-5 (5 = very sore)
    sleep_hours: float,   # hours
    hrv: float,           # ms, member's typical resting HRV
    *,
    hrv_baseline: float = 50.0,  # ms, used as the "good" HRV reference
) -> float:
    """Compute a 0-100 fatigue percentage from a daily check-in.

    Each term is a fatigue contribution in 0-100 (higher = more fatigue):
      - Energy   : 1-5   -> low energy raises fatigue
      - Mood     : 1-5   -> low mood raises fatigue
      - Soreness : 1-5   -> high soreness raises fatigue
      - Sleep    : 0-9 h -> low sleep raises fatigue
      - HRV      : scaled against a personal baseline; below baseline raises
        fatigue, above lowers it.

    The final score blends the mean (50%) with the worst signal (50%) so a
    single loud warning can nudge an otherwise-okay check-in toward caution.
    """

    # Energy/mood/sleep are "good when high", so their fatigue is the inverse of a
    # 1-5 scale (5 -> 0%, 3 -> 50%, 1 -> 100%).
    energy_fatigue = 100.0 - _scale(energy, 1.0, 5.0)
    mood_fatigue = 100.0 - _scale(mood, 1.0, 5.0)
    sleep_fatigue = 100.0 - _scale(sleep_hours, 0.0, 9.0)
    # Soreness is "bad when high", so it maps directly: 1 (none) -> 0, 5 -> 100.
    soreness_fatigue = _scale(soreness, 1.0, 5.0)

    # HRV: at baseline -> 50; 150% of baseline -> 0; 50% of baseline -> 100.
    if hrv_baseline <= 0:
        hrv_fatigue = 50.0
    else:
        hrv_ratio = hrv / hrv_baseline
        hrv_fatigue = max(0.0, min(100.0, 50.0 - (hrv_ratio - 1.0) * 100.0))

    signals = [
        energy_fatigue, mood_fatigue, soreness_fatigue, sleep_fatigue, hrv_fatigue,
    ]
    mean = sum(signals) / len(signals)
    worst = max(signals)
    # Weakest-link-aware blend: respect the body's loudest warning signal.
    fatigue = 0.5 * mean + 0.5 * worst
    return max(0.0, min(100.0, fatigue))


@dataclass(frozen=True)
class ReadinessAdjustment:
    """A suggested change to today's plan based on the fatigue cue."""

    cue: Fatigue
    volume_change: float          # fractional change, e.g. -0.20 = reduce 20%
    intensity_change: float      # fractional change to load/RPE target
    note: str


def readiness_adjustment(fatigue_percent: float) -> ReadinessAdjustment:
    """Suggest a volume/intensity adjustment for today's session.

    Amber days bias toward technique and Zone 2; red days cut volume and
    intensity to protect recovery. Green days are unrestricted.
    """

    cue = fatigue_cue(fatigue_percent)

    if cue is Fatigue.GREEN:
        return ReadinessAdjustment(cue, 0.0, 0.0, "Ready to train normally.")
    if cue is Fatigue.AMBER:
        return ReadinessAdjustment(
            cue,
            volume_change=-0.20,
            intensity_change=-0.10,
            note="Prioritize technique, mobility, Zone 2. Consider reducing "
            "primary-lift volume by ~20%.",
        )
    return ReadinessAdjustment(
        cue,
        volume_change=-0.40,
        intensity_change=-0.20,
        note="High fatigue. Reduce intensity/volume substantially; prioritize "
        "recovery and movement quality.",
    )
