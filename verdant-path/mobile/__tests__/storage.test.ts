import { describe, expect, it } from "@jest/globals";
import { JournalRepository, CheckInRepository, InMemoryDatabase, SCHEMA } from "../src/storage/db";
import { makeJournalEntry, makeCheckIn } from "../src/domain/tracker";



/**
 * The in-memory fallback (used on web/tests) must honour ORDER BY ... DESC and
 * LIMIT so the Journal "recent" list returns newest-first, and range filters
 * (`day >= ? AND day <= ?`) so weekly queries don't leak rows from other weeks.
 */
describe("in-memory storage", () => {
  function freshDb() {
    return new InMemoryDatabase(SCHEMA);
  }

  it("returns journal entries newest-first via ORDER BY day DESC LIMIT", async () => {
    const repo = new JournalRepository(freshDb());
    const days = ["2025-01-02", "2025-01-05", "2025-01-03"];
    for (const d of days) {
      await repo.save(
        makeJournalEntry({ id: `j-${d}`, day: new Date(d), text: `note ${d}`, tags: [] })
      );
    }
    const recent = await repo.recent(50);
    expect(recent.map((e) => e.day.toISOString().slice(0, 10))).toEqual([
      "2025-01-05",
      "2025-01-03",
      "2025-01-02",
    ]);
  });

  it("honours LIMIT after ordering", async () => {
    const repo = new JournalRepository(freshDb());
    for (const d of ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04"]) {
      await repo.save(makeJournalEntry({ id: `j-${d}`, day: new Date(d), text: d, tags: [] }));
    }
    expect((await repo.recent(2)).map((e) => e.text)).toEqual(["2025-01-04", "2025-01-03"]);
  });

  it("filters check-ins by week range (no leak from other weeks)", async () => {
    const repo = new CheckInRepository(freshDb());
    const ci = (d: string) =>
      makeCheckIn({
        id: `c-${d}`,
        day: new Date(d),
        energy: 4,
        mood: 3,
        soreness: 2,
        sleepHours: 7,
        hrv: 55,
      });
    // Mon-Sun of the week of 2025-01-06 is 2025-01-06..2025-01-12.
    await repo.save(ci("2025-01-05")); // prior week — must be excluded
    await repo.save(ci("2025-01-06")); // in week
    await repo.save(ci("2025-01-12")); // in week (Sunday)
    await repo.save(ci("2025-01-13")); // next week — must be excluded

    const week = await repo.forWeek(new Date("2025-01-06"), new Date("2025-01-12"));
    const days = week.map((c) => c.day.toISOString().slice(0, 10)).sort();
    expect(days).toEqual(["2025-01-06", "2025-01-12"]);
  });
});
