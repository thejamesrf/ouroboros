/** Onboarding quiz: goals, frequency, experience, injuries (spec §9). */
import React, { useState } from "react";
import { ScrollView, StyleSheet, Text, TextInput, View } from "react-native";
import { Button, Card, SectionTitle } from "../components/ui";
import { useTheme } from "../theme";
import { spacing } from "../theme/tokens";
import { useAppStore } from "../state/store";
import {
  type Experience,
  type Goal,
  type UserProfile,
} from "../domain/roles";

const GOAL_OPTIONS: Goal[] = [
  "resilience",
  "longevity",
  "endurance",
  "strength",
  "hypertrophy",
  "mobility",
  "work_capacity",
  "cardio",
];

const EXPERIENCE_OPTIONS: Experience[] = ["beginner", "intermediate", "advanced"];

export default function Onboarding() {
  const { theme } = useTheme();
  const completeOnboarding = useAppStore((s) => s.completeOnboarding);

  const [goals, setGoals] = useState<Goal[]>(["resilience", "longevity"]);
  const [frequency, setFrequency] = useState(3);
  const [experience, setExperience] = useState<Experience>("intermediate");
  const [injuries, setInjuries] = useState("");
  const [diet, setDiet] = useState<UserProfile["dietChoice"]>();
  const [hrvBaseline, setHrvBaseline] = useState(50);

  const toggleGoal = (g: Goal) =>
    setGoals((cur) => (cur.includes(g) ? cur.filter((x) => x !== g) : [...cur, g]));

  return (
    <ScrollView contentContainerStyle={[styles.container, { backgroundColor: theme.bg }]}>
      <Text style={[styles.title, { color: theme.text }]}>Welcome to Verdant Path 🌿</Text>
      <Text style={[styles.subtitle, { color: theme.muted }]}>
        Let's tailor your training. A few quick questions.
      </Text>

      <Card>
        <SectionTitle>Goals</SectionTitle>
        <View style={styles.chipRow}>
          {GOAL_OPTIONS.map((g) => {
            const active = goals.includes(g);
            return (
              <Button
                key={g}
                label={g}
                variant={active ? "primary" : "ghost"}
                onPress={() => toggleGoal(g)}
              />
            );
          })}
        </View>
      </Card>

      <Card>
        <SectionTitle>Weekly gym frequency</SectionTitle>
        <View style={styles.chipRow}>
          {[1, 2, 3, 4, 5, 6].map((n) => (
            <Button
              key={n}
              label={`${n}x`}
              variant={frequency === n ? "primary" : "ghost"}
              onPress={() => setFrequency(n)}
            />
          ))}
        </View>
        <Text style={{ color: theme.muted, marginTop: spacing.sm }}>
          We'll suggest the matching split and ensure all six movement patterns are hit weekly.
        </Text>
      </Card>

      <Card>
        <SectionTitle>Experience</SectionTitle>
        <View style={styles.chipRow}>
          {EXPERIENCE_OPTIONS.map((e) => (
            <Button
              key={e}
              label={e}
              variant={experience === e ? "primary" : "ghost"}
              onPress={() => setExperience(e)}
            />
          ))}
        </View>
      </Card>

      <Card>
        <SectionTitle>Injuries or limitations</SectionTitle>
        <TextInput
          style={[styles.input, { color: theme.text, borderColor: theme.border }]}
          placeholder="e.g. lower back tightness, history of ankle sprain"
          placeholderTextColor={theme.muted}
          value={injuries}
          onChangeText={setInjuries}
          multiline
        />
      </Card>

      <Card>
        <SectionTitle>Diet choice</SectionTitle>
        <View style={styles.chipRow}>
          {(["Kauffmann", "Paleo", "Whole30"] as const).map((d) => (
            <Button
              key={d}
              label={d}
              variant={diet === d ? "primary" : "ghost"}
              onPress={() => setDiet(d)}
            />
          ))}
        </View>
      </Card>

      <Card>
        <SectionTitle>HRV baseline (ms)</SectionTitle>
        <TextInput
          style={[styles.input, { color: theme.text, borderColor: theme.border }]}
          keyboardType="numeric"
          value={String(hrvBaseline)}
          onChangeText={(v) => setHrvBaseline(Number(v) || 50)}
        />
        <Text style={{ color: theme.muted, marginTop: spacing.sm }}>
          Your typical resting HRV. Used to scale the fatigue cue to you personally.
        </Text>
      </Card>

      <Button
        label="Start my journey"
        onPress={() =>
          completeOnboarding({
            goals,
            weeklyFrequency: frequency,
            experience,
            injuries: injuries.split(",").map((s) => s.trim()).filter(Boolean),
            dietChoice: diet,
            hrvBaseline,
          })
        }
      />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: spacing.lg, paddingBottom: spacing.xxl },
  title: { fontSize: 26, fontWeight: "800", marginBottom: spacing.xs },
  subtitle: { fontSize: 15, marginBottom: spacing.lg },
  chipRow: { flexDirection: "row", flexWrap: "wrap", gap: spacing.sm },
  input: {
    borderWidth: 1,
    borderRadius: 12,
    padding: spacing.md,
    minHeight: 48,
    textAlignVertical: "top",
  },
});
