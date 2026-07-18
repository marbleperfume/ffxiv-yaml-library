import React, { useState, useEffect, useMemo, useRef } from "react";
import htm from "htm";

const html = htm.bind(React.createElement);

/* ── shared helpers ──────────────────────────────────────────────────────── */

const numeric = (v) => (typeof v === "string" && /^-?\d+(\.\d+)?$/.test(v.trim()) ? Number(v) : v);

function useDebounced(fn, ms) {
  const t = useRef(null);
  return (...args) => {
    clearTimeout(t.current);
    t.current = setTimeout(() => fn(...args), ms);
  };
}

/* Methodology field logic — mirrors the backend grader; alias data comes from
   the schema's x-fieldAliases so it is never duplicated by hand. */

const METHODOLOGY = ["TriggerCondition", "ItemBaselineReplaced", "DecisionCreated", "CCStage", "RankProgression"];

const FIELD_DOCS = {
  TriggerCondition: "When is this the correct button? “None (always available)” is a valid declared trigger.",
  ItemBaselineReplaced: "Which item(s) a party without this class uses for the same job — and why this is the premium replacement. “No item equivalent — …” is valid.",
  DecisionCreated: "The player choice this ability forces. Decision density is the game.",
  CCStage: "CC budget contract. “No CC (null)” is an explicit declaration, not an omission.",
  RankProgression: "Per-rank capability changes — Rank = capability, gear = numbers.",
};

function aliasList(schema, canonical) {
  const map = (schema.schema && schema.schema["x-fieldAliases"]) || {};
  return [canonical, ...(map[canonical] || []).filter((s) => s !== canonical)];
}

function readField(rec, schema, canonical) {
  for (const sp of aliasList(schema, canonical)) {
    if (sp in rec) return { key: sp, value: rec[sp] };
  }
  return { key: null, value: undefined };
}

const isPending = (v) => typeof v === "string" && v.trim().toUpperCase().startsWith("PENDING");

function gradeOf(rec, schema) {
  const missing = [];
  for (const f of METHODOLOGY) {
    const { key, value } = readField(rec, schema, f);
    if (key === null || isPending(value)) missing.push(f + (key !== null ? " (PENDING)" : ""));
  }
  return { grade: missing.length ? "draft" : "finalized", missing };
}

function resolveWriteKey(rec, schema, canonical) {
  for (const sp of aliasList(schema, canonical)) if (sp in rec) return sp;
  const keys = Object.keys(rec);
  const snakeish = keys.filter((k) => k === k.toLowerCase()).length;
  if (keys.length && snakeish >= keys.length / 2) {
    for (const sp of aliasList(schema, canonical)) if (sp === sp.toLowerCase()) return sp;
  }
  return canonical;
}

/* ── FileBrowser ─────────────────────────────────────────────────────────── */

export function FileBrowser({ files, current, onOpen }) {
  const [open, setOpen] = useState({ Skills: true, Attributes: true, Schemas: true });
  const groups = useMemo(() => {
    const g = {};
    for (const f of files) {
      const top = f.split("/")[0];
      (g[top] = g[top] || []).push(f);
    }
    return g;
  }, [files]);

  return html`
    <div class="sidebar">
      ${Object.entries(groups).map(([group, list]) => html`
        <div key=${group}>
          <div class="group-title" onClick=${() => setOpen({ ...open, [group]: !open[group] })}>
            ${open[group] ? "▾" : "▸"} ${group} (${list.length})
          </div>
          ${open[group] && list.map((f) => html`
            <div key=${f} class=${"file" + (f === current ? " active" : "")}
                 title=${f} onClick=${() => onOpen(f)}>
              ${f.slice(group.length + 1)}
            </div>
          `)}
        </div>
      `)}
    </div>
  `;
}

/* ── Findings list (shared) ──────────────────────────────────────────────── */

function FindingRow({ f, onOpenFile }) {
  return html`
    <div class=${"finding " + f.severity}>
      <span class="sev">${f.severity}</span>
      <span class="rule">${f.rule || ""}</span>
      <span>
        ${f.message}
        ${f.file && html` <span class="file-ref" style=${{ cursor: onOpenFile ? "pointer" : "default" }}
          onClick=${() => onOpenFile && onOpenFile(f.file)}>— ${f.file}${f.line ? ":" + f.line : ""}</span>`}
      </span>
    </div>
  `;
}

/* ── EffectCard (typed mechanical packet) ────────────────────────────────── */

const UNIVERSAL_OPTIONAL = ["Condition", "Flavor", "Note"];

function EffectCard({ effect, vocab, onChange, onRemove }) {
  const spec = vocab[effect.Type] || {};
  const req = spec.RequiredParams || [];
  const opt = [...(spec.OptionalParams || []), ...UNIVERSAL_OPTIONAL];
  const setParam = (k, v) => onChange({ ...effect, [k]: v === "" ? undefined : numeric(v) });

  return html`
    <div class="effect-card">
      <div class="effect-head">
        <select value=${effect.Type} onChange=${(e) => onChange({ Type: e.target.value })}>
          ${Object.keys(vocab).map((t) => html`<option key=${t} value=${t}>${t}</option>`)}
        </select>
        <span class="desc">${spec.Description || ""}</span>
        <button class="ghost" onClick=${onRemove}>Remove</button>
      </div>
      <div class="effect-params">
        ${req.map((p) => html`
          <div key=${p} class="field req">
            <label>${p}</label>
            <input value=${effect[p] ?? ""} onInput=${(e) => setParam(p, e.target.value)} />
          </div>
        `)}
        ${opt.map((p) => html`
          <div key=${p} class="field">
            <label>${p}</label>
            <input value=${effect[p] ?? ""} onInput=${(e) => setParam(p, e.target.value)} />
          </div>
        `)}
      </div>
    </div>
  `;
}

/* ── Methodology widgets ─────────────────────────────────────────────────── */

function CCStageField({ draft, schema, update }) {
  const cc = readField(draft, schema, "CCStage");
  const mode = cc.key === null ? "__nd__"
    : cc.value === null ? "null"
    : typeof cc.value === "number" ? String(cc.value)
    : "custom";

  const set = (m) => {
    if (m === "__nd__") return;
    if (m === "null") update("CCStage", null, true);
    else if (m === "custom") update("CCStage", typeof cc.value === "string" ? cc.value : "Varies — describe per variant", true);
    else update("CCStage", Number(m), true);
  };

  return html`
    <div class="field">
      <label>CCStage ${cc.key && cc.key !== "CCStage" ? html`<span class="alias-note">(${cc.key})</span>` : ""}</label>
      <select value=${mode} onChange=${(e) => set(e.target.value)}>
        ${cc.key === null && html`<option value="__nd__">— not declared —</option>`}
        <option value="null">No CC (null — declared)</option>
        <option value="1">Stage 1</option>
        <option value="2">Stage 2</option>
        <option value="3">Stage 3</option>
        <option value="custom">Custom / varies…</option>
      </select>
      ${mode === "custom" && html`
        <input value=${typeof cc.value === "string" ? cc.value : ""}
               onInput=${(e) => update("CCStage", e.target.value, true)} />
      `}
    </div>
  `;
}

function RankProgressionField({ draft, schema, update }) {
  const rp = readField(draft, schema, "RankProgression");
  const writeKey = resolveWriteKey(draft, schema, "RankProgression");
  const makeTable = () => {
    const keys = writeKey === writeKey.toLowerCase()
      ? ["rank_1", "rank_2", "rank_3", "rank_4"] : ["R1", "R2", "R3", "R4"];
    const table = {};
    for (const k of keys) table[k] = "";
    update("RankProgression", table, true);
  };

  if (rp.key === null) {
    return html`
      <div class="field wide">
        <label>RankProgression <span class="alias-note">— not declared</span></label>
        <div class="btn-row">
          <button class="ghost" onClick=${makeTable}>Create rank table</button>
          <button class="ghost" onClick=${() => update("RankProgression", "PENDING — rank pass not yet run for this ability", true)}>Mark PENDING</button>
        </div>
      </div>
    `;
  }
  if (typeof rp.value === "string") {
    return html`
      <div class="field wide">
        <label>RankProgression ${rp.key !== "RankProgression" ? html`<span class="alias-note">(${rp.key})</span>` : ""}</label>
        <textarea value=${rp.value} onInput=${(e) => update("RankProgression", e.target.value, true)}></textarea>
        <div class="btn-row"><button class="ghost" onClick=${makeTable}>Convert to rank table</button></div>
      </div>
    `;
  }
  const table = rp.value || {};
  return html`
    <div class="field wide">
      <label>RankProgression ${rp.key !== "RankProgression" ? html`<span class="alias-note">(${rp.key})</span>` : ""}</label>
      ${Object.entries(table).map(([rk, rv]) => html`
        <div key=${rk} class="rank-row">
          <span class="rank-label">${rk}</span>
          <textarea value=${typeof rv === "string" ? rv : JSON.stringify(rv)}
                    onInput=${(e) => update("RankProgression", { ...table, [rk]: e.target.value }, true)}></textarea>
        </div>
      `)}
    </div>
  `;
}

function MethodologyTextField({ draft, schema, update, canonical, missing }) {
  const f = readField(draft, schema, canonical);
  const isMissing = missing.some((m) => m.startsWith(canonical));
  return html`
    <div class=${"field wide" + (isMissing ? " missing" : "")}>
      <label>
        ${canonical}
        ${f.key && f.key !== canonical ? html`<span class="alias-note">(${f.key})</span>` : ""}
        ${isMissing ? html`<span class="missing-flag">needed for finalized</span>` : ""}
      </label>
      <div class="field-doc">${FIELD_DOCS[canonical]}</div>
      <textarea value=${typeof f.value === "string" ? f.value : f.value === undefined ? "" : JSON.stringify(f.value)}
                onInput=${(e) => update(canonical, e.target.value, true)}></textarea>
    </div>
  `;
}

/* ── AbilityForm — the methodology-first editor ──────────────────────────── */

const PROSE_KEYS = ["Intent", "Flavor", "effect", "Effect", "notes", "Notes", "DesignIntent", "AntiPattern", "section_25_note"];
const PACKET_SCALARS = ["Type", "Potency", "Range", "Duration"];
const GATING = ["ResourceCost", "ResourceGeneration", "Cooldown"];

function AbilityForm({ file, ability, schema, api, onSaved }) {
  const [draft, setDraft] = useState(() => JSON.parse(JSON.stringify(ability.record)));
  const [findings, setFindings] = useState([]);
  const [saved, setSaved] = useState(false);
  const vocab = schema.effectTypes;

  const revalidate = useDebounced((payload) => {
    api.post("/api/validate/payload", payload).then((d) => setFindings(d.findings)).catch(() => {});
  }, 500);

  const update = (name, value, canonical) => {
    const key = canonical ? resolveWriteKey(draft, schema, name) : name;
    const next = { ...draft, [key]: value };
    setDraft(next);
    setSaved(false);
    revalidate(next);
  };

  const save = () => {
    const original = ability.record;
    const patch = {};
    for (const [k, v] of Object.entries(draft)) {
      if (!(k in original) || JSON.stringify(original[k]) !== JSON.stringify(v)) patch[k] = v;
    }
    api.put(`/api/ability/${file.path}`, { path: ability.path, patch }).then(() => {
      setSaved(true);
      onSaved && onSaved();
    });
  };

  const { grade, missing } = gradeOf(draft, schema);
  const effects = draft.Effects || [];

  // §25 hint: a cooldown over 15s with no §25 marker anywhere in the record
  const cd = readField(draft, schema, "Cooldown");
  const cdSecs = typeof cd.value === "number" ? cd.value
    : typeof cd.value === "string" ? parseFloat(cd.value) : NaN;
  const s25Marked = Object.values(draft).some((v) => typeof v === "string" && /§\s*25|section_25/i.test(v)) || "section_25_note" in draft;
  const s25Warn = !Number.isNaN(cdSecs) && cdSecs > 15 && !s25Marked;

  // keys already rendered by a dedicated section — everything else goes to "Other"
  const consumed = new Set(["Name", "name", "Effects", "Key"]);
  for (const c of [...METHODOLOGY, ...GATING, "CritCondition"]) {
    const f = readField(draft, schema, c);
    if (f.key) consumed.add(f.key);
  }
  for (const p of PROSE_KEYS) if (p in draft && typeof draft[p] === "string") consumed.add(p);
  for (const p of PACKET_SCALARS) {
    const f = readField(draft, schema, p);
    if (f.key && (typeof f.value !== "object" || f.value === null)) consumed.add(f.key);
  }
  const other = Object.keys(draft).filter((k) => !consumed.has(k));

  return html`
    <div class="ability-form">
      <div class="editor-head">
        <span class=${"grade-banner " + grade}>
          ${grade === "finalized" ? "FINALIZED ✓" : `DRAFT — missing: ${missing.join(", ")}`}
        </span>
        <button class="primary" onClick=${save}
                disabled=${findings.some((f) => f.severity === "error")}>Save</button>
        ${saved && html`<span class="saved-note">saved ✓</span>`}
      </div>

      <div class="section-title">Design — methodology (the actual work)</div>
      <${MethodologyTextField} draft=${draft} schema=${schema} update=${update} canonical="TriggerCondition" missing=${missing} />
      <${MethodologyTextField} draft=${draft} schema=${schema} update=${update} canonical="ItemBaselineReplaced" missing=${missing} />
      <${MethodologyTextField} draft=${draft} schema=${schema} update=${update} canonical="DecisionCreated" missing=${missing} />
      <div class="form-grid">
        <${CCStageField} draft=${draft} schema=${schema} update=${update} />
        <div class="field">
          <label>CritCondition <span class="alias-note">(deterministic — never RNG)</span></label>
          <input value=${readField(draft, schema, "CritCondition").value ?? ""}
                 onInput=${(e) => update("CritCondition", e.target.value, true)} />
        </div>
      </div>
      <${RankProgressionField} draft=${draft} schema=${schema} update=${update} />

      <div class="section-title">Gating — §25: identity = resource-gated, never CD-gated</div>
      ${s25Warn && html`<div class="s25-warn">⚠ Cooldown over 15s with no §25 marker — if this is an identity ability, convert to a resource gate (or add a section_25_note).</div>`}
      <div class="form-grid">
        ${GATING.map((g) => {
          const f = readField(draft, schema, g);
          return html`
            <div key=${g} class="field">
              <label>${g} ${f.key && f.key !== g ? html`<span class="alias-note">(${f.key})</span>` : ""}</label>
              <input value=${f.value === undefined || f.value === null ? "" : (typeof f.value === "object" ? JSON.stringify(f.value) : f.value)}
                     onInput=${(e) => update(g, numeric(e.target.value), true)} />
            </div>
          `;
        })}
      </div>

      <div class="section-title">Mechanical packet — downstream serialization</div>
      <div class="form-grid">
        ${PACKET_SCALARS.map((p) => {
          const f = readField(draft, schema, p);
          if (f.key && typeof f.value === "object" && f.value !== null) return null;
          return html`
            <div key=${p} class="field">
              <label>${p} ${f.key && f.key !== p ? html`<span class="alias-note">(${f.key})</span>` : ""}</label>
              <input value=${f.value ?? ""} onInput=${(e) => update(f.key || p, numeric(e.target.value), !f.key)} />
            </div>
          `;
        })}
      </div>
      ${effects.map((eff, i) => html`
        <${EffectCard} key=${i} effect=${eff} vocab=${vocab}
          onChange=${(next) => update("Effects", effects.map((e, j) => (j === i ? next : e)))}
          onRemove=${() => update("Effects", effects.filter((_, j) => j !== i))} />
      `)}
      <button class="ghost" onClick=${() => update("Effects", [...effects, { Type: "Damage" }])}>+ Add typed effect</button>

      ${PROSE_KEYS.some((p) => p in draft && typeof draft[p] === "string") && html`
        <div class="section-title">Prose</div>
      `}
      ${PROSE_KEYS.filter((p) => p in draft && typeof draft[p] === "string").map((p) => html`
        <div key=${p} class="field wide">
          <label>${p}</label>
          <textarea value=${draft[p]} onInput=${(e) => update(p, e.target.value)}></textarea>
        </div>
      `)}

      ${other.length > 0 && html`
        <details class="other-fields">
          <summary>Other fields (${other.length}) — edit in raw mode</summary>
          <pre>${JSON.stringify(Object.fromEntries(other.map((k) => [k, draft[k]])), null, 2)}</pre>
        </details>
      `}

      <div class="findings">
        ${findings.map((f, i) => html`<${FindingRow} key=${i} f=${f} />`)}
      </div>
    </div>
  `;
}

/* ── AbilityFileEditor — ability list + form ─────────────────────────────── */

export function AbilityFileEditor({ file, schema, api, onSaved }) {
  const [idx, setIdx] = useState(0);
  const abilities = file.abilities;
  const sel = abilities[Math.min(idx, abilities.length - 1)];
  const counts = abilities.reduce((a, x) => { a[x.grade] = (a[x.grade] || 0) + 1; return a; }, {});

  return html`
    <div>
      <div class="editor-head">
        <span class="path">${file.path}</span>
        <span class="file-counts">
          ${counts.finalized || 0} finalized · ${counts.draft || 0} draft
        </span>
      </div>
      <div class="ability-layout">
        <div class="ability-list">
          ${abilities.map((a, i) => html`
            <div key=${i} class=${"ability-item" + (a === sel ? " active" : "")}
                 onClick=${() => setIdx(i)} title=${a.missing.join(", ")}>
              <span class=${"grade-dot " + a.grade}></span>
              <span class="ability-name">${a.name}</span>
              ${a.grade === "draft" && html`<span class="miss-count">${a.missing.length}</span>`}
            </div>
          `)}
        </div>
        ${sel && html`<${AbilityForm} key=${file.path + ":" + abilities.indexOf(sel)}
          file=${file} ability=${sel} schema=${schema} api=${api} onSaved=${onSaved} />`}
      </div>
    </div>
  `;
}

/* ── RawEditor ───────────────────────────────────────────────────────────── */

export function RawEditor({ file, api }) {
  const [text, setText] = useState(file.raw);
  const [saved, setSaved] = useState(false);
  return html`
    <div>
      <div class="editor-head">
        <span class="path">${file.path} <span style=${{ color: "var(--muted)" }}>(raw mode)</span></span>
        <button class="primary" onClick=${() =>
          api.put(`/api/file/${file.path}`, { raw: text }).then(() => setSaved(true))}>Save</button>
        ${saved && html`<span class="saved-note">saved ✓</span>`}
      </div>
      <textarea class="raw-editor" value=${text}
                onInput=${(e) => { setText(e.target.value); setSaved(false); }}></textarea>
    </div>
  `;
}

/* ── ValidationPanel ─────────────────────────────────────────────────────── */

const SEVERITIES = ["error", "warning", "pending", "legacy", "info"];

export function ValidationPanel({ api, onOpenFile }) {
  const [data, setData] = useState(null);
  const [show, setShow] = useState({ error: true, warning: true, pending: true, legacy: true, info: false });

  useEffect(() => { api.post("/api/validate").then(setData); }, []);

  if (!data) return html`<div class="empty">Running validators…</div>`;

  const visible = data.findings.filter((f) => show[f.severity]);
  return html`
    <div>
      <div class="counts">
        ${SEVERITIES.map((s) => html`
          <span key=${s} class=${"count-chip" + (show[s] ? "" : " off")}
                onClick=${() => setShow({ ...show, [s]: !show[s] })}>
            ${s}: ${data.counts[s] || 0}
          </span>
        `)}
        <button class="ghost" onClick=${() => { setData(null); api.post("/api/validate").then(setData); }}>Re-run</button>
      </div>
      ${visible.map((f, i) => html`<${FindingRow} key=${i} f=${f} onOpenFile=${onOpenFile} />`)}
      ${visible.length === 0 && html`<div class="empty">Nothing at the selected severities.</div>`}
    </div>
  `;
}

/* ── TrackerPanel — the iterative-draft-finalization queue ───────────────── */

const STATUS_META = {
  complete: { icon: "✅", label: "complete" },
  undesigned: { icon: "🔴", label: "undesigned" },
  blocked: { icon: "⛔", label: "blocked" },
  "listed-elsewhere": { icon: "📘", label: "race-locked" },
  unknown: { icon: "❔", label: "unknown" },
};

export function TrackerPanel({ api, onOpenFile }) {
  const [data, setData] = useState(null);
  const [show, setShow] = useState({ complete: true, undesigned: true, blocked: true, "listed-elsewhere": true, unknown: true });
  const [expanded, setExpanded] = useState(null);

  useEffect(() => { api.get("/api/tracker").then(setData); }, []);

  if (!data) return html`<div class="empty">Building tracker…</div>`;

  const visible = data.classes.filter((c) => show[c.designStatus]);
  const tiers = [...new Set(visible.map((c) => c.tier))];
  const reworkCount = data.classes.filter((c) => c.rework).length;

  return html`
    <div>
      <div class="counts">
        ${Object.entries(STATUS_META).map(([s, meta]) => (data.counts[s] || 0) === 0 ? null : html`
          <span key=${s} class=${"count-chip" + (show[s] ? "" : " off")}
                onClick=${() => setShow({ ...show, [s]: !show[s] })}>
            ${meta.icon} ${meta.label}: ${data.counts[s] || 0}
          </span>
        `)}
        ${reworkCount > 0 && html`<span class="count-chip" style=${{ cursor: "default" }}>⚠️ rework-flagged: ${reworkCount}</span>`}
      </div>

      ${tiers.map((tier) => html`
        <div key=${tier}>
          <div class="section-title">${tier}</div>
          ${visible.filter((c) => c.tier === tier).map((c) => {
            const meta = STATUS_META[c.designStatus] || STATUS_META.unknown;
            const pct = c.abilities.total ? Math.round((c.abilities.finalized / c.abilities.total) * 100) : 0;
            const isOpen = expanded === c.name;
            return html`
              <div key=${c.name} class="tracker-row" onClick=${() => setExpanded(isOpen ? null : c.name)}>
                <div class="tracker-main">
                  <span class="tracker-icon">${meta.icon}${c.rework ? "⚠️" : ""}</span>
                  <span class="tracker-name">${c.name}</span>
                  <span class="tracker-meta">${c.role || ""}</span>
                  ${c.abilities.total > 0 && html`
                    <span class="tracker-abilities">
                      <span class="prog-bar"><span class="prog-fill" style=${{ width: pct + "%" }}></span></span>
                      ${c.abilities.finalized}/${c.abilities.total} finalized
                    </span>
                  `}
                </div>
                ${isOpen && html`
                  <div class="tracker-detail" onClick=${(e) => e.stopPropagation()}>
                    ${c.race && html`<div><span class="detail-label">Race:</span> ${c.race}</div>`}
                    <div><span class="detail-label">Status:</span> ${c.statusText}</div>
                    ${c.qualContext && html`<div class="qual-context"><span class="detail-label">Qual context:</span> ${c.qualContext}</div>`}
                    ${c.skillFiles.length > 0 && html`
                      <div><span class="detail-label">Skill files:</span>
                        ${c.skillFiles.map((f) => html`
                          <span key=${f} class="file-ref" style=${{ cursor: "pointer", marginRight: "10px" }}
                                onClick=${() => onOpenFile(f)}>${f}</span>
                        `)}
                      </div>
                    `}
                  </div>
                `}
              </div>
            `;
          })}
        </div>
      `)}
    </div>
  `;
}

/* ── GraphView (dependency-free force layout) ────────────────────────────── */

const PALETTE = ["#4da3ff", "#4dd0b1", "#ffb347", "#ff6b9d", "#b39dff", "#8fd14d", "#ff8a5c", "#5cd6ff"];

export function GraphView({ api }) {
  const [graph, setGraph] = useState(null);

  useEffect(() => {
    api.get("/api/graph").then((g) => {
      const W = 1200, H = 800;
      const nodes = g.nodes.map((n, i) => ({
        ...n,
        x: W / 2 + Math.cos((i / g.nodes.length) * 2 * Math.PI) * 300,
        y: H / 2 + Math.sin((i / g.nodes.length) * 2 * Math.PI) * 300,
      }));
      const byId = Object.fromEntries(nodes.map((n) => [n.id, n]));
      const edges = g.edges.filter((e) => byId[e.from] && byId[e.to]);
      for (let it = 0; it < 260; it++) {
        for (const a of nodes) {
          let fx = (W / 2 - a.x) * 0.002, fy = (H / 2 - a.y) * 0.002;
          for (const b of nodes) {
            if (a === b) continue;
            const dx = a.x - b.x, dy = a.y - b.y;
            const d2 = Math.max(dx * dx + dy * dy, 40);
            fx += (dx / d2) * 900; fy += (dy / d2) * 900;
          }
          a.x += fx; a.y += fy;
        }
        for (const e of edges) {
          const a = byId[e.from], b = byId[e.to];
          const dx = b.x - a.x, dy = b.y - a.y;
          a.x += dx * 0.02; a.y += dy * 0.02;
          b.x -= dx * 0.02; b.y -= dy * 0.02;
        }
      }
      const cats = [...new Set(nodes.map((n) => n.category))];
      setGraph({ nodes, edges, byId, cats, W, H });
    });
  }, []);

  if (!graph) return html`<div class="empty">Loading graph…</div>`;

  const color = (cat) => PALETTE[graph.cats.indexOf(cat) % PALETTE.length];
  return html`
    <div>
      <div class="legend">
        ${graph.cats.map((c) => html`
          <span key=${c}><span class="swatch" style=${{ background: color(c) }}></span>${c}</span>
        `)}
      </div>
      <div class="graph-wrap">
        <svg viewBox=${`0 0 ${graph.W} ${graph.H}`}>
          ${graph.edges.map((e, i) => {
            const a = graph.byId[e.from], b = graph.byId[e.to];
            return html`<line key=${i} x1=${a.x} y1=${a.y} x2=${b.x} y2=${b.y}
                              stroke="#3a4152" stroke-width="1.2"><title>${e.kind}</title></line>`;
          })}
          ${graph.nodes.map((n) => html`
            <g key=${n.id}>
              <circle cx=${n.x} cy=${n.y} r="7" fill=${color(n.category)} opacity="0.9">
                <title>${n.id} (${n.category})</title>
              </circle>
              <text class="graph-node-label" x=${n.x + 10} y=${n.y + 3}>${n.id.split(".").pop()}</text>
            </g>
          `)}
        </svg>
      </div>
    </div>
  `;
}
