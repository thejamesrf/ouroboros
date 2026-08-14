"""Tests for the 90-day habits program."""

from verdant_path.habits import (
    BUILDUP_PHASES,
    NINETY_DAY_PROGRAM,
    all_habits,
    habit_score,
    habit_streak,
)


def test_program_has_three_groups():
    assert len(NINETY_DAY_PROGRAM) == 3
    names = [g.name for g in NINETY_DAY_PROGRAM]
    assert "Morning Routine (Minimum)" in names
    assert "Evening Routine (Minimum)" in names


def test_all_habits_nonempty():
    habits = all_habits()
    assert len(habits) >= 12
    assert all(h.name for h in habits)


def test_perfect_score():
    completed = {h.name: True for h in all_habits()}
    assert habit_score(completed) == 100.0


def test_zero_score():
    completed = {h.name: False for h in all_habits()}
    assert habit_score(completed) == 0.0


def test_partial_score_in_range():
    completed = {h.name: True for h in all_habits()[:6]}
    score = habit_score(completed)
    assert 0 < score < 100


def test_streak_counts_consecutive_good_days():
    scores = [60, 85, 90, 82]
    assert habit_streak(scores, threshold=80) == 3


def test_streak_broken_resets():
    scores = [90, 90, 70, 90]
    assert habit_streak(scores, threshold=80) == 1


def test_buildup_phases_present():
    assert len(BUILDUP_PHASES) == 4
    assert BUILDUP_PHASES[-1].weeks == "End of 90 Days"
