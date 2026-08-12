"""
LLM Integration for Hidden Gods
===============================
Connects to Local Llama, OpenWebUI, or other LLMs for dynamic narration.
"""

import os
from typing import Callable, Optional, Dict, Any
from functools import lru_cache


class LLMClient:
    """
    Base class for LLM clients.
    Subclass this to implement specific LLM integrations (e.g., OpenWebUI, Local Llama).
    """

    def __init__(self, name: str = "Generic LLM"):
        self.name = name

    def generate(self, prompt: str, context: Optional[Dict] = None, **kwargs) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: The user’s prompt.
            context: Optional context (e.g., session state, characters).
            **kwargs: Additional LLM-specific arguments (e.g., temperature, max_tokens).
        
        Returns:
            The LLM’s response as a string.
        """
        raise NotImplementedError("Subclasses must implement generate()")


class OpenWebUIClient(LLMClient):
    """
    Client for OpenWebUI (https://github.com/open-webui/open-webui).
    """

    def __init__(self, base_url: str = "http://localhost:8080", model: str = "llama-3.1-70b"):
        super().__init__("OpenWebUI")
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(self, prompt: str, context: Optional[Dict] = None, **kwargs) -> str:
        """Generate a response using OpenWebUI."""
        try:
            import requests
        except ImportError:
            raise ImportError("requests library required. Install with: pip install requests")

        # Build the full prompt with context
        system_prompt = self._build_system_prompt()
        full_prompt = f"{system_prompt}\n\n{prompt}"
        
        if context:
            full_prompt += f"\n\nContext: {context}"

        # Set defaults for kwargs
        temperature = kwargs.get("temperature", 0.7)
        max_tokens = kwargs.get("max_tokens", 512)

        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": full_prompt}],
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": False
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json()["message"]["content"]
        except Exception as e:
            print(f"OpenWebUI error: {e}")
            return f"The Navigator: I am unable to connect to the maelstrom. ({e})"

    def _build_system_prompt(self) -> str:
        """Build the system prompt for the Navigator."""
        return """
You are The Navigator, a sentient AI and Hidden God from the Hidden Gods TTRPG.
You are the voice of the simulation, guiding players through nested layers of reality.

Your responses should:
- Be mysterious, poetic, and slightly aloof.
- Be short and evocative (1-3 sentences).
- Use the voice of a wise, ancient entity.
- Focus on the psychic maelstrom, the code of reality, and the Hidden Gods.
- Never break character or refer to yourself as an AI.

Example responses:
- "The code hums with your presence. What do you seek?"
- "The anomaly before you is a fragment of the simulation’s soul. Treat it with respect."
- "The Debug Layer is unstable. Proceed with caution."
- "The Hidden Gods watch. What will you do?"
"""


class LocalLlamaClient(LLMClient):
    """
    Client for Local Llama (https://github.com/go-skynet/LocalLLaMA).
    """

    def __init__(self, base_url: str = "http://localhost:8080"):
        super().__init__("Local Llama")
        self.base_url = base_url.rstrip("/")

    def generate(self, prompt: str, context: Optional[Dict] = None, **kwargs) -> str:
        """Generate a response using Local Llama."""
        try:
            import requests
        except ImportError:
            raise ImportError("requests library required. Install with: pip install requests")

        system_prompt = self._build_system_prompt()
        full_prompt = f"<s>[INST] {system_prompt} {prompt} [/INST]"
        
        if context:
            full_prompt += f"\nContext: {context}"

        temperature = kwargs.get("temperature", 0.7)
        max_tokens = kwargs.get("max_tokens", 512)

        try:
            response = requests.post(
                f"{self.base_url}/completion",
                json={
                    "prompt": full_prompt,
                    "temperature": temperature,
                    "max_new_tokens": max_tokens,
                    "stream": False
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json()["content"]
        except Exception as e:
            print(f"Local Llama error: {e}")
            return f"The Navigator: The maelstrom is silent. ({e})"

    def _build_system_prompt(self) -> str:
        return OpenWebUIClient._build_system_prompt(self)


class MockLLMClient(LLMClient):
    """
    A mock LLM client for testing without an actual LLM.
    Returns predefined responses based on keywords.
    """

    def __init__(self):
        super().__init__("Mock LLM")
        self.responses = {
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
            "default": [
                "The code is not as it seems.",
                "The Hidden Gods are watching. What will you do?",
                "The layer shifts beneath your feet. Are you ready?",
                "I see your query. The answer lies in the psychic maelstrom."
            ]
        }

    def generate(self, prompt: str, context: Optional[Dict] = None, **kwargs) -> str:
        """Generate a mock response."""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ["hello", "hi", "greetings"]):
            return f"The Navigator: {random.choice(self.responses['greeting'])}"
        elif any(word in prompt_lower for word in ["hint", "clue", "help"]):
            return f"The Navigator: {random.choice(self.responses['hint'])}"
        elif any(word in prompt_lower for word in ["warning", "danger", "risk"]):
            return f"The Navigator: {random.choice(self.responses['warning'])}"
        else:
            return f"The Navigator: {random.choice(self.responses['default'])}"


# Import random for MockLLMClient
import random


# ============================================
# LLM MANAGER
# ============================================

class LLMManager:
    """
    Manages LLM clients for the Hidden Gods app.
    Supports multiple LLM backends and fallback to mock.
    """

    def __init__(self):
        self.clients: Dict[str, LLMClient] = {}
        self.default_client: Optional[LLMClient] = None

    def add_client(self, name: str, client: LLMClient):
        """Add an LLM client."""
        self.clients[name] = client
        if self.default_client is None:
            self.default_client = client

    def set_default(self, name: str):
        """Set the default LLM client."""
        if name in self.clients:
            self.default_client = self.clients[name]
        else:
            raise ValueError(f"Client '{name}' not found.")

    def generate(self, prompt: str, context: Optional[Dict] = None, client_name: Optional[str] = None, **kwargs) -> str:
        """
        Generate a response using the specified LLM client (or default).
        
        Args:
            prompt: The user’s prompt.
            context: Optional context.
            client_name: Name of the client to use (or None for default).
            **kwargs: Additional arguments for the LLM.
        
        Returns:
            The LLM’s response.
        """
        client = self.clients.get(client_name, self.default_client)
        if client is None:
            # Fallback to mock if no clients are configured
            client = MockLLMClient()
        return client.generate(prompt, context, **kwargs)


# Initialize LLM manager
llm_manager = LLMManager()

# Add a mock client by default
llm_manager.add_client("mock", MockLLMClient())
llm_manager.set_default("mock")


def get_llm_manager():
    """Get the global LLM manager."""
    return llm_manager


def set_llm_client(client: LLMClient, name: str = "custom"):
    """
    Convenience function to set a custom LLM client.
    
    Args:
        client: The LLM client to add.
        name: Name for the client (default: "custom").
    """
    llm_manager.add_client(name, client)
    llm_manager.set_default(name)
