# Contributing to The Ouroboros Project

> 🤝 *The Ouroboros Project thrives on collaboration. Whether you build layers, design languages, write lore, or code tools—there's a place for you here.*

---

## 🌍 **Our Voice**
We write in a **warm, communal, and human** voice—think Mr. Rogers, James Foster, or MLK Jr. We avoid corporate or AI-like phrasing. Be curious, be empathetic, and assume good intent.

A few conventions:
- **Emojis are welcome** (✨ magic, 🎲 mechanics, 🔍 exploration, 🟢 world-building, 🟣 introspection, 🔵 simulation).
- **Markdown** for structure: headers, tables, and lists over long prose.
- Keep paragraphs short. Break up lists of more than 5 items.
- **Creation as connection** matters more than mechanics. Aim for ~35% introspection and ~65% world-building.

---

## 🗂️ **Where to Contribute**

| Area | Location | What to add |
|------|----------|-------------|
| **Hidden Gods (TTRPG)** | [`hidden-gods/`](hidden-gods/) | Moves, playbooks, anomalies, lore in [`simulation_bible.md`](hidden-gods/simulation_bible.md) |
| **Ontos Language** | [`ontos-language/`](ontos-language/) | Symbols, grammar, examples, tools |
| **Aperios Language** | [`aperios/`](aperios/) | Paradoxes, fluid symbols, dream-layer examples |
| **Shared Tools** | [`src/`](src/) | Python tools (Anomaly Forge, simulation generator, CLI) |
| **Simulation Bible** | [`docs/`](docs/) | Shared world-building bible |
| **Roadmap** | [`ROADMAP.md`](ROADMAP.md) | Track progress and claim tasks |

---

## 🎲 **Adding Hidden Gods Content**
- **Moves**: Add to [`hidden-gods/moves/`](hidden-gods/moves/). Each move needs a stat (e.g., *Roll+Weird*), a 10+/7-9/6- outcome table, and a one-line flavor description.
- **Playbooks**: Add to [`hidden-gods/playbooks/`](hidden-gods/playbooks/). Include highlighted stats, playbook moves, and a "Look" section.
- **Anomalies**: Add to [`hidden-gods/examples/sample_anomalies.md`](hidden-gods/examples/sample_anomalies.md) or [`simulation_bible.md`](hidden-gods/simulation_bible.md). Each anomaly needs: **Manifestation**, **Clue**, **Purpose**, and **Risk**.
- **Lore**: Expand [`hidden-gods/simulation_bible.md`](hidden-gods/simulation_bible.md) with new layers, gods, or history.

## 🧠 **Adding Language Content (Ontos / Aperios)**
- **Ontos symbols**: Add to [`ontos-language/phonology.md`](ontos-language/phonology.md) and follow the symbol tables' format. Every symbol needs a name, meaning, and example.
- **Ontos grammar**: Extend [`ontos-language/grammar.md`](ontos-language/grammar.md) with new rules or sentence types.
- **Aperios**: Follow [`aperios/README.md`](aperios/README.md). Embrace paradox and fluid meaning.
- **Tools**: Python tools live in [`ontos-language/tools/`](ontos-language/tools/) and [`aperios/tools/`](aperios/tools/). Follow PEP 8 and add a module docstring.

## 🛠️ **Adding Code**
- Python tools go in [`src/`](src/) or the relevant language `tools/` directory.
- Follow **PEP 8**. Keep snippets readable and commented.
- Don't add dependencies unless the project already uses them.
- Test your code before submitting: `python3 -m py_compile <file>` at minimum.

---

## 📝 **How to Submit**
1. **Pick a task** from the [`ROADMAP.md`](ROADMAP.md) (look for unstarted `[ ]` items) or propose your own.
2. **Open an issue** to claim it and let others know you're working on it.
3. **Fork and branch**: `git checkout -b your-name/your-feature`.
4. **Make your changes**, keeping commits focused. Use [conventional commit messages](https://www.conventionalcommits.org/) where possible (e.g., `feat:`, `docs:`, `fix:`).
5. **Open a pull request** and describe what you added and why.
6. Be kind in review. We're building this together. 🌱

---

## ✅ **Style Checklist**
Before submitting, confirm your contribution:
- [ ] Matches the project's **warm, communal tone**.
- [ ] Uses **markdown** formatting (headers, tables, lists).
- [ ] **Links resolve** — check that any `[text](path)` links point to real files.
- [ ] Stays in scope — doesn't undo unrelated work.
- [ ] Includes a short commit message explaining the change.

---

## 🙏 **Code of Conduct**
Be excellent to each other. This is a space for **collaborative creation and introspection**. Disrespect, harassment, or exclusionary behavior are not welcome. We're all here because reality is a nested simulation and we want to build better layers together.

---

> *"The ouroboros eats its own tail. We build the layers that build us."*
