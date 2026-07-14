# Class–Item Baselines

## Foundation Document: Items Define the Floor, Classes Are the Ceiling

> **Core Principle:** If a class can do it, a consumable MUST also do it (worse). No party composition is locked out of strategic solutions. Items are the BASELINE. Classes are the PREMIUM replacement.

> **How to read this document:** For each class, the Item Baseline section describes what a party WITHOUT that class uses to cover the same strategic ground. The class then replaces those items with persistent, scaling, adaptive solutions — that replacement IS the class's value proposition.

---

## Siren / Cantor — Item Baseline

### What This Class Does (Strategic Summary)

The Siren is the "I force you to do X" class. It overrides enemy action queues through biological vocal compulsion — not suppressing, degrading, or debuffing, but directly COMMANDING enemy behavior. Enemies are forced into specific actions against their will: attacking allies, moving to bad positions, using abilities at suboptimal times. This is distinct from confusion (random behavior) or aggro manipulation (priority shifts). The Siren dictates with precision. Secondary role: healing via harmonic resonance, delivered simultaneously through the same vocalization system.

### Item Baseline (What a Party Uses WITHOUT This Class)

| # | Item Name | Strategic Function | Why It's Worse Than the Class |
| --- | --- | --- | --- |
| 1 | **Pheromone Tag** (existing) | Forces all enemies within 10m to prioritize a tagged target for 8s — redirects aggro | Single-use, 8s duration only, cannot specify WHICH action enemies take (just who they target), no precision in what the target does. CC Stage: 2 |
| 2 | **Rivalmark Dust** (existing) | Two enemies prioritize attacking each other for 10s — forces infighting | Requires two enemies near each other, breaks if you hit either, no control over WHO attacks whom beyond the pair, cannot redirect to a specific location. CC Stage: 2 |
| 3 | **Compulsion Chime** (new) | Rung bell forces one enemy to use its NEXT ability immediately (even if on cooldown recovery), wasting it into empty space. Single-target, 1 action forced, consumed on use | Forces one wasted action but you can't choose WHICH ability or WHERE they aim it. Single instance, no persistence, no follow-up command. Requires 1.5s activation time. CC Stage: 2 |
| 4 | **Sycophant Incense** (new) | Burned incense (3m radius, 10s) causes enemies inside to path toward the incense instead of toward players. Passive movement command — enemies "want" to be near the incense | Stationary, enemies only MOVE toward it (don't attack it, don't use abilities on it), 10s duration, SR3 enemies can resist after 4s. Does not command actions, only pathing. CC Stage: 1 |
| 5 | **Harmony Draught** (new) | Consumed by an ally. For 12s, that ally regenerates 3% HP/s. The "non-magical healing" item baseline — slow, predictable, no triage | Fixed regen rate regardless of damage taken, cannot burst heal, does not scale with danger level, occupies the ally's consumable slot (not the healer's action), single target only |
| 6 | **Resonance Crystal** (new) | Placed installation (4m radius, 15s). Allies inside gain +15% healing received from ALL sources. Amplifies existing healing but provides none on its own | Positional (allies must stay inside), provides zero healing without another source, 15s duration, SR3+ enemies can destroy it (3 hits), amplification only — not generation |
| 7 | **Taunt Cracker** (existing) | All enemies in 6m radius forced to path toward detonation point for 3s — brief movement override | Only 3s, only forces MOVEMENT (not actions), enemies resume normal behavior immediately after, cannot chain commands, radius-based (not target-selective) |
| 8 | **Hollowform Decoy** (existing) | Deployed decoy draws aggro within 8m for 15s — enemies attack the decoy instead of players | Enemies choose to attack the decoy but aren't COMMANDED — they attack in their normal patterns, just toward the wrong target. Decoy is destructible. No healing component. |

### The Class Advantage (Why Pick The Class Over Items)

The Siren provides **precision command sequencing** — not just "redirect aggro" but "YOU, attack HIM, with THAT ability, NOW." Items can redirect attention or force brief movement, but they cannot dictate specific actions, chain commands in sequence, or maintain continuous control over multiple enemies simultaneously. The Siren also heals WHILE commanding — the same vocalization that overrides enemy cognition resonates at frequencies that accelerate ally tissue repair. No item combines offensive behavior control with healing delivery in a single action economy. The Siren never runs out of commands, never has a 15s duration window, and adapts commands in real-time based on battlefield state.

### Strategic Problems This Class Solves

1. **"The boss has a devastation ability and we need it used at the wrong time"** — Items can interrupt (Stupor Bell) but cannot FORCE early activation into empty space. The Siren commands the dangerous ability to fire prematurely.
2. **"Multiple enemies are coordinating focus fire on our backline"** — Items address individual enemies (Pheromone Tag = one target redirect). The Siren commands the entire group to attack each other or to path away simultaneously.
3. **"We need sustained healing WITHOUT dedicating a character to pure heal stance"** — Items provide fixed regen or amplification but no adaptive throughput. The Siren heals passively through vocalization while actively commanding enemies.
4. **"An enemy is positioned perfectly and won't move"** — Items like Taunt Cracker force 3s of movement. The Siren commands continuous repositioning until the target is where the party wants it.
5. **"SR3 enemies are too smart to fall for decoys or simple aggro tricks"** — Item-based attention manipulation degrades against high-SR enemies. Biological compulsion bypasses AI decision-making entirely.

### Open Design Questions

- How does command interact with boss immunity? Partial override (reduced duration? weaker command?) or total immunity with the Siren needing to target adds?
- Healing modality — same vocalization simultaneously heals allies and commands enemies, or separate voice "channels" that compete for the Siren's action economy?
- At what point does command overlap with Shaman's aggro redirection to installations? The distinction (Siren = precise behavioral override vs. Shaman = aggro priority manipulation) must remain clear mechanically.
- Does command have a "line of hearing" requirement? Can the Siren command through walls if sound propagates?

---

## Siegebreaker — Item Baseline

### What This Class Does (Strategic Summary)

The Siegebreaker is the commitment-based immovable force. Once pointed at a target, it walks forward, absorbs everything in its path through exoskeleton armor, and destroys what it reaches. SPD 5, STR 18, MAGICCAP 6 — no magic, no reactions, no redirection. The skill expression is entirely in the ONE decision: where do I go? Low ceiling, high floor. Rewards simple play with enormous impact when commitment matches the situation.

### Item Baseline (What a Party Uses WITHOUT This Class)

| # | Item Name | Strategic Function | Why It's Worse Than the Class |
| --- | --- | --- | --- |
| 1 | **Hardshell Powder** (existing, MH reference) | Party-wide defense boost in AoE — the "become tanky briefly" team item | 3-minute duration but fixed magnitude, doesn't scale with forward momentum, provides damage REDUCTION but not damage IMMUNITY through sustained forward pressure, doesn't threaten enemies |
| 2 | **Quartzwall Capsule** (existing) | Creates a crystal wall (4m wide, 2.5m tall) — blocks movement and projectiles | Static, doesn't move, blocks BOTH teams, has HP and is destructible. The Siegebreaker IS a moving wall that only blocks enemies. Cannot be destroyed by normal damage. |
| 3 | **Ironhide Tincture** (new) | Consumed: +50% damage reduction for 8s, movement speed reduced by 40% during effect. The "become a bad Siegebreaker for 8 seconds" potion | 8s duration only, slows you without the compensating threat of inevitable arrival, no offensive component (you're tanky but not dangerous), any class can use it but none become the THREAT the Siegebreaker is |
| 4 | **Ramcharge Capsule** (new) | Consumed: next movement action in a straight line deals impact damage to all enemies in path, knocks them aside. Single-use directional charge | One use, fixed direction at activation, no ongoing momentum bonus, no super armor during the charge (can be interrupted), does not get stronger the longer it travels |
| 5 | **Concussion Charge** (existing) | Directional blast that pushes entities 4m — the "clear a path" explosive | 2s delay, doesn't move WITH you, only displaces enemies once (they return), no sustained area denial, blast direction fixed at placement |
| 6 | **Barricade Foam** (existing) | Custom-shaped barrier — the "block this corridor" tool | Defensive only (blocks, doesn't threaten), 2s harden time, destructible, stationary. The Siegebreaker IS the barricade AND the battering ram simultaneously |
| 7 | **Stoneskin Scroll** (BG3 reference) | Resistance to nonmagical physical damage — the defensive buff | Doesn't provide offensive presence, doesn't force enemies to respect your approach, duration-limited, doesn't scale. Enemies ignore you and target your backline. |

### The Class Advantage (Why Pick The Class Over Items)

Items can make a character temporarily tanky or create one-shot displacement, but NO item creates **sustained directional threat pressure**. The Siegebreaker's value is that enemies MUST deal with it or die — its approach is inevitable, its arrival is destruction, and the decision to ignore it is suicide. Items provide moments of tankiness; the Siegebreaker provides PERMANENT battlefield gravity. Its exoskeleton doesn't expire after 8 seconds. Its momentum doesn't reset after one charge. The commitment-based movement means that once the Siegebreaker decides, the map geometry changes — it's no longer "can we go through there?" but "the Siegebreaker IS going through there, move or die."

### Strategic Problems This Class Solves

1. **"There's a fortified position we can't approach without losing party members"** — Items provide brief survivability windows (8s tincture, one-shot charge). The Siegebreaker walks through sustained fire indefinitely.
2. **"Enemies are spread across a corridor and we can't engage without getting flanked"** — The Siegebreaker's approach forces enemies to deal with IT, collapsing their formation around its path rather than around your squishies.
3. **"We need a frontline but nobody wants to play a complex tank"** — Items require management (timing, placement, charges). The Siegebreaker's skill expression is a single commitment decision — accessible to players who don't want mechanical complexity.
4. **"SR2+ enemies target our healer/DPS and aggro items only last seconds"** — The Siegebreaker's physical presence IS the permanent aggro tool. Enemies can't ignore an approaching STR 18 exoskeleton.

### Open Design Questions

- How does commitment-lock work? Does the Siegebreaker literally CANNOT turn for X seconds, or is turning penalized with momentum loss?
- What counterplay do enemies have? If they just dodge sideways, is the Siegebreaker useless? How does "inevitable but slow" remain threatening?
- Base tier class — how does it scale? Gear-dependent (heavier exoskeleton plating), or pure stat growth?
- Party role tension: if Siegebreaker doesn't need a healer (self-sustaining through exoskeleton absorption), what does the healer DO during Siegebreaker's approach?

---

## Grappler — Item Baseline

### What This Class Does (Strategic Summary)

The Grappler is the pre-committed predator. Before entering an instance, the player locks a tentacle stance that determines their entire combat expression: Stealth (ambush opener), Long-range (displacement/pull), Ink (area denial/vision reduction), or Melee Grapple (Stage 3 full disable). The tentacle IS the offhand slot — a biological appendage that replaces equipment. Main hand carries conventional weapons. Skill expression is in READING upcoming content and choosing the right stance. Once committed, adaptation is impossible — preparation IS the gameplay.

### Item Baseline (What a Party Uses WITHOUT This Class)

| # | Item Name | Strategic Function | Why It's Worse Than the Class |
| --- | --- | --- | --- |
| 1 | **Ripcord Harpoon** (existing) | Single-target pull 8m toward player — the "get over here" displacement tool | Single use, pulls toward YOU (not to an arbitrary position), large enemies only pulled 4m, no follow-up disable after pull. Grappler Long-range stance has infinite pulls + can chain into grapple. |
| 2 | **Stasis Pin** (existing) | Total freeze for 3s — the strongest single-target CC item. CC Stage: 3 | Single use, requires hitting (projectile accuracy), 3s only, no scaling, enemy unfreezes with stasis sickness but is fully free. Grappler Melee stance pins INDEFINITELY until released or broken. |
| 3 | **Blindveil Powder** (existing) | 60% detection range reduction for 12s — vision impairment as CC Stage: 1 | Thrown radius, affects enemies' detection of ALL players (not selective), 12s duration, doesn't stack with repeated applications. Grappler Ink stance creates persistent vision denial zones that last entire encounters. |
| 4 | **Phantom Echo** (existing) | 3s invisibility + ghost image — the ambush-enabling item | 3s only, player reappears and is instantly re-acquired, no damage bonus from stealth-break. Grappler Stealth stance provides extended concealment + massive initiation damage bonus on first strike. |
| 5 | **Frostweave Net** (existing) | 70% speed reduction for 6s OR enemy spends 2 actions breaking free — restraint CC. Stage: 1-2 | Slows but doesn't immobilize completely, enemy can still attack and use abilities, breakable by spending actions. Grappler Melee stance = complete pin (Stage 3), target cannot act at all. |
| 6 | **Webspinner Sac** (existing) | Progressive slow zone (root at 6s+ exposure) — area denial installation | 15s duration, combustible (fire destroys instantly), progressive slow only (not immediate control), doesn't work on single targets, root can be broken. CC Stage: 1→2 over time |
| 7 | **Numbsense Spike** (existing) | Enemies can't detect stealth or hear sound cues — stealth enabler installation | 15s duration, 5m radius only, doesn't GRANT stealth (only prevents detection OF stealth), destroyable. Grappler Stealth stance IS native stealth — no external enabler needed. |
| 8 | **Scatterlung Phial** (existing) | -30% accuracy cloud (3m radius, 12s) — the "you can't see well" debuff | Stationary, enemies can leave, only reduces accuracy (doesn't eliminate vision), doesn't combine with territorial control. Grappler Ink stance creates OPAQUE ink clouds + persistent terrain denial. |

### The Class Advantage (Why Pick The Class Over Items)

The Grappler's premium is **stance-wide persistence and integration**. Items provide isolated instances of pull, pin, stealth, or vision denial. The Grappler's chosen stance makes that function its ENTIRE identity for the run — unlimited uses, synergy between tentacle and main-hand weapon, and scaling with tentacle augment gear. A Melee Grapple stance Grappler doesn't use one Stasis Pin and hope — it pins, holds, releases, repositions, and pins again indefinitely. The pre-commitment also means the Grappler arrives PREPARED in ways items cannot replicate: a stealth-stance Grappler has been invisible since before combat began, not from the moment they popped a 3s consumable.

### Strategic Problems This Class Solves

1. **"We need a high-value target PERMANENTLY disabled, not frozen for 3s"** — Items provide windows. Melee Grapple stance provides indefinite Stage 3 CC at the cost of the Grappler's own action economy.
2. **"The enemy has terrain advantage and we can't close the gap safely"** — Long-range stance pulls enemies from elevated/defended positions repeatedly, no consumable budget spent.
3. **"We need persistent area denial that doesn't expire in 15s"** — Ink stance creates ink that persists until cleaned, providing encounter-long vision denial zones.
4. **"We need to open with perfect information and a devastation strike before enemies react"** — Stealth stance Grappler scouts AND delivers a massive first hit. Items like Phantom Echo give 3s of invisibility after combat starts — Stealth stance starts BEFORE combat.
5. **"Our party can predict what we'll face but needs a specialist for it"** — The stance-lock mechanic means the Grappler IS a specialist. Items are generalist — anyone carries them. The Grappler commits to mastery of one function.

### Open Design Questions

- Melee Grapple Stage 3 pin — does the Grappler also immobilize itself? If yes, the pin is a 2-for-1 CC. If no, what prevents the pin from being always-dominant?
- Tentacle augment gear — how much does this change stance behavior? Is a "fire-enchanted tentacle" in Ink stance meaningfully different from a "frost-enchanted" one?
- Open-world stance rules — if locked per-instance, what happens in overworld exploration? Stance locked per play session? Changeable at rest points?
- Party communication burden — does the Grappler need to "declare" their stance to the party pre-run? Is there UI for this?

---

## Spiritcaller / Tidebinder — Item Baseline

### What This Class Does (Strategic Summary)

The Spiritcaller is a healer who doesn't cast spells. A Water Slime — an innate biological symbiote born with the Lower Drakol — serves as the healing delivery system, scout, and damage dealer. The Drakol fights conventionally (melee/physical) while directing the slime via companion commands. GenerateWater (racial bonus skill) fuels the slime's actions. This is a split-attention class: fight as the warrior, heal as the slime, simultaneously. Distinct input modality from any caster healer.

### Item Baseline (What a Party Uses WITHOUT This Class)

| # | Item Name | Strategic Function | Why It's Worse Than the Class |
| --- | --- | --- | --- |
| 1 | **Healing Specter** (ToS reference) | Deployable healing zone that persists — positional healing | Stationary (allies must stand in it), fixed throughput, duration-limited, can't follow mobile allies, occupies a ground space that might conflict with combat positioning |
| 2 | **Harmony Draught** (new) | Ally-consumed regen potion (3% HP/s for 12s) — the baseline heal-over-time | Single target, fixed rate, consumed by the RECIPIENT (not the "healer"), doesn't respond to burst damage, ally uses their own consumable slot |
| 3 | **Rejuvenation Flask** (new) | Thrown flask that splashes a 2m area, instantly restoring 20% HP to allies hit — the AoE burst heal item | Single use, small radius (allies must cluster), flat 20% regardless of max HP scaling, doesn't provide ongoing healing, requires aim (can miss) |
| 4 | **Scout Familiar Scroll** (new, from Scroll of Summon Quasit reference) | Summons a temporary invisible scout for 30s — provides vision in unexplored areas | 30s duration only, scout cannot heal or interact with allies, cannot attack, consumable (one scroll = one scout), doesn't persist between encounters |
| 5 | **Springboard Disc** (existing) | Provides vertical mobility at a fixed point — traversal utility | Stationary, requires returning to the disc to use, doesn't provide scouting information, enemies can trigger it too. The slime can scout through gaps, under doors, into water — no fixed point needed. |
| 6 | **Divine Blessing** (MH reference) | Full HP + removes all ailments — the emergency recovery button | Single use PER ENTIRE RUN equivalent, doesn't heal the party (self only in item form), represents the most extreme healing item rather than sustained throughput |
| 7 | **Adrenaline Specter** (ToS reference) | Deployable SP regen zone for nearby players — resource recovery installation | Stationary, only restores resources (not HP), duration-limited, destroyable. The slime IS the resource: it doesn't expire, moves with the party, and provides HP rather than mana. |
| 8 | **Hexcage Lantern** (existing) | Reveals enemy positions through walls (installation, 5m radius, 30s) — scouting information | Stationary, 30s duration, only provides vision (doesn't interact with enemies or heal allies), destroyable at SR3+. The slime scouts, heals, AND can damage threats it finds. |

### The Class Advantage (Why Pick The Class Over Items)

The slime is **permanent, multirole, and action-economy-free**. Items provide healing OR scouting OR traversal — each costs a consumable slot, a use, and time to deploy. The Spiritcaller's slime does all three SIMULTANEOUSLY while the Drakol fights at full output. The slime never expires, never requires restocking, can be redirected instantly, and scales with the Drakol's GenerateWater output. It also can't be "used up" at the wrong time — it's always available, always present. The split-attention gameplay means the party effectively has 1.5 characters' worth of output from one player slot: a melee fighter AND a companion healer/scout.

### Strategic Problems This Class Solves

1. **"We need healing but our healer needs to fight too"** — Potions/items heal at the cost of the drinker's action economy. The Spiritcaller heals passively through the slime WHILE fighting in melee.
2. **"Scouting ahead costs consumables and delays the party"** — Scout scrolls are single-use and require stopping. The slime scouts while the party continues.
3. **"Water terrain is blocking our path / an enemy is in water we can't reach"** — Traversal items are positional. The slime IS water — it goes wherever water can go. Under doors, through cracks, into flooded chambers.
4. **"We need a healer immune to Silence effects"** — The slime isn't casting spells. Anti-magic effects that shut down Elementalist/Siren healing don't affect biological companion healing.
5. **"The party splits at a branch and one sub-group has no healer"** — The slime can potentially detach and heal a separate group while the Drakol fights with the other.

### Open Design Questions

- If the slime "dies" — regeneration timeline? Is the Drakol temporarily without a companion (vulnerability window), or does it regenerate from water generation quickly?
- Slime HP targeting — can enemies attack the slime? If yes, protecting the slime is gameplay. If no, there's no counterplay to the Spiritcaller's healing output.
- Burst healing capability — can the slime do emergency throughput, or is it exclusively sustained/passive? If only sustained, what does the party do during spike damage without burst-heal items?
- How far can the slime detach from the Drakol? Unlimited range (scout anywhere) or tethered (must stay within X meters)?

---

## Reaver / Deephunter — Item Baseline

### What This Class Does (Strategic Summary)

The Reaver is a pursuit-locked DPS. Once a target drops below an HP threshold, the Reaver's Bloodscent triggers: tracking, acceleration, and damage ramping engage simultaneously, and the Reaver CANNOT voluntarily disengage. It kills the target or dies trying. Before triggering, the Reaver is calm and mediocre. After triggering, it's terrifying and unstoppable. The skill expression is entirely in TARGET SELECTION — choosing who to commit to, because once committed, there's no take-back.

### Item Baseline (What a Party Uses WITHOUT This Class)

| # | Item Name | Strategic Function | Why It's Worse Than the Class |
| --- | --- | --- | --- |
| 1 | **Might Potion** (MH reference) | +ATK for 3 minutes — the baseline "hit harder" consumable | Fixed magnitude, doesn't ramp over time, doesn't scale with target health, doesn't provide any tracking or speed, doesn't commit you (no risk = no reward scaling) |
| 2 | **Bloodhound Capsule** (new) | Consumed: marks one enemy. For 20s, you can see the marked enemy through walls and gain +15% movement speed toward it. Does not increase damage or force commitment. | Doesn't increase damage at all, 20s duration, no acceleration over time, no "can't disengage" pressure that forces escalating commitment. It's GPS without the teeth. |
| 3 | **Berserker's Draught** (new) | Consumed: +30% damage dealt, -20% damage resistance, lasts 15s. The "go aggressive" trade item | Fixed duration (15s whether you need it or not), fixed magnitude (doesn't ramp), the defense loss is a COST not a mechanic, doesn't help you FIND or REACH the target. Doesn't lock commitment. |
| 4 | **Elixir of Bloodlust** (Diablo III reference) | Attack speed + movement speed on kill — the kill-chaining offensive buff | Only triggers AFTER a kill (not during pursuit), resets between targets, doesn't help against the FIRST target in a sequence, doesn't provide tracking or commitment-pressure |
| 5 | **Flashstep Cartridge** (existing) | 8m teleport in facing direction — gap closer | Single use, 8m only, doesn't track (teleports in a fixed direction, not toward a target), no damage component, no ongoing acceleration. The Reaver's gap close is PERMANENT and ACCELERATING. |
| 6 | **Ripcord Harpoon** (existing) | Pull enemy 8m toward self — alternative gap close approach | Pulls enemy to YOU (not you to enemy), single use, doesn't work well on large targets, no damage ramp after pull. The Reaver chases — it doesn't pull prey in. |
| 7 | **Rupture Oil** (existing) | 3-stack armor shred (40% reduction for 8s after stacking) — the "kill faster" damage amplifier | Requires 3-hit investment before payoff, 8s vulnerability window, doesn't increase YOUR damage (reduces enemy defense), doesn't persist beyond the window, doesn't accelerate your speed. |

### The Class Advantage (Why Pick The Class Over Items)

The Reaver's premium is **commitment-driven escalation with no ceiling**. Items provide flat bonuses for fixed durations — +30% damage for 15s, then back to normal. The Reaver RAMPS. The longer the pursuit, the faster it moves, the harder it hits. There is no upper limit within a single chase sequence. Items also provide no TRACKING — you can chug a Might Potion and the enemy can still outrun you. The Reaver's Bloodscent means the target is found regardless of stealth, distance, or terrain. And the commitment lock (cannot disengage) creates a risk/reward dynamic that no item replicates: the Reaver's damage scales BECAUSE it cannot retreat. The danger is the fuel.

### Strategic Problems This Class Solves

1. **"An enemy is fleeing at low HP and we can't finish it before it heals/repositions/calls reinforcements"** — Items provide burst speed (Flashstep) but not sustained pursuit. The Reaver literally cannot stop chasing.
2. **"We need guaranteed kill pressure on a priority target regardless of what it does"** — Items don't lock commitment. The Reaver's value is that once marked, the target WILL die or the Reaver WILL die. No middle ground.
3. **"Enemies scatter when pressured and we waste time chasing individuals"** — Items don't select and track targets. The Reaver's Bloodscent marks one target and ignores all distractions.
4. **"We need DPS that scales in extended fights rather than front-loading burst"** — Items provide fixed windows. The Reaver gets STRONGER the longer the fight continues (against a single target).
5. **"Our party needs someone who punishes enemies that try to kite or flee from our frontline"** — No item prevents an enemy from running. The Reaver prevents running by being faster AND unkillable (from the target's perspective) during pursuit.

### Open Design Questions

- "Can't disengage" — what happens if the marked target goes through a one-way door, teleports to another arena, or enters a phase transition? Does the Reaver break lock or remain helplessly committed?
- Calm state — what IS the Reaver's gameplay when not pursuing? If it's "mediocre DPS waiting for a trigger," that's potentially boring. Is calm-state Reaver still fun moment-to-moment?
- Target healed above threshold — does Bloodscent break? If yes, healers counter the Reaver hard. If no, once marked is marked forever?
- Team coordination — the Reaver can't peel off to help allies. How does the party compensate for having a member who is functionally "gone" once triggered?

---

## Colony — Item Baseline

### What This Class Does (Strategic Summary)

The Colony is three classes in one race: Builder (barriers/fortification/repair), Flutter (aerial mobility/pollen CC/seed attacks), and Nightfly (bioluminescent lures/darkness control/ambush traps). Each phenotype is a complete combat expression determined by Harvester biology. The eusocial insect identity means each Colony player is one specialized role within a greater organism. Every phenotype must be self-sufficient in solo play but synergizes with other phenotypes when multiple Harvesters group.

### Item Baseline (What a Party Uses WITHOUT This Class)

| # | Item Name | Strategic Function | Why It's Worse Than the Class |
| --- | --- | --- | --- |
| 1 | **Quartzwall Capsule** (existing) | Crystal wall (4m wide, blocks all) — the barrier/fortification item [Builder function] | Single use, blocks allies too, fixed shape, cannot be repaired, destructible (5 hits). Builder phenotype creates REPAIRABLE, SELECTIVELY-PERMEABLE barriers with no consumable cost. |
| 2 | **Barricade Foam** (existing) | Custom-shaped barrier (3m, 20s) — the construction item [Builder function] | 2s harden time, 20s duration, lower HP than Quartzwall, single use. Builder secretes construction material biologically — unlimited supply, instant hardening, repairable. |
| 3 | **Springboard Disc** (existing) | Vertical mobility installation (45s) — the aerial access item [Flutter function] | Fixed position, must return to disc to reuse, enemies can trigger it, 45s duration. Flutter phenotype HAS WINGS — doesn't need an installation for vertical mobility. |
| 4 | **Lockjaw Spore** (existing) | Spore cloud (3m radius, 15s, -20% speed, 25% action skip) — the pollen CC item [Flutter function] | Stationary cloud, 15s duration, affects a fixed area, single use. Flutter produces pollen from biological sacs — unlimited applications, mobile delivery (aerial drop), variable CC strength. CC Stage: 1-2 |
| 5 | **Hexcage Lantern** (existing) | Reveals enemies through walls (5m radius, 30s) — the lure/detection item [Nightfly function] | Only reveals, doesn't attract. Stationary. 30s duration. Nightfly bioluminescence actively LURES enemies toward the light AND provides detection simultaneously. |
| 6 | **Blindveil Powder** (existing) | -60% detection range for 12s — the darkness item [Nightfly function] | 12s duration, thrown (requires proximity), doesn't selectively enable the USER to see in the darkness they create. Nightfly sees through its own darkness natively. |
| 7 | **Thornveil Seed** (existing) | Thorny hedge barrier (3m, 40s) — the area denial/construction item [Builder function] | 4s growth time, combustible, fixed shape, single use. Builder constructs non-combustible fortifications instantly from biological secretion. |
| 8 | **Rattletrap Mine** (existing) | Alarm/slow trap installation — the early warning item [Nightfly function] | Single trigger, consumed on activation, detectable by SR3+. Nightfly lure-traps are reusable (bioluminescent organs regenerate), undetectable (appear natural), and chain into ambush setups. |

### The Class Advantage (Why Pick The Class Over Items)

Each Colony phenotype replaces an ENTIRE CATEGORY of consumables through biological capability. Builder replaces all construction/fortification items with unlimited biological secretion. Flutter replaces mobility items AND CC deployables with wings and pollen sacs. Nightfly replaces detection, luring, and darkness items with integrated bioluminescent organs and dark-adapted vision. The key premium is **biological regeneration** — the Colony never runs out. Pollen sacs refill, secretion glands produce continuously, bioluminescent organs recharge. Items are one-and-done. The Colony's body IS the inventory.

### Strategic Problems This Class Solves

1. **"We need persistent fortification that survives the whole encounter, not 20-30s barricades"** — Builder creates structures that last until destroyed AND can be repaired mid-fight.
2. **"We need aerial scouting AND pollen CC AND mobility without spending 3 item slots"** — Flutter consolidates flight + CC + ranged harassment into one phenotype.
3. **"We need to control enemy pathing using light/dark manipulation without running out of lure items"** — Nightfly's bioluminescence is biological and regenerating, not consumable.
4. **"We're doing a long dungeon and can't afford the item budget for ongoing construction/CC/detection"** — Colony phenotypes provide these functions for FREE — no economy drain over extended content.
5. **"Multiple Harvesters in a party need to synergize their phenotypes"** — No item combination replicates Builder walls channeling enemies into Flutter pollen clouds illuminated by Nightfly lures. Colony-Colony synergy is an exclusive emergent space.

### Open Design Questions

- Phenotype permanence — character creation (one body type forever) or spec choice (changeable between runs)?
- Base tier with 3-phenotype complexity — is each individual phenotype simple enough for Base tier accessibility?
- Colony-Colony synergy — does the game incentivize multi-Harvester parties? Or is one Colony per party the expected pattern?
- Builder resource — even biological secretion should have some resource gate. What limits construction volume per encounter?

---

## Strix — Item Baseline

### What This Class Does (Strategic Summary)

The Strix is a pre-calculation dive bomber. From altitude (true flight via Featherin wings), the player reads the battlefield, selects AoE/cleave targets, "loads" the dive trajectory, then commits. Dive trajectory is fixed once initiated. On landing: massive damage resolves, then the Strix is GROUNDED and vulnerable (hollow bones, STR 6, SPD 15). Skill expression is in the READ and the COMMIT — not in execution. The player must be right BEFORE they dive because they can't adjust during or recover after a bad dive.

### Item Baseline (What a Party Uses WITHOUT This Class)

| # | Item Name | Strategic Function | Why It's Worse Than the Class |
| --- | --- | --- | --- |
| 1 | **Upheaval Flask** (existing) | AoE eruption (3m radius, launches enemies airborne 1.5s) — the "burst AoE from above" analog | Deals moderate damage, launches enemies UP (not player going DOWN), 1.5s window is fixed (doesn't scale with setup time), no pre-calculation phase, no persistent altitude advantage between uses |
| 2 | **Brineshelf Compound** (existing) | Creates a 2m×2m elevated platform (1.5m high) — the height advantage item | Static, 3s crystallization delay, only 1.5m elevation (not true flight altitude), doesn't provide DIVE capability from height, exposes you to anti-air without escape route |
| 3 | **Springboard Disc** (existing) | Launch 6m upward + 4m directional — the vertical mobility item | Fixed point (must return to disc), doesn't sustain you in the air (you come back down immediately), no sustained aerial reconnaissance, can't "hover" to read the battlefield |
| 4 | **Charcoal Pine Bundle** (DS3 reference) | Thrown fire projectile — gives melee a ranged poke | Fixed damage, no AoE, no pre-calculation reward, doesn't scale with positioning, single use. The Strix's dive IS the ranged-into-melee attack but does AOE damage scaled by altitude. |
| 5 | **Aerial Vantage Scope** (new) | Consumed: for 10s, reveals all enemies on the current floor from a "bird's eye" perspective on HUD — the reconnaissance item | 10s only, only provides INFORMATION (no damage), requires stopping to "use" the scope, doesn't provide ongoing altitude-vision, doesn't enable engagement from the information |
| 6 | **Gravwell Orb** (existing) | Clusters enemies together (4m radius pull, 3s) — the "set up my AoE" item | 3s clustering only, requires immediate follow-up with a SEPARATE damage action, doesn't provide the damage itself, thrown from ground level (no altitude selection). The Strix's pre-calculation INCLUDES target clustering into the dive path. |
| 7 | **Concussion Charge** (existing) | Directional blast (90° cone, 6m, pushes 4m) — the area damage + displacement combo | 2s delay, ground-level only, fixed direction at placement, no altitude selection, damage is moderate. The Strix hits from ABOVE with kinetic mass + velocity — fundamentally different damage profile. |

### The Class Advantage (Why Pick The Class Over Items)

The Strix provides **persistent altitude as a strategic resource**. No item sustains a character in the air for extended periods, allowing them to continuously read the battlefield, select optimal dive targets, and wait for the perfect moment. Items provide one-shot AoE or brief elevation — the Strix provides ONGOING aerial dominance between dives. The pre-calculation phase is exclusive to the class: items are reactive (throw NOW), the Strix is proactive (read → calculate → commit → devastate). The damage scaling from altitude × mass × velocity means the Strix's burst exceeds any thrown consumable by design. And SPD 15 means even when grounded, the Strix can escape back to air faster than enemies can punish.

### Strategic Problems This Class Solves

1. **"Enemies are clustered but our AoE items require ground-level access which is too dangerous"** — The Strix attacks from altitude, bypassing ground-level threats entirely during the approach.
2. **"We need burst damage but can't tell which targets to prioritize from ground level"** — Altitude provides complete battlefield vision. The Strix sees everything and chooses the optimal dive.
3. **"Enemies are using elevation or cover and our ground-based attacks can't reach them"** — The Strix attacks from ABOVE. Cover and elevation that protect against horizontal attacks are meaningless against vertical dives.
4. **"We need reconnaissance without committing a scout to danger"** — The Strix's sustained flight IS the scouting. No item expenditure, no commitment — just flying overhead and reading.
5. **"We need a DPS who can wait for the perfect moment without losing DPS uptime"** — Airborne time is "setup" time that makes the dive MORE lethal (better target selection, more precise AoE placement). Other DPS lose damage by waiting; the Strix gains it.

### Open Design Questions

- Altitude abstraction — continuous (real height in meters) or tiered (low/med/high states)? Continuous allows more nuance but is harder to communicate to the player.
- Anti-air counterplay — what threatens the Strix while airborne? If nothing, altitude is risk-free and the class degenerates into "always stay up, dive only on cooldown."
- Ground recovery time — how long is the Strix vulnerable post-dive? Fixed state duration or "until you re-ascend" (with re-ascend requiring time/resource)?
- Dive damage scaling formula — does altitude directly multiply damage? Is there a sweet spot (too high = less accurate, too low = less kinetic energy)?

---

## Wavecaller — Item Baseline

### What This Class Does (Strategic Summary)

The Wavecaller is the aggressive healer with positional tension. Sound-based healing (vocalization, possibly no LoS requirement via sound propagation) is strongest at RANGE. Damage comes from water portal generation → dive through → physical melee impact → emerge. The core tension: stay back and heal optimally, or dive forward for damage and accept suboptimal healing. Constant push/pull between safe healing position and aggressive damage position. The player's skill is knowing WHEN the party can survive reduced healing while they dive.

### Item Baseline (What a Party Uses WITHOUT This Class)

| # | Item Name | Strategic Function | Why It's Worse Than the Class |
| --- | --- | --- | --- |
| 1 | **Healing Specter** (ToS reference) | Deployable healing zone — positional AoE healing | Stationary, doesn't propagate through walls, allies must STAND IN IT, duration-limited. Wavecaller's sound healing reaches through obstacles and doesn't require allies to cluster. |
| 2 | **Rejuvenation Flask** (new) | Thrown AoE burst heal (2m radius, 20% HP) — emergency healing | Single use, small radius, requires aim, flat magnitude. Wavecaller healing is continuous, no-LoS, and scales with vocalization intensity. |
| 3 | **Flashstep Cartridge** (existing) | 8m directional teleport — gap closer for aggression | Single use, no damage on arrival, 8m fixed distance, no return mechanism. Water portal provides gap close + damage ON ARRIVAL + potential return route. |
| 4 | **Retrograde Bead** (existing) | Mark position → recall to it within 20s — the "dive and return" tool | 20s window, requires pre-placement, SR3 enemies camp the recall point, single use. Water portals can potentially be two-way AND instant AND repeated. |
| 5 | **Resonance Crystal** (new) | +15% healing received in 4m radius (installation, 15s) — healing amplification | Positional, no baseline healing, 15s duration, amplifies other healing (useless alone). Wavecaller doesn't need amplification — sound IS the healing. |
| 6 | **Concussion Charge** (existing) | Directional blast (area damage) — the "I went in and need to hit things" tool | 2s delay, ground-placed, can hit allies, no return mechanism, no healing component. Water portal dive IS the damage without needing a separate item for the offensive moment. |
| 7 | **Smokebreak Ampule** (existing) | 4m radius untargetable smoke (5s) — safety after aggression | 5s safety but you CAN'T ATTACK in the smoke either, stationary, single use. Wavecaller heals AT RANGE (already safe) and only enters melee by choice through portals. |
| 8 | **Springboard Disc** (existing) | Vertical repositioning — movement utility | Fixed position, reusable but stationary. Water portals are generated anywhere, provide traversal through any space, and deal damage at the destination. |

### The Class Advantage (Why Pick The Class Over Items)

The Wavecaller unifies healing + gap-close + damage + return into a SINGLE integrated kit. Items require separate slots for healing (flask), gap-closing (Flashstep), damage delivery (Concussion Charge), and safe return (Retrograde Bead). That's 4 item slots and 4 separate action commitments to achieve what one portal dive + sound healing does. The Wavecaller's sound healing also solves the "LoS healing" problem that no item addresses — healing that propagates through walls means the healer doesn't need sight lines to allies. And the constant push/pull of portal aggression vs. safe-position healing creates DECISION DENSITY that no item collection matches.

### Strategic Problems This Class Solves

1. **"Our healer needs LoS to heal but enemies are pressuring from around corners"** — Sound propagates through/around obstacles. Wavecaller heals without sight lines.
2. **"We need burst melee damage on a target but our healer can't abandon the backline"** — Water portal dive delivers damage WHILE sound healing continues (reduced output). The healer IS the burst DPS at the cost of healing efficiency.
3. **"We need to cross water terrain / gap / obstacle that items require multiple uses to solve"** — Water portals traverse any space water can occupy. No item budget spent on traversal.
4. **"Enemies are between our healer and the party and we can't reach them to protect the healer"** — The Wavecaller can portal THROUGH threats to rejoin the party or portal threats away from themselves.
5. **"We need a healer who can punish overextended enemies without losing the healing role entirely"** — Portal dive is a calculated aggression tool: the Wavecaller decides when reduced healing output is acceptable for burst damage.

### Open Design Questions

- Sound healing no-LoS — how powerful? If full throughput ignores walls, positioning becomes irrelevant for healing. Needs a degradation model (weaker through walls? reduced by distance?).
- Portal return — one-way or two-way? If two-way, the dive has no commitment. If one-way, the Wavecaller must walk back (or enemies can enter the portal behind them?).
- Distinction from Siren — both are voice-based healers. Siren = voice commands enemies, Wavecaller = voice heals allies. In practice, do these FEEL different enough?
- Positional tension tuning — is there a mathematical sweet spot where diving is approximately equal-value to staying back? Or is one clearly dominant at different SR tiers?

---

## Elementalist — Item Baseline

### What This Class Does (Strategic Summary)

The Elementalist is the flexible reactive answer. Element-based DPS/healing hybrid that adapts to environmental demands — fire for damage, water for healing, earth for shielding/CC, wind for mobility/disruption. The Tryll academic tradition studies ALL elements. The value proposition is that no situation is unanswerable — the Elementalist always has the right element for the current problem. Self-defense through CC and shielding (not healing self), team healing through water magic. Replaces: potions, elemental coatings, AoE consumables, terrain manipulation items.

### Item Baseline (What a Party Uses WITHOUT This Class)

| # | Item Name | Strategic Function | Why It's Worse Than the Class |
| --- | --- | --- | --- |
| 1 | **Conductance Gel** (existing) | +40% lightning vulnerability to enemies (3m radius, 15s) — elemental vulnerability application | Only lightning, requires a teammate with matching element to capitalize, 15s duration, single use, does nothing on its own. Elementalist applies AND exploits vulnerability simultaneously. |
| 2 | **Gold Pine Resin** (DS reference) / **Grease** (BG3 reference) | Weapon element coating (10 turns/hits) — elemental damage addition | Single element per coating, fixed duration/charges, must be pre-applied, doesn't stack, commit to one element before knowing what you'll face. Elementalist switches elements reactively mid-combat. |
| 3 | **Upheaval Flask** (existing) | AoE eruption displacement (3m, 1.5s airborne) — elemental displacement | One element (earth-coded), fixed radius, single use, 1.5s only. Elementalist casts eruptions with variable element (fire = damage zone, ice = freeze zone, earth = displacement, wind = scatter). |
| 4 | **Voidpatch Emitter** (existing) | Nullifies terrain effects in 3m radius — terrain manipulation | Only REMOVES terrain (can't create or transmute), 20s duration, stationary. Elementalist TRANSMUTES enemy terrain into allied terrain (poison field → healing field, lava → stone barrier). |
| 5 | **Rejuvenation Flask** (new) | AoE burst heal (2m, 20% HP) — water-coded healing | Single use, small radius, flat amount, can't adapt between healing and damage. Elementalist's water magic provides sustained healing with variable throughput based on need. |
| 6 | **Antarctic Wind** (FF reference) | Deals ice damage to all enemies — the "everyone can cast for one turn" item | Fixed damage, no vulnerability exploitation, no synergy with team elements, no ongoing zone creation. Elementalist's ice creates persistent freeze zones, slows, and walls. |
| 7 | **Dragon's Dream** (Witcher reference) | Gas cloud that requires fire trigger — combo setup item | Requires a SEPARATE fire source to detonate, stationary, single-use setup, doesn't chain into further reactions. Elementalist IS both the primer and the detonator — sets up and executes chains solo. |
| 8 | **Firebomb** (DS reference) | AoE fire damage, ignites environment — elemental area damage | One element, fixed radius, fixed damage, single use, doesn't create persistent terrain. Elementalist's fire creates ongoing damage zones, ignites oil (chain reaction), and scales with investment. |

### The Class Advantage (Why Pick The Class Over Items)

The Elementalist's premium is **reactive element switching and self-contained chain reactions**. Items commit you to one element (fire resin, ice bomb, lightning gel) and provide one use. The Elementalist carries ALL elements simultaneously and switches based on what the fight demands RIGHT NOW. It also combines elements — setting up its own combos (oil → fire → steam → lightning arc) without consuming multiple item slots. The adaptation speed is the core premium: where items require pre-fight prediction ("I THINK I'll need ice so I'll bring Antarctic Wind"), the Elementalist responds to CURRENT reality.

### Strategic Problems This Class Solves

1. **"We don't know what element the boss is weak to and can't afford to bring all elemental coatings"** — The Elementalist tests and switches mid-fight. No wasted item slots.
2. **"We need healing AND elemental damage AND terrain control but those are three different item categories"** — The Elementalist is all three roles through element switching.
3. **"Enemy terrain (poison pools, lava, ice patches) is degrading our positions and we need to counter it"** — Voidpatch Emitter removes terrain. The Elementalist TRANSMUTES it — turning enemy hazards into party advantages.
4. **"We need sustained elemental chain reactions but items are one-shot primers/detonators"** — The Elementalist IS the chain reaction engine — continuous primer + detonator in one class.
5. **"The fight's demands change between phases and our item loadout was wrong for phase 2"** — Items are committed at prep time. The Elementalist adapts to every phase without preparation.

### The Class Advantage (Why Pick The Class Over Items) — Extended

Additionally: the Elementalist's self-defense (CC + shields, not self-healing) means it survives without consuming the party's healing resources. Items for self-defense (Stoneskin Scroll, Shield Generator) are single-use. The Elementalist's earth shields and wind displacement are PERMANENT kit tools.

### 2-Minute Bias Audit

**Mechanics that assume fixed burst windows or rotation cadences:**

- If the Elementalist has an "element rotation" (cycle through fire → ice → earth → wind in order), this imposes a cadence. The element available at any given time becomes predictable rather than reactive.
- If elemental convergence (combining elements for ultimate effects) requires "building up" each element sequentially over a fixed timeframe, this creates a 2-minute burst analog: accumulate for 90s, converge for 10s, repeat.
- If mana/resource recovery follows fixed intervals that dictate when the Elementalist can afford to swap elements, this creates an implicit rotation cadence (cheap element → expensive element → recovery → repeat).

**Reframing as RESPONSES TO STRATEGIC PROBLEMS:**

- Element switching should be triggered by ENEMY BEHAVIOR, not by internal cooldowns. The Elementalist swaps to ice BECAUSE the enemy is charging, not because "ice is next in the rotation."
- Convergence (multi-element ultimate) should respond to PARTY NEED — "we need burst NOW because the boss is about to phase" — not accumulate on a timer. Convergence availability should track with encounter pressure, not internal clock.
- Resource recovery should be tied to STRATEGIC DECISIONS: "I used earth shielding to protect the party from that AoE, now I'm low on earth resource and must use water/fire until earth recovers." The recovery creates vulnerability windows that the ENCOUNTER exploits, not a fixed cycle the player memorizes.

**Items as baseline for elemental damage/healing/CC:**

- Elemental DAMAGE: Firebomb, Antarctic Wind, Grease coatings, Charcoal Pine Bundle. All single-use, single-element, fixed magnitude.
- Elemental HEALING: Rejuvenation Flask, Healing Specter, Harmony Draught. All duration-limited, positional, non-scaling.
- Elemental CC: Upheaval Flask (displacement), Bogcrust Grenade (difficult terrain), Thornveil Seed (barrier + slow). All single-use, fixed shape, non-reactive.
- The Elementalist replaces ALL of these by being a permanent, adaptive, scaling source of any element the situation demands. The bias audit ensures it does so REACTIVELY (responding to problems) rather than CYCLICALLY (following a rotation).

### Open Design Questions

- STR 6/STAM 6 Tryll baseline — potency adjustment mandatory. How much does equipment normalize this vs. how much is the Elementalist simply squishier by design?
- Fire degeneration on flat maps — if room geometry doesn't force element switching, fire (pure damage) dominates. Map design MUST create problems that demand non-fire elements.
- Water healing throughput vs. dedicated healer classes — is Elementalist a viable PRIMARY healer, or always a secondary/supplement?
- Element recovery rates per element — should fire (the aggressive element) recover fastest (enabling spam) or slowest (forcing diversity)?

---

## Shaman — Item Baseline

### What This Class Does (Strategic Summary)

The Shaman makes enemies less dangerous. It is the debuffer/attrition/denial caster: accuracy curses, speed reduction, action nullification (paralysis), damage suppression, awareness reduction, economy disruption, and aggro delegation to installations/summons. The Shaman is SLOW (matches its race's isolative tradition) and replaces the ENTIRE debuff/CC consumable catalog as a premium class solution. Secondary healer through life-drain mechanics (Blood Sucking/Hex Drain equivalent — lower DPS tradeoff). The party with a Shaman fights EASIER enemies; the party without a Shaman fights the enemies as-designed and spends items to compensate.

### Item Baseline (What a Party Uses WITHOUT This Class)

| # | Item Name | Strategic Function | Why It's Worse Than the Class |
| --- | --- | --- | --- |
| 1 | **Scatterlung Phial** (existing) | -30% accuracy (3m radius cloud, 12s) — the accuracy debuff item | Stationary cloud, 12s only, -30% (not scaling), enemies can leave. Shaman's accuracy curse follows targets, stronger magnitude, no duration limit while maintained. |
| 2 | **Thickglass Flask** (existing) | -50% movement / -25% attack speed (4m puddle, 20s) — the speed reduction item | Stationary puddle, enemies can leave, 20s duration, doesn't follow. Shaman's speed curse attaches TO the enemy — no escape, no terrain dependency. |
| 3 | **Lockjaw Spore** (existing) | -20% speed + 25% action skip (3m cloud, 15s) — the paralysis item | 25% is probabilistic (unreliable), 15s duration, stationary, enemies can leave. Shaman provides GUARANTEED action suppression on marked targets with controllable timing. CC Stage: 2-3 |
| 4 | **Fogmind Censer** (existing) | Reduces enemy AI by one SR for 12s — the awareness reduction item | Single use, 12s only, doesn't affect SR4 enemies, radius-based (6m burst). Shaman provides sustained AI suppression, longer duration, potentially affecting SR4 (class-level solutions breach the item ceiling). |
| 5 | **Witherfield Totem** (existing) | -20% damage/-20% speed/-20% attack speed (4m installation, 25s) — the "mini-Shaman" item | Destroyable at SR3+ (3 hits), 25s duration, weaker magnitudes, single installation. Shaman's totem is INDESTRUCTIBLE, stronger effects, and the Shaman can deploy MULTIPLE. |
| 6 | **Hollowform Decoy** (existing) | Aggro redirect to a deployable target (8m range, 15s) — the aggro delegation item | 15s duration, 5-8 HP (destructible), doesn't DO anything beyond absorbing aggro. Shaman spirit effigy REFORMS when destroyed, has unlimited duration, and can COUNTERATTACK. |
| 7 | **Stasis Pin** (existing) | Total freeze (3s, single target) — the hard CC item. CC Stage: 3 | 3s only, single use, requires hitting, no reapplication. Shaman provides longer stasis with reapplication and no projectile accuracy requirement. |
| 8 | **Drainwick Candle** (existing) | -50% resource regen (3m installation, 20s) — the economy disruption item | Stationary, 20s, only suppresses regen (doesn't drain). Shaman actively DRAINS resources — theft, not just suppression — accelerating enemy depletion. |

### The Class Advantage (Why Pick The Class Over Items)

The Shaman replaces approximately **8-12 consumable items worth of value per encounter** through persistent, reusable, stronger-magnitude class abilities. The core premiums:

- **Persistence**: Shaman curses don't expire on timers. They persist while maintained.
- **Targeting**: Curses follow enemies (no stationary clouds to walk out of).
- **Multi-target**: Shaman affects multiple enemies simultaneously where items are single-target or small-radius.
- **No consumable cost**: Frees the entire party's inventory from debuff/CC item slots.
- **SR4 breach**: Items explicitly cannot handle SR4 enemies. Shaman can.
- **Installation superiority**: Shaman totems are indestructible, self-repairing, and multi-effect where item installations have HP and get destroyed by SR3+ enemies.
- **Life-drain secondary healing**: Items don't heal by debuffing. Shaman's Hex Drain is a heal that COMES FROM enemy degradation — uniquely efficient.

### Strategic Problems This Class Solves

1. **"SR3+ enemies destroy our installations and ignore our debuff items"** — Shaman installations are indestructible. Shaman curses have no dodge, no destroy, no resist (class-level solutions breach item limitations).
2. **"We're running out of debuff/CC items mid-dungeon and can't sustain control"** — Shaman never runs out. No consumable economy for debuff effects.
3. **"We need MULTIPLE debuffs on MULTIPLE enemies simultaneously and items are single-target"** — Shaman maintains multiple curses across multiple targets as core gameplay.
4. **"SR4 enemies are too reactive for items — they dodge thrown items, destroy traps before activation"** — SR4 is explicitly the "class solutions required" tier. Shaman curses bypass dodge/destroy.
5. **"We need a healer who doesn't sacrifice damage/control to heal"** — Hex Drain heals FROM enemy debuffing. The healing IS the offensive action. No role-switching required.

### 2-Minute Bias Audit

**Mechanics that assume fixed burst windows or rotation cadences:**

- If the Shaman has a "curse rotation" (apply accuracy debuff → wait for it to "mature" → apply speed debuff → wait → apply paralysis → burst window where all curses peak simultaneously), this creates a burst cadence. The 30-40s where curses build up, followed by a "peak" where enemies are maximally debilitated, followed by a reset — is a 2-minute cycle in disguise.
- If Bone/Spirit summon deployment follows a "deploy → buff up → unleash → cooldown" pattern, the summon becomes a burst tool on a fixed cycle rather than a persistent asset.
- If Hex Drain healing is gated behind a "build up curse intensity over X seconds, then drain" mechanic, this creates fixed accumulation windows that mirror burst healing cadences.
- If totem deployment has a "setup phase" where the Shaman does reduced DPS while placing totems, then a "payoff phase" where totems are active and the Shaman does full DPS — this is a burst cadence with extra steps.

**Reframing as RESPONSES TO STRATEGIC PROBLEMS:**

- Curses should be applied in response to ENEMY ACTIONS, not on a timer. Enemy starts casting? Apply action nullification NOW. Enemy starts moving toward backline? Apply speed reduction NOW. The trigger is enemy behavior, not internal cooldown rotation.
- Installations should be placed in response to MAP GEOMETRY and ENEMY SPAWNS, not as a "setup phase." The Shaman reads the room and deploys totems where they address the CURRENT threat map — not where the rotation says to place them.
- Hex Drain should activate when the Shaman CHOOSES to prioritize healing over control intensity — not when a resource bar fills up. It's a real-time cost/benefit decision: "I could maintain this curse at full power OR drain it for healing. Party HP determines which."
- Bone Spirit deployment should respond to "I need a persistent body holding this corridor" — a MAP POSITION problem — not "my summon cooldown is up."

**Items as baseline for debuffs/slows/installations/interrupts:**

- DEBUFFS: Scatterlung Phial (-30% accuracy), Siphonwax Pellet (-30% damage), Dulleye Canister (-20% accuracy, -crit). All duration-limited (8-15s), stationary or single-target, single-use.
- SLOWS: Thickglass Flask (-50% move, -25% atk speed), Frostweave Net (-70% all speeds), Muddling Tincture (stacking -45%). All positional, duration-limited, breakable.
- INSTALLATIONS: Witherfield Totem (multi-debuff), Hexcage Lantern (detection), Drainwick Candle (resource drain). All destroyable at SR3+, duration-limited, fixed effects.
- INTERRUPTS: Stupor Bell (AoE interrupt, one-time), Vasselroot Extract (guaranteed next-action nullify). Single-use, no persistence.
- The Shaman replaces this entire catalog with PERMANENT, TARGETING, SCALING, INDESTRUCTIBLE versions. The bias audit ensures the Shaman deploys these in response to STRATEGIC DEMAND rather than following a fixed application order.

### Open Design Questions

- Curse maintenance cost — maintaining multiple curses simultaneously should have a resource tension. What prevents "apply everything always"?
- Slow class identity — how does "SLOW" manifest mechanically? Long cast times? Low mobility? If the Shaman is slow but curses are instant-apply, where is the weakness?
- Totem count limit — how many simultaneous installations? Unlimited installations break map control if positioning is correct.
- Hex Drain healing throughput vs. dedicated healers — is Shaman a viable solo healer, or always secondary?
- SR4 interaction — if Shaman CAN breach SR4 limitations that items cannot, what makes SR4 still challenging for a party WITH a Shaman?

---

## Cross-Reference: Item Categories by Class Replacement

| Item Category | Items in Catalog | Primary Class Replacement | Secondary Class Interactions |
| --- | --- | --- | --- |
| Accuracy Reduction (4 items) | Scatterlung Phial, Glintjam Paste, Dulleye Canister, Mirage Salt | **Shaman** | Siren (commands override targeting accuracy indirectly) |
| Speed Reduction (4 items) | Thickglass Flask, Chronotar Bead, Frostweave Net, Muddling Tincture | **Shaman** | Elementalist (ice element provides speed reduction) |
| Action Nullification (4 items) | Lockjaw Spore, Stupor Bell, Vasselroot Extract, Tanglesynapse Dart | **Shaman** | Siren (forced actions ≈ nullified intended actions) |
| Damage Reduction (4 items) | Siphonwax Pellet, Marrowchill Bomb, Bluntveil Incense, Featherstrike Resin | **Shaman** | Siegebreaker (absorbs damage, reducing effective party damage taken) |
| Awareness Reduction (4 items) | Fogmind Censer, Scatterthought Thorn, Befuddlement Smoke, Memoryburn Ash | **Shaman** (+ Madolt Warrior Unfocus) | Nightfly Colony (darkness control reduces awareness) |
| Vulnerability Application (4 items) | Brittlemark Chalk, Conductance Gel, Harmonic Stake, Rupture Oil | **Elementalist** (elemental vuln) / **Shaman** (general vuln via totems) | Reaver (damage ramp on single target ≈ vulnerability through DPS) |
| Economy Disruption (4 items) | Voidleech Capsule, Drainwick Candle, Backlash Glyph, Atrophy Mist | **Shaman** | — |
| Sensory Impairment (2 items) | Blindveil Powder, Numbsense Spike | **Shaman** | Nightfly Colony (darkness), Grappler Ink stance |
| Terrain Creation (5 items) | Quartzwall Capsule, Bogcrust Grenade, Brineshelf Compound, Thornveil Seed, Voidpatch Emitter | **Colony Builder** / **Elementalist** | Shaman (spirit-vine barriers) |
| Enemy Displacement (5 items) | Concussion Charge, Gravwell Orb, Ripcord Harpoon, Slipgate Mine, Upheaval Flask | **Grappler Long-range** / **Elementalist** | Wavecaller (portal displacement?) |
| Movement Denial (5 items) | Ironvine Snare, Permafrost Band, Leadweight Tonic, Barricade Foam, Stasis Pin | **Shaman** / **Grappler Melee** | Elementalist (ice walls, root zones) |
| Attention Manipulation (5 items) | Hollowform Decoy, Pheromone Tag, Taunt Cracker, Phantom Echo, Rivalmark Dust | **Siren** / **Shaman** (installations) | — |
| Escape/Repositioning (5 items) | Flashstep Cartridge, Retrograde Bead, Smokebreak Ampule, Springboard Disc, Ghoststep Chalk | **Wavecaller** (portals) / **Strix** (flight) / **Flutter Colony** | Grappler Long-range (escape via displacement) |
| Installations/Traps (5 items) | Hexcage Lantern, Rattletrap Mine, Witherfield Totem, Webspinner Sac, Nullfield Generator | **Shaman** (totems) / **Colony Builder** | Nightfly Colony (lure-traps) |
| Healing/Recovery (10 items from reference) | Mega Elixir, Divine Blessing, Estus, Healing Specter, etc. | **Spiritcaller** / **Wavecaller** / **Elementalist** / **Siren** | — |
| Offensive Buffs (12 items from reference) | Demon Powder, Might Potion, Pine Resin, etc. | **Reaver** (self-ramp) / **Strix** (dive burst) | — |
| Tracking/Pursuit (items invented above) | Bloodhound Capsule, Berserker's Draught | **Reaver** | — |

---

## Design Validation Checklist

For each class to pass the Item Baseline test:

- [ ] Can a party WITHOUT this class still accomplish the same strategic goals using items? (Must be YES)
- [ ] Is the item solution meaningfully WORSE? (Limited charges, shorter duration, weaker effect, requires setup, no scaling)
- [ ] Does the class provide something items CANNOT? (Persistence, adaptation, scaling, no carry limit, kit synergy)
- [ ] Are the strategic PROBLEMS clear? (What creates DEMAND for this class over items?)
- [ ] Does the class solve problems that arise when items RUN OUT or AREN'T ENOUGH? (SR3+, extended encounters, multi-target, resource attrition)

If any class fails this checklist, it either:

1. Does something no item can do at ANY level → violates "items define baseline" principle → needs item analogs designed
2. Does the same thing items do at the same quality → no class premium → needs class power increased
3. Has no clear strategic demand → role is poorly defined → needs strategic problem identification

---

## Next Steps

1. **Quantify item magnitudes** — resolve consumable effect numbers (carry limits, durations, magnitudes) so class "premium" can be measured against a concrete baseline
2. **Map geometry primitives** — define room sizes, elevation tiers, corridor widths so positional items/classes can be validated spatially
3. **SR4 interaction rules** — define what SR4 enemies DO that makes items fail and classes succeed
4. **Phenotype permanence decision** — Colony needs its character creation vs. spec choice question answered before item baseline can be finalized
5. **Cross-class chain reactions** — map which classes can COMBO with which items (Pyrien fire + Dragon's Dream gas, Elementalist oil + Shaman fire totem, etc.)
6. **Economy integration** — connect item production to Nom gem-craft pipeline, validate that the item catalog maps to racial manufacturing lore

