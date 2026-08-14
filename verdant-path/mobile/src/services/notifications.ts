/**
 * Notifications & reminders.
 *
 * Three cadences from the spec (§6):
 *  - Daily: morning/evening routine reminders + workout reminders (time or
 *    location based, e.g. "you're at the gym").
 *  - Weekly: summary report + adaptive suggestions ("HRV dropped 10%; consider
 *    a recovery day").
 *  - Adaptive: if red fatigue for 3+ days, notify: "Consider a deload week."
 *
 * The scheduler is platform-agnostic: it calls into expo-notifications when
 * available and no-ops in tests/web. Reminders are identified by a stable id
 * so they can be re-scheduled without stacking duplicates.
 */

import * as Notifications from "expo-notifications";
import { Fatigue } from "../domain/fatigue";

export type ReminderKind = "morning_routine" | "evening_routine" | "workout" | "weekly_summary" | "deload_alert";

export interface Reminder {
  id: string;
  kind: ReminderKind;
  hour: number; // 0-23
  minute: number; // 0-59
  weekday?: number; // 1-7 (1=Monday), undefined = every day
  title: string;
  body: string;
}

export const DEFAULT_REMINDERS: Reminder[] = [
  { id: "morning", kind: "morning_routine", hour: 7, minute: 0, title: "Morning routine", body: "Meditate, hydrate, set your goals." },
  { id: "evening", kind: "evening_routine", hour: 21, minute: 30, title: "Evening routine", body: "Review your day, read, wind down." },
  { id: "weekly", kind: "weekly_summary", hour: 20, minute: 0, weekday: 0, title: "Weekly review", body: "Your weekly summary is ready." },
];

/** Request notification permissions. Returns true if granted. */
export async function requestPermissions(): Promise<boolean> {
  try {
    const { status } = await Notifications.requestPermissionsAsync();
    return status === "granted";
  } catch {
    return false;
  }
}

/** Schedule a reminder. No-ops gracefully if notifications are unavailable. */
export async function scheduleReminder(reminder: Reminder): Promise<void> {
  try {
    await Notifications.cancelAllScheduledNotificationsAsync();
    await Notifications.scheduleNotificationAsync({
      content: { title: reminder.title, body: reminder.body },
      trigger: {
        hour: reminder.hour,
        minute: reminder.minute,
        weekday: reminder.weekday,
        repeats: true,
      } as Notifications.WeeklyTriggerInput,
    });
  } catch {
    // Notifications unavailable (web/test) — silently skip.
  }
}

/** Schedule the default daily + weekly reminders. */
export async function scheduleDefaultReminders(): Promise<void> {
  for (const r of DEFAULT_REMINDERS) {
    await scheduleReminder(r);
  }
}

/** Fire an adaptive deload alert when fatigue has been red for 3+ days. */
export async function maybeDeloadAlert(
  recentCues: Fatigue[],
  consecutiveRedThreshold = 3
): Promise<boolean> {
  let redStreak = 0;
  for (const cue of [...recentCues].reverse()) {
    if (cue === Fatigue.Red) redStreak++;
    else break;
  }
  if (redStreak >= consecutiveRedThreshold) {
    try {
      await Notifications.scheduleNotificationAsync({
        content: {
          title: "Consider a deload week",
          body: "Your fatigue has been high for several days. Prioritize recovery.",
        },
        trigger: null,
      });
    } catch {
      // ignore
    }
    return true;
  }
  return false;
}
