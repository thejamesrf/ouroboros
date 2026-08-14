"""Tests for the Ontos validator against grammar.md's golden cases."""

from ouroboros.ontos import (
    GOLDEN_CASES,
    generate_batch,
    generate_statement,
    validate_statement,
    validate_many,
)


def test_all_golden_cases_agree_with_grammar_md():
    """Every golden case must validate exactly as the spec says."""

    failures = []
    for statement, expected in GOLDEN_CASES.items():
        result = validate_statement(statement)
        if result.valid != expected:
            failures.append((statement, expected, result.valid, result.errors))
    assert not failures, failures


def test_missing_parens_invalid():
    r = validate_statement("A ∧ B → C")
    assert not r.valid
    assert any(e.rule == "grouping" for e in r.errors)


def test_parenthesized_binary_valid():
    assert validate_statement("(A ∧ B) → C").valid


def test_unbound_variable_invalid():
    r = validate_statement("x ∈ λ_Debug")
    assert not r.valid
    assert any(e.rule == "unbound" for e in r.errors)


def test_bound_variable_valid():
    assert validate_statement("∀x (x ∈ λ_Debug)").valid


def test_raw_self_reference_invalid():
    r = validate_statement("A = A")
    assert not r.valid
    assert any(e.rule == "self-reference" for e in r.errors)


def test_marked_self_reference_valid():
    assert validate_statement("⍶(A) = A").valid


def test_layer_scope_valid():
    assert validate_statement("[λ_Debug] (A → B)").valid


def test_layer_shift_valid():
    assert validate_statement("(λ_Debug → λ_Dream) (A)").valid


def test_empty_statement_invalid():
    assert not validate_statement("").valid


def test_validate_many_returns_one_per_statement():
    results = validate_many(["(A ∧ B) → C", "A ∧ B → C"])
    assert len(results) == 2
    assert results[0].valid
    assert not results[1].valid


def test_generator_output_is_always_valid():
    """The generator must only ever emit statements that pass the validator."""

    for stmt in generate_batch(50, seed=42):
        assert validate_statement(stmt).valid, f"generator emitted invalid: {stmt}"


def test_generate_batch_is_seeded_reproducibly():
    a = generate_batch(10, seed=99)
    b = generate_batch(10, seed=99)
    assert a == b


def test_generate_statement_single():
    s = generate_statement()
    assert isinstance(s, str) and s
