"""Tests for the Ontos → English translator."""

from ouroboros.translate import translate_to_english


def test_binary_parenthesized():
    assert translate_to_english("(A ∧ B) → C") == "A and B implies C"


def test_layer_scope():
    out = translate_to_english("[λ_Debug] (A → B)")
    assert out.startswith("In the Debug Layer,")
    assert "A implies B" in out


def test_layer_shift():
    out = translate_to_english("(λ_Debug → λ_Dream) (A)")
    assert "A transitions from the Debug Layer to the Dream Layer" == out


def test_quantified():
    out = translate_to_english("∀x (x ∈ λ_Debug)")
    assert out == "for all x, x is in the Debug Layer"


def test_entity_glosses():
    out = translate_to_english("𝒢_Architect → ⚡_EchoingDoor")
    assert "the Hidden God Architect" in out
    assert "the anomaly EchoingDoor" in out
    assert "implies" in out


def test_marked_self_reference():
    out = translate_to_english("⍶(A) = A")
    assert "refers to itself" in out


def test_godelian_statement():
    out = translate_to_english("⏅(Ontos) ∧ (Ontos → ⏄)")
    assert "is incomplete" in out
    assert "the unknown" in out


def test_empty():
    assert translate_to_english("") == ""


def test_base_reality_layer():
    out = translate_to_english("[λ₀] (A → B)")
    assert out.startswith("In Base Reality,")


# --------------------------------------------------------------------------- #
# English -> Ontos + Story Navigator (the reverse direction).
# --------------------------------------------------------------------------- #

from ouroboros.translate import translate_from_english, summarize_story
from ouroboros.ontos import validate_statement


def test_english_to_ontos_finds_entities_and_layer():
    out = translate_from_english("Alice enters the Debug layer and reveals the Architect.")
    assert "\u03bb_Debug" in out          # layer scoped
    assert "\U0001D4AB_Alice" in out      # player
    assert "\U0001D4A2_Architect" in out  # god
    assert validate_statement(out).valid


def test_english_to_ontos_valid_output_always():
    """Generated Ontos must always pass the validator."""
    for s in [
        "The Debugger creates a glitch.",
        "Alice and Brett encounter the Echoing Door.",
        "Something entirely unrelated to the lore.",
        "",
    ]:
        out = translate_from_english(s)
        if out:  # empty input returns ""
            assert validate_statement(out).valid, f"invalid: {out}"


def test_english_to_ontos_godelian_for_unknown():
    out = translate_from_english("Something entirely unrelated to the lore.")
    assert "\u23C5" in out  # incomplete marker
    assert validate_statement(out).valid


def test_empty_english_returns_empty():
    assert translate_from_english("") == ""


def test_summarize_story_extracts_actors_layers_anomalies():
    story = (
        "Alice enters the Debug layer. She triggers the Echoing Door. "
        "The Architect reveals a new anomaly."
    )
    nav = summarize_story(story)
    assert "\U0001D4AB_Alice" in nav.entities
    assert "\U0001D4A2_Architect" in nav.entities
    assert "\u03bb_Debug" in nav.layers
    assert "\u26A1_EchoingDoor" in nav.anomalies
    assert "\u26A1_Anomaly" in nav.anomalies
    assert len(nav.statements) >= 3
    assert nav.summary
    # Every statement must be valid Ontos.
    for stmt in nav.statements:
        assert validate_statement(stmt).valid, f"invalid: {stmt}"


def test_summarize_story_empty_input():
    nav = summarize_story("")
    assert nav.summary == "(empty input)"
    assert nav.statements == []


def test_navigator_render_has_sections():
    nav = summarize_story("Alice triggers the Echoing Door in the Debug layer.")
    out = nav.render()
    assert "Navigator Output" in out
    assert "Actors:" in out
    assert "Ontos statements:" in out
    assert "Summary:" in out
