/**
 * Verdant Path design system.
 *
 * Clean, minimalist, nature-inspired: earth tones and organic shapes. The palette
 * is rooted in forest, moss, clay, and stone, with the three fatigue colors as
 * semantic accents. A high-contrast variant supports accessibility.
 */

import { Fatigue } from "../domain/fatigue";

export const palette = {
  // Earth tones
  forest: "#2E4A3F",
  moss: "#5B7361",
  sage: "#8DA590",
  clay: "#B07A5B",
  stone: "#E8E2D5",
  cream: "#F7F4ED",
  bark: "#3A2E26",
  // Semantic / fatigue
  green: "#3FA34D",
  amber: "#E0A030",
  red: "#C0504A",
  // Neutrals
  ink: "#1F2A24",
  muted: "#6B7B72",
  white: "#FFFFFF",
};

export type Theme = {
  bg: string;
  surface: string;
  text: string;
  muted: string;
  primary: string;
  accent: string;
  border: string;
  highContrast: boolean;
};

export const lightTheme: Theme = {
  bg: palette.cream,
  surface: palette.white,
  text: palette.ink,
  muted: palette.muted,
  primary: palette.forest,
  accent: palette.moss,
  border: palette.stone,
  highContrast: false,
};

export const highContrastTheme: Theme = {
  bg: "#000000",
  surface: "#0E0E0E",
  text: "#FFFFFF",
  muted: "#D8D8D8",
  primary: "#9FE0AB",
  accent: "#FFD166",
  border: "#3A3A3A",
  highContrast: true,
};

export const fatigueColor: Record<Fatigue, string> = {
  [Fatigue.Green]: palette.green,
  [Fatigue.Amber]: palette.amber,
  [Fatigue.Red]: palette.red,
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  xxl: 32,
} as const;

export const radius = {
  sm: 8,
  md: 14,
  lg: 20,
  pill: 999,
} as const;
