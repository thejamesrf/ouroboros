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


def test_time_frame_is_enum_for_known_value():
    """The canonical realm's 'Outside' time-frame loads as the TimeFrame enum."""
    from ouroboros.realms import TimeFrame

    realm = canonical_realm()
    assert isinstance(realm.time_frame, TimeFrame)
    assert realm.time_frame is TimeFrame.OUTSIDE
    assert str(realm.time_frame) == "Outside"


def test_time_frame_falls_back_to_str_for_unknown():
    """An unrecognized time-frame string is kept as a plain string (lenient)."""
    from ouroboros.realms import TimeFrame

    minimal = {
        "name": "Test", "type": "Pocket", "time_frame": "The Heat Death",
        "location": {"realm": "R", "coordinates": "C"},
        "population": "1", "dimensions": "3",
        "essence": {"primary_language": "Ontos"},
        "purpose": {"function": "None"},
        "architecture": {"structure": {}}, "environment": {},
    }
    realm = load_realm_dict(minimal)
    assert not isinstance(realm.time_frame, TimeFrame)
    assert realm.time_frame == "The Heat Death"


def test_to_json_round_trips_enum_field():
    """to_json must emit the enum's string value, not 'TimeFrame.OUTSIDE'."""
    import json

    out = json.loads(canonical_realm().to_json())
    assert out["time_frame"] == "Outside"
    assert out == CANONICAL_REALM_DICT


def test_main_prints_canonical_realm(capsys):
    """Running the module with no args prints the canonical realm."""
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "-m", "ouroboros.realms"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert "Labyrinth of Eternity" in result.stdout
