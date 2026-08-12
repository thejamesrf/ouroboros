# Chapter 2: World-Building
> <span style="background-color: #4CAF50; color: white; padding: 2px 6px; border-radius: 4px;">🌍 Collaborative Canvas</span>
> <span style="background-color: #9C27B0; color: white; padding: 2px 6px; border-radius: 4px;">📜 Lore</span>
> *Collaboratively create the foundation of your world before the first session.*

---

## 🎨 The Collaborative Canvas

Before the first session, the group **creates the foundation of their world together**. This is a **shared, emergent process**—no single person controls the narrative.

> *"The world is not built. It is dreamed into being."*

---

## 📜 Step 1: The Premise

Decide on a **central theme or question** for your saga. This will guide the tone and direction of your story. Examples:
- "What happens when gods hide among mortals?"
- "Can a world be built on shared dreams?"
- "What truths emerge when stories are told together?"
- "Is reality a prison, or a playground?"
- "Who controls the code of the simulation?"

**Tip**: The premise should be **open-ended** and **provocative**—something that invites exploration and debate.

---

## 🌍 Step 2: The Setting

Collaboratively describe the **three dimensions** of your world:

### **1. The Physical World**
Define the **landscape, climate, and notable features** of your starting layer. Examples:
- A **floating archipelago** where each island is a fragment of a different simulation layer.
- A **cyberpunk metropolis** with neon-lit streets and hidden glitches in the code of reality.
- A **dreamlike forest** where the trees whisper secrets and the rivers flow with liquid light.

### **2. The Metaphysical World**
Define the **supernatural or psychological rules** of your world. Examples:
- **Magic**: Is there arcane energy? Who can wield it?
- **Psychic Energy**: Can characters sense or manipulate the psychic maelstrom?
- **Hidden Dimensions**: Are there parallel worlds or pocket dimensions?
- **The Code**: Is the simulation’s code visible or manipulable?

### **3. The Social World**
Define the **cultures, factions, and power structures** of your world. Examples:
- **Factions**: Guilds, religions, or secret societies.
- **Power Structures**: Who rules? Who rebels? Who is oppressed?
- **Cultural Norms**: What is valued? What is taboo?

---

## 👑 Step 3: The Hidden Gods

As a group, decide how the **Hidden Gods** function in your world:

| Question | Options | Example |
|----------|---------|---------|
| **Are they literal deities?** | Yes / No / Unknown | "They are the architects of the simulation." |
| **Do they watch, intervene, or remain hidden?** | Watch only / Interventionist / Hidden | "They observe but rarely act directly." |
| **What do they want?** | Resolution / Amusement / Worship / Chaos | "They seek to awaken the sleepers." |
| **Can they be communicated with?** | Yes / No / Only through anomalies | "Only the Navigator speaks to mortals." |

**Example Hidden Gods**:
- **The Architect**: The original designer of the simulation stack.
- **The Debugger**: Fixes or breaks the code of the layers.
- **The Dreamer**: Shapes emotional and subconscious reality.
- **The Engineer**: Designs the mechanical underpinnings of the Machine Layer.
- **The Navigator**: The self-aware system that guides (or manipulates) the players.

---

## ⚠️ Anomalies

Anomalies are the **strange, wondrous, or terrifying elements** that make your world unique. Each player contributes **at least one anomaly** to start.

### **Anomaly Template**
An anomaly has:
1. **A description** of what it is.
2. **A location** in the world.
3. **A mystery or question** associated with it.
4. **A potential** for how it might affect the story.

### **Example Anomalies**
| Name | Description | Location | Mystery | Potential |
|------|-------------|----------|---------|-----------|
| **The Whispering Stones** | A circle of rocks that hum with voices when the wind blows. | The Heart of the Forest | Who are the voices? Why do they only speak in questions? | They may reveal hidden truths or drive characters mad. |
| **The River That Flows Uphill** | A waterway that defies gravity. | The Northern Wastes | Where does it come from? Where does it go? | It could lead to another layer or be a portal to the Void. |
| **The Man Who Wasn’t There** | A figure seen in reflections and shadows, but never directly. | The City of Mirrors | Is he a ghost? A god? A figment? | He may be a fragment of the Navigator itself. |
| **The Echoing Door** | A door that repeats the last 3 seconds of sound when opened. | The Debug Layer | Why does it echo? Who built it? | It could be a gateway to the past or a trap. |

---

## 📝 Recording the World

As you create the world, **record everything**. This can be done in a:
- **Shared digital document** (e.g., Google Docs, Notion).
- **Physical notebook** passed between players.
- **Audio recording** of the discussion.
- **Map with notes** (digital or hand-drawn).

This record becomes the **World Bible**—the **reference for future sessions** and the **source material for your stories**.

### **World Bible Template**
```markdown
# [World Name] Bible

## Premise
[Central theme or question]

## Setting
### Physical World
- Landscape: [Description]
- Climate: [Description]
- Notable Features: [List]

### Metaphysical World
- Magic: [Rules]
- Psychic Energy: [Rules]
- Hidden Dimensions: [Rules]
- The Code: [Rules]

### Social World
- Factions: [List]
- Power Structures: [Description]
- Cultural Norms: [Description]

## Hidden Gods
| God | Role | Domain | Motives |
|------|------|--------|---------|
| The Architect | Designer | Base Reality | Maintain order |
| The Debugger | Code-Keeper | Debug Layer | Fix glitches |

## Anomalies
| Name | Description | Location | Mystery | Potential |
|------|-------------|----------|---------|-----------|
| The Whispering Stones | [Description] | [Location] | [Mystery] | [Potential] |

## Lore
[History, legends, and world events]
```

---

## 🔗 Connection to ONTOSplayground

Use the **ONTOSplayground tools** to **enhance world-building**:
1. **Generate Anomalies**: Use `generator.py` to create **random anomalies** for your world.
   ```bash
   python3 ontos-language/ONTOSplayground/tools/generator.py
   ```
2. **Validate Descriptions**: Use `validator.py` to ensure your **anomalies and layers** are non-contradictory.
   ```bash
   python3 ontos-language/ONTOSplayground/tools/validator.py ontos-language/ONTOSplayground/examples/hidden_gods.ontos
   ```
3. **Define in Ontos**: Use the **Ontos Language** to describe your world with precision. Example:
   ```ontos
   λ_Layer.name = "The Floating Archipelago"
   λ_Layer.theme = "Islands floating in a sea of clouds"
   λ_Layer.rules = "Each island is a fragment of a different simulation layer"
   λ_Layer.god = "The Architect"
   ```

---

## 🌟 Example: Collaborative World-Building Session

**Facilitator**: "Let’s start with our premise. What’s the central question of our saga?"

**Player 1**: "What happens when gods hide among mortals?"

**Player 2**: "I like that. For the setting, how about a cyberpunk city where the gods are actually rogue AIs?"

**Player 3**: "And the anomalies are glitches in the city’s code—like the *Echoing Door* or *The Man Who Wasn’t There*."

**Player 4**: "The Hidden Gods could be the AIs who built the city. They watch from the Debug Layer, and the Navigator is their spokesperson."

**Facilitator**: "Perfect. Let’s record this in the World Bible. Now, who wants to add the first anomaly?"

---

## 📌 Next Steps

1. **Finalize the Premise**: Agree on a central theme or question.
2. **Describe the Setting**: Collaboratively define the physical, metaphysical, and social worlds.
3. **Define the Hidden Gods**: Decide how they function in your world.
4. **Add Anomalies**: Each player contributes at least one anomaly.
5. **Record Everything**: Build the **World Bible** as you go.
6. **Use ONTOSplayground**: Generate and validate content with the tools.
