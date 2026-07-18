"""Wraps the existing repo-root Project_Validator.py — no logic duplicated.

Project_Validator.validate_project(collector=...) appends its message strings
to the collector instead of printing; we lift them into structured findings.
"""

import re
import sys

from ..repo import REPO_ROOT, chdir_repo

sys.path.insert(0, str(REPO_ROOT))
import Project_Validator  # noqa: E402  (the real, unduplicated validator)

_FILE_RE = re.compile(r"^([\w./\\-]+\.ya?ml)\b")


def run_core_validator():
    collector = []
    with chdir_repo():
        Project_Validator.validate_project(collector=collector)
    findings = []
    for msg in collector:
        m = _FILE_RE.match(msg)
        findings.append({
            "severity": "error",
            "file": m.group(1).replace("\\", "/") if m else "",
            "line": None,
            "rule": "core.integrity",
            "message": msg,
        })
    return findings
