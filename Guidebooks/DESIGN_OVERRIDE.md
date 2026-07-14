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

> **Scale note:** Original LLM.md used 1-3. This document extends to **1-4** (confirmed). Old Rank 3 split into Rank 3 (reactive tactics) and Rank 4 (proactive strategy).

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

This is intentional and good. Rank 1 = the floor. Not everyone needs to engage with the full system. The game must feel GOOD at the floor.

---

## 3. NO 2-Minute Burst Cycle

This game has **no fixed burst cadence**. Classes are justified by their **use case**, not by their contribution to a party-wide synchronized damage window.

Anti-patterns (NEVER design these):
- Fixed-interval "burst windows" that must align with party buffs
- Grant chains (if you miss the window, the entire cycle is wasted)
- Gauge timers that force spending at a specific moment
- "Opener" sequences that only matter once per fight

Instead: Classes act when the SITUATION demands. Resources build through engagement and are spent when tactically optimal, not when a timer expires.

---

## 3b. Frontliner Identity (NOT "Tank")

**Madolt Warrior = Frontliner.** Primary identity is damage-first, survives by killing and parrying. NOT a traditional tank that absorbs for the party.

Two frontliner identities:
- **Adafold** = Force Targeting (physically compel enemies, facetank everything, dungeon escort king)
- **Madolt Warrior** = Unfocus suppression (keep enemies at lower Strategy Rank so they don't flank/target split party)

---

## 3c. Voltaic Parry (Madolt Warrior)

Skill-based survival mechanic:
- **Window:** 0.75s (League of Legends reaction standard, tentative — needs netcode testing)
- **Success:** 100% damage negation + 5% HP restore + 15 gauge + enables Voltaic Counter
- **Failure:** 0.6s recovery lockout (punished for misprediction)
- **Rank scaling:** Rank 1 = not needed (cluster with healer). Rank 2+ = primary survival when solo.

---

## 3d. Electromagnetic Suction / Capacitor Pull (Madolt Warrior)

Electron Guard stance mechanic:
- Enemies within **8y** pulled toward Madolt at **1.5y/s**. Cannot sprint away. Creates vortex with Unfocus.
- Rank 3+ enemies can dash/teleport to escape (costs them a CD)
- Rank 4 enemies recognize the field and retreat BEFORE entering
- Boss enemies: **0.5y/s** (drift, not lock)

---

## 3e. Rank 1 Frontliners Cluster with Healer

At Rank 1 content, the party stacks. Frontliners don't need to solo-survive because the healer is RIGHT THERE. Parry, suction, and Unfocus only become load-bearing at Rank 2+ where the party splits on procgen branching paths.

---

## 4. Procgen Maps = Party Splits

Non-negotiable design pillar. Maps procedurally generate branching paths that force separation:
- Not "stack on boss" MMO design
- Every path needs at least one frontliner
- Tanks operate solo (escort, pull, clear paths, self-sustaining without healer)
- Healers as DPS until party splits, then triage becomes real

---

## 5. Enmity = Spatial/Tactical (No Enmity Table)

**There is NO enmity table.** Enemies don't have a threat list. Enemy targeting is determined by:
- **Strategy Rank** (AI behavior set)
- **Physical blocking** (Force Targeting — Adafold stands in the way)
- **AI Suppression** (Unfocus — Madolt reduces enemy Strategy Rank)
- **Proximity and pathing** (enemies path toward valid targets)

---

## 6. Unfocus = AI Suppression

Unfocus is NOT damage reduction. It reduces enemy **Strategy Rank** by up to 2 tiers:
- A Rank 3 enemy under full Unfocus behaves as Rank 1 (attack closest, no flanking, no target priority)
- This makes enemies DUMBER, not weaker. They still hit hard.
- Spatial control through intelligence reduction, not through a threat meter.

---

## 7. Healers = DPS Until Not

Healers are self-sufficient damage dealers at low Strategy Rank content. Traditional healing only becomes necessary at high Strategy Rank where:
- Party splits on procgen paths (healer can't be everywhere)
- Rank 3+ enemies deal enough damage that self-sustain isn't sufficient
- Multiple simultaneous threats overload individual survivability

---

## 8. DPS = Different Games

Each DPS class is a fundamentally different INPUT EXPERIENCE:
- **Archer:** Free-aim, stealth, travel-time projectiles, shot arc. Not just "different buttons."
- **Shaman:** Deployment, curse management, bone economy, spatial installations.
- **Strix:** Altitude as resource, pre-calculation from above, committed dive trajectory.
- **Reaver:** Instinct-reading (no gauges), pursuit commitment, can't disengage once engaged.

The goal is that switching classes feels like switching GAMES, not switching hotbars.

---

## 9. >50% HP Rule — ENEMIES, Not Players (CORRECTED)

**Enemies above 50% HP take +25% incoming damage from players.**

This accelerates the first half of enemy health bars. The fight "opens fast" then slows as enemies enter danger zone. Creates natural pacing without scripted phases.

> **CORRECTION:** Previous versions applied this to PLAYERS taking incoming damage. That is WRONG. It applies to ENEMIES receiving damage.

---

## 10. Classes ≠ Races (Unless Specified)

A class is not automatically tied to a race. Racial locks exist only where:
- **Biological lock:** The race's BODY is the mechanic (Grappler = tentacles, Strix = wings)
- **Cultural lock:** The race's TRADITION is the knowledge (Shaman = Soue spiritual tradition)

All other classes are available to multiple races with potential racial variants (same class name, different execution emphasis per race).

---

## 11. Anti-Cheese for Ranged

Enemy movement + shot arc prevents extreme-range sniping:
- Long range eligible ONLY for CC (life-saving for team), not damage farming
- Enemies close distance. Maps have corridors. Elevation doesn't create permanent safety.
- The game is about ENGAGEMENT, not about finding a perch and never being threatened.

---

## 12. Crit is NOT RNG

Crit is **positional/conditional** — never random:
- Backstab/flank position
- Attacking CC'd targets
- Hitting enemies above 50% HP (interaction with §9)
- Class-specific conditions (Reaver: rhythmic timing, Strix: altitude threshold)

This means crit is a SKILL EXPRESSION, not a slot machine.

---

## 13. Three Axes of Enemy Impairment

Distinct, stackable, different classes specialize:

| Axis | Effect | Primary Class |
|------|--------|---------------|
| **Unfocus** | Reduce Strategy Rank (AI behavior) | Madolt Warrior |
| **Accuracy Debuffs** | Reduce hit rate (physical miss) | Shaman, consumables |
| **Darkness** | Reduce vision distance (detection range) | Nightmare |

---

## 14. What This File Overrides in LLM.md

| LLM.md Says | This File Says |
|-------------|----------------|
| Enmity/aggro system | No enmity table. Spatial + AI rank targeting. |
| 2-minute burst cycle | No fixed cadence. Use-case justified. |
| Tank absorbs for party | Frontliner (damage-first, parry-based survival) |
| Strategy Rank 1-3 | Strategy Rank 1-4 (confirmed) |
| >50% HP rule on players | >50% HP rule on ENEMIES (corrected) |
| Rank 1 enemies flank/seek | Rank 1 = FFXIV Normal. No flanking. Clusters with healer |
| Strategy Rank 1-3 | Strategy Rank 1-4 (confirmed) |
| Enemies stay at range if not aggro'd | Capacitor Pull (suction) forces enemies into melee via Electron Guard field |

---

<!-- ▼ CONTINUES IN: DESIGN_OVERRIDE_SYSTEMS.md -->
<!-- ▼ System-level rules (MAG/MED, SPD, CC immunity, water systems, file structure) start there -->

*Last updated: 2026-07-14*
