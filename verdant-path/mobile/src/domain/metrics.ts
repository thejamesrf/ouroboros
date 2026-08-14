/**
 * Weekly and monthly review logic: ACWR, fatigue trends, deload cues.
 *
 * The weekly review is the feedback loop of progressive oscillation. It compares
 * this week's training stress (TRIMP) against the recent average (ACWR) and
 * reads HRV trend to decide whether to push, hold, or deload.
 */

import { Fatigue, fatigueCue } from "./fatigue";
import { CheckIn, WorkoutLog, sessionTrimpFor } from "./tracker";
import { weeklyTrimp, weeklyTrimpStatus, Trimp } from "./trimp";

export interface WeeklySummary {
  weekStart: Date;
  weekEnd: Date;
  totalTrimp: number;
  trimpStatus: string;
  avgHrv: number;
  avgSleep: number;
  avgFatiguePercent: number;
  fatigueCue: Fatigue;
  redDays: number; // days at red fatigue
  acwr: number | null;
  suggestion: string;
}

/** Acute:chronic workload ratio: this week's TRIMP / average of prior weeks'. */
export function acwr(thisWeekTrimp: number, priorWeeksTrimp: number[]): number | null {
  if (priorWeeksTrimp.length === 0) return null;
  const chronic = priorWeeksTrimp.reduce((a, b) => a + b, 0) / priorWeeksTrimp.length;
  if (chronic <= 0) return null;
  return thisWeekTrimp / chronic;
}

/** Return the Mon-Sun week range containing `day`. */
export function weekRange(day: Date): { start: Date; end: Date } {
  const start = new Date(day);
  start.setDate(start.getDate() - start.getDay() + 1); // Monday
  start.setHours(0, 0, 0, 0);
  const end = new Date(start);
  end.setDate(end.getDate() + 6);
  end.setHours(23, 59, 59, 999);
  return { start, end };
}

export interface WeeklyReviewInput {
  weekOf: Date;
  checkins: CheckIn[];
  logs: WorkoutLog[];
  priorWeeksTrimp?: number[];
  hrvTrendDown?: boolean;
}

/** Build a weekly summary with a deload suggestion. */
export function weeklyReview(input: WeeklyReviewInput): WeeklySummary {
  const { weekOf, checkins, logs, priorWeeksTrimp = [], hrvTrendDown = false } = input;
  const { start, end } = weekRange(weekOf);

  const weekCheckins = checkins.filter((c) => c.day >= start && c.day <= end);
  const weekLogs = logs.filter((w) => w.day >= start && w.day <= end);

  const trimpTotal = weeklyTrimp(weekLogs.map((w) => sessionTrimpFor(w)));
  const trimpStatus = weeklyTrimpStatus(trimpTotal);

  const avgHrv = weekCheckins.length
    ? weekCheckins.reduce((s, c) => s + c.hrv, 0) / weekCheckins.length
    : 0;
  const avgSleep = weekCheckins.length
    ? weekCheckins.reduce((s, c) => s + c.sleepHours, 0) / weekCheckins.length
    : 0;

  const fatiguePcts = weekCheckins.map((c) => c.fatiguePercent);
  const avgFatigue = fatiguePcts.length ? fatiguePcts.reduce((a, b) => a + b, 0) / fatiguePcts.length : 0;
  const cue = fatiguePcts.length ? fatigueCue(avgFatigue) : Fatigue.Green;

  const redDays = weekCheckins.filter((c) => c.cue === Fatigue.Red).length;
  const ratio = acwr(trimpTotal, priorWeeksTrimp);
  const suggestion = deloadSuggestion(ratio, hrvTrendDown, redDays, cue);

  return {
    weekStart: start,
    weekEnd: end,
    totalTrimp: trimpTotal,
    trimpStatus,
    avgHrv,
    avgSleep,
    avgFatiguePercent: avgFatigue,
    fatigueCue: cue,
    redDays,
    acwr: ratio,
    suggestion,
  };
}

function deloadSuggestion(
  ratio: number | null,
  hrvTrendDown: boolean,
  redDays: number,
  cue: Fatigue
): string {
  if (redDays >= 3) return "🔴 fatigue 3+ days this week — consider a deload week.";
  if (ratio != null && ratio > 1.5 && hrvTrendDown) return "ACWR > 1.5 with HRV trending down — consider a deload week.";
  if (ratio != null && ratio > 1.5) return "ACWR > 1.5 — hold volume steady; watch readiness closely.";
  if (ratio != null && ratio >= 0.8 && ratio <= 1.2 && !hrvTrendDown) return "ACWR ≈ 1.0 with HRV stable/↑ — progressive load OK.";
  if (cue === Fatigue.Red) return "Average fatigue is high — prioritize recovery next week.";
  return "Stable week — continue progressive oscillation.";
}
