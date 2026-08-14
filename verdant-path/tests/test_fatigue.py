"""Tests for fatigue scoring and readiness auto-regulation."""

from verdant_path.fatigue import (
    Fatigue,
    fatigue_cue,
    fatigue_from_checkin,
    readiness_adjustment,
)


def test_low_fatigue_is_green():
    # Well rested, low soreness, good HRV relative to baseline.
    pct = fatigue_from_checkin(energy=5, mood=5, soreness=1, sleep_hours=8, hrv=60)
    assert pct < 40
    assert fatigue_cue(pct) is Fatigue.GREEN


def test_high_fatigue_is_red():
    # Exhausted, very sore, poor sleep, low HRV.
    pct = fatigue_from_checkin(energy=1, mood=1, soreness=5, sleep_hours=2, hrv=30)
    assert pct >= 70
    assert fatigue_cue(pct) is Fatigue.RED


def test_medium_fatigue_is_amber():
    # The spec example: Energy=4 Mood=3 Soreness=2 Sleep=7 HRV=55 → 🟠.
    pct = fatigue_from_checkin(energy=4, mood=3, soreness=2, sleep_hours=7, hrv=55)
    assert 40 <= pct < 70
    assert fatigue_cue(pct) is Fatigue.AMBER


def test_cue_boundaries():
    assert fatigue_cue(0) is Fatigue.GREEN
    assert fatigue_cue(39.9) is Fatigue.GREEN
    assert fatigue_cue(40) is Fatigue.AMBER
    assert fatigue_cue(69.9) is Fatigue.AMBER
    assert fatigue_cue(70) is Fatigue.RED
    assert fatigue_cue(100) is Fatigue.RED


def test_higher_soreness_raises_fatigue():
    low = fatigue_from_checkin(5, 5, 1, 8, 50)
    high = fatigue_from_checkin(5, 5, 5, 8, 50)
    assert high > low


def test_readiness_green_no_change():
    adj = readiness_adjustment(10.0)
    assert adj.cue is Fatigue.GREEN
    assert adj.volume_change == 0.0


def test_readiness_amber_cuts_volume():
    adj = readiness_adjustment(50.0)
    assert adj.cue is Fatigue.AMBER
    assert adj.volume_change < 0
    assert "technique" in adj.note.lower()


def test_readiness_red_deep_cut():
    adj = readiness_adjustment(85.0)
    assert adj.cue is Fatigue.RED
    assert adj.volume_change <= -0.40


def test_fatigue_clamped_to_range():
    extreme = fatigue_from_checkin(1, 1, 5, 0, 0)
    assert 0 <= extreme <= 100
    perfect = fatigue_from_checkin(5, 5, 1, 9, 100)
    assert 0 <= perfect <= 100
