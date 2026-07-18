"""Ability-record conformance (v2 — methodology-first, direction INVERTED).

The Guidebooks methodology (class_item_baselines.md, elementalist_shaman_rework.md)
is the canon: every ability is authored as TriggerCondition | ItemBaselineReplaced |
DecisionCreated | CCStage | RankProgression. The per-class Classes/2.0/*_Skills*.yaml
files already practice this; thin Skills/*.yaml records that predate it are the
MIGRATION TARGETS, classified `pre-methodology` (severity: legacy).

Grades per ability:
  finalized — all five methodology fields declared (PENDING-valued fields don't count)
  draft     — some missing/PENDING; deliberate state while thematic clashes are
              unresolved, reported as `pending`, never as an error

Plus the §25 audit (DESIGN_OVERRIDE_SYSTEMS.md): cooldowns over 15s without a §25
marker are surfaced as info — identity abilities must be resource-gated.
"""

import json
import re

import jsonschema

from ..repo import REPO_ROOT, plain_yaml

SKILL_SCHEMA_PATH = "Schemas/skill.schema.json"
EFFECT_TYPES_PATH = "Schemas/EffectTypes.yaml"

_UNIVERSAL_PARAMS = {"Type", "Flavor", "Note", "Condition"}

# Canonical methodology fields → accepted spellings in existing files
ALIASES = {
    "TriggerCondition": ["TriggerCondition", "trigger_condition", "Trigger"],
    "ItemBaselineReplaced": ["ItemBaselineReplaced", "item_baseline_replaced", "item_replaced", "ItemBaseline"],
    "DecisionCreated": ["DecisionCreated", "decision_created", "decision"],
    "CCStage": ["CCStage", "cc_stage"],
    "RankProgression": ["RankProgression", "rank_progression", "RankBehavior", "RankEvolution"],
}
METHODOLOGY_FIELDS = list(ALIASES.keys())

# Fields that mark a dict as an ability record (besides Name/name)
_ABILITY_MARKERS = {
    "type", "Type", "potency", "Potency", "trigger_condition", "TriggerCondition",
    "effect", "Effect", "Effects", "cooldown", "Cooldown", "Recast", "RecastTime",
    "cc_stage", "CCStage", "ActionType", "Mechanics", "gcd",
    "Arc", "Recovery", "Targets", "Stacks", "Range", "range",
    "StackGeneration", "StackCosts", "Shape", "Element", "ID",
}

_COOLDOWN_KEYS = ("cooldown", "Cooldown", "Recast", "RecastTime")
_S25_MARKER = re.compile(r"§\s*25|section_25|s25", re.IGNORECASE)


def _finding(severity, file, rule, message, line=None):
    return {"severity": severity, "file": file, "line": line,
            "rule": rule, "message": message}


def _load_vocabulary():
    data = plain_yaml(EFFECT_TYPES_PATH)
    return data.get("EffectTypes") or {}


def _load_schema():
    return json.loads((REPO_ROOT / SKILL_SCHEMA_PATH).read_text(encoding="utf-8"))


def _get_aliased(record, canonical):
    """(present, value) for a methodology field under any accepted spelling.
    Presence means the KEY exists — an explicit null (e.g. cc_stage: null) is
    a declaration, not an omission."""
    for spelling in ALIASES[canonical]:
        if spelling in record:
            return True, record[spelling]
    return False, None


def _is_pending(value):
    return isinstance(value, str) and value.strip().upper().startswith("PENDING")


def grade_ability(record):
    """Returns (grade, missing) — grade is 'finalized' or 'draft';
    missing lists absent or PENDING methodology fields."""
    missing = []
    for field in METHODOLOGY_FIELDS:
        present, value = _get_aliased(record, field)
        if not present or _is_pending(value):
            missing.append(field + (" (PENDING)" if present else ""))
    return ("finalized" if not missing else "draft"), missing


def methodology_field_count(record):
    return sum(1 for f in METHODOLOGY_FIELDS if _get_aliased(record, f)[0])


def _ability_name(record):
    return record.get("Name") or record.get("name") or "(unnamed)"


def find_ability_records(node, out, path=None):
    """Walk a parsed class file collecting (path, record) pairs: dicts carrying
    a Name/name plus at least two other ability-marker fields. `path` is the
    list of keys/indices from the document root to the record — the address
    the editor uses for targeted writes."""
    if path is None:
        path = []
    if isinstance(node, dict):
        has_name = "Name" in node or "name" in node
        markers = sum(1 for k in node if k in _ABILITY_MARKERS)
        if has_name and markers >= 2:
            out.append((path, node))
            return  # don't scan inside a record for nested records
        for k, v in node.items():
            find_ability_records(v, out, path + [k])
    elif isinstance(node, list):
        for i, v in enumerate(node):
            find_ability_records(v, out, path + [i])


def _parse_seconds(value):
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        m = re.match(r"\s*(\d+(?:\.\d+)?)\s*s?\b", value)
        if m:
            return float(m.group(1))
    return None


def audit_s25(record, file, context):
    """Cooldown >15s without a §25 marker → info (identity abilities must be
    resource-gated per DESIGN_OVERRIDE_SYSTEMS.md §25)."""
    findings = []
    marked = any(_S25_MARKER.search(str(record.get(k, ""))) for k in record)
    if "section_25_note" in record:
        marked = True
    for key in _COOLDOWN_KEYS:
        if key not in record or marked:
            continue
        secs = _parse_seconds(record[key])
        if secs is not None and secs > 15:
            findings.append(_finding(
                "info", file, "skill.s25-audit",
                f"{context}: {key} {record[key]!r} exceeds 15s with no §25 marker "
                f"— verify this is a tactical utility, not an identity ability "
                f"(identity = resource-gated, never CD-gated)"))
    return findings


def validate_effects(effects, vocabulary, file, context=""):
    """Typed mechanical-packet check (unchanged from v1)."""
    findings = []
    for i, eff in enumerate(effects):
        where = f"{context}Effects[{i}]"
        if not isinstance(eff, dict):
            findings.append(_finding("error", file, "skill.effect",
                                     f"{where}: effect must be a mapping"))
            continue
        etype = eff.get("Type")
        if etype not in vocabulary:
            findings.append(_finding(
                "error", file, "skill.effect",
                f"{where}: Type {etype!r} is not in the controlled vocabulary "
                f"({EFFECT_TYPES_PATH})"))
            continue
        spec = vocabulary[etype] or {}
        for param in spec.get("RequiredParams") or []:
            if param not in eff:
                findings.append(_finding(
                    "error", file, "skill.effect",
                    f"{where} ({etype}): missing required param '{param}'"))
        allowed = (_UNIVERSAL_PARAMS
                   | set(spec.get("RequiredParams") or [])
                   | set(spec.get("OptionalParams") or []))
        for key in eff:
            if key not in allowed:
                findings.append(_finding(
                    "warning", file, "skill.effect",
                    f"{where} ({etype}): param '{key}' is not declared for this "
                    f"type in {EFFECT_TYPES_PATH} — typo, or extend the vocabulary"))
    return findings


def validate_skill_payload(payload, file="(unsaved payload)"):
    """Schema + packet validation of one ability record (editor live-check)."""
    findings = []
    validator = jsonschema.Draft7Validator(_load_schema())
    for err in validator.iter_errors(payload):
        path = ".".join(str(p) for p in err.absolute_path)
        findings.append(_finding("error", file, "skill.schema",
                                 f"{path or '(root)'}: {err.message}"))
    if isinstance(payload, dict) and isinstance(payload.get("Effects"), list):
        findings += validate_effects(payload["Effects"], _load_vocabulary(), file)
    return findings


def _grade_file(records, rel):
    """Per-file grading findings: one summary (info) + one aggregated draft
    detail (pending) so a 17-ability file doesn't flood the report."""
    findings = []
    finalized, drafts = [], []
    for rec in records:
        grade, missing = grade_ability(rec)
        if grade == "finalized":
            finalized.append(_ability_name(rec))
        else:
            drafts.append(f"{_ability_name(rec)} (missing {', '.join(missing)})")
    findings.append(_finding(
        "info", rel, "skill.methodology",
        f"{len(records)} abilities: {len(finalized)} finalized, {len(drafts)} draft"))
    if drafts:
        shown = "; ".join(drafts[:8]) + ("; …" if len(drafts) > 8 else "")
        findings.append(_finding(
            "pending", rel, "skill.draft",
            f"draft abilities awaiting iterative finalization: {shown}"))
    return findings


def run_skill_schema_checks():
    findings = []
    vocabulary = _load_vocabulary()

    # Standalone Skills/*.yaml — schema-validate; thin records without ANY
    # methodology fields are pre-methodology migration targets.
    for p in sorted((REPO_ROOT / "Skills").glob("*.yaml")):
        rel = p.relative_to(REPO_ROOT).as_posix()
        try:
            data = plain_yaml(rel)
        except Exception as e:
            findings.append(_finding("error", rel, "skill.schema",
                                     f"unparseable YAML ({e})"))
            continue
        if not isinstance(data, dict):
            continue
        findings += validate_skill_payload(data, file=rel)
        if methodology_field_count(data) == 0:
            findings.append(_finding(
                "legacy", rel, "skill.pre-methodology",
                "thin pre-methodology record (no TriggerCondition / "
                "ItemBaselineReplaced / DecisionCreated / CCStage / "
                "RankProgression) — this is the MIGRATION TARGET; upgrade it "
                "to the Guidebooks ability framework"))
        else:
            findings += _grade_file([data], rel)
            findings += audit_s25(data, rel, _ability_name(data))

    # Per-class skill files — the format the methodology lives in. Grade each
    # ability; validate any typed Effects packets; run the §25 audit.
    for p in sorted((REPO_ROOT / "Classes").rglob("*_Skills*.yaml")):
        rel = p.relative_to(REPO_ROOT).as_posix()
        try:
            data = plain_yaml(rel)
        except Exception as e:
            findings.append(_finding("error", rel, "skill.schema",
                                     f"unparseable YAML ({e})"))
            continue
        pairs = []
        find_ability_records(data, pairs)
        records = [rec for _, rec in pairs]
        if not records:
            findings.append(_finding(
                "warning", rel, "skill.methodology",
                "no ability records recognized — file structure may need an "
                "alias/marker added to the v2 walker"))
            continue
        findings += _grade_file(records, rel)
        for rec in records:
            name = _ability_name(rec)
            if isinstance(rec.get("Effects"), list):
                findings += validate_effects(rec["Effects"], vocabulary, rel,
                                             context=f"{name}.")
            findings += audit_s25(rec, rel, name)
    return findings
