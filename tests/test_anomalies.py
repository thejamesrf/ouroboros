"""Tests for the Anomaly Forge."""

from ouroboros.anomalies import (
    ALL_STATS,
    CANONICAL_ANOMALY,
    LAYERS,
    Anomaly,
    canonical_anomaly,
    generate_anomaly,
    generate_batch,
)


def test_canonical_anomaly_matches_readme():
    a = canonical_anomaly()
    assert a.name == CANONICAL_ANOMALY["name"]
    assert a.manifestation == CANONICAL_ANOMALY["manifestation"]
    assert a.clue == CANONICAL_ANOMALY["clue"]
    assert a.purpose == CANONICAL_ANOMALY["purpose"]
    assert a.risk == CANONICAL_ANOMALY["risk"]
    assert a.layer is not None
    assert a.layer.name == "Debug"


def test_canonical_anomaly_as_dict_has_required_keys():
    d = canonical_anomaly().as_dict()
    for key in ("name", "manifestation", "clue", "purpose", "risk"):
        assert key in d
    for key in ("stat", "roll", "threshold"):
        assert key in d["risk"]


def test_generated_anomaly_has_full_schema():
    a = generate_anomaly(rng=__import__("random").Random(0))
    assert a.name
    assert a.manifestation
    assert a.clue
    assert a.purpose
    assert a.risk["stat"] in ALL_STATS
    assert "roll" in a.risk and "threshold" in a.risk
    assert a.layer is not None


def test_layer_constraint_is_respected():
    a = generate_anomaly(layer="Dream", rng=__import__("random").Random(1))
    assert a.layer.name == "Dream"


def test_unknown_layer_raises():
    import pytest

    with pytest.raises(ValueError):
        generate_anomaly(layer="Nope")


def test_batch_count_and_seeding():
    batch = generate_batch(5, seed=3)
    assert len(batch) == 5
    again = generate_batch(5, seed=3)
    assert [a.as_dict() for a in batch] == [a.as_dict() for a in again]


def test_render_contains_markers():
    out = canonical_anomaly().render()
    assert "🔍" in out
    assert "Manifestation" in out
    assert "Risk" in out


def test_all_four_layers_present():
    assert set(LAYERS) == {"Base Reality", "Debug", "Dream", "Machine"}
    for layer in LAYERS.values():
        assert layer.god
        assert layer.rules


def test_anomaly_is_mutable_dataclass():
    a = Anomaly(
        name="X",
        manifestation="m",
        clue="c",
        purpose="p",
        risk={"stat": "Weird", "roll": "2d6+Weird", "threshold": "t"},
    )
    a.name = "Y"  # Anomaly is a regular (mutable) dataclass
    assert a.name == "Y"
