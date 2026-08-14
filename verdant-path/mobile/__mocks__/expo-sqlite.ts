/**
 * Test mock for expo-sqlite. openDatabaseAsync always throws so that
 * `openDatabase` falls back to the in-memory store — which is what the storage
 * tests exercise.
 */
export async function openDatabaseAsync(_name: string): Promise<unknown> {
  throw new Error("expo-sqlite is mocked out in tests");
}
