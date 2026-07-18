"""Design Hub API — FastAPI backend editing the LIVE YAML Library working tree.

Run from the repo root (YAML Library):
    python -m uvicorn WebApp.backend.main:app --reload --port 8400
"""

import json
from pathlib import Path
from typing import Optional

from fastapi import Body, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from . import repo
from . import ability_io
from . import tracker
from .validators import run_all
from .validators.skill_schema import validate_skill_payload

app = FastAPI(title="Juice Design Hub", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def no_cache_frontend(request, call_next):
    """Local dev tool: the browser must always revalidate the ESM modules,
    or UI changes silently don't appear until a hard refresh."""
    response = await call_next(request)
    if not request.url.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-cache"
    return response


@app.get("/api/files")
def list_files(category: Optional[str] = Query(default=None)):
    return {"files": repo.list_files(category)}


@app.get("/api/file/{rel_path:path}")
def read_file(rel_path: str):
    try:
        return repo.read_file(rel_path)
    except FileNotFoundError:
        raise HTTPException(404, f"No such file: {rel_path}")
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.put("/api/file/{rel_path:path}")
def write_file(rel_path: str, body: dict = Body(...)):
    """Write to the live tree. Body: {"raw": "..."} writes text verbatim;
    {"parsed": {...}} merges into the round-trip-loaded YAML (comments and
    untouched keys survive; payload keys overwrite/add; lists replace)."""
    try:
        if "raw" in body:
            repo.write_raw(rel_path, body["raw"])
        elif "parsed" in body:
            if not rel_path.lower().endswith((".yaml", ".yml")):
                raise HTTPException(400, "parsed writes are YAML-only")
            repo.merge_write_yaml(rel_path, body["parsed"])
        else:
            raise HTTPException(400, "body must contain 'raw' or 'parsed'")
    except HTTPException:
        raise
    except FileNotFoundError:
        raise HTTPException(404, f"No such file: {rel_path}")
    except ValueError as e:
        raise HTTPException(400, str(e))
    return {"ok": True, "path": rel_path}


@app.get("/api/attributes")
def attributes():
    """Stat contract: Tier-1 attributes, derived stats with coefficient states,
    and the StatOverrides registry assembled from class Design files."""
    base = repo.plain_yaml("Attributes/Base_Attributes.yaml")
    bc = base.get("Base_Character") or {}
    derived = bc.get("DerivedStats") or {}

    pending = []
    for stat_name, stat in derived.items():
        if not isinstance(stat, dict):
            continue
        for cname, coeff in (stat.get("Coefficients") or {}).items():
            if isinstance(coeff, dict) and coeff.get("Value") == "PENDING":
                pending.append({"stat": stat_name, "coefficient": cname,
                                "note": coeff.get("Note", "")})

    overrides = []
    for p in sorted((repo.REPO_ROOT / "Classes").rglob("*_Design.yaml")):
        rel = p.relative_to(repo.REPO_ROOT).as_posix()
        try:
            data = repo.plain_yaml(rel)
        except Exception:
            continue
        for ov in (data or {}).get("StatOverrides") or []:
            overrides.append({"declaredIn": rel, **(ov or {})})

    return {"attributes": bc.get("Attributes") or {},
            "derivedStats": derived,
            "pendingCoefficients": pending,
            "statOverrides": overrides}


@app.get("/api/skills")
def skills():
    registry = []
    for p in sorted((repo.REPO_ROOT / "Skills").glob("*.yaml")):
        rel = p.relative_to(repo.REPO_ROOT).as_posix()
        try:
            data = repo.plain_yaml(rel)
        except Exception:
            continue
        if isinstance(data, dict) and data.get("Key"):
            registry.append({
                "key": data["Key"], "name": data.get("Name", ""), "file": rel,
                "actionType": data.get("ActionType"),
                "effectTypes": [e.get("Type") for e in data.get("Effects") or []
                                if isinstance(e, dict)],
                "migrated": bool(data.get("Effects")),
            })
    return {"skills": registry}


@app.get("/api/abilities/{rel_path:path}")
def list_abilities(rel_path: str):
    """Every ability record in a skill file, with its address (path from the
    document root), methodology grade, and missing fields."""
    try:
        return {"abilities": ability_io.list_abilities(rel_path)}
    except FileNotFoundError:
        raise HTTPException(404, f"No such file: {rel_path}")
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.put("/api/ability/{rel_path:path}")
def write_ability(rel_path: str, body: dict = Body(...)):
    """Targeted, alias-aware merge into ONE ability record.
    Body: {"path": [keys/indices...], "patch": {field: value}} — canonical
    methodology field names are written to the record's existing spelling."""
    try:
        ability_io.write_ability(rel_path, body.get("path") or [], body.get("patch") or {})
    except FileNotFoundError:
        raise HTTPException(404, f"No such file: {rel_path}")
    except (ValueError, KeyError, IndexError, TypeError) as e:
        raise HTTPException(400, f"bad ability path/patch: {e}")
    return {"ok": True}


@app.get("/api/tracker")
def get_tracker():
    """Finalization tracker: roster design status (class_list_qual_context.md)
    joined with per-class ability finalized/draft counts."""
    return tracker.build_tracker()


@app.get("/api/schema/skill")
def skill_schema():
    schema = json.loads((repo.REPO_ROOT / "Schemas/skill.schema.json")
                        .read_text(encoding="utf-8"))
    vocab = repo.plain_yaml("Schemas/EffectTypes.yaml").get("EffectTypes") or {}
    return {"schema": schema, "effectTypes": vocab}


@app.post("/api/validate")
def validate():
    findings = run_all()
    counts = {}
    for f in findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1
    return {"counts": counts, "findings": findings}


@app.post("/api/validate/payload")
def validate_payload(payload: dict = Body(...)):
    return {"findings": validate_skill_payload(payload)}


@app.get("/api/graph")
def graph():
    """Relationship graph — port of Hub_Master.pyw's export_project_relationships
    scan, extended with skill→class and race→bonus-skill edges."""
    nodes, edges, seen = [], [], set()

    def add_node(node_id, category):
        if node_id and node_id not in seen:
            seen.add(node_id)
            nodes.append({"id": node_id, "category": category})

    def add_edge(src, dst, kind):
        if src and dst:
            edges.append({"from": src, "to": dst, "kind": kind})

    for rel in repo.list_files():
        if not rel.endswith((".yaml", ".yml")):
            continue
        try:
            data = repo.plain_yaml(rel)
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        key = data.get("Key")
        category = rel.split("/")[0]
        if key:
            add_node(key, category)
            for status in data.get("AppliesStatuses") or []:
                add_node(status, "Passives")
                add_edge(key, status, "applies")
            for cls in data.get("ClassRestrictions") or []:
                add_node(cls, "Classes")
                add_edge(key, cls, "restricted_to")
            for skill in data.get("AssignedSkills") or []:
                add_node(skill, "Skills")
                add_edge(key, skill, "assigned")
            for eff in data.get("Effects") or []:
                if isinstance(eff, dict) and eff.get("Type") == "StatusApply":
                    add_node(eff.get("Status"), "Passives")
                    add_edge(key, eff.get("Status"), "applies")
        definition = data.get("Definition") or {}
        if isinstance(definition, dict) and definition.get("Subrace"):
            race = definition["Subrace"]
            add_node(race, "Race_Ideas")
            for skill in definition.get("BonusSkills") or []:
                add_node(skill, "Skills")
                add_edge(race, skill, "bonus_skill")
    return {"nodes": nodes, "edges": edges}


# Serve the frontend: a Vite build (dist/) wins if present; otherwise the
# no-build ESM app in public/ (works without Node installed).
_frontend = Path(__file__).resolve().parent.parent / "frontend"
_serve_dir = _frontend / "dist" if (_frontend / "dist").is_dir() else _frontend / "public"
if _serve_dir.is_dir():
    app.mount("/", StaticFiles(directory=_serve_dir, html=True), name="frontend")
