# ONTOSplayground
> <span style="background-color: #2196F3; color: white; padding: 2px 6px; border-radius: 4px;">🔢 Logic</span>
> <span style="background-color: #FF9800; color: white; padding: 2px 6px; border-radius: 4px;">⚖️ Precision</span>
> *A sandbox for developing Ontos as a programming and communication language for AIs.*

---

## 🎯 **Purpose**
**ONTOSplayground** is a **practical workspace** for experimenting with **Ontos Language** in the context of **AI communication and programming**. It focuses on:
- **Specificity**: Eliminating vagueness in language to ensure unambiguous communication.
- **Legalistic Syntax**: Designing rules that enforce clarity and avoid misinterpretation.
- **Non-Contradiction**: Avoiding paradoxes (e.g., the liar's paradox) to maintain logical consistency.
- **Gödelian Awareness**: Acknowledging incompleteness while striving for **maximal completeness** within the constraints of non-contradiction.

> *"Ontos is the language of the Architect. ONTOSplayground is where we build the tools to speak it."*

---

## 🔗 **Connection to Ontos Language**
This playground **extends** the [Ontos Language](../README.md) project by:
- Focusing on **AI-specific use cases** (e.g., machine-readable syntax for communication between AIs or with humans).
- Experimenting with **programming-like structures** (e.g., conditionals, loops, variables) in Ontos.
- Validating **non-contradictory logic** in real-world scenarios (e.g., Hidden Gods anomalies, simulation rules).
- Prototyping **tools** (e.g., validators, translators) before integrating them into the main [`/tools`](../tools/) directory.

---

## 🛠️ **Structure**
```
ONTOSplayground/
├── README.md          # This file
├── examples/         # Example Ontos statements for AIs and Hidden Gods
│   ├── ai_communication.ontos  # Ontos statements for AI interactions
│   └── hidden_gods.ontos       # Ontos descriptions of layers, gods, and anomalies
├── tools/            # Prototypes for Ontos tools
│   ├── validator.py   # Checks Ontos statements for contradictions
│   └── generator.py   # Generates Ontos statements for Hidden Gods content
└── tests/            # Test cases for Ontos logic
    ├── test_validator.py
    └── test_grammar.py
```

---

## 📌 **Example: Ontos for AI Communication**
Ontos is designed to be **unambiguous and non-contradictory**, making it ideal for AI communication. Below are examples of how Ontos can be used in different contexts.

### **1. Basic Statements**
```ontos
-- Non-contradictory statement
λ_Agent.act(open_door) → λ_Door.state = "open"

-- Legalistic condition (no vagueness)
IF λ_Sensor.detect("intruder") THEN λ_Alarm.trigger() ELSE λ_Alarm.silence()
```

### **2. Avoiding Paradoxes**
Ontos **explicitly avoids** self-referential paradoxes like the liar's paradox:
```ontos
-- Valid: Self-referential but non-contradictory
λ_Statement.value = "This statement is true"

-- INVALID: Paradox (would cause a contradiction)
λ_Statement.value = "This statement is false"
```

### **3. Ontos for Hidden Gods**
Ontos can describe **simulation layers, gods, and anomalies** with precision:
```ontos
-- Defining a simulation layer
λ_Layer.name = "Debug"
λ_Layer.theme = "Glitchy, monochrome, floating symbols"
λ_Layer.rules = "Code is visible as geometry; time is non-linear"
λ_Layer.god = "The Debugger"

-- Defining an anomaly
λ_Anomaly.name = "The Echoing Door"
λ_Anomaly.manifestation = "A door that repeats the last 3 seconds of sound when opened"
λ_Anomaly.clue = "The air smells like ozone"
λ_Anomaly.purpose = "To test the party’s perception of time"
λ_Anomaly.risk = "Roll+Weird to resist disorientation (2-Weird)"
```

---

## 🧪 **Tools in Development**
The `tools/` directory contains prototypes for working with Ontos:

| Tool | Purpose | Status |
|------|---------|--------|
| `validator.py` | Checks Ontos statements for **contradictions or invalid syntax**. | 🟡 Planned |
| `generator.py` | Generates **random Ontos statements** for anomalies, layers, or gods. | 🟡 Planned |
| `translator.py` | Converts **Ontos to English** (and vice versa). | 🟡 Planned |

---

## 📝 **Grammar Rules (Experimental)**
This section outlines **experimental grammar rules** for Ontos in the context of AI communication. These rules are designed to:
1. **Eliminate ambiguity** (every term has a single, precise meaning).
2. **Avoid contradiction** (no statement can be both true and false in the same context).
3. **Enforce specificity** (vagueness is not allowed).

### **1. Syntax Basics**
- **Variables**: Prefixed with `λ_` (e.g., `λ_Agent`, `λ_Door`).
- **Statements**: End with a newline or semicolon (`;`).
- **Comments**: Start with `--`.
- **Implications**: Use `→` for logical implication (e.g., `A → B`).
- **Equivalence**: Use `≡` for logical equivalence (e.g., `A ≡ B`).

### **2. Non-Contradiction Rule**
A statement **cannot** imply its own negation. For example:
```ontos
-- INVALID: Contradiction
λ_Statement.value = "This statement is false"

-- VALID: Non-contradictory
λ_Statement.value = "This statement is true"
```

### **3. Specificity Rule**
Every term must be **unambiguously defined** in the current context. For example:
```ontos
-- INVALID: Vague
λ_Door.state = "openish"

-- VALID: Specific
λ_Door.state = "open"
```

### **4. No Raw Self-Reference**
Ontos **avoids raw self-reference** to prevent paradoxes. However, **marked self-reference** (e.g., using a special symbol like `⟪` and `⟫`) is allowed for advanced use cases:
```ontos
-- VALID: Marked self-reference
λ_Statement.value = "This statement ⟪λ_Statement.value⟫ is true"
```

---

## 🚀 **Getting Started**
1. **Explore the examples**: Check out the [`/examples`](examples/) directory for sample Ontos statements.
2. **Experiment with tools**: Use the prototypes in [`/tools`](tools/) to validate or generate Ontos statements.
3. **Test your logic**: Add test cases in [`/tests`](tests/) to ensure your Ontos statements are non-contradictory.
4. **Contribute**: Add new examples, tools, or grammar rules to help develop Ontos further.

---

## 📚 **Related Projects**
- **[Ontos Language](../README.md)**: The core philosophy, grammar, and phonology of Ontos.
- **[Hidden Gods](../../hidden-gods/README.md)**: The PbtA TTRPG where Ontos is used to describe simulation layers and anomalies.
- **[Aperios](../../aperios/README.md)**: The right-brain counterpart to Ontos, embracing paradox and ambiguity.
