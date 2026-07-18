# Design Hub — User's Guide

How to evolve the design data safely: **transition** existing variables, **add** new
ones, and **deprecate/delete** old files. Written so you can come back cold and not
break the contract.

> **The one rule that prevents most mistakes:** after any change, run the validator.
> Zero `error`-severity findings is the gate. Everything else (`pending`, `legacy`,
> `info`, `warning`) is informational — a to-do list, not a failure.

```
# from the repo root (YAML Library):
WebApp\.venv\Scripts\python.exe WebApp\backend\run_validators.py
```

Common commands:

| Task | Command (from repo root) |
|---|---|
| Validate everything | `WebApp\.venv\Scripts\python.exe WebApp\backend\run_validators.py` |
| Regenerate `attributes.json` | `WebApp\.venv\Scripts\python.exe WebApp\backend\generate_legacy.py` |
| Start the editor | `WebApp\.venv\Scripts\python.exe -m uvicorn WebApp.backend.main:app --port 8400` → http://127.0.0.1:8400 |

**Source-of-truth files** (edit these; everything else follows):
- `Attributes/Base_Attributes.yaml` — every stat and coefficient.
- `Schemas/EffectTypes.yaml` — the effect-type vocabulary.
- `Schemas/skill.schema.json` — the ability-record shape + field aliases.
- `Schemas/stat_contract.schema.json` — the stat-contract shape.

**Never hand-edit** `Attributes/attributes.json` — it is generated. If you change a
stat, regenerate it (the validator flags drift as an `error` if you forget).

---

## Part 1 — Transitioning an existing variable

### 1a. Set a `PENDING` coefficient to a real number

When a balance pass decides a value:

1. Open `Attributes/Base_Attributes.yaml`, find the coefficient (e.g.
   `evasion_per_speed`).
2. Change `Value: PENDING` to the number. Keep or update the `Note:`.
3. Validate. The `stat.pending-coeff` finding for it disappears; nothing else moves.

Do **not** replace `PENDING` with a placeholder like `0` or `1` "for now" — a real
zero and an undecided value must stay distinguishable. `PENDING` *is* the honest state.

### 1b. Change a formula

1. Edit the `Formula:` string and its `Coefficients:` in `Base_Attributes.yaml`.
2. If the formula now references a new constant, add it as a named coefficient
   (`Value: PENDING` until decided) — bare bracket placeholders like `[coeff_TBD]`
   are rejected (`stat.legacy-placeholder`).
3. Validate.

### 1c. Rename a stat or attribute

1. Rename it in `Base_Attributes.yaml` (both the `Attributes:` entry and any
   `Inputs:`/`Formula:` references).
2. Update `ScalingStat` enums in `Schemas/skill.schema.json` if it's a Tier-1 stat.
3. Search the repo for the old name (`grep -r OldName`) and update references.
4. If it's a Tier-1 attribute, regenerate `attributes.json`.
5. Validate — `stat.dangling-ref` and drift findings catch anything you missed.

### 1d. Migrate a skill from freeform → methodology format

This is the main day-to-day transition. Do it in the editor:

1. Start the server, open the class's `*_Skills.yaml` in the **Editor** tab.
2. Pick a `draft` ability (amber dot). Fill the Design fields the banner lists as
   missing — `TriggerCondition`, `ItemBaselineReplaced`, `DecisionCreated`,
   `CCStage`, `RankProgression`. The banner flips to **FINALIZED ✓** live.
3. Save. The write is surgical (one ability, its own spelling) and preserves comments.

Grappler_Skills.yaml is the reference for what "finalized" looks like.

### 1e. Promote a per-class override into the central contract (or demote)

If a `StatOverrides` deviation becomes the rule for everyone, move it into
`Base_Attributes.yaml` as the central formula and delete the `StatOverrides:` block
from the class file. To go the other way, add a `StatOverrides:` block (see §2e).
Validate either way.

---

## Part 2 — Adding a new variable

### 2a. New Tier-1 attribute (e.g. a new `Luck` stat)

1. Add it under `Base_Character.Attributes:` in `Base_Attributes.yaml` with a default
   and a `#` intent comment (the comment becomes the generated json's `intent`).
2. Add any derived stats that consume it (see §2b).
3. Add it to the `ScalingStat` enum in `Schemas/skill.schema.json` so skills can scale
   from it.
4. Regenerate `attributes.json`.
5. Validate.

### 2b. New derived stat

1. Add a block under `DerivedStats:` with `Inputs`, `Formula`, `Coefficients`
   (new constants → `Value: PENDING`), and `Prose`.
2. Match the shape of an existing entry — `stat_contract.schema.json` enforces it.
3. Validate.

### 2c. New effect type (extend the vocabulary)

1. Add the type to `Schemas/EffectTypes.yaml` with `Description`, `RequiredParams`,
   `OptionalParams`.
2. Add its name to the `Effects[].Type` enum in `Schemas/skill.schema.json`.
3. Refresh the browser (the editor caches the vocabulary at page load) — the new type
   appears in every effect-card dropdown automatically.
4. Validate.

### 2d. New methodology / ability field

1. Decide the canonical name and add it to `METHODOLOGY_FIELDS` + `ALIASES` in
   `WebApp/backend/validators/skill_schema.py` (list every existing spelling so old
   files count without rewrites).
2. Mirror it in `Schemas/skill.schema.json` (`properties` + `x-fieldAliases`) — the
   frontend reads aliases from there, so the editor picks it up with no JS change.
3. Add a short entry to `FIELD_DOCS` in `WebApp/frontend/public/components.js` so the
   form shows its help line.
4. Validate; the grader now requires the new field for `finalized`.

### 2e. New `StatOverrides` declaration (a class legitimately diverges)

Add to the class's `_Design.yaml`:

```yaml
StatOverrides:
  - OverridesDerivedStat: EffectiveDefense.DamageReduction
    Scope: "when/where it applies"
    ReplacementFormula: "the class-specific formula"
    Interaction: replaces_within_scope   # or stacks_with_base
    Reason: "the design argument, not just the math"
```

Without this, a class-file formula trips `stat.undeclared-override` (an `error`).
See Spiritcaller and Strix for worked examples.

### 2f. New class or standalone skill

- **New ability in an existing class:** add it in the editor, or append to the
  `*_Skills.yaml` following the Grappler field pattern.
- **New standalone skill:** create `Skills/YourSkill.yaml` with a `Key` and the
  methodology fields. A thin record with no methodology fields is tagged
  `skill.pre-methodology` (`legacy`) until you flesh it out.

---

## Part 3 — Deprecating & deleting old files

Prefer **deprecate-then-verify-then-delete**. The validator is your safety net: it
reports `stat.dangling-ref` / `core.integrity` errors when something still points at
what you removed.

### 3a. Retire a superseded file

1. Grep for references first: `grep -rn "OldFile" .` (design docs cross-reference by
   filename a lot).
2. Repoint or remove those references.
3. Delete the file.
4. Validate — a clean run means nothing depended on it. A `dangling-ref`/`integrity`
   finding means back up and fix the reference first.

### 3b. Finish the `attributes.json` deprecation

`attributes.json` is already generated. When the legacy tkinter `*Creator.pyw` tools
are gone for good, you can delete both `attributes.json` and `Attributes/attr_loader.py`
and drop the `generate_legacy.py` step. Until then, leave it generated — don't edit it.

### 3c. Migrate then delete a pre-methodology record

`Skills/GenerateWater.yaml` is the last thin pre-methodology record (flagged
`skill.pre-methodology`). Either bring it up to the methodology format (§1d) or, if
it's truly obsolete, confirm nothing references its `Key`
(`grep -rn "GenerateWater" .`) and delete it.

### 3d. Deprecate a class

1. In `Guidebooks/class_list_qual_context.md`, set its `YAML Status` marker
   (🔴/✅/⚠️) — this drives the **Tracker** tab, so status stays visible without
   deleting anything.
2. To fully remove: delete the class's `_Design` / `_Skills` / `_Validation` files,
   grep for the class name, clean references, validate.

### 3e. Archive rather than delete

The repo already uses a `Legacy files/` archive convention (outside the git working
tree). For pre-2.0 or superseded-but-worth-keeping content, move it there instead of
deleting, then validate.

---

## Golden rules (the short version)

1. **Run the validator after every change.** Zero errors is the gate.
2. **`PENDING` is a real state** — never fake-fill a coefficient.
3. **Declare divergence** — a class formula without a `StatOverrides` block is an error.
4. **Never hand-edit generated files** (`attributes.json`); regenerate them.
5. **Prose stays** — typed fields live *alongside* design prose, never replace it.
6. **Schemas are source of truth** — to add a *kind* of variable, update the schema
   first, then the content follows.
