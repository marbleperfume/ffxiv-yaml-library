# CLAUDE.md — Unified RPG Design Hub / YAML Library

## Project Overview

This project is a suite of standalone Python desktop tools that generate and edit
YAML "spec" files for a UE5 RPG (FFXIV-inspired). There is no game engine code
here — this is the **design/data authoring layer**. Each tool is a form-based
editor that writes structured YAML into a category folder (`NPCs/`, `Items/`,
`Skills/`, etc.), which is later consumed by the UE5 project as GameplayTag-driven
data assets.

- Most tools: Tkinter (`*.pyw`), one entry point (`Hub_Master.pyw`): PyQt6
- Output: YAML files, organized by category folder, meant to be human- and
  Claude-readable design docs as much as engine input
- `Project_Validator.py`: cross-reference integrity checker (Race/Class/Item
  references actually exist)

## Directory / Category Layout

Each category has its own folder, created on first save if missing:
`NPCs/`, `NPCs/Hostile/`, `NPCs/Bosses/`, `Items/`, `Attire/`, `Skills/`,
`Conditions/`, `Passives/`, `Loot/`, `Summons/`, `Titles/`, `Quests/`,
`Races/`, `Classes/`, `Tutorials/`, `tags/`, `Attributes/`.

`Hub_Master.pyw` treats the whole tree as one project (`PROJECT_DIR`) and scans
it recursively for `.yaml`/`.yml` files to build a live tag/key registry and an
exported `Project_Relationships.json` for external/LLM context.

## Key Conventions

- **Keys vs filenames**: hand-authored "template" YAML files use dot-namespaced
  keys as the literal filename (e.g. `Skill.Combat.AeroSlash.yaml`,
  `NPC.Enemy.Swarm.BeeCloud.yaml`). Tool-generated files instead take whatever
  the user typed in the Name field and do `name.replace(' ', '_')` for the
  filename. **Both conventions currently coexist** — see Known Issues below.
- **Tags**: a shared `tags/tag_library.txt` (one tag per line) backs an
  "Add Tag" + "Tag List" picker modal (`TagSelectorModal`) that's copy-pasted
  near-identically into `Item Registry Creator.pyw`, `ConditionCreator.pyw`,
  and `AttireCreator.pyw`. Treat these three as the same logical component.
- **Attributes**: single source of truth is `Attributes/attributes.json`
  (schema: name → default + intent) plus `Attributes/Base_Attributes.yaml`
  (actual starting values under `Base_Character.Attributes`). Loaded via
  `attr_loader.get_full_attribute_data(caller_file)`, which resolves paths
  relative to the calling script's own directory + `/Attributes`.
- **Three design "pillars"** show up repeatedly in NPC/Passive/Boss/Summon
  schemas — always in this order: **Adventurer** (loot/progression),
  **Mercenary** (counter-play, commitment level, interrupt windows),
  **Strategy** (tactics/formation/AI behavior). Any new combat-facing content
  type should probably expose these three the same way.
- **Rank scaling pattern**: enemy NPC YAML uses a nested `RankScaling` block
  with `AdventurerLoot` (a reference to a global loot curve),
  `MercenaryReaction.Rank1/Rank2` (condition/action/cast-time), and
  `StrategyAI` (aggro/leash/terrain profile). Follow this shape for new
  hostile NPCs rather than inventing a new structure.

## Known Issues / Inconsistencies (fix opportunistically, don't assume intentional)

Resolved (see git history / file contents for the actual fix):

- ~~`PassiveCreator.pyw::save_yaml` referenced undefined names `name` and
  `cleanse_req`~~ — now uses `self.name_entry.get()` / `self.cleanse_req.get()`.
- ~~`DutySupportCreator.pyw` was missing the `ttk` import and a launcher~~ —
  added `from tkinter import ttk`, an `if __name__ == "__main__"` block, and
  folder creation for `Tutorials/` on save (matching the standard pattern).
- ~~`Hub_Master.pyw::export_project_relationships` called `QFileDialog`
  without importing it~~ — added to the `PyQt6.QtWidgets` import.
- ~~`QuestPipelineViewer.pyw` read `data['Metadata']['PipelineID'/'SequenceIndex'/'Intent']`
  but `QuestCreator.pyw` saves those fields flat~~ — viewer now reads the flat
  fields (`PipelineID`, `SequenceIndex`, `NarrativeIntent`) that the creator
  actually produces.
- ~~`PROJECT_DIR` in `Hub_Master.pyw` hardcoded the author's absolute path~~ —
  now resolved via `os.path.dirname(os.path.abspath(__file__))`, same pattern
  already used by `RaceCreator.pyw`/`ClassCreator.pyw` (their `BASE_DIR` was
  never actually hardcoded — only a misleading comment suggested it was).
- ~~`NPC.Enemy.Drakol.Lower.yaml`'s `Key` field didn't match its filename~~ —
  `Key` updated to `NPC.Enemy.Drakol.Lower` to match.
- ~~Tag-library helper (`get_tag_library` / `add_to_tag_library`) and
  `TagSelectorModal` were duplicated verbatim in three tools~~ — extracted into
  shared `tag_library.py`, imported by `Item Registry Creator.pyw`,
  `ConditionCreator.pyw`, and `AttireCreator.pyw`.

Still open (needs a decision, not a unilateral fix):

- File naming is inconsistent at the tool level: `NPC Hostile Creator.pyw`,
  `Item Registry Creator.pyw`, `Skill Creator.pyw`, `Title Registry Creator.pyw`
  have spaces; most other tools don't. Nothing references these filenames
  programmatically (grepped — clean), but renaming may break desktop
  shortcuts/muscle memory, so ask before renaming.

## Roadmap / Direction (from design notes)

Longer-term direction is moving this data pipeline toward:
- **Class switching** and save/load state (FFXIV-style)
- Gear-specific visuals, new actions/traits, internal databases
- UE5-side: migrate combat logic onto **GAS** (Gameplay Ability System),
  **Gameplay Tags + Gameplay Cues**, modular character + data assets
- Treat this YAML tool suite as the authoring front-end for that eventual
  **Python-to-Asset pipeline** — i.e., schema decisions made here should stay
  compatible with being imported as UE5 Data Assets later.

## Environment Notes

- Windows machine. If Bash tool calls fail with a "requires git-bash" error,
  Git Bash is installed but not being detected — do **not** assume Git is
  missing. The fix is `CLAUDE_CODE_GIT_BASH_PATH`, either in
  `.claude/settings.json`:
  ```json
  { "env": { "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe" } }
  ```
  or as a user-level environment variable pointing at the actual `bash.exe`
  (typically `C:\Program Files\Git\bin\bash.exe`). If it's set but still not
  detected, that's a known Claude Code rough edge on Windows — don't loop on
  re-diagnosing it; just note it and fall back to the CLI/Git Bash terminal
  directly instead of the VS Code extension panel.

## Working Conventions for Claude Code

- Don't "fix" the dot-namespaced-filename vs `Name.replace(' ','_')` question
  unilaterally — ask which convention to standardize on before doing a
  sweeping rename.
- When adding a new Creator tool, mirror the existing pattern: Tkinter form →
  `save_yaml()` → category folder created if missing → `messagebox.showinfo`
  on success.
- Prefer extracting duplicated logic (tag picker, `get_list(folder)` helpers)
  into shared modules over copy-pasting into new tools.
