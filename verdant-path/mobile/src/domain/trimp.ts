/**
 * TRIMP — Training Impulse scoring on a subjective 1-3 scale.
 *
 * TRIMP is Verdant Path's unit of training stress. A foundation week targets
 * 8-12 TRIMP. The scale is intentionally coarse to stay grounded in embodied
 * awareness rather than false precision:
 *
 *   1 (Low)    — recovery / Zone 2 (walking, mobility)
 *   2 (Medium) — moderate training (normal gym session)
 *   3 (High)   — heavy / CNS-demanding (HIIT, heavy lifts)
 */

/** Foundation weekly TRIMP range — the floor of sustainable resilience work. */
export const FOUNDATION_WEEKLY_TRIMP_RANGE: [number, number] = [8, 12];

export enum Trimp {
  Low = 1,
  Medium = 2,
  High = 3,
}

export const TRIMP_LABEL: Record<Trimp, string> = {
  [Trimp.Low]: "Low",
  [Trimp.Medium]: "Medium",
  [Trimp.High]: "High",
};

/** Coerce an integer (1-3) into a TRIMP level, clamping out-of-range values. */
export function trimpLevel(value: number): Trimp {
  if (value <= 1) return Trimp.Low;
  if (value >= 3) return Trimp.High;
  return Trimp.Medium;
}

/** A single logged set: the raw unit of a training session. */
export interface SetLog {
  load?: number;
  reps?: number;
  tempo?: string;
  rpe?: number;
  restSec?: number;
  notes?: string;
}

/**
 * Estimate a session's TRIMP from logged sets, with an explicit override.
 *
 * Trainers often assign an intended TRIMP when planning; members can override
 * it after training based on how the body actually responded (embodied
 * awareness over prescribed intent). If no override is given, we estimate
 * from the heaviest RPE recorded.
 */
export function trimpForSession(sets: SetLog[], assigned?: Trimp): Trimp {
  if (assigned !== undefined) return assigned;
  if (sets.length === 0) return Trimp.Low;

  const rpes = sets.map((s) => s.rpe).filter((r): r is number => r != null);
  if (rpes.length === 0) return Trimp.Low;
  const peak = Math.max(...rpes);
  if (peak >= 8.5) return Trimp.High;
  if (peak >= 6.0) return Trimp.Medium;
  return Trimp.Low;
}

/** Sum TRIMP levels across a week's sessions. */
export function weeklyTrimp(levels: Trimp[]): number {
  return levels.reduce((sum, l) => sum + l, 0);
}

/** Human-readable status for a weekly TRIMP total. */
export function weeklyTrimpStatus(total: number): string {
  const [low, high] = FOUNDATION_WEEKLY_TRIMP_RANGE;
  if (total < low) return `under-foundation (${total}/${low}-${high}): consider a bit more volume`;
  if (total <= high) return `foundation range (${total}/${low}-${high}): sustainable`;
  return `above foundation (${total}/${low}-${high}): watch recovery cues`;
}
