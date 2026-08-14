/** Planner screen: splits, session structure, template library, assignments. */
import React from "react";
import { ScrollView, StyleSheet, Text, View } from "react-native";
import { Body, Card, SectionTitle } from "../components/ui";
import { useTheme } from "../theme";
import { spacing } from "../theme/tokens";
import { SPLITS } from "../domain/planner";
import { defaultPlanner } from "../domain/templates";
import { canEditPlans } from "../domain/roles";
import { useAppStore } from "../state/store";

export default function Planner() {
  const { theme } = useTheme();
  const profile = useAppStore((s) => s.profile);
  const planner = defaultPlanner();
  const split = SPLITS[profile.weeklyFrequency] ?? SPLITS[3];

  return (
    <ScrollView contentContainerStyle={[styles.container, { backgroundColor: theme.bg }]}>
      <Text style={[styles.title, { color: theme.text }]}>Planner 🗓️</Text>

      <Card>
        <SectionTitle>Your split</SectionTitle>
        <Body>{split.name} · {profile.weeklyFrequency}x/week</Body>
        {split.days.map((day, i) => (
          <View key={i} style={{ marginTop: spacing.sm }}>
            <Text style={{ color: theme.text, fontWeight: "600" }}>Day {i + 1}</Text>
            <Body muted>{day.join(", ")}</Body>
          </View>
        ))}
      </Card>

      <Card>
        <SectionTitle>Template library</SectionTitle>
        {Object.values(planner.templates).map((t) => (
          <View key={t.id} style={styles.templateRow}>
            <Text style={{ color: theme.text, fontWeight: "600" }}>{t.name}</Text>
            <Body muted>{t.tag} · TRIMP {t.intendedTrimp}</Body>
          </View>
        ))}
      </Card>

      {canEditPlans(profile.role) && (
        <Card>
          <SectionTitle>Trainer tools</SectionTitle>
          <Body muted>Create workouts, assign splits (1x–6x/week), and adjust plans based on member metrics. Member-adjustment requests appear here.</Body>
        </Card>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: spacing.lg, paddingBottom: spacing.xxl },
  title: { fontSize: 26, fontWeight: "800", marginBottom: spacing.md },
  templateRow: { paddingVertical: spacing.sm, borderBottomWidth: 1, borderBottomColor: "rgba(0,0,0,0.05)" },
});
