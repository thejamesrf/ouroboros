# 📱 Verdant Path — Mobile App

> The mobile (iOS/Android/Web) app for **Ouroboros Verdant Path** — a
> resilience-focused training, recovery, and lifestyle system.

Built with **Expo + React Native + TypeScript**. Offline-first (SQLite), with a
full TypeScript port of the [core domain logic](../src/verdant_path/) so the app
runs fully native without shelling out to Python.

Part of the [Ouroboros Project](../../README.md) ecosystem.

---

## 🌱 Architecture

| Layer | Path | Responsibility |
|-------|------|----------------|
| **Domain** | `src/domain/` | Pure TypeScript port of the training logic (movements, TRIMP, fatigue, planner, metrics, habits, roles). No UI deps. |
| **Storage** | `src/storage/` | Offline-first SQLite repositories (with an in-memory fallback for web/tests). |
| **State** | `src/state/` | Zustand store: profile, recent records, derived cues. |
| **Services** | `src/services/` | Notifications, wearable adapters (Apple Health / Oura / Garmin stubs), CSV export. |
| **Theme** | `src/theme/` | Earth-tone design system with a high-contrast accessibility variant. |
| **Screens** | `src/screens/` | Today, Planner, Metrics, Journal, Community + Onboarding. |
| **App** | `src/app/` | Expo Router tab layout. |

## 🚀 Getting started

```bash
cd verdant-path/mobile
npm install
npm start          # Expo dev server (press i / a / w for iOS/Android/Web)
```

## 🧪 Tests

```bash
npm test           # Jest (domain logic — verifies parity with the Python core)
npm run typecheck  # tsc --noEmit
```

## 📱 Bottom tabs (spec §9)

- **Today** — daily check-in → fatigue cue 🟢/🟠/🔴 + readiness adjustment + workout of the day
- **Planner** — splits (1x–6x), session structure, template library, trainer tools
- **Metrics** — TRIMP, HRV, sleep, fatigue trends, ACWR, heatmap, CSV export
- **Journal** — free-form notes, tags, photo + voice-to-text
- **Community** — group challenges, shared templates, forum

## 🔌 Wearables (spec §8)

`src/services/wearables.ts` defines a common `WearableAdapter` interface with
stubs for Apple Health, Oura, and Garmin. Wire up the native modules per-platform
when ready; the UI is provider-agnostic.

## 🔔 Notifications (spec §6)

Daily (morning/evening routines + workouts), weekly (summary + adaptive
suggestions), and adaptive (red-fatigue-3-days → deload alert) via
`expo-notifications`.

## ♿ Accessibility

High-contrast theme toggle in the header. Voice-to-text and photo journaling
buttons are wired into the Journal screen.

## 📦 Scope

This is the **full-spec** mobile build: roles (member/trainer), notifications,
wearable architecture, community, dashboards, and the complete onboarding quiz.
Persistence is offline-first (local SQLite); cloud sync / member-trainer sync is
the next phase.
