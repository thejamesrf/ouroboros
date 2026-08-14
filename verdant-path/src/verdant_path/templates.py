"""Pre-built session templates for the Verdant Path template library.

These seed the planner's template library with the sessions referenced in the
spec's example workflow, so a trainer can assign a 5x/week resistance split out
of the box.
"""

from __future__ import annotations

from verdant_path.planner import Planner, SetTarget
from verdant_path.trimp import TRIMP


def register_default_templates(planner: Planner) -> Planner:
    """Register the default template library onto a planner."""

    # --- Resistance days (5x/week example split) ---------------------------

    planner.register_template(
        planner.build_session(
            name="Posterior Chain",
            main=[
                ("deadlift", SetTarget(5, "3", load="RPE 8", rest_sec=180, notes="focus on hip drive")),
                ("romanian_deadlift", SetTarget(4, "6-8", rpe=7.5, rest_sec=120)),
                ("back_extension", SetTarget(3, "10-12", rpe=7, rest_sec=60)),
            ],
            accessory=[
                ("suitcase_carry", SetTarget(3, "40m", rest_sec=60)),
                ("goblet_squat", SetTarget(3, "8-10", rpe=7, rest_sec=90)),
            ],
            conditioning="Zone 2 ruck or LISS 20 min",
            tag="Strength",
            intended_trimp=TRIMP.HIGH,
        )
    )

    planner.register_template(
        planner.build_session(
            name="Chest + Biceps",
            main=[
                ("bench_press", SetTarget(5, "5", load="RPE 8", rest_sec=150)),
                ("barbell_row", SetTarget(4, "6-8", rpe=7.5, rest_sec=120)),
                ("biceps_curl", SetTarget(3, "10-12", rpe=7, rest_sec=60)),
            ],
            accessory=[
                ("face_pull", SetTarget(3, "15", rpe=6, rest_sec=45)),
                ("walking_lunge", SetTarget(3, "10/leg", rpe=7, rest_sec=90)),
            ],
            conditioning=None,
            tag="Strength",
            intended_trimp=TRIMP.MEDIUM,
        )
    )

    planner.register_template(
        planner.build_session(
            name="Shoulders + Triceps",
            main=[
                ("overhead_press", SetTarget(5, "5", load="RPE 8", rest_sec=150)),
                ("lateral_raise", SetTarget(4, "12-15", rpe=7, rest_sec=45)),
                ("dips", SetTarget(3, "8-10", rpe=7.5, rest_sec=90)),
            ],
            accessory=[("pallof_press", SetTarget(3, "10/side", rest_sec=45))],
            conditioning=None,
            tag="Strength",
            intended_trimp=TRIMP.MEDIUM,
        )
    )

    # --- Endurance days ----------------------------------------------------

    planner.register_template(
        planner.build_session(
            name="LISS Run",
            main=[],
            conditioning="Zone 2 run 45+ min, nasal breathing",
            tag="Endurance",
            intended_trimp=TRIMP.LOW,
            cooldown="Walk + stretch",
        )
    )

    planner.register_template(
        planner.build_session(
            name="HIIT / Work-Capacity",
            main=[],
            conditioning="Intervals 30s on / 90s off x8, or ruck intervals",
            tag="Endurance",
            intended_trimp=TRIMP.HIGH,
            cooldown="Walk + box breathing",
        )
    )

    # --- Recovery ----------------------------------------------------------

    planner.register_template(
        planner.build_session(
            name="Active Recovery",
            main=[],
            conditioning="Yoga + 30 min walk",
            tag="Recovery",
            intended_trimp=TRIMP.LOW,
            cooldown="Sauna or swim",
        )
    )

    return planner


def default_planner() -> Planner:
    """A planner preloaded with the default movement library and templates."""

    return register_default_templates(Planner())
