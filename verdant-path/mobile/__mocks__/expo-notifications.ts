/**
 * Test mock for expo-notifications. Records scheduled/cancelled calls so the
 * reminder scheduler can be verified without native modules.
 */
export interface RecordedSchedule {
  content: { title?: string; body?: string };
  trigger: { hour?: number; minute?: number; weekday?: number; repeats?: boolean } | null;
}

export interface NotificationRecords {
  scheduled: RecordedSchedule[];
  cancelledAll: number;
  reset(): void;
}

const scheduled: RecordedSchedule[] = [];
let cancelledAll = 0;

export const __records: NotificationRecords = {
  scheduled,
  get cancelledAll() {
    return cancelledAll;
  },
  reset() {
    scheduled.length = 0;
    cancelledAll = 0;
  },
};

export async function requestPermissionsAsync() {
  return { status: "granted" };
}

export async function cancelAllScheduledNotificationsAsync() {
  cancelledAll += 1;
  scheduled.length = 0;
}

export async function scheduleNotificationAsync(input: RecordedSchedule) {
  scheduled.push(input);
  return "id";
}
