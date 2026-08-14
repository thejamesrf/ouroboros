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
