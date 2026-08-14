/** Metrics screen: TRIMP, HRV, sleep, fatigue trends, ACWR, heatmap. */
import React, { useMemo } from "react";
import { ScrollView, StyleSheet, Text, View } from "react-native";
import { Body, Button, Card, SectionTitle } from "../components/ui";
import { useTheme } from "../theme";
import { spacing, fatigueColor } from "../theme/tokens";
import { useAppStore } from "../state/store";
import { weeklyReview } from "../domain/metrics";
import { weekRange } from "../domain/metrics";
import { Fatigue } from "../domain/fatigue";
import { exportAll } from "../services/export";
import * as Sharing from "expo-sharing";

export default function Metrics() {
  const { theme } = useTheme();
  const checkins = useAppStore((s) => s.checkins);
  const logs = useAppStore((s) => s.workoutLogs);
  const journal = useAppStore((s) => s.journal);

  const summary = useMemo(() => {
    const { start, end } = weekRange(new Date());
    return weeklyReview({
      weekOf: new Date(),
      checkins,
      logs,
      priorWeeksTrimp: [],
      hrvTrendDown: false,
    });
    void start;
    void end;
  }, [checkins, logs]);

  const onExport = async () => {
    try {
      const csv = exportAll(checkins, logs, journal);
      // In a full build, write to FileSystem cache and share. For now, log length.
      void csv;
      if (await Sharing.isAvailableAsync()) {
        // Sharing.shareAsync(uri) would go here with a cached file.
      }
    } catch {
      // ignore
    }
  };

  return (
    <ScrollView contentContainerStyle={[styles.container, { backgroundColor: theme.bg }]}>
      <Text style={[styles.title, { color: theme.text }]}>Metrics 📊</Text>

      <Card>
        <SectionTitle>This week</SectionTitle>
        <Stat label="Total TRIMP" value={String(summary.totalTrimp)} hint={summary.trimpStatus} />
        <Stat label="Avg HRV" value={`${summary.avgHrv.toFixed(0)} ms`} />
        <Stat label="Avg sleep" value={`${summary.avgSleep.toFixed(1)} h`} />
        <Stat
          label="Avg fatigue"
          value={`${summary.avgFatiguePercent.toFixed(1)}%`}
          color={fatigueColor[summary.fatigueCue]}
        />
        <Stat label="Red days" value={String(summary.redDays)} />
        {summary.acwr != null && <Stat label="ACWR" value={summary.acwr.toFixed(2)} />}
        <View style={{ marginTop: spacing.md }}>
          <Body muted>{summary.suggestion}</Body>
        </View>
      </Card>

      <Card>
        <SectionTitle>Fatigue heatmap (recent days)</SectionTitle>
        <Heatmap cues={checkins.slice(-14).map((c) => c.cue)} theme={theme} />
      </Card>

      <Button label="Export data (CSV)" onPress={onExport} variant="ghost" />
    </ScrollView>
  );
}

function Stat({ label, value, hint, color }: { label: string; value: string; hint?: string; color?: string }) {
  const { theme } = useTheme();
  return (
    <View style={{ flexDirection: "row", justifyContent: "space-between", paddingVertical: spacing.xs }}>
      <Text style={{ color: theme.muted }}>{label}</Text>
      <View style={{ alignItems: "flex-end" }}>
        <Text style={{ color: color ?? theme.text, fontWeight: "700" }}>{value}</Text>
        {hint ? <Text style={{ color: theme.muted, fontSize: 12 }}>{hint}</Text> : null}
      </View>
    </View>
  );
}

function Heatmap({ cues, theme }: { cues: Fatigue[]; theme: ReturnType<typeof useTheme>["theme"] }) {
  if (cues.length === 0) {
    return <Body muted>No check-ins yet this period.</Body>;
  }
  return (
    <View style={{ flexDirection: "row", flexWrap: "wrap", gap: spacing.xs }}>
      {cues.map((c, i) => (
        <View
          key={i}
          style={{
            width: 28,
            height: 28,
            borderRadius: 8,
            backgroundColor: fatigueColor[c],
            opacity: 0.5 + 0.5 * ((i + 1) / cues.length),
          }}
        />
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: spacing.lg, paddingBottom: spacing.xxl },
  title: { fontSize: 26, fontWeight: "800", marginBottom: spacing.md },
});
