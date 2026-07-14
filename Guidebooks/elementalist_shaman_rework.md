# Elementalist & Shaman — Item-First Redesign
## Stripping the 2-Minute Rotation Bias, Rebuilding from Strategic Demand

> **Governing Documents:** DESIGN_OVERRIDE.md (wins all conflicts), Game_Juice_Taste_Design.md (hierarchy), class_item_baselines.md (item floor)
>
> **Core Mandate:** These classes respond to STRATEGIC PROBLEMS (Position × Action × Time). They do not follow rotations. They do not have burst windows. Every action is triggered by something happening in the encounter — not by an internal timer completing.

---
---

## Elementalist — Item-First Redesign

### Design Philosophy Change

#### What Was Wrong With the Old Design

The previous Elementalist YAML (Elementalist_Complete.yaml) carried multiple rotation-cadence assumptions despite explicitly trying to avoid them:

1. **Convergence as build→spend on a timer.** The 5-element stack system created implicit "fill 4 stacks → Converge → use modifier" loops. Players optimized this into a fixed rotation: Fire-Fire-Fire-Converge(Fire)-Water-Converge(Water)-Wind... This IS a burst cadence — the Convergence moment becomes the "burst window" and players solve for the fastest stack-fill cycle.

2. **Prominence combo condition.** "Previous 2 GCDs were Fire element skills" is a ROTATION SEQUENCE REQUIREMENT. It tells the player: cast Fire → Fire → Prominence. That's a 1-2-3 combo, which is a fixed order.

3. **Mana recovery as cyclical pressure.** The sustain loop (build 4 stacks → consume → net +800 mana) creates a fixed economic cycle. Players optimize the RATE at which they execute this cycle, producing a predictable mana oscillation that maps to ~20-30s micro-rotations.

4. **Element identity collapse.** On flat geometry with no environmental demands, Fire dominates (highest raw potency, cheapest mana). The old design acknowledged this ("fire degeneration on flat maps") but treated it as a level design problem rather than a class design problem. Both must be solved.

5. **Healing as a "mode switch."** "DPS until someone needs healing → pivot to Water" is reactive in concept but creates two rotation states: DPS rotation and Heal rotation. The player still has two memorized sequences and switches between them.

#### What the New Design Is Built Around

- **Responding to encounter pressure.** Every element has a TRIGGER — an external condition that makes switching correct. No element is "default."
- **Items define the baseline.** Firebomb, Antarctic Wind, Rejuvenation Flask, Upheaval Flask, Conductance Gel, Voidpatch Emitter — these set the floor. The Elementalist replaces them permanently with adaptive, scaling, persistent solutions.
- **The class replaces items, not rotation.** A party without an Elementalist carries 6-8 elemental consumables per run. The Elementalist IS those consumables — available on demand, unlimited uses, contextually superior.
- **Vulnerability through element depletion, not cooldowns.** Using Water for healing means you can't freeze enemies. Using Earth for CC means you can't shield. The vulnerability is STRATEGIC (I chose wrong, or I was forced into a bad trade) not TEMPORAL (my cooldown is ticking down).

---

### Trigger System (Replaces Rotation)

Instead of "cast Fire × 3 → Converge → switch element → repeat," the Elementalist responds to:

| Trigger Condition | Element Response | Why This Over Items |
|---|---|---|
| **Enemy charging / closing distance** | Ice (freeze terrain in path, apply root) | Frostweave Net is single-use, positional. Ice terrain persists. |
| **Enemy casting (interrupt needed)** | Earth (stun/interrupt via petrification) | Stupor Bell is single-use. Earth petrify is repeatable, scales with stacks. |
| **Party HP dropping (Triage Minor: ally ≤50%)** | Water (reactive AoE heal, terrain-based recovery zone) | Rejuvenation Flask heals 20% once. Water heals adaptively, terrain lingers. |
| **Multiple enemies clustered** | Wind (AoE scatter + damage conversion) | Concussion Charge has 2s delay. Wind displacement is instant, repeatable. |
| **Enemy resistant to current element** | Switch to exploitable weakness | Gold Pine Resin is pre-committed to one element. Elementalist reads and adapts. |
| **Terrain disadvantage (poison field, lava, etc.)** | Earth transmutation (convert enemy terrain to neutral/allied) | Voidpatch Emitter removes terrain. Elementalist CONVERTS it. |
| **Boss above 50% HP (+25% damage taken)** | Fire (capitalize on vulnerability window with pure damage) | Items provide flat damage. Elementalist scales fire output with encounter knowledge. |
| **Boss below 50% HP (damage resistance phase)** | Shift to utility/CC/healing — damage is less efficient now | Items don't adapt to phase shifts. Elementalist reads HP and adjusts. |
| **Mana depletion (below 30%)** | Light (cheapest sustained output, barrier-focused, recovery posture) | No item equivalent — this is the class's internal pressure state. |
| **Ally under focused fire (needs shielding)** | Light barrier → Earth wall → Fire zone denial (layered response) | Shield Generator is one-use ultimate defense. Elementalist provides layered defenses of varying cost. |

**The critical difference:** In the old system, the player asked "what's next in my rotation?" In the new system, the player asks "what is the encounter DEMANDING right now?"

---

### Core Mechanic Redesign — Elemental Attunement (Replaces Convergence Stacks)

#### The Problem With Convergence Stacks

The old system (5 independent counters, build → consume cross-element) was clever mechanically but produced a solvable optimization loop. Players would derive the mathematically optimal consumption pattern and execute it on repeat. That's a rotation.

#### The New System: Elemental Saturation

**Concept:** The Elementalist doesn't "build stacks to spend." Instead, casting an element saturates the local magical field with that element. Saturation creates PASSIVE ENVIRONMENTAL EFFECTS that persist as long as the Elementalist maintains that element's presence. Switching elements causes the previous saturation to FADE (over 4-6s), during which the old element's passive effect weakens and the new one strengthens.

**Why this eliminates rotation:**
- There is no "spend" moment. There is no "burst" from consumption.
- The decision is: WHICH element do I maintain NOW? What passive effect does the encounter need?
- Switching has a transition cost (4-6s of weakened output while fields shift) — this IS the vulnerability window.

#### Saturation Effects (Passive, Persistent While Maintained)

| Element | Saturation Effect (Passive While Active) | Fade Penalty (4-6s During Transition) |
|---|---|---|
| **Fire** | Enemies in 15y take ambient burn damage (low potency DoT). Terrain inside 15y becomes "heated" — enemies move 10% slower through it. | Burn damage stops immediately. Heated terrain cools over 6s. |
| **Water** | Allies in 15y regenerate HP (low sustained regen). "Moist" terrain makes ice abilities instant-root instead of slow. | Regen ticks stop. Moist terrain dries over 4s. |
| **Earth** | Allies in 15y gain a damage absorption buffer (thin persistent shield that regenerates every 8s). Ground becomes "dense" — enemies are Heavy (move speed -20%). | Shield stops regenerating. Dense terrain softens over 6s. |
| **Wind** | All allies in 15y gain +15% movement speed. Projectiles aimed at allies have 20% miss chance (wind deflection). | Speed bonus fades. Deflection drops over 4s. |
| **Light** | All allies in 15y gain conditional crit (next action after dodging an attack is guaranteed crit — positional/conditional, NOT RNG). Vision radius +5y for the party. | Crit condition removed. Vision bonus fades. |

**The player's moment-to-moment decision:** "Fire saturation is giving me ambient damage, but the boss just targeted our backline and they need Water regen. Do I switch NOW (losing fire pressure for 6s) or trust their potions for one more cast cycle?"

#### Mana Economy (Encounter-Driven, Not Cyclical)

**Old problem:** Build stacks → consume → refund mana → repeat. Fixed cycle.

**New model:** Each element has a MAINTENANCE COST. Heavier elements cost more mana per second to sustain their saturation field.

| Element | Maintenance Cost/s | Why |
|---|---|---|
| Fire | 80 mana/s | Pure offense should drain fastest — forces eventual switching |
| Water | 100 mana/s | Healing is expensive. Can't sustain Water forever. |
| Earth | 60 mana/s | Defensive posture is more sustainable — intended safe harbor |
| Wind | 50 mana/s | Utility/mobility is cheapest — the transition element |
| Light | 40 mana/s | Recovery posture. Weakest output, most sustainable. When you're low. |

**Recovery mechanic:** Mana regenerates at base rate (67/s) PLUS bonus regen when you AREN'T maintaining any saturation (neutral state). Neutral state = no passive effects, basic attacks only, mana recovery at 3× rate. This is the vulnerability window — you're regenerating but providing NOTHING to the encounter.

**Strategic implication:** An Elementalist who maintains Fire too long will run dry and be forced into neutral state (total vulnerability). An Elementalist who alternates between expensive elements (Fire → Water → Fire) will exhaust faster than one who uses Wind/Earth as breathing room. The encounter's demands — not an internal timer — determine when you switch and how fast you drain.

---

### Ability Framework (16 Abilities, Organized by Response Trigger)

#### Response to: Enemy Aggression / Charges

| # | Name | Trigger Condition | Replaces (Item Baseline) | CC Stage | Decision Created |
|---|---|---|---|---|---|
| 1 | **Glacier Wall** | Enemy within 10y and closing on ally | Quartzwall Capsule (barrier) + Frostweave Net (slow) | Stage 1 (root in ice) | Costs Water saturation — if you're in Fire mode, switching means 6s transition AND losing Fire damage aura. Do you wall now or let the frontliner handle it? |
| 2 | **Scorch Line** | Enemy crossing an approach corridor | Firebomb (area damage) | Stage 1 (slow via heated terrain) | Creates fire terrain that persists 12s. Enemies won't cross willingly. But if the PARTY needs to retreat through that corridor, they take burn too. Placement matters. |
| 3 | **Petrify** | Enemy mid-cast (interruptible) or mid-charge | Stupor Bell (single interrupt) | Stage 3 (stun, 2-3s) | HIGH mana cost, instant cast. Using this when Earth isn't your active element costs DOUBLE mana (out-of-saturation penalty). Do you eat the cost or let the cast go through? |

#### Response to: Party HP Drop / Damage Spike

| # | Name | Trigger Condition | Replaces (Item Baseline) | CC Stage | Decision Created |
|---|---|---|---|---|---|
| 4 | **Tidal Basin** | Triage Minor triggered (ally ≤50% HP within 30y) | Healing Specter (zone heal) + Rejuvenation Flask (burst) | None (healing) | Ground-targeted water zone (6y radius). Allies standing inside heal rapidly. BUT: you must PLACE it correctly. If the fight moves, the zone is wasted. Costs a GCD + forces Water saturation if not already active. |
| 5 | **Cleansing Rain** | Ally has debuff OR Triage Over triggered | Harmony Draught (regen) + debuff cleanse item | None (heal + cleanse) | oGCD, instant. Heals one target + removes one debuff. 2 charges, 25s per charge. Your "free" healing — use these FIRST before committing GCDs to Water. Using both charges means you're out of emergency responses for 25s. |
| 6 | **Aqua Veil** | Predictable damage incoming (boss wind-up visible) | Water Shield (barrier) | None (barrier) | Proactive barrier on one ally. If you mispredict WHO gets hit, the barrier is wasted. 30s cooldown — misjudging costs you the only proactive tool for half a minute. |

#### Response to: Map Geometry Challenge

| # | Name | Trigger Condition | Replaces (Item Baseline) | CC Stage | Decision Created |
|---|---|---|---|---|---|
| 7 | **Earthen Bridge** | Gap/elevation the party cannot cross normally | Springboard Disc (vertical access) + Brineshelf Compound (platform) | None (terrain creation) | Creates a stone ramp/bridge (6y long). Persists 30s. Costs Earth saturation + a GCD. If enemies use your bridge too, you've given them access to the party's high ground. |
| 8 | **Gale Corridor** | Party needs to reposition quickly through narrow space | Flashstep Cartridge (gap close) | None (utility) | Wind tunnel in a line — allies inside move at 2× speed for 4s. Enemies inside are pushed backward (Stage 1 displacement). Brief, directional. If you aim wrong, nothing happens and you've spent the GCD. |
| 9 | **Terrain Transmute** | Enemy terrain hazard (poison pool, lava, ice patch) blocking party | Voidpatch Emitter (nullify terrain) | None (terrain conversion) | Converts a 4y radius of enemy terrain into ALLIED terrain (poison → healing zone, lava → stone platform, ice → water for saturation bonus). Unique class function — no item converts, only removes. 20s cooldown. The transmuted terrain lasts 15s. |

#### Response to: Resource Depletion

| # | Name | Trigger Condition | Replaces (Item Baseline) | CC Stage | Decision Created |
|---|---|---|---|---|---|
| 10 | **Meditation (Neutral Stance)** | Mana below 20% OR no immediate encounter pressure | No item equivalent (this is the class's recovery state) | None | Drop all saturation → 3× mana regen. You provide NOTHING to the party during this. No passive effects, no ambient damage, no regen aura. If an emergency happens while meditating, you must restart from zero saturation. The timing of when to meditate IS the skill expression. |
| 11 | **Elemental Recycling** | Transition between elements (passive) | No item equivalent | None | During the 4-6s fade transition, the departing element provides one final "burst" effect at reduced power: Fire departure = one last AoE tick, Water departure = one last heal tick, etc. This rewards PLANNED transitions over panic switches. |

#### Response to: Multiple Simultaneous Threats

| # | Name | Trigger Condition | Replaces (Item Baseline) | CC Stage | Decision Created |
|---|---|---|---|---|---|
| 12 | **Convergence Burst** | 3+ enemies clustered AND party under pressure (compound threat) | Antarctic Wind (AoE ice) + Upheaval Flask (AoE displacement) combined | Stage 2 (stagger/interrupt all targets) | The "ultimate." Requires being in ACTIVE saturation (any element). Detonates current saturation for massive AoE effect: Fire = explosion, Water = tidal wave heal, Earth = quake displacement, Wind = tornado scatter, Light = blind flash. EMPTIES your mana by 50%. You will need to Meditate soon after. This is the "I solved the problem but now I'm vulnerable" button. |
| 13 | **Elemental Chain** | Allied Elementalist or fire-element class present, OR enemy affected by elemental debuff | Dragon's Dream (combo setup) + Conductance Gel (vulnerability) | Varies by element used | Your cast "detonates" an existing elemental debuff on a target for bonus damage. Oil + your Fire = explosion. Your Ice + ally Lightning = Superconductor. This is the Layer 3 Chain Reaction system — rewards composition diversity but isn't mandatory. |

#### Core DPS Abilities (Element-Specific Damage)

| # | Name | Element | Notes |
|---|---|---|---|
| 14 | **Fireball** | Fire | 1.5s cast, baseline DPS filler while in Fire saturation. Potency adjusted for STR 6/STAM 6 Tryll baseline (+15% magic potency racial to compensate). |
| 15 | **Stone Spike** | Earth | Instant cast, lower potency than Fireball but usable while moving. Applies "Heavy" to target (Stage 1 slow) for 8s. |
| 16 | **Gale Blade** | Wind | Instant cast, lowest potency, but extends Wind saturation duration by 2s per cast (efficiency tool). Enables sustained kiting patterns. |

---

### Vulnerability Windows

The Elementalist is NOT overpowered because:

1. **Saturation Transition (4-6s).** Every time you switch elements to address a new problem, you spend 4-6s at reduced effectiveness. If two problems arise simultaneously (enemies charge AND party HP drops), you cannot address both instantly — you must triage.

2. **Mana Depletion → Forced Neutral State.** Aggressive element use (Fire + Water cycling) drains mana rapidly. When depleted, you're useless for 10-15s while regenerating. A Shaman or Siren doesn't have this vulnerability — they can operate at reduced capacity indefinitely.

3. **STR 6 / STAM 6 (Tryll racial).** Physically fragile. Cannot self-heal efficiently (Water heals allies, not self). Relies on party positioning, Earth shields, and avoiding damage entirely. Getting caught in melee is near-death.

4. **No sustained single-element dominance.** Fire has the highest DPS maintenance cost (80 mana/s). Staying in Fire for more than ~30s without switching requires sacrificing future flexibility. The encounter will punish fire-only play.

5. **Strategic depletion.** Using Water for healing means you CAN'T freeze the next charging enemy. Using Earth for CC means your party loses the persistent shield. Every response to one problem creates vulnerability to the NEXT problem. Good Elementalists solve problems in an order that minimizes cascading vulnerability.

---

### Healer Identity Distinction

**Elementalist heals through WATER TERRAIN.** The healing is positional and reactive:
- Tidal Basin creates a ZONE. Allies must stand in it.
- Cleansing Rain is the emergency oGCD (limited charges).
- Water Saturation provides ambient regen (passive, low, persistent).
- The Elementalist cannot efficiently heal themselves (Water heals ALLIES in the saturation field; the Elementalist is the source, not the recipient).

**Item Baseline for Elementalist Healing:**
- Rejuvenation Flask (20% HP burst, 2y AoE, single-use) → Elementalist provides repeatable zone healing that persists.
- Healing Specter (zone heal, 15s duration) → Elementalist's Tidal Basin is stronger but costs saturation commitment.
- Harmony Draught (3% HP/s, 12s, ally-consumed) → Water Saturation provides ~2% HP/s to all nearby allies, no ally action required.

**What makes it worse than dedicated healers:** Limited charges on oGCD heal. Zone requirement means immobile allies don't benefit. Mana competition between healing (Water) and DPS (Fire) means healing degrades offensive output significantly. Cannot burst-heal above Triage Minor without entering Triage Over (max mana dump → forced Meditation afterward).

---

### Anti-Patterns (What This Class Does NOT Do)

- ❌ **No fixed burst windows.** Convergence Burst is emergency-only, not a timed payoff.
- ❌ **No "build to X stacks then spend" on a timer.** Saturation is maintained, not accumulated-and-detonated.
- ❌ **No rotation order.** There is no "Fire → Water → Earth → Wind → Light → repeat." Element choice responds to encounter state.
- ❌ **No party-buff-alignment dependency.** Saturation effects are LOCAL and PASSIVE. They don't "align" with other players' burst windows.
- ❌ **No Freecure.** No RNG proc that rewards casting wrong elements. Healing is deliberate and costly.
- ❌ **No "stay in Fire forever" optimization.** Fire maintenance cost (80 mana/s) ensures Fire-only play runs dry in ~60s. Map geometry and encounter design punish mono-element.
- ❌ **No Prominence-style combo sequences.** No ability requires "cast X then Y then Z in order."

---

### How Items Complement (Not Compete)

Even WITH an Elementalist in the party, these items retain value:

| Item | Why It Still Matters |
|---|---|
| **Conductance Gel** (+40% lightning vuln) | Elementalist has no Lightning element. This enables Chain Reaction combos that the Elementalist can DETONATE but not PRIME alone. |
| **Gold Pine Resin** (elemental weapon coating) | Applies to MELEE characters. The Elementalist amplifies the party's elemental diversity but doesn't coat weapons. Melee + coating + Elementalist detonation = team synergy. |
| **Voidpatch Emitter** (terrain removal) | Elementalist CONVERTS terrain (into allied). Sometimes you want terrain GONE entirely (no lingering effects). Different strategic choice. |
| **Stasis Pin** (3s total freeze, Stage 3) | Elementalist's Petrify is 2-3s and costs heavy mana. Stasis Pin is free (consumable budget, not mana). In mana-starved states, items carry the CC load. |
| **Firebomb** (AoE fire, single-use) | When the Elementalist is in Neutral State (recovering mana), ANY party member can throw a Firebomb to maintain fire terrain. The class isn't the ONLY source — just the best one. |
| **Premium crafted items** (rare drops) | "Inferno Orb" (hypothetical rare) might create fire terrain that ALSO applies vulnerability. Better than what the Elementalist can produce for 15s. Worth using even with the class present. |

---

### CC Stage Budget

| Ability | CC Stage | Notes |
|---|---|---|
| Glacier Wall | Stage 1 (Root in ice) | Root broken by taking damage. Brief immobilization. |
| Scorch Line | Stage 1 (Slow via heated terrain) | Terrain-based, avoidable by pathing around. |
| Stone Spike (passive) | Stage 1 (Heavy / slow) | Attached to basic attack. Low impact, high uptime. |
| Petrify | **Stage 3** (Stun, 2-3s) | HIGH mana cost. Out-of-element penalty if Earth isn't active. DR on repeated use. |
| Convergence Burst (Earth) | Stage 2 (Stagger/interrupt) | AoE interrupt only when Earth is active saturation. |
| Convergence Burst (Light) | Stage 2 (Flash Blind, 2s) | AoE blind only when Light is active saturation. |
| Gale Corridor | Stage 1 (Displacement/pushback) | Pushes enemies back through wind. Does not stun or disable. |

**Budget Assessment:** The Elementalist has ONE reliable Stage 3 CC (Petrify) at very high cost. Stage 2 is situational (only via Convergence Burst, which is the mana-expensive ultimate). Stage 1 is plentiful (terrain effects, slows, roots). This is appropriate for a healer/DPS hybrid — strong in soft control, limited in hard disable, and the hard disable has steep opportunity cost.

---
---

## Shaman — Item-First Redesign

### Design Philosophy Change

#### What Was Wrong With the Old Design

The Shaman_Complete.yaml exhibited rotation-cadence assumptions despite conscious efforts to avoid them:

1. **"Build Hex stacks → Curse Explosion → stacks reset → Floating Bone re-applies → repeat."** This is a burst cadence. The accumulation phase (5-25s depending on Floating Bone placement) followed by the explosion (consuming all stacks) followed by rebuild IS a cycle. Players solve for optimal stack-count-to-detonate and execute that cycle on repeat.

2. **"Setup phase → payoff phase" via Bone deployment.** Deploy Bone Spirit + Floating Bone at fight start = setup phase (reduced DPS while summoning). Then all tools online = payoff phase (full DPS + overshield). This creates a predictable power ramp at fight initiation.

3. **Spirit Ascension as timed invulnerability burst.** The YAML notes it's "use-case driven," but the 25s enhanced duration with Invocation creates a window that players will optimize around: "save Spirit Ascension for boss phase 2" becomes a burst cadence aligned to encounter scripting.

4. **Bone Harvest on 60s cooldown = fixed resource cadence.** Every 60s you get 2 Bones. This creates economic cycles: 0-60s = spend initial stock, 60-120s = first resupply, etc. Players optimize deployment timing around this clock.

5. **Hex Drain as passive overshield generation.** Because Hex Drain converts to overshield while Hex stacks persist, the optimal play is: maintain 5 stacks forever → Mastema for damage (doesn't consume) → Hex Drain for overshield → never Curse Explode. This collapses the "explosion vs. maintenance" decision into "always maintain."

#### What the New Design Is Built Around

- **Responding to MAP GEOMETRY and ENEMY BEHAVIOR.** Bone deployments respond to spatial problems (corridors to hold, zones to deny). Curses respond to enemy actions (it's casting, slow it; it's flanking, cripple it).
- **Hex Drain as REAL-TIME cost/benefit decision.** Maintaining curses = maximum debuff on enemies (damage amp, slow, etc.). Draining curses = healing the party. These are MUTUALLY EXCLUSIVE at any given moment. The encounter determines which matters more RIGHT NOW.
- **Items define baseline.** Witherfield Totem, Scatterlung Phial, Hollowform Decoy, Lockjaw Spore — the Shaman replaces this ENTIRE debuff/CC item catalog as a persistent, scaling, adaptive solution.
- **MonsterBone as strategic resource with meaningful depletion.** Bones aren't a rotation clock — they're a BUDGET for the entire run. Spending one is a commitment. Losing a summon to enemy destruction is a meaningful setback, not a routine re-deploy.

---

### Trigger System (Replaces Rotation)

Instead of "deploy → build Hex → explode → rebuild," the Shaman responds to:

| Trigger Condition | Response | Why This Over Items |
|---|---|---|
| **Enemy begins casting** | Bone Spirit auto-interrupt (if deployed at that chokepoint) OR direct interrupt curse | Stupor Bell is single-use. Bone Spirit interrupts every 10s, permanently. |
| **Enemy closing on backline (SR2+ pathing to squishies)** | Apply speed curse directly via Effigy targeting | Thickglass Flask creates a puddle enemies walk out of. Speed curse FOLLOWS the target. |
| **New corridor/room entered (map geometry changes)** | Reposition Floating Bone to new chokepoint; consider Bone Spirit redeployment | Witherfield Totem is single-use, 25s duration, destroyable. Floating Bone is persistent, re-positionable for free. |
| **Multiple enemies spawning simultaneously** | Dark Theurgy (AoE Hex application) + Floating Bone positioned to catch spawn | Lockjaw Spore covers 3m for 15s. Floating Bone covers 10y indefinitely. |
| **Party HP dropping (Triage Minor triggered)** | Hex Drain: DRAIN current curses from enemies, convert to party overshield/healing | Rejuvenation Flask heals once. Hex Drain heals proportional to curse intensity — rewards aggressive curse upkeep. |
| **SR3+ enemies targeting installations** | Reposition summons (GCD cost, no Bone cost) OR accept destruction + budget a re-deploy | No item equivalent — items don't get "targeted" because they expire before enemies react. Shaman's persistent assets create a NEW problem space. |
| **Boss entering dangerous phase (visible wind-up)** | Spirit Ascension (ground immunity + damage amp) — the "this phase is lethal, I need airborne safety" | No item provides total AoE immunity while maintaining offense. |
| **Bone reserves low (≤2 remaining)** | Prioritize curse maintenance via Effigy (free) over summon deployment. Accept reduced zone control. | MonsterBone depletion has no item analog — it's the class's unique pressure state. |
| **Boss above 50% HP (+25% damage bonus)** | Maintain max Hex stacks for damage amplification (+25% from Hex × +25% from >50% rule = massive damage) | Items can't provide sustained +25% damage amp. Hex stacks are the class's premium damage amplifier. |
| **Ally needs emergency heal, no dedicated healer available** | SACRIFICE Hex stacks via drain (lose damage amp on enemy) to generate healing/overshield for party | No item does "I give up my damage buff to heal the team." This is the Shaman's unique role tension. |

---

### Core Mechanic Redesign — Hex System as Cost/Benefit Tension

#### The Problem With the Old Hex System

The old system made Hex stacks purely beneficial to maintain: +5/10/15/20/25% damage amp at 1-5 stacks, PLUS enabling Hex Drain for overshield, PLUS Curse Explosion for burst. There was no COST to maintaining stacks. The optimal play was always "keep stacks at 5."

#### The New System: Hex as Dual-State Resource

**Concept:** Hex stacks exist in two states — **Invested** (stacks remain on enemy, providing passive debuffs and damage amp) and **Harvested** (stacks consumed to generate healing/overshield). These states are mutually exclusive AT ANY MOMENT. Maintaining Hex = enemy gets weaker. Harvesting Hex = your party gets healed. You cannot have both simultaneously.

**Hex Stack Effects (While Invested/Maintained):**

| Stacks | Enemy Debuff | Shaman Damage Amp |
|---|---|---|
| 1 | -5% accuracy (Impairment Axis: Accuracy) | +5% Shaman damage to target |
| 2 | -10% accuracy, -10% move speed | +10% Shaman damage to target |
| 3 | -15% accuracy, -15% move speed, -10% attack speed | +15% Shaman damage to target |
| 4 | -20% accuracy, -20% move speed, -15% attack speed | +20% Shaman damage to target |
| 5 | -25% accuracy, -25% move speed, -20% attack speed, 10% action skip chance | +25% Shaman damage to target |

**Hex Drain (Harvesting):**

When you Harvest Hex stacks, you LOSE the debuffs on the enemy (they return to full accuracy/speed) in exchange for healing output proportional to stacks consumed:

- 1 stack harvested = 150 HP restored to lowest ally
- 3 stacks harvested = 450 HP + overshield (150 HP buffer)
- 5 stacks harvested = 750 HP + overshield (300 HP buffer) + cleanse 1 debuff from target ally

**The decision at every moment:** "This enemy has 5 Hex stacks. They're -25% accuracy, -25% speed, basically neutered. My tank is at 55% HP. Do I HARVEST those stacks to heal (losing all debuffs on this enemy, who becomes dangerous again) or MAINTAIN them (keeping the enemy weak but letting my tank stay at 55%)?"

**This IS the class.** No rotation answers this. Only encounter reading does.

#### Bone Deployment as Spatial Response (Not Setup Phase)

**Old problem:** Deploy at fight start → summons persist → fight occurs around them. The deployment was a pre-fight setup, not a mid-fight decision.

**New model:** Bone deployment responds to MAP GEOMETRY CHANGES during the encounter.

- **Room transition:** Party enters new room → Shaman reads the geometry → places Floating Bone at the optimal chokepoint.
- **Enemy spawn change:** New wave spawns from a different direction → Reposition Floating Bone (free GCD) to cover new approach.
- **Boss phase transition:** Boss moves to new arena section → Bone Spirit repositioned to new interrupt-critical location.
- **Party split:** Party splits at a branch → Shaman deploys Bone Spirit at one corridor, stays with the other group. Bone Spirit holds that position independently.

**The deployment ISN'T "setup."** It's continuous spatial adaptation. The Shaman who places Bone Spirit at the start and never moves it is playing like it's a rotation. The Shaman who repositions 3-4 times per encounter based on geometry shifts is playing correctly.

---

### Ability Framework (16 Abilities, Organized by Response Trigger)

#### Response to: Enemy Aggression / Dangerous Actions

| # | Name | Trigger Condition | Replaces (Item Baseline) | CC Stage | Decision Created |
|---|---|---|---|---|---|
| 1 | **Effigy** | Enemy acting aggressively (default filler, but contextual: apply Hex to the most dangerous target) | Scatterlung Phial (accuracy debuff) | None (debuff via Hex) | Instant GCD. Applies 1 Hex stack. Do you Hex the most dangerous enemy (building toward neutering them) or spread Hex across multiple targets (enabling multi-target Drain later)? Target selection IS the decision. |
| 2 | **Nerve Curse** | Enemy casting a heal / buffing allies / doing something that MUST be stopped | Vasselroot Extract (next-action nullify) | Stage 2 (Silence, 4s) | oGCD. 20s cooldown. Silences ONE target for 4s. If Bone Spirit's interrupt is on cooldown or out of range, this is the backup. But it has a 20s CD — use it frivolously and you won't have it for the important cast. |
| 3 | **Mastema** | Priority target with 3+ Hex stacks (maximize damage without resetting debuff) | No direct item equivalent (premium damage) | None | 2.5s cast, 30s CD. Heavy damage. Does NOT consume Hex stacks. This is your "I've got this enemy debuffed and I want to HIT it without losing the debuffs." The 2.5s cast means you're committed — if the encounter changes mid-cast, you can't react. |

#### Response to: Party HP Drop / Damage Spike

| # | Name | Trigger Condition | Replaces (Item Baseline) | CC Stage | Decision Created |
|---|---|---|---|---|---|
| 4 | **Hex Drain** | Triage Minor triggered (ally ≤50% HP) OR preemptive sustain needed | Harmony Draught (regen) + Rejuvenation Flask (burst) combined | None (healing) | oGCD. Consumes Hex stacks from target enemy → heals lowest ally proportionally. THE core tension: maintaining Hex = enemy stays weak. Draining = party heals but enemy recovers. You're choosing between offense (debuffed enemy) and survival (healed party). |
| 5 | **Bone Salve** | Emergency single-target heal, ally critically low | Divine Blessing equivalent (emergency button) | None (healing) | GCD, 2.0s cast, 45s CD. Strong single-target heal (350p). Costs 1 MonsterBone. The BONE COST is the decision — every Bone spent on healing is a Bone NOT spent on summons. Healing drains your strategic assets. |
| 6 | **Ancestral Rite** | Multiple allies damaged, sustained healing needed (Triage Over threshold) | Healing Specter (zone heal) | None (channel heal) | GCD, channeled 4s (2 ticks × 250p heal to all allies in 10y). Locks you in place for 4s. Maximum healing throughput — but you're doing ZERO damage and cannot reposition. If the boss moves or AoE drops on your position during channel, you eat it. |

#### Response to: Map Geometry Challenge

| # | Name | Trigger Condition | Replaces (Item Baseline) | CC Stage | Decision Created |
|---|---|---|---|---|---|
| 7 | **Summon Bone Spirit** | Chokepoint identified where interrupt coverage is needed | Stupor Bell (AoE interrupt) | Stage 2 (Interrupt on 10s auto-CD) | GCD, 2.0s cast, costs 1 MonsterBone. Persistent sentry. The PLACEMENT decision: where does this sentry provide maximum value? Near the party (safe from enemies, limited interrupt range coverage)? At the chokepoint (maximum coverage, vulnerable to SR3+ destruction)? |
| 8 | **Bone Pointing** (Floating Bone deploy/reposition) | Enemy approach path identified, zone denial needed | Witherfield Totem (debuff zone) + Hexcage Lantern (detection zone) | Stage 1 (Slow via Hex debuff aura) | GCD, 2.0s cast. Costs 1 MonsterBone if new; FREE if repositioning existing. The Floating Bone's 10y aura applies Hex passively. Placement determines WHICH enemies get cursed. Wrong placement = wasted. Right placement = entire packs debuffed for free. |
| 9 | **Spirit Vine Barrier** | Party needs physical barrier at a doorway/passage | Quartzwall Capsule (crystal wall) + Thornveil Seed (thorny hedge) | Stage 1 (Root on contact) | GCD, 2.5s cast, 30s CD. Creates a vine wall (4y wide) that roots enemies on contact and persists 20s. Enemies can attack through it (not a full block) but can't PASS without being rooted. Unlike Quartzwall, allies can pass freely. |

#### Response to: Resource Depletion

| # | Name | Trigger Condition | Replaces (Item Baseline) | CC Stage | Decision Created |
|---|---|---|---|---|---|
| 10 | **Bone Harvest** | Between encounters OR MonsterBone reserves ≤2 | No item equivalent (class resource generation) | None | oGCD, 60s CD. Generates 2 MonsterBone. Timing this matters: use it the instant it's available (maximize bones over the run) or hold it (in case a summon dies and you need emergency redeploy)? In hard content (SR4), this is your LIFELINE — mistime it and you have no summons for 60s. |
| 11 | **Bone Scavenge** | Enemy dies near Shaman (passive) | No item equivalent | None | PASSIVE. 30% chance on enemy death within 15y to gain 1 MonsterBone. In dungeon trash pulls: bone-positive. In boss fights: bone-neutral (only adds spawn during add phases). This incentivizes the Shaman to be NEAR kills — positional requirement. |

#### Response to: Multiple Simultaneous Threats

| # | Name | Trigger Condition | Replaces (Item Baseline) | CC Stage | Decision Created |
|---|---|---|---|---|---|
| 12 | **Dark Theurgy** | 3+ enemies clustered, need mass Hex application | Lockjaw Spore (area CC) + Fogmind Censer (awareness reduction) | Stage 1 (slow via mass Hex) | GCD, 2.5s cast, 15s CD. AoE ground circle (5y) applies 1 Hex stack to all enemies hit + lingering DoT zone. The "I need to Hex EVERYTHING" button. 2.5s cast means no weaving — full commitment. If enemies move out of the zone during your cast, it misses. |
| 13 | **Curse Explosion** | High-stack Hexed target that NEEDS to die NOW (execute threshold) | Berserker's Draught (damage boost) + Rupture Oil (armor shred) | None (burst) | GCD, 2.5s cast. Consumes ALL Hex stacks on target for burst damage (50 + stacks × 50). This RESETS the enemy to un-debuffed state. Use ONLY when the damage will kill or when you don't need the debuff anymore. Using this at 5 stacks when the enemy has 60% HP remaining is GRIEF — you lose all your debuffs for inadequate burst. |
| 14 | **Spirit Ascension** | Unavoidable AoE phase, OR need elevated position for cast safety | No item equivalent (class ultimate) | None | GCD, 2.0s cast. Shaman levitates (immune to ground AoE, +range on all abilities). Lasts 15s. Damage amp +20% while airborne. Costs 2 MonsterBone. The Bone cost is STEEP — this isn't used on cooldown. It's used when the encounter DEMANDS ground immunity. Misusing it means 2 fewer summon deploys available. |

#### Sustained Damage Tool

| # | Name | Trigger Condition | Notes |
|---|---|---|---|
| 15 | **Spirit Channel** | Bone Spirit alive + want burst (sacrifice summon for huge hit) | GCD, 2.0s cast. CONSUMES Bone Spirit for 400-500p damage. Bone Spirit is GONE. Need a new MonsterBone + 10s delay to re-summon. Only use when: fight is nearly over (don't need sentry), OR bone reserves are high and burst is critical. |
| 16 | **Invocation** | Both summons active + extended fight that warrants enhanced deployments | GCD, 2.5s cast, 90s CD. Upgrades both summons for 25s: +50% HP, Bone Spirit attack potency doubled, Floating Bone Hex application rate doubled. The "I'm investing in my deployments for this phase." Wasted if summons die during the window. Rewards protecting your assets. |

---

### Vulnerability Windows

The Shaman is NOT overpowered because:

1. **Hex Drain REMOVES debuffs from enemies.** Healing the party means the enemy you've spent 15-25s debuffing returns to full capability. Sustaining your party costs you offensive pressure directly.

2. **MonsterBone is FINITE and CONSUMABLE.** Every Bone Salve (emergency heal) is a summon you can't deploy. Every Spirit Channel (burst damage) is a lost sentry. Every Spirit Ascension costs TWO bones. Resource mismanagement across the entire run — not per-fight — creates cascading vulnerability.

3. **Slow class identity.** Soue racial: not fast, not dodgy. Cast times of 2.5s on key skills (Curse Explosion, Dark Theurgy, Mastema) mean the Shaman is COMMITTED during casts. If AoE drops during your 2.5s cast, you eat it or cancel (losing the GCD + the effect).

4. **Summon destruction at SR3+.** At high difficulty, enemies actively destroy your installations. Floating Bone (15% HP, stationary) dies frequently. Bone Spirit (25% HP, mobile) dies to AoE phases. Replacing them costs Bones + GCDs + positioning time. In SR4 content, the Shaman is constantly MANAGING LOSS rather than pressing an advantage.

5. **No self-healing.** Hex Drain heals ALLIES (lowest HP party member). The Shaman's overshield comes FROM maintaining Hex stacks — but if they Drain stacks to heal others, they lose their own overshield generation. Protecting yourself competes with protecting others.

6. **Triage requires SACRIFICING DPS entirely.** Ancestral Rite (channel heal) locks you for 4s doing ZERO damage. Bone Salve costs a MonsterBone. The Shaman's healing is effective but EXPENSIVE — in opportunity cost, resource cost, and positioning vulnerability.

---

### Healer Identity Distinction

**Shaman heals through LIFE-DRAIN (Hex Drain).** The offensive action IS the heal:
- Apply curses to enemies (debuffing them) → Drain curses (healing allies, but releasing the enemy from debuffs).
- Healing throughput scales with how many curses you've INVESTED. More aggressive Hex application = more Drain potential later.
- The Shaman must be OFFENSIVE first to enable healing second. A passive Shaman can't heal because they have no Hex stacks to drain.

**Item Baseline for Shaman Healing:**
- Rejuvenation Flask (20% HP burst) → Hex Drain at 5 stacks provides comparable healing but requires 15-25s of prior Hex investment.
- Healing Specter (zone heal, stationary, 15s) → Ancestral Rite is mobile (centered on Shaman) but channeled (4s lock).
- Harmony Draught (ally-consumed, 12s regen) → Bone Salve is stronger but costs MonsterBone (the class's premium resource).

**What makes it DISTINCT from Elementalist:**
- Elementalist heals with TERRAIN (place water zone, allies stand in it). Positional, AoE, passive.
- Shaman heals with AGGRESSION (curse enemies, drain curses into healing). Active, requires prior offensive investment, single-target-selectable.
- Elementalist healing costs MANA (recoverable by meditation). Shaman healing costs HEX STACKS (recoverable only by re-cursing over 15-25s) and sometimes BONES (irreplaceable outside Bone Harvest CD).
- Elementalist can heal without engaging enemies (Water saturation works in any state). Shaman MUST have cursed enemies to Drain — no enemies cursed = no healing possible.

---

### Anti-Patterns (What This Class Does NOT Do)

- ❌ **No fixed burst windows.** Curse Explosion is used when the target needs to DIE, not when a timer completes. Spirit Ascension is used when the ground is lethal, not every 90s.
- ❌ **No "build to 5 stacks then spend" on a timer.** Maintaining 5 stacks IS the sustained DPS state. Exploding them is a conscious SACRIFICE of that sustained state for burst — and it's rarely optimal. The tension is maintain vs. drain vs. explode.
- ❌ **No rotation order.** Effigy is filler. Dark Theurgy is used when enemies cluster. Mastema is used when stacks are high and you want damage without consuming. Bone Salve when someone's dying. These respond to STATE, not SEQUENCE.
- ❌ **No "setup phase → payoff phase" cadence.** Bone deployment is CONTINUOUS spatial adaptation, not a pre-fight setup ritual. You reposition throughout the fight.
- ❌ **No Bone Harvest alignment.** The 60s cooldown on Bone Harvest doesn't create a cadence because the SPENDING is variable — some fights burn 4 bones/minute (SR4 destruction), others burn 0 (SR1 persistence). The generation is fixed; the consumption is encounter-dependent.
- ❌ **No passive overshield farming.** Old design let you maintain Hex forever and farm overshield. New design: Hex Drain CONSUMES stacks. You must choose between debuff maintenance and overshield generation. Can't have both.

---

### How Items Complement (Not Compete)

Even WITH a Shaman in the party:

| Item | Why It Still Matters |
|---|---|
| **Scatterlung Phial** (-30% accuracy, 12s, stationary) | Shaman's accuracy debuff requires Hex stack investment (15-25s to reach -25%). Phial provides INSTANT -30% for emergencies before Hex builds. |
| **Thickglass Flask** (-50% move speed puddle, 20s) | Shaman's speed curse follows targets but builds over time. Flask provides immediate -50% at a specific location — useful for denying a path NOW, not after 10s of Hex buildup. |
| **Stasis Pin** (3s total freeze, Stage 3) | Shaman has NO Stage 3 CC. For total lockdown, the party needs items (or another class). Shaman provides sustained debuff, not hard disable. |
| **Hollowform Decoy** (aggro redirect, 15s) | Shaman's Bone Spirit redirects via interrupt, not aggro. Decoys draw attacks. Different function — Decoy says "hit this instead," Bone Spirit says "you can't cast here." |
| **Witherfield Totem** (multi-debuff zone, 25s, destroyable) | If the Shaman's Floating Bone is destroyed and Bones are depleted, the PARTY can cover the gap with Witherfield Totems. Worse (destroyable, duration-limited) but functional. This is the item-as-fallback design working correctly. |
| **Premium rare: Cursed Chalice** (hypothetical) | A crafted item that provides +2 Hex stacks instantly on use. Accelerates the Shaman's Hex buildup. The class is better WITH it, but doesn't require it. |

---

### CC Stage Budget

| Ability | CC Stage | Notes |
|---|---|---|
| Hex Stacks (passive at 5) | Indirect Stage 1 (10% action skip ≈ minor disruption) | Passive. Requires 5 stacks invested. Action skip is probabilistic — not reliable hard CC. |
| Floating Bone Aura (Hex slow) | Stage 1 (Speed reduction via Hex) | Passive, positional. Enemies must be in 10y range. |
| Spirit Vine Barrier | Stage 1 (Root on contact) | 20s duration, 30s CD. Enemies rooted can still attack/cast. |
| Nerve Curse | **Stage 2** (Silence, 4s) | oGCD, 20s CD. Single-target. Primary caster-shutoff tool. |
| Bone Spirit Auto-Interrupt | **Stage 2** (Interrupt) | Auto, 10s CD per spirit. Only interrupts CASTS — does nothing to physical attackers. |
| Dark Theurgy (lingering zone) | Stage 1 (Slow via ground effect) | Terrain-based. Avoidable. |

**Budget Assessment:** The Shaman has ZERO Stage 3 CC. Maximum reliable CC is Stage 2 (Silence + Interrupt). This is appropriate for a DPS/offtank/healer hybrid — the class trades hard disable for sustained attrition pressure. If the party needs Stage 3 lockdown, they bring a Grappler (melee stance) or use Stasis Pin items. The Shaman makes enemies progressively weaker but never completely locks them down.

---
---

## Cross-Class Comparison: Healer Identity

| Dimension | Elementalist | Shaman |
|---|---|---|
| **Heal trigger** | Party HP threshold (reactive to damage) | Hex stack availability (requires prior offensive investment) |
| **Heal delivery** | Terrain zone (allies stand in water area) | Targeted drain (Shaman selects ally to heal via Drain targeting) |
| **Heal cost** | Mana (recoverable via Meditation, ~15s) | Hex stacks (recoverable only by re-cursing over 15-25s) + sometimes MonsterBone |
| **AoE healing** | Strong (Tidal Basin, Water saturation regen) | Weak (only Ancestral Rite channel, 4s commitment) |
| **Single-target burst** | Weak (Cleansing Rain oGCD is moderate, limited charges) | Strong (Hex Drain at 5 stacks, Bone Salve emergency) |
| **Self-healing** | Cannot (Water heals allies, not self) | Cannot (Hex Drain heals allies; overshield requires maintaining stacks you might need to Drain) |
| **What breaks healing** | Running out of mana (forced Meditation = 0 output for 15s) | No Hex stacks available (enemies died / stacks were Drained / new target not yet cursed) |
| **Healing without enemies** | YES (Water saturation works any time) | NO (must have cursed enemies to Drain from) |
| **Item baseline replaced** | Rejuvenation Flask, Healing Specter, Harmony Draught | Drainwick Candle (conceptually — drain from enemies), plus healing items via Bone Salve |

**Why both can exist in the same party:** Elementalist covers sustained AoE maintenance healing (Water saturation) and emergency burst prevention (Aqua Veil barrier). Shaman covers spike damage recovery (5-stack Drain is massive single-target) and triage when the Elementalist's mana is depleted. They're different TIMING profiles: Elementalist is the "always-on, moderate" healer; Shaman is the "expensive, powerful, intermittent" healer.

---

## Fire Degeneration Mitigation (Both Classes)

**The known problem:** On flat, featureless maps with no environmental demands, both classes degenerate:
- Elementalist → Fire saturation forever (highest DPS, no reason to switch)
- Shaman → Effigy spam + Curse Explosion cycle (no geometry to exploit with deployments)

**Class-level solutions (in addition to level design forcing variety):**

| Solution | Elementalist | Shaman |
|---|---|---|
| **Mana drain** | Fire costs 80 mana/s (highest). Cannot sustain >60s without switching to cheaper element or meditating. | N/A (Shaman doesn't have element switching) |
| **Enemy resistance escalation** | Sustained same-element damage builds RESISTANCE in targets (ToS-style). After 20s of Fire, target gains +20% Fire resist. Forces switching. | Hex stacks cap at 5. No further debuff benefit beyond 5 — incentivizes Exploding or Draining rather than indefinite maintenance. |
| **>50% HP rule interaction** | Fire is most efficient above 50% enemy HP (bonus damage). Below 50%, the bonus disappears — CC/utility from other elements becomes relatively more valuable. Natural fire→utility transition point. | At enemy 50% HP, kill pressure is lower (no bonus). Shaman shifts from damage amp (maintaining Hex) toward finishing (Curse Explosion) or pivoting to heal the party (Hex Drain). The HP threshold creates a natural decision point. |
| **Encounter-forced geometry** | Corridors, elevation, water terrain, environmental hazards — all demand non-Fire elements to navigate. | Spawn directions, chokepoint shifts, add phases from new angles — all demand summon repositioning and spatial reading. |

---

## Impairment Axis Coverage

Both classes contribute to the three impairment axes differently:

| Impairment Axis | Elementalist Contribution | Shaman Contribution |
|---|---|---|
| **Unfocus (reduce SR)** | None — Elementalist doesn't suppress AI | None — Shaman debilitates but doesn't make enemies dumber (that's Madolt's job) |
| **Accuracy Debuffs (reduce hit rate)** | Minor — Wind saturation provides 20% projectile miss chance (deflection, not accuracy) | Primary — Hex stacks provide -5% to -25% accuracy scaling. This is the Shaman's CORE impairment contribution. |
| **Darkness (reduce vision distance)** | Minor — No native darkness tools | None — Shaman doesn't affect vision (that's Nightfly Colony / Grappler Ink stance) |

**Design note:** The Shaman IS the accuracy impairment specialist. If you want enemies to miss, you bring a Shaman (persistent, scaling, multi-target) or you bring Scatterlung Phials (temporary, single-use, single-zone). The Elementalist's deflection (Wind) is incidental — it's not the reason you bring an Elementalist.

---

## Summary: What Makes These Classes Worth Picking Over Items

| Question | Elementalist Answer | Shaman Answer |
|---|---|---|
| **Why not just carry items?** | Items commit you to ONE element pre-fight. Elementalist adapts to what's needed NOW. Items are single-use; Elementalist is permanent. | Items expire (8-25s), are destroyable, single-use. Shaman's debuffs are persistent, follow targets, and scale over time. |
| **What's the premium over items?** | Terrain transmutation (items remove; Elementalist converts). Element-adaptive response. Sustained healing zone (items are burst). Chain reaction detonation (items prime; Elementalist finishes). | SR4 breach (items can't affect SR4 enemies; Shaman can). Persistent indestructible-equivalent deployments (enemies can destroy but Shaman re-deploys). Hex Drain healing-from-offense (no item does this). |
| **When is the class BETTER than items?** | Extended encounters (items run out). Multi-element encounters (items commit wrong). Terrain-heavy maps (items remove; class converts). | Extended encounters (Bone economy sustains indefinitely with Harvest). SR3-4 content (items are dodged/destroyed; class abilities bypass). Multi-target debuff scenarios (items cover 1-2; Shaman covers all). |
| **When are items BETTER than the class?** | Mana-depleted state (Elementalist in Meditation = useless; items still work). Specific rare items exceed class output for 15s windows. | Bone-depleted state (no summons, no Bone Salve). Stage 3 CC (Shaman has none; Stasis Pin does). Instant debuff application (Shaman requires 15-25s buildup; Phials are instant). |

---

*This document is the qualitative foundation for rebuilding Elementalist_Complete.yaml and Shaman_Complete.yaml with item-first logic, trigger-based ability design, and zero rotation-cadence assumptions.*
