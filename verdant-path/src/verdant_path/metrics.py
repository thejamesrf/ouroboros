"""Weekly and monthly review logic: ACWR, fatigue trends, deload cues.

The weekly review is the feedback loop of progressive oscillation. It compares
this week's training stress (TRIMP) against the recent average (ACWR) and reads
HRV trend to decide whether to push, hold, or deload.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta

from verdant_path.fatigue import Fatigue, fatigue_cue
from verdant_path.tracker import CheckIn, WorkoutLog
from verdant_path.trimp import TRIMP, weekly_trimp, weekly_trimp_status


@dataclass(frozen=True)
class WeeklySummary:
    """Aggregated review of one training week."""

    week_start: date
    week_end: date
    total_trimp: int
    trimp_status: str
    avg_hrv: float
    avg_sleep: float
    avg_fatigue_percent: float
    fatigue_cue: Fatigue
    red_days: int                       # days at 🔴 fatigue
    acwr: float | None                  # acute:chronic workload ratio
    suggestion: str


def acwr(this_week_trimp: int, prior_weeks_trimp: list[int]) -> float | None:
    """Acute:chronic workload ratio.

    ACWR = this week's TRIMP / average of the prior weeks' TRIMP.
    Returns None if there is no history to compare against.
    """

    if not prior_weeks_trimp:
        return None
    chronic = sum(prior_weeks_trimp) / len(prior_weeks_trimp)
    if chronic <= 0:
        return None
    return this_week_trimp / chronic


def _week_range(day: date) -> tuple[date, date]:
    """Return the Mon-Sun week containing `day`."""

    start = day - timedelta(days=day.weekday())  # Monday=0
    return start, start + timedelta(days=6)


def weekly_review(
    week_of: date,
    checkins: list[CheckIn],
    logs: list[WorkoutLog],
    prior_weeks_trimp: list[int] | None = None,
    *,
    hrv_trend_down: bool = False,
) -> WeeklySummary:
    """Build a weekly summary with a deload suggestion.

    `prior_weeks_trimp` is the list of TRIMP totals for the preceding weeks
    (most recent last), used to compute ACWR. `hrv_trend_down` lets the caller
    encode an observed downward HRV trend from wearable data.
    """

    start, end = _week_range(week_of)
    week_checkins = [c for c in checkins if start <= c.day <= end]
    week_logs = [w for w in logs if start <= w.day <= end]

    trimp_total = weekly_trimp([w.session_trimp() for w in week_logs])
    trimp_status = weekly_trimp_status(trimp_total)

    avg_hrv = (
        sum(c.hrv for c in week_checkins) / len(week_checkins)
        if week_checkins
        else 0.0
    )
    avg_sleep = (
        sum(c.sleep_hours for c in week_checkins) / len(week_checkins)
        if week_checkins
        else 0.0
    )
    fatigue_pcts = [c.fatigue_percent() for c in week_checkins]
    avg_fatigue = sum(fatigue_pcts) / len(fatigue_pcts) if fatigue_pcts else 0.0
    cue = fatigue_cue(avg_fatigue) if fatigue_pcts else Fatigue.GREEN

    red_days = sum(1 for c in week_checkins if c.cue() is Fatigue.RED)

    ratio = acwr(trimp_total, prior_weeks_trimp or [])
    suggestion = _deload_suggestion(ratio, hrv_trend_down, red_days, cue)

    return WeeklySummary(
        week_start=start,
        week_end=end,
        total_trimp=trimp_total,
        trimp_status=trimp_status,
        avg_hrv=avg_hrv,
        avg_sleep=avg_sleep,
        avg_fatigue_percent=avg_fatigue,
        fatigue_cue=cue,
        red_days=red_days,
        acwr=ratio,
        suggestion=suggestion,
    )


def _deload_suggestion(
    ratio: float | None,
    hrv_trend_down: bool,
    red_days: int,
    cue: Fatigue,
) -> str:
    """Decide whether to push, hold, or deload for the coming week."""

    if red_days >= 3:
        return "🔴 fatigue 3+ days this week — consider a deload week."
    if ratio is not None and ratio > 1.5 and hrv_trend_down:
        return "ACWR > 1.5 with HRV trending down — consider a deload week."
    if ratio is not None and ratio > 1.5:
        return "ACWR > 1.5 — hold volume steady; watch readiness closely."
    if ratio is not None and 0.8 <= ratio <= 1.2 and not hrv_trend_down:
        return "ACWR ≈ 1.0 with HRV stable/↑ — progressive load OK."
    if cue is Fatigue.RED:
        return "Average fatigue is high — prioritize recovery next week."
    return "Stable week — continue progressive oscillation."
