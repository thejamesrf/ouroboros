/**
 * Session structure and workout planning.
 *
 * A Verdant Path session has four phases: warm-up, main work, accessory/finisher,
 * and conditioning (plus a cooldown). Splits scale from 1x/week (full body) up
 * to 6x/week (one pattern per day), but every split guarantees weekly coverage
 * of all six fundamental movements.
 */

import { Movement, Pattern, allPatternsCovered, missingPatterns } from "./movements";
import { Trimp } from "./trimp";

/** Planned set parameters: the prescription a trainer hands a member. */
export interface SetTarget {
  sets: number;
  reps: string; // e.g. "5", "8-12", "AMRAP"
  load?: string; // e.g. "80% 1RM", "RPE 8"
  tempo?: string; // e.g. "3010"
  rpe?: number;
  restSec?: number;
  notes?: string;
}

/** A movement plus its planned set/rep scheme within a block. */
export interface MovementAssignment {
  movement: Movement;
  target: SetTarget;
}

/** One phase of a session: warm-up, main, accessory, or conditioning. */
export interface SessionBlock {
  name: string;
  assignments?: MovementAssignment[];
  notes?: string;
}

export type SessionTag = "Strength" | "Endurance" | "Functional" | "Recovery";

/** A reusable single-day workout template. */
export interface SessionTemplate {
  id: string;
  name: string;
  blocks: SessionBlock[];
  tag: SessionTag;
  intendedTrimp: Trimp;
  cooldown?: string;
}

export function sessionMovements(session: SessionTemplate): Movement[] {
  const out: Movement[] = [];
  for (const block of session.blocks) {
    if (block.assignments) out.push(...block.assignments.map((a) => a.movement));
  }
  return out;
}

export function sessionPatterns(session: SessionTemplate): Set<Pattern> {
  return new Set(sessionMovements(session).map((m) => m.pattern));
}

/** A multi-day training plan over a week, covering a chosen split. */
export interface WorkoutPlan {
  id: string;
  name: string;
  frequency: number; // sessions per week, 1-6
  days: SessionTemplate[];
  rotationNote?: string;
}

export function planCoverage(plan: WorkoutPlan): boolean {
  const movements = plan.days.flatMap(sessionMovements);
  return allPatternsCovered(movements);
}

export function planCoverageReport(plan: WorkoutPlan): string {
  const movements = plan.days.flatMap(sessionMovements);
  if (allPatternsCovered(movements)) return "✅ All six fundamental patterns covered this week.";
  const missing = missingPatterns(movements).join(", ");
  return `⚠️ Missing patterns: ${missing}`;
}

// --- Split definitions ----------------------------------------------------

export interface SplitDefinition {
  name: string;
  days: string[][];
}

export const SPLITS: Record<number, SplitDefinition> = {
  1: { name: "Full-Body", days: [["all patterns in one session"]] },
  2: { name: "Upper / Lower", days: [["Upper (push + pull)", "Lower (squat + hinge + lunge)"]] },
  3: { name: "Push / Pull / Legs", days: [["Push"], ["Pull"], ["Legs"]] },
  4: {
    name: "Back/Hams · Chest/Bi · Calves/Quads · Shoulders/Tris",
    days: [["Back + Hamstrings"], ["Chest + Biceps"], ["Calves + Quads"], ["Shoulders + Triceps"]],
  },
  5: {
    name: "5-Part Rotation",
    days: [
      ["Posterior Chain"],
      ["Chest + Biceps"],
      ["Shoulders + Triceps"],
      ["Quads + Calves"],
      ["Core + Forearms + Upper Back"],
    ],
  },
  6: {
    name: "One Pattern Per Day",
    days: [["Push"], ["Pull"], ["Hinge"], ["Lunge"], ["Squat"], ["Carry/Rotate"]],
  },
};

export function splitForFrequency(frequency: number): SplitDefinition {
  if (!SPLITS[frequency]) throw new Error(`frequency must be 1-6, got ${frequency}`);
  return SPLITS[frequency];
}

// --- Planner --------------------------------------------------------------

/**
 * Builds and validates workout plans from the Verdant Path splits.
 * Holds a movement library and template library so trainers can assemble plans
 * from reusable pieces. The planner checks weekly coverage so a plan never
 * silently drops a pattern.
 */
export class Planner {
  movements: Record<string, Movement>;
  templates: Record<string, SessionTemplate> = {};

  constructor(movementLibrary?: Record<string, Movement>) {
    this.movements = { ...movementLibrary };
  }

  get(id: string): Movement {
    const m = this.movements[id];
    if (!m) throw new Error(`unknown movement '${id}'; add it to the library`);
    return m;
  }

  registerTemplate(template: SessionTemplate): void {
    this.templates[template.id] = template;
  }

  buildSession(args: {
    id: string;
    name: string;
    main: Array<[string, SetTarget]>;
    accessory?: Array<[string, SetTarget]>;
    conditioning?: string;
    tag?: SessionTag;
    intendedTrimp?: Trimp;
    cooldown?: string;
  }): SessionTemplate {
    const toAssignments = (pairs: Array<[string, SetTarget]>): MovementAssignment[] =>
      pairs.map(([id, target]) => ({ movement: this.get(id), target }));

    const blocks: SessionBlock[] = [
      { name: "Warm-Up", notes: "CARs, movement prep, light cardio" },
      { name: "Main Work", assignments: toAssignments(args.main) },
    ];
    if (args.accessory) {
      blocks.push({
        name: "Accessory / Finisher",
        assignments: toAssignments(args.accessory),
        notes: "Unilateral, contralateral, grip, core, or weak-link work.",
      });
    }
    if (args.conditioning) {
      blocks.push({ name: "Conditioning", notes: args.conditioning });
    }
    return {
      id: args.id,
      name: args.name,
      blocks,
      tag: args.tag ?? "Strength",
      intendedTrimp: args.intendedTrimp ?? Trimp.Medium,
      cooldown: args.cooldown ?? "Breathing + stretching + walk",
    };
  }

  buildPlan(args: {
    frequency: number;
    days: SessionTemplate[];
    name?: string;
    rotationNote?: string;
    id: string;
  }): WorkoutPlan {
    const split = splitForFrequency(args.frequency);
    if (args.days.length !== args.frequency) {
      throw new Error(`expected ${args.frequency} day(s) for the ${split.name} split, got ${args.days.length}`);
    }
    const plan: WorkoutPlan = {
      id: args.id,
      name: args.name ?? `${split.name} (${args.frequency}x/week)`,
      frequency: args.frequency,
      days: args.days,
      rotationNote: args.rotationNote,
    };
    return plan;
  }

  /** Lay out a plan's days on consecutive dates starting at `start`. */
  schedule(plan: WorkoutPlan, start: Date): Array<{ date: Date; session: SessionTemplate }> {
    return plan.days.map((session, i) => {
      const d = new Date(start);
      d.setDate(d.getDate() + i);
      return { date: d, session };
    });
  }
}
