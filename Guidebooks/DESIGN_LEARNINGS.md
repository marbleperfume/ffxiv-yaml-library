# DESIGN_LEARNINGS.md
## What We Learned From Simulation — juice-yaml-library
### Observations that inform future level design and encounter tuning.

---

## 1. Elementalist is Highly Linear in FFXIV-Flat Circumstances

**Test:** Lv32 Rank 2 Elementalist in Brayflox-equivalent dungeon (3 trash → 7+elite → boss). Bad tank scenario.

**Result:** Fire-dominant output. Wind and Earth disappear entirely against bosses. Rotation collapses to Fire spam + Aqua Burst maintenance. Convergence stacks cycle between Fire (damage) and Water (heal). No decision point beyond "is the tank dying?"

**Why:** In a single room with predictable damage and no movement pressure:
- Wind has no use case (nothing forces repositioning, instant casts unnecessary)
- Earth has no use case (nothing needs interrupting, no choke points to hold)
- The "5 elements" system degenerates to "2 elements + oGCDs"

**Root cause:** Not a numbers problem. Not a potency tuning issue. The ENVIRONMENT doesn't demand the tools. FFXIV dungeons are flat arenas where the only variable is "am I taking damage?" — which only touches Fire and Water.

**What forces all 5 elements into relevance:**
| Element | Environmental demand |
|---------|---------------------|
| Wind | Enemies that chase (SR2+), terrain that forces repositioning, party splits requiring mobility |
| Earth | Enemies with interruptible casts, chokepoints to hold, SR3+ flankers to root |
| Light | Telegraphed burst damage (already works in flat content) |

**Design rule:** Do NOT tune potency to "fix" element balance. Tune ENCOUNTER DESIGN to demand the tools. Level design is the missing variable.

---

## 2. >50% HP Rule — CORRECTION

**The rule makes ENEMIES above 50% HP take +25% damage FROM players. NOT players taking +25% incoming.**

Previous simulation incorrectly modeled this as a player penalty. The actual intent:
- Enemies above 50% HP are EASIER to damage (accelerates the first half of their health bar)
- Enemies below 50% HP take normal damage (second half is harder — they "toughen up")
- This creates a natural cadence: fast burn → slow grind → execute phase
- For Rank 1 players with fewer kit options: the +25% compensates for lower output by making the early fight forgiving

**Implication for healing math:** Healing pressure calculations from the sim need to be redone WITHOUT the +25% incoming damage on players. Tanks survive LONGER than modeled. Healing demand is LOWER than calculated. The Elementalist's "never needs to heal on trash" finding becomes even more extreme.

**Implication for encounter design:** The real difficulty lever is enemy ATTACK PATTERNS (speed, tells, multi-hit), not raw damage numbers. If enemies don't hit hard enough to threaten, no amount of HP rules creates tension.

---

## 3. Low-Level Content Doesn't Create Kill Thresholds

**Observation:** At Brayflox-equivalent (Lv32, SR1 enemies), NEITHER class is ever in danger of dying. Shaman's overshield absorbs all incidental damage. Elementalist's oGCDs handle everything. Decisions exist but are never load-bearing (both options work, neither is punished).

**Root cause:** Damage inflation at low level + full Rank 2 kit = the environment can't threaten. Same problem FFXIV solves by limiting kit (Lv32 WHM has no oGCD heals). Games generally limit skills available or gear to prevent this.

**Design question:** Do we limit kit at low rank? Or do we make SR1 content intentionally brain-dead (FFXIV floor) and accept that decisions only become load-bearing at SR2+ content?

---

## 4. Three Engagement Models (The Real Framework)

These three circumstances determine what skills matter, what decisions exist, and where kill thresholds emerge. They are the ACTUAL design space — not potency tuning.

### Model 1: Player Can LEAVE (Kite/Disengage)

**Situation:** Free map, no forced intersection. Enemy isn't fast enough to punish disengagement. Combined with tanks, enemies get lured into kill zones and bursted over time.

**Logically easy UNTIL:** Enemy pulls tactics (SR2+) and begins ignoring basic lure behavior, or casts spells/attacks requiring direct player responses. The more enemies present, the more "risk range" expands (multiple simultaneous casts to dodge/interrupt).

**What matters here:**
- Movement speed (League-style — movement = time = map control)
- Kiting tools (Wind for Elementalist, Spirit Ascension for Shaman)
- Tank lure/suppress (Madolt Unfocus, Adafold tether)
- Enemy COUNT scales risk (not just individual enemy power)

**Kill threshold emerges from:** Too many enemies casting simultaneously. Player can leave ONE enemy's range, but not five.

### Model 2: Player CANNOT Leave (Locked Room / Boss Arena)

**Situation:** Raw statcheck. Forced to take damage and manage eHP. Healing or eHP equivalents become mandatory. Cast variety is extremely low — just survive and output.

**At Rank 2+:** Enemy interruptions begin mimicking Soulslike timing. Extraordinarily easy to lose vs multiple targets if characters aren't overtuned. Balanced for bosses (FFXIV model) but could flip with higher damage variance.

**What matters here:**
- Mitigation/sustain (Parry for Madolt, Overshield for Shaman, Healing for Elem)
- Interrupt tools (Bone Spirit auto-interrupt becomes life-saving)
- Burst efficiency (kill before resources deplete)
- The fewer GCDs "wasted" on non-damage, the faster you escape

**Kill threshold emerges from:** Attrition. Can't leave, can't outheal forever. Either kill fast enough or die.

### Model 3: Multi-Threat with Proximity-Based Decision Making

**Situation:** Multiple enemy types demanding different responses. Plan of action depends on proximity to other players. DENSE with choices.

**Critical design constraint:** If this is too dense / too many simultaneous choices, it LIMITS the player by overloading mental stack. Having multiple viable choices needs a SIMPLE flowchart to compare. Differences in:
- Enemy altitude (above/below, ranged/melee)
- Fight type (casters vs vanguard/beefy targets)
- Player class compatibility

...must NOT enforce encyclopedic knowledge until higher rank categories. Even at high rank, mental stack must be MAINTAINABLE.

**What matters here:**
- 3 limited choices + 1 significantly more limited one (League model)
- Depth from PREDICTED INTERACTIONS, not combinatorial explosion
- Personal success against multiple circumstances / cast environments
- The flowchart must be learnable, not memorized

**Kill threshold emerges from:** Decision paralysis → too slow → enemies reach you. OR: wrong priority → wrong enemy survives → chain reaction.

---

## 5. League of Legends as Decision Model

League demonstrates the target decision density:
- 3 core abilities with clear use cases (contextual but learnable)
- 1 ultimate with significantly higher commitment (longer CD = bigger decision weight)
- Depth from PREDICTING opponent behavior, not from having 30 buttons
- Movement speed IS a resource (map traversal = time = opportunity cost)
- Champion mastery comes from reading situations, not from rotation execution

**Application to juice-yaml-library:**
- At Rank 1: 3 skills + 1 big CD should be sufficient for engagement (FFXIV floor)
- At Rank 2+: same 3+1 skeleton but context demands reading enemy behavior
- At Strategist: the same skills, but the SITUATIONS demanding them are more complex
- Complexity is in the ENCOUNTER, not in the HOTBAR

---

## 6. Shaman DOES NOT Degenerate in FFXIV-Flat Content (But Isn't Threatened Either)

**Test:** Same dungeon, same bad-tank scenario. Shaman as DPS in Lv32 Brayflox equivalent.

**Result:** Shaman maintains 4-6 meaningful decisions per pull even in a flat room. The ToS-heritage design (deployable assets + dual-use economy) creates engagement that doesn't require terrain. HOWEVER: none of these decisions are load-bearing because nothing can kill the Shaman.

**Why decisions exist but don't matter (yet):**
| Design Element | Creates decision? | Decision matters? (at SR1 Lv32) |
|---------------|:-:|:-:|
| CE vs Mastema (DPS vs survival) | ✓ | ✗ (nothing threatens survival) |
| Spirit Channel (sacrifice deployment) | ✓ | ✗ (interrupt utility not needed at SR1) |
| Floating Bone placement | ✓ | ✗ (flat room, no geometry to exploit) |
| Bone economy management | ✓ | ✗ (SR1 enemies don't destroy summons) |

**The fundamental difference from Elementalist:** Shaman has decisions that WILL matter at SR3+ (when summons die, when enemies threaten). Elementalist has decisions that only matter with specific TERRAIN (which may or may not generate). Shaman's design is future-proof. Elementalist's needs level design to activate.

---

## 7. SR3 Isn't Just "Smarter Enemies" — It's Terrain + Movement Cost + Spawn Patterns

SR3's real impact isn't captured by "enemies flank" — it's the combination of:
- **Terrain limiting escape routes** (can't kite if corridor is one-way)
- **Movement cost** (League-style: distance = time = you're NOT doing something else)
- **Spawn patterns** (procgen puts enemies in configurations that don't repeat)

These three together create the engagement models above. SR3 just means the ENEMIES participate in all three models simultaneously (they can chase in Model 1, pressure in Model 2, and create multi-threat in Model 3).

---

## 8. Overshield as "Offtank Without Being a Tank" — Unproven at Kill Threshold

**Observation:** In the Brayflox sim, Shaman's overshield absorbs ALL incidental damage without ever being threatened. This PROVES the self-sustain works, but DOESN'T prove it creates meaningful gameplay.

**The design only sings when:** Overshield is insufficient alone. When Shaman must CHOOSE between:
- Maintaining stacks for overshield (safety) vs consuming for burst (kill speed)
- AND the wrong choice leads to DEATH

This requires enemies that deal enough sustained damage to eat through 30% overshield AND threaten real HP underneath. SR1 Brayflox doesn't do this. Procgen corridor with 3 SR3 flankers probably does.

---

## 9. Healer Identity Architecture — MAG/MED Split & Failure Modes

**Discovery session:** Healer identity is NOT "healer with DPS" vs "healer without DPS." It's a three-way split where each archetype fails DIFFERENTLY — and the failure mode IS the design.

### Key Findings:

- **Healer identity split discovered:** Proactive (barrier/MAG), Reactive (drain/MED), Sacrifice (consume debuffs). Each fails differently. The failure mode creates the class identity MORE than the success mode does.

- **"Healers cannot replace frontline" is load-bearing.** Every healer design MUST have a reason they die in melee sustained combat. This is not flavor text — it's a structural constraint that prevents healer homogenization. If any healer can facetank, the frontliner role collapses.

- **Charm as healing resource works** because it creates genuine cost (actions spent charming ≠ actions spent elsewhere) AND risk (Stage 3 Devotion pulls enemies toward the Siren). The resource isn't "mana that refills" — it's "attention from targets that must be maintained." This is fundamentally different from every other healing resource in the genre.

- **SPD ≠ movement speed resolves the "slow but unstoppable" fantasy** without making traversal painful. Siegebreaker walks at normal speed but REACTS slowly and ATTACKS slowly. The slowness is in combat animation commitment, not in getting from A to B. CC immunity as compensation for low SPD/NTU creates a genuine trade that feels fair from both sides.

- **Feedback-based detection (no gauges) works for feral classes** because the FANTASY is instinct, not calculation. Reading the game state IS the skill expression. Putting a number on screen for Reaver's pursuit state would turn a visceral "am I losing control?" feeling into a spreadsheet optimization problem. Audio/visual cues preserve immersion.

- **Colony at Special tier is correct.** Phenotype depth was underestimated at Base tier evaluation. Each phenotype (Builders, Flutters, Nightflies) is its own mastery path with distinct stats, engagement patterns, economic roles. Three phenotypes = three games under one racial umbrella. This is Special-tier complexity by definition.

### Implications for Future Design:

- Every new healer class needs its failure mode defined BEFORE its success mode. "How does this healer die?" precedes "How does this healer heal?"
- The MAG/MED hard split means hybrid healer/DPS is impossible within one stat investment. You commit to one role. This prevents the "do everything" healer problem.
- Weapon assignments (Trident, Harpoon) should be economic items tied to racial crafting. Merryin (Depth Dead) as potential weapon crafters for aquatic classes?
- "Skills that do nothing waste budget" extends beyond healers — every class should audit for invisible passives that could merge into observable feedback.

---

*Last updated: 2026-07-14*
*Source: Healer identity architecture session — MAG/MED formalization, Charm economy, SPD redefinition, pursuit feedback, Colony evaluation, water class design*
