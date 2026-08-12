"""
Hidden Gods Game Engine
======================
Core game state and logic for the Hidden Gods TTRPG.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
import random


# Enums
class Stat(Enum):
    COOL = "Cool"
    HARD = "Hard"
    HOT = "Hot"
    SHARP = "Sharp"
    WEIRD = "Weird"
    HX = "Hx"


class RollOutcome(Enum):
    MISS = "miss"
    PARTIAL = "partial"
    SUCCESS = "success"


# Data Classes
@dataclass
class RollResult:
    dice: List[int]
    total: int
    stat: Optional[Stat] = None
    stat_value: int = 0
    outcome: RollOutcome = RollOutcome.MISS

    @property
    def final_value(self) -> int:
        return self.total + self.stat_value


@dataclass
class Character:
    name: str
    player: str
    archetype: str
    secondary_archetype: Optional[str] = None
    stats: Dict[Stat, int] = field(default_factory=dict)
    moves: List[str] = field(default_factory=list)
    hx: Dict[str, int] = field(default_factory=dict)
    highlighted_stats: List[Stat] = field(default_factory=list)
    ifs_parts: List[str] = field(default_factory=list)
    equipment: List[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class Anomaly:
    name: str
    layer: str
    manifestation: str
    clue: str
    purpose: str
    risk: str
    god: str
    resolved: bool = False


@dataclass
class Layer:
    name: str
    theme: str
    rules: str
    god: str


@dataclass
class Session:
    id: str
    title: str
    date: str
    characters: List[str]
    anomalies_encountered: List[str] = field(default_factory=list)
    log: List[str] = field(default_factory=list)
    current_layer: str = "Base Reality"


# Game State
class GameState:
    def __init__(self):
        self.characters: Dict[str, Character] = {}
        self.sessions: Dict[str, Session] = {}
        self.layers: Dict[str, Layer] = {}
        self.anomalies: Dict[str, Anomaly] = {}
        self.current_session: Optional[Session] = None
        self._load_defaults()

    def _load_defaults(self):
        # Default layers
        for layer in [
            Layer("Base Reality", "Normal life with subtle glitches", 
                  "Standard physics; time is linear; glitches are rare.", "The Architect"),
            Layer("Debug", "Glitchy, monochrome, floating symbols",
                  "Code is visible as geometry; time is non-linear; logic can be rewritten.", "The Debugger"),
            Layer("Dream", "Surreal, emotional, shifting landscapes",
                  "Rules are fluid; emotions shape reality; time is subjective.", "The Dreamer"),
            Layer("Machine", "Mechanical, cold, clockwork",
                  "Everything is a machine; free will is an illusion; determinism reigns.", "The Engineer"),
            Layer("Void", "Empty, silent, infinite",
                  "No rules apply; reality is malleable; time does not exist.", "The Weaver"),
        ]:
            self.layers[layer.name] = layer

        # Default anomalies
        for anomaly in [
            Anomaly("The Whispering Stones", "Base Reality",
                    "A circle of rocks that hum with voices when the wind blows.",
                    "The voices only speak in questions.",
                    "To reveal hidden truths.", "Roll+Sharp to decipher (2-Sharp).", "The Architect"),
            Anomaly("The Echoing Door", "Debug",
                    "A door that repeats the last 3 seconds of sound when opened.",
                    "The air smells like ozone.",
                    "To test the party’s perception of time.", "Roll+Weird to resist disorientation (2-Weird).", "The Debugger"),
            Anomaly("The River That Flows Uphill", "Dream",
                    "A waterway that defies gravity.",
                    "The water sparkles like liquid silver.",
                    "To test the party’s perception of reality.", "Roll+Weird to navigate (2-Weird).", "The Dreamer"),
            Anomaly("The Clockwork NPC", "Machine",
                    "An NPC that moves in perfectly predictable patterns.",
                    "Its gears are visible through its skin.",
                    "To demonstrate the deterministic nature of the layer.", "Roll+Cool to avoid being pulled into its pattern (2-Cool).", "The Engineer"),
            Anomaly("The Man Who Wasn’t There", "Void",
                    "A figure seen in reflections and shadows, but never directly.",
                    "His reflection moves independently.",
                    "To force the party to confront the unseen.", "Roll+Cool to resist fear (2-Cool).", "The Weaver"),
        ]:
            self.anomalies[anomaly.name] = anomaly

    def add_character(self, character: Character):
        self.characters[character.name] = character

    def get_character(self, name: str) -> Optional[Character]:
        return self.characters.get(name)

    def add_session(self, session: Session):
        self.sessions[session.id] = session
        self.current_session = session

    def get_session(self, session_id: str) -> Optional[Session]:
        return self.sessions.get(session_id)

    def roll_dice(self, stat: Optional[Stat] = None, stat_value: int = 0) -> RollResult:
        d1, d2 = random.randint(1, 6), random.randint(1, 6)
        total = d1 + d2 + stat_value
        outcome = RollOutcome.MISS if total <= 6 else (RollOutcome.PARTIAL if total <= 9 else RollOutcome.SUCCESS)
        return RollResult([d1, d2], d1 + d2, stat, stat_value, outcome)

    def resolve_move(self, move_name: str, character_name: str, stat: Stat, stat_value: int) -> str:
        roll = self.roll_dice(stat, stat_value)
        move_outcomes = {
            "Act Under Pressure": {RollOutcome.SUCCESS: "You do it.", RollOutcome.PARTIAL: "You do it, but choose one: it takes longer, you draw attention, or it costs you.", RollOutcome.MISS: "The Facilitator makes a move."},
            "Open Your Brain": {RollOutcome.SUCCESS: "The Navigator whispers a secret: the code is not as it seems.", RollOutcome.PARTIAL: "You sense a presence, but it’s fleeting. Roll+Sharp to decipher.", RollOutcome.MISS: "The psychic maelstrom lashes out. The Facilitator makes a move."},
            "Hack the Code": {RollOutcome.SUCCESS: "The code bends to your will. Describe what happens.", RollOutcome.PARTIAL: "The code resists. Choose: the effect is temporary, or you take 1-Weird harm.", RollOutcome.MISS: "The code fights back. Roll+Cool to avoid a glitch."},
            "Layer Hop": {RollOutcome.SUCCESS: "You arrive safely. Describe the transition.", RollOutcome.PARTIAL: "You arrive, but something is off. The Facilitator introduces a complication.", RollOutcome.MISS: "You’re lost in the void between layers. Roll+Sharp to find your way."},
            "Negotiate with a God": {RollOutcome.SUCCESS: "The god agrees to your terms. Name your price.", RollOutcome.PARTIAL: "The god agrees, but demands something unexpected in return.", RollOutcome.MISS: "The god is offended. Roll+Weird to avoid its wrath."},
        }
        if move_name not in move_outcomes:
            return f"{move_name}: Rolled {roll.final_value} ({roll.outcome.value})."
        outcome = move_outcomes[move_name][roll.outcome]
        if self.current_session:
            self.current_session.log.append(f"{character_name} used {move_name}: {roll.final_value} ({roll.outcome.value})")
        return f"{character_name} used {move_name} ({roll.final_value}): {outcome}"

    def generate_anomaly(self, layer: Optional[str] = None) -> Anomaly:
        candidates = [a for a in self.anomalies.values() if not layer or a.layer == layer]
        return random.choice(candidates) if candidates else random.choice(list(self.anomalies.values()))

    def generate_layer(self) -> Layer:
        return random.choice(list(self.layers.values()))


# Global game state
game_state = GameState()
