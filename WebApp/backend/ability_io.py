"""Ability-level read/write for the editor.

Reads return every ability record in a file with its address (path from the
document root) and its methodology grade. Writes are TARGETED: only the one
record at the given path is merged, alias-aware — a canonical field name in
the patch is written to the spelling the record already uses (so editing
Grappler never churns its snake_case into PascalCase), and brand-new fields
adopt the record's dominant convention. Everything else in the file — other
abilities, comments, folded blocks — is untouched.
"""

import io

from .repo import _yaml, load_yaml, newline_for, safe_path
from .validators.skill_schema import (
    ALIASES, find_ability_records, grade_ability, _ability_name,
)


def list_abilities(rel_path):
    data = _plain(rel_path)
    pairs = []
    if isinstance(data, (dict, list)):
        find_ability_records(data, pairs)
    out = []
    for path, rec in pairs:
        grade, missing = grade_ability(rec)
        out.append({
            "path": path,
            "name": _ability_name(rec),
            "grade": grade,
            "missing": missing,
            "record": rec,
        })
    return out


def _plain(rel_path):
    import yaml as pyyaml
    with safe_path(rel_path).open("r", encoding="utf-8") as f:
        return pyyaml.safe_load(f)


def _navigate(doc, path):
    node = doc
    for step in path:
        node = node[step]
    return node


def _resolve_write_key(record, field):
    """The spelling to write `field` under: the record's existing alias if any;
    otherwise the record's dominant naming convention (snake_case files get the
    snake alias, PascalCase files get the canonical name)."""
    spellings = ALIASES.get(field, [field])
    for sp in spellings:
        if sp in record:
            return sp
    keys = [k for k in record.keys() if isinstance(k, str)]
    snakeish = sum(1 for k in keys if k == k.lower())
    if keys and snakeish >= len(keys) / 2:
        for sp in spellings:
            if sp == sp.lower():
                return sp
    return field


def write_ability(rel_path, path, patch):
    """Merge `patch` into the ability at `path` inside the live file.
    Patch keys may be canonical methodology names (resolved to the record's
    spelling) or literal keys (written as-is when already present). A patch
    value of None on an aliased field writes an explicit null (a declaration,
    e.g. cc_stage: null), never a deletion."""
    doc = load_yaml(rel_path)
    node = _navigate(doc, path)
    if not isinstance(node, dict):
        raise ValueError(f"path {path} does not address a mapping")

    for field, value in patch.items():
        key = _resolve_write_key(node, field)
        if key in node and node[key] == value:
            continue  # unchanged — keep the original node & its styling
        node[key] = value

    p = safe_path(rel_path)
    nl = newline_for(p)
    buf = io.StringIO()
    _yaml().dump(doc, buf)
    with p.open("w", encoding="utf-8", newline=nl) as f:
        f.write(buf.getvalue())
