"""Tests for the three-level translation stack (narrator.py)."""

from ouroboros.narrator import (
    ThreeLevelOutput,
    to_level1,
    to_level2,
    to_level3,
    translate_three_levels,
)
from ouroboros.ontos import validate_statement


def test_level1_produces_valid_ontos():
    stmts = to_level1("Alice enters the Debug layer. She triggers the Echoing Door.")
    assert len(stmts) >= 1
    for s in stmts:
        assert validate_statement(s).valid, f"invalid: {s}"


def test_level1_empty_input():
    assert to_level1("") == []


def test_level2_quill_is_nonempty_and_strained():
    import random
    out = to_level2("Alice triggers the Echoing Door in the Debug layer.", random.Random(1))
    assert out
    # The Quill voice references the precision/English tension.
    assert "Ontos" in out or "English" in out or "→" in out


def test_level2_handles_unrecognized_input():
    out = to_level2("A completely unrelated sentence about tax policy.")
    assert out  # does not crash; returns a Gödelian acknowledgement


def test_level3_poetic_is_nonempty_and_mythic():
    import random
    out = to_level3("Alice encounters the Architect in the Debug layer.", random.Random(2))
    assert out
    # The poetic voice should mention at least one extracted entity by name.
    assert "Alice" in out or "Architect" in out or "Debug" in out


def test_level3_handles_unrecognized_input():
    out = to_level3("A sentence about nothing recognizable.")
    assert out  # graceful, no crash


def test_three_levels_all_populated():
    story = "Alice enters the Debug layer. She triggers the Echoing Door, which reveals the Architect."
    result = translate_three_levels(story, seed=5)
    assert isinstance(result, ThreeLevelOutput)
    assert len(result.level1_ontos) >= 1
    assert result.level2_quill
    assert result.level3_poetic
    # Navigator extraction carries through.
    assert result.navigator.entities or result.navigator.anomalies


def test_three_levels_seeded_reproducible():
    story = "Alice triggers the Echoing Door in the Debug layer."
    a = translate_three_levels(story, seed=42)
    b = translate_three_levels(story, seed=42)
    assert a.level2_quill == b.level2_quill
    assert a.level3_poetic == b.level3_poetic


def test_render_has_all_three_levels():
    result = translate_three_levels("Alice in the Debug layer.", seed=1)
    out = result.render()
    assert "Level 1" in out
    assert "Level 2" in out
    assert "Level 3" in out
    assert "Navigator" in out


def test_level1_ontos_all_validate():
    """Every Level 1 statement must pass the validator."""
    story = (
        "Alice enters the Debug layer. She triggers the Echoing Door. "
        "The Architect reveals a new anomaly. The Debugger awakens."
    )
    for stmt in to_level1(story):
        assert validate_statement(stmt).valid, f"invalid Ontos: {stmt}"
