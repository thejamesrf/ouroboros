"""Tests for the realm loader."""

import json

import pytest

from ouroboros.realms import (
    CANONICAL_REALM_DICT,
    RealmValidationError,
    canonical_realm,
    load_realm_dict,
)


def test_canonical_realm_round_trips():
    realm = canonical_realm()
    assert realm.name == "The Labyrinth of Eternity"
    assert realm.type == "Nexus"
    assert realm.location.realm == "Noosphere"
    assert realm.essence.primary_concepts == ["Fate", "Free Will", "Consciousness", "Unity"]
    # Serializing back should match the canonical dict.
    again = json.loads(realm.to_json())
    assert again == CANONICAL_REALM_DICT


def test_missing_required_key_raises():
    bad = dict(CANONICAL_REALM_DICT)
    del bad["essence"]
    with pytest.raises(RealmValidationError):
        load_realm_dict(bad)


def test_malformed_location_raises():
    bad = dict(CANONICAL_REALM_DICT)
    bad["location"] = {"realm": "X"}  # missing coordinates
    with pytest.raises(RealmValidationError):
        load_realm_dict(bad)


def test_lists_default_to_empty():
    minimal = {
        "name": "Test",
        "type": "Pocket",
        "time_frame": "Now",
        "location": {"realm": "R", "coordinates": "C"},
        "population": "1",
        "dimensions": "3",
        "essence": {"primary_language": "Ontos"},
        "purpose": {"function": "None"},
        "architecture": {"structure": {}},
        "environment": {},
    }
    realm = load_realm_dict(minimal)
    assert realm.essence.primary_concepts == []
    assert realm.environment.landmarks == []
    assert realm.architecture.structure.forms == []


def test_load_from_file(tmp_path):
    p = tmp_path / "realm.json"
    p.write_text(json.dumps(CANONICAL_REALM_DICT), encoding="utf-8")
    from ouroboros.realms import load_realm

    realm = load_realm(p)
    assert realm.name == "The Labyrinth of Eternity"
