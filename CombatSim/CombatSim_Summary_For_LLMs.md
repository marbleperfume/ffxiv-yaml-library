# Combat Simulation Summary — Wavecaller + Frontliner Duo (juice-yaml-library)

## Reference Files

- `CombatSim/Wavecaller_Duo_Scenario.md` — Base movement + healing math
- `CombatSim/Skyreign_R3_Displacement_Strategy.md` — R3 strategy variations
- `Guidebooks/DESIGN_OVERRIDE_RACIAL_LOCKS.md` — Racial lock expression rules

---

## Revised Wavecaller Model (supersedes old file's healing design)

### Core Change

Wavecaller is a **DPS-first healer** whose healing is a FREE BASELINE (passive, no GCD cost). GCD heals exist for burst/emergency but cost damage output. This matches FFXIV healer profiles (~85% damage GCDs / ~15% heal GCDs).

### Healing System

| Layer | HPS | GCD Cost | Notes |
| --- | --- | --- | --- |
| Tidepool Aura | 50 | FREE | Passive, 20m radius, always on |
| Sound Pulse | 40 | FREE (oGCD) | Auto-fires every 3s |
| Resonance HoT | 30 | FREE | Persistent regen on allies in range |
| **Total Free** | **120** | **0** | Covers most sustained incoming |
| Resonant Heal (GCD) | 167/s if spammed | 1 GCD per cast (300 HP) | Emergency only — costs damage |

### Resource Model

- **Pressure Charges (4 max, 12s regen):** OFFENSIVE ONLY. Rift Dive (gap close + damage) and Return Tide (reposition). No longer spent on healing or mobility tax.
- **Resonance:** Does NOT reset on movement or dives. Only affects GCD heal potency (Cold 70% / Warm 100% / Resonant 120%). Walking + healing at Warm is always viable.
- **Hydration:** Tidepool self-maintains. Not a combat constraint under the revised model.

### Movement

- Base speed: 5.5 m/s (universal for all players)
- Walking 15m to keep pace with a dashing frontliner: 2.7s (trivial)
- Movement is NOT the problem. Healing while walking works (Warm state, 100% potency).

---

## Key Simulation Findings

### 1. Healing Throughput Is Viable

- Single healer sustains a frontliner vs 5 melee + bomber AoE at Rank 1.
- At Rank 3 (×1.4 enemy DPS, ×1.8 HP), viable ONLY with scatter strategy (reduced simultaneous pressure).

### 2. Self-Peel Gap (UNRESOLVED)

- Wavecaller dies in 5-7s to 3 dedicated rushers at any rank.
- 800 HP, no self-heal, no hard CC, cannot outrun (5.5 vs 6.5-7.5 m/s).
- Requires frontliner peel (Adabold MBAS) or a new WC self-defense tool.
- This gap persists across all tested configurations.

### 3. Rank 3 Scales Via Strategy, Not Throughput

- Healer GCD split stays constant (~85/15) across ranks.
- Frontliner decision quality determines difficulty:- R1: Any approach works.
- R3: Only "Scatter" (Dragon breath displacement → reduced pack → cleave) is viable.
- R3 skill expression = knowing to scatter BEFORE committing, timing charged breath for regroup window.

### 4. Skyreign Form Swap (1.2s Super Armor + CC Immunity + 50% DR)

- Cannot be interrupted mid-transformation.
- Takes chip damage (30 HP per swap from bombers) but free healing exceeds it.
- Hawk-dive descent IS the 1.2s swap animation — dramatic, readable, creates R3 dodge skill check.
- eHP during swap: 2200 (vs base 1467). Swap windows are the SAFEST moments.

### 5. Asymmetric Error Tolerance

| Scenario | Result | Implication |
| --- | --- | --- |
| Bad healer + Good frontliner | FL dies at 12.4s (scatter delays but can't prevent) | FL must disengage (Dragon escape) |
| Good healer + Bad frontliner | FL survives (WC goes 100% healbot, 287 HPS) | Healer carries but loses DPS identity |

- The frontliner determines whether the healer gets to play DPS or is forced into healbot.
- Good scatter → pressure below free HPS → healer at 86/14 ceiling.
- No scatter → pressure above free HPS → healer at 0/100 floor.
- **Design recommendation:** Keep this asymmetry. 100% healbot is skill FLOOR (boring, works). 86/14 is skill CEILING. The decision of "when can I DPS vs when must I healbot" IS the healer expression.

---

## Frontliner Comparison (Same Map, Same Enemies)

| Factor | Adabold | Skyreign (no Draconite) | MetaKnight |
| --- | --- | --- | --- |
| HP / DR | 1600 / 30% | 1100 / 25% | ~1300 / 20% |
| Healer peel | ✅ MBAS (15-18m instant) | ✗ None | ✗ Pull range too short |
| Elevation access | ✗ None | ✅ Dragon flight | ✗ Horizontal only |
| Survivability floor | 52% (comfortable) | 27-59% (rank-dependent) | ~40% |
| DPS contribution | Low (tank) | High (DPS/FL hybrid) | Medium |
| R3 strategy | Ground displacement | Breath scatter + hawk-dive | Vortex pull (limited) |

No single frontliner solves both elevation + healer protection simultaneously.

---

## Numbers for Simulation Reference

| Parameter | Value |
| --- | --- |
| Base move speed (all) | 5.5 m/s |
| Dash (class ability) | 12-18m instant |
| Wavecaller GCD | 1.8s (SPD 12) |
| Pressure Charges | 4 max, 1 per 12s regen |
| Free HPS | 120 (passive, no GCD cost) |
| GCD heal | 300 HP per cast |
| Max HPS (100% healbot) | 287 |
| Enemy melee DPS (R1/R3) | 50 / 70 raw |
| Enemy HP (R1/R3) | 1000 / 1800 |
| Frontliner TTK per pack (R1/R3) | 22s / 34-38s |
| Skyreign form swap | 1.2s, CC immune, 50% DR |

---

## Anti-Patterns (confirmed by simulation)

1. ✗ Heal OR Damage as competing resources (old model — replaced)
2. ✗ Resonance reset on movement/dive (punished mobility — removed)
3. ✗ Pressure Charges as shared heal/offense/mobility pool (created unwinnable math — now offense-only)
4. ✗ Free HPS high enough to cover ALL scenarios passively (makes GCD heal button dead design)
5. ✗ Frontliner commit without scatter at R3 (lethal regardless of healing)
6. ✗ Leaving healer alone on ground while FL takes elevation (healer dies in 2-5s)

