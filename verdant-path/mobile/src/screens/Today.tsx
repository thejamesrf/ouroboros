/** Today screen: daily check-in → fatigue cue, plus workout of the day. */
import React, { useState } from "react";
import { ScrollView, StyleSheet, Text, View } from "react-native";
import { Body, Button, Card, FatigueBadge, ProgressBar, SectionTitle } from "../components/ui";
import { useTheme } from "../theme";
import { spacing, fatigueColor } from "../theme/tokens";
import { useAppStore } from "../state/store";
import { makeCheckIn } from "../domain/tracker";
import { fatigueFromCheckin, readinessAdjustment } from "../domain/fatigue";
import { defaultPlanner } from "../domain/templates";

export default function Today() {
  const { theme } = useTheme();
  const profile = useAppStore((s) => s.profile);
  const addCheckin = useAppStore((s) => s.addCheckin);

  const [energy, setEnergy] = useState(4);
  const [mood, setMood] = useState(4);
  const [soreness, setSoreness] = useState(2);
  const [sleep, setSleep] = useState(7);
  const [hrv, setHrv] = useState(50);

  const fatiguePct = fatigueFromCheckin({
    energy,
    mood,
    soreness,
    sleepHours: sleep,
    hrv,
    hrvBaseline: profile.hrvBaseline,
  });
  const adj = readinessAdjustment(fatiguePct);

  const planner = defaultPlanner();
  const todayPlan =
    profile.weeklyFrequency >= 1
      ? Object.values(planner.templates)[0]
      : null;

  const submit = () => {
    addCheckin(
      makeCheckIn({
        id: `ci-${Date.now()}`,
        day: new Date(),
        energy,
        mood,
        soreness,
        sleepHours: sleep,
        hrv,
        hrvBaseline: profile.hrvBaseline,
      })
    );
  };

  return (
    <ScrollView contentContainerStyle={[styles.container, { backgroundColor: theme.bg }]}>
      <Text style={[styles.title, { color: theme.text }]}>Today 🌿</Text>

      <Card>
        <SectionTitle>Daily check-in</SectionTitle>
        <Slider label="Energy" value={energy} onChange={setEnergy} theme={theme} />
        <Slider label="Mood" value={mood} onChange={setMood} theme={theme} />
        <Slider label="Soreness" value={soreness} onChange={setSoreness} theme={theme} />
        <Slider label="Sleep (hours)" value={sleep} max={9} onChange={setSleep} theme={theme} />
        <Slider label="HRV (ms)" value={hrv} max={90} onChange={setHrv} theme={theme} />

        <View style={{ marginTop: spacing.md }}>
          <Text style={{ color: theme.muted, marginBottom: spacing.xs }}>
            Fatigue {fatiguePct.toFixed(1)}%
          </Text>
          <ProgressBar percent={fatiguePct} color={fatigueColor[adj.cue]} />
          <View style={{ marginTop: spacing.sm }}>
            <FatigueBadge fatigue={adj.cue} />
          </View>
          <Body muted style={{ marginTop: spacing.sm }}>{adj.note}</Body>
          {(adj.volumeChange || adj.intensityChange) && (
            <Body muted>
              Volume {adj.volumeChange < 0 ? `reduce ${(-adj.volumeChange * 100).toFixed(0)}%` : "hold"} ·{" "}
              Intensity {adj.intensityChange < 0 ? `reduce ${(-adj.intensityChange * 100).toFixed(0)}%` : "hold"}
            </Body>
          )}
        </View>

        <View style={{ marginTop: spacing.lg }}>
          <Button label="Save check-in" onPress={submit} />
        </View>
      </Card>

      {todayPlan && (
        <Card>
          <SectionTitle>Workout of the day</SectionTitle>
          <Body>{todayPlan.name} · {todayPlan.tag}</Body>
          {todayPlan.blocks.map((b) => (
            <View key={b.name} style={{ marginTop: spacing.sm }}>
              <Text style={{ color: theme.text, fontWeight: "600" }}>{b.name}</Text>
              <Body muted>
                {b.assignments?.map((a) => a.movement.name).join(", ") || b.notes}
              </Body>
            </View>
          ))}
          <Body muted style={{ marginTop: spacing.sm }}>Cooldown: {todayPlan.cooldown}</Body>
        </Card>
      )}
    </ScrollView>
  );
}

function Slider({
  label,
  value,
  onChange,
  max = 5,
  theme,
}: {
  label: string;
  value: number;
  onChange: (v: number) => void;
  max?: number;
  theme: ReturnType<typeof useTheme>["theme"];
}) {
  return (
    <View style={{ marginBottom: spacing.sm }}>
      <Text style={{ color: theme.text, marginBottom: spacing.xs }}>
        {label}: <Text style={{ fontWeight: "700" }}>{value}</Text>
      </Text>
      <View style={{ flexDirection: "row", gap: spacing.xs }}>
        {Array.from({ length: max }, (_, i) => i + 1).map((n) => (
          <Button
            key={n}
            label={String(n)}
            variant={value === n ? "primary" : "ghost"}
            onPress={() => onChange(n)}
          />
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: spacing.lg, paddingBottom: spacing.xxl },
  title: { fontSize: 26, fontWeight: "800", marginBottom: spacing.md },
});
