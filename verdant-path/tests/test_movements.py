"""Tests for the six fundamental movement patterns."""

from verdant_path.movements import (
    MOVEMENT_PATTERNS,
    Movement,
    Pattern,
    all_patterns_covered,
    missing_patterns,
)


def test_six_patterns_defined():
    assert len(list(Pattern)) == 6
    expected = {"push", "pull", "hinge", "lunge", "squat", "carry/rotate/anti-rotate"}
    assert {p.value for p in Pattern} == expected


def test_library_covers_all_patterns():
    movements = list(MOVEMENT_PATTERNS.values())
    assert all_patterns_covered(movements) is True
    assert missing_patterns(movements) == []


def test_missing_patterns_detected():
    only_push = [Movement("Bench", Pattern.PUSH)]
    assert all_patterns_covered(only_push) is False
    missing = missing_patterns(only_push)
    assert Pattern.PULL in missing
    assert len(missing) == 5


def test_empty_name_rejected():
    import pytest

    with pytest.raises(ValueError):
        Movement("  ", Pattern.PUSH)
