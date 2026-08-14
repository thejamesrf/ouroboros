/** Community screen: group challenges, shared templates, forum stub. */
import React from "react";
import { ScrollView, StyleSheet, Text, View } from "react-native";
import { Body, Button, Card, SectionTitle } from "../components/ui";
import { useTheme } from "../theme";
import { spacing } from "../theme/tokens";

interface Challenge {
  id: string;
  name: string;
  description: string;
  participants: number;
}

const CHALLENGES: Challenge[] = [
  { id: "90day", name: "90-Day Habit Streak", description: "Build the foundational habits together.", participants: 42 },
  { id: "trimp10", name: "Weekly TRIMP 10", description: "Hit the foundation range every week.", participants: 18 },
];

export default function Community() {
  const { theme } = useTheme();
  return (
    <ScrollView contentContainerStyle={[styles.container, { backgroundColor: theme.bg }]}>
      <Text style={[styles.title, { color: theme.text }]}>Community 🌍</Text>

      <Card>
        <SectionTitle>Group challenges</SectionTitle>
        {CHALLENGES.map((c) => (
          <View key={c.id} style={styles.row}>
            <Text style={{ color: theme.text, fontWeight: "700" }}>{c.name}</Text>
            <Body muted>{c.description}</Body>
            <Body muted>{c.participants} members</Body>
            <View style={{ marginTop: spacing.sm }}>
              <Button label="Join" onPress={() => {}} />
            </View>
          </View>
        ))}
      </Card>

      <Card>
        <SectionTitle>Shared templates</SectionTitle>
        <Body muted>Trainers and members share workouts and habit protocols. (Browse and import coming with sync.)</Body>
      </Card>

      <Card>
        <SectionTitle>Forum</SectionTitle>
        <Body muted>Discuss tips, adjustments, and philosophy. (Forum threads coming with community sync.)</Body>
      </Card>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: spacing.lg, paddingBottom: spacing.xxl },
  title: { fontSize: 26, fontWeight: "800", marginBottom: spacing.md },
  row: { paddingVertical: spacing.md, borderBottomWidth: 1, borderBottomColor: "rgba(0,0,0,0.05)" },
});
