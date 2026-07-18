import React, { useState, useEffect, useCallback } from "react";
import { createRoot } from "react-dom/client";
import htm from "htm";
import { FileBrowser, AbilityFileEditor, RawEditor, ValidationPanel, GraphView, TrackerPanel } from "./components.js?v=2";

const html = htm.bind(React.createElement);

export const api = {
  get: (p) => fetch(p).then((r) => { if (!r.ok) throw new Error(r.statusText); return r.json(); }),
  put: (p, body) => fetch(p, { method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }).then((r) => { if (!r.ok) throw new Error(r.statusText); return r.json(); }),
  post: (p, body) => fetch(p, { method: "POST", headers: { "Content-Type": "application/json" }, body: body === undefined ? undefined : JSON.stringify(body) }).then((r) => { if (!r.ok) throw new Error(r.statusText); return r.json(); }),
};

const isSkillFile = (path) =>
  path.endsWith(".yaml") && (path.startsWith("Skills/") || /_Skills[^/]*\.yaml$/.test(path));

function App() {
  const [tab, setTab] = useState("editor");
  const [files, setFiles] = useState([]);
  const [current, setCurrent] = useState(null);   // {path, raw, parsed, abilities?}
  const [schema, setSchema] = useState(null);
  const [rawMode, setRawMode] = useState(false);

  useEffect(() => {
    api.get("/api/files").then((d) => setFiles(d.files));
    api.get("/api/schema/skill").then(setSchema);
  }, []);

  const openFile = useCallback((path) => {
    setRawMode(false);
    const wants = isSkillFile(path)
      ? Promise.all([api.get(`/api/file/${path}`), api.get(`/api/abilities/${path}`)])
          .then(([f, a]) => ({ path, ...f, abilities: a.abilities }))
      : api.get(`/api/file/${path}`).then((f) => ({ path, ...f }));
    wants.then(setCurrent);
    setTab("editor");
  }, []);

  const reload = useCallback(() => current && openFile(current.path), [current, openFile]);

  const abilityView = current && current.abilities && current.abilities.length > 0 && !rawMode;

  return html`
    <div class="topbar">
      <h1>Juice Design Hub</h1>
      <div class="tabs">
        <button class=${"tab" + (tab === "editor" ? " active" : "")} onClick=${() => setTab("editor")}>Editor</button>
        <button class=${"tab" + (tab === "tracker" ? " active" : "")} onClick=${() => setTab("tracker")}>Tracker</button>
        <button class=${"tab" + (tab === "validation" ? " active" : "")} onClick=${() => setTab("validation")}>Validation</button>
        <button class=${"tab" + (tab === "graph" ? " active" : "")} onClick=${() => setTab("graph")}>Graph</button>
      </div>
      ${tab === "editor" && current && current.abilities && current.abilities.length > 0 && html`
        <button class="ghost" onClick=${() => setRawMode(!rawMode)}>
          ${rawMode ? "Form mode" : "Raw mode"}
        </button>
      `}
    </div>
    <div class="layout">
      <${FileBrowser} files=${files} current=${current?.path} onOpen=${openFile} />
      <div class="main">
        ${tab === "editor" && (
          !current
            ? html`<div class="empty">Pick a file from the sidebar.<br/>Skill files open in the methodology editor; everything else opens raw.</div>`
            : abilityView && schema
              ? html`<${AbilityFileEditor} key=${current.path} file=${current} schema=${schema} api=${api} onSaved=${reload} />`
              : html`<${RawEditor} key=${current.path + (rawMode ? ":raw" : "")} file=${current} api=${api} />`
        )}
        ${tab === "tracker" && html`<${TrackerPanel} api=${api} onOpenFile=${openFile} />`}
        ${tab === "validation" && html`<${ValidationPanel} api=${api} onOpenFile=${openFile} />`}
        ${tab === "graph" && html`<${GraphView} api=${api} />`}
      </div>
    </div>
  `;
}

createRoot(document.getElementById("root")).render(html`<${App} />`);
