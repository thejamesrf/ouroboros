/**
 * Central app store (Zustand).
 *
 * Holds the active user profile plus the in-memory caches of recent records.
 * The store is the single source of truth the screens read from; it delegates
 * persistence to the repositories (offline-first SQLite).
 */

import { create } from "zustand";
import { defaultProfile, type UserProfile } from "../domain/roles";
import type { CheckIn, JournalEntry, WorkoutLog } from "../domain/tracker";
import { fatigueCue, type Fatigue } from "../domain/fatigue";
import type { WeeklySummary } from "../domain/metrics";

export interface AppState {
  profile: UserProfile;
  onboarded: boolean;

  // Recent records (loaded from storage on app open).
  checkins: CheckIn[];
  workoutLogs: WorkoutLog[];
  journal: JournalEntry[];

  // Derived/cached.
  lastSummary: WeeklySummary | null;

  setProfile: (profile: Partial<UserProfile>) => void;
  completeOnboarding: (profile: Partial<UserProfile>) => void;
  setRole: (role: UserProfile["role"]) => void;

  addCheckin: (c: CheckIn) => void;
  addWorkoutLog: (w: WorkoutLog) => void;
  addJournal: (e: JournalEntry) => void;
  setSummary: (s: WeeklySummary) => void;

  /** Today's fatigue cue from the latest check-in (or null). */
  todayCue: () => Fatigue | null;
}

export const useAppStore = create<AppState>((set, get) => ({
  profile: defaultProfile(),
  onboarded: false,
  checkins: [],
  workoutLogs: [],
  journal: [],
  lastSummary: null,

  setProfile: (profile) => set((s) => ({ profile: { ...s.profile, ...profile } })),

  completeOnboarding: (profile) =>
    set((s) => ({ profile: { ...s.profile, ...profile, onboarded: true }, onboarded: true })),

  setRole: (role) => set((s) => ({ profile: { ...s.profile, role } })),

  addCheckin: (c) => set((s) => ({ checkins: [...s.checkins.filter((x) => x.id !== c.id), c] })),
  addWorkoutLog: (w) => set((s) => ({ workoutLogs: [...s.workoutLogs.filter((x) => x.id !== w.id), w] })),
  addJournal: (e) => set((s) => ({ journal: [e, ...s.journal.filter((x) => x.id !== e.id)] })),
  setSummary: (summary) => set({ lastSummary: summary }),

  todayCue: () => {
    const today = new Date().toISOString().slice(0, 10);
    const latest = get().checkins.find((c) => c.day.toISOString().slice(0, 10) === today);
    if (!latest) return null;
    return fatigueCue(latest.fatiguePercent);
  },
}));
