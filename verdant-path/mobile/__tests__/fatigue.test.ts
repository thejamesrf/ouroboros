import { describe, expect, it } from "@jest/globals";
import {
  fatigueFromCheckin,
  fatigueCue,
  readinessAdjustment,
  Fatigue,
} from "../src/domain/fatigue";

describe("fatigue cues", () => {
  it("maps boundaries to the correct cue", () => {
    expect(fatigueCue(0)).toBe(Fatigue.Green);
    expect(fatigueCue(39.9)).toBe(Fatigue.Green);
    expect(fatigueCue(40)).toBe(Fatigue.Amber);
    expect(fatigueCue(69.9)).toBe(Fatigue.Amber);
    expect(fatigueCue(70)).toBe(Fatigue.Red);
    expect(fatigueCue(100)).toBe(Fatigue.Red);
  });

  it("lands the spec worked example in amber", () => {
    // Energy=4, Mood=3, Soreness=2, Sleep=7h, HRV=55ms, baseline 50
    const pct = fatigueFromCheckin({ energy: 4, mood: 3, soreness: 2, sleepHours: 7, hrv: 55 });
    expect(pct).toBeGreaterThanOrEqual(40);
    expect(pct).toBeLessThan(70);
    expect(fatigueCue(pct)).toBe(Fatigue.Amber);
  });

  it("flags exhaustion as red", () => {
    const pct = fatigueFromCheckin({ energy: 1, mood: 1, soreness: 5, sleepHours: 2, hrv: 30 });
    expect(pct).toBeGreaterThanOrEqual(70);
    expect(fatigueCue(pct)).toBe(Fatigue.Red);
  });

  it("flags a well-rested day as green", () => {
    const pct = fatigueFromCheckin({ energy: 5, mood: 5, soreness: 1, sleepHours: 8, hrv: 60 });
    expect(pct).toBeLessThan(40);
    expect(fatigueCue(pct)).toBe(Fatigue.Green);
  });

  it("higher soreness raises fatigue", () => {
    const low = fatigueFromCheckin({ energy: 5, mood: 5, soreness: 1, sleepHours: 8, hrv: 50 });
    const high = fatigueFromCheckin({ energy: 5, mood: 5, soreness: 5, sleepHours: 8, hrv: 50 });
    expect(high).toBeGreaterThan(low);
  });

  it("clamps to 0-100", () => {
    const extreme = fatigueFromCheckin({ energy: 1, mood: 1, soreness: 5, sleepHours: 0, hrv: 0 });
    expect(extreme).toBeGreaterThanOrEqual(0);
    expect(extreme).toBeLessThanOrEqual(100);
  });
});

describe("readiness adjustment", () => {
  it("leaves green days unrestricted", () => {
    const adj = readinessAdjustment(10);
    expect(adj.cue).toBe(Fatigue.Green);
    expect(adj.volumeChange).toBe(0);
  });

  it("cuts volume on amber days", () => {
    const adj = readinessAdjustment(50);
    expect(adj.cue).toBe(Fatigue.Amber);
    expect(adj.volumeChange).toBeLessThan(0);
  });

  it("deep-cuts volume on red days", () => {
    const adj = readinessAdjustment(85);
    expect(adj.cue).toBe(Fatigue.Red);
    expect(adj.volumeChange).toBeLessThanOrEqual(-0.4);
  });
});
