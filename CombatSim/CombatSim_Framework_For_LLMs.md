# CombatSim Framework & Design Intent — For LLMs

Companion to `CombatSim_Summary_For_LLMs.md`. That file holds the **numbers/model**
(free HPS, charges, error tolerance, frontliner comparison). This file holds the
**design intent** — what the competency checks are *for*, and how to read a kit's
results. Read this before proposing any change to a kit's balance.

---

## 1. What the competency checks are FOR (two audiences)

The apparatus — Skill Quests, Strategy Rank tests, and the CombatSim sim/scenarios —
serves two audiences at once.

**Player-facing** — two instruments, split from the deprecated Mercenary Rank:

- **Skill Quests = comprehension.** "Do you understand *when* to use this ability?"
  Per-ability, tested directly, before you hold it.
- **Strategy Rank = execution.** "Can you *do it live* in the actual instance, under
  encounter pressure?"

> Mercenary Rank (legacy) was one numeric gate bundling both jobs — bar a skill until
> the player understands *when* to use it, AND gate difficulty/execution. It was
> deprecated; those two jobs were split into the two instruments above. Skill Quests
> took the comprehension half; Strategy Rank was refined to absorb the execution half.

**Designer-facing** — the diagnostic. When a kit fails a competency scenario, the
failure distinguishes exactly two things:

- **Kit needs adjusting** — LOCAL: a number, a missing tool, a timing window. Tunable.
- **Central integrity failure** — the underlying model is STRUCTURALLY broken. Not
  tunable.

This is what the sim apparatus is *for*: telling "tune the kit" apart from "rethink
the framework." Running a kit through the test = finding out which.

---

## 2. Rank scope — R2 is the on-ramp, not the ceiling

- **R1 = the FFXIV Normal floor.** Strategy Rank 1 enemies attack nearest; content is
  cluster-valid and mindless. Complexity mechanics (targetable healers, positioning,
  peeling) EXIST but never bite here. This floor is intentional and good — the casual
  retention pillar.
- **R2 = complexity introduced.** Enemies path toward squishies; mechanics
  comprehension becomes load-bearing.
- **R3+ = harder than R2 implies.** Procgen geometry, order-of-operations, every class
  axis engaged. R2 is the *introduction* of complexity, not its ceiling — so competency
  checks are continuous validation as difficulty climbs, not a one-time doorway. A kit
  passing R2 is NOT validated for the whole game.

---

## 3. The self-peel gap is INTENDED — not a hole to plug

The Wavecaller "self-peel gap" (she dies to dedicated healer-seeking pressure without
party protection) is **the mechanical form of the R2+ competency gate**, not a balance
problem.

Causal chain:

1. Healers can be targeted — a core mechanic (unlike FFXIV's un-punishable pocket healer).
2. R1 floor: targetability exists but never bites (attack-nearest AI, cluster-valid).
3. R2+: dedicated healer-seeking pressure appears; targetability becomes load-bearing.
4. Therefore the gap emerges automatically: a competent frontliner protects the
   targetable healer; a bad one doesn't, and she dies. **Her death is the signal that
   the frontliner didn't understand the encounter.**

**Do NOT close this gap with a Wavecaller self-defense/escape tool.** That defuses the
gate and recreates the FFXIV pocket-healer the framework rejects. The frontliner-peel
dependency IS the tested mechanic. The only design work here is TUNING *when / how hard*
the gate bites — never removing it, never letting it bite at R1.

The Wavecaller is not passive: the healbot-vs-DPS decision is hers, and her kit buys
time. The point is that her survival *under dedicated focus at R2+* is correctly
party-dependent, and that dependency is the skill being tested.

---

## 4. The diagnostic lens applied (self-peel worked example)

Reading a "Wavecaller under focus" result:

| Result | Verdict |
|---|---|
| Dies with **no** frontliner peel | Intended — gate working. Not a failure. |
| Dies **even with a correct** frontliner peel | **Central integrity failure** — the protection mechanic doesn't deliver the framework's promise. |
| Survives fine even under a **bad** frontliner | Gate not biting — targetability rendered meaningless (integrity/tuning problem, other direction). |

The competency check tells you which regime you're in. "The WC needs a self-defense
tool" is a *kit-adjust* answer to something that is not a kit failure — the wrong reflex.

---

## 5. Error tolerance is the healer's skill expression

(Per `CombatSim_Summary_For_LLMs.md`.) The frontliner determines whether the healer gets
to play DPS or is forced to healbot:

- Good scatter → pressure below free HPS → healer at ~86/14 damage/heal (skill CEILING).
- No scatter → pressure above free HPS → healer at 0/100 healbot (skill FLOOR — boring,
  but works).

Keep this asymmetry. The "when can I DPS vs when must I healbot" decision IS the healer
expression. (Note: this ~85/15 split, held roughly constant across ranks, is the
committed Wavecaller model — it supersedes the 55/15/30 rank-scaling table in
`DESIGN_OVERRIDE_HEALER.md`, which was an assumption not reproduced in any simulated kit.)

---

## 6. Why this avoids FFXIV's and ToS's healer failures

- **FFXIV** gates engagement by *difficulty*: the kit is only interesting at Savage,
  which casuals never reach; the "2-minute meta" is invisible to the audience actually
  experiencing the boredom. Solve a Savage tier and nothing's left → players leave at the
  last tier.
- **ToS** gates by *build*: a healer is either damage-built-and-solo-viable (support
  identity incidental) or full-support (no damage, never solos). No build is both.
- **This game** keeps healer freedom at every rank: strategic depth is an *exploration*
  (procgen, multiple discoverable approaches), never a single mandated solution — so
  there's no "solved" state to abandon, and R1 stays fully optional for casuals. Depth
  lives in reading the encounter, not executing one memorized script.

---

## References

- `CombatSim/CombatSim_Summary_For_LLMs.md` — numbers/model (free HPS, charges, error
  tolerance, frontliner comparison, super-armor spec)
- `Guidebooks/DESIGN_OVERRIDE_PROGRESSION.md` — Skill Unlock Quests, Strategy Rank,
  Mercenary Rank deprecation
- `Guidebooks/DESIGN_OVERRIDE_HEALER.md` — three-axis healer model
- `CombatSim/Skyreign_R3_Displacement_Strategy.md` — R3 strategy variations
