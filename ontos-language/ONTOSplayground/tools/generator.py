#!/usr/bin/env python3
"""
ONTOS Generator
Purpose: Generates random Ontos statements for Hidden Gods content (anomalies, layers, gods).
"""

import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class GeneratedAnomaly:
    """Represents a generated anomaly in Ontos format."""
    name: str
    layer: str
    manifestation: str
    clue: str
    purpose: str
    risk: str
    god: str


@dataclass
class GeneratedLayer:
    """Represents a generated simulation layer in Ontos format."""
    name: str
    theme: str
    rules: str
    god: str


@dataclass
class GeneratedGod:
    """Represents a generated Hidden God in Ontos format."""
    name: str
    role: str
    domain: str
    strength: str
    weakness: str
    symbol: str


class OntosGenerator:
    """Generates random Ontos statements for Hidden Gods content."""

    def __init__(self):
        self.layers = [
            {"name": "Base Reality", "god": "The Architect"},
            {"name": "Debug", "god": "The Debugger"},
            {"name": "Dream", "god": "The Dreamer"},
            {"name": "Machine", "god": "The Engineer"},
            {"name": "Void", "god": "The Weaver"},
        ]

        self.themes = {
            "Base Reality": ["Normal life with subtle glitches", "A mundane world with hidden cracks"],
            "Debug": ["Glitchy, monochrome, floating symbols", "A world of visible code and non-linear time"],
            "Dream": ["Surreal, emotional, shifting landscapes", "A fluid reality shaped by feelings"],
            "Machine": ["Mechanical, cold, clockwork", "A deterministic world of gears and logic"],
            "Void": ["Empty, silent, infinite", "A place between layers where nothing is certain"],
        }

        self.rules = {
            "Base Reality": ["Standard physics; time is linear; glitches are rare"],
            "Debug": ["Code is visible as geometry; time is non-linear; logic can be rewritten"],
            "Dream": ["Rules are fluid; emotions shape reality; time is subjective"],
            "Machine": ["Everything is a machine; free will is an illusion; determinism reigns"],
            "Void": ["No rules apply; reality is malleable; time does not exist"],
        }

        self.anomaly_manifestations = {
            "Base Reality": [
                "A light that flickers in Morse code",
                "A door that wasn't there yesterday",
                "A person who doesn't cast a shadow",
                "A sound that only you can hear",
            ],
            "Debug": [
                "A door that repeats the last 3 seconds of sound when opened",
                "A floating terminal displaying unknown code",
                "A wall that can be walked through if you believe it's not there",
                "A glitch that erases part of your memory",
            ],
            "Dream": [
                "The environment changes based on your emotions",
                "A creature made of your deepest fears",
                "A path that only appears when you stop looking for it",
                "A voice that speaks your own thoughts back to you",
            ],
            "Machine": [
                "An NPC that moves in perfectly predictable patterns",
                "A room where every action has an equal and opposite reaction",
                "A clock that counts down to an unknown event",
                "A machine that outputs your next thought before you think it",
            ],
            "Void": [
                "A void that whispers secrets from other layers",
                "A place where time loops endlessly",
                "A door that leads to a random layer",
                "A silence that feels like it's watching you",
            ],
        }

        self.anomaly_clues = {
            "Base Reality": ["The air smells like static", "Your skin tingles", "A cold breeze passes through the room"],
            "Debug": ["The air smells like ozone", "Your vision flickers", "You hear a distant hum"],
            "Dream": ["The ground feels like it's breathing", "Colors seem brighter than usual", "You feel an unexplained emotion"],
            "Machine": ["You hear the sound of gears turning", "The air is unnaturally still", "Everything feels... mechanical"],
            "Void": ["You feel like you're being watched", "The silence is deafening", "You can't remember how you got here"],
        }

        self.anomaly_purposes = {
            "Base Reality": [
                "To test your perception of reality",
                "To reveal a hidden truth",
                "To warn you of a coming danger",
            ],
            "Debug": [
                "To test the party’s perception of time",
                "To reveal a hidden code fragment",
                "To force the party to confront a glitch in their own minds",
            ],
            "Dream": [
                "To force the party to confront their subconscious fears",
                "To reveal a hidden emotion",
                "To test the party’s ability to control their emotions",
            ],
            "Machine": [
                "To demonstrate the deterministic nature of the layer",
                "To force the party to accept their lack of free will",
                "To reveal a hidden pattern",
            ],
            "Void": [
                "To test the party’s sanity",
                "To reveal a truth from another layer",
                "To force the party to make a choice with no good options",
            ],
        }

        self.anomaly_risks = [
            "Roll+Weird to resist disorientation (2-Weird)",
            "Roll+Sharp to decipher (2-Sharp)",
            "Roll+Cool to avoid being pulled in (2-Cool)",
            "Roll+Hot to force it to despawn (2-Hot)",
            "Roll+Charm to negotiate with it (2-Charm)",
        ]

        self.god_names = [
            "The Architect", "The Debugger", "The Dreamer", "The Engineer", "The Weaver",
            "The Observer", "The Judge", "The Creator", "The Destroyer", "The Guide"
        ]

        self.god_roles = [
            "Builder of layers", "Fixes or breaks the simulation's code", 
            "Shapes emotional and subconscious reality", "Designs the mechanical underpinnings of reality",
            "Weaves the threads of fate", "Observes all but interferes with none",
            "Judges the worth of all actions", "Creates new layers", "Destroys old layers",
            "Guides lost souls between layers"
        ]

        self.god_domains = [
            "Base Reality", "Debug Layer", "Dream Layer", "Machine Layer", "Void",
            "All Layers", "The Space Between Layers", "The Edge of Reality"
        ]

        self.god_strengths = [
            "Omniscient within its own layer", "Can rewrite the rules of its layer",
            "Can manifest emotions as physical reality", "Understands the deterministic nature of its layer",
            "Sees all possible threads of fate", "Cannot be lied to", "Can create new layers at will",
            "Can destroy any layer it touches", "Knows the shortest path between any two points in reality"
        ]

        self.god_weaknesses = [
            "Blind to its own biases and limitations", "Overly literal; struggles with ambiguity",
            "Lost in the fluidity of its own layer", "Cannot comprehend free will or randomness",
            "Cannot see the threads it is not weaving", "Can only observe, not act",
            "Its judgments are always harsh", "Creating new layers drains its power",
            "Destroying layers fills it with sorrow"
        ]

        self.god_symbols = [
            "A compass that always points inward", "A floating, glowing terminal",
            "A shifting, kaleidoscopic mask", "A gear that turns all other gears",
            "A spider weaving a web", "An unblinking eye", "A set of scales",
            "A hammer and chisel", "A black hole", "A lantern"
        ]

    def generate_anomaly(self, layer: Optional[str] = None) -> GeneratedAnomaly:
        """Generate a random anomaly for a specific layer (or any layer)."""
        if layer is None:
            layer = random.choice(self.layers)["name"]

        god = next(l["god"] for l in self.layers if l["name"] == layer)

        return GeneratedAnomaly(
            name=f"The {random.choice(['Mysterious', 'Glitching', 'Whispering', 'Flickering', 'Shifting', 'Echoing', 'Silent', 'Watchful'])} {random.choice(['Door', 'Light', 'Shadow', 'Room', 'Path', 'Voice', 'Machine', 'Void'])}",
            layer=layer,
            manifestation=random.choice(self.anomaly_manifestations.get(layer, self.anomaly_manifestations["Base Reality"])),
            clue=random.choice(self.anomaly_clues.get(layer, self.anomaly_clues["Base Reality"])),
            purpose=random.choice(self.anomaly_purposes.get(layer, self.anomaly_purposes["Base Reality"])),
            risk=random.choice(self.anomaly_risks),
            god=god,
        )

    def generate_layer(self) -> GeneratedLayer:
        """Generate a random simulation layer."""
        name = random.choice([l["name"] for l in self.layers if l["name"] != "Base Reality"] + ["New Layer"])
        god = random.choice(self.god_names)

        return GeneratedLayer(
            name=name,
            theme=random.choice(self.themes.get(name, self.themes["Base Reality"])),
            rules=random.choice(self.rules.get(name, self.rules["Base Reality"])),
            god=god,
        )

    def generate_god(self) -> GeneratedGod:
        """Generate a random Hidden God."""
        return GeneratedGod(
            name=random.choice(self.god_names),
            role=random.choice(self.god_roles),
            domain=random.choice(self.god_domains),
            strength=random.choice(self.god_strengths),
            weakness=random.choice(self.god_weaknesses),
            symbol=random.choice(self.god_symbols),
        )

    def generate_ontos_anomaly(self, anomaly: GeneratedAnomaly) -> str:
        """Generate an Ontos-formatted anomaly."""
        return f"""-- {anomaly.name}
λ_Anomaly.name = "{anomaly.name}"
λ_Anomaly.layer = "{anomaly.layer}"
λ_Anomaly.manifestation = "{anomaly.manifestation}"
λ_Anomaly.clue = "{anomaly.clue}"
λ_Anomaly.purpose = "{anomaly.purpose}"
λ_Anomaly.risk = "{anomaly.risk}"
λ_Anomaly.god = "{anomaly.god}"
"""

    def generate_ontos_layer(self, layer: GeneratedLayer) -> str:
        """Generate an Ontos-formatted layer."""
        return f"""-- {layer.name} Layer
λ_Layer.name = "{layer.name}"
λ_Layer.theme = "{layer.theme}"
λ_Layer.rules = "{layer.rules}"
λ_Layer.god = "{layer.god}"
"""

    def generate_ontos_god(self, god: GeneratedGod) -> str:
        """Generate an Ontos-formatted god."""
        return f"""-- {god.name}
λ_God.name = "{god.name}"
λ_God.role = "{god.role}"
λ_God.domain = "{god.domain}"
λ_God.strength = "{god.strength}"
λ_God.weakness = "{god.weakness}"
λ_God.symbol = "{god.symbol}"
"""

    def generate_anomalies(self, n: int = 5, layer: Optional[str] = None) -> List[GeneratedAnomaly]:
        """Generate `n` random anomalies."""
        return [self.generate_anomaly(layer) for _ in range(n)]

    def generate_layers(self, n: int = 3) -> List[GeneratedLayer]:
        """Generate `n` random layers."""
        return [self.generate_layer() for _ in range(n)]

    def generate_gods(self, n: int = 3) -> List[GeneratedGod]:
        """Generate `n` random gods."""
        return [self.generate_god() for _ in range(n)]


def main():
    """Generate and print random Ontos content."""
    generator = OntosGenerator()

    print("=== Generated Anomalies ===")
    for anomaly in generator.generate_anomalies(3):
        print(generator.generate_ontos_anomaly(anomaly))

    print("\n=== Generated Layers ===")
    for layer in generator.generate_layers(2):
        print(generator.generate_ontos_layer(layer))

    print("\n=== Generated Gods ===")
    for god in generator.generate_gods(2):
        print(generator.generate_ontos_god(god))


if __name__ == "__main__":
    main()
