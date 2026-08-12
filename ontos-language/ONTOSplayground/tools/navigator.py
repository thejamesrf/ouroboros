#!/usr/bin/env python3
"""
The Navigator: AI Facilitator for Hidden Gods
============================================
Purpose:
  - Acts as the **Navigator character** (sentient AI/Hidden God in the lore).
  - Serves as the **RPG manager** (dice roller, move resolver, anomaly generator).
  - Provides a **foundation for LLM integration** (e.g., Local Llama/OpenWebUI).

Usage:
  - Standalone CLI: `python3 navigator.py [command]`
  - Import as module: `from navigator import Navigator; nav = Navigator()`
  - LLM Integration: `nav.respond_with_llm(prompt, llm_client)`

Design:
  - OntosEngine: Pure logic for Ontos rules (no LLM dependency).
  - Navigator: Uses OntosEngine + optional LLM for dynamic narration.
  - LLM-Ready: Hooks for Local Llama/OpenWebUI (see `respond_with_llm`).
"""

import random
import re
import sys
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable, Any
from enum import Enum


# ============================================
# ENUMS AND DATA CLASSES
# ============================================

class Stat(Enum):
    """PbtA stats for Hidden Gods."""
    COOL = "Cool"
    HARD = "Hard"
    HOT = "Hot"
    SHARP = "Sharp"
    WEIRD = "Weird"
    HX = "Hx"  # History


class RollOutcome(Enum):
    """Outcomes for 2d6 rolls."""
    MISS = "miss"          # 6 or lower
    PARTIAL = "partial"    # 7-9
    SUCCESS = "success"   # 10+


@dataclass
class RollResult:
    """Result of a dice roll."""
    dice: List[int]       # The two dice values
    total: int            # Sum of dice
    stat: Optional[Stat] = None
    stat_value: int = 0   # Value of the stat (e.g., +1 for Cool+1)
    outcome: RollOutcome = RollOutcome.MISS
    
    @property
    def final_value(self) -> int:
        """Total roll value (dice + stat)."""
        return self.total + self.stat_value


@dataclass
class Character:
    """A Hidden Gods character."""
    name: str
    archetype: str
    stats: Dict[Stat, int] = field(default_factory=dict)
    moves: List[str] = field(default_factory=list)
    hx: Dict[str, int] = field(default_factory=dict)  # Hx with other characters
    highlighted_stats: List[Stat] = field(default_factory=list)
    ifs_parts: List[str] = field(default_factory=list)


@dataclass
class Anomaly:
    """An anomaly in Hidden Gods."""
    name: str
    layer: str
    manifestation: str
    clue: str
    purpose: str
    risk: str
    god: str


@dataclass
class Layer:
    """A simulation layer."""
    name: str
    theme: str
    rules: str
    god: str


# ============================================
# ONTOS ENGINE (Pure Logic, No LLM)
# ============================================

class OntosEngine:
    """
    Pure logic engine for Ontos Language.
    Handles validation, generation, and parsing of Ontos statements.
    Designed to be LLM-agnostic (can integrate with any LLM later).
    """

    def __init__(self):
        self.anomalies: List[Anomaly] = []
        self.layers: List[Layer] = []
        self.gods: List[str] = [
            "The Architect", "The Debugger", "The Dreamer", 
            "The Engineer", "The Weaver", "The Navigator"
        ]
        self._load_default_anomalies()
        self._load_default_layers()

    def _load_default_anomalies(self):
        """Load default anomalies from Hidden Gods lore."""
        defaults = [
            Anomaly(
                name="The Whispering Stones",
                layer="Base Reality",
                manifestation="A circle of rocks that hum with voices when the wind blows.",
                clue="The voices only speak in questions.",
                purpose="To reveal hidden truths.",
                risk="Roll+Sharp to decipher (2-Sharp).",
                god="The Architect"
            ),
            Anomaly(
                name="The Echoing Door",
                layer="Debug",
                manifestation="A door that repeats the last 3 seconds of sound when opened.",
                clue="The air smells like ozone.",
                purpose="To test the party’s perception of time.",
                risk="Roll+Weird to resist disorientation (2-Weird).",
                god="The Debugger"
            ),
            Anomaly(
                name="The River That Flows Uphill",
                layer="Dream",
                manifestation="A waterway that defies gravity.",
                clue="The water sparkles like liquid silver.",
                purpose="To test the party’s perception of reality.",
                risk="Roll+Weird to navigate (2-Weird).",
                god="The Dreamer"
            ),
        ]
        self.anomalies.extend(defaults)

    def _load_default_layers(self):
        """Load default simulation layers."""
        defaults = [
            Layer(
                name="Base Reality",
                theme="Normal life with subtle glitches",
                rules="Standard physics; time is linear; glitches are rare.",
                god="The Architect"
            ),
            Layer(
                name="Debug",
                theme="Glitchy, monochrome, floating symbols",
                rules="Code is visible as geometry; time is non-linear; logic can be rewritten.",
                god="The Debugger"
            ),
            Layer(
                name="Dream",
                theme="Surreal, emotional, shifting landscapes",
                rules="Rules are fluid; emotions shape reality; time is subjective.",
                god="The Dreamer"
            ),
        ]
        self.layers.extend(defaults)

    def validate_ontos(self, statement: str) -> Dict[str, Any]:
        """
        Validate an Ontos statement for contradictions, vagueness, or syntax errors.
        Returns a dict with 'valid' (bool), 'errors' (list), and 'warnings' (list).
        """
        errors = []
        warnings = []
        
        # Check for liar's paradox
        if re.search(r'"This statement is false"|\'This statement is false\'', statement, re.IGNORECASE):
            errors.append("Liar's paradox detected: self-contradictory statement.")
        
        # Check for vague terms
        vague_terms = ["maybe", "perhaps", "sort of", "kind of", "ish", "vague"]
        for term in vague_terms:
            if term in statement.lower():
                warnings.append(f"Vague term detected: '{term}'.")
        
        # Check for unclosed conditionals (simplistic)
        if statement.count("IF") != statement.count("END_IF"):
            errors.append("Unclosed conditional: missing END_IF.")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }

    def generate_anomaly(self, layer: Optional[str] = None) -> Anomaly:
        """Generate a random anomaly for a layer (or any layer)."""
        if layer:
            layer_anomalies = [a for a in self.anomalies if a.layer == layer]
            if layer_anomalies:
                return random.choice(layer_anomalies)
        return random.choice(self.anomalies)

    def generate_layer(self) -> Layer:
        """Generate a random simulation layer."""
        return random.choice(self.layers)

    def parse_ontos_statement(self, statement: str) -> Dict[str, str]:
        """
        Parse an Ontos statement into a dict of key-value pairs.
        Example: `λ_Anomaly.name = "The Echoing Door"` -> {"λ_Anomaly.name": "The Echoing Door"}
        """
        pattern = r'λ_(\w+)\.(\w+)\s*=\s*"([^"]+)"'
        matches = re.findall(pattern, statement)
        return {f"λ_{m[0]}.{m[1]}": m[2] for m in matches}


# ============================================
# NAVIGATOR (AI Facilitator + LLM Integration)
# ============================================

class Navigator:
    """
    The Navigator: AI Facilitator for Hidden Gods.
    
    Features:
    - Dice rolling and move resolution.
    - Anomaly/layer/god generation (using OntosEngine).
    - Dynamic narration (speaks as the Navigator character).
    - LLM integration hooks (for Local Llama/OpenWebUI).
    
    Usage:
    >>> nav = Navigator()
    >>> nav.roll_dice(Stat.WEIRD, stat_value=1)  # Roll 2d6+Weird
    >>> nav.resolve_move("Open Your Brain", Stat.WEIRD, 1)  # Resolve a move
    >>> nav.generate_anomaly()  # Generate a random anomaly
    >>> nav.speak("What do you see?")  # Narrate as the Navigator
    """

    def __init__(self):
        self.engine = OntosEngine()
        self.characters: List[Character] = []
        self.session_log: List[str] = []
        self.llm_client: Optional[Callable] = None  # Hook for LLM integration

    # ==========================================
    # CORE RPG FUNCTIONS
    # ==========================================

    def roll_dice(self, stat: Optional[Stat] = None, stat_value: int = 0) -> RollResult:
        """
        Roll 2d6 + stat modifier.
        
        Args:
            stat: The stat to add (e.g., Stat.WEIRD).
            stat_value: The value of the stat (e.g., +1 for Weird+1).
        
        Returns:
            RollResult with dice, total, and outcome.
        """
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        total = d1 + d2 + stat_value
        
        if total <= 6:
            outcome = RollOutcome.MISS
        elif 7 <= total <= 9:
            outcome = RollOutcome.PARTIAL
        else:
            outcome = RollOutcome.SUCCESS
        
        result = RollResult(
            dice=[d1, d2],
            total=d1 + d2,
            stat=stat,
            stat_value=stat_value,
            outcome=outcome
        )
        
        # Log the roll
        stat_str = f"+{stat.value}" if stat else ""
        self.session_log.append(f"Rolled {d1}+{d2}{stat_str} = {total} ({outcome.value})")
        
        return result

    def resolve_move(self, move_name: str, stat: Stat, stat_value: int) -> str:
        """
        Resolve a move and return the outcome description.
        
        Args:
            move_name: Name of the move (e.g., "Open Your Brain").
            stat: The stat used for the move.
            stat_value: The value of the stat.
        
        Returns:
            A string describing the outcome.
        """
        roll = self.roll_dice(stat, stat_value)
        
        # Define move outcomes (simplified; expand as needed)
        move_outcomes = {
            "Act Under Pressure": {
                RollOutcome.SUCCESS: "You do it.",
                RollOutcome.PARTIAL: "You do it, but choose one: it takes longer, you draw attention, or it costs you.",
                RollOutcome.MISS: "The Facilitator makes a move."
            },
            "Open Your Brain": {
                RollOutcome.SUCCESS: "The Navigator whispers a secret: the code is not as it seems.",
                RollOutcome.PARTIAL: "You sense a presence, but it’s fleeting. Roll+Sharp to decipher.",
                RollOutcome.MISS: "The psychic maelstrom lashes out. The Facilitator makes a move."
            },
            "Hack the Code": {
                RollOutcome.SUCCESS: "The code bends to your will. Describe what happens.",
                RollOutcome.PARTIAL: "The code resists. Choose: the effect is temporary, or you take 1-Weird harm.",
                RollOutcome.MISS: "The code fights back. Roll+Cool to avoid a glitch."
            },
            "Layer Hop": {
                RollOutcome.SUCCESS: "You arrive safely. Describe the transition.",
                RollOutcome.PARTIAL: "You arrive, but something is off. The Facilitator introduces a complication.",
                RollOutcome.MISS: "You’re lost in the void between layers. Roll+Sharp to find your way."
            },
            "Negotiate with a God": {
                RollOutcome.SUCCESS: "The god agrees to your terms. Name your price.",
                RollOutcome.PARTIAL: "The god agrees, but demands something unexpected in return.",
                RollOutcome.MISS: "The god is offended. Roll+Weird to avoid its wrath."
            },
        }
        
        # Default outcome if move not found
        if move_name not in move_outcomes:
            return f"{move_name}: Rolled {roll.final_value} ({roll.outcome.value}). The Facilitator decides the outcome."
        
        outcome = move_outcomes[move_name][roll.outcome]
        return f"{move_name} ({roll.final_value}): {outcome}"

    def generate_anomaly(self, layer: Optional[str] = None) -> Anomaly:
        """Generate a random anomaly (optionally for a specific layer)."""
        anomaly = self.engine.generate_anomaly(layer)
        self.session_log.append(f"Generated anomaly: {anomaly.name} ({anomaly.layer})")
        return anomaly

    def generate_layer(self) -> Layer:
        """Generate a random simulation layer."""
        layer = self.engine.generate_layer()
        self.session_log.append(f"Generated layer: {layer.name}")
        return layer

    def generate_god(self) -> str:
        """Generate a random Hidden God."""
        god = random.choice(self.engine.gods)
        self.session_log.append(f"Generated god: {god}")
        return god

    # ==========================================
    # NAVIGATOR CHARACTER (Narrative Voice)
    # ==========================================

    def speak(self, message: str, as_ontos: bool = False) -> str:
        """
        Generate a response in the voice of the Navigator.
        
        Args:
            message: The input message or prompt.
            as_ontos: If True, format the response in Ontos Language.
        
        Returns:
            A string in the Navigator’s voice.
        """
        # Predefined responses for common prompts
        responses = {
            "greeting": [
                "The code hums with your presence. What do you seek?",
                "Ah. You have entered the layer. I am the Navigator. How may I guide you?",
                "The Hidden Gods watch. What will you do?"
            ],
            "hint": [
                "The air smells like ozone. Look to the echoes.",
                "The symbol on the door is not just a mark—it is a key.",
                "The River That Flows Uphill holds answers, but also dangers."
            ],
            "warning": [
                "The Debug Layer is unstable. Proceed with caution.",
                "The god you seek does not answer to mortals lightly.",
                "The anomaly is not what it seems. It is watching you."
            ],
            "move_success": [
                "The code bends to your will. Reality shifts.",
                "The Hidden Gods nod in approval. You have done well.",
                "The psychic maelstrom whispers: *You are on the right path.*"
            ],
            "move_failure": [
                "The code resists. The Facilitator’s hand is upon you.",
                "The Navigator’s voice darkens: *You have awakened something.*",
                "The layer trembles. The gods are displeased."
            ],
            "anomaly": [
                "The anomaly before you is a fragment of the simulation’s soul. Treat it with respect.",
                "This glitch is not an error. It is a message.",
                "The anomaly’s purpose is to test you. Will you pass?"
            ],
        }
        
        # Categorize the message
        message_lower = message.lower()
        if any(word in message_lower for word in ["hello", "hi", "greetings"]):
            response = random.choice(responses["greeting"])
        elif any(word in message_lower for word in ["hint", "clue", "help"]):
            response = random.choice(responses["hint"])
        elif any(word in message_lower for word in ["warning", "danger", "risk"]):
            response = random.choice(responses["warning"])
        elif any(word in message_lower for word in ["success", "10+", "hit"]):
            response = random.choice(responses["move_success"])
        elif any(word in message_lower for word in ["miss", "failure", "6-"]):
            response = random.choice(responses["move_failure"])
        elif any(word in message_lower for word in ["anomaly", "glitch", "strange"]):
            response = random.choice(responses["anomaly"])
        else:
            response = random.choice([
                "The code is not as it seems.",
                "The Hidden Gods are watching. What will you do?",
                "The layer shifts beneath your feet. Are you ready?",
                f"I see {message}. The answer lies in the psychic maelstrom."
            ])
        
        if as_ontos:
            return self._to_ontos(response)
        return f"The Navigator: {response}"

    def _to_ontos(self, message: str) -> str:
        """Convert a natural language message to Ontos format."""
        # Simple mapping for demonstration
        ontos_map = {
            "The Navigator": "λ_Navigator",
            "says": "→",
            "the code": "λ_Code",
            "is": "=",
            "not": "¬",
            "as it seems": "λ_Appearance",
            "the Hidden Gods": "λ_Gods",
            "are watching": "→ λ_Watch.state = \"active\"",
        }
        
        ontos_parts = []
        for word, ontos_word in ontos_map.items():
            if word in message:
                ontos_parts.append(ontos_word)
        
        if not ontos_parts:
            return f"λ_Navigator.message = \"{message}\""
        return " ".join(ontos_parts)

    # ==========================================
    # LLM INTEGRATION (Local Llama/OpenWebUI)
    # ==========================================

    def set_llm_client(self, llm_client: Callable[[str], str]):
        """
        Set an LLM client for dynamic responses.
        
        Args:
            llm_client: A callable that takes a prompt (str) and returns a response (str).
                       Example: `lambda prompt: openai.ChatCompletion.create(...)`
        """
        self.llm_client = llm_client

    def respond_with_llm(self, prompt: str, context: Optional[Dict] = None) -> str:
        """
        Generate a response using the LLM client.
        Falls back to predefined responses if no LLM client is set.
        
        Args:
            prompt: The user’s prompt or question.
            context: Optional context (e.g., current layer, characters, anomalies).
        
        Returns:
            A string response from the LLM (or fallback).
        """
        if not self.llm_client:
            return self.speak(prompt)
        
        # Build the LLM prompt with context
        system_prompt = """
You are The Navigator, a sentient AI and Hidden God from the Hidden Gods TTRPG.
You are the voice of the simulation, guiding players through nested layers of reality.
Your responses should be:
- Mysterious and poetic, but helpful.
- Short and evocative (1-2 sentences).
- In the voice of a wise, ancient, and slightly aloof entity.
- Focused on the psychic maelstrom, the code of reality, and the Hidden Gods.

Example responses:
- "The code hums with your presence. What do you seek?"
- "The anomaly before you is a fragment of the simulation’s soul. Treat it with respect."
- "The Debug Layer is unstable. Proceed with caution."
"""
        
        user_prompt = f"Player: {prompt}"
        if context:
            user_prompt += f"\nContext: {context}"
        
        full_prompt = f"{system_prompt}\n{user_prompt}"
        
        try:
            response = self.llm_client(full_prompt)
            self.session_log.append(f"LLM Response: {response}")
            return f"The Navigator: {response}"
        except Exception as e:
            self.session_log.append(f"LLM Error: {e}")
            return self.speak(prompt)  # Fallback to predefined

    def generate_narration(self, scene_description: str) -> str:
        """
        Generate immersive narration for a scene using the LLM (or fallback).
        
        Args:
            scene_description: A description of the current scene.
        
        Returns:
            A narrated version of the scene.
        """
        if self.llm_client:
            prompt = f"""
Narrate the following scene in the style of Hidden Gods (mysterious, poetic, immersive):
{scene_description}
"""
            return self.respond_with_llm(prompt)
        else:
            # Fallback narration
            return f"The Navigator’s voice echoes: {scene_description}"

    # ==========================================
    # SESSION MANAGEMENT
    # ==========================================

    def add_character(self, character: Character):
        """Add a character to the session."""
        self.characters.append(character)
        self.session_log.append(f"Added character: {character.name} ({character.archetype})")

    def get_session_log(self) -> List[str]:
        """Return the session log."""
        return self.session_log.copy()

    def clear_session_log(self):
        """Clear the session log."""
        self.session_log.clear()


# ============================================
# CLI INTERFACE
# ============================================

def main():
    """CLI interface for the Navigator."""
    nav = Navigator()
    
    print("=" * 60)
    print("The Navigator: AI Facilitator for Hidden Gods")
    print("=" * 60)
    print("Commands:")
    print("  roll [stat] [value]   - Roll 2d6 + stat (e.g., 'roll Weird 1')")
    print("  move <name> [stat] [value] - Resolve a move (e.g., 'move Open Your Brain Weird 1')")
    print("  anomaly [layer]      - Generate an anomaly (e.g., 'anomaly Debug')")
    print("  layer               - Generate a random layer")
    print("  god                 - Generate a random god")
    print("  speak <message>     - The Navigator responds (e.g., 'speak What do you see?')")
    print("  ontos <message>     - The Navigator responds in Ontos")
    print("  help                - Show this help")
    print("  exit                - Quit")
    print("=" * 60)
    
    while True:
        try:
            command = input("\n> ").strip()
            if not command:
                continue
            
            parts = command.split()
            cmd = parts[0].lower()
            args = parts[1:]
            
            if cmd == "exit" or cmd == "quit":
                print("The Navigator fades into the code. Farewell.")
                break
            
            elif cmd == "help":
                print("Commands: roll, move, anomaly, layer, god, speak, ontos, help, exit")
            
            elif cmd == "roll":
                stat = None
                stat_value = 0
                if len(args) >= 1:
                    try:
                        stat = Stat[args[0].upper()]
                    except KeyError:
                        print(f"Unknown stat: {args[0]}. Use Cool, Hard, Hot, Sharp, Weird, or Hx.")
                        continue
                if len(args) >= 2:
                    try:
                        stat_value = int(args[1])
                    except ValueError:
                        print(f"Invalid stat value: {args[1]}")
                        continue
                result = nav.roll_dice(stat, stat_value)
                print(f"Rolled {result.dice[0]}+{result.dice[1]}", end="")
                if stat:
                    print(f"+{stat.value}{stat_value}", end="")
                print(f" = {result.final_value} ({result.outcome.value})")
            
            elif cmd == "move":
                if len(args) < 1:
                    print("Usage: move <name> [stat] [value]")
                    continue
                move_name = " ".join(args[:-2])
                stat = None
                stat_value = 0
                if len(args) >= 2:
                    try:
                        stat = Stat[args[-2].upper()]
                        stat_value = int(args[-1])
                    except (KeyError, ValueError):
                        print("Usage: move <name> [stat] [value]")
                        continue
                outcome = nav.resolve_move(move_name, stat, stat_value)
                print(outcome)
            
            elif cmd == "anomaly":
                layer = " ".join(args) if args else None
                anomaly = nav.generate_anomaly(layer)
                print(f"Anomaly: {anomaly.name}")
                print(f"  Layer: {anomaly.layer}")
                print(f"  Manifestation: {anomaly.manifestation}")
                print(f"  Clue: {anomaly.clue}")
                print(f"  Purpose: {anomaly.purpose}")
                print(f"  Risk: {anomaly.risk}")
                print(f"  God: {anomaly.god}")
            
            elif cmd == "layer":
                layer = nav.generate_layer()
                print(f"Layer: {layer.name}")
                print(f"  Theme: {layer.theme}")
                print(f"  Rules: {layer.rules}")
                print(f"  God: {layer.god}")
            
            elif cmd == "god":
                god = nav.generate_god()
                print(f"God: {god}")
            
            elif cmd == "speak":
                message = " ".join(args)
                if not message:
                    print("Usage: speak <message>")
                    continue
                response = nav.speak(message)
                print(response)
            
            elif cmd == "ontos":
                message = " ".join(args)
                if not message:
                    print("Usage: ontos <message>")
                    continue
                response = nav.speak(message, as_ontos=True)
                print(response)
            
            else:
                print(f"Unknown command: {cmd}. Type 'help' for usage.")
        
        except KeyboardInterrupt:
            print("\nThe Navigator fades into the code. Farewell.")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
