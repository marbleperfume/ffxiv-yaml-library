# DESIGN_OVERRIDE_OTHER_ROLES.md

## Healer & DPS Subcategory Taxonomy — TODO

### This file will mirror DESIGN_OVERRIDE_FRONTLINE.md for non-frontliner roles.

---

## Status: PENDING DISCOVERY

The frontliner taxonomy (DESIGN_OVERRIDE_FRONTLINE.md) proved that defining race-agnostic
mechanical subcategories BEFORE writing class files prevents identity drift. The same
work is needed for Healer and DPS roles.

---

## Problem Statement

Current healer and DPS class files have:
- Too much emphasis on specific abilities with functional cross-references (items, game characters)
- Not enough filtering to define what their GOALS ARE IN COMBAT
- The same hollow-identity pattern frontliners had: complete-looking files, vague on purpose

The fix is the same: define race-agnostic mechanical subcategories FIRST, then place
classes into those fields. Until these taxonomies exist, healer/DPS class files will
continue to drift into jargon-heavy, identity-light territory.

---

## Healer Subcategories (TBD — needs discovery session)

What are the mechanical BEHAVIORS a healer can express?

Possible axes (DO NOT ASSUME THESE ARE CORRECT — listed as starting points only):
- Triage vs sustained vs prevention?
- Reactive (heal after damage) vs proactive (prevent damage)?
- Single-target focus vs AoE coverage?
- Heal-through-damage (DPS that incidentally heals) vs dedicated restoration?

These need the same treatment frontliners got: "What is the PARTY CONTRACT for this
subtype?" and "What mechanical behavior defines it, race-agnostic?"

---

## DPS Subcategories (TBD — needs discovery session)

What are the mechanical BEHAVIORS a DPS can express?

Possible axes (DO NOT ASSUME THESE ARE CORRECT — listed as starting points only):
- Burst vs sustained vs DoT vs setup?
- Ranged vs melee vs hybrid?
- Solo-target vs AoE vs cleave?
- Committed (can't disengage) vs flexible (can reposition freely)?

Current DPS files lean on ability lists and game-character references instead of
mechanical behavior definitions. The question is NOT "what does this class DO" but
"what is this class's GOAL in combat and how does the party BENEFIT from its presence?"

---

## Priority

Define the fields → audit existing classes against them → rewrite as needed.

Same workflow as frontliners:
1. Discovery session (human defines the contract and mechanical behaviors)
2. Taxonomy file written (this file, expanded)
3. Class files audited and rewritten where hollow

---

## Authority

This file: pending. Once healer/DPS taxonomies are defined, this file becomes
authoritative for those roles in the same way DESIGN_OVERRIDE_FRONTLINE.md is
authoritative for frontliner subcategories.

---

Last updated: 2026-07-15
Status: PLACEHOLDER — awaiting discovery sessions
