# Rank-Up Methods Reference

Authoring reference for how a player actually raises each of the three rank
pillars. `Ranks/Rank_System.yaml` defines the *contract* (snapshot, scopes,
defaulting rule); this doc explains the *methods* — what a player does to move
the needle on each pillar. Written for design/authoring use (including other
LLM sessions picking up this project), not shown to players in-game.

Status: all three pillars plus the racial-summon exception are specified
below.

## Adventurer

Scope: per-Subzone (widens to Region only via `RankEscalation` in
`Zones/Zone_Library.yaml`). Fully passive/exploratory — no combat test gate,
unlike Mercenary/Strategy.

Score (0-100) is a weighted sum of four sources, defined in
`Ranks/Adventurer_Thresholds.yaml`:

| Source | Default Weight | Notes |
|---|---|---|
| `CharacterLevel` | 30 | Capped at the subzone's `LevelBand` ceiling — over-leveling contributes nothing, so it can't be used to trivialize a low band. |
| `HuntingLog` | 30 | % completion of that subzone's hunting log. |
| `Exploration` | 20 | % of the subzone map revealed. |
| `RegionEnhancement` | 20 | Progress on the Region's enhancement track (see below). If a Region declares no `Enhancement.TrackRef`, this weight redistributes proportionally across the other three for that Region only. |

Thresholds: Rank1 = 0 (always met), Rank2 = 40, Rank3 = 80.

### Region Enhancement — the active component

Each Region in `Zones/Zone_Library.yaml` declares one enhancement model under
`Enhancement:`. The model **varies per-Region** — pick whichever fits that
region's identity, not a single global choice:

```yaml
# Zones/Zone_Library.yaml, under a Region
Enhancement:
  Model: Relic        # or: Materia
  TrackRef: Enhancements.<Model>.<RegionName>
```

The referenced file lives in `Enhancements/` and follows one of two shapes:

**Relic model** — one evolving item, sequential steps, each step gated behind
a task in a specific subzone (FFXIV relic-weapon analog). Use when a region's
identity centers on a single narrative arc / heirloom item.

```yaml
Key: Enhancements.Relic.<RegionName>
Model: Relic
Region: <RegionName>
Steps:
  Step1: {Subzone: <name>, Task: "<description>", ItemStage: Item.Relic.<RegionName>.Stage1, ScoreContribution: <n>}
  Step2: {Subzone: <name>, Task: "<description>", ItemStage: Item.Relic.<RegionName>.Stage2, ScoreContribution: <n>}
MaxScoreContribution: <sum of steps> # must equal RegionEnhancement Weight (20 by default)
```

See `Enhancements/Relic.FanVillage.yaml` for the worked example.

**Materia model** — socketable gems earned in the region, slotted into any
gear; granular and incremental rather than one tracked item. Use when a
region's identity is about grinding/customization rather than a single arc.

```yaml
Key: Enhancements.Materia.<RegionName>
Model: Materia
Region: <RegionName>
GemTiers:
  Tier1: {Subzone: <name>, Source: "<how it drops/is earned>", ScorePerGem: <n>, MaxGemsCounted: <n>}
  Tier2: {Subzone: <name>, Source: "<how it drops/is earned>", ScorePerGem: <n>, MaxGemsCounted: <n>}
SocketSlotsPerGearPiece: <n>
MaxScoreContribution: <n>  # must equal RegionEnhancement Weight (20 by default)
```

No worked example authored yet — write one the first time a region actually
wants this model, rather than inventing a placeholder region for it.

### In-game guidebook

Each Region should get a `Guidebooks/Guidebook.Adventurer.RankUp.<RegionName>.yaml`
entry: a short in-world pop-up (`PopupTitle`/`PopupText`) shown on
`TriggerCondition` (default: `FirstEntryToRegion`), plus an optional
`WaypointNPC` pointing the player at a guide who can explain further. Leave
`WaypointNPC: null` until a real guide NPC exists for that region rather than
inventing one to fill the field — see `Guidebook.Adventurer.RankUp.FanVillage.yaml`.

## Mercenary

Scope: Account. Never adds potency — only kit breadth (skills, classes) and
how much of that kit survives an Area-Stage down-sync (`SyncRetention`,
defined in `Ranks/Mercenary_Unlocks.yaml`: 0.25/0.5/0.75 at Rank1/2/3).

### The SkillQuestGate

Before the broad Rank2/Rank3 test unlocks, the player must clear every
available skill quest (mini rank-test) for skills NOT granted by their
CURRENT class's normal level-up schema. "Reach the height of the current
class" = every such skill quest for *that* class cleared, not overall
account completion — switch class, and the gate re-evaluates against that
class's own skill quests.

Worked example: `Skills/Shield_Bash.yaml` is Adafold's Tank RoleMechanic
skill, gated behind `Quests/SkillQuest.Adafold.ShieldBash_Seq0.yaml` rather
than granted by leveling.

### RoleMechanic vs ClassMechanic

Defined in `Ranks/RoleMechanics.yaml` (per-Role, shared across every class in
that role) and `Classes/ClassMechanics.yaml` (per-Class, PLACEHOLDER —
class kits aren't finished):

| Role | RoleMechanic |
|---|---|
| Tank | Focus generation + Aggro management + Unfocus application — see `Combat/AggroSystem.yaml`. This IS the mechanic, not a separate bolt-on. |
| Healer | Healing output under genuine HP pressure — can't be exercised on demand, hence the different test shape below. |
| DPS | Maximum rotation uptime. No worked example yet. |

`Combat/AggroSystem.yaml` is the canonical Focus/Aggro contract:
`Aggro = Proximity + Focus + StrategyRankModifier` (weighted). If a
non-current-target's Aggro crosses `RankProfile.Doctrine.<Tier>
.FocusRedirectThreshold`, the enemy drops its cast and retargets — a genuine
self-interrupt, not a threat-table swap. Only Tanks can safely trigger this
on purpose; for anyone else it's a punishment. `Passives/Unfocus.yaml` lets a
Tank blunt an enemy's higher-Doctrine-tier skills specifically (not baseline)
while holding Aggro.

### The broad test (worked example: Tank)

Test fixture: `NPCs/Bosses/NPC.Boss.Test.MechaGolem.yaml`. Unlike Strategy
tests (below), Mercenary escalates by tiering `RankProfile.Doctrine` on ONE
reused NPC:

- **Rank2** (`Quests/Test.Mercenary.Rank2.Tank_Seq0.yaml`): forces Doctrine
  Level2 — a `RandomCastPool` of 3 skills, one randomly selected per attempt
  (tests adaptability, not memorization). Passing requires RoleMechanic use
  (Shield Bash), ClassMechanic use (Adafold's placeholder "Bulwark Gauge"),
  and correct cast-bar timing.
- **Rank3** (`Quests/Test.Mercenary.Rank3.Tank_Seq0.yaml`): forces Doctrine
  Level3, adding a `StabilityContest` — casting a `Tag.Skill.Risky` skill
  while the Golem is mid-cast instantly drops the player's own cast.

### The broad test (worked example: Healer)

`Quests/Test.Mercenary.Rank2.Healer_Seq0.yaml` is deliberately a different
shape, not a reskinned Golem fight: Phase1 requires sustaining buffs/damage
(no healing expected), Phase2 triggers on a genuine crisis
(`PartyHP <= 25% OR SelfHP <= 25%`) and grades whether the player can heal
decisively once it hits — because Healing can't be graded as a continuous
check for a role that spends most of an encounter not healing.

### Class advancement (Promoted / Special)

NOT listed under each rank's `Unlocks` — see `Classes/Class_Prerequisites.yaml`.
Base has no gate. Promoted requires a Base class at a level threshold + a
Role Quest + Mercenary Rank2. Special is a **separate track**, not built on
Promoted — its own quest + Mercenary Rank3. One worked example each
(Lancer, Dracomancer), both with forward-referenced quests that don't exist
yet.

## Strategy (player) / Doctrine (enemy)

Scope: Account. Player-facing name is Strategy (item gate + progression
indicator); enemy-facing name is Doctrine (AI pattern tiers) — see
`Ranks/Strategy_Unlocks.yaml`.

### Test encounter constraints

Strategy tests always draw from a Goblin/Flying-enemy pool — never a new
monster archetype per rank. Escalation works differently than Mercenary:
instead of tiering one NPC's Doctrine, Strategy tests **recombine** a small
set of building-block NPCs into a new layout per rank (different count,
arrangement, which building blocks appear).

### RoleToolBudget

Tanks are expected to need fewer of a test's provided tactical tools than
other roles, since their RoleMechanic (Focus/Aggro/mitigation) already
covers part of the job — and that gap widens at higher Strategy rank, since
more inherent tools unlock as rank rises.

### Worked example: Rank2

`NPCs/Bosses/NPC.Boss.Test.GoblinVanguard.yaml` (melee frontline, Doctrine
Level1 only — no tier escalation on this file, unlike the Mercenary fixture)
plus `NPCGroups/Group.Test.GoblinRangedCasters.yaml` (3 ranged AoE casters).
Run **solo** (`Quests/Test.Strategy.Rank2_Seq0.yaml`,
`SoloOnly: true`) specifically because a party's tank/healer would trivially
split this fight otherwise — the player must learn the toolkit themselves:

| Item | Effect |
|---|---|
| `Item.Tactical.Smokescreen` | Suppresses ranged targeting so the player can safely close on the Vanguard. |
| `Item.Tactical.Bombs` | Flat burst damage, any role. |
| `Item.Tactical.Traps` | Conditional immobilize — breaks free if cumulative damage on the target exceeds a small threshold, so committing real damage costs you the control. |

`RoleToolBudget` for this test: Tank expected to need at most 1 of the 3
tools, non-Tank expected to use all 3.

## Racial Summons exception

`Ranks/Rank_System.yaml` → `RacialSummonExemption`: a Summon with a
`RacialAttachment` field (`RaceKey` + `MercStratExempt: true`) bypasses
Mercenary/Strategy gating entirely, even though summons normally count as
"extra buttons" gated like Skills/Classes. Cross-referenced from both
`Mercenary_Unlocks.yaml` and `Strategy_Unlocks.yaml`.

Worked example: `Summons/Water_Slime.yaml`, unique to the "Lower Drakols"
race. Mechanically not a normal on/off summon — `PresenceType: Innate`
(present by default, no cast needed), with a `DismissTrigger`
(`Skills/GenerateWater.yaml`, a race-restricted AoE) that temporarily
dismisses it for a water-environment synergy; it returns on its own after
`ReturnAfterSeconds`. The Slime's presence suppresses
`Passives/DrySkin.yaml` (Fire damage-taken +15%, Speed -10) — dismissing it
removes that suppression for the window, which is the trade-off.

Note: the real race/Drakol lore this is based on lives in a text file on
the user's other PC, not in this repo — treat this section as a
from-scratch retelling, authoritative only until that original file
resurfaces.
