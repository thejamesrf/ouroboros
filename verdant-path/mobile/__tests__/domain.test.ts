import { describe, expect, it } from "@jest/globals";
import {
  MOVEMENT_LIBRARY,
  allPatternsCovered,
  missingPatterns,
  Pattern,
} from "../src/domain/movements";
import { Trimp, trimpForSession, weeklyTrimp, weeklyTrimpStatus, trimpLevel } from "../src/domain/trimp";
import { SPLITS, splitForFrequency, planCoverage } from "../src/domain/planner";
import { defaultPlanner } from "../src/domain/templates";
import { makeCheckIn, makeJournalEntry, sessionTrimpFor } from "../src/domain/tracker";
import { weeklyReview, acwr } from "../src/domain/metrics";
import { allHabits, habitScore, habitStreak, NINETY_DAY_PROGRAM, BUILDUP_PHASES } from "../src/domain/habits";

describe("movements", () => {
  it("defines all six patterns", () => {
    const patterns = new Set(Object.values(Pattern));
    expect(patterns.size).toBe(6);
  });

  it("the library covers all patterns", () => {
    const movements = Object.values(MOVEMENT_LIBRARY);
    expect(allPatternsCovered(movements)).toBe(true);
    expect(missingPatterns(movements)).toEqual([]);
  });

  it("detects missing patterns", () => {
    const onlyPush = [MOVEMENT_LIBRARY.bench_press];
    expect(allPatternsCovered(onlyPush)).toBe(false);
    expect(missingPatterns(onlyPush).length).toBe(5);
  });
});

describe("trimp", () => {
  it("clamps levels", () => {
    expect(trimpLevel(0)).toBe(Trimp.Low);
    expect(trimpLevel(2)).toBe(Trimp.Medium);
    expect(trimpLevel(99)).toBe(Trimp.High);
  });

  it("estimates from peak RPE", () => {
    expect(trimpForSession([{ rpe: 9 }])).toBe(Trimp.High);
    expect(trimpForSession([{ rpe: 7 }])).toBe(Trimp.Medium);
    expect(trimpForSession([{ rpe: 4 }])).toBe(Trimp.Low);
  });

  it("explicit override wins", () => {
    expect(trimpForSession([{ rpe: 9 }], Trimp.Low)).toBe(Trimp.Low);
  });

  it("sums a week and reports status", () => {
    const total = weeklyTrimp([Trimp.High, Trimp.Medium, Trimp.Low, Trimp.Medium]);
    expect(total).toBe(8);
    expect(weeklyTrimpStatus(total)).toContain("foundation");
  });
});

describe("planner", () => {
  it("has splits for frequencies 1-6", () => {
    for (let f = 1; f <= 6; f++) {
      expect(splitForFrequency(f).name).toBeTruthy();
    }
  });

  it("rejects invalid frequency", () => {
    expect(() => splitForFrequency(7)).toThrow();
    expect(() => splitForFrequency(0)).toThrow();
  });

  it("default plan covers all six patterns", () => {
    const planner = defaultPlanner();
    const plan = planner.buildPlan({
      id: "p1",
      frequency: 5,
      days: [
        planner.templates["posterior_chain"],
        planner.templates["liss_run"],
        planner.templates["chest_biceps"],
        planner.templates["hiit"],
        planner.templates["shoulders_triceps"],
      ],
    });
    expect(planCoverage(plan)).toBe(true);
  });

  it("schedules consecutive days", () => {
    const planner = defaultPlanner();
    const plan = planner.buildPlan({
      id: "p1",
      frequency: 3,
      days: [planner.templates["posterior_chain"], planner.templates["liss_run"], planner.templates["active_recovery"]],
    });
    const schedule = planner.schedule(plan, new Date("2025-01-06"));
    expect(schedule.length).toBe(3);
    expect(schedule[2].date.getDate() - schedule[0].date.getDate()).toBe(2);
  });
});

describe("tracker", () => {
  it("check-in cue matches the spec example (amber)", () => {
    const ci = makeCheckIn({
      id: "ci1",
      day: new Date("2025-01-06"),
      energy: 4,
      mood: 3,
      soreness: 2,
      sleepHours: 7,
      hrv: 55,
    });
    expect(ci.fatiguePercent).toBeGreaterThanOrEqual(40);
    expect(ci.fatiguePercent).toBeLessThan(70);
  });

  it("resolves explicit trimp override", () => {
    const ci = makeCheckIn({ id: "ci1", day: new Date(), energy: 5, mood: 5, soreness: 1, sleepHours: 8, hrv: 60 });
    const log = { id: "w1", day: new Date(), movement: MOVEMENT_LIBRARY.deadlift, sets: [{ rpe: 9 }], trimp: Trimp.Medium };
    expect(sessionTrimpFor(log)).toBe(Trimp.Medium);
  });

  it("normalizes journal tags", () => {
    const entry = makeJournalEntry({
      id: "j1",
      day: new Date(),
      text: "Lower back tight.",
      tags: ["#Recovery", "  #Soreness ", "recovery"],
    });
    expect(entry.tags).toEqual(["recovery", "soreness"]);
  });
});

describe("metrics", () => {
  it("computes ACWR", () => {
    expect(acwr(10, [])).toBeNull();
    expect(acwr(10, [8, 8])).toBeCloseTo(1.25);
  });

  it("suggests deload on high ACWR + HRV down", () => {
    const ci = makeCheckIn({ id: "ci1", day: new Date("2025-01-06"), energy: 4, mood: 3, soreness: 2, sleepHours: 7, hrv: 52 });
    const log = {
      id: "w1",
      day: new Date("2025-01-06"),
      movement: MOVEMENT_LIBRARY.deadlift,
      sets: [{ rpe: 9 }],
      trimp: Trimp.High,
    };
    const summary = weeklyReview({
      weekOf: new Date("2025-01-06"),
      checkins: [ci],
      logs: [log],
      priorWeeksTrimp: [1, 2],
      hrvTrendDown: true,
    });
    expect(summary.acwr).not.toBeNull();
    expect(summary.acwr!).toBeGreaterThan(1.5);
    expect(summary.suggestion.toLowerCase()).toContain("deload");
  });

  it("suggests progressive load when stable", () => {
    const ci = makeCheckIn({ id: "ci1", day: new Date("2025-01-06"), energy: 5, mood: 5, soreness: 1, sleepHours: 8, hrv: 60 });
    const log = {
      id: "w1",
      day: new Date("2025-01-06"),
      movement: MOVEMENT_LIBRARY.bench_press,
      sets: [{ rpe: 7 }],
      trimp: Trimp.Medium,
    };
    const summary = weeklyReview({
      weekOf: new Date("2025-01-06"),
      checkins: [ci],
      logs: [log],
      priorWeeksTrimp: [2, 2, 2],
      hrvTrendDown: false,
    });
    expect(summary.suggestion.toLowerCase()).toContain("progressive load");
  });
});

describe("habits", () => {
  it("has three habit groups", () => {
    expect(NINETY_DAY_PROGRAM.length).toBe(3);
  });

  it("scores a perfect day at 100", () => {
    const habits = allHabits();
    const completed = Object.fromEntries(habits.map((h) => [h.id, true]));
    expect(habitScore(completed)).toBe(100);
  });

  it("counts a streak of good days", () => {
    expect(habitStreak([60, 85, 90, 82])).toBe(3);
    expect(habitStreak([90, 90, 70, 90])).toBe(1);
  });

  it("has four buildup phases", () => {
    expect(BUILDUP_PHASES.length).toBe(4);
    expect(BUILDUP_PHASES[3].weeks).toBe("End of 90 Days");
  });
});
