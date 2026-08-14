/**
 * Pre-built session templates for the Verdant Path template library.
 *
 * These seed the planner's template library with the sessions referenced in the
 * spec's example workflow, so a trainer can assign a 5x/week resistance split
 * out of the box.
 */

import { Planner, type SessionTemplate } from "./planner";
import { MOVEMENT_LIBRARY } from "./movements";
import { Trimp } from "./trimp";

export function registerDefaultTemplates(planner: Planner): Planner {
  planner.registerTemplate(
    planner.buildSession({
      id: "posterior_chain",
      name: "Posterior Chain",
      main: [
        ["deadlift", { sets: 5, reps: "3", load: "RPE 8", restSec: 180, notes: "focus on hip drive" }],
        ["romanian_deadlift", { sets: 4, reps: "6-8", rpe: 7.5, restSec: 120 }],
        ["back_extension", { sets: 3, reps: "10-12", rpe: 7, restSec: 60 }],
      ],
      accessory: [["suitcase_carry", { sets: 3, reps: "40m", restSec: 60 }], ["goblet_squat", { sets: 3, reps: "8-10", rpe: 7, restSec: 90 }]],
      conditioning: "Zone 2 ruck or LISS 20 min",
      tag: "Strength",
      intendedTrimp: Trimp.High,
    })
  );

  planner.registerTemplate(
    planner.buildSession({
      id: "chest_biceps",
      name: "Chest + Biceps",
      main: [
        ["bench_press", { sets: 5, reps: "5", load: "RPE 8", restSec: 150 }],
        ["barbell_row", { sets: 4, reps: "6-8", rpe: 7.5, restSec: 120 }],
        ["biceps_curl", { sets: 3, reps: "10-12", rpe: 7, restSec: 60 }],
      ],
      accessory: [["face_pull", { sets: 3, reps: "15", rpe: 6, restSec: 45 }], ["walking_lunge", { sets: 3, reps: "10/leg", rpe: 7, restSec: 90 }]],
      tag: "Strength",
      intendedTrimp: Trimp.Medium,
    })
  );

  planner.registerTemplate(
    planner.buildSession({
      id: "shoulders_triceps",
      name: "Shoulders + Triceps",
      main: [
        ["overhead_press", { sets: 5, reps: "5", load: "RPE 8", restSec: 150 }],
        ["lateral_raise", { sets: 4, reps: "12-15", rpe: 7, restSec: 45 }],
        ["dips", { sets: 3, reps: "8-10", rpe: 7.5, restSec: 90 }],
      ],
      accessory: [["pallof_press", { sets: 3, reps: "10/side", restSec: 45 }]],
      tag: "Strength",
      intendedTrimp: Trimp.Medium,
    })
  );

  planner.registerTemplate(
    planner.buildSession({
      id: "liss_run",
      name: "LISS Run",
      main: [],
      conditioning: "Zone 2 run 45+ min, nasal breathing",
      tag: "Endurance",
      intendedTrimp: Trimp.Low,
      cooldown: "Walk + stretch",
    })
  );

  planner.registerTemplate(
    planner.buildSession({
      id: "hiit",
      name: "HIIT / Work-Capacity",
      main: [],
      conditioning: "Intervals 30s on / 90s off x8, or ruck intervals",
      tag: "Endurance",
      intendedTrimp: Trimp.High,
      cooldown: "Walk + box breathing",
    })
  );

  planner.registerTemplate(
    planner.buildSession({
      id: "active_recovery",
      name: "Active Recovery",
      main: [],
      conditioning: "Yoga + 30 min walk",
      tag: "Recovery",
      intendedTrimp: Trimp.Low,
      cooldown: "Sauna or swim",
    })
  );

  return planner;
}

export function defaultPlanner(): Planner {
  return registerDefaultTemplates(new Planner(MOVEMENT_LIBRARY));
}
