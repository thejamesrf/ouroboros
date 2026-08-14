/**
 * The six fundamental movement patterns.
 *
 * Every Verdant Path program hits all six at least weekly, regardless of
 * training frequency. These are the non-negotiable movement roots of the system.
 */

export enum Pattern {
  Push = "push",
  Pull = "pull",
  Hinge = "hinge",
  Lunge = "lunge",
  Squat = "squat",
  CarryRotate = "carry/rotate/anti-rotate",
}

export const ALL_PATTERNS: Pattern[] = [
  Pattern.Push,
  Pattern.Pull,
  Pattern.Hinge,
  Pattern.Lunge,
  Pattern.Squat,
  Pattern.CarryRotate,
];

export interface Movement {
  /** Stable identifier, e.g. "deadlift". */
  id: string;
  /** Display name. */
  name: string;
  pattern: Pattern;
  /** Accessory/finisher movements target weak links: unilateral, grip, core. */
  isAccessory?: boolean;
}

/**
 * A working library of movements keyed by id. Trainers can extend this freely;
 * these seed the template library with the lifts referenced in the spec.
 */
export const MOVEMENT_LIBRARY: Record<string, Movement> = {
  // Push
  bench_press: { id: "bench_press", name: "Bench Press", pattern: Pattern.Push },
  overhead_press: { id: "overhead_press", name: "Overhead Press", pattern: Pattern.Push },
  dips: { id: "dips", name: "Dips", pattern: Pattern.Push },
  lateral_raise: { id: "lateral_raise", name: "Lateral Raises", pattern: Pattern.Push, isAccessory: true },
  push_up: { id: "push_up", name: "Push-Up", pattern: Pattern.Push },
  // Pull
  pull_up: { id: "pull_up", name: "Pull-Up", pattern: Pattern.Pull },
  barbell_row: { id: "barbell_row", name: "Barbell Row", pattern: Pattern.Pull },
  cable_row: { id: "cable_row", name: "Cable Row", pattern: Pattern.Pull },
  biceps_curl: { id: "biceps_curl", name: "Biceps Curl", pattern: Pattern.Pull, isAccessory: true },
  face_pull: { id: "face_pull", name: "Face Pull", pattern: Pattern.Pull, isAccessory: true },
  // Hinge
  deadlift: { id: "deadlift", name: "Deadlift", pattern: Pattern.Hinge },
  romanian_deadlift: { id: "romanian_deadlift", name: "Romanian Deadlift", pattern: Pattern.Hinge },
  back_extension: { id: "back_extension", name: "Back Extension", pattern: Pattern.Hinge, isAccessory: true },
  kettlebell_swing: { id: "kettlebell_swing", name: "Kettlebell Swing", pattern: Pattern.Hinge },
  // Lunge
  walking_lunge: { id: "walking_lunge", name: "Walking Lunge", pattern: Pattern.Lunge },
  bulgarian_split_squat: { id: "bulgarian_split_squat", name: "Bulgarian Split Squat", pattern: Pattern.Lunge },
  step_up: { id: "step_up", name: "Step-Up", pattern: Pattern.Lunge },
  // Squat
  back_squat: { id: "back_squat", name: "Back Squat", pattern: Pattern.Squat },
  front_squat: { id: "front_squat", name: "Front Squat", pattern: Pattern.Squat },
  goblet_squat: { id: "goblet_squat", name: "Goblet Squat", pattern: Pattern.Squat },
  leg_press: { id: "leg_press", name: "Leg Press", pattern: Pattern.Squat },
  calf_raise: { id: "calf_raise", name: "Calf Raise", pattern: Pattern.Squat, isAccessory: true },
  // Carry / rotate / anti-rotate
  farmers_carry: { id: "farmers_carry", name: "Farmer's Carry", pattern: Pattern.CarryRotate },
  suitcase_carry: { id: "suitcase_carry", name: "Suitcase Carry", pattern: Pattern.CarryRotate },
  pallof_press: { id: "pallof_press", name: "Pallof Press", pattern: Pattern.CarryRotate, isAccessory: true },
  plank: { id: "plank", name: "Plank", pattern: Pattern.CarryRotate, isAccessory: true },
  hanging_leg_raise: { id: "hanging_leg_raise", name: "Hanging Leg Raise", pattern: Pattern.CarryRotate, isAccessory: true },
  forearm_curl: { id: "forearm_curl", name: "Forearm Curl", pattern: Pattern.CarryRotate, isAccessory: true },
};

/** Patterns not yet hit by the given movements — for trainer feedback. */
export function missingPatterns(movements: Movement[]): Pattern[] {
  const covered = new Set(movements.map((m) => m.pattern));
  return ALL_PATTERNS.filter((p) => !covered.has(p));
}

/** True if every fundamental pattern appears at least once (the weekly invariant). */
export function allPatternsCovered(movements: Movement[]): boolean {
  return missingPatterns(movements).length === 0;
}
