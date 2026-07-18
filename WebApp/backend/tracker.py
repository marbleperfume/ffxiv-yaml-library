"""Finalization tracker — the iterative-draft-finalization queue made visible.

Design status comes from Guidebooks/class_list_qual_context.md (the roster's
✅/🔴/⚠️ markers and blocking notes). Implementation status comes from grading
every ability in the class's Classes/2.0/*_Skills*.yaml files (methodology
grader). Race-locked classes that live outside the roster doc (Grappler,
Wavecaller, Skyreign, ... — covered by new_locked_classes_qual.md and
class_item_baselines.md instead) are included from their files and marked so.
"""

import re

from .repo import REPO_ROOT
from . import ability_io

ROSTER_DOC = "Guidebooks/class_list_qual_context.md"

# Roster name → skill-file basename stem. Each alias is evidenced in the repo:
#   Warrior      → MadoltMetaknight_Design.yaml:55  "PreviousName: Madolt Warrior"
#   Elementalist → TryllElementalScholar_Design.yaml:33 "CategoryTag: Elementalist"
#   Adafold      → files use the Adabold spelling (both appear in the repo)
FILE_ALIASES = {
    "warrior": "MadoltMetaknight",
    "elementalist": "TryllElementalScholar",
    "adafold": "Adabold",
}

_BLOCKED_PHRASES = re.compile(
    r"lacking enemy design|needs enemy NPCs|will have to wait", re.IGNORECASE)


def _parse_roster():
    """Yield one entry per `### N. Class` section, carrying its tier heading."""
    text = (REPO_ROOT / ROSTER_DOC).read_text(encoding="utf-8")
    entries = []
    tier = ""
    current = None
    for line in text.splitlines():
        m_tier = re.match(r"^##\s+([^#].*)$", line)
        m_class = re.match(r"^###\s+\d+\.\s+(.+)$", line)
        if m_tier and not m_class:
            tier = m_tier.group(1).strip()
            continue
        if m_class:
            current = {"title": m_class.group(1).strip(), "tier": tier, "fields": {}}
            entries.append(current)
            continue
        if current is not None:
            m_field = re.match(r"^-\s+\*\*(.+?):\*\*\s*(.*)$", line)
            if m_field:
                current["fields"][m_field.group(1).strip()] = m_field.group(2).strip()
    return entries


def _classify(entry):
    status_text = entry["fields"].get("YAML Status", "")
    qual = entry["fields"].get("Qual Context", "")
    if "🔴" in status_text:
        status = "blocked" if _BLOCKED_PHRASES.search(qual) else "undesigned"
    elif "✅" in status_text:
        status = "complete"
    else:
        status = "unknown"
    rework = "⚠️" in status_text or "⚠" in status_text
    return status, rework, status_text


def _skill_files_for(stem):
    return sorted(
        p.relative_to(REPO_ROOT).as_posix()
        for p in (REPO_ROOT / "Classes").rglob(f"{stem}_Skills*.yaml"))


def _ability_counts(files):
    finalized = draft = 0
    for rel in files:
        try:
            for a in ability_io.list_abilities(rel):
                if a["grade"] == "finalized":
                    finalized += 1
                else:
                    draft += 1
        except Exception:
            continue
    return {"finalized": finalized, "draft": draft, "total": finalized + draft}


def build_tracker():
    classes = []
    matched_stems = set()

    for entry in _parse_roster():
        title = entry["title"]
        base_name = re.sub(r"\s*\(.*\)$", "", title).strip()
        status, rework, status_text = _classify(entry)
        stem = FILE_ALIASES.get(base_name.lower(), base_name.replace(" ", ""))
        files = _skill_files_for(stem)
        matched_stems.add(stem)
        classes.append({
            "name": title,
            "tier": entry["tier"],
            "race": entry["fields"].get("Race", ""),
            "role": entry["fields"].get("Role", ""),
            "designStatus": status,
            "rework": rework,
            "statusText": status_text,
            "qualContext": entry["fields"].get("Qual Context", ""),
            "skillFiles": files,
            "abilities": _ability_counts(files),
        })

    # Race-locked classes with skill files but no roster entry
    seen = set()
    for p in sorted((REPO_ROOT / "Classes").rglob("*_Skills*.yaml")):
        stem = re.sub(r"_Skills.*$", "", p.stem)
        if stem in matched_stems or stem in seen:
            continue
        seen.add(stem)
        files = _skill_files_for(stem)
        classes.append({
            "name": stem,
            "tier": "Race-Locked (outside roster doc)",
            "race": "",
            "role": "",
            "designStatus": "listed-elsewhere",
            "rework": False,
            "statusText": "Not in class_list_qual_context.md — covered by new_locked_classes_qual.md / class_item_baselines.md",
            "qualContext": "",
            "skillFiles": files,
            "abilities": _ability_counts(files),
        })

    counts = {}
    for c in classes:
        counts[c["designStatus"]] = counts.get(c["designStatus"], 0) + 1
    return {"classes": classes, "counts": counts}
