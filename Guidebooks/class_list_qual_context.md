# Class List — Qualitative Context Pass

**Purpose:** Add qual context to every class so we can work backwards (Qual_class → Qual_strat → Quant).  
**Source:** Classes/Class_Library.yaml + session design decisions.

---

## Base Available (No Merc gate, easy rank-1 on-ramp)

### 1. Adafold (Shield Knight)
- **Race:** Rawrotin (Linfree) — bodyguard/courier
- **Role:** Tank (Force Targeting)
- **Mechanic:** Bulwark Gauge (builds by blocking/mitigating)
- **Strategic Role:** Physically contain enemies. Collision-based control.
- **Replaces (items):** Barricade items, decoys
- **YAML Status:** ✅ Complete (Revised), 70KB
- **Qual Context:** Designed as the frontline who follows more traditional tank design within our constraints. Stamina / STR focus.

### 2. Warrior (Madolt Warrior)
- **Race:** Madolt (Landwin) — precision engineer
- **Role:** Frontliner (NOT "tank" — damage-first)
- **Mechanic:** Charge Gauge → EC Weapon/Shield Discharge
- **Strategic Role:** Suppress enemy intelligence + deal damage. Unfocus = AI suppression. Capacitor Pull.
- **Replaces (items):** Flash/distraction items
- **YAML Status:** ✅ Complete (Revised v3), 71KB
- **Qual Context:** Strategic role maps to what other races' versions should do, but Madolt uses NTU as basis of damage design (reacting to enemy) instead of STR. Fixed damage design + percent design instead of pure scaling DEX for EC ranged attacks and shot bursts (matters).

### 3. Rogue
- **Race:** Unassigned (Nyanto? Mantidia?)
- **Role:** DPS
- **Mechanic:** —
- **Strategic Role:** -
- **Replaces (items):** —
- **YAML Status:** 🔴 Undesigned
- **Qual Context:** DPS. Steathily move ahead of team or behind enemies for backstab or CC. Critical hit focused. Crit is NOT RNG. It needs a character to hit from the back or use special guarantee skills that take advantage of CC'd enemies or "flank vulnerable" to attack from the side. Evasion focused with boosters similar to ToS scout > Rogue that make it deceptively tanky but turn into glass if targeted by too many enemies (EVA penalty). Designed for fast races.

### 4. Archer
- **Race:** Unassigned (Featherin? Soue non-Shaman branch?)
- **Role:** DPS (free-aim, stealth, travel-time projectiles, shot arc)
- **Mechanic:** —
- **Strategic Role:** —
- **Replaces (items):** —
- **YAML Status:** 🔴 Undesigned (identity discussed: fundamentally different input, 1st person?)
- **Qual Context:** DPS. Anything able to hold a bow can use this class. The uniqueness from race depends on how they enchant the bow, but many shots will operate similarly. The stealth benefit relies on ease of position, so items for scaling terrain or Quarrel Shooter Deploy Pavise equivalent are going to matter if the race has no alternative i.e. Midnight has racial armor with a block effect that can apply and make a much tankier archer.

### 5. Elementalist
- **Race:** Tryll (Landwin) — academic tradition, all-element study
- **Role:** Healer/DPS
- **Mechanic:** Elemental Convergence (5 elements cross-consume)
- **Strategic Role:** Flexible response to environment. Element-reactive.
- **Replaces (items):** Potions, elemental coatings, AoE consumables
- **YAML Status:** ✅ Complete (Approved), 65KB. ⚠️ Potency adjustment needed for Tryll STR 6/STAM 6.
- **Qual Context:**  Other racial versions will likely use fewer elements and need narrower effect trees (less flexibility but more power budget)

### 6. Body Specialist
- **Race:** Unassigned
- **Role:** —
- **Mechanic:** —
- **Strategic Role:** —
- **Replaces (items):** —
- **YAML Status:** 🔴 Undesigned
- **Qual Context:** DPS. This is a DFO MFighter (Nen Master and Striker) / FFighter (Nen Master and Striker) / FFXIV Monk / Blade and Soul Force Master inspired class. Has phys and mag variants of their skills where they can either use martial arts or spiritual strikes. STR/SPD class that has defense ignore % to make low stat variants still do damage. Weaker racial variants will need to rely more on spiritual strikes that gain bonus damage or ignore defense with passives that list excuses i.e. "As a Tryll you have mastered the martial arts against your culture's judgement. You have become enlightened toward your enemy's weaknesses." Something to justify us balancing them correctly for the fantasy vibe.

---

## Experienced (Mercenary Rank 2 + originating area)

### 7. Lancer
- **Race:** Unassigned
- **Role:** — (was "Adafold upgrade" → now sideways option)
- **Mechanic:** —
- **Strategic Role:** —
- **Replaces (items):** —
- **YAML Status:** 🔴 Undesigned
- **Qual Context:**  DPS. Not sure if this class is going to end up being a floor hugger but it's my absolute favorite concept due to Fate/Stay Night's Cu Chulainn with his signature GAE BOLG, Ara from Elsword, FFXIV Dragoon, ToS Dragoon, DFO Skirmisher, etc. Must have a throw spear skill that pins the enemy and hits AoE. Definitely a DEX/SPD + NTU with a primary focus on SPD and "jump back" gimmick akin to DFO Backstep; difficult to design realistic fight simulation so they should mostly be looking to weave in and out of the fight. I believe Blue Protocol: Star Resonance got pretty close with Wind Knight but had too many bugs with Skyward.

### 8. Dancer
- **Race:** Unassigned
- **Role:** —
- **Mechanic:** —
- **Strategic Role:** —
- **Replaces (items):** —
- **YAML Status:** 🔴 Undesigned
- **Qual Context:** A FFXIV rip, pretty shameless. I wanted more Bard / music variation though, so this class might be renamed to Fiesta to accommodate a mix between the two. No bow usage. Instead, uses a racial instrument which influences the type of buff support they offer. MAG / MAG Capacity is the main stat but they gain a Cadence or Tempo buff that boosts these two stats as long as they don't mis-time their music minigame. MUST BE ABLE TO HOLD AN INSTRUMENT. Healer/DPS.

### 9. Nightmare
- **Race:** Unassigned
- **Role:** —
- **Mechanic:** —
- **Strategic Role:** —
- **Replaces (items):** —
- **YAML Status:** 🔴 Undesigned
- **Qual Context:** FFXIV Dark Knight shameless rip inspired by Soul Caliber. Frontline that prioritizes inflicting Darkness to decrease enemy vision max distance instead of Strategy rank decrease, and utilizes shadow clones, HP-costing blood techniques, and berserker HP regen on-hit that rewards only taking fights Nightmare can win. Class gameplay design is definitely borrowing from Crimson Avenger / Bloody Queen with a self-res for limit testing and priority on fast gameplay. STA is the most important stat to not die horribly, followed by defense (not in attributes currently), and then STR+MAG average. Wields claymore, greatsword or shadow slicer (thin corrupted katana).

### 10. Machinist
- **Race:** Unassigned (Madolt strong fit — tech-race → tech-class)
- **Role:** —
- **Mechanic:** —
- **Strategic Role:** —
- **Replaces (items):** —
- **YAML Status:** 🔴 Undesigned
- **Qual Context:** Madolt, Nom appropriate and designed to deploy installations, bombs, summons or shoot guns. Able to copy archer to use 1st person mode and fire rockets that ragdoll enemies, mark super armor foes. They carry long-range rifles for non-hitscan precision shots that are better at mid range. DPS

### 11. Summoner
- **Race:** Unassigned (Noms? HBD? — gem-craft or dragonic pacts)
- **Role:** —
- **Mechanic:** —
- **Strategic Role:** —
- **Replaces (items):** —
- **YAML Status:** 🔴 Undesigned
- **Qual Context:** We are lacking enemy design for this one. The closest start uses a fairy like Scholar FFXIV or other cute summon like a carbuncle but we are far away from this design.

### 12. Samurai (Pyrien Samurai)
- **Race:** Pyrien (Wanderers) — fire elf, military chain-of-command
- **Role:** DPS (chain reaction PRIMER + DETONATOR)
- **Mechanic:** Flame sword DoTs → explosions
- **Strategic Role:** Apply fire debuffs then self-detonate. Or be detonated by allies.
- **Replaces (items):** Elemental oils/coatings (fire-specific, permanent uptime)
- **YAML Status:** 🔴 Undesigned (identity discussed)
- **Qual Context:** For Pyrien: Frontline that prioritizes weaving in, dealing tons of damage and using black smog cover to avoid getting focused too hard after a combo ends (rather than before). // Other samurai are intended to do similar weaves and may need to rely on passive parry / evasion to survive without external help. FFXIV is a good mockup but too much 2 min focus.

### 13. Ninja (Pyrien Ninja)
- **Race:** Pyrien (Wanderers) — fire elf, military chain-of-command
- **Role:** DPS (chain reaction DETONATOR)
- **Mechanic:** DFO Kunoichi trace — spam-cast, rapid reposition
- **Strategic Role:** Approach/burst/retreat. Triggers combustible debuffs laid by others.
- **Replaces (items):** Ignition items (detonation consumables)
- **YAML Status:** 🔴 Undesigned (identity discussed)
- **Qual Context:** Pyrien Ninja is a chain reaction detonator that otherwise is a fire caster. Other ninjas rely on some elemental basis of play when applicable and use traps heavily, along with SPD or decoys to replace the req. Stealth is not traditional; they use light footsteps passive to not be detected but otherwise need smokescreens or environment costumes like Rogues (forgot to list). Love using poisons.

### 14. Magiknight / Fencer
- **Race:** Unassigned
- **Role:** —
- **Mechanic:** —
- **Strategic Role:** —
- **Replaces (items):** —
- **YAML Status:** 🔴 Undesigned
- **Qual Context:** RDM FFXIV inspired but like ToS Fencer there are pure phys variants. DPS

### 15. Monster Eater / Specialist
- **Race:** Unassigned
- **Role:** —
- **Mechanic:** —
- **Strategic Role:** —
- **Replaces (items):** —
- **YAML Status:** 🔴 Undesigned
- **Qual Context:** BLU; it exists to steal monster skills that are eligible to register. Specialist is the racial class variant for things like Triclaw which do not follow traditional class paths.

### 16. Shaman (Soue Shaman)
- **Race:** Soue (Wanderers) — isolative forest elf, bone/spirit tradition
- **Role:** DPS/Healer (CC paradigm, debuffer)
- **Mechanic:** Bone Summon Cycle (consumable-gated, not numeric gauge)
- **Strategic Role:** Make enemies less dangerous. Accuracy debuff, slow, paralyze, delegate damage to installations.
- **Replaces (items):** Smokescreen, Paralysis Bombs, Potions
- **YAML Status:** ✅ Complete (Revised), 63KB
- **Qual Context:** As noted, uses DoTs and class locked to Soue race. This also has skin color restrictions but this isn't within scope currently.

---

## Special (Mercenary Rank 3, "almost a different game")

### 17. Dracomancer
- **Race:** Unassigned (HBD strong fit — closest to dragons, MAGICCAP 18)
- **Role:** Frontline in Dragon mode, DPS in the normal mode.
- **Mechanic:** —
- **Strategic Role:** —
- **Replaces (items):** —
- **YAML Status:** 🔴 Undesigned
- **Qual Context:** HBD exclusive, able to transform into Midnight variant, Dragonic Humanoid variant or Dragon mode. Based on Artix Entertainment's version extremely loosely; this class is about dragonic magic, dragon breath and claw strikes and bites. Dragonfable by Artix Entertainment had big dragon battles that were actually closer to what I was thinking.

### 18. Tribalist
- **Race:** Unassigned
- **Role:** —
- **Mechanic:** —
- **Strategic Role:** —
- **Replaces (items):** —
- **YAML Status:** 🔴 Undesigned
- **Qual Context:** This is based on what Dragon Saga online made me think of when I saw Savage, but I was disappointed when it wasn't. Bone claws are the default weapon. They have laced poison in their strikes and various tools like bolas, nets, and darts. Like Shamans, they also can lay curses but are a frontline class. Racially locked to wilder races like Nyanto, Rawrotin, Triclaw, etc.

### 19. Magical Girl
- **Race:** Unassigned
- **Role:** —
- **Mechanic:** —
- **Strategic Role:** —
- **Replaces (items):** —
- **YAML Status:** 🔴 Undesigned
- **Qual Context:** Not racially locked. Tons of inspiration to draw from here like Metamorphy from Elsword, Sailor Moon, Cardcaptor Sakura, and many more. Designed to be girly and cute but pack a punch. And yes males can play it because it's funny to me. Healer obviously.

### 20. Calvary
- **Race:** Unassigned
- **Role:** —
- **Mechanic:** —
- **Strategic Role:** —
- **Replaces (items):** —
- **YAML Status:** 🔴 Undesigned
- **Qual Context:** Rider class designed around ToS Cataphract / Lancer. Able to ride magic beasts, but these aren't designed yet. This class will have to wait. Frontline default.

### 21. Beast Master
- **Race:** Unassigned
- **Role:** —
- **Mechanic:** —
- **Strategic Role:** —
- **Replaces (items):** —
- **YAML Status:** 🔴 Undesigned
- **Qual Context:** Same situation as summoner, needs enemy NPCs to pull a catalog from.

---

## Notes

- **"Qual Context" = your design intent.** What should this class FEEL like? What game/class is it traced from? What fantasy does it sell? What does the player DO moment-to-moment?
- **We work backwards from here:** Qual_class → Qual_strat → Quant values. Each class's qualitative identity tells us what strategic problems it solves, which tells us what numbers it needs.
- **Classes ≠ unique per race.** ToS-scale: races share archetypes but vary on execution specialty. Multiple races may eventually access the same class name with different kits.
- **Potency note:** Any class locked to a low-stat race (Tryll, Featherin) needs potency adjustment to compensate in early testing before equipment normalization.
