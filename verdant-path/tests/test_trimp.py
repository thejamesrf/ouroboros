"""Tests for TRIMP scoring."""

from verdant_path.tracker import SetLog
from verdant_path.trimp import (
    FOUNDATION_WEEKLY_TRIMP_RANGE,
    TRIMP,
    trimp_for_session,
    trimp_level,
    weekly_trimp,
    weekly_trimp_status,
)


def test_levels_clamp():
    assert trimp_level(0) is TRIMP.LOW
    assert trimp_level(1) is TRIMP.LOW
    assert trimp_level(2) is TRIMP.MEDIUM
    assert trimp_level(3) is TRIMP.HIGH
    assert trimp_level(99) is TRIMP.HIGH


def test_explicit_override_wins():
    sets = [SetLog(rpe=9.5)]  # would estimate HIGH
    assert trimp_for_session(sets, assigned_level=TRIMP.LOW) is TRIMP.LOW


def test_estimate_from_peak_rpe():
    assert trimp_for_session([SetLog(rpe=9)]) is TRIMP.HIGH
    assert trimp_for_session([SetLog(rpe=7)]) is TRIMP.MEDIUM
    assert trimp_for_session([SetLog(rpe=4)]) is TRIMP.LOW


def test_empty_session_is_low():
    assert trimp_for_session([]) is TRIMP.LOW


def test_weekly_sum_and_status():
    total = weekly_trimp([TRIMP.HIGH, TRIMP.MEDIUM, TRIMP.LOW, TRIMP.MEDIUM])
    assert total == 8
    low, high = FOUNDATION_WEEKLY_TRIMP_RANGE
    assert low <= total <= high
    assert "foundation" in weekly_trimp_status(total)


def test_under_foundation_status():
    total = weekly_trimp([TRIMP.LOW])
    assert "under-foundation" in weekly_trimp_status(total)


def test_above_foundation_status():
    total = weekly_trimp([TRIMP.HIGH] * 5)  # 15
    assert "above foundation" in weekly_trimp_status(total)
