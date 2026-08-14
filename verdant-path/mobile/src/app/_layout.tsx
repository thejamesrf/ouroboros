/**
 * Root layout: theme provider + onboarding gate + bottom-tab navigation.
 *
 * Bottom tabs (spec §9): Today, Planner, Metrics, Journal, Community.
 * A high-contrast toggle lives in the header for accessibility.
 */
import React from "react";
import { Pressable, Text } from "react-native";
import { Tabs } from "expo-router";
import { ThemeProvider, useTheme } from "../theme";
import { useAppStore } from "../state/store";
import Onboarding from "../screens/Onboarding";
import { requestPermissions, scheduleDefaultReminders } from "../services/notifications";
import { useEffect } from "react";

function TabLayout() {
  const { theme, toggleHighContrast } = useTheme();

  useEffect(() => {
    (async () => {
      await requestPermissions();
      await scheduleDefaultReminders();
    })();
  }, []);

  return (
    <Tabs
      screenOptions={{
        headerStyle: { backgroundColor: theme.surface },
        headerTintColor: theme.text,
        tabBarStyle: { backgroundColor: theme.surface, borderTopColor: theme.border },
        tabBarActiveTintColor: theme.primary,
        tabBarInactiveTintColor: theme.muted,
        headerRight: () => (
          <Pressable onPress={toggleHighContrast} style={{ paddingHorizontal: 16 }}>
            <Text style={{ color: theme.primary, fontWeight: "700" }}>Aa</Text>
          </Pressable>
        ),
      }}
    >
      <Tabs.Screen name="today" options={{ title: "Today" }} />
      <Tabs.Screen name="planner" options={{ title: "Planner" }} />
      <Tabs.Screen name="metrics" options={{ title: "Metrics" }} />
      <Tabs.Screen name="journal" options={{ title: "Journal" }} />
      <Tabs.Screen name="community" options={{ title: "Community" }} />
    </Tabs>
  );
}

function Root() {
  const onboarded = useAppStore((s) => s.onboarded);
  if (!onboarded) return <Onboarding />;
  return <TabLayout />;
}

export default function RootLayout() {
  return (
    <ThemeProvider>
      <Root />
    </ThemeProvider>
  );
}
