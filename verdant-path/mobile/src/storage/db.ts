/**
 * Offline-first storage layer.
 *
 * Verdant Path is offline-first: every record is written to a local SQLite
 * database before any cloud sync attempt. The schema mirrors the domain models;
 * repositories handle serialization between rows and domain objects. Sync (when
 * enabled) is a separate concern layered on top — see sync.ts.
 *
 * On platforms without SQLite (web/legacy), we fall back to an in-memory store
 * so the app and tests keep working.
 */

import * as SQLite from "expo-sqlite";
import type { CheckIn, JournalEntry, WorkoutLog } from "../domain/tracker";
import { makeCheckIn, makeJournalEntry } from "../domain/tracker";
import type { Movement } from "../domain/movements";
import { MOVEMENT_LIBRARY } from "../domain/movements";
import { Trimp, type SetLog } from "../domain/trimp";

/** ISO date helper for storage keys. */
export function isoDay(d: Date): string {
  return d.toISOString().slice(0, 10);
}

export const SCHEMA = `
CREATE TABLE IF NOT EXISTS checkins (
  id TEXT PRIMARY KEY,
  day TEXT NOT NULL,
  energy REAL NOT NULL,
  mood REAL NOT NULL,
  soreness REAL NOT NULL,
  sleep_hours REAL NOT NULL,
  hrv REAL NOT NULL,
  hrv_baseline REAL DEFAULT 50
);
CREATE TABLE IF NOT EXISTS workout_logs (
  id TEXT PRIMARY KEY,
  day TEXT NOT NULL,
  movement_id TEXT NOT NULL,
  sets_json TEXT NOT NULL,
  trimp INTEGER,
  notes TEXT
);
CREATE TABLE IF NOT EXISTS journal_entries (
  id TEXT PRIMARY KEY,
  day TEXT NOT NULL,
  text TEXT NOT NULL,
  tags_json TEXT NOT NULL,
  photo TEXT
);
CREATE TABLE IF NOT EXISTS habit_completions (
  day TEXT NOT NULL,
  habit_id TEXT NOT NULL,
  completed INTEGER NOT NULL,
  PRIMARY KEY (day, habit_id)
);
CREATE TABLE IF NOT EXISTS templates (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  json TEXT NOT NULL,
  shared INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS assignments (
  id TEXT PRIMARY KEY,
  member_id TEXT NOT NULL,
  template_id TEXT NOT NULL,
  weekday INTEGER NOT NULL
);
`;

export interface VerdantDatabase {
  /** Run a write statement. */
  exec(sql: string, params?: unknown[]): Promise<void>;
  /** Run a read statement and return rows. */
  all<T>(sql: string, params?: unknown[]): Promise<T[]>;
}

/** Open (and migrate) the SQLite database, with an in-memory fallback. */
export async function openDatabase(name = "verdant_path.db"): Promise<VerdantDatabase> {
  try {
    const db = await SQLite.openDatabaseAsync(name);
    await db.execAsync(SCHEMA);
    return {
      async exec(sql: string, params: unknown[] = []) {
        await db.runAsync(sql, ...(params as SQLite.SQLiteBindValue[]));
      },
      async all<T>(sql: string, params: unknown[] = []) {
        const result = await db.getAllAsync(sql, ...(params as SQLite.SQLiteBindValue[]));
        return result as T[];
      },
    };
  } catch {
    // Fallback: in-memory store (web/legacy/test environments without SQLite).
    return new InMemoryDatabase(SCHEMA);
  }
}

/**
 * A minimal in-memory SQL-ish store for environments without SQLite. It
 * understands the small subset of SQL the repositories use: equality and range
 * WHERE filters, ORDER BY (ASC|DESC), and LIMIT. This keeps web/test parity
 * with SQLite so the Journal "recent" list and weekly range queries behave
 * correctly when the native module is unavailable.
 */
export class InMemoryDatabase implements VerdantDatabase {
  private tables: Record<string, Map<string, Record<string, unknown>>> = {};

  constructor(schema: string) {
    for (const stmt of schema.split(";")) {
      const match = stmt.match(/CREATE TABLE IF NOT EXISTS (\w+)\s*\([\s\S]*\)/i);
      if (match) {
        const [, name] = match;
        this.tables[name] = new Map();
      }
    }
  }

  private parse(sql: string): { table: string; op: string } | null {
    const insert = sql.match(/^INSERT (?:OR REPLACE )?INTO (\w+)/i);
    if (insert) return { table: insert[1], op: "insert" };
    const del = sql.match(/^DELETE FROM (\w+)/i);
    if (del) return { table: del[1], op: "delete" };
    const sel = sql.match(/^SELECT [\s\S]* FROM (\w+)/i);
    if (sel) return { table: sel[1], op: "select" };
    return null;
  }

  async exec(sql: string, params: unknown[] = []): Promise<void> {
    const info = this.parse(sql);
    if (!info) return;
    const table = this.tables[info.table];
    if (!table) return;

    if (info.op === "insert") {
      // Naive: assumes params map to columns by position. Sufficient for repos.
      const cols = sql.match(/\(([^)]+)\)/)?.[1].split(",").map((c) => c.trim()) ?? [];
      const placeholders = (sql.match(/\?/g) ?? []).length;
      const values = params.slice(0, placeholders);
      const row: Record<string, unknown> = {};
      cols.forEach((c, i) => (row[c] = values[i]));
      const id = String(row["id"] ?? crypto.randomUUID());
      table.set(id, row);
    } else if (info.op === "delete") {
      const where = sql.match(/WHERE (\w+)\s*=\s*\?/i);
      if (where) {
        const [, col] = where;
        for (const [id, row] of table) {
          if (String(row[col]) === String(params[0])) table.delete(id);
        }
      } else {
        table.clear();
      }
    }
  }

  async all<T>(sql: string, params: unknown[] = []): Promise<T[]> {
    const info = this.parse(sql);
    if (!info) return [];
    const table = this.tables[info.table];
    if (!table) return [];
    let rows = Array.from(table.values()) as Record<string, unknown>[];

    // Bindings are positional; consume them in the order clauses appear.
    let p = 0;

    // Equality filters: `col = ?`.
    for (const m of sql.matchAll(/(\w+)\s*=\s*\?/gi)) {
      const col = m[1];
      const v = String(params[p++]);
      rows = rows.filter((r) => String(r[col]) === v);
    }
    // Range filters: `col >= ?` / `col <= ?` (kept in source order).
    for (const m of sql.matchAll(/(\w+)\s*(>=|<=)\s*\?/gi)) {
      const col = m[1];
      const op = m[2];
      const v = params[p++];
      rows = rows.filter((r) => {
        const rv = r[col];
        if (rv == null) return false;
        const cmp = String(rv) < String(v) ? -1 : String(rv) > String(v) ? 1 : 0;
        return op === ">=" ? cmp >= 0 : cmp <= 0;
      });
    }

    // ORDER BY col DESC|ASC.
    const order = sql.match(/ORDER BY (\w+)\s*(DESC|ASC)?/i);
    if (order) {
      const [, col, dir] = order;
      rows.sort((a, b) => {
        const av = String(a[col] ?? "");
        const bv = String(b[col] ?? "");
        const cmp = av < bv ? -1 : av > bv ? 1 : 0;
        return dir?.toUpperCase() === "DESC" ? -cmp : cmp;
      });
    }

    // LIMIT ?.
    const limit = sql.match(/LIMIT\s*\?/i);
    if (limit) {
      const n = Number(params[p++]);
      if (Number.isFinite(n) && n >= 0) rows = rows.slice(0, n);
    }

    return rows as T[];
  }
}

// --- Repositories ---------------------------------------------------------

export class CheckInRepository {
  constructor(private db: VerdantDatabase) {}

  async save(c: CheckIn): Promise<void> {
    await this.db.exec(
      `INSERT OR REPLACE INTO checkins (id, day, energy, mood, soreness, sleep_hours, hrv, hrv_baseline)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
      [c.id, isoDay(c.day), c.energy, c.mood, c.soreness, c.sleepHours, c.hrv, c.hrvBaseline ?? 50]
    );
  }

  async forDay(day: Date): Promise<CheckIn[]> {
    const rows = await this.db.all<Record<string, unknown>>(
      `SELECT * FROM checkins WHERE day = ?`,
      [isoDay(day)]
    );
    return rows.map(rowToCheckIn);
  }

  async forWeek(start: Date, end: Date): Promise<CheckIn[]> {
    const rows = await this.db.all<Record<string, unknown>>(
      `SELECT * FROM checkins WHERE day >= ? AND day <= ?`,
      [isoDay(start), isoDay(end)]
    );
    return rows.map(rowToCheckIn);
  }
}

export class WorkoutLogRepository {
  constructor(private db: VerdantDatabase) {}

  async save(log: WorkoutLog): Promise<void> {
    await this.db.exec(
      `INSERT OR REPLACE INTO workout_logs (id, day, movement_id, sets_json, trimp, notes)
       VALUES (?, ?, ?, ?, ?, ?)`,
      [log.id, isoDay(log.day), log.movement.id, JSON.stringify(log.sets), log.trimp ?? null, log.notes ?? null]
    );
  }

  async forWeek(start: Date, end: Date): Promise<WorkoutLog[]> {
    const rows = await this.db.all<Record<string, unknown>>(
      `SELECT * FROM workout_logs WHERE day >= ? AND day <= ?`,
      [isoDay(start), isoDay(end)]
    );
    return rows.map((r) => rowToWorkoutLog(r));
  }
}

export class JournalRepository {
  constructor(private db: VerdantDatabase) {}

  async save(entry: JournalEntry): Promise<void> {
    await this.db.exec(
      `INSERT OR REPLACE INTO journal_entries (id, day, text, tags_json, photo)
       VALUES (?, ?, ?, ?, ?)`,
      [entry.id, isoDay(entry.day), entry.text, JSON.stringify(entry.tags), entry.photo ?? null]
    );
  }

  async recent(limit = 50): Promise<JournalEntry[]> {
    const rows = await this.db.all<Record<string, unknown>>(
      `SELECT * FROM journal_entries ORDER BY day DESC LIMIT ?`,
      [limit]
    );
    return rows.map(rowToJournal);
  }
}

export class HabitRepository {
  constructor(private db: VerdantDatabase) {}

  async setCompletion(day: Date, habitId: string, completed: boolean): Promise<void> {
    await this.db.exec(
      `INSERT OR REPLACE INTO habit_completions (day, habit_id, completed) VALUES (?, ?, ?)`,
      [isoDay(day), habitId, completed ? 1 : 0]
    );
  }

  async completionsForDay(day: Date): Promise<Record<string, boolean>> {
    const rows = await this.db.all<{ habit_id: string; completed: number }>(
      `SELECT habit_id, completed FROM habit_completions WHERE day = ?`,
      [isoDay(day)]
    );
    const out: Record<string, boolean> = {};
    for (const r of rows) out[r.habit_id] = r.completed === 1;
    return out;
  }
}

// --- Row mappers ----------------------------------------------------------

function rowToCheckIn(r: Record<string, unknown>): CheckIn {
  return makeCheckIn({
    id: String(r.id),
    day: new Date(String(r.day) + "T00:00:00"),
    energy: Number(r.energy),
    mood: Number(r.mood),
    soreness: Number(r.soreness),
    sleepHours: Number(r.sleep_hours),
    hrv: Number(r.hrv),
    hrvBaseline: r.hrv_baseline != null ? Number(r.hrv_baseline) : 50,
  });
}

function rowToWorkoutLog(r: Record<string, unknown>): WorkoutLog {
  const movement: Movement =
    MOVEMENT_LIBRARY[String(r.movement_id)] ?? {
      id: String(r.movement_id),
      name: String(r.movement_id),
      pattern: "push" as Movement["pattern"],
    };
  const sets: SetLog[] = JSON.parse(String(r.sets_json));
  return {
    id: String(r.id),
    day: new Date(String(r.day) + "T00:00:00"),
    movement,
    sets,
    trimp: r.trimp != null ? (Number(r.trimp) as Trimp) : undefined,
    notes: r.notes != null ? String(r.notes) : undefined,
  };
}

function rowToJournal(r: Record<string, unknown>): JournalEntry {
  return makeJournalEntry({
    id: String(r.id),
    day: new Date(String(r.day) + "T00:00:00"),
    text: String(r.text),
    tags: JSON.parse(String(r.tags_json)),
    photo: r.photo != null ? String(r.photo) : undefined,
  });
}
