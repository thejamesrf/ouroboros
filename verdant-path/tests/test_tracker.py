"""Tests for tracker records: check-ins, workout logs, journal."""

from datetime import date

from verdant_path.movements import MOVEMENT_PATTERNS
from verdant_path.tracker import CheckIn, JournalEntry, SetLog, WorkoutLog
from verdant_path.fatigue import Fatigue
from verdant_path.trimp import TRIMP


def test_checkin_cue_matches_spec_example():
    ci = CheckIn(date(2025, 1, 6), energy=4, mood=3, soreness=2, sleep_hours=7, hrv=55)
    pct = ci.fatigue_percent()
    assert 40 <= pct < 70
    assert Fatigue.AMBER in ci.cue().value


def test_workout_log_uses_explicit_trimp():
    mv = MOVEMENT_PATTERNS["deadlift"]
    log = WorkoutLog(
        date(2025, 1, 6), mv,
        sets=[SetLog(load=190, reps=3, rpe=9)],
        trimp=TRIMP.MEDIUM,
    )
    assert log.session_trimp() is TRIMP.MEDIUM  # explicit override


def test_workout_log_estimates_trimp():
    mv = MOVEMENT_PATTERNS["deadlift"]
    log = WorkoutLog(date(2025, 1, 6), mv, sets=[SetLog(rpe=9.5)])
    assert log.session_trimp() is TRIMP.HIGH  # from peak RPE


def test_journal_tag_normalization():
    entry = JournalEntry(date(2025, 1, 6), "Lower back tight.", tags=["#Recovery"])
    entry.add_tag("  #Soreness ")
    entry.add_tag("recovery")  # duplicate, should be ignored
    assert entry.tags == ["recovery", "soreness"]


def test_journal_photo_optional():
    entry = JournalEntry(date(2025, 1, 6), "notes", photo="/img/me.jpg")
    assert entry.photo == "/img/me.jpg"
    no_photo = JournalEntry(date(2025, 1, 6), "notes")
    assert no_photo.photo is None
