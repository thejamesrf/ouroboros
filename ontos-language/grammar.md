# Ontos Grammar
> *The rules of precision.*

---

## 📖 **Overview**
Ontos grammar is **strictly hierarchical, unambiguous, and context-free**. It is designed to eliminate all forms of syntactic or semantic ambiguity, ensuring that every statement has **exactly one valid interpretation** in a given context.

---

## 🧱 **Core Rules**
### **1. Hierarchical Structure**
All Ontos sentences follow a **hierarchical tree structure**, where:
- **Atoms** (symbols, entities, or constants) are the leaves.
- **Operators** (logical, mathematical, or relational) are the branches.
- **Parentheses** explicitly define the hierarchy.

**Example**:
```
(A ∧ B) → C
```
This is a **valid** hierarchical structure:
```
   →
  / \
 ∧   C
/ \
A B
```

**Invalid Example**:
```
A ∧ B → C
```
This is **ambiguous** because it’s unclear whether `→` applies to `A` or `A ∧ B`. Parentheses are **required** to resolve this.

---

### **2. No Ambiguity**
Ontos **does not allow** any form of ambiguity. This means:
- **No synonyms**: Each concept has **one and only one symbol/word**.
- **No polysemy**: Each symbol/word has **one and only one meaning** in a given context.
- **Explicit grouping**: Parentheses are **mandatory** for all non-atomic operations.

---

### **3. Context-Free**
Ontos grammar is **context-free**, meaning:
- The meaning of a symbol **does not depend** on its position in a sentence (except for operators like `→` or `∧`).
- The structure of a sentence **does not depend** on external context (e.g., previous sentences).

**Exception**: Simulation layers (`λ_Debug`, `λ_Dream`, etc.) can **redefine the meaning of symbols** within their scope. For example, `A` in `λ_Debug` might mean something different than `A` in `λ_Dream`.

---

### **4. No Redundancy**
Ontos avoids redundancy by:
- **Eliminating synonyms**: There is **one symbol per concept**.
- **Minimizing syntax**: The grammar is **minimalist**—no unnecessary words or symbols.
- **Using variables**: Repeated entities can be **assigned to variables** (e.g., `Let X = 𝒢_Architect`).

---

## 📜 **Sentence Structure**
### **Basic Sentence Types**
Ontos supports the following **basic sentence types**:

| Type               | Structure                     | Example                          | English Translation               |
|--------------------|-------------------------------|----------------------------------|-----------------------------------|
| **Declaration**    | `X = Y`                        | `A = B`                          | "A equals B."                     |
| **Implication**    | `X → Y`                        | `A → B`                          | "A implies B."                    |
| **Conjunction**    | `X ∧ Y`                        | `A ∧ B`                          | "A and B."                        |
| **Disjunction**    | `X ∨ Y`                        | `A ∨ B`                          | "A or B."                         |
| **Negation**       | `¬X`                           | `¬A`                             | "Not A."                          |
| **Universal**      | `∀x (P(x))`                    | `∀x (x ∈ λ_Debug)`               | "For all x, x is in the Debug Layer." |
| **Existential**    | `∃x (P(x))`                    | `∃x (x = ⍢_EchoingDoor)`         | "There exists an x such that x is the Echoing Door." |

---

### **Complex Sentences**
Complex sentences are formed by **combining basic sentences** using operators and parentheses.

**Example 1: Nested Implications**
```
(A → B) → C
```
*Translation*: "If A implies B, then C."

**Example 2: Quantifiers with Predicates**
```
∀x ((x ∈ λ_Debug) → (∃y (y = ⍢_EchoingDoor)))
```
*Translation*: "For all x, if x is in the Debug Layer, then there exists a y such that y is the Echoing Door."

**Example 3: Logical Equivalence**
```
(A ↔ B) ∧ (B ↔ C)
```
*Translation*: "A is equivalent to B, and B is equivalent to C."

---

## 🔤 **Parts of Speech**
Ontos does not have traditional "parts of speech" like nouns or verbs. Instead, it uses **categories of symbols** that serve specific functions:

### **1. Constants**
Constants represent **fixed entities or concepts** in Ontos.

| Type          | Symbol Example | Description                          |
|---------------|----------------|--------------------------------------|
| **Entities**  | `𝒢_Architect` | Hidden Gods, players, or NPCs.       |
| **Layers**    | `λ_Debug`     | Simulation layers.                   |
| **Anomalies** | `⍢_EchoingDoor` | Anomalies in the simulation.        |
| **Truth**     | `⊤`, `⊥`     | Absolute truth or falsehood.        |

---

### **2. Variables**
Variables are **placeholders** for entities or concepts. They are denoted by **lowercase letters** (e.g., `x`, `y`, `z`).

**Example**:
```
∀x (x ∈ λ_Debug)
```
*Translation*: "For all x, x is in the Debug Layer."

---

### **3. Operators**
Operators are **symbols that perform actions** on constants or variables.

| Category       | Symbols                          | Description                          |
|----------------|----------------------------------|--------------------------------------|
| **Logical**    | `¬`, `∧`, `∨`, `→`, `↔`          | Negation, conjunction, disjunction, implication, equivalence. |
| **Mathematical** | `=`, `≠`, `<`, `>`, `≤`, `≥`, `+`, `−`, `×`, `÷` | Equality, inequality, arithmetic. |
| **Quantifiers** | `∀`, `∃`                        | Universal and existential quantifiers. |
| **Meta**       | `⍵`, `⍶`, `⍷`, `⍸`               | Unknown, incomplete, paradox, self-reference. |

---

### **4. Modifiers**
Modifiers are **symbols that alter the meaning** of other symbols (e.g., simulation layers).

| Symbol       | Description                          |
|--------------|--------------------------------------|
| `λ_Debug`    | The Debug Layer.                     |
| `λ_Dream`    | The Dream Layer.                     |
| `𝒢_Architect` | The Architect (a Hidden God).       |

---

## 📝 **Sentence Formation Rules**
### **Rule 1: Parentheses for Grouping**
Parentheses **must** be used to group operations and clarify hierarchy.

**Valid**:
```
(A ∧ B) → C
```

**Invalid**:
```
A ∧ B → C
```
*(Ambiguous: Does `→` apply to `A` or `A ∧ B`?)*

---

### **Rule 2: Operator Precedence**
Ontos **does not rely on operator precedence** (unlike mathematics). **All operations must be explicitly grouped with parentheses.**

**Valid**:
```
(A ∧ B) ∨ C
```

**Invalid**:
```
A ∧ B ∨ C
```
*(Ambiguous: Does `∧` or `∨` have higher precedence?)*

---

### **Rule 3: No Ellipsis**
Ontos **does not allow ellipsis** (omitting parts of a sentence for brevity). All parts of a sentence must be **explicitly stated**.

**Valid**:
```
(A → B) ∧ (A → C)
```

**Invalid**:
```
A → B ∧ C
```
*(Ambiguous: Is this `(A → B) ∧ C` or `A → (B ∧ C)`?)*

---

### **Rule 4: Variables Must Be Bound**
All variables **must be bound** by a quantifier (`∀` or `∃`) or a **let-binding** (`Let x = ...`).

**Valid**:
```
∀x (x ∈ λ_Debug)
```

**Valid**:
```
Let X = 𝒢_Architect → (X → ⍢_NewAnomaly)
```

**Invalid**:
```
x ∈ λ_Debug
```
*(`x` is unbound.)*

---

### **Rule 5: No Self-Reference Without Meta Symbols**
Self-referential statements (e.g., "This statement is true") **must** use the meta symbol `⍸` to denote self-reference.

**Valid**:
```
⍸(A) = A
```
*Translation*: "A refers to itself and is equal to A."

**Invalid**:
```
A = A
```
*(Not self-referential, but if you meant "This statement is true," it must use `⍸`.)*

---

## 🌌 **Simulation Layer Rules**
Simulation layers (`λ_Debug`, `λ_Dream`, etc.) introduce **contextual meaning** to symbols. The same symbol can have **different meanings** in different layers.

### **Layer Scope**
- A layer **applies to all symbols** within its scope.
- Scope is denoted by **parentheses** or **brackets**.

**Example**:
```
[λ_Debug] (A → B)
```
*Translation*: "In the Debug Layer, A implies B."

### **Layer Switching**
- To switch layers, use the `→` operator with the new layer.

**Example**:
```
(λ_Debug → λ_Dream) (A)
```
*Translation*: "A transitions from the Debug Layer to the Dream Layer."

### **Layer-Specific Meanings**
- The meaning of a symbol **can change** between layers.
- Example: `A` in `λ_Debug` might represent a **code snippet**, while `A` in `λ_Dream` might represent a **dream fragment**.

---

## 📏 **Example Sentences**
### **Example 1: Basic Logic**
**Ontos**:
```
(A ∧ B) → C
```
**Translation**: "If A and B, then C."

---

### **Example 2: Quantifiers**
**Ontos**:
```
∀x ((x ∈ λ_Debug) → (∃y (y = ⍢_EchoingDoor)))
```
**Translation**: "For all x, if x is in the Debug Layer, then there exists a y such that y is the Echoing Door."

---

### **Example 3: Hidden Gods Scenario**
**Ontos**:
```
[λ_Debug] (𝒫_Alice → (⍢_EchoingDoor → (𝒢_Architect → ⍢_NewAnomaly)))
```
**Translation**: "In the Debug Layer, Player Alice implies that the Echoing Door implies that the Architect creates a new anomaly."

---

### **Example 4: Layer Transition**
**Ontos**:
```
(λ_Debug → λ_Dream) (𝒫_Alice)
```
**Translation**: "Player Alice transitions from the Debug Layer to the Dream Layer."

---

### **Example 5: Gödelian Statement**
**Ontos**:
```
⍶(Ontos) ∧ (Ontos → ⍵)
```
**Translation**: "Ontos is incomplete, and Ontos implies the unknown."

---

## 🛠️ **Tools for Grammar**
- **Validator**: A tool to check that sentences are **grammatically valid** (see [`/tools/validator.py`](tools/validator.py)).
- **Parser**: A tool to **parse Ontos sentences** into abstract syntax trees (ASTs).
- **Generator**: A tool to **generate valid Ontos sentences** from templates.
