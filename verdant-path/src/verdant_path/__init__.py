"""Ouroboros Verdant Path — resilience-focused training, recovery, and lifestyle.

A library modeling the Verdant Path training philosophy: progressive oscillation,
auto-regulation via embodied awareness, TRIMP-based training stress, and fatigue
color cues. Pairs workout planning with daily check-ins, habit tracking, and
reflective journaling.
"""

from verdant_path.fatigue import Fatigue, fatigue_from_checkin, readiness_adjustment
from verdant_path.habits import NINETY_DAY_PROGRAM, habit_score, habit_streak
from verdant_path.metrics import acwr, weekly_review
from verdant_path.movements import MOVEMENT_PATTERNS, Movement, Pattern
from verdant_path.planner import Planner, SPLITS, split_for_frequency
from verdant_path.session import SessionBlock, SessionTemplate, WorkoutPlan
from verdant_path.tracker import CheckIn, JournalEntry, SetLog, WorkoutLog
from verdant_path.trimp import TRIMP, trimp_level, trimp_for_session

__version__ = "0.1.0"

__all__ = [
    "Fatigue",
    "fatigue_from_checkin",
    "readiness_adjustment",
    "NINETY_DAY_PROGRAM",
    "habit_score",
    "habit_streak",
    "acwr",
    "weekly_review",
    "MOVEMENT_PATTERNS",
    "Movement",
    "Pattern",
    "Planner",
    "SPLITS",
    "split_for_frequency",
    "SessionBlock",
    "SessionTemplate",
    "WorkoutPlan",
    "CheckIn",
    "JournalEntry",
    "SetLog",
    "WorkoutLog",
    "TRIMP",
    "trimp_level",
    "trimp_for_session",
]
