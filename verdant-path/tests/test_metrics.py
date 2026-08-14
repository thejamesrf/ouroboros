"""Tests for ACWR and the weekly review."""

from datetime import date, timedelta

from verdant_path.fatigue import Fatigue
from verdant_path.metrics import acwr, weekly_review
from verdant_path.movements import MOVEMENT_PATTERNS
from verdant_path.tracker import CheckIn, SetLog, WorkoutLog
from verdant_path.trimp import TRIMP


def test_acwr_no_history():
    assert acwr(10, []) is None
    assert acwr(10, [0, 0]) is None


def test_acwr_ratio():
    # 10 this week, 8 avg prior → 1.25
    assert acwr(10, [8, 8]) == 1.25


def test_deload_on_high_acwr_and_hrv_down():
    monday = date(2025, 1, 6)
    ci = CheckIn(monday, energy=4, mood=3, soreness=2, sleep_hours=7, hrv=52)
    mv = MOVEMENT_PATTERNS["deadlift"]
    log = WorkoutLog(
        monday, mv,
        sets=[SetLog(load=190, reps=3, rpe=9)],
        trimp=TRIMP.HIGH,
    )
    summary = weekly_review(monday, [ci], [log], prior_weeks_trimp=[1, 2], hrv_trend_down=True)
    assert summary.acwr is not None
    assert summary.acwr > 1.5
    assert "deload" in summary.suggestion.lower()


def test_progressive_load_when_stable():
    monday = date(2025, 1, 6)
    ci = CheckIn(monday, energy=5, mood=5, soreness=1, sleep_hours=8, hrv=60)
    mv = MOVEMENT_PATTERNS["bench_press"]
    log = WorkoutLog(monday, mv, sets=[SetLog(rpe=7)], trimp=TRIMP.MEDIUM)
    summary = weekly_review(monday, [ci], [log], prior_weeks_trimp=[2, 2, 2], hrv_trend_down=False)
    assert "progressive load" in summary.suggestion.lower()


def test_red_days_trigger_deload():
    monday = date(2025, 1, 6)
    # Three red check-ins across the week.
    checkins = [
        CheckIn(monday + timedelta(days=i), energy=1, mood=1, soreness=5, sleep_hours=2, hrv=30)
        for i in range(3)
    ]
    summary = weekly_review(monday, checkins, [], prior_weeks_trimp=[8], hrv_trend_down=False)
    assert summary.red_days >= 3
    assert "deload" in summary.suggestion.lower()


def test_week_range_filters_correctly():
    monday = date(2025, 1, 6)  # a Monday
    in_week = CheckIn(monday + timedelta(days=2), energy=4, mood=4, soreness=2, sleep_hours=7, hrv=55)
    out_week = CheckIn(monday + timedelta(days=10), energy=4, mood=4, soreness=2, sleep_hours=7, hrv=55)
    summary = weekly_review(monday, [in_week, out_week], [], prior_weeks_trimp=None)
    assert summary.week_start == monday
    assert summary.avg_hrv == in_week.hrv  # only the in-week check-in counted
