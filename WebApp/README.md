# Juice Design Hub (WebApp)

Web replacement for the standalone `*Creator.pyw` tkinter tools. Edits the
**live repo files** (no copy, no database) with comment-preserving YAML writes,
validates everything against the formal schemas in `Schemas/`, and supersedes
`Hub_Master.pyw`'s relationship-graph view.

**See also:** [USER_GUIDE.md](USER_GUIDE.md) — how to transition/add variables and
deprecate old files. [HISTORY.md](HISTORY.md) — sectioned change history.

## Running it

Python 3.9+ is required. This machine's system Python needs elevation, so the
venv was built from UE5's bundled interpreter:

```
"C:\Program Files\Epic Games\UE_5.3\Engine\Binaries\ThirdParty\Python3\Win64\python.exe" -m venv WebApp\.venv
WebApp\.venv\Scripts\python.exe -m pip install -r WebApp\backend\requirements.txt
```

Start the server **from the repo root** (`YAML Library`):

```
WebApp\.venv\Scripts\python.exe -m uvicorn WebApp.backend.main:app --port 8400
```

Open http://127.0.0.1:8400 — the UI is served by the same process.
(The frontend is no-build React via ES modules — no Node/npm required. If Node
is ever installed, a Vite build placed in `WebApp/frontend/dist/` wins over
`WebApp/frontend/public/` automatically.)

## CLI tools (no server needed)

```
WebApp\.venv\Scripts\python.exe WebApp\backend\run_validators.py    # structured findings; exit 1 on errors
WebApp\.venv\Scripts\python.exe WebApp\backend\generate_legacy.py   # regenerate Attributes/attributes.json
python Project_Validator.py                                         # original validator — unchanged behavior
```

## What the validators enforce

| Rule | Severity | Meaning |
|---|---|---|
| `core.integrity` | error | The original Project_Validator checks (wrapped, not duplicated) |
| `stat.schema` / `stat.legacy-placeholder` | error | Base_Attributes.yaml must match `Schemas/stat_contract.schema.json`; no `[coeff_TBD]` brackets |
| `stat.drift` | error | `attributes.json` differs from what `generate_legacy.py` produces — regenerate, never hand-edit |
| `stat.undeclared-override` / `stat.override-shape` | error | A class file defines a `Formula:` without a `StatOverrides:` declaration, or the declaration is malformed |
| `skill.schema` / `skill.effect` | error | `Skills/*.yaml` must match `Schemas/skill.schema.json`; every effect's params must match `Schemas/EffectTypes.yaml` |
| `stat.dangling-ref` | warning | Reference to a repo file that doesn't exist |
| `stat.pending-coeff` | pending | A coefficient the user has intentionally not decided (`Value: PENDING`) — surfaced, never invented |
| `skill.legacy-format` | legacy | Pre-schema class skill file awaiting incremental migration — not wrong |
| `stat.hardcoded-formula` | info | A file hardcodes a central formula (e.g. STA × 100) instead of referencing the contract |

## Editing model

- `Skills/*.yaml` open in the schema-driven form (typed `Effects`, live
  validation, Save disabled while errors exist). Everything else opens raw.
- Saves merge into the round-trip-parsed file: **unchanged keys keep their
  comments, key order, folded blocks, and quoting**; changed keys are updated
  in place; lists are replaced wholesale; keys absent from the payload are
  left untouched.

## Roadmap (not built)

- **Phase 3 — UE5 export**: port `Hub_Master.pyw`'s `collect_gameplay_tags()`
  to an endpoint; map typed `Effects` onto GameplayEffect/GameplayAbility
  DataTable rows. The typed schema was designed as the prerequisite for this.
- **Phase 4 — repo-wide LLM directive**: generalize
  `CombatSim/LLM_Directive_Transient_Variables.md` into a root `LLM_README.md`
  (authority order, schema locations, PENDING semantics). The enforced schema
  is itself the main token-usage lever — typed reads replace whole-file prose.
