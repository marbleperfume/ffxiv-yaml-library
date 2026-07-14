# DESIGN_OVERRIDE_SYSTEMS.md
## System-Level Rules & Architecture — juice-yaml-library
### Continuation of DESIGN_OVERRIDE.md (§15 onward)

<!-- ▲ CONTINUES FROM: DESIGN_OVERRIDE.md -->
<!-- ▲ Core philosophy (§1-14): Strategy Rank, Player Rank, Frontliner identity, -->
<!-- ▲ Parry, Capacitor Pull, Engagement Models, Rank 1 design, >50% HP rule -->

---

## 15. Healer Stat Architecture (MAG/MED Split)

**MAG = barriers + damage. MED = direct healing + drain/sustain.**

| Stat | Scales | Does NOT Scale | Healer Type |
|------|--------|----------------|-------------|
| MAG | Barrier strength, damage output | Direct HP restoration | Proactive (Elementalist) |
| MED | Direct healing, drain/sustain | Damage | Reactive (Siren, Shaman) |

---

## 15b. Healer Identity Triad

| Class | Stat | Behavior | Failure Mode |
|-------|------|----------|--------------|
| Elementalist (Tryll) | MAG 13 / MED 13 (split) | Barriers proactively → forced reactive when barriers break → CC for survival → Triage Over → mana crash | Deteriorates under pressure. Mediocre on purpose. Ramp = situation worsening. |
| Siren/Cantor (Merryin) | MED primary | Constant passive healing through Charm drain economy. Scales with battlefield presence. | Deteriorates in isolation. Needs enemies + allies nearby. |
| Shaman (Soue) | Choice-dependent | Heals by SACRIFICING enemy debuffs (Harvested state). Not primary healer. | Must choose: keep enemy weak OR heal team. Cannot do both. |

---

## 15c. Healers CANNOT Replace Frontline

**Solo healers are NOT designed to replace frontline.** Explicit anti-pattern for ALL healer classes. Every healer design must have a clear reason they die in sustained melee combat:
- Elementalist: mana crashes under sustained reactive healing
- Siren: Charm Stage 3 pulls enemies TO her (dangerous for a healer)
- Wavecaller: slowed on land, needs water portals for full throughput
- Shaman: sacrificing debuffs to heal removes offensive pressure

---

## 15d. Siren Charm Economy

Charm as central mechanic — sustain comes from making enemies/allies LOVE her:
- **Stage 1 (Fascination):** Enemy deprioritizes Siren as target. Minor drain trickle.
- **Stage 2 (Infatuation):** Enemy approaches Siren (repositioning tool). Moderate drain.
- **Stage 3 (Devotion):** Full behavioral override, max drain. BUT enemy now in melee with Siren.

Ally Charm stacking: Allies near Siren build attachment → receive passive healing from enemy drain. Charmed allies draw indirect aggro from charmed enemies.

Control-oriented players deteriorate from misreading Position × Action × Time — wrong Charm target, wrong refresh timing = Charm drops, exposed, no heals.

---

## 16. SPD Stat ≠ Movement Speed

**SPD = reaction time, dodge frames, animation speed. NOT walk/run speed.**

All classes walk/run at the same base movement speed. SPD affects:
- Dodge i-frame duration
- Animation cancel windows
- Reaction-based mechanic timing (parry windows scale with SPD)

A Siegebreaker (SPD 5) walks at normal pace. Cannot dodge, cannot react, cannot be stopped.

---

## 16b. CC Immunity as Core Trade

Low-SPD/NTU classes receive **CC immunity** instead of reaction-based survival:
- Siegebreaker: SPD 5 / NTU 3 but immune to stun, knockback, root, fear, sleep, pull, silence, slow
- CC immunity always active while Endurance > 0
- This is the TRADE for having no dodge frames and no parry window

---

## 16c. Momentum Ramp-Up

Directional commitment builds speed (Siegebreaker):
- Momentum Gauge: Moving → Rolling → Charging → Unstoppable (4 tiers)
- Direction change resets momentum to zero
- Once committed and built up: ACCELERATES beyond base speed
- "I walk at normal speed. Can't dodge, can't react, can't be stopped. Once I build momentum, I get FASTER."

---

## 17. Feedback-Based Detection (No Gauges)

For feral/pursuit classes (Reaver), internal state communicated through environmental feedback, NOT on-screen meters:
- Enemy behavior changes (flinching → staggering → blood trail → red outline)
- Audio cues (faint bass → rapid heartbeat → THUMP)
- Visual effects (subtle red vignette → screen pulse)
- Hotbar skill swaps (available skills change based on state)

**HP bar is the ONLY numeric resource displayed.** Player reads the game state. Reading IS the skill.

---

## 17b. Sated State (Pursuit Termination)

Post-pursuit forced calm period (Reaver):
- Cannot re-engage Frenzy/berserk after pursuit ends
- Duration scales with Frenzy length (15-25s)
- Has its OWN dedicated gameplay (defensive skills, party buffs, recovery)
- NOT a cooldown timer — it's a real playstyle with active decisions
- Physiological refractory period (body cooling down after exertion)

---

## 18. Skill Budget Rule

**Skills that do nothing waste budget.** Merge passive/waiting skills with functional feedback skills.

Anti-pattern: A skill whose only purpose is "I'm waiting" or "I'm preparing."
Correct: Every skill press produces IMMEDIATE output (damage, movement, debuff, information) even if its secondary purpose is building toward something larger.

---

## 19. Colony = Special Tier

Colony (Harvesters) upgraded from Base to **Special** tier:
- 3 phenotypes (Builder/Flutter/Nightfly) = 3 complete mastery paths
- Each phenotype is its own game with unique resource interactions
- Deceptively complex despite simple individual actions

---

## 19b. Harvesters Fly (Racial Trait)

All Harvesters have innate flight. Colony class leverages this:
- Builder: 80% flight speed (construction focus, less mobile)
- Flutter: 120% flight speed (aerial bomber, permanent flight viable)
- Nightfly: 100% flight speed (balanced, darkness zones from above)

---

## 20. Water Slime = Invulnerable Spirit (Spiritcaller)

Lower Drakol racial companion:
- Water elemental spirit, NOT a pet/creature
- Cannot be killed, has NO HP. Always present.
- Produces water passively (puddles, terrain interactions)
- Player manages proximity: close = safe (Moisture maintained), far = healing allies (Moisture drains)

---

## 20b. Moisture Gauge (Spiritcaller)

Defensive resource (0-100):
- High Moisture = DR bonus (wet skin absorbs impact)
- Low Moisture = vulnerable
- Slime proximity maintains Moisture passively
- Water skills COST Moisture (offense vs defense trade)
- Core tension: keep Slime close (stay safe) vs send Slime far (heal allies, lose DR)

---

## 20c. Hydration Gauge (Wavecaller)

Water exposure tracking:
- High Hydration = full healing power + normal movement speed
- Low Hydration = healing reduced + movement SLOWED on land (not rooted)
- Water portals and submerging restore Hydration
- Creates terrain preference: water zones = Wavecaller thrives, dry land = Wavecaller weakened

---

## 20d. Wavecaller Identity

**Dolphin/orca/killer whale.** Physical, fast, playful-violent predator.
- NOT Siren. No charm, no enchantment, no lure, no allure.
- Weapon: Harpoon (aquatic hunter)
- Sound magic = healing (fast, AoE, possibly no LoS)
- Water portal dive = damage delivery
- The AGGRESSIVE HEALER — wants to fight but should be healing. Push/pull tension IS the class.

---

## 21. Strix Ground State

Weaker altitude-themed ground variants for corridors/caves:
- Low hops, short glides, wall-jumps
- Ground = weaker but FUNCTIONAL (not helpless)
- Storm Talons (dual elemental short blades) for ground combat
- Ground outputs 55-60% DPS reference (dive = full power)

---

## 21b. Evasion Baked into Dashes (Strix)

Dashes GUARANTEE evasion frames (not chance-based):
- DEX → frame duration (0.3-0.5s)
- EVA → dash cooldown reduction (4s → 2.5s)
- SPD → distance (6m → 10m)
- Fantasy: "don't get hit" — untouchable FEEL when dashing

---

## 21c. Regen Starts on Descent

Recovery begins the MOMENT altitude decreases (Strix):
- "Thermal Recovery" triggers on downward movement
- 3% HP/s during dive descent, continues 4s tapering on ground
- Ascent cancels regen
- Cycle: up = spend, down = recover

---

## 22. Low STR Weapon Philosophy

Low-STR classes use elemental/poison weapons (damage from weapon properties, not raw strength):

| Class | Weapon | Property | Rationale |
|-------|--------|----------|-----------|
| Spiritcaller | Trident | Water/elemental (Moisture-powered) | Three-pronged = spread/multi-hit potential |
| Wavecaller | Harpoon | Physical + sound (MED-scaled) | Reach weapon, piercing, aquatic predator |
| Strix | Elemental/Poison (type TBD) | Elemental coating | Flight-compatible, light weapon required |

---

## 23. File Structure — Class-Chain Split Principle

Class specifications MUST split into a two-file chain when combined size exceeds **50 KB**:

| File | Target Size | Contains |
|------|-------------|----------|
| `{Class}_Design.yaml` | 25-45 KB | Identity, race lock, role objective, class mechanic (resource system, state machine), class-specific systems, rotation philosophy, anti-patterns, design notes |
| `{Class}_Skills.yaml` | 25-45 KB | Full GCD/oGCD skill roster with potencies, rank progression, balance targets, system interactions (Aggro, >50% HP, Crit, Procgen), matchup analysis, item baseline comparison, balance validation, visualization hooks, constraints |

**Header cross-references (mandatory):**
```yaml
# In {Class}_Design.yaml footer:
# ▼ CONTINUES IN: {Class}_Skills.yaml
# ▼ PICK UP AT: Section N (first skills section)

# In {Class}_Skills.yaml header:
# ▲ CONTINUES FROM: {Class}_Design.yaml
# ▲ GAP: Sections 1-M NOT in this file (identity, mechanic, systems)
```

**Chain extension for complex classes:**
```
Colony_Design.yaml
Colony_Skills_Builder.yaml
Colony_Skills_Flutter.yaml
Colony_Skills_Nightfly.yaml
```

**Rationale:**
- LLM generation trims quality on sections past ~50 KB context load
- Design identity and numerical implementation have different change cadences
- Either file can be regenerated independently without full context
- Git diffs become meaningful (design change vs number tweak)

**Rules:**
- Design file is WHAT THE CLASS IS. Skills file is WHAT IT DOES.
- Potency changes, skill additions/deletions, balance tweaks → Skills file ONLY.
- Mechanic redesigns, identity shifts, resource reworks → Design file.
- Both files must be independently readable (no dangling references).
- `_Complete.yaml` naming is DEPRECATED for new work. Existing files converted on next rebuild.

---

## 24. Document Chain — Design Override Split Principle

DESIGN_OVERRIDE.md itself follows the same chain logic. When this file exceeds **30 KB**:

| File | Contains |
|------|----------|
| `DESIGN_OVERRIDE.md` | Core philosophy (§1-14): Strategy Rank, Player Rank, Frontliner identity, Parry, Capacitor Pull, Engagement Models, Rank 1 design, >50% HP rule |
| `DESIGN_OVERRIDE_SYSTEMS.md` | System rules (§15+): MAG/MED split, SPD definition, CC immunity, feedback detection, Sated state, Colony tier, water systems, weapon assignments, file structure |

**Applies to ALL design documents.** Any `.md` or `.yaml` exceeding 50 KB should split at the natural design/implementation boundary. The chain is freely extensible — add or remove files as scope demands.

---

## 25. Resource Gating > Cooldowns (No Long CDs)

**Identity-defining skills are NEVER gated by long cooldowns (90s/120s/180s).** They are gated by RESOURCE COST — gauge, materials, field state, or consumables that the player actively earns through play.

### Why Cooldowns Fail

- 180s CD = 3 minutes where the class has no access to its defining power
- Player forgets the skill exists between uses → class identity is forgettable
- RPG encounter balance can't assume "maybe they used it 2 min ago"
- Opportunities permanently shut down by one bad timing → feels punishing, not strategic
- **Racially bound classes suffer double:** boring class = boring race

### Correct Pattern: Resource Gating

| Gate Type | How It Works | Example |
|-----------|--------------|---------|
| Gauge cost | Powerful skill drains gauge earned through combat actions | Reaver Frenzy (HP-gated, earned by fighting) |
| Material cost | Consumable resource (MonsterBone, Biomass, etc.) | Shaman summon deployment |
| Field state | Skill unlocks when battlefield conditions are met | Colony: terrain placed → big skill available |
| Escalation | Resource builds FASTER under pressure | Intensity-scaled gauge gen in hard fights |

### Key Principles

1. **Normal play emphasizes repetition or retreat to earn power.** The cycle of setup → payoff → reset → setup keeps the identity PRESENT. Never "wait 3 minutes."

2. **Intensity scales resource generation.** Bigger fights = more gauge = more access to powerful tools. The game REWARDS you for being in hard content with MORE of your class identity, not less. Avoid the pitfall of farming weak mobs for gauge to spend on bosses.

3. **Setup IS the resource.** For Colony, terrain placed = gauge accruing. For Shaman, hexes maintained = Harvest available. The preparatory actions ARE the gating — the payoff comes FROM the setup, not despite it.

4. **Stage 3 CC as resource-gated power** (not just burst damage). A Colony Nightfly's paralysis dust on retreat lets the party turn around and rain hell. This is IMMENSELY powerful precisely BECAUSE it's Stage 3. It's earned through positioning and resource, never trivially available on a timer.

5. **Never permanently shut down.** A missed opportunity costs time/resources to rebuild, NOT a 3-minute lockout. Player can retreat, re-earn, re-attempt. The punishment is inefficiency, not inaccessibility.

6. **Class identity present in EVERY engagement.** Player is always either USING the thing that makes their class/race special, or BUILDING TOWARD it. Zero dead-identity windows.

### Anti-Patterns

- ❌ 180s/120s/90s cooldowns on identity-defining skills
- ❌ Building gauge on weak enemies to spend on strong ones
- ❌ Spike-and-forget identity (3 strong hits then filler for 2 min — ToS Featherfoot problem)
- ❌ Opportunities permanently shut down by one bad timing
- ❌ "Ultimate" skills that exist outside normal play flow

### Correct Anti-Example: ToS Featherfoot

Featherfoot spews debuffs for 3 strong Kundela Slash hits, then goes back to Blood Sucking or other class rotations. The class identity (curse damage) only exists for ~10s every 30-40s. The rest is filler from a different class. This makes the identity forgettable. Colony/Shaman/any race-locked class CANNOT have this problem — the race will look boring.

### Short Cooldowns Are Fine

Tactical cooldowns (5-15s) that gate individual skill FREQUENCY without removing class identity are acceptable. The rule targets cooldowns long enough to create "dead identity" windows where the player has no access to what makes their class special.

---

*Last updated: 2026-07-14*
*Source conversation: Healer identity session + file structure reform + resource gating principle*
