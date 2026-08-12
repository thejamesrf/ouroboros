"""
Hidden Gods Session Management
===============================
Handles session creation, logging, and state.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import uuid

from . import game_state, Session, Character, Anomaly, Layer


class SessionManager:
    """Manages game sessions for Hidden Gods."""

    def __init__(self):
        self.game_state = game_state

    def create_session(self, title: str, character_names: List[str], layer: str = "Base Reality") -> Session:
        """Create a new session."""
        session_id = str(uuid.uuid4())[:8]
        session = Session(
            id=session_id,
            title=title,
            date=datetime.now().strftime("%Y-%m-%d %H:%M"),
            characters=character_names,
            current_layer=layer
        )
        self.game_state.add_session(session)
        return session

    def end_session(self) -> Optional[Session]:
        """End the current session and return it."""
        session = self.game_state.current_session
        if session:
            self.game_state.current_session = None
        return session

    def add_to_log(self, message: str):
        """Add a message to the current session log."""
        if self.game_state.current_session:
            self.game_state.current_session.log.append(message)

    def add_anomaly_encounter(self, anomaly_name: str):
        """Record an anomaly encounter in the current session."""
        if self.game_state.current_session:
            self.game_state.current_session.anomalies_encountered.append(anomaly_name)

    def change_layer(self, layer_name: str) -> str:
        """Change the current layer and log the transition."""
        if not self.game_state.current_session:
            return "No active session."
        
        old_layer = self.game_state.current_session.current_layer
        self.game_state.current_session.current_layer = layer_name
        
        log_message = f"Transitioned from {old_layer} to {layer_name}"
        self.add_to_log(log_message)
        return log_message

    def get_session_summary(self) -> Dict[str, Any]:
        """Get a summary of the current session."""
        if not self.game_state.current_session:
            return {"error": "No active session"}
        
        session = self.game_state.current_session
        return {
            "id": session.id,
            "title": session.title,
            "date": session.date,
            "current_layer": session.current_layer,
            "characters": session.characters,
            "anomalies_encountered": session.anomalies_encountered,
            "log_size": len(session.log),
            "last_log_entry": session.log[-1] if session.log else None
        }


# Initialize session manager
session_manager = SessionManager()
