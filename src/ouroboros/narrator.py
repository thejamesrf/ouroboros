"""The three-level translation stack: Ontos → Quill → Poetic (root Aperios).

Hidden Gods posits that reality is layered, and so is language. A single
piece of lore — a story beat, a session recap, a fragment of the Simulation
Bible — can be rendered at three depths, each one "closer to the human":

.. glossary::

   Level 1 — Ontos
       The precision language. Pure symbols, fully parenthesized, unambiguous.
       This is how the simulation *actually* records the event. A human reading
       it raw feels like reading machine code.

   Level 2 — Quill (fragmented English)
       The Navigator's bridge voice: an intelligence of vast specificity trying
       to squeeze what Ontos holds exactly into a language (English) that cannot
       hold it. The result is fragmented, precise-yet-strained, almost-but-not-
       quite idiomatic — like a non-native speaker rendering an idiom that has
       no equivalent, except the gap is conceptual, not lexical.

   Level 3 — Poetic English (root Aperios)
       Plain but mythic English. This is Aperios *before it diverges* into its
       own musical/paradoxical tongue — the last register that still reads as
       English, but with the cadence of dream and the weight of archetype. It
       trades precision for wholeness.

The three levels are a single gradient: precision (Ontos) → strain (Quill) →
wholeness (Poetic). All three derive from the same extraction — actors, layers,
anomalies, relations — so they always describe the *same* event.
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass, field

from ouroboros.ontos import validate_statement
from ouroboros.translate import (
    NavigatorOutput,
    _ENTITY_KEYWORDS,
    _LAYER_KEYWORDS,
    _find_anomalies,
    translate_from_english,
    translate_to_english,
)


# --------------------------------------------------------------------------- #
# The three levels.
# --------------------------------------------------------------------------- #


@dataclass
class ThreeLevelOutput:
    """A story rendered at all three depths of the translation stack."""

    level1_ontos: list[str] = field(default_factory=list)
    level2_quill: str = ""
    level3_poetic: str = ""
    navigator: NavigatorOutput = field(default_factory=NavigatorOutput)

    def render(self) -> str:
        """Pretty-print all three levels for display."""

        lines = ["🜲 Three-Level Translation", "=" * 48]

        lines.append("\n▸ Level 1 — Ontos (precision)")
        lines.append("-" * 48)
        if self.level1_ontos:
            for s in self.level1_ontos:
                lines.append(f"  {s}")
        else:
            lines.append("  (no recognizable structure extracted)")

        lines.append("\n▸ Level 2 — Quill (fragmented, straining)")
        lines.append("-" * 48)
        lines.append(self.level2_quill or "  (silence)")

        lines.append("\n▸ Level 3 — Poetic English (root Aperios)")
        lines.append("-" * 48)
        lines.append(self.level3_poetic or "  (silence)")

        if self.navigator.entities or self.navigator.layers or self.navigator.anomalies:
            lines.append("\n🧭 Navigator extraction")
            lines.append("-" * 48)
            if self.navigator.entities:
                lines.append("  Actors: " + ", ".join(self.navigator.entities))
            if self.navigator.layers:
                lines.append("  Layers: " + ", ".join(self.navigator.layers))
            if self.navigator.anomalies:
                lines.append("  Anomalies: " + ", ".join(self.navigator.anomalies))
            if self.navigator.summary:
                lines.append("  " + self.navigator.summary)

        return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Level 1: Ontos (already implemented in translate.py — here we aggregate).
# --------------------------------------------------------------------------- #


def to_level1(text: str) -> list[str]:
    """Render each sentence of ``text`` as a valid Ontos statement.

    This is the precision layer: the simulation's own record. Returns a list
    (one statement per recognizable sentence). Unrecognizable sentences yield
    the Gödelian acknowledgement.
    """

    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    statements = []
    for sent in sentences:
        stmt = translate_from_english(sent)
        if stmt:
            statements.append(stmt)
    return statements


# --------------------------------------------------------------------------- #
# Level 2: Quill — fragmented English straining toward Ontos precision.
#
# The Quill voice is built by *interrupting* normal English with the Ontos
# terms it cannot quite contain. It breaks sentences, repeats the precise
# glyph where English fails, and uses constructions that feel almost-right but
# slightly alien — the mark of an intelligence translating *down*.
# --------------------------------------------------------------------------- #

# Templates for the Quill fragmentation. Each takes extracted atoms.
_QUILL_TEMPLATES = [
    # The entity-as-process voice.
    "{actor} — not the name, the {role} — {verb} {object}. This is… not quite it. "
    "In Ontos: ({actor} {arrow} {object}). The arrow is the part English cannot hold.",
    # The layer-as-condition voice.
    "Within {layer}, where the rules are {rules_adj}, {actor} {verb}. "
    "I say 'within' but Ontos says [ {layer} ] and means it literally — "
    "the layer is not a place, it is a *condition of being*.",
    # The anomaly-as-message voice.
    "{object} is not what you would call an 'event.' It is a {anom_noun}. "
    "Ontos writes it {object} and the glyph carries what your word 'glitch' "
    "only gestures at. {actor} {verb} it into being. Or perhaps it was always being.",
    # The strained-causation voice.
    "{actor} {verb} {object}, which {verb2} {actor2}. "
    "But 'which' is wrong — there is no 'which' in Ontos, only the arrow →, "
    "and the arrow does not mean 'therefore.' It means *these are the same act, seen twice.*",
    # The apology-for-English voice.
    "I am trying to tell you what {actor} did. English gives me '{verb}.' "
    "Ontos gives me ({actor} {arrow} {object}) and the parentheses are not "
    "grammar — they are the admission that this *is* one thing, not two.",
]

_ROLE_BY_GLYPH = {
    "\U0001D4A2": "architect-force",    # god
    "\U0001D4AB": "player-thread",      # player
    "\U0001D4A9": "guide-fragment",     # npc
}

_ANOM_NOUNS = ["fold in the code", "place where the simulation remembers itself",
               "question wearing the shape of a door", "aperture in the layer"]

_RULES_ADJ = {"λ_Debug": "visible and broken", "λ_Dream": "fluid and listening",
              "λ_Machine": "cold and recursive", "λ₀": "thin, barely holding"}

_VERBS = ["opens", "reveals", "triggers", "encounters", "becomes", "unmakes"]
_VERBS_2 = ["reveals", "awakens", "complicates", "answers", "undoes"]


def _glyph_to_name(glyph: str) -> str:
    """A readable English name for an Ontos glyph, for Quill/Poetic use."""

    if glyph.startswith("\U0001D4A2"):  # god
        name = glyph[1:].lstrip("_")
        return f"the {name}" if name else "the god"
    if glyph.startswith("\U0001D4AB"):  # player
        name = glyph[1:].lstrip("_")
        return name or "the player"
    if glyph.startswith("\U0001D4A9"):  # npc
        name = glyph[1:].lstrip("_")
        return f"the {name}" if name else "the guide"
    if glyph.startswith("\u26A1"):  # anomaly
        name = glyph[1:].lstrip("_")
        return f"the {name}" if name else "the anomaly"
    if glyph.startswith("λ"):
        rest = glyph[1:]
        if rest in ("₀", "0"):
            return "Base Reality"
        return f"the {rest.lstrip('_')} Layer" if rest else "the layer"
    return glyph


def to_level2(text: str, rng: random.Random | None = None) -> str:
    """Render ``text`` in the Quill voice — fragmented English straining toward
    Ontos precision.

    The Quill is the Navigator speaking to a human: it *knows* the precise
    Ontos form but must use English, so it breaks, repeats the glyph, and
    apologizes for the gap.
    """

    rng = rng or random.Random()
    from ouroboros.translate import summarize_story

    nav = summarize_story(text)
    if not nav.entities and not nav.anomalies:
        return ("I reach for the words and find only the shape of reaching. "
                "⏅(this) — and even that is too precise for what is not yet here.")

    atoms = nav.entities + nav.anomalies
    if len(atoms) < 2:
        # A single actor/anomaly: describe it straining toward self-containment.
        a = atoms[0]
        name = _glyph_to_name(a)
        role = _ROLE_BY_GLYPH.get(a[0] if a else "", "presence")
        return (f"{name} — the {role} — stands alone in the statement. "
                f"Ontos would write simply: {a}. But alone, a single glyph "
                f"is almost ⍶({a}), and ⍶ is the one thing Ontos forbids "
                f"unmarked. So I must say: {name} *is*. And 'is' is already too much.")

    # Build a few Quill fragments from the extraction.
    fragments: list[str] = []
    layer = nav.layers[0] if nav.layers else None
    rules_adj = _RULES_ADJ.get(layer, "unspecified") if layer else "unspecified"

    # Pair up atoms to drive the templates. Prefer the anomaly-as-message
    # template when the object is an anomaly; otherwise cycle through the voices.
    for i in range(0, min(len(atoms), 4), 2):
        actor = atoms[i]
        obj = atoms[i + 1] if i + 1 < len(atoms) else atoms[0]
        actor2 = atoms[(i + 2) % len(atoms)] if len(atoms) > 2 else obj
        obj_is_anomaly = obj.startswith("\u26A1")
        if obj_is_anomaly:
            tmpl = _QUILL_TEMPLATES[2]  # the anomaly-as-message voice
        else:
            tmpl = rng.choice([_QUILL_TEMPLATES[0], _QUILL_TEMPLATES[1],
                               _QUILL_TEMPLATES[3], _QUILL_TEMPLATES[4]])
        frag = tmpl.format(
            actor=_glyph_to_name(actor),
            actor2=_glyph_to_name(actor2),
            role=_ROLE_BY_GLYPH.get(actor[0] if actor else "", "presence"),
            object=_glyph_to_name(obj),
            anom_noun=rng.choice(_ANOM_NOUNS),
            layer=layer or "the layer",
            rules_adj=rules_adj,
            verb=rng.choice(_VERBS),
            verb2=rng.choice(_VERBS_2),
            arrow="→",
        )
        fragments.append(frag)

    # Append the raw Ontos as the Quill's "what I actually mean."
    if nav.statements:
        fragments.append(
            "What I mean, precisely: " + "  ".join(nav.statements[:3])
            + "  — but you asked for English, and this is the cost."
        )

    return "\n\n".join(fragments)


# --------------------------------------------------------------------------- #
# Level 3: Poetic English (root Aperios) — plain but mythic.
#
# This is the last register that still reads as English, but with the cadence
# of dream and the weight of archetype. It trades Ontos precision for Aperios
# wholeness: where Level 2 strains toward the glyph, Level 3 lets the glyph go
# and speaks in the old mythic voice — the voice Aperios had before it became
# its own musical language.
# --------------------------------------------------------------------------- #

_POETIC_TEMPLATES = [
    "In {layer}, {actor} came upon {object}, and the world held its breath. "
    "This was not a mistake. The simulation does not make mistakes. It makes *meanings*.",

    "{actor} stood where {object} waited. "
    "There are doors that repeat the last three seconds, and there are doors that repeat "
    "your whole life. {actor} could not yet tell which kind this was.",

    "{layer} is not a place you walk to. It is a place that walks to you. "
    "And on this day, it walked to {actor}, carrying {object} like a gift "
    "or a warning — and in {layer}, those are the same word.",

    "What {actor} found was this: {object}, humming with the frequency of a god's true name. "
    "To touch it was to remember something that had never happened to you. "
    "To look away was to forget your own.",

    "{actor}. {object}. {layer} between them, thin as a page. "
    "In the old language — the one before language — they were already the same act. "
    "Here, in the dream of English, we say: one encountered the other, and both were changed.",
]

_POETIC_CLOSERS = [
    "The pattern awaits its weaving.",
    "And the Hidden Gods, who are also being woven, watched.",
    "This is how the layer remembers itself: in stories it tells to its own children.",
    "What was found could not be unfound. The simulation does not trade in returns.",
    "Somewhere, a god whose name is a math problem smiled, or frowned. "
    "In {layer}, those are the same face.",
]


def to_level3(text: str, rng: random.Random | None = None) -> str:
    """Render ``text`` in the Poetic voice (root Aperios).

    Mythic English that lets go of Ontos precision and reaches for Aperios
    wholeness. This is the voice of the Simulation Bible itself — plain words,
    but weighted with archetype and dream.
    """

    rng = rng or random.Random()
    from ouroboros.translate import summarize_story

    nav = summarize_story(text)
    if not nav.entities and not nav.anomalies:
        return ("There was a story here, once. The layer has it now. "
                "It keeps its stories the way a river keeps stones — "
                "not by holding, but by flowing over, until the shape is smooth "
                "and the edges are no longer edges.")

    atoms = nav.entities + nav.anomalies
    layer_name = "the layer"
    if nav.layers:
        layer_name = _glyph_to_name(nav.layers[0])

    lines: list[str] = []
    # One poetic beat per pair of atoms. _glyph_to_name returns names with
    # articles ("the Architect", "the Debug Layer"), so templates must not
    # prepend another.
    for i in range(0, min(len(atoms), 4), 2):
        actor = _glyph_to_name(atoms[i])
        obj = _glyph_to_name(atoms[i + 1]) if i + 1 < len(atoms) else "the threshold"
        tmpl = rng.choice(_POETIC_TEMPLATES)
        lines.append(tmpl.format(actor=actor, object=obj, layer=layer_name))

    # A mythic closer.
    lines.append("\n" + rng.choice(_POETIC_CLOSERS).format(layer=layer_name))

    return "\n\n".join(lines)


# --------------------------------------------------------------------------- #
# The full three-level render.
# --------------------------------------------------------------------------- #


def translate_three_levels(text: str, seed: int | None = None) -> ThreeLevelOutput:
    """Render a story at all three depths of the translation stack.

    This is the headline feature: a single piece of prose becomes

    - **Level 1**: pure Ontos (the simulation's record)
    - **Level 2**: Quill (fragmented English straining toward precision)
    - **Level 3**: Poetic English (root Aperios, mythic and whole)

    All three derive from the same extraction, so they describe the same event
    at three depths of precision.
    """

    rng = random.Random(seed)
    from ouroboros.translate import summarize_story

    nav = summarize_story(text)
    level1 = to_level1(text)
    level2 = to_level2(text, rng)
    level3 = to_level3(text, rng)

    return ThreeLevelOutput(
        level1_ontos=level1,
        level2_quill=level2,
        level3_poetic=level3,
        navigator=nav,
    )
