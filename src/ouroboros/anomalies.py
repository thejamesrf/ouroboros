"""Anomaly Forge — generate anomalies for Hidden Gods sessions.

Hidden Gods is a PbtA game where anomalies are the glitches, clues, and
disruptions that hint at the simulation's layered nature. This module is the
runnable counterpart to the anomaly format documented in
``hidden-gods/README.md``:

    🔍 Anomaly: The Echoing Door
    - Manifestation: A door that repeats the last 3 seconds of sound when opened.
    - Clue: "The air smells like ozone."
    - Purpose: To test the party's perception of time.
    - Risk: Roll+Weird to resist disorientation (2-Weird).

Each anomaly belongs to a simulation layer, and each layer carries its own god
and rules. Generation is deterministic when seeded, so a Facilitator can replay
or share a session's anomalies.
"""

from __future__ import annotations

import random
import textwrap
from dataclasses import dataclass, field
from typing import Literal

# --------------------------------------------------------------------------- #
# Layers — the four example layers from hidden-gods/README.md, each carrying
# its administering god and governing rules.
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Layer:
    """A simulation layer: its theme, governing god, and rules of operation."""

    name: str
    theme: str
    god: str
    rules: str

    def __str__(self) -> str:
        return self.name


LAYERS: dict[str, Layer] = {
    "Base Reality": Layer(
        name="Base Reality",
        theme='"Normal" life',
        god="The Architect",
        rules="Standard physics, but with subtle glitches.",
    ),
    "Debug": Layer(
        name="Debug",
        theme="Glitchy, monochrome",
        god="The Debugger",
        rules="Code is visible as geometry; time is non-linear.",
    ),
    "Dream": Layer(
        name="Dream",
        theme="Surreal, emotional",
        god="The Dreamer",
        rules="Rules are fluid; emotions shape reality.",
    ),
    "Machine": Layer(
        name="Machine",
        theme="Mechanical, cold",
        god="The Engineer",
        rules="Everything is a machine; free will is an illusion.",
    ),
}

# The five PbtA stats from hidden-gods/README.md. Risk rolls reference one.
Stat = Literal["Weird", "Cool", "Sharp", "Hot", "Charm"]
ALL_STATS: tuple[Stat, ...] = ("Weird", "Cool", "Sharp", "Hot", "Charm")

# The canonical example anomaly — the reference implementation of the schema.
CANONICAL_ANOMALY = {
    "name": "The Echoing Door",
    "manifestation": "A door that repeats the last 3 seconds of sound when opened.",
    "clue": "The air smells like ozone.",
    "purpose": "To test the party's perception of time.",
    "risk": {"stat": "Weird", "roll": "2d6+Weird", "threshold": "resist disorientation"},
}


# --------------------------------------------------------------------------- #
# Generators — tables of fragments the forge combines into an anomaly.
# --------------------------------------------------------------------------- #

_NAMES_BY_LAYER: dict[str, list[str]] = {
    "Base Reality": ["The Lagging Clock", "The Misfile", "The Repeat Letter", "The Ghost Reflection"],
    "Debug": ["The Echoing Door", "The Stack Overflow", "The Null Pointer", "The Dangling Reference"],
    "Dream": ["The Weeping Mirror", "The Unfinished Room", "The Memory Loop", "The Sobbing Tide"],
    "Machine": ["The Seized Gear", "The Overrun Process", "The Misaligned Belt", "The Idle Servo"],
}

_MANIFESTATIONS = [
    "A {noun} that repeats the last 3 seconds of {sense} when {trigger}.",
    "A {noun} whose surface flickers between two states of matter.",
    "A {noun} that casts a shadow pointing the wrong way.",
    "A corridor that is longer when walked than when measured.",
    "A {noun} that hums at the frequency of a nearby god's true name.",
    "A {noun} that only exists when no one is looking directly at it.",
]

_NOUNS = ["door", "window", "staircase", "mirror", "archway", "terminal", "fountain", "key"]
_SENSES = ["sound", "light", "touch", "smell", "memory"]
_TRIGGERS = ["opened", "touched", "named aloud", "crossed", "remembered"]

_CLUES = [
    "The air smells like ozone.",
    "A cold spot lingers where none should be.",
    "Your reflection blinks a half-second late.",
    "You taste copper at the back of your throat.",
    "A nearby clock reads the same time twice.",
    "Something hums beneath the floor that shouldn't.",
    "Your shadow stretches toward the anomaly.",
    "You hear your own voice, slightly ahead of itself.",
]

_PURPOSES = [
    "To test the party's perception of time.",
    "To reveal the seam between two layers.",
    "To bait a Hidden God's attention.",
    "To mark the boundary the party just crossed.",
    "To echo a choice the party has not yet made.",
    "To conceal a door the party already passed.",
    "To translate a god's warning into sensation.",
]

# Which stat an anomaly tends to test, loosely keyed to the layer's flavor.
_LAYER_RISK_STAT: dict[str, Stat] = {
    "Base Reality": "Sharp",
    "Debug": "Weird",
    "Dream": "Charm",
    "Machine": "Cool",
}


@dataclass
class Anomaly:
    """A generated or hand-built anomaly."""

    name: str
    manifestation: str
    clue: str
    purpose: str
    risk: dict[str, str]
    layer: Layer | None = None

    def as_dict(self) -> dict:
        """Return the plain-dict form documented in hidden-gods/README.md."""

        d = {
            "name": self.name,
            "manifestation": self.manifestation,
            "clue": self.clue,
            "purpose": self.purpose,
            "risk": self.risk,
        }
        if self.layer is not None:
            d["layer"] = self.layer.name
        return d

    def render(self) -> str:
        """Pretty-print in the README's canonical markdown block format."""

        layer_line = f"  Layer: {self.layer}\n" if self.layer else ""
        return textwrap.dedent(f"""\
            🔍 **Anomaly: {self.name}**
            {layer_line}- **Manifestation**: {self.manifestation}
            - **Clue**: "{self.clue}"
            - **Purpose**: {self.purpose}
            - **Risk**: Roll+{self.risk['stat']} to {self.risk['threshold']} ({self.risk['roll']}).
            """)


def generate_anomaly(
    layer: str | Layer | None = None,
    rng: random.Random | None = None,
) -> Anomaly:
    """Generate a single random anomaly, optionally constrained to a layer.

    Pass a ``layer`` name (e.g. ``"Debug"``) or :class:`Layer` to anchor the
    anomaly's name and risk stat. Pass an ``rng`` for deterministic output.
    """

    rng = rng or random.Random()

    if layer is None:
        layer_obj = rng.choice(list(LAYERS.values()))
    elif isinstance(layer, Layer):
        layer_obj = layer
    else:
        layer_obj = LAYERS.get(layer)
        if layer_obj is None:
            raise ValueError(f"unknown layer {layer!r}; choose from {list(LAYERS)}")

    name = rng.choice(_NAMES_BY_LAYER[layer_obj.name])
    manifestation = rng.choice(_MANIFESTATIONS).format(
        noun=rng.choice(_NOUNS),
        sense=rng.choice(_SENSES),
        trigger=rng.choice(_TRIGGERS),
    )
    clue = rng.choice(_CLUES)
    purpose = rng.choice(_PURPOSES)
    stat = _LAYER_RISK_STAT.get(layer_obj.name, "Weird")
    threshold = "resist disorientation"
    risk = {"stat": stat, "roll": f"2d6+{stat}", "threshold": threshold}

    return Anomaly(
        name=name,
        manifestation=manifestation,
        clue=clue,
        purpose=purpose,
        risk=risk,
        layer=layer_obj,
    )


def generate_batch(n: int, layer: str | None = None, seed: int | None = None) -> list[Anomaly]:
    """Generate ``n`` anomalies, optionally seeded and constrained to a layer."""

    rng = random.Random(seed)
    return [generate_anomaly(layer=layer, rng=rng) for _ in range(n)]


def canonical_anomaly() -> Anomaly:
    """Return the reference anomaly from hidden-gods/README.md, typed.

    Useful as a fixture and as living documentation of the schema.
    """

    return Anomaly(
        name=CANONICAL_ANOMALY["name"],
        manifestation=CANONICAL_ANOMALY["manifestation"],
        clue=CANONICAL_ANOMALY["clue"],
        purpose=CANONICAL_ANOMALY["purpose"],
        risk=dict(CANONICAL_ANOMALY["risk"]),
        layer=LAYERS["Debug"],
    )
