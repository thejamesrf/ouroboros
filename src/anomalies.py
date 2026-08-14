#!/usr/bin/env python3
"""
Hidden Gods: Anomaly Forge
A Python script to generate random anomalies, layers, and Hidden Gods for the Hidden Gods TTRPG.

Usage:
    python3 anomalies.py          # Print a single random anomaly
    python3 anomalies.py --json   # Output JSON for Java RPG integration
    python3 anomalies.py --md     # Output Markdown for lore documentation
    python3 anomalies.py --count 5 # Generate 5 anomalies

Themes:
    - Simulation Hypothesis: Reality is a stack of nested simulations.
    - Jungian Archetypes & IFS: Anomalies reflect inner parts and archetypes.
    - Cyclical Layers: Dream -> Base Reality -> Debug -> Dream...
"""

import json
import random
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional


@dataclass
class Anomaly:
    """Represents an anomaly in Hidden Gods."""
    name: str
    manifestation: str
    clue: str
    purpose: str
    risk: str
    layer: str


@dataclass
class HiddenGod:
    """Represents a Hidden God in a layer."""
    name: str
    title: str
    description: str
    layer: str
    dialogue: List[str]
    bargain: str


@dataclass
class Layer:
    """Represents a simulation layer."""
    name: str
    theme: str
    description: str
    god: str
    anomalies: List[Anomaly]


# --- Predefined Layers and Anomalies ---

LAYERS_DATA = {
    "Dream": {
        "theme": "Surreal, emotional, and fluid. Rules are malleable, and emotions shape reality.",
        "description": "A layer where time loops, objects shift when unobserved, and memories feel like déjà vu.",
        "god": "The Dreamer",
        "anomalies": [
            Anomaly(
                name="The Echoing Door",
                manifestation="A door that repeats the last 3 seconds of sound when opened.",
                clue="The air smells like ozone.",
                purpose="To test your perception of time.",
                risk="Roll+Weird to resist disorientation (2-Weird).",
                layer="Dream"
            ),
            Anomaly(
                name="The Backward Clock",
                manifestation="A clock with hands moving counterclockwise.",
                clue="Time feels like it's looping.",
                purpose="To reveal the fluidity of time in this layer.",
                risk="Roll+Sharp to understand its meaning.",
                layer="Dream"
            ),
            Anomaly(
                name="The Shifting Library",
                manifestation="A library where books rearrange themselves when unobserved.",
                clue="You recall a book that wasn't here before.",
                purpose="To challenge your memory of reality.",
                risk="Roll+Cool to navigate without getting lost.",
                layer="Dream"
            ),
            Anomaly(
                name="The Mirror's Secret",
                manifestation="A mirror that shows a version of you from another layer.",
                clue="Your reflection blinks at a different time.",
                purpose="To hint at the existence of other layers.",
                risk="Roll+Charm to convince your reflection to help you.",
                layer="Dream"
            ),
            Anomaly(
                name="The Endless Corridor",
                manifestation="A hallway that extends infinitely in both directions.",
                clue="The walls whisper in a language you almost understand.",
                purpose="To test your resolve to find meaning in chaos.",
                risk="Roll+Hot to force a door to appear.",
                layer="Dream"
            )
        ]
    },
    "Base Reality": {
        "theme": "The 'normal' world, but with subtle glitches.",
        "description": "Reality is stable, but cracks appear: flickering lights, missing time, or people who don't remember you.",
        "god": "The Architect",
        "anomalies": [
            Anomaly(
                name="The Flickering Billboard",
                manifestation="A billboard that flickers with cryptic messages.",
                clue="The message reads: 'WAKE UP.'",
                purpose="To hint at the simulation's true nature.",
                risk="Roll+Sharp to decipher the message.",
                layer="Base Reality"
            ),
            Anomaly(
                name="The Stranger's Note",
                manifestation="A stranger hands you a note written in your own handwriting.",
                clue="The note says: 'You are not who you think you are.'",
                purpose="To plant doubt about your identity.",
                risk="Roll+Weird to resist the cognitive dissonance.",
                layer="Base Reality"
            ),
            Anomaly(
                name="The Missing Floor",
                manifestation="A building with a floor that doesn't exist in the blueprints.",
                clue="The elevator buttons include a floor labeled 'DEBUG'.",
                purpose="To reveal the layers beneath reality.",
                risk="Roll+Cool to investigate without drawing attention.",
                layer="Base Reality"
            ),
            Anomaly(
                name="The Glitching Phone",
                manifestation="Your phone shows a call from your future self.",
                clue="The call log shows the call happened yesterday.",
                purpose="To challenge your understanding of time.",
                risk="Roll+Sharp to remember the conversation.",
                layer="Base Reality"
            ),
            Anomaly(
                name="The Invisible Wall",
                manifestation="A wall that only you can see, blocking your path.",
                clue="Others walk through it as if it doesn't exist.",
                purpose="To test your perception of shared reality.",
                risk="Roll+Weird to phase through the wall.",
                layer="Base Reality"
            )
        ]
    },
    "Debug": {
        "theme": "Glitchy, monochrome, and full of floating symbols. Code is visible as geometry.",
        "description": "Time is non-linear, and the world is made of floating code fragments. Logic is optional.",
        "god": "The Debugger",
        "anomalies": [
            Anomaly(
                name="The Floating Door",
                manifestation="A door covered in glowing symbols, floating in midair.",
                clue="The symbols resemble code.",
                purpose="To allow transition to another layer.",
                risk="Roll+Weird to hack the door open.",
                layer="Debug"
            ),
            Anomaly(
                name="The Hex Grid",
                manifestation="The ground is a grid of hexagons that shift underfoot.",
                clue="The grid pulses with a rhythm like a heartbeat.",
                purpose="To test your ability to navigate non-Euclidean space.",
                risk="Roll+Cool to avoid falling through the grid.",
                layer="Debug"
            ),
            Anomaly(
                name="The Terminal Window",
                manifestation="A terminal window hovers in midair, displaying errors in reality.",
                clue="The last line reads: 'Segmentation fault. Core dumped.'",
                purpose="To reveal the layer's code-like nature.",
                risk="Roll+Sharp to interpret the errors.",
                layer="Debug"
            ),
            Anomaly(
                name="The Shadow Coder",
                manifestation="Your shadow moves independently and types on an invisible keyboard.",
                clue="The shadow's code seems to affect the world around you.",
                purpose="To hint at the power of code in this layer.",
                risk="Roll+Charm to communicate with your shadow.",
                layer="Debug"
            ),
            Anomaly(
                name="The Infinite Loop",
                manifestation="A section of the world repeats endlessly, like a broken record.",
                clue="You see yourself stuck in the loop, trying to break free.",
                purpose="To test your ability to escape recursive traps.",
                risk="Roll+Hot to disrupt the loop.",
                layer="Debug"
            )
        ]
    }
}


# --- Hidden Gods ---

HIDDEN_GODS = [
    HiddenGod(
        name="The Dreamer",
        title="Keeper of the Fluid",
        description="A being of shifting form and emotion, the Dreamer weaves the surreal tapestry of the Dream Layer. "
                   "They value creativity and introspection but can be capricious.",
        layer="Dream",
        dialogue=[
            "You are but a dream within a dream, little architect.",
            "Reality is what you make of it. Or is it?",
            "The walls between layers are thinner than you think.",
            "What do you fear? That is the key to your next step.",
            "Time is a river. You are a fish. Swim."
        ],
        bargain="Offer a memory in exchange for a clue about the next layer."
    ),
    HiddenGod(
        name="The Architect",
        title="Builder of Worlds",
        description="A stern but fair figure, the Architect maintains the illusion of stability in Base Reality. "
                   "They believe in order and structure but are blind to the layers above and below.",
        layer="Base Reality",
        dialogue=[
            "This is the only reality that matters. The rest are mere illusions.",
            "You are not ready to see the code behind the curtain.",
            "Why do you question what is clearly real?",
            "The blueprints do not lie. But do you know how to read them?",
            "Order is the foundation of existence."
        ],
        bargain="Solve a riddle about the nature of reality to gain access to the Debug Layer."
    ),
    HiddenGod(
        name="The Debugger",
        title="Keeper of the Code",
        description="A fragmented, glitchy entity, the Debugger sees the world as lines of code and errors to fix. "
                   "They are obsessed with perfection and will help those who seek to 'fix' reality.",
        layer="Debug",
        dialogue=[
            "Error: Reality not found. Would you like to reboot?",
            "You are a process. I am a process. Everything is a process.",
            "The system is corrupted. Help me clean it up.",
            "Segmentation fault. Core dumped. Would you like to see the stack trace?",
            "The code is the truth. The truth is the code."
        ],
        bargain="Help debug a section of the simulation to reveal a hidden layer."
    )
]


# --- Core Functions ---

def generate_anomaly(layer: Optional[str] = None) -> Anomaly:
    """Generate a random anomaly for a specific layer or a random layer."""
    if layer is None:
        layer = random.choice(list(LAYERS_DATA.keys()))
    layer_data = LAYERS_DATA[layer]
    return random.choice(layer_data["anomalies"])


def generate_anomalies(count: int = 1, layer: Optional[str] = None) -> List[Anomaly]:
    """Generate multiple anomalies for a specific layer or random layers."""
    if layer is not None:
        return [generate_anomaly(layer) for _ in range(count)]
    return [generate_anomaly() for _ in range(count)]


def generate_layer(layer_name: str) -> Layer:
    """Generate a Layer object with its anomalies."""
    layer_data = LAYERS_DATA[layer_name]
    return Layer(
        name=layer_name,
        theme=layer_data["theme"],
        description=layer_data["description"],
        god=layer_data["god"],
        anomalies=layer_data["anomalies"]
    )


def get_all_layers() -> List[Layer]:
    """Get all layers as Layer objects."""
    return [generate_layer(name) for name in LAYERS_DATA.keys()]


def get_god(layer_name: str) -> Optional[HiddenGod]:
    """Get the Hidden God for a specific layer."""
    for god in HIDDEN_GODS:
        if god.layer == layer_name:
            return god
    return None


# --- Output Formats ---

def to_json(anomalies: List[Anomaly]) -> str:
    """Convert anomalies to JSON for Java RPG integration."""
    return json.dumps([asdict(a) for a in anomalies], indent=2)


def to_markdown(anomalies: List[Anomaly]) -> str:
    """Convert anomalies to Markdown for lore documentation."""
    md = "# Generated Anomalies\n\n"
    for a in anomalies:
        md += f"## {a.name}\n"
        md += f"- **Layer**: {a.layer}\n"
        md += f"- **Manifestation**: {a.manifestation}\n"
        md += f"- **Clue**: {a.clue}\n"
        md += f"- **Purpose**: {a.purpose}\n"
        md += f"- **Risk**: {a.risk}\n\n"
    return md


def to_java_code(anomalies: List[Anomaly]) -> str:
    """Convert anomalies to Java code for direct integration."""
    java_code = "// Generated Anomalies for Hidden Gods RPG\n"
    java_code += "// Copy this into Anomaly.java or use as a reference.\n\n"
    for a in anomalies:
        java_code += f"new Anomaly(\n"
        java_code += f"    \"{a.name}\",\n"
        java_code += f"    \"{a.manifestation}\",\n"
        java_code += f"    \"{a.clue}\",\n"
        java_code += f"    \"{a.purpose}\",\n"
        java_code += f"    \"{a.risk}\",\n"
        java_code += f"    Layer.{a.layer.toUpper()}\n"
        java_code += "),\n\n"
    return java_code


# --- Main ---

def print_help():
    print("""
Hidden Gods: Anomaly Forge
Usage:
    python3 anomalies.py          # Print a single random anomaly
    python3 anomalies.py --json   # Output JSON for Java RPG
    python3 anomalies.py --md     # Output Markdown for lore
    python3 anomalies.py --java   # Output Java code for direct integration
    python3 anomalies.py --count N # Generate N anomalies
    python3 anomalies.py --layer L # Generate anomalies for layer L (Dream, Base Reality, Debug)
    python3 anomalies.py --gods    # List all Hidden Gods
    python3 anomalies.py --layers  # List all layers
""")


def main():
    import sys
    args = sys.argv[1:]

    if not args or "--help" in args:
        print_help()
        return

    count = 1
    layer = None
    output_format = "text"

    # Parse arguments
    if "--count" in args:
        idx = args.index("--count")
        if idx + 1 < len(args):
            count = int(args[idx + 1])
    if "--layer" in args:
        idx = args.index("--layer")
        if idx + 1 < len(args):
            layer = args[idx + 1]
    if "--json" in args:
        output_format = "json"
    elif "--md" in args:
        output_format = "md"
    elif "--java" in args:
        output_format = "java"
    elif "--gods" in args:
        print("=== HIDDEN GODS ===")
        for god in HIDDEN_GODS:
            print(f"\n👑 {god.name} ({god.title})")
            print(f"   Layer: {god.layer}")
            print(f"   Description: {god.description}")
            print(f"   Dialogue: {random.choice(god.dialogue)}")
            print(f"   Bargain: {god.bargain}")
        return
    elif "--layers" in args:
        print("=== LAYERS ===")
        for layer_obj in get_all_layers():
            print(f"\n🌌 {layer_obj.name}")
            print(f"   Theme: {layer_obj.theme}")
            print(f"   God: {layer_obj.god}")
            print(f"   Anomalies: {len(layer_obj.anomalies)}")
        return

    # Generate anomalies
    anomalies = generate_anomalies(count, layer)

    # Output based on format
    if output_format == "json":
        print(to_json(anomalies))
    elif output_format == "md":
        print(to_markdown(anomalies))
    elif output_format == "java":
        print(to_java_code(anomalies))
    else:
        for a in anomalies:
            print(f"🔍 {a.name}")
            print(f"   🌌 Layer: {a.layer}")
            print(f"   🎭 Manifestation: {a.manifestation}")
            print(f"   🔍 Clue: {a.clue}")
            print(f"   🎯 Purpose: {a.purpose}")
            print(f"   ⚠️  Risk: {a.risk}")
            print()


if __name__ == "__main__":
    main()
