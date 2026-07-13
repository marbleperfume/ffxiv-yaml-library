# DESIGN_OVERRIDE.md
## Authoritative Combat & Class Philosophy — juice-yaml-library
### Overrides LLM.md where conflicts exist. This document wins.

---

## 1. Strategy Rank (Enemy AI Tiers)

Enemies have an innate **Strategy Rank** that determines their combat AI:

| Rank | Behavior | Example |
|------|----------|---------|
| 1 | Attack whoever's closest. No tactics. | Trash mobs, wildlife |
| 2 | Seek shortest open path to casters/squishies. Will try to path around blockers. | Dungeon elites, pack leaders |
| 3 | Flank, coordinate, retreat when low HP, target installations (summons). | Boss adds, veteran enemies |
| 4 | Call reinforcements, set ambushes, destroy deployables, exploit split parties. | Bosses, named NPCs |

> **Scale note:** Original LLM.md used 1-3. This document extends to 1-4 by splitting old Rank 3 (tactical) into Rank 3 (reactive tactics) and Rank 4 (proactive strategy). Review whether this split earns its keep or whether 1-3 is sufficient.

**Strategy Rank is NOT a difficulty slider.** It's an AI behavior set. A Rank 4 trash mob is weak but *smart* — it just dies fast when caught. A Rank 1 boss is strong but *dumb* — it hits hard but never flanks.

Higher-rank enemies demand strategy from the party. Lower-rank enemies can be brute-forced by clustering and hitting things.

---

## 2. Player Rank & Encounter Awareness

Player progression uses a **Rank system** (Rank = capability, gear = numbers):

| Player Rank | Expected Behavior | Design Target |
|-------------|-------------------|---------------|
| Low Rank (1-2) | Cluster together, execute basics, mash through encounters. | Viable and intended. Content clears. |
| Mercenary (3-4) | Understand encounter flow, make positioning decisions, build toward roles. | Branching paths become relevant. |
| Strategist (5+) | Actively reading encounters, splitting when advantageous, deploying summons/positioning tanks at chokepoints, managing resources across fight duration. | The full system sings here. |

**Critical design rule:** Low-rank clustering is VALID, not punished. The system rewards strategic play at higher ranks — it does not *require* it at lower ranks. A party of Rank 1 players stacking on each other and mashing will clear Rank 1 content. The complexity gradient is in the CONTENT, not gatekept by the controls.

---

## 2b. Rank 1 Content Design = FFXIV Normal (Intentional)

Rank 1 content explicitly mirrors FFXIV's Normal-difficulty dungeon/trial design:

- **Low dead time.** Enemies attack on rhythm. No variable pauses, no ambiguous tells. GCD rolls continuously.
- **Telegraphed danger.** Ground markers, cast bars, obvious wind-ups. "Don't stand in orange" is sufficient.
- **Cluster-valid.** Stack on tank, hit things, win. No positioning puzzle.
- **Linear combo reward.** Press 1-2-3, get payoff. No branching decisions required.
- **Forgiving GCD.** 2.0s base means input errors are recoverable. Single-weave only = no double-weave punishment.
- **No AI reading required.** Enemies at Strategy Rank 1 don't flank, don't prioritize, don't do anything clever.

**This is the intentional floor, not an accident.** FFXIV retains casuals because that floor *feels good* — smooth, rhythmic, rewarding without demanding mastery. The mistake is making the floor the ceiling.

The progression gradient FROM that floor:

| Rank | Feel | What the content adds |
|------|------|-----------------------|
| 1 | FFXIV Normal | Linear combos, telegraphed attacks, cluster-valid, no dead time |
| 2 | FFXIV Extreme | Enemies path toward squishies. Positionals appear. Tank is visibly working. |
| 3-4 (Merc) | Monster Hunter | Enemy tells are read, not telegraphed. Gauge decisions matter. Splitting becomes advantageous. |
| 5+ (Strat) | DRG Haz 5 | Procgen geometry matters. Summon placement matters. Every class axis engaged simultaneously. |

A Strategist running Rank 1 content still gets the smooth FFXIV flow — it just takes 30 seconds instead of 3 minutes. Complexity lives in the CONTENT demanding use of tools the class already provides, not in the controls themselves.

---

## 3. Dual-Tank Model (Force Targeting vs Unfocus)

There is NO enmity table. No "aggro number." Tanking is **spatial and cognitive.**

### Adafold — Force Targeting (Physical Compulsion)
- **How it works:** Adafold physically blocks paths, tethers enemies, pins them in place, body-blocks corridors. Enemies attack Adafold because they CANNOT PATH AROUND the shield.
- **Best in:** Corridors, chokepoints, escort scenarios, any geometry with limited paths.
- **Fantasy:** "I am the doorway. Nothing gets past."
- **Race lock:** Rawrotin (Linfree). Bodyguard/caretaker identity maps 1:1.

### Madolt Warrior — Unfocus (AI Suppression)
- **How it works:** Madolt's attacks apply Unfocus, which temporarily REDUCES an enemy's effective Strategy Rank. A Rank 3 enemy hit with Unfocus behaves like Rank 1 — mindlessly attacking the nearest target (Madolt, standing right there).
- **Best in:** Open areas, multiple approach routes, arenas where physical blocking is impossible.
- **Fantasy:** "I keep enemies stupid. They don't try to get past because I've suppressed their tactics."
- **Race lock:** None currently specified.

### Why two tanks?
Procgen maps generate BOTH corridor sections and open areas. Neither tank trivializes the other's terrain. A party with both covers all geometry. A party with one must adapt.

---

## 4. No Burst Cadence

**There is NO 2-minute cycle. No fixed burst window. No raid-alignment timer.**

Cooldowns exist for **use-case** reasons:
- "I'm entering a dangerous corridor" → press Overcharge
- "An elite just spawned" → deploy Bone Spirit
- "Party is taking lethal AoE" → Spirit Ascension for ground immunity

If a skill has a 90s cooldown, it's because **that skill would be degenerate at 30s** — not because it "aligns with party buffs every 180s."

**Party buffs do not stack multiplicatively on a shared timer.** Each class operates on its own resource economy. "Burst" happens when the situation demands it, not when a clock says so.

---

## 5. Tanks Operate Solo (At Higher Ranks)

At Mercenary+ content, the party may choose to split based on map geometry:
- Tank pushes a side corridor to clear flankers or escort an objective
- DPS + Healer handle the main path
- Shaman deploys summons at a junction to hold both lanes

**Tanks are self-sustaining.** They do not require healer attention to function. Healers are DPS until triage is needed.

At Low Rank, the party clusters. This is fine. The system doesn't force splits — it rewards them when the party is skilled enough.

---

## 6. Healers = DPS Until Not

Healers deal full DPS at low Strategy Rank content. Their healing kit is for **triage** — reactive intervention when things go wrong or when high-Rank enemies force sustained pressure.

A healer who never heals in a fight did their job correctly (the fight was easy enough). A healer who heals 100% of the time is in hard content. The design never forces "stand there and heal."

---

## 7. DPS = Different Games

Each DPS class is a fundamentally different **input experience**, not just "different buttons on the same hotbar":
- **Archer:** Free-aim, travel-time projectiles, shot arc, stealth, first-person ADS option
- **Elementalist:** 5-element Convergence stacks, cross-element consumption, mana refund loops (approved, Invoker-style)
- **Shaman:** Bone economy + curse uptime + summon positioning + overshield maintenance (4 axes)

The goal: each class feels like a different GENRE of game running on the same engine.

---

## 8. Summons Are Persistent Deployable Assets

Shaman summons (Bone Spirit, Floating Bone) are NOT disposable fire-and-forget pets:
- They have real HP pools (25% and 15% of Shaman max HP respectively)
- They persist until destroyed or dismissed — no arbitrary timer
- They can HOLD POSITIONS (Bone Spirit interrupts at a chokepoint, Floating Bone controls a zone with Hex stacks)
- Higher Strategy Rank enemies will target and destroy installations
- Destruction costs Bones to replace — the economic cost IS the punishment

**This creates asymmetric difficulty:** In low-rank content, summons persist forever (enemies ignore them). In high-rank content, summons get focused and Bone economy tightens.

---

## 9. >50% HP Rule

Players above 50% HP take **+25% incoming damage.** This:
- Pushes aggressive play (you WANT to hover around 50%, not sit at full)
- Makes chip damage relevant (you can't just ignore small hits)
- Creates a natural triage threshold for healers (heal to 50%, not to full)
- Rewards Shaman's overshield model (overshield doesn't count as HP for this rule)

---

## 10. Anti-Cheese for Ranged DPS

**Enemy movement + shot arc prevents extreme-range damage farming:**
- Enemies at Strategy Rank 2+ will advance on ranged attackers, not stand still
- Projectile arc means shots at extreme range are inaccurate / dodgeable by moving enemies
- Long-range attacks are eligible ONLY for CC (life-saving for team, repositioning tools)
- Actual damage must be dealt at medium range where risk exists

---

## 11. Race-Class Locks

| Class | Race Lock | Justification |
|-------|-----------|---------------|
| Adafold (Shield Knight) | Rawrotin (Linfree) | Bodyguard/caretaker society. "Mark and grind down" combat tradition. Physical protector identity. |
| Shaman | Soue (Wanderers) | Bone/spirit tradition developed in isolation within Soue's magic forest. Not adapted from other traditions. Players are always Soue. |
| Madolt Warrior | None | — |
| Elementalist | None | — |

**NPC exceptions exist** (adopted individuals, narrative edge cases) but are never available to players.

---

## 12. Gear & Progression (Unchanged from BalanceTargets)

- **Rank = capability** (what you can DO). Gear = numbers (how HARD you do it).
- 30-40% power gain fresh → BiS. Square-root diminishing returns above soft cap.
- No sync-down. Diminishing returns naturally keep old content from being trivialized.
- Weekly lockouts on gear, not on content access.

---

## 13. Procgen Maps (Non-Negotiable)

Maps are procedurally generated. This means:
- No memorizable scripted sequences (anti-parse-culture)
- Branching paths create strategic choices (split or cluster?)
- Corridor vs open-area geometry varies per run (both tank types stay relevant)
- Enemy placement varies (can't pre-plan cooldown usage to a timeline)
- Replayability is in the ENVIRONMENT, not in damage optimization (DRG model)

---

## 14. What This File Overrides in LLM.md

If LLM.md says any of the following, **this document takes priority:**

| LLM.md (old) | DESIGN_OVERRIDE (new) |
|--------------|----------------------|
| Enmity/aggro as a numeric table | Strategy Rank AI + Force/Unfocus dual model |
| Burst windows, buff alignment, 2-min cycle language | Use-case driven cooldowns, no cadence |
| "Focus/Unfocus" as aggro generation | Unfocus = AI suppression, Force = physical compulsion |
| Summons as disposable/timed | Summons as persistent HP-bearing assets |
| Any implication that party must split | Party CHOOSES to strategize; clustering is valid at low rank |
| Healer role = healing | Healer = DPS until triage |
| Ranged DPS can kite indefinitely | Anti-cheese: arc + enemy advance + CC-only at range |

---

*Last updated: 2026-07-12*
*Source conversation: FFXIV analysis → retention economics → 9-pillar framework → class design session*
