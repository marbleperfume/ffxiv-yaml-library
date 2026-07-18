"""Structured validators for the YAML Library.

Every check returns findings shaped as:
    {"severity": "error"|"warning"|"pending"|"legacy"|"info",
     "file": "repo/relative/path.yaml", "line": int|None,
     "rule": "dotted.rule.id", "message": "..."}

Severities:
    error   — contract violation; must be fixed or formally declared
    warning — suspicious / dangling; worth a look
    pending — a coefficient the user has intentionally not decided yet
    legacy  — pre-schema content awaiting incremental migration (not wrong)
    info    — surfaced for awareness (e.g. hardcoded formula copies)
"""

from .core import run_core_validator
from .stat_contract import run_stat_contract_checks
from .skill_schema import run_skill_schema_checks


def run_all():
    findings = []
    findings += run_core_validator()
    findings += run_stat_contract_checks()
    findings += run_skill_schema_checks()
    order = {"error": 0, "warning": 1, "pending": 2, "legacy": 3, "info": 4}
    findings.sort(key=lambda f: (order.get(f["severity"], 9), f["file"]))
    return findings
