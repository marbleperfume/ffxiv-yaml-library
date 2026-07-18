# Design Hub — Change History

Readable, sectioned record of the tooling + schema initiative. Each section maps
to one commit on the `design-hub-tooling` branch (same title). Newest work is at
the bottom; read top-to-bottom for the full story.

The through-line: the repo had **design philosophy in `Guidebooks/`** and
**content in `Classes/`, `Attributes/`, `Skills/`**, but nothing enforced that the
content actually followed the philosophy. This initiative makes the philosophy
machine-checkable and gives it an editor.

---

## 1. Formalize the stat contract

**What:** Restructured `Attributes/Base_Attributes.yaml` so every derived stat is
uniform and checkable: `Inputs` / `Formula` / `Coefficients` / `Prose`. Every
tunable constant is now a **named coefficient** whose value is either a number or
the literal `PENDING` — a first-class "not decided yet" state, so a balance number
is never silently invented. Added a formal `StatOverrides:` construct for declared
per-class deviations, and used it on the two classes that diverge:
Spiritcaller (linear Moisture-DR) and Strix (momentum Dive damage).
`Attributes/attributes.json` became **generated output** (see §6, `generate_legacy.py`)
rather than a hand-maintained second copy that could drift.

**Why:** The stat rules lived as prose scattered across files, with a drifted JSON
duplicate and undeclared per-class formula divergences. There was no way to tell an
intended exception from an accident, or a genuinely-undecided number from a typo.

**Files:** `Attributes/Base_Attributes.yaml`, `Attributes/attributes.json`,
`Classes/2.0/Spiritcaller_Design.yaml`, `Classes/2.0/Strix_Design.yaml`.

---

## 2. Add `Schemas/` — effect vocabulary + JSON Schemas

**What:** New top-level `Schemas/` folder (LLM-visible on clone):
- `EffectTypes.yaml` — the controlled vocabulary of mechanical effect types
  (Damage, DoT, Heal, HoT, Shield, Barrier, StatModifier, CrowdControl, Displacement,
  Movement, ResourceModify, ZoneCreate, StatusApply, ExploitWindow) with per-type
  required/optional params. Single source of truth for the vocabulary.
- `skill.schema.json` — the ability-record schema. **This started as a thin
  "mechanical packet" schema (v1) and was then reversed (v2)** to be
  methodology-first: `TriggerCondition` / `ItemBaselineReplaced` / `DecisionCreated` /
  `CCStage` / `RankProgression` are the load-bearing fields, with the typed `Effects`
  packet nested as the downstream detail. Carries an `x-fieldAliases` map so the
  existing lowercase spellings in class files validate without rewrites.
- `stat_contract.schema.json` — validates §1's structured shape and the
  `StatOverride` construct.

**Why:** No controlled vocabulary for effects existed anywhere (the keys
`effect_type` / `scaling_stat` appeared in zero files). The v1→v2 reversal happened
after confirming against `Guidebooks/class_item_baselines.md` that the per-class
files (Grappler etc.) are the *current* methodology and the thin `Skills/*.yaml`
records are the *outdated* ones — the opposite of the initial assumption.

**Files:** `Schemas/EffectTypes.yaml`, `Schemas/skill.schema.json`,
`Schemas/stat_contract.schema.json`.

---

## 3. Repair 4 unparseable class files

**What:** Fixed pre-existing YAML syntax errors that had never parsed:
`Grappler_Skills.yaml` and `Skyreign_Skills_Dragonguard.yaml` (unquoted scalars
containing `:` and `|`, e.g. `Stacks: 1 | Gauge: +4`), `Strix_Skills.yaml`
(mapping/list mixes — inserted `Abilities:` keys), `Wavecaller_Design.yaml`
(one indentation slip + a `X: y` prose scalar). All fixes are minimal quoting/indent
repairs; no design content changed.

**Why:** The new validator surfaced these on its first full run — the files were
silently broken and no tool had ever loaded them.

**Files:** `Classes/2.0/Grappler_Skills.yaml`,
`Classes/2.0/Skyreign_Skills_Dragonguard.yaml`, `Classes/2.0/Strix_Skills.yaml`,
`Classes/2.0/Wavecaller_Design.yaml`.

---

## 4. Migrate worked-example skills to typed Effects + methodology

**What:** Demonstrated the new schema on real skills, in place, preserving all prose:
- `Skills/Shield_Bash.yaml` — full migration: typed `Effects`, `ScalingStat`, and
  all five methodology fields (its `RankProgression` is honestly marked `PENDING`).
- `Skyreign_Skills_Dragon.yaml` (SmokeBreath) — its three ad-hoc effect sub-keys
  became typed `Damage` / `StatModifier` / `CrowdControl` / `ZoneCreate` instances.
- `Wavecaller_Skills.yaml` (Tidal Hymn) — added a typed `HoT` effect + `ScalingStat`.

**Why:** Proof the methodology serializes onto real content without losing the
hand-authored design prose, and a template for migrating the rest.

**Files:** `Skills/Shield_Bash.yaml`, `Classes/2.0/Skyreign_Skills_Dragon.yaml`,
`Classes/2.0/Wavecaller_Skills.yaml`.

---

## 5. Make `Project_Validator.py` embeddable

**What:** Minimal refactor: `validate_project(collector=None)` now accepts an
injectable collector; with no collector it prints and exits exactly as before
(CLI behavior byte-identical). The Design Hub wraps it via the collector instead
of duplicating any logic.

**Why:** Reuse the existing integrity checks from the web tool without a second copy.

**Files:** `Project_Validator.py`.

---

## 6. Design Hub — FastAPI backend

**What:** New `WebApp/backend/` serving the **live working tree** (no copy, no DB):
- `repo.py` — comment-preserving YAML I/O (ruamel round-trip; per-file CRLF/LF
  preservation so one edit doesn't reflow the whole file).
- `validators/` — `core.py` (wraps §5), `stat_contract.py` (§1/§2 conformance,
  PENDING surfacing, drift detection, undeclared-override detection),
  `skill_schema.py` (methodology grading + typed-effect checks + §25 cooldown audit).
- `ability_io.py` — ability-level read/write with document paths and alias-aware
  targeted merges (a one-field edit is one surgical diff line, in the file's own
  spelling).
- `generate_legacy.py` — regenerates `Attributes/attributes.json` from the contract.
- `tracker.py` — parses `Guidebooks/class_list_qual_context.md` roster status and
  joins it with per-class ability grades.
- `main.py` — all `/api/*` endpoints + static frontend serving.

**Why:** A single tool to edit content, enforce the schemas, and see finalization
status — replacing the 19 standalone `*Creator.pyw` editors and the abandoned
`Hub_Master.pyw`.

**Files:** `WebApp/backend/**`, `WebApp/__init__.py`, `WebApp/README.md`.

---

## 7. Design Hub — frontend (methodology editor, tracker, validation, graph)

**What:** No-build React (ES modules + htm via import map — no Node required):
- **Editor** — skill files open as an ability list (grade dots) + a methodology-first
  form: Design section (Trigger / ItemBaseline / Decision / CCStage / RankProgression)
  on top, gating with a live §25 hint, the typed `Effects` packet demoted below,
  prose, and a raw-mode escape hatch. Live grading mirrors the backend.
- **Tracker** — all 30 classes across 4 tiers with status chips
  (complete / undesigned / blocked / race-locked / rework-flagged) and per-class
  ability progress bars.
- **Validation** — findings grouped by severity, click-to-open.
- **Graph** — dependency-free force-layout of the relationship graph.

**Why:** The point of the schema is to make gaps fillable; the editor is where you
fill them, and the tracker is the finalization queue made visible.

**Files:** `WebApp/frontend/public/**`.

---

## 8. Docs & housekeeping

**What:** This `HISTORY.md`, the `USER_GUIDE.md` (how to transition/add variables and
deprecate files), and `.gitignore` entries for `WebApp/.venv/` and
`WebApp/frontend/dist/`.

**Files:** `WebApp/HISTORY.md`, `WebApp/USER_GUIDE.md`, `.gitignore`.

---

## Where things stand

- **0 validation errors** repo-wide. Remaining findings are informational:
  `pending` (undecided coefficients + draft abilities), `legacy`
  (`GenerateWater.yaml`, the one un-migrated pre-methodology record), `info`
  (hardcoded-formula copies in `CombatSim/`), `warning` (real dangling file refs).
- **Grappler is the only fully methodology-finalized class** (21/21). The four
  roster-"complete" classes grade 0-finalized — design-doc-complete is not the same
  as methodology-finalized. That delta is the finalization backlog the Tracker shows.
- Open decisions left to you: effect-type taxonomy naming; the many `PENDING`
  coefficient values; the duplicate `DESIGN_OVERRIDE.md` (root vs `Guidebooks/`).
