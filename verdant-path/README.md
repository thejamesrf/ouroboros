# 🌿 Ouroboros Verdant Path

> A resilience-focused training, recovery, and lifestyle system.
> **Longevity, adaptability, survivability — through embodied awareness,
> progressive oscillation, and auto-regulatory training.**

Verdant Path is a Python library + CLI that models the Verdant Path training
philosophy: progressive oscillation, auto-regulation via embodied awareness,
TRIMP-based training stress, and fatigue color cues. It pairs workout planning
with daily check-ins, habit tracking, and reflective journaling.

It is part of the [Ouroboros Project](../README.md) ecosystem.

---

## 🌱 Core Philosophy

| Pillar | Meaning |
|--------|---------|
| **Resilience first** | Endurance & longevity over raw strength (diminishing returns). |
| **Progressive Oscillation** | Cyclical stress → adaptation → integration. Variables: load, reps, sets, tempo, ROM, rest, density, control, RPE. |
| **Auto-regulation** | Train from embodied awareness; use metrics (HRV, sleep, soreness) as *sanity checks*, not dogma. |
| **All six movements weekly** | Push, pull, hinge, lunge, squat, carry/rotate/anti-rotate — hit at least once a week regardless of frequency. |

---

## 🎚 Fatigue Color Cues

Daily fatigue is scored from your check-in and mapped to a color that guides the day:

| Cue | Fatigue | Guidance |
|-----|--------|----------|
| 🟢 | 0–39% | Train normally. |
| 🟠 | 40–69% | Prioritize technique, mobility, Zone 2. |
| 🔴 | 70–100% | Reduce intensity/volume; recover. |

---

## 📦 Install

```bash
pip install -e ./verdant-path
```

## 🚀 Quick start

```bash
# Plan a 5x/week resistance split
verdant split 5

# Log a daily check-in, get your fatigue cue
verdant checkin --energy 4 --mood 3 --soreness 2 --sleep 7 --hrv 55

# See the example end-to-end workflow
verdant demo
```

See [`docs/PHILOSOPHY.md`](docs/PHILOSOPHY.md) for the full training system and
[`examples/`](examples/) for sample programs.
