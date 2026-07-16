# DESIGN_OVERRIDE_FRONTLINE.md

## Frontliner Subcategory Taxonomy — Authoritative Definitions

### Overrides §3b of DESIGN_OVERRIDE.md. This document is the canonical reference for frontliner subcategories.

---

## Purpose

This document defines frontliner subcategories as **race-agnostic mechanical archetypes**.
These are BEHAVIOR PATTERNS, not racial identities. Any race could theoretically express
any subcategory through different flavor. The categories exist independently of any
specific class that currently fills them.

---

## §F1. The Frontliner Contract (Universal)

All frontliners share ONE contract with the party:

> **Redirect traffic. DPS and healers must be unbothered.**

Expression: Force enemy MOVEMENT or answer enemy INTERACTIONS directly.

Every frontliner fulfills this contract. The subcategory defines HOW.

---

## §F2. Subcategory Definitions (Mechanical Only)

### Zone Control

**Definition:** I dictate what happens at specific positions. Enemies at those positions
are at a clear disadvantage — not necessarily dead, but disadvantaged. I control the SPACE.

**Mechanical behavior:**
- Persistent area effect tied to positions on the ground
- Enemies inside the zone suffer escalating consequences for staying
- The zone itself does the work — the class maintains/empowers it
- Enemies must choose: leave (redirected) or stay (disadvantaged)

**What it is NOT:**
- Not defined by any specific damage type (could be electrical, fire, poison, holy)
- Not defined by the caster's race or physicality
- Not "killing everything in the zone" — it's about DISADVANTAGE, not necessarily death
- Not always ground-based (could be a vertical column, a sphere, etc.)

**Does it matter that enemies aren't oneshot?** No. What matters is that the character
has impact on XYZ positions. Enemies at those positions are worse off BECAUSE the zone
exists. That's zone control.

---

### Pinpoint Defense

**Definition:** I reactively answer specific individual threats aimed at my team.
Single-target interception, redirection, escort.

**Mechanical behavior:**
- Identifies a specific threat (one enemy, one attack, one ability)
- Responds to THAT threat directly (intercept, redirect, interrupt, block)
- Ally-aware — the value is measured in "threats neutralized FOR the team"
- Reactive timing — responds to what enemies do, not pre-placed

**What it is NOT:**
- Not area denial (that's zone control)
- Not broad coverage (covers one thing at a time)
- Not proactive placement — it's REACTIVE to emerging threats
- Not defined by shield/armor/race — a psychic catching an arrow is pinpoint defense

---

### Cropduster

**Definition:** I blanket broad areas with damage/denial drops. Wide AoE coverage
over large spaces, not precision targeting.

**Mechanical behavior:**
- Covers a BROAD area (wider than zone control — think field-scale, not room-corner)
- Delivery is mobile or from a position enemies cannot easily contest
- The "drops" deny ground TRANSIENTLY — pass over, deny, move on
- Does NOT hold a single point indefinitely (contrast with zone control which persists)

**What it is NOT:**
- Not defined by flight (flight is ONE delivery method — mortars, summoned rain, etc.)
- Not defined by race (a dragon breathes, a mage rains fire, an engineer carpet-bombs)
- Not about armor restrictions (irrelevant to the mechanical behavior)
- Not precision (that's pinpoint defense) — it's BROAD and SWEEPING
- Not persistent (that's zone control) — it's TRANSIENT passes over areas

**Key distinction from Zone Control:** Zone control says "this SPOT is mine, stay and suffer."
Cropduster says "I just PASSED OVER this entire area and everything in it got hit."
Zone = persistent point. Cropduster = transient area.

---

## §F3. Simultaneous Field Membership

Classes are NOT limited to one subcategory. A class occupies multiple fields
simultaneously with PRIMARY and SECONDARY weighting:

| Class | Primary | Secondary | Tertiary |
|-------|---------|-----------|----------|
| MetaKnight | Zone Control | Pinpoint Defense | — |
| Adabold | Pinpoint Defense | Zone Control | — |
| Skyreign (Dragon form) | Cropduster | Zone Control | — |

**MetaKnight as Zone Control + Pinpoint Defense:**
- PRIMARY: CC field (tase stacks) controls positions — enemies inside get locked down
- SECONDARY: EC Ballistic (single-target knockback launcher), targeted stun, ranged interrupt

**Adabold as Pinpoint Defense + Zone Control:**
- PRIMARY: MBAS (intercepts specific threats to specific allies), Redirection, Shield Lob
- SECONDARY: Shield Projection (blocks a corridor — that's area denial in one direction)

**Skyreign Dragon Form as Cropduster + Zone Control:**
- PRIMARY: Broad aerial sweeps, breath charge drops over large areas
- SECONDARY: Breath zones persist on ground after pass (becomes zone control temporarily)

**Important:** Skyreign has MULTIPLE FORMS. Dragon form demonstrates cropdusting.
The entire class cannot be "the cropduster" because:
1. That narrows the category to one class (wrong — categories exist independently)
2. Other forms would overpower other class choices if they ALSO fully expressed different subcategories

---

## §F4. What Categories Do NOT Include

The following are NOT part of subcategory definitions:

- **Race** — What race plays the class is irrelevant to the mechanical category
- **Damage type** — Electrical, fire, physical, etc. is flavor, not category
- **Armor/equipment restrictions** — Gear rules are balance concerns, not behavioral taxonomy
- **Specific ability names** — The category is the BEHAVIOR, not the button
- **Lore/tradition** — Why a class does what it does is separate from what it mechanically IS
- **Flight/ground state** — Delivery method, not category definition

---

## §F5. Crane (Construction Crane — Grab & Relocate)

**Definition:** I pick up targets and PUT THEM SOMEWHERE ELSE. Grab, lift, carry, drop.
Relocation as control.

**Mechanical behavior:**
- Grabs a specific target (single-target selection)
- Carries/relocates them to a chosen position
- The TARGET is moved, not the caster moving through them
- Overlaps with Grappler (both grab and reposition enemies)

**What it is NOT:**
- Not about moving THROUGH enemies (that's Battering Ram)
- Not about the caster's movement — it's about the TARGET's forced relocation
- Not area denial — it's single-target repositioning

**Overlap note:** Crane and Grappler share grab/relocate mechanics. The distinction
is context-dependent on class design — a frontliner Crane grabs to REPOSITION for
team benefit; a DPS Grappler grabs to DAMAGE. Same input, different purpose.

---

## §F5b. Battering Ram (Linear Breakthrough)

**Definition:** I move through terrain and enemies in a straight line. Everything in
the path gets shoved or broken. Unstoppable forward momentum.

**Mechanical behavior:**
- Linear advance in a committed direction
- Pushes/scatters/destroys everything in the path (enemies AND terrain)
- CC immunity during advance (cannot be stopped mid-charge)
- Directional commitment — cannot reverse once started
- Terrain destruction as a unique frontliner tool (creates new paths)

**What it is NOT:**
- Not about grabbing/carrying specific targets (that's Crane)
- Not about holding a position (that's Zone Control)
- Not reversible or redirectable mid-action — LINEAR COMMITMENT

**Current class expression:** Siegebreaker (needs further work — noted for later)

---

## §F6. Superseded Content

This document supersedes §3b of DESIGN_OVERRIDE.md in its entirety.
Any reference to "Force Targeting," "Unfocus + Capacitor Pull" as frontliner
SUBCATEGORY definitions, or racial characteristics mixed into category labels
should be read through the lens of this document instead.

§3b remains in DESIGN_OVERRIDE.md for historical context but is no longer
the canonical source for frontliner subcategory taxonomy.

---

Last updated: 2026-07-15
Authority: This file = DESIGN_OVERRIDE.md §3b (supersedes) > class Design files > LLM.md