/**
 * Data export & insights.
 *
 * Export member records to CSV for offline review (spec §7). PDF export uses the
 * platform share sheet when available; CSV is fully portable and the baseline.
 */

import type { CheckIn, WorkoutLog, JournalEntry } from "../domain/tracker";
import { sessionTrimpFor } from "../domain/tracker";

function csvEscape(value: unknown): string {
  const s = String(value ?? "");
  if (/[",\n]/.test(s)) return `"${s.replace(/"/g, '""')}"`;
  return s;
}

function toCsv(rows: Array<Record<string, unknown>>, columns: string[]): string {
  const header = columns.map(csvEscape).join(",");
  const body = rows.map((r) => columns.map((c) => csvEscape(r[c])).join(",")).join("\n");
  return `${header}\n${body}`;
}

/** Export check-ins to CSV. */
export function checkinsToCsv(checkins: CheckIn[]): string {
  return toCsv(
    checkins.map((c) => ({
      day: c.day.toISOString().slice(0, 10),
      energy: c.energy,
      mood: c.mood,
      soreness: c.soreness,
      sleep_hours: c.sleepHours,
      hrv: c.hrv,
      fatigue_percent: c.fatiguePercent.toFixed(1),
      cue: c.cue,
    })),
    ["day", "energy", "mood", "soreness", "sleep_hours", "hrv", "fatigue_percent", "cue"]
  );
}

/** Export workout logs to CSV. */
export function workoutsToCsv(logs: WorkoutLog[]): string {
  return toCsv(
    logs.map((w) => ({
      day: w.day.toISOString().slice(0, 10),
      movement: w.movement.name,
      pattern: w.movement.pattern,
      sets: w.sets.length,
      trimp: sessionTrimpFor(w),
      notes: w.notes ?? "",
    })),
    ["day", "movement", "pattern", "sets", "trimp", "notes"]
  );
}

/** Export journal entries to CSV. */
export function journalToCsv(entries: JournalEntry[]): string {
  return toCsv(
    entries.map((e) => ({
      day: e.day.toISOString().slice(0, 10),
      tags: e.tags.join(";"),
      text: e.text,
    })),
    ["day", "tags", "text"]
  );
}

/** Combine all exports into a single CSV string (one section per record type). */
export function exportAll(
  checkins: CheckIn[],
  logs: WorkoutLog[],
  journal: JournalEntry[]
): string {
  return [
    "# Check-ins",
    checkinsToCsv(checkins),
    "",
    "# Workout logs",
    workoutsToCsv(logs),
    "",
    "# Journal",
    journalToCsv(journal),
  ].join("\n");
}
