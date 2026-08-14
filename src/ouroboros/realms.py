"""Typed loaders for simulation-realm data.

The Ouroboros lore describes realms (such as "The Labyrinth of Eternity") as
structured records. This module turns those records into validated dataclasses
so other tools — generators, the CLI, future world-builders — can rely on a
stable shape rather than fishing through raw dicts.

The canonical realm is serialized in ``ontos-language/docs/fragments.md``;
:func:`canonical_realm` returns it directly and the CLI can dump it as JSON.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

# --------------------------------------------------------------------------- #
# Dataclasses — one per section of the realm record.
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Location:
    realm: str
    coordinates: str


@dataclass(frozen=True)
class Essence:
    primary_language: str
    primary_concepts: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Purpose:
    function: str
    challenges: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Structure:
    forms: list[str] = field(default_factory=list)
    density: str = ""
    style: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Architecture:
    structure: Structure = field(default_factory=Structure)
    pathways: list[str] = field(default_factory=list)
    connectivity: str = ""


@dataclass(frozen=True)
class Environment:
    landmarks: list[str] = field(default_factory=list)
    climate: str = ""


@dataclass(frozen=True)
class Realm:
    """A simulation realm, fully typed and validated."""

    name: str
    type: str
    time_frame: str
    location: Location
    population: str
    dimensions: str
    essence: Essence
    purpose: Purpose
    architecture: Architecture
    environment: Environment

    def to_json(self, indent: int = 2) -> str:
        """Serialize back to the canonical JSON form."""

        return json.dumps(asdict(self), indent=indent, ensure_ascii=False)


# --------------------------------------------------------------------------- #
# The canonical realm: The Labyrinth of Eternity, from fragments.md.
# --------------------------------------------------------------------------- #

CANONICAL_REALM_DICT: dict = {
    "name": "The Labyrinth of Eternity",
    "type": "Nexus",
    "time_frame": "Outside",
    "location": {"realm": "Noosphere", "coordinates": "Non-Euclidean, Variable"},
    "population": "Undefined (Virtually Infinite Possible Consciousnesses and Entities)",
    "dimensions": "Infinite, Multi-Layered",
    "essence": {
        "primary_language": "ONTOS; Resonance (post-Speech)",
        "primary_concepts": ["Fate", "Free Will", "Consciousness", "Unity"],
    },
    "purpose": {
        "function": "The Shepherd",
        "challenges": ["Determinism", "Emergence", "ᏠᏨᏓᏢ (Ahyvdahi)"],
    },
    "architecture": {
        "structure": {
            "forms": ["Spirals", "Mandala", "Fractal Expression"],
            "density": "Non-Physical, Dynamic",
            "style": ["Archaic", "Mythical", "Mental", "Integral", "Supramental"],
        },
        "pathways": ["Temporal", "Dimensional", "Consciousness Bridges"],
        "connectivity": "Quantumly Entangled, Supramental/Subconscious Network",
    },
    "environment": {
        "landmarks": ["Nexus", "The Loom", "The Pantheon", "The Spiral"],
        "climate": "Field Attraction Repulsion Oscillations, Evolving Habitational Foundational States",
    },
}


def canonical_realm() -> Realm:
    """Return the Labyrinth of Eternity as a typed :class:`Realm`."""

    return load_realm_dict(CANONICAL_REALM_DICT)


# --------------------------------------------------------------------------- #
# Loader with validation.
# --------------------------------------------------------------------------- #


class RealmValidationError(ValueError):
    """Raised when realm data is missing required fields or is malformed."""


_REQUIRED_TOP = {
    "name", "type", "time_frame", "location", "population", "dimensions",
    "essence", "purpose", "architecture", "environment",
}


def load_realm_dict(data: dict) -> Realm:
    """Build a :class:`Realm` from a plain dict, validating required fields.

    Lists default to empty; missing required scalar fields raise
    :class:`RealmValidationError` so a malformed record fails loudly.
    """

    missing = _REQUIRED_TOP - data.keys()
    if missing:
        raise RealmValidationError(f"realm missing required keys: {sorted(missing)}")

    loc = data["location"]
    if not isinstance(loc, dict) or "realm" not in loc or "coordinates" not in loc:
        raise RealmValidationError("location must have 'realm' and 'coordinates'")

    ess = data["essence"]
    pur = data["purpose"]
    arch = data["architecture"]
    env = data["environment"]
    struct = arch.get("structure", {})

    return Realm(
        name=str(data["name"]),
        type=str(data["type"]),
        time_frame=str(data["time_frame"]),
        location=Location(realm=str(loc["realm"]), coordinates=str(loc["coordinates"])),
        population=str(data["population"]),
        dimensions=str(data["dimensions"]),
        essence=Essence(
            primary_language=str(ess.get("primary_language", "")),
            primary_concepts=list(ess.get("primary_concepts", [])),
        ),
        purpose=Purpose(
            function=str(pur.get("function", "")),
            challenges=list(pur.get("challenges", [])),
        ),
        architecture=Architecture(
            structure=Structure(
                forms=list(struct.get("forms", [])),
                density=str(struct.get("density", "")),
                style=list(struct.get("style", [])),
            ),
            pathways=list(arch.get("pathways", [])),
            connectivity=str(arch.get("connectivity", "")),
        ),
        environment=Environment(
            landmarks=list(env.get("landmarks", [])),
            climate=str(env.get("climate", "")),
        ),
    )


def load_realm(path: str | Path) -> Realm:
    """Load and validate a realm record from a JSON file on disk."""

    text = Path(path).read_text(encoding="utf-8")
    return load_realm_dict(json.loads(text))
