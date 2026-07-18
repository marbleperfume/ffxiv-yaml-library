"""Regenerates Attributes/attributes.json from Attributes/Base_Attributes.yaml.

attributes.json is GENERATED OUTPUT kept only so the legacy tkinter creator
tools (via Attributes/attr_loader.py) keep working. Base_Attributes.yaml is
the single source of truth; hand-editing the json recreates the drift this
generator exists to kill.

Run:  python WebApp/backend/generate_legacy.py   (from the repo root, or anywhere)
"""

import io
import json
import re
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from backend.repo import REPO_ROOT, load_yaml, safe_path
else:
    from .repo import REPO_ROOT, load_yaml, safe_path

_GENERATED_NOTE = (
    "AUTO-GENERATED from Attributes/Base_Attributes.yaml — do not hand-edit. "
    "Regenerate with: python WebApp/backend/generate_legacy.py"
)


def _clean_comment(token_text: str) -> str:
    """Turn a ruamel end-of-line comment blob into one intent sentence."""
    lines = []
    for line in token_text.splitlines():
        line = line.strip()
        if not line.startswith("#"):
            break  # stop at the first blank/non-comment line
        lines.append(line.lstrip("#").strip())
    return " ".join(lines).strip()


def build_legacy_json() -> dict:
    doc = load_yaml("Attributes/Base_Attributes.yaml")
    attrs = doc["Base_Character"]["Attributes"]

    out = {"_generated": _GENERATED_NOTE}
    for key, value in attrs.items():
        intent = ""
        try:
            comment_items = attrs.ca.items.get(key)
            if comment_items and comment_items[2] is not None:
                intent = _clean_comment(comment_items[2].value)
        except Exception:
            intent = ""
        out[str(key).upper()] = {"default": str(value), "intent": intent}
    return out


def write_legacy_json() -> Path:
    target = safe_path("Attributes/attributes.json")
    data = build_legacy_json()
    with target.open("w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False) + "\n")
    return target


if __name__ == "__main__":
    path = write_legacy_json()
    print(f"Regenerated {path.relative_to(REPO_ROOT)} from Base_Attributes.yaml")
