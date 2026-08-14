# 🜲 Hidden Gods Simulation Bible
> <span style="background-color: #4CAF50; color: white; padding: 2px 6px; border-radius: 4px;">🟢 World-Building</span>
> The shared world-building bible for nested layers, gods, and anomalies.

This is the canonical lore reference for **Hidden Gods**. It is the living
counterpart to the runnable tools in the [`ouroboros`](../src) package — every
layer, god, and anomaly here has a matching data structure in
`ouroboros.anomalies`.

---

## 🜲 Core Layers

| Layer | Theme | God | Rules |
|-------|-------|-----|-------|
| **Base Reality** | "Normal" life | The Architect | Standard physics, but with subtle glitches. |
| **Debug** | Glitchy, monochrome | The Debugger | Code is visible as geometry; time is non-linear. |
| **Dream** | Surreal, emotional | The Dreamer | Rules are fluid; emotions shape reality. |
| **Machine** | Mechanical, cold | The Engineer | Everything is a machine; free will is an illusion. |

> *"The deeper you go, the more the rules relax — and the more the gods notice."*

---

## 🜲 The Hidden Gods

Hidden Gods are the architects, admins, and players of higher layers. They are
not omnipotent — they are *privileged users* of the simulation, each with their
own agenda.

- **The Architect** — maintains Base Reality; values stability above all.
- **The Debugger** — hunts anomalies in the Debug layer; treats players as test cases.
- **The Dreamer** — shapes the Dream layer through emotion; paradox is their mother tongue.
- **The Engineer** — runs the Machine layer; believes everything is (and should be) a process.

---

## 🜲 Anomalies

Anomalies are the simulation's glitches, clues, and disruptions. Each carries:
a **manifestation** (what players perceive), a **clue** (the sensory hint), a
**purpose** (why it exists), and a **risk** (what it costs to engage).

Forge your own with the Anomaly Forge:

```bash
ouroboros anomaly --layer Debug -n 3 --seed 7
```

### Canonical anomaly (reference)

```markdown
🔍 **Anomaly: The Echoing Door**
- **Layer**: Debug
- **Manifestation**: A door that repeats the last 3 seconds of sound when opened.
- **Clue**: "The air smells like ozone."
- **Purpose**: To test the party's perception of time.
- **Risk**: Roll+Weird to resist disorientation (2d6+Weird).
```

---

## 🜲 Ontos in the World

The simulation's deeper logic is written in **Ontos** — a precision language
where every statement has exactly one meaning. Validate or translate one:

```bash
ouroboros validate "[λ_Debug] (𝒫_Alice → (⚡_EchoingDoor → (𝒢_Architect → ⚡_NewAnomaly)))"
ouroboros translate "[λ_Debug] (𝒫_Alice → (⚡_EchoingDoor → (𝒢_Architect → ⚡_NewAnomaly)))"
```

> *"The pattern awaits its weaving…"*
