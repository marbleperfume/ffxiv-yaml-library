# CombatSim/LLM_Directive_Transient_Variables.md
# ═══════════════════════════════════════════════════════════════════════════════
# LLM DIRECTIVE: Transient Variables & Simulation Integrity
# ═══════════════════════════════════════════════════════════════════════════════
#
# Date: 2026-07-15
# Authority: Supersedes any prior CombatSim doc that declares a simulation
#            finding as a permanent design rule.
# Read BEFORE: CombatSim_Framework_For_LLMs.md, CombatSim_Summary_For_LLMs.md
# ═══════════════════════════════════════════════════════════════════════════════

## Purpose

This directive corrects a recurring LLM failure pattern: treating SIMULATION OUTPUTS
as DESIGN PILLARS. A simulation result tells you the current state of tunable numbers.
It does NOT tell you what the game's philosophy is.

---

## Rule 1: All simulation numbers are TRANSIENT

The following values are tunable and will change during development. Never lock
design decisions to their current state.

| Variable | Current Value | Why It's Transient |
|----------|--------------|-------------------|
| Wavecaller STA | 8 | Racial base stat — balanceable |
| Wavecaller HP | 800 | Derived from STA (STA × 100) — moves with STA |
| Free HPS | 120 | Tidepool + Sound Pulse + HoT coefficients — tunable per encounter tier |
| GCD Heal potency | 300 | MED-scaled — moves with stat budget |
| Tidepool evasion | ~30% | SPD coefficient — tunable |
| Pressure Charge max | 4 | Economy knob |
| Pressure Charge regen | 12s | Economy knob |
| Enemy DPS per type | 50-70 raw | Encounter design lever |
| Enemy HP | 1000-1800 | Encounter design lever |
| Rusher speed | 6.5-7.5 m/s | AI tuning knob |
| Skyreign HP | 1100 | STA × 100 — racial base |
| Skyreign DR | 25% | Defense stat + gear slot budget |
| Form swap duration | 1.2s | Animation timing — feel tunable |
| Heal range | 20m | Sound propagation coefficient |
| Base move speed | 5.5 m/s | Universal constant (less likely to change but still tunable) |

**When you run a sim and get a result (e.g., "WC dies in 7.6s"), that result is
a MEASUREMENT of the current numbers, not a verdict on the design.**

---

## Rule 2: Distinguish findings from philosophy

| Type | Example | How to treat it |
|------|---------|-----------------|
| **Finding** | "WC dies in 7.6s to 3 rushers at STA 8" | Transient. Changes if STA changes. |
| **Finding** | "Scatter strategy is viable, commit is not at R3" | Transient. Changes if enemy HP/DPS changes. |
| **Finding** | "86/14 damage/heal split matches FFXIV healer profile" | Transient. The TARGET ratio is a design choice; the specific numbers producing it are tunable. |
| **Philosophy** | "Healers are DPS-first, healing is cheap infrastructure" | Persistent. This is a design DIRECTION, not a number. |
| **Philosophy** | "R3 difficulty scales via strategy, not throughput" | Persistent. This is a structural claim about rank design. |
| **Philosophy** | "The frontliner's decision quality determines the healer's fun" | Persistent (observation about role coupling). |

**Findings expire when their input numbers change.**
**Philosophy persists until explicitly superseded by the user.**

---

## Rule 3: Never declare a gap "intended" or "unfixable" from a sim alone

The CombatSim_Framework_For_LLMs.md states the self-peel gap is "intended" and
should not be closed. THIS IS PREMATURE.

Correct framing:
- The self-peel gap EXISTS at current numbers (STA 8, 800 HP, 120 HPS, no self-heal).
- Whether it SHOULD exist is a design decision that depends on:
  - Final party size (duo vs 4-man)
  - Encounter design (do rushers always exist? At what ranks?)
  - Other healer classes (does Spiritcaller have the same gap?)
  - Racial stat rebalancing (Jumpers STA could become 10-12)
  - Tidepool interaction design (could gain knockback, stronger slow, etc.)
- The sim's job is to MEASURE the gap, not PRESCRIBE whether it should exist.

**Do NOT write "Do NOT close this gap" in any design document based on simulation
alone. That's a user decision, not a calculation.**

---

## Rule 4: How to use sim results across sessions (hop-to-hop)

When continuing combat simulation work from a prior session:

1. **Re-read this directive first.** Reminds you that prior findings are measurements, not rules.
2. **Check if input numbers have changed.** If any variable in the table above was
   updated in a class file, Guidebook, or Base_Attributes.yaml since the sim ran,
   the sim results are STALE. Re-run before drawing conclusions.
3. **State your assumptions at the top of any new sim.** List which values you're using
   and where they came from (file reference or "assumed from prior session").
4. **Never propagate a prior sim's CONCLUSION as an INPUT to a new sim.**
   Wrong: "WC can't self-peel (proven), so model WC as always dying to rushers."
   Right: "At STA 8 / 800 HP / 30% evasion / 0 self-heal, WC survives X seconds vs N rushers at Y DPS."
5. **Mark findings with their dependencies.** Example:
   "Finding: Sky survives R3 scatter at 53% floor. DEPENDS ON: 1100 HP, 25% DR, 145 HPS healing, 3 enemies post-scatter."
   If ANY dependency changes, the finding is invalidated.

---

## Rule 5: The 85/15 split is a TARGET, not a law

The ~85% damage / ~15% heal GCD split emerged from simulating a specific scenario
(13-enemy multi-elevation map, duo, Rank 3). It matched FFXIV healer parse profiles
and felt right as a design DIRECTION.

But:
- Different encounter shapes produce different ratios (low-pressure = 95/5, high-pressure = 70/30).
- The ratio is an OUTCOME of tuning free HPS vs incoming damage, not a fixed constraint.
- If free HPS is raised, the ratio shifts toward more damage. If lowered, toward more healing.
- The GOAL is "healer spends most GCDs on damage" — the exact percentage is a byproduct.

**When proposing changes, check whether the change MOVES the ratio and in which
direction. Don't reject a change because it makes the ratio 80/20 instead of 85/15.**

---

## Rule 6: Encounter design is HALF the equation

Every sim finding has two halves:
1. **Kit capability** (what the class can do) — tunable via class files
2. **Encounter pressure** (what the enemies demand) — tunable via encounter design

A finding like "WC can't sustain 313 eDPS" is equally solved by:
- Raising WC's healing output (kit change)
- Reducing simultaneous enemy count via encounter pacing (encounter change)
- Giving the frontliner better scatter tools (partner kit change)
- Staggering rusher spawn timing (encounter change)

**Never assume the fix must come from the class that "failed." The encounter
is equally valid as the tuning surface.**

---

## Summary for quick reference

```
TRANSIENT: numbers, ratios, TTK values, HP floors, HPS values
PERSISTENT: design directions, role coupling observations, anti-patterns
NEVER DO: declare sim results as permanent philosophy
ALWAYS DO: state assumptions, mark dependencies, re-validate when inputs change
```
