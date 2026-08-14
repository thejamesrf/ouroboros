/** Shared UI primitives: cards, buttons, fatigue badge, progress bar. */
import React from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";
import { useTheme } from "../theme";
import { radius, spacing, fatigueColor } from "../theme/tokens";
import { Fatigue, FATIGUE_ICON, FATIGUE_GUIDANCE } from "../domain/fatigue";

export function Card({ children, style }: { children: React.ReactNode; style?: any }) {
  const { theme } = useTheme();
  return <View style={[styles.card, { backgroundColor: theme.surface, borderColor: theme.border }, style]}>{children}</View>;
}

export function SectionTitle({ children }: { children: React.ReactNode }) {
  const { theme } = useTheme();
  return <Text style={[styles.sectionTitle, { color: theme.text }]}>{children}</Text>;
}

export function Body({ children, muted, style }: { children: React.ReactNode; muted?: boolean; style?: any }) {
  const { theme } = useTheme();
  return <Text style={[styles.body, { color: muted ? theme.muted : theme.text }, style]}>{children}</Text>;
}

export function Button({
  label,
  onPress,
  variant = "primary",
  disabled,
}: {
  label: string;
  onPress: () => void;
  variant?: "primary" | "ghost";
  disabled?: boolean;
}) {
  const { theme } = useTheme();
  const isPrimary = variant === "primary";
  return (
    <Pressable
      onPress={onPress}
      disabled={disabled}
      style={[
        styles.button,
        {
          backgroundColor: isPrimary ? theme.primary : "transparent",
          borderColor: isPrimary ? theme.primary : theme.border,
          opacity: disabled ? 0.5 : 1,
        },
      ]}
    >
      <Text style={{ color: isPrimary ? "#FFFFFF" : theme.text, fontWeight: "600", textAlign: "center" }}>{label}</Text>
    </Pressable>
  );
}

export function FatigueBadge({ fatigue }: { fatigue: Fatigue }) {
  const { theme } = useTheme();
  return (
    <View style={[styles.badge, { backgroundColor: fatigueColor[fatigue] }]}>
      <Text style={styles.badgeText}>
        {FATIGUE_ICON[fatigue]} {fatigue} · {FATIGUE_GUIDANCE[fatigue]}
      </Text>
    </View>
  );
}

export function ProgressBar({ percent, color }: { percent: number; color?: string }) {
  const { theme } = useTheme();
  return (
    <View style={[styles.progressTrack, { backgroundColor: theme.border }]}>
      <View
        style={{
          width: `${Math.max(0, Math.min(100, percent))}%`,
          height: "100%",
          backgroundColor: color ?? theme.accent,
          borderRadius: radius.pill,
        }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    borderRadius: radius.lg,
    borderWidth: 1,
    padding: spacing.lg,
    marginBottom: spacing.md,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: "700",
    marginBottom: spacing.sm,
  },
  body: {
    fontSize: 15,
    lineHeight: 21,
  },
  button: {
    borderWidth: 1,
    borderRadius: radius.pill,
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.xl,
  },
  badge: {
    borderRadius: radius.pill,
    paddingVertical: spacing.sm,
    paddingHorizontal: spacing.md,
    alignSelf: "flex-start",
  },
  badgeText: {
    color: "#FFFFFF",
    fontWeight: "700",
    fontSize: 13,
  },
  progressTrack: {
    height: 8,
    borderRadius: radius.pill,
    overflow: "hidden",
    marginVertical: spacing.xs,
  },
});
