import { describe, expect, it, beforeEach } from "@jest/globals";
import {
  scheduleDefaultReminders,
  scheduleReminder,
  clearReminders,
  DEFAULT_REMINDERS,
} from "../src/services/notifications";
jest.mock("expo-notifications");
// The manual mock in __mocks__/expo-notifications records every call.
import { __records as notif, type RecordedSchedule } from "../__mocks__/expo-notifications";

/**
 * Guards the reminder scheduler against a regression where scheduling each
 * reminder cancelled all the others, leaving only the last one registered.
 */
describe("reminder scheduling", () => {
  beforeEach(() => notif.reset());

  it("schedules every default reminder (none dropped)", async () => {
    await scheduleDefaultReminders();
    expect(notif.scheduled.length).toBe(DEFAULT_REMINDERS.length);
    const titles = notif.scheduled.map((s: RecordedSchedule) => s.content.title);
    expect(titles).toContain("Morning routine");
    expect(titles).toContain("Evening routine");
    expect(titles).toContain("Weekly review");
  });

  it("clears the slate exactly once before re-scheduling", async () => {
    await scheduleDefaultReminders();
    // Cancellation should happen once for the whole batch, not once per item.
    expect(notif.cancelledAll).toBe(1);
  });

  it("a single scheduleReminder does not wipe existing reminders", async () => {
    await scheduleReminder(DEFAULT_REMINDERS[0]);
    await scheduleReminder(DEFAULT_REMINDERS[1]);
    expect(notif.scheduled.length).toBe(2);
    expect(notif.cancelledAll).toBe(0);
  });

  it("clearReminders wipes without scheduling", async () => {
    await scheduleReminder(DEFAULT_REMINDERS[0]);
    expect(notif.scheduled.length).toBe(1);
    await clearReminders();
    expect(notif.scheduled.length).toBe(0);
    expect(notif.cancelledAll).toBe(1);
  });

  it("omits weekday for daily reminders and sets it for the weekly one", async () => {
    await scheduleDefaultReminders();
    const morning = notif.scheduled.find((s: RecordedSchedule) => s.content.title === "Morning routine");
    const weekly = notif.scheduled.find((s: RecordedSchedule) => s.content.title === "Weekly review");
    expect((morning!.trigger as { weekday?: number }).weekday).toBeUndefined();
    // expo-notifications weekday is 1-7 (1 = Sunday). 0 is invalid.
    const w = (weekly!.trigger as { weekday?: number }).weekday;
    expect(w).toBeGreaterThanOrEqual(1);
    expect(w).toBeLessThanOrEqual(7);
  });
});
