"""Stat-contract conformance: Base_Attributes.yaml shape, PENDING coefficients,
attributes.json drift, undeclared per-class formula divergence, hardcoded
formula copies, dangling file references.
"""

import json
import re

import jsonschema

from ..repo import REPO_ROOT, plain_yaml
from ..generate_legacy import build_legacy_json

STAT_SCHEMA_PATH = "Schemas/stat_contract.schema.json"
BASE_ATTRS = "Attributes/Base_Attributes.yaml"
LEGACY_JSON = "Attributes/attributes.json"


def _finding(severity, file, rule, message, line=None):
    return {"severity": severity, "file": file, "line": line,
            "rule": rule, "message": message}


def _load_schema():
    return json.loads((REPO_ROOT / STAT_SCHEMA_PATH).read_text(encoding="utf-8"))


# ── check 1: Base_Attributes.yaml conforms to the contract schema ──────────────

def check_contract_shape():
    findings = []
    schema = _load_schema()
    data = plain_yaml(BASE_ATTRS)
    validator = jsonschema.Draft7Validator(schema)
    for err in validator.iter_errors(data):
        path = ".".join(str(p) for p in err.absolute_path)
        findings.append(_finding(
            "error", BASE_ATTRS, "stat.schema",
            f"{path or '(root)'}: {err.message}"))

    # forbid legacy bracket placeholders anywhere in the raw text
    raw = (REPO_ROOT / BASE_ATTRS).read_text(encoding="utf-8")
    for i, line in enumerate(raw.splitlines(), 1):
        if re.search(r"\[(coeff|small_coeff)[^\]]*\]", line):
            findings.append(_finding(
                "error", BASE_ATTRS, "stat.legacy-placeholder",
                f"line {i}: bracket placeholder survives — name the coefficient "
                f"and mark it PENDING instead: {line.strip()!r}", line=i))
    return findings


# ── check 2: PENDING coefficients (surfaced, never errors) ─────────────────────

def check_pending_coefficients():
    findings = []
    data = plain_yaml(BASE_ATTRS)
    derived = (data.get("Base_Character") or {}).get("DerivedStats") or {}
    for stat_name, stat in derived.items():
        if not isinstance(stat, dict):
            continue
        for coeff_name, coeff in (stat.get("Coefficients") or {}).items():
            if isinstance(coeff, dict) and coeff.get("Value") == "PENDING":
                note = coeff.get("Note", "")
                findings.append(_finding(
                    "pending", BASE_ATTRS, "stat.pending-coeff",
                    f"{stat_name}.{coeff_name} awaits a user balance decision"
                    + (f" — {note}" if note else "")))
    return findings


# ── check 3: attributes.json drift against generated output ────────────────────

def check_legacy_drift():
    on_disk_path = REPO_ROOT / LEGACY_JSON
    if not on_disk_path.exists():
        return [_finding("warning", LEGACY_JSON, "stat.drift",
                         "attributes.json missing — run WebApp/backend/generate_legacy.py")]
    try:
        on_disk = json.loads(on_disk_path.read_text(encoding="utf-8"))
    except Exception as e:
        return [_finding("error", LEGACY_JSON, "stat.drift",
                         f"attributes.json unparseable: {e}")]

    generated = build_legacy_json()
    a = {k: v for k, v in on_disk.items() if k != "_generated"}
    b = {k: v for k, v in generated.items() if k != "_generated"}
    if a == b:
        return []

    diffs = []
    for key in sorted(set(a) | set(b)):
        if key not in a:
            diffs.append(f"missing key {key}")
        elif key not in b:
            diffs.append(f"extra key {key}")
        elif a[key] != b[key]:
            diffs.append(f"{key} differs (e.g. intent/default drifted from Base_Attributes.yaml)")
    detail = "; ".join(diffs[:6]) + ("; …" if len(diffs) > 6 else "")
    return [_finding(
        "error", LEGACY_JSON, "stat.drift",
        f"attributes.json has drifted from Base_Attributes.yaml — regenerate with "
        f"WebApp/backend/generate_legacy.py. Diffs: {detail}")]


# ── check 4: undeclared per-class formula divergence + StatOverrides shape ─────

def _walk_formulas(node, path, out):
    if isinstance(node, dict):
        for k, v in node.items():
            p = f"{path}.{k}" if path else str(k)
            if k in ("Formula", "ReplacementFormula") and isinstance(v, str):
                out.append(p)
            else:
                _walk_formulas(v, p, out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            _walk_formulas(v, f"{path}[{i}]", out)


def check_class_overrides():
    findings = []
    schema = _load_schema()
    override_schema = schema["definitions"]["StatOverride"]
    base = plain_yaml(BASE_ATTRS)
    derived_names = set(((base.get("Base_Character") or {}).get("DerivedStats") or {}).keys())

    for path in sorted((REPO_ROOT / "Classes").rglob("*_Design.yaml")):
        rel = path.relative_to(REPO_ROOT).as_posix()
        try:
            data = plain_yaml(rel)
        except Exception as e:
            findings.append(_finding("error", rel, "stat.undeclared-override",
                                     f"unparseable YAML ({e})"))
            continue
        if not isinstance(data, dict):
            continue

        overrides = data.get("StatOverrides")
        formulas = []
        _walk_formulas({k: v for k, v in data.items() if k != "StatOverrides"},
                       "", formulas)

        if formulas and not overrides:
            findings.append(_finding(
                "error", rel, "stat.undeclared-override",
                f"defines formula(s) at {', '.join(formulas[:4])}"
                + ("…" if len(formulas) > 4 else "")
                + " but declares no StatOverrides block — formula divergence "
                  "from Base_Attributes.yaml must be formally declared"))

        for i, ov in enumerate(overrides or []):
            v = jsonschema.Draft7Validator(override_schema)
            for err in v.iter_errors(ov):
                findings.append(_finding(
                    "error", rel, "stat.override-shape",
                    f"StatOverrides[{i}]: {err.message}"))
            target = (ov or {}).get("OverridesDerivedStat", "")
            root = str(target).split(".")[0]
            if root and root not in derived_names:
                findings.append(_finding(
                    "error", rel, "stat.override-shape",
                    f"StatOverrides[{i}] targets '{target}' but '{root}' is not "
                    f"a DerivedStat in Base_Attributes.yaml"))
    return findings


# ── check 5: hardcoded copies of central formulas outside the contract ─────────

_HARDCODE_RE = re.compile(r"\b(STA|Stamina)\s*(?:×|x|\*)\s*100\b", re.IGNORECASE)


def check_hardcoded_formulas():
    findings = []
    scan_roots = ["CombatSim", "Classes", "Guidebooks", "Combat"]
    for root in scan_roots:
        base = REPO_ROOT / root
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*")):
            if p.suffix.lower() not in (".py", ".md", ".yaml", ".yml"):
                continue
            rel = p.relative_to(REPO_ROOT).as_posix()
            try:
                text = p.read_text(encoding="utf-8")
            except Exception:
                continue
            for i, line in enumerate(text.splitlines(), 1):
                if _HARDCODE_RE.search(line):
                    findings.append(_finding(
                        "info", rel, "stat.hardcoded-formula",
                        f"line {i}: hardcodes the MaxHP formula (Stamina × 100) "
                        f"instead of referencing Base_Attributes.yaml — currently "
                        f"consistent by luck, not construction", line=i))
    return findings


# ── check 6: dangling file references in the Attributes contract ───────────────

_REF_RE = re.compile(r"\b((?:Combat|Roles|Ranks)/[A-Za-z_]+\.(?:yaml|yml|md))\b")


def check_dangling_refs():
    findings = []
    for p in sorted((REPO_ROOT / "Attributes").glob("*")):
        if p.suffix.lower() not in (".yaml", ".yml", ".json"):
            continue
        rel = p.relative_to(REPO_ROOT).as_posix()
        text = p.read_text(encoding="utf-8")
        seen = set()
        for m in _REF_RE.finditer(text):
            ref = m.group(1)
            if ref in seen:
                continue
            seen.add(ref)
            if not (REPO_ROOT / ref).exists():
                findings.append(_finding(
                    "warning", rel, "stat.dangling-ref",
                    f"references {ref}, which does not exist in the repo "
                    f"(aspirational contract — create the file or drop the reference)"))
    return findings


def run_stat_contract_checks():
    findings = []
    findings += check_contract_shape()
    findings += check_pending_coefficients()
    findings += check_legacy_drift()
    findings += check_class_overrides()
    findings += check_hardcoded_formulas()
    findings += check_dangling_refs()
    return findings
