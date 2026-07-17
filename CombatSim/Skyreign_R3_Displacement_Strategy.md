# CombatSim/Skyreign_R3_Displacement_Strategy.md
# ═══════════════════════════════════════════════════════════════════════════════
# COMBAT SIMULATION: Skyreign (no Draconite) + Wavecaller — Rank 3 Strategies
# ═══════════════════════════════════════════════════════════════════════════════
#
# Date: 2026-07-15
# Purpose: Test R3 strategy variations for Skyreign + Wavecaller duo.
#          Identify the only viable approach and document the skill sequence.
# Prerequisite: Wavecaller_Duo_Scenario.md (base movement + healing math)
# Reference: Skyreign_Design.yaml, Wavecaller_Design.yaml, DESIGN_OVERRIDE_RACIAL_LOCKS.md
# ═══════════════════════════════════════════════════════════════════════════════

## Rank 3 Enemy Upgrades

| Stat | R1 Value | R3 Value | Multiplier |
|------|----------|----------|------------|
| HP | 1000 | 1800 | ×1.8 |
| Melee DPS | 50 raw | 70 raw | ×1.4 |
| Archer DPS | 35 raw | 49 raw | ×1.4 |
| Bomber DPS | 40 raw | 56 raw | ×1.4 |
| Rusher speed | 6.5 m/s | 7.5 m/s | ×1.15 |

### R3 AI Behaviors
- Melee: Rotate facing to deny Exploit positionals
- Archers: Focus-fire lowest HP target
- Bombers: Lead-target AoE on movement prediction
- Rushers: Follow portals (2.5s delay), 1 dedicated interrupter
- ALL: CC Diminishing Returns (8s immunity after stun)

### Class-Specific R3 Counters
**Skyreign:**
- Enemies DODGE hawk-dive landing zone (1.5s telegraph)
- Focused burst on Dragon form (large hitbox = easy target)
- Form-swap animation has 0.5s vulnerability window

**Wavecaller:**
- 1 interrupter rusher disrupts Sound Pulse within 8m
- Portal exits watched — enemies pre-position at dive destinations
- Archers switch to WC if within 30m LoS

---

## Three Strategy Variations Tested

### Variation A: "Commit" (Dragonguard rush, max DPS)

| Metric | Result |
|--------|--------|
| Duration | 34s |
| Strategy | Walk into 5 melee, cleave them down |
| Peak incoming | 313 eDPS (5 melee + 2 bombers after DR) |
| Healing | 120 free + 50 GCD (30% allocation) = 170 HPS |
| Skyreign HP floor | **DEAD at 7.6s** |
| WC GCD split | 70% damage / 30% heal |
| Verdict | ✗ FAILS. Peak pressure exceeds survivability. |

**Why it fails:** 1100 HP + 25% DR cannot absorb 313 eDPS even with 170 HPS healing. The first 8s (before first kill) are lethal. No escape without Draconite.

---

### Variation B: "Scatter" (Dragon displacement → Dragonguard pick-off) ✅

| Metric | Result |
|--------|--------|
| Duration | 38s (+4s vs A) |
| Strategy | Dragon breath scatters 2-3 melee, fight reduced pack |
| Peak incoming | 158 eDPS (3 melee + bombers) |
| Healing | 120 free + 25 GCD (15% allocation) = 145 HPS |
| Skyreign HP floor | 587 / 1100 (53%) at t=18s |
| WC GCD split | 86% damage / 14% heal |
| Charges spent (WC) | 2 of 9 available (aggressive tail-end dives) |
| Verdict | ✅ WORKS. Only viable R3 path. |

**Why it works:** Displacement reduces simultaneous enemy count below the healing threshold. Scattered enemies take 20s to regroup (fire terrain + distance). Provides clean kill window on 3 enemies before the other 2 return.

---

### Variation C: "Elevation First" (Dragon flies to bombers immediately)

| Metric | Result |
|--------|--------|
| Duration | 48s |
| Strategy | Kill bombers first (removes AoE), then ground clear |
| Skyreign safety | Fine (solo vs 2 bombers, no melee reach) |
| WC alone on ground | 3-8 enemies, no frontline presence for 18s |
| WC time to death | **2.0s** (8 enemies) or **5.4s** (3 rushers only) |
| Verdict | ✗ FAILS. Cannot leave healer unprotected. |

**Why it fails:** Even with best-case aggro (melee stay on Sky, only rushers chase WC), Wavecaller dies in 5.4s to 3 R3 rushers. Self-peel gap confirmed at all ranks.

---

## The Correct R3 Sequence (B → C hybrid)

```
t=0-4s:    DRAGON — Breath scatter (displaces center melee + catches rushers)
t=4-8s:    DRAGONGUARD — Kill scattered rushers (3 enemies, low HP from breath)
t=8-28s:   DRAGONGUARD — Clean up center 3 melee (scattered 2 return at t=24)
t=28-32s:  DRAGON — Fly to bombers (elevation access)
t=32-50s:  DRAGON/GUARD — Kill bombers + archers (elevation phases)
```

Total: ~50s. R3 takes longer than R1 (66s→50s effective due to better strategy) but survival is assured.

---

## Skyreign Displacement Skill Sequence (GCD-by-GCD)

### Phase B1: Dragon Entry & Scatter (t=0–4s)

| GCD | Time | Skill | Form | Effect |
|-----|------|-------|------|--------|
| 1 | 0s | Form Shift → Dragon | 🐉 Dragon | Lift off. 0.5s vulnerability. Breath gauge resets. |
| 2 | 1.8s | Breath Weapon (AoE Cone) | 🐉 Dragon | 120° cone, 12m. Hits 5 melee + 2 rushers. Displacement 10-15m. Fire terrain 6s. |
| — | 3.6s | Flight reposition | 🐉 Dragon | 2-3m adjustment over near cluster. No GCD cost. |

**WC during B1:** Sound Interrupt (oGCD, covers swap window) → Harpoon ×2 (ranged DPS on scattered enemies)

### Phase B2: Hawk-Dive & Cleave (t=4–24s)

| GCD | Time | Skill | Form | Effect |
|-----|------|-------|------|--------|
| 3 | 4.0s | Form Shift → Dragonguard (Hawk-Dive) | ⚔️ Guard | Air-to-ground drop. Emerge damage + OffBalance Exploit on 2-3 targets. |
| 4 | 5.8s | Claw Rend (Exploit follow-up) | ⚔️ Guard | +30% Exploit damage on OffBalance targets. Cleave 2. |
| 5 | 7.4s | Tail Sweep (360° AoE) | ⚔️ Guard | No positional required. Answers R3 facing-rotation AI. |
| 6 | 9.0s | Breath Terrain (ground fire) | ⚔️ Guard | DoT zone + 30% slow. Pins enemies in lose-lose choice. |
| 7-10 | 10.8-18s | Cleave Rotation (Claw ↔ Tail) | ⚔️ Guard | Standard loop. Enemies die: t=12, t=16, t=20. Gauge building. |
| 11 | 20s | Charged Breath (aimed at returning enemies) | ⚔️ Guard | SAVED gauge for regroup window. Knockback resets approach by 8m. |

**WC during B2:** Walk 2.7s → Harpoon ×7 → Resonant Heal ×2 (at t=18 when Sky dips to 53%)

### Phase B3: Cleanup (t=24–38s)

| GCD | Time | Skill | Effect |
|-----|------|-------|--------|
| 12-21 | 24-38s | Cleave vs 2 staggered enemies | Low pressure (53-105 eDPS). Free healing covers. |

**WC during B3:** Rift Dive (1 charge) → Breaching Strike → Return Tide (1 charge) → Harpoon ×5. **Full DPS mode.**

---

## R3 Skill Expression: What Separates Good from Bad Play

| Decision Point | Good Play | Bad Play | Consequence |
|----------------|-----------|----------|-------------|
| t=0 form choice | Dragon first (scatter) | Dragonguard first (commit) | Death at 7.6s |
| t=1.8 breath aim | Cone covers melee + rushers | Misses rushers (only hits melee) | WC dies to rushers |
| t=4 hawk-dive target | Land on near-cluster (2-3 grouped) | Land on isolated enemy | Lose cleave value |
| t=20 charged breath | Aimed at regrouping enemies | Wasted on dead targets | 2 extra enemies early |
| WC t=0 interrupt | Covers Sky swap window | Used offensively | Sky takes burst during 0.5s vulnerability |

---

## Key Design Findings

1. **R3 difficulty scales via STRATEGY, not healer throughput.**
   WC's GCD split stays ~85/15 across ranks. The frontliner's decision quality is what changes.

2. **Displacement is the R3 unlock skill.**
   Without scatter, 5 simultaneous melee at R3 stats is lethal regardless of healing. Scatter reduces simultaneous count below healing threshold.

3. **Breath gauge timing is the R3 mastery expression.**
   Saving charged breath for the regroup window (t=20) is a DECISION, not a rotation. Miss it and the fight collapses.

4. **Self-peel gap persists at R3 (Variation C proof).**
   WC dies in 5.4s to 3 R3 rushers. Any strategy that leaves WC unprotected is invalid.

5. **Without Draconite, Skyreign has NO emergency exit.**
   Variation A's failure proves: once committed to Dragonguard, the only disengage is form-swap to Dragon (gauge reset + 0.5s vulnerability + slow flight). This is EXPENSIVE and SLOW. The class must scatter BEFORE engaging, not after.
