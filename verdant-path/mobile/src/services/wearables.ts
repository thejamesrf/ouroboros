/**
 * Wearable integration architecture.
 *
 * Verdant Path reads HRV, sleep, and (optionally) workout data from wearables to
 * pre-fill daily check-ins. Each provider implements a common adapter so the UI
 * is provider-agnostic. Concrete integration requires platform native modules
 * (Apple HealthKit, Garmin Connect IQ, Oura Cloud) and is stubbed here; the
 * interfaces let the app compile and run everywhere while real providers are
 * wired up per-platform.
 */

export interface WearableReading {
  hrv?: number; // ms
  sleepHours?: number;
  sleepQuality?: number; // 1-5
  restingHr?: number; // bpm
  steps?: number;
  timestamp: Date;
}

export interface WearableAdapter {
  readonly id: string;
  readonly label: string;
  /** Whether this provider is available on the current device. */
  isAvailable(): Promise<boolean>;
  /** Request user authorization to read metrics. */
  requestAuth(): Promise<boolean>;
  /** Pull the most recent reading (last night's sleep + morning HRV). */
  latestReading(): Promise<WearableReading | null>;
}

/** A no-op adapter for environments without a wearable provider. */
export class NullWearableAdapter implements WearableAdapter {
  readonly id = "none";
  readonly label = "No wearable";
  async isAvailable() {
    return true;
  }
  async requestAuth() {
    return true;
  }
  async latestReading() {
    return null;
  }
}

/** Apple Health adapter (stubbed — wire up with react-native-health in native build). */
export class AppleHealthAdapter implements WearableAdapter {
  readonly id = "apple_health";
  readonly label = "Apple Health";
  async isAvailable() {
    return false; // enable when react-native-health is installed
  }
  async requestAuth() {
    return false;
  }
  async latestReading() {
    return null;
  }
}

/** Oura Cloud adapter (stubbed — wire up with Oura API tokens). */
export class OuraAdapter implements WearableAdapter {
  readonly id = "oura";
  readonly label = "Oura";
  async isAvailable() {
    return false;
  }
  async requestAuth() {
    return false;
  }
  async latestReading() {
    return null;
  }
}

/** Garmin Connect adapter (stubbed — wire up with Garmin Connect IQ / Health API). */
export class GarminAdapter implements WearableAdapter {
  readonly id = "garmin";
  readonly label = "Garmin";
  async isAvailable() {
    return false;
  }
  async requestAuth() {
    return false;
  }
  async latestReading() {
    return null;
  }
}

export const AVAILABLE_ADAPTERS: WearableAdapter[] = [
  new AppleHealthAdapter(),
  new OuraAdapter(),
  new GarminAdapter(),
];

let activeAdapter: WearableAdapter = new NullWearableAdapter();

export function getActiveWearable(): WearableAdapter {
  return activeAdapter;
}

export function setActiveWearable(adapter: WearableAdapter): void {
  activeAdapter = adapter;
}
