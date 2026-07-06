# LLM.md — Unified RPG Design Hub / YAML Library

## Project Overview

This project is a suite of standalone Python desktop tools that generate and edit
YAML "spec" files for a UE5 RPG (FFXIV-inspired). There is no game engine code
here — this is the **design/data authoring layer**. Each tool is a form-based
editor that writes structured YAML into a category folder (`NPCs/`, `Items/`,
`Skills/`, etc.), which is later consumed by the UE5 project as GameplayTag-driven
data assets.

- Most tools: Tkinter (`*.pyw`), one entry point (`Hub_Master.pyw`): PyQt6
- Output: YAML files, organized by category folder, meant to be human- and
  LLM-readable design docs as much as engine input
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
- ~~All `tk.Listbox` widgets defaulted to `exportselection=True`, so selecting
  in one listbox silently cleared another's selection (multi-list forms lost
  data on save)~~ — every Listbox in the repo now passes `exportselection=False`.
- ~~`Skill Creator.pyw` had its own stale copy of `add_to_tag_library` and no
  cooldown/combo/status/class fields~~ — reworked to the GameplayAbility shape
  (ActionType/IsOGCD, RecastTime, MaxCharges, Resource, Combo, AppliesStatuses,
  ClassRestrictions), now imports shared `tag_library.py`.
- ~~`LootCreator.pyw` wrote one entry per file, unable to express the loot
  tables NPC YAML references~~ — now a table editor: one file per table with an
  `Entries` list (load/edit/save roundtrip).
- ~~`SummonCreator.pyw` hardcoded its own attribute list~~ — now pulls the
  schema from `attr_loader` like Race/Character/Class creators.
- ~~`BossCreator.pyw` output had no identity — no Key, TemplateRef, skills, or
  loot link~~ — now writes `Identity.Key` (`NPC.Boss.*`), optional TemplateRef,
  AssignedSkills, and a LootTable reference.

## Additions (2026-07-06)

- **New content types + folders**: `Quests/` (extended step schema: StepType,
  TargetNPCs list, TargetNPCGroup, DialogueRef, GrantItem, RequiresFlag /
  OnComplete.SetsFlag, Branches, Reward.Copper / Reward.Reputation),
  `Dialogue/` (per-scene files: Participants, Lines with
  Speaker/Text/ExpressionTag/VOPath, LevelSequenceRef for cutscenes),
  `Expressions/expression_library.txt` (+ shared `expression_library.py`,
  mirrors tag_library pattern; maps to GameplayCue.Expression.* / facial
  montages in UE5), `NPCGroups/`, `Reputation/`, `World/WorldClock.yaml`
  (Eorzea-style accelerated clock), `Zones/Zone_Library.yaml` (MalachiteCity
  is `IsPlaceholder: true` — a stand-in town until maps exist).
- **New tools**: `DialogueCreator.pyw`; `QuestCreator.pyw` reworked (tabbed,
  produces the extended schema; still viewer-compatible).
- **Reference quest chain**: `Chef.Crem.Courier` Seq0–Seq5 + 6 dialogue files —
  treat as the canonical example of the extended schema.
- **Races**: `Race_Library.yaml` gained a `Monsters` category (unique race per
  monster, e.g. `Bee Cloud`); ClassCreator/CharacterCreator exclude it — class
  kits are racially locked to playable races only. `ClassCreator.pyw` now
  multi-selects races and batch-writes one `Race_Class.yaml` per selection.
- **`NPC Hostile Creator.pyw` deleted** (was a strict field subset of
  `NPCCreator.pyw`; confirmed with user before removing).
- **Hub_Master**: `export_project_relationships` was never wired into the File
  menu (unreachable) — now added, alongside a new **Export Gameplay Tags**
  action that emits a UE5 `DefaultGameplayTags.ini` from the tag library,
  expression library (as `GameplayCue.Expression.*`), and every YAML `Tags:`
  list, skipping entries that violate UE5 tag naming.
- **Rank pipeline (`Ranks/` folder)** — the three-pillar system is now a
  formal contract; `Ranks/Rank_System.yaml` is canonical. Core rules: enemies
  only read a per-area-resolved snapshot `{Adventurer, Mercenary, Strategy:
  1-3}`, never raw progression; enemy `RankProfile` requires `Mercenary.Rank1`
  and `Doctrine.Level1` (higher tiers optional, missing tier inherits the tier
  below); enemy-side Strategy is named **Doctrine**; Adventurer is
  subzone-scoped (widens per `Zone_Library.yaml` `RankEscalation`), Mercenary
  and Strategy are account-scoped; Mercenary adds kit breadth + SyncRetention,
  never potency; gear never feeds rank computation; Doctrine mechanics
  requiring outside knowledge must declare `KnowledgeChecks` with a
  `LoreSource`. `Zone_Library.yaml` restructured to Regions → Subzones with
  LevelBand. Drakol/BeeCloud migrated `RankScaling` → `RankProfile` (Drakol =
  minimal example, BeeCloud = full-tier example). `NPCCreator.pyw` authors the
  new shape (empty tier box = omitted = inherits). `Project_Validator.py`
  enforces the contract (required tiers, inherit direction, LoreSource,
  RaceKey ↔ Race_Library, Location ↔ Zone_Library) and exits nonzero on
  failure. `CharacterCreator.pyw` rank spinboxes now 1-3 to match the
  snapshot range.
- **Adventurer rank-up methods** — see **`RankUpMethods.md`** (design-doc
  reference, not shown in-game) for the full writeup. Summary: Adventurer
  gained a 4th weighted source, `RegionEnhancement` (20 of 100, redistributed
  to the other three if a Region declares none), fed by a per-Region
  enhancement track declared in `Zone_Library.yaml` (`Enhancement.Model`:
  `Relic` or `Materia` — varies per region, not fixed globally) and defined in
  the new `Enhancements/` folder (`Enhancements/Relic.FanVillage.yaml` is the
  worked Relic example; Materia has no worked example yet — write one when a
  region actually wants it). New `Guidebooks/` folder holds in-game pop-up
  content pointing players at rank-up methods
  (`Guidebook.Adventurer.RankUp.FanVillage.yaml`: PopupTitle/PopupText +
  optional WaypointNPC, left `null` until a real guide NPC exists — don't
  invent one to fill the field). `Project_Validator.py` now checks every
  Region's `Enhancement.TrackRef` resolves to a real `Enhancements/*.yaml`.
  Mercenary/Strategy/racial-summon rank-up methods are still pending — stubbed
  in `RankUpMethods.md` so they read as "not designed yet," not forgotten.
- **Mercenary rank-up methods (worked example)** — new `Combat/AggroSystem.yaml`
  is the canonical Focus/Aggro/Unfocus contract: `Aggro = Proximity + Focus +
  StrategyRankModifier` (weighted), an enemy drops its current cast and
  retargets if a non-current-target's Aggro crosses
  `RankProfile.Doctrine.<Tier>.FocusRedirectThreshold` — a genuine
  self-interrupt, not just a threat-table swap. This *is* the Tank
  RoleMechanic (`Ranks/RoleMechanics.yaml`), not a separate system; Healer's
  RoleMechanic is Healing-under-pressure (can't be exercised on demand, hence
  its test's different shape); DPS is Maximum Rotation Uptime (no worked
  example yet). `Classes/ClassMechanics.yaml` (PLACEHOLDER, only Adafold's
  "Bulwark Gauge" defined) and `Classes/Class_Prerequisites.yaml` (Base = no
  gate; Promoted = Base-class level + Role Quest + Mercenary Rank2; Special =
  a SEPARATE track, not built on Promoted, requiring its own quest + Mercenary
  Rank3 — one worked example each, Lancer/Dracomancer, both forward-reference
  quests that don't exist yet) round out the class side.
  `Passives/Unfocus.yaml` (stacking debuff, reduces potency of an enemy's
  Doctrine Level2/3 skills only) and `Skills/Shield_Bash.yaml` (Adafold's
  Focus-generating RoleMechanic skill, gated behind a skill quest rather than
  granted by leveling) are the worked content. `Ranks/Mercenary_Unlocks.yaml`
  now states the `SkillQuestGate` rule explicitly (clear every skill quest for
  skills outside the current class's level-up schema before the broad
  Rank2/Rank3 test unlocks) and `TestQuest` varies per Role. Test fixture:
  `NPCs/Bosses/NPC.Boss.Test.MechaGolem.yaml` reuses `RankProfile.Doctrine` to
  express the test tiers themselves — Level2 has a `RandomCastPool` of 3
  skills (one randomly selected per attempt, tests adaptability not
  memorization), Level3 adds a `StabilityContest` hazard (using a
  `Tag.Skill.Risky` skill mid-cast instantly drops the player's own cast). Four
  worked quests in `Quests/`: `SkillQuest.Adafold.ShieldBash`,
  `Test.Mercenary.Rank2.Tank`, `Test.Mercenary.Rank3.Tank`,
  `Test.Mercenary.Rank2.Healer` (buff/damage phase → crisis-triggered healing
  phase, rather than a continuous check). `Project_Validator.py`'s existing
  RankProfile checks cover this fixture without modification (Doctrine
  inherit-direction, required tiers).
- **Racial summon exemption (worked example)** — `Ranks/Rank_System.yaml`
  gained `RacialSummonExemption`: a Summon with a `RacialAttachment` field
  (`RaceKey` + `MercStratExempt: true`) bypasses Mercenary/Strategy gating
  entirely, even though summons normally count as "extra buttons" gated like
  Skills/Classes — cross-referenced from both `Mercenary_Unlocks.yaml` and
  `Strategy_Unlocks.yaml`. Worked example: `Summons/Water_Slime.yaml`, unique
  to the "Lower Drakols" race (matches `Race_Library.yaml` exactly — the
  existing `NPC.Enemy.Drakol.Lower.yaml` gained `RaceKey: Lower Drakols` and
  `InnateSummon: Summon.Water.Slime` to tie the lore in). Mechanically it's
  not a normal on/off summon: `PresenceType: Innate` (present by default, no
  cast needed) with a `DismissTrigger` — the new racial skill
  `Skills/GenerateWater.yaml` (`Skill.Combat.Drakol.GenerateWater`, gated via
  a new `RaceRestrictions` field, parallel to `ClassRestrictions`) temporarily
  dismisses it for a water-environment synergy, and it returns on its own
  after `ReturnAfterSeconds`. The trade-off: the Slime's `PassiveEffect`
  suppresses `Passives/DrySkin.yaml` (new — Fire damage-taken +15%, Speed
  -10) while present; dismissing it removes that suppression for the
  window. `Water Slime` as a name already existed as an unrelated alchemy
  consumable (`Items/Item.Consumable.WaterSlime.yaml`) — confirmed by the
  user to be a deliberate planted artifact testing exactly this kind of
  naming-collision handling; left untouched, different category/key, no
  actual collision. Correct call was to flag it and not merge/rename either
  file.
  Note: the real race/Drakol lore this is based on lives in a text file on
  the user's other PC, not in this repo — what's captured here is a
  from-scratch retelling given in this conversation, so treat it as
  authoritative unless the original file resurfaces and disagrees.
- **Strategy rank-up methods (worked example)** — `Ranks/Strategy_Unlocks.yaml`
  gained `TestEncounterConstraints`: Strategy tests always draw from a
  Goblin/Flying-enemy pool and escalate by RECOMBINING those building blocks
  into a new layout per rank — a different pattern than Mercenary tests,
  which reuse one NPC and escalate via `RankProfile.Doctrine` tiers. Also
  gained `RoleToolBudget`: Tanks are expected to need fewer of a test's
  provided tactical tools than other roles (their RoleMechanic already
  covers part of the job), and that gap widens at higher Strategy rank.
  Worked example (Rank2): `NPCs/Bosses/NPC.Boss.Test.GoblinVanguard.yaml`
  (melee frontline, Doctrine Level1 only — no tier escalation on this file)
  plus `NPCGroups/Group.Test.GoblinRangedCasters.yaml` (3 ranged AoE
  casters). New `Items/Item.Tactical.*.yaml` (Category: `Tactical`, not yet
  in Item Registry Creator's Category dropdown): Smokescreen
  (suppresses ranged targeting so the player can safely close on the
  Vanguard), Bombs (flat burst damage, any role), Traps (conditional
  immobilize — breaks free if cumulative damage on the target exceeds a
  small threshold, so committing real damage costs you the control). The
  quest `Quests/Test.Strategy.Rank2_Seq0.yaml` runs the whole thing solo
  (`SoloOnly: true`) specifically because a party's tank/healer would
  trivially split this fight otherwise; `RoleToolBudget` per-role
  (Tank: 1 tool expected, NonTank: 3) is encoded on both the quest and the
  Vanguard NPC.
- **Racial bonus skills (GAS-referenced design decision)** — bonus racial
  skills are granted via `RaceKey`, NOT baked into Class files. Rationale
  (GAS-grounded): Lyra's `AbilitySet` pattern grants multiple independent
  ability sets onto one ASC (class kit, racial bonus, equipment) rather than
  one monolithic per-archetype blob; baking racial skills into Class files
  would also reintroduce the Race×Class file multiplication problem already
  avoided for class-switching. Mechanism, split grant-from-restriction like
  GAS does: `RaceCreator.pyw`'s per-subrace spec files
  (`Races/<Parent>_<Subrace>.yaml`) gained `Definition.Subrace` (the race's
  own name, for cross-checking) and `Definition.BonusSkills` (a multi-select
  Skill picker — the grant list, GAS-AbilitySet-equivalent), while the Skill
  itself still carries `RaceRestrictions` (already existed on
  `Skill.Combat.Drakol.GenerateWater` — the GAS-tag-requirement-equivalent
  gate). A character's real kit is the union of Class `AssignedSkills` +
  Race `BonusSkills` + skill-quest-earned skills + Mercenary-rank unlocks —
  four independent sources, never one combined file. Worked example:
  `Races/Wanderers_Lower_Drakols.yaml` grants `GenerateWater` via
  `BonusSkills`. `Project_Validator.py` now cross-checks every Race's
  `BonusSkills` resolve to a real `Skills/*.yaml` Key, and — if that skill
  declares `RaceRestrictions` — that the granting race's `Subrace` is
  actually on the list.

- **Two Madolt NPCs, full quest chains (worked example)** — `Goldwyn.PathOfTravelers`
  (Seq0-5) and `Reiden.GalactosUprising` (Seq0-4), each a full quest
  Seq*.yaml + matching Dialogue/*.yaml chain like Chef.Crem.Courier.
  Goldwyn Excelsior (`NPC.Friendly.MalachiteCity.GoldwynExcelsior.yaml`) is
  a comedic-weak rich-boy Traveler hopeful whose gear
  (`Items/Item.Equipment.Goldwyn.SpineSword.yaml`,
  `Items/Item.Equipment.Goldwyn.RecallSphere.yaml`,
  `Attire/GoldWasteplate_*.yaml`) does the work his own strength can't; his
  mentor Kaeloth Windpaw (`NPC.Friendly.MalachiteCity.KaelothWindpaw.yaml`,
  RaceKey `Unrecorded` -- new Landwin subrace added to
  `Races/Race_Library.yaml` specifically to encode "lineage never
  recorded" as intentional lore) dies in Seq2 to Nekrath
  (`NPCs/Bosses/NPC.Boss.Nekrath.yaml`, RaceKey `Ancient Feline` -- new
  Monsters entry), an Ancient feline offended by a Landwin inheriting their
  martial style (`Skills/Skill.Combat.Landwin.EnergyChannel.yaml` +
  `FelineSpiritForm.yaml` + `Summons/Summon.Landwin.FelineSpirit.yaml`).
  Seq4 is the full cinematic finale (armor stripped piece by piece, player
  downed, ignite via the Spine Sword's pre-magnetized lock on Nekrath's
  internally-held energy, two failed Recall Sphere attempts, a ghost-assist
  redirect, final explosion) -- the internal-vs-external energy distinction
  is stated on-screen in Seq3 specifically to seal the "why doesn't this
  work on anyone" plothole. Chain closes with the `Reputation.Agents.yaml`
  faction founded as this world's Scions-equivalent. Reiden Kurogane
  (`NPC.Friendly.MalachiteCity.ReidenKurogane.yaml`) is the anime-competent
  foil: same RaceKey (Madolt), opposite relationship to strength. His paired
  `Item.Equipment.Reiden.ConvergenceBlade/Shield.yaml` (gunlance-style
  sword + tower shield, both electron-field "Elemental Convergence" tech)
  block/discharge loop is taught small in Seq1 against
  `NPCGroups/Group.MalachiteCity.GalactosDroneSquad.yaml`, then scaled up
  in the Seq3 Chapter 1 finale (Susano-style ally-blocks-the-unblockable
  beat vs `NPC.Boss.ColossusPrime.yaml`, deployed by recurring villain
  `NPC.Boss.Galactos.yaml`, who escapes by design rather than dying).
  Both Madolts share the same payoff line ("strength isn't the only thing
  that wins a fight" / "it's not always about strength when you fight a
  Landwin") as a deliberate structural echo. All Boss-folder files carry a
  minimal `RankProfile` (Drakol-minimal pattern) purely for contract
  completeness -- these are one-off scripted story fights, not repeatable
  rank trials.

Still open (needs a decision, not a unilateral fix):

- File naming is inconsistent at the tool level: `Item Registry Creator.pyw`,
  `Skill Creator.pyw`, `Title Registry Creator.pyw` have spaces; most other
  tools don't. Nothing references these filenames programmatically (grepped —
  clean), but renaming may break desktop shortcuts/muscle memory, so ask
  before renaming.

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
  missing. The fix is `LLM_CODE_GIT_BASH_PATH`, either in
  `.LLM/settings.json`:
  ```json
  { "env": { "LLM_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe" } }
  ```
  or as a user-level environment variable pointing at the actual `bash.exe`
  (typically `C:\Program Files\Git\bin\bash.exe`). If it's set but still not
  detected, that's a known LLM Code rough edge on Windows — don't loop on
  re-diagnosing it; just note it and fall back to the CLI/Git Bash terminal
  directly instead of the VS Code extension panel.

## Working Conventions for LLM Code

- Don't "fix" the dot-namespaced-filename vs `Name.replace(' ','_')` question
  unilaterally — ask which convention to standardize on before doing a
  sweeping rename.
- When adding a new Creator tool, mirror the existing pattern: Tkinter form →
  `save_yaml()` → category folder created if missing → `messagebox.showinfo`
  on success.
- Prefer extracting duplicated logic (tag picker, `get_list(folder)` helpers)
  into shared modules over copy-pasting into new tools.
