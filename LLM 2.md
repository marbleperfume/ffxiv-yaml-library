Here is your converted markdown:

---

# LLM.md — Unified RPG Design Hub / YAML Library

## Project Overview

This project is a suite of standalone Python desktop tools that generate and edit YAML "spec" files for a UE5 RPG (FFXIV-inspired). There is no game engine code here — this is the **design/data authoring layer**. Each tool is a form-based editor that writes structured YAML into a category folder (`NPCs/`, `Items/`, `Skills/`, etc.), which is later consumed by the UE5 project as GameplayTag-driven data assets.

- Most tools: Tkinter (`*.pyw`), one entry point (`Hub_Master.pyw`): PyQt6
- Output: YAML files, organized by category folder, meant to be human- and LLM-readable design docs as much as engine input
- `Project_Validator.py`: cross-reference integrity checker (Race/Class/Item references actually exist)

---

## Directory / Category Layout

Each category has its own folder, created on first save if missing:

`NPCs/`, `NPCs/Hostile/`, `NPCs/Bosses/`, `Items/`, `Attire/`, `Skills/`, `Conditions/`, `Passives/`, `Loot/`, `Summons/`, `Titles/`, `Quests/`, `Races/`, `Classes/`, `Tutorials/`, `tags/`, `Attributes/`

`Hub_Master.pyw` treats the whole tree as one project (`PROJECT_DIR`) and scans it recursively for `.yaml`/`.yml` files to build a live tag/key registry and an exported `Project_Relationships.json` for external/LLM context.

---

## Key Conventions

### File Naming
Hand-authored "template" YAML files use dot-namespaced keys as the literal filename (e.g. `Skill.Combat.AeroSlash.yaml`, `NPC.Enemy.Swarm.BeeCloud.yaml`). Tool-generated files instead take whatever the user typed in the Name field and do `name.replace(' ', '_')` for the filename. **Both conventions currently coexist** — see Known Issues below.

### Tags
A shared `tags/tag_library.txt` (one tag per line) backs an "Add Tag" + "Tag List" picker modal (`TagSelectorModal`) that is imported via `tag_library.py` into `Item Registry Creator.pyw`, `ConditionCreator.pyw`, and `AttireCreator.pyw`. Treat these three as the same logical component.

### Attributes
Single source of truth is `Attributes/attributes.json` (schema: name → default + intent) plus `Attributes/Base_Attributes.yaml` (actual starting values under `Base_Character.Attributes`). Loaded via `attr_loader.get_full_attribute_data(caller_file)`, which resolves paths relative to the calling script's own directory + `/Attributes`.

### Three Design Pillars
Three design pillars appear repeatedly in NPC/Passive/Boss/Summon schemas — always in this order:

- **Adventurer** — loot/progression
- **Mercenary** — counter-play, commitment level, interrupt windows
- **Strategy** — tactics/formation/AI behavior

Any new combat-facing content type should expose these three in the same order.

### Rank Scaling Pattern
Enemy NPC YAML uses a nested `RankScaling` block with `AdventurerLoot` (a reference to a global loot curve), `MercenaryReaction.Rank1/Rank2` (condition/action/cast-time), and `StrategyAI` (aggro/leash/terrain profile). Follow this shape for new hostile NPCs rather than inventing a new structure.

---

## Known Issues / Inconsistencies

> Fix opportunistically — do not assume intentional.

### Resolved

| Issue | Resolution |
|---|---|
| `PassiveCreator.pyw::save_yaml` referenced undefined `name` and `cleanse_req` | Now uses `self.name_entry.get()` / `self.cleanse_req.get()` |
| `DutySupportCreator.pyw` missing `ttk` import and launcher | Added `from tkinter import ttk`, `if __name__ == "__main__"` block, and `Tutorials/` folder creation on save |
| `Hub_Master.pyw::export_project_relationships` called `QFileDialog` without importing it | Added to `PyQt6.QtWidgets` import |
| `QuestPipelineViewer.pyw` read nested `Metadata` fields that `QuestCreator.pyw` saves flat | Viewer now reads flat fields (`PipelineID`, `SequenceIndex`, `NarrativeIntent`) |
| `PROJECT_DIR` in `Hub_Master.pyw` hardcoded author's absolute path | Now resolved via `os.path.dirname(os.path.abspath(__file__))` |
| `NPC.Enemy.Drakol.Lower.yaml` `Key` field didn't match filename | `Key` updated to `NPC.Enemy.Drakol.Lower` |
| Tag-library helper and `TagSelectorModal` duplicated verbatim in three tools | Extracted into shared `tag_library.py`, imported by all three tools |

### Still Open

| Issue | Status |
|---|---|
| File naming inconsistency — `NPC Hostile Creator.pyw`, `Item Registry Creator.pyw`, `Skill Creator.pyw`, `Title Registry Creator.pyw` have spaces; most other tools don't | Nothing references these filenames programmatically (grepped — clean), but renaming may break desktop shortcuts/muscle memory. **Ask before renaming.** |

---

## Gap Analysis

### Layer 1: Authoring — Per-Category YAML Creators
`✅ Mostly built`

### Layer 2: Shared State — Cross-Tool
`⚠️ Partially built`

| Component | Status |
|---|---|
| `tag_library.py` | ✅ Fixed |
| `attr_loader.py` | ✅ Exists |
| `Project_Validator.py` | ✅ Exists |
| `Project_Relationships.json` | ✅ Exists |
| Shared enum/constant definitions | ❌ Missing |
| Schema enforcement module | ❌ Missing |

### Layer 3: Validation — Integrity
`⚠️ Partially built`

| Component | Status |
|---|---|
| Reference integrity (Race/Class/Item) | ✅ Exists |
| Circular quest dependency checks | ⚠️ Partial |
| Skill prerequisite chain validation | ❌ Missing |
| Loot table item validity | ❌ Missing |
| Condition → Skill conflict checks | ❌ Missing |
| RankScaling curve reference checks | ❌ Missing |
| Semantic tag validation | ❌ Missing |
| Attribute propagation check | ❌ Missing |

### Layer 4: Export / Translation
`❌ Not yet built`

| Component | Status |
|---|---|
| YAML → UE5 Data Asset format | ❌ Missing |
| Tag library → Gameplay Tag hierarchy | ❌ Missing |
| Naming convention resolver | ❌ Missing |
| Schema version migration tool | ❌ Missing |

### Layer 5: UE5 Runtime
`❌ Future phase`

| Component | Status |
|---|---|
| GAS AttributeSet | ❌ Future |
| Gameplay Abilities (Skills) | ❌ Future |
| Data Tables (Items, NPCs, etc.) | ❌ Future |
| Gameplay Tag driven logic | ❌ Future |

---

## Roadmap

### Immediate — Authoring Layer Completeness
- [ ] Shared enum/constant definitions (damage types, status categories, slot types)
- [ ] Schema enforcement for the three design pillars across all combat-facing content
- [ ] Attribute propagation validation — confirm all tools use `attr_loader`, no hardcoded attribute names

### Short Term — Cross-Project Coherence
- [ ] Naming convention decision — standardize dot notation vs underscore before UE5 pipeline grows
- [ ] Deeper validator coverage — quest chains, skill prerequisites, loot table validity
- [ ] Stale YAML detection — flag files affected when shared definitions change

### Medium Term — UE5 Boundary Definition
- [ ] Export layer — define YAML → UE5 Data Asset mapping explicitly
- [ ] Gameplay Tag hierarchy document — map `tag_library.txt` to UE5 Gameplay Tag tree
- [ ] GAS AttributeSet spec — define UE5 counterpart for `attributes.json` before GAS implementation begins

---

## Long-Term Direction

- **Class switching** and save/load state (FFXIV-style)
- Gear-specific visuals, new actions/traits, internal databases
- UE5-side: migrate combat logic onto **GAS** (Gameplay Ability System), **Gameplay Tags + Gameplay Cues**, modular character and data assets
- Treat this YAML tool suite as the authoring front-end for a **Python-to-Asset pipeline** — schema decisions made here must stay compatible with UE5 Data Asset import

---

## Environment Notes

### Windows / Git Bash
If Bash tool calls fail with a `requires git-bash` error, Git Bash is installed but not being detected. Do **not** assume Git is missing.

**Fix:** Set `LLM_CODE_GIT_BASH_PATH` in `.LLM/settings.json`:
```json
{
  "env": {
    "LLM_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```
Or set it as a user-level environment variable pointing at `bash.exe` (typically `C:\Program Files\Git\bin\bash.exe`). If set but still not detected, this is a known LLM Code rough edge on Windows — fall back to the CLI/Git Bash terminal directly rather than the VS Code extension panel.

---

## Working Conventions for LLM Code

- Do **not** resolve the dot-namespaced vs underscore filename convention unilaterally — ask which to standardize on before any sweeping rename
- When adding a new Creator tool, mirror the existing pattern: Tkinter form → `save_yaml()` → category folder created if missing → `messagebox.showinfo` on success
- Prefer extracting duplicated logic (`tag_library.py`, `get_list(folder)` helpers) into shared modules over copy-pasting into new tools

---

*Last updated: 2026-07-05*
