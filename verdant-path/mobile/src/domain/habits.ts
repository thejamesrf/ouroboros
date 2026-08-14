/**
 * The 90-Day Foundational Habits Program.
 *
 * A structured habit-stacking program that builds the lifestyle foundation under
 * the training: morning/evening routines, daily movement, nutrition, and a
 * gradual buildup from one to two movement sessions per day. The 90 days close
 * with a daily progress photo and a 48-hour fast.
 *
 * Habits are scored per day (0-100%) as a weighted average of habit completion.
 */

export interface Habit {
  id: string;
  name: string;
  weight: number; // relative weight in the daily score
  description?: string;
}

export interface HabitGroup {
  name: string;
  habits: Habit[];
}

export const MORNING_ROUTINE: HabitGroup = {
  name: "Morning Routine (Minimum)",
  habits: [
    { id: "meditation", name: "Meditation 10+ min", weight: 1.5, description: "Sit, breathe, settle." },
    { id: "water_am", name: "Drink a glass of water", weight: 1 },
    { id: "brush_teeth", name: "Brush teeth", weight: 1 },
    { id: "todo_list", name: "Make a to-do list", weight: 1 },
    { id: "write_goals_am", name: "Write goals", weight: 1 },
  ],
};

export const DAILY_HABITS: HabitGroup = {
  name: "Daily Habits",
  habits: [
    { id: "water_gallon", name: "Drink 1 gallon of water", weight: 1.5 },
    {
      id: "wellness_cycle",
      name: "4-Day Holistic Wellness Cycle",
      weight: 2.0,
      description:
        "2x movement sessions/day: 1x 30+ min, 1x 45+ min outdoors, Zone 2 or RPE 8+. " +
        "Day 1 resistance (6 fundamentals, splittable), Day 2 cardio (LISS→threshold→LISS→fartlek), " +
        "Day 3 active recovery, Day 4 explosive/ballistic/functional/bodyweight/outdoor.",
    },
    { id: "diet", name: "Follow one diet (Kauffmann/Paleo/Whole30), minimize processed foods", weight: 1.5 },
    { id: "no_phone_bed", name: "No phone/social media in bed", weight: 1 },
  ],
};

export const EVENING_ROUTINE: HabitGroup = {
  name: "Evening Routine (Minimum)",
  habits: [
    { id: "review_todo", name: "Review to-do list", weight: 1 },
    { id: "write_goals_pm", name: "Write goals", weight: 1 },
    { id: "read", name: "Read a real book 15 min (alternate fiction/non-fiction)", weight: 1 },
    { id: "wind_down", name: "Wind-down or tapping meditation", weight: 1.5 },
  ],
};

export const NINETY_DAY_PROGRAM: HabitGroup[] = [MORNING_ROUTINE, DAILY_HABITS, EVENING_ROUTINE];

export function allHabits(): Habit[] {
  return NINETY_DAY_PROGRAM.flatMap((g) => g.habits);
}

/** Daily score (0-100%) as a weighted average of habit completion. */
export function habitScore(completed: Record<string, boolean>): number {
  const habits = allHabits();
  const totalWeight = habits.reduce((s, h) => s + h.weight, 0);
  if (totalWeight <= 0) return 0;
  const earned = habits.filter((h) => completed[h.id]).reduce((s, h) => s + h.weight, 0);
  return (earned / totalWeight) * 100;
}

/** Current streak of days scoring at or above `threshold` (most recent first). */
export function habitStreak(dailyScores: number[], threshold = 80): number {
  let streak = 0;
  for (let i = dailyScores.length - 1; i >= 0; i--) {
    if (dailyScores[i] >= threshold) streak++;
    else break;
  }
  return streak;
}

export interface BuildupPhase {
  weeks: string;
  focus: string;
  sessionsPerDay: number;
}

export const BUILDUP_PHASES: BuildupPhase[] = [
  { weeks: "Weeks 1-4", focus: "1 movement session/day (30+ min primary focus).", sessionsPerDay: 1 },
  { weeks: "Weeks 5-8", focus: "Add a second session (15-20 min Zone 2 or mobility) as capacity improves.", sessionsPerDay: 2 },
  { weeks: "Weeks 9-12", focus: "Full 2-session days; scale habits incrementally. Daily progress photo.", sessionsPerDay: 2 },
  { weeks: "End of 90 Days", focus: "Complete a 48-hour fast to close the program.", sessionsPerDay: 2 },
];
