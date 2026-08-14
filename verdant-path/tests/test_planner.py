"""Tests for the planner, splits, and templates."""

from datetime import date

import pytest

from verdant_path.planner import Planner, SetTarget, SPLITS, split_for_frequency
from verdant_path.templates import default_planner, register_default_templates


def test_all_frequencies_have_splits():
    for freq in range(1, 7):
        split = split_for_frequency(freq)
        assert split["name"]
        assert len(split["days"]) >= 1


def test_invalid_frequency_rejected():
    with pytest.raises(ValueError):
        split_for_frequency(0)
    with pytest.raises(ValueError):
        split_for_frequency(7)


def test_build_session_creates_phases():
    planner = Planner()
    session = planner.build_session(
        name="Test",
        main=[("deadlift", SetTarget(5, "3", rpe=8))],
        accessory=[("suitcase_carry", SetTarget(3, "40m"))],
        conditioning="Zone 2 20 min",
    )
    block_names = [b.name for b in session.blocks]
    assert "Warm-Up" in block_names
    assert "Main Work" in block_names
    assert "Accessory / Finisher" in block_names
    assert "Conditioning" in block_names


def test_plan_validates_day_count():
    planner = default_planner()
    with pytest.raises(ValueError):
        planner.build_plan(frequency=5, days=[planner.templates["Posterior Chain"]])


def test_default_plan_covers_all_patterns():
    planner = default_planner()
    plan = planner.build_plan(
        frequency=5,
        days=[
            planner.templates["Posterior Chain"],
            planner.templates["LISS Run"],
            planner.templates["Chest + Biceps"],
            planner.templates["HIIT / Work-Capacity"],
            planner.templates["Shoulders + Triceps"],
        ],
    )
    assert plan.weekly_coverage() is True
    assert "covered" in plan.coverage_report()


def test_schedule_lays_out_consecutive_days():
    planner = default_planner()
    plan = planner.build_plan(
        frequency=3,
        days=[
            planner.templates["Posterior Chain"],
            planner.templates["LISS Run"],
            planner.templates["Active Recovery"],
        ],
    )
    start = date(2025, 1, 6)
    scheduled = planner.schedule(plan, start)
    assert len(scheduled) == 3
    assert scheduled[0][0] == start
    assert scheduled[2][0] == date(2025, 1, 8)


def test_unknown_movement_rejected():
    planner = Planner()
    with pytest.raises(KeyError):
        planner.build_session(name="x", main=[("nope", SetTarget(3, "5"))])
