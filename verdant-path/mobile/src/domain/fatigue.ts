/**
 * Fatigue scoring and readiness-based auto-regulation.
 *
 * Each check-in signal is normalized to its own 0-100 *fatigue* contribution
 * (higher = more fatigued). The final score blends the mean (50%) with the
 * worst signal (50%) so a single loud warning can nudge an otherwise-okay
 * check-in toward caution — honoring auto-regulation's respect for the body's
 * loudest warning.
 *
 * The spec's worked example (Energy=4, Mood=3, Soreness=2, Sleep=7h, HRV=55ms,
 * baseline 50ms) lands in the amber band (40-69%).
 *
 * These cues are sanity checks, not commands — embodied awareness has the
 * final word.
 */

/** The three fatigue color cues that guide a training day. */
export enum Fatigue {
  Green = "GREEN", // 0-39%  train normally
  Amber = "AMBER", // 40-69% technique, mobility, Zone 2
  Red = "RED", // 70-100% reduce intensity/volume; recover
}

export const FATIGUE_ICON: Record<Fatigue, string> = {
  [Fatigue.Green]: "🟢",
  [Fatigue.Amber]: "🟠",
  [Fatigue.Red]: "🔴",
};

export const FATIGUE_GUIDANCE: Record<Fatigue, string> = {
  [Fatigue.Green]: "Train normally.",
  [Fatigue.Amber]: "Prioritize technique, mobility, Zone 2.",
  [Fatigue.Red]: "Reduce intensity/volume; recover.",
};

/** Map a fatigue percentage (0-100) to its color cue. */
export function fatigueCue(percent: number): Fatigue {
  if (percent < 40) return Fatigue.Green;
  if (percent < 70) return Fatigue.Amber;
  return Fatigue.Red;
}

/** Linearly map `value` from [low, high] onto [0, 100], clamped. */
function scale(value: number, low: number, high: number): number {
  if (high <= low) return 0;
  const pct = ((value - low) / (high - low)) * 100;
  return Math.max(0, Math.min(100, pct));
}

export interface CheckInInput {
  energy: number; // 1-5
  mood: number; // 1-5
  soreness: number; // 1-5 (5 = very sore)
  sleepHours: number; // hours
  hrv: number; // ms
  hrvBaseline?: number; // ms, personal baseline (default 50)
}

/** Compute a 0-100 fatigue percentage from a daily check-in. */
export function fatigueFromCheckin(input: CheckInInput): number {
  const { energy, mood, soreness, sleepHours, hrv, hrvBaseline = 50 } = input;

  // Energy/mood/sleep are "good when high" → fatigue is the inverse of a 1-5
  // scale (5 -> 0%, 3 -> 50%, 1 -> 100%).
  const energyFatigue = 100 - scale(energy, 1, 5);
  const moodFatigue = 100 - scale(mood, 1, 5);
  const sleepFatigue = 100 - scale(sleepHours, 0, 9);
  // Soreness is "bad when high" → maps directly: 1 -> 0, 5 -> 100.
  const sorenessFatigue = scale(soreness, 1, 5);

  // HRV: at baseline -> 50; 150% of baseline -> 0; 50% of baseline -> 100.
  let hrvFatigue = 50;
  if (hrvBaseline > 0) {
    const ratio = hrv / hrvBaseline;
    hrvFatigue = Math.max(0, Math.min(100, 50 - (ratio - 1) * 100));
  }

  const signals = [energyFatigue, moodFatigue, sorenessFatigue, sleepFatigue, hrvFatigue];
  const mean = signals.reduce((a, b) => a + b, 0) / signals.length;
  const worst = Math.max(...signals);
  // Weakest-link-aware blend: respect the body's loudest warning signal.
  const fatigue = 0.5 * mean + 0.5 * worst;
  return Math.max(0, Math.min(100, fatigue));
}

/** A suggested change to today's plan based on the fatigue cue. */
export interface ReadinessAdjustment {
  cue: Fatigue;
  volumeChange: number; // fractional change, e.g. -0.20 = reduce 20%
  intensityChange: number; // fractional change to load/RPE target
  note: string;
}

/** Suggest a volume/intensity adjustment for today's session. */
export function readinessAdjustment(fatiguePercent: number): ReadinessAdjustment {
  const cue = fatigueCue(fatiguePercent);
  if (cue === Fatigue.Green) {
    return { cue, volumeChange: 0, intensityChange: 0, note: "Ready to train normally." };
  }
  if (cue === Fatigue.Amber) {
    return {
      cue,
      volumeChange: -0.2,
      intensityChange: -0.1,
      note: "Prioritize technique, mobility, Zone 2. Consider reducing primary-lift volume by ~20%.",
    };
  }
  return {
    cue,
    volumeChange: -0.4,
    intensityChange: -0.2,
    note: "High fatigue. Reduce intensity/volume substantially; prioritize recovery and movement quality.",
  };
}
