"""
Hidden Gods Moves
=================
Expanded move definitions and resolutions.
"""

from typing import Dict, Any
from enum import Enum
from . import Stat, RollOutcome, game_state


# Expanded move definitions
MOVES = {
    # Basic Moves
    "Act Under Pressure": {
        "stat": Stat.COOL,
        "description": "When you do something risky or under stress.",
        "outcomes": {
            RollOutcome.SUCCESS: "You do it.",
            RollOutcome.PARTIAL: "You do it, but choose one: it takes longer, you draw attention, or it costs you.",
            RollOutcome.MISS: "The Facilitator makes a move."
        }
    },
    "Go Aggro": {
        "stat": Stat.HARD,
        "description": "When you threaten or attack someone directly.",
        "outcomes": {
            RollOutcome.SUCCESS: "They have to choose: force your hand and suck it up, or cave and do what you want.",
            RollOutcome.PARTIAL: "They can choose one of the above, or: get the hell out of your way, barricade themselves securely in, give you something they think you want, or back off calmly, hands where you can see.",
            RollOutcome.MISS: "Be prepared for the worst."
        }
    },
    "Seduce or Manipulate": {
        "stat": Stat.HOT,
        "description": "When you try to influence someone through charm, persuasion, or deception.",
        "outcomes": {
            RollOutcome.SUCCESS: "They’ll go along with you unless something betrays your intent.",
            RollOutcome.PARTIAL: "They’ll go along but need some assurance first.",
            RollOutcome.MISS: "Be prepared for the worst."
        }
    },
    "Read a Situation": {
        "stat": Stat.SHARP,
        "description": "When you assess a scene or situation.",
        "outcomes": {
            RollOutcome.SUCCESS: "Ask 3 questions from the list below.",
            RollOutcome.PARTIAL: "Ask 1 question.",
            RollOutcome.MISS: "Ask 1 anyway, but be prepared for the worst."
        },
        "questions": [
            "What’s my best escape route/way in/way past?",
            "Which enemy is most vulnerable to me?",
            "Which enemy is the biggest threat?",
            "What should I be on the lookout for?",
            "What’s my enemy’s true position?",
            "Who’s in control here?"
        ]
    },
    "Read a Person": {
        "stat": Stat.SHARP,
        "description": "When you study someone in a charged interaction.",
        "outcomes": {
            RollOutcome.SUCCESS: "Hold 3.",
            RollOutcome.PARTIAL: "Hold 1.",
            RollOutcome.MISS: "Ask 1 anyway, but be prepared for the worst."
        },
        "hold_questions": [
            "Are you telling the truth?",
            "What are you really feeling?",
            "What do you intend to do?",
            "What do you wish I’d do?",
            "How could I get you to ___?"
        ]
    },
    "Open Your Brain": {
        "stat": Stat.WEIRD,
        "description": "When you open your mind to the psychic maelstrom.",
        "outcomes": {
            RollOutcome.SUCCESS: "The Facilitator tells you something new and interesting with good detail.",
            RollOutcome.PARTIAL: "You get an impression.",
            RollOutcome.MISS: "Be prepared for the worst."
        }
    },
    "Help or Interfere": {
        "stat": Stat.HX,
        "description": "When you assist or hinder someone making a roll.",
        "outcomes": {
            RollOutcome.SUCCESS: "They get +2 (help) or -2 (interfere) to their roll.",
            RollOutcome.PARTIAL: "They get +1 or -1.",
            RollOutcome.MISS: "Be prepared for the worst."
        }
    },
    
    # Special Moves (Archetype-Specific)
    "World-Shaper": {
        "stat": Stat.WEIRD,
        "description": "When you describe a new aspect of the world, it becomes real.",
        "archetype": "The Creator",
        "outcomes": {
            RollOutcome.SUCCESS: "It manifests perfectly.",
            RollOutcome.PARTIAL: "It manifests but with a twist.",
            RollOutcome.MISS: "It manifests in a dangerous or unexpected way."
        }
    },
    "Deep Insight": {
        "stat": Stat.SHARP,
        "description": "When you seek understanding of a person or situation.",
        "archetype": "The Sage",
        "outcomes": {
            RollOutcome.SUCCESS: "Ask 3 questions.",
            RollOutcome.PARTIAL: "Ask 1 question.",
            RollOutcome.MISS: "The Facilitator makes a move."
        }
    },
    "Defy Authority": {
        "stat": Stat.HOT,
        "description": "When you challenge a rule or norm.",
        "archetype": "The Rebel",
        "outcomes": {
            RollOutcome.SUCCESS: "You inspire others to question as well.",
            RollOutcome.PARTIAL: "You inspire others, but draw unwanted attention.",
            RollOutcome.MISS: "Be prepared for the worst."
        }
    },
    "Pathfinder": {
        "stat": Stat.SHARP,
        "description": "When you navigate unfamiliar terrain.",
        "archetype": "The Explorer",
        "outcomes": {
            RollOutcome.SUCCESS: "You find the safest route and avoid dangers.",
            RollOutcome.PARTIAL: "You find a route but face a hazard.",
            RollOutcome.MISS: "You’re lost. The Facilitator makes a move."
        }
    },
    "Curiosity’s Reward": {
        "stat": Stat.WEIRD,
        "description": "When you investigate an anomaly.",
        "archetype": "The Explorer",
        "outcomes": {
            RollOutcome.SUCCESS: "You uncover a hidden truth or secret.",
            RollOutcome.PARTIAL: "You uncover a clue, but at a cost.",
            RollOutcome.MISS: "The anomaly lashes out. The Facilitator makes a move."
        }
    },
    "Hack the Code": {
        "stat": Stat.WEIRD,
        "description": "When you manipulate the simulation’s rules.",
        "archetype": "The Magician",
        "outcomes": {
            RollOutcome.SUCCESS: "The code bends to your will. Describe what happens.",
            RollOutcome.PARTIAL: "The code resists. Choose: the effect is temporary, or you take 1-Weird harm.",
            RollOutcome.MISS: "The code fights back. Roll+Cool to avoid a glitch."
        }
    },
    "Layer Hop": {
        "stat": Stat.COOL,
        "description": "When you move between simulation layers.",
        "archetype": "The Explorer",
        "outcomes": {
            RollOutcome.SUCCESS: "You arrive safely. Describe the transition.",
            RollOutcome.PARTIAL: "You arrive, but something is off. The Facilitator introduces a complication.",
            RollOutcome.MISS: "You’re lost in the void between layers. Roll+Sharp to find your way."
        }
    },
    "Negotiate with a God": {
        "stat": Stat.HOT,
        "description": "When you bargain with a Hidden God.",
        "archetype": None,
        "outcomes": {
            RollOutcome.SUCCESS: "The god agrees to your terms. Name your price.",
            RollOutcome.PARTIAL: "The god agrees, but demands something unexpected in return.",
            RollOutcome.MISS: "The god is offended. Roll+Weird to avoid its wrath."
        }
    },
    
    # Introspection Moves
    "Inner Dialogue": {
        "stat": Stat.WEIRD,
        "description": "When you engage in inner dialogue between your parts.",
        "outcomes": {
            RollOutcome.SUCCESS: "You gain insight into a conflict between your parts and can choose to resolve it or let it continue.",
            RollOutcome.PARTIAL: "You gain insight but must act on it immediately.",
            RollOutcome.MISS: "The conflict between your parts intensifies."
        }
    },
    "Shadow Work": {
        "stat": Stat.SHARP,
        "description": "When you confront a difficult truth about yourself.",
        "outcomes": {
            RollOutcome.SUCCESS: "You integrate this truth and gain +1 forward related to it.",
            RollOutcome.PARTIAL: "You acknowledge the truth but struggle to accept it.",
            RollOutcome.MISS: "You resist the truth and suffer -1 forward related to it."
        }
    },
    "Archetype Reflection": {
        "stat": Stat.COOL,
        "description": "When you reflect on how your archetype is manifesting.",
        "outcomes": {
            RollOutcome.SUCCESS: "You understand your archetype’s influence and can choose to embrace or challenge it.",
            RollOutcome.PARTIAL: "You see your archetype’s influence but can’t change it yet.",
            RollOutcome.MISS: "Your archetype controls you in an unexpected way."
        }
    }
}


def get_move(move_name: str) -> Dict[str, Any]:
    """Get a move by name."""
    return MOVES.get(move_name, {})


def resolve_move(move_name: str, character_name: str, stat_value: int, stat: Stat = None) -> str:
    """
    Resolve a move with expanded logic.
    
    Args:
        move_name: Name of the move.
        character_name: Name of the character.
        stat_value: Value of the stat (e.g., +1 for Weird+1).
        stat: The stat to use (defaults to the move's stat).
    
    Returns:
        A string describing the outcome.
    """
    move = get_move(move_name)
    if not move:
        return f"Unknown move: {move_name}"
    
    # Use the move's default stat if not provided
    if stat is None:
        stat = move.get("stat", Stat.COOL)
    
    # Roll the dice
    roll = game_state.roll_dice(stat, stat_value)
    
    # Get the outcome
    outcome = move["outcomes"].get(roll.outcome, "The Facilitator decides the outcome.")
    
    # Special handling for moves with questions/holds
    if move_name == "Read a Situation" and roll.outcome != RollOutcome.MISS:
        num_questions = 3 if roll.outcome == RollOutcome.SUCCESS else 1
        outcome += f" Questions: {', '.join(move['questions'][:num_questions])}"
    
    if move_name == "Read a Person" and roll.outcome != RollOutcome.MISS:
        num_holds = 3 if roll.outcome == RollOutcome.SUCCESS else 1
        outcome += f" Hold {num_holds}: {', '.join(move['hold_questions'][:num_holds])}"
    
    # Log the move
    if game_state.current_session:
        game_state.current_session.log.append(
            f"{character_name} used {move_name}: {roll.final_value} ({roll.outcome.value})"
        )
    
    return f"{character_name} used {move_name} ({roll.final_value}): {outcome}"


def list_moves(archetype: Optional[str] = None) -> List[str]:
    """List all moves, optionally filtered by archetype."""
    if archetype:
        return [name for name, move in MOVES.items() if move.get("archetype") == archetype]
    return list(MOVES.keys())
