"""The Ouroboros Project — tools for nested simulations.

This package turns the project's prose specs into runnable code:

* :mod:`ouroboros.ontos`      — validate, parse, and generate Ontos statements
* :mod:`ouroboros.translate`  — Ontos ↔ English translation
* :mod:`ouroboros.anomalies`  — the Anomaly Forge for Hidden Gods sessions
* :mod:`ouroboros.realms`     — typed loaders for simulation-realm data
* :mod:`ouroboros.cli`        — the ``ouroboros`` command-line interface

Run ``ouroboros demo`` to see everything working end-to-end.
"""

from __future__ import annotations

__version__ = "0.2.0"

__all__ = ["__version__"]
