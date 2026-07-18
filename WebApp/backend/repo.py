"""Live working-tree I/O for the YAML Library.

All reads/writes hit the REAL repo files (no copy, no database). YAML writes
go through ruamel.yaml round-trip mode so hand-written comments, key order,
and quoting survive an edit — these files are design documents first.
"""

import contextlib
import io
import json
import os
from pathlib import Path
from typing import Optional

from ruamel.yaml import YAML

# backend/ -> WebApp/ -> YAML Library (repo root)
REPO_ROOT = Path(__file__).resolve().parents[2]

# Folders exposed to the file browser. Everything else (git internals, the
# WebApp itself) stays out of the editing surface.
CONTENT_DIRS = [
    "Attributes", "Classes", "CombatSim", "Combat", "Enhancements",
    "Guidebooks", "NPCs", "Passives", "Race_Ideas", "Ranks", "Schemas",
    "Skills", "Zones",
]


def _represent_none_explicit(representer, _data):
    # The repo's hand-written style (and Skill Creator.pyw's output) writes
    # explicit `null`, not an empty scalar.
    return representer.represent_scalar("tag:yaml.org,2002:null", "null")


def _yaml() -> YAML:
    y = YAML()  # round-trip mode is the default
    y.preserve_quotes = True
    y.width = 4096  # never re-wrap long prose lines
    # Match the repo's hand style: sequence dashes indented 2 under their key
    y.indent(mapping=2, sequence=4, offset=2)
    y.representer.add_representer(type(None), _represent_none_explicit)
    return y


def safe_path(rel_path: str) -> Path:
    """Resolve a repo-relative path, refusing traversal outside the repo."""
    p = (REPO_ROOT / rel_path).resolve()
    if REPO_ROOT not in p.parents and p != REPO_ROOT:
        raise ValueError(f"Path escapes repo root: {rel_path}")
    return p


def list_files(category: Optional[str] = None):
    """Repo-relative paths of all YAML/JSON/MD content files, optionally
    limited to one top-level folder."""
    roots = [category] if category else CONTENT_DIRS
    out = []
    for root in roots:
        base = REPO_ROOT / root
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*")):
            if p.suffix.lower() in (".yaml", ".yml", ".json", ".md") and p.is_file():
                out.append(p.relative_to(REPO_ROOT).as_posix())
    return out


def read_file(rel_path: str):
    """Return {"raw": text, "parsed": data-or-None}."""
    p = safe_path(rel_path)
    raw = p.read_text(encoding="utf-8")
    parsed = None
    try:
        if p.suffix.lower() in (".yaml", ".yml"):
            parsed = _yaml().load(io.StringIO(raw))
        elif p.suffix.lower() == ".json":
            parsed = json.loads(raw)
    except Exception:
        parsed = None  # unparseable content is still viewable/editable as raw
    return {"raw": raw, "parsed": parsed}


def load_yaml(rel_path: str):
    """Round-trip-parsed YAML document (CommentedMap) for merge-and-save."""
    p = safe_path(rel_path)
    with p.open("r", encoding="utf-8") as f:
        return _yaml().load(f)


def plain_yaml(rel_path: str):
    """Plain-python parse (safe) — for validators that only inspect."""
    import yaml as pyyaml
    p = safe_path(rel_path)
    with p.open("r", encoding="utf-8") as f:
        return pyyaml.safe_load(f)


def newline_for(p: Path) -> str:
    """Preserve the file's existing dominant line-ending style — the user's
    original files are CRLF; rewriting them as LF turns a one-line edit into
    a whole-file git diff."""
    try:
        return "\r\n" if b"\r\n" in p.read_bytes() else "\n"
    except FileNotFoundError:
        return "\n"


def write_raw(rel_path: str, text: str):
    p = safe_path(rel_path)
    with p.open("w", encoding="utf-8", newline=newline_for(p)) as f:
        f.write(text)


def deep_merge(target, payload):
    """Merge payload into a ruamel round-trip structure IN PLACE.

    Semantics (documented for the PoC): payload keys overwrite or add;
    keys absent from the payload are left untouched (so comments and
    unrelated sections survive); lists are replaced wholesale.
    """
    for key, value in payload.items():
        if (
            key in target
            and isinstance(target[key], dict)
            and isinstance(value, dict)
        ):
            deep_merge(target[key], value)
        elif key in target and target[key] == value:
            # unchanged — keep the original node so its style survives
            # (folded/literal blocks, quoting, inline comments)
            continue
        else:
            target[key] = value
    return target


def merge_write_yaml(rel_path: str, payload: dict):
    """Load the live file round-trip, merge the payload, write back."""
    doc = load_yaml(rel_path)
    if doc is None:
        doc = payload
    else:
        deep_merge(doc, payload)
    p = safe_path(rel_path)
    nl = newline_for(p)
    buf = io.StringIO()
    _yaml().dump(doc, buf)
    with p.open("w", encoding="utf-8", newline=nl) as f:
        f.write(buf.getvalue())


@contextlib.contextmanager
def chdir_repo():
    """Project_Validator.py assumes cwd == repo root; wrap calls in this."""
    prev = os.getcwd()
    os.chdir(REPO_ROOT)
    try:
        yield
    finally:
        os.chdir(prev)
