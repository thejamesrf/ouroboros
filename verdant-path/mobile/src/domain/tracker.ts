/**
 * Daily check-ins, workout logs, and journal entries.
 *
 * These are the member-facing records: what they did, how they felt, and what
 * they noticed. They feed fatigue scoring, TRIMP totals, and weekly reviews.
 */

import { Fatigue, fatigueCue, fatigueFromCheckin } from "./fatigue";
import { Movement } from "./movements";
import { Trimp, trimpForSession, type SetLog } from "./trimp";

export type { SetLog };

export interface CheckIn {
  id: string;
  day: Date;
  energy: number; // 1-5
  mood: number; // 1-5
  soreness: number; // 1-5 (5 = very sore)
  sleepHours: number; // hours
  hrv: number; // ms
  hrvBaseline?: number; // ms
  readonly fatiguePercent: number;
  readonly cue: Fatigue;
}

export function makeCheckIn(args: Omit<CheckIn, "fatiguePercent" | "cue">): CheckIn {
  const fatiguePercent = fatigueFromCheckin({
    energy: args.energy,
    mood: args.mood,
    soreness: args.soreness,
    sleepHours: args.sleepHours,
    hrv: args.hrv,
    hrvBaseline: args.hrvBaseline,
  });
  return { ...args, fatiguePercent, cue: fatigueCue(fatiguePercent) };
}

export interface WorkoutLog {
  id: string;
  day: Date;
  movement: Movement;
  sets: SetLog[];
  trimp?: Trimp; // explicit override after the session
  notes?: string;
}

/** Resolve the session's TRIMP: explicit override, else estimate from sets. */
export function sessionTrimpFor(log: WorkoutLog): Trimp {
  if (log.trimp !== undefined) return log.trimp;
  return trimpForSession(log.sets);
}

export interface JournalEntry {
  id: string;
  day: Date;
  text: string;
  tags: string[];
  photo?: string; // path or URI to a progress photo
}

/** Normalize a raw tag string ("#Recovery", "  #soreness ") to "recovery". */
export function normalizeTag(tag: string): string {
  return tag.trim().replace(/^#+/, "").toLowerCase();
}

/** Build a JournalEntry with normalized, de-duplicated tags. */
export function makeJournalEntry(args: {
  id: string;
  day: Date;
  text: string;
  tags?: string[];
  photo?: string;
}): JournalEntry {
  const seen = new Set<string>();
  const tags: string[] = [];
  for (const raw of args.tags ?? []) {
    const clean = normalizeTag(raw);
    if (clean && !seen.has(clean)) {
      seen.add(clean);
      tags.push(clean);
    }
  }
  return { id: args.id, day: args.day, text: args.text, tags, photo: args.photo };
}
