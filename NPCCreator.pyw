import tkinter as tk
from tkinter import messagebox, ttk
import yaml, os

MERC_RANK1_TEMPLATE = (
    '- Condition: "TargetInRange"\n'
    '  Action: "Skill.Combat.YourSkill"\n'
    '  CastTime: 2.5\n'
)
OPTIONAL_TIER_HINT = "# Optional. Leave empty to inherit the tier below.\n"
DOCTRINE_TIER_HINT = (
    "# Optional. Leave empty to inherit the tier below. Example:\n"
    "# Inherit: Level1\n"
    "# KitOptions: [Skill.Combat.X.Instant]\n"
    "# KnowledgeChecks:\n"
    "#   - Mechanic: Mechanic.X\n"
    "#     LoreSource: Lore.Bestiary.X\n"
)

class NPCCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AAA NPC Architect: RankProfile Suite")
        self.root.geometry("680x1000")

        # --- Engagement Profile ---
        profile_frame = tk.LabelFrame(root, text="Engagement Profile (Failure Logic)")
        profile_frame.pack(fill="x", padx=10, pady=5)

        self.telegraphed = tk.BooleanVar(value=True)
        self.interactive = tk.BooleanVar(value=True)

        tk.Checkbutton(profile_frame, text="Telegraphed (Casual Friendly)", variable=self.telegraphed).pack(side="left", padx=5)
        tk.Checkbutton(profile_frame, text="Interactive (Veteran Opportunities)", variable=self.interactive).pack(side="left", padx=5)

        tk.Label(profile_frame, text="Failure Severity:").pack(side="left", padx=5)
        self.severity_cb = ttk.Combobox(profile_frame, values=["None", "Player Death (Respawn)", "Full Encounter Reset"], state="readonly")
        self.severity_cb.current(0)
        self.severity_cb.pack(side="left", padx=5)

        # --- Base Data ---
        tk.Label(root, text="NPC Name:").pack(); self.name_entry = tk.Entry(root, width=40); self.name_entry.pack()
        tk.Label(root, text="Intent:").pack(); self.intent_entry = tk.Entry(root, width=50); self.intent_entry.pack()

        tk.Label(root, text="Character Template (optional — leave blank for a flat NPC):").pack()
        self.template_cb = ttk.Combobox(root, values=[""] + self.get_list("Characters"), state="readonly", width=47)
        self.template_cb.current(0)
        self.template_cb.pack()

        tk.Label(root, text="Party Rank Resolution:").pack()
        self.party_res_cb = ttk.Combobox(root, values=["Lowest", "Average", "Highest"], state="readonly")
        self.party_res_cb.current(0)
        self.party_res_cb.pack()

        # --- Pillar Tabs ---
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # 1. Adventurer Pillar
        self.tab_adv = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_adv, text="Adventurer (Loot)")
        tk.Label(self.tab_adv, text="Loot Curve / Table Ref (e.g. Global.LootScaling.CurveA):").pack()
        self.loot_entry = tk.Entry(self.tab_adv, width=50); self.loot_entry.pack()
        tk.Label(self.tab_adv, text="Progression Tier (1-5):").pack(); self.tier_spin = tk.Spinbox(self.tab_adv, from_=1, to=5); self.tier_spin.pack()

        # 2. Mercenary Pillar (tiered reactions, Rank1 required)
        self.tab_merc = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_merc, text="Mercenary (Counter-play)")
        tk.Label(self.tab_merc, text="Rank 1 Reactions (REQUIRED — YAML list of Condition/Action/CastTime):").pack()
        self.merc_r1_text = tk.Text(self.tab_merc, height=5, width=70)
        self.merc_r1_text.insert(tk.END, MERC_RANK1_TEMPLATE)
        self.merc_r1_text.pack()
        tk.Label(self.tab_merc, text="Rank 2 Reactions:").pack()
        self.merc_r2_text = tk.Text(self.tab_merc, height=4, width=70)
        self.merc_r2_text.insert(tk.END, OPTIONAL_TIER_HINT)
        self.merc_r2_text.pack()
        tk.Label(self.tab_merc, text="Rank 3 Reactions:").pack()
        self.merc_r3_text = tk.Text(self.tab_merc, height=4, width=70)
        self.merc_r3_text.insert(tk.END, OPTIONAL_TIER_HINT)
        self.merc_r3_text.pack()

        # 3. Doctrine Pillar (enemy-side Strategy)
        self.tab_doc = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_doc, text="Doctrine (AI Tiers)")
        tk.Label(self.tab_doc, text="Level 1 (REQUIRED — fully telegraphed default pattern)").pack()
        tk.Label(self.tab_doc, text="Nav/Terrain Profile:").pack(); self.doc_profile_entry = tk.Entry(self.tab_doc, width=50); self.doc_profile_entry.pack()
        tk.Label(self.tab_doc, text="Behavior:").pack(); self.doc_behavior_entry = tk.Entry(self.tab_doc, width=50); self.doc_behavior_entry.pack()
        tk.Label(self.tab_doc, text="Aggro Radius:").pack(); self.doc_aggro_entry = tk.Entry(self.tab_doc, width=15); self.doc_aggro_entry.insert(0, "800"); self.doc_aggro_entry.pack()
        tk.Label(self.tab_doc, text="Leash Radius:").pack(); self.doc_leash_entry = tk.Entry(self.tab_doc, width=15); self.doc_leash_entry.insert(0, "2500"); self.doc_leash_entry.pack()
        tk.Label(self.tab_doc, text="Reset Behavior:").pack(); self.doc_reset_entry = tk.Entry(self.tab_doc, width=30); self.doc_reset_entry.insert(0, "HealAndReturn"); self.doc_reset_entry.pack()
        tk.Label(self.tab_doc, text="Level 2 (YAML mapping):").pack()
        self.doc_l2_text = tk.Text(self.tab_doc, height=4, width=70)
        self.doc_l2_text.insert(tk.END, DOCTRINE_TIER_HINT)
        self.doc_l2_text.pack()
        tk.Label(self.tab_doc, text="Level 3 (YAML mapping):").pack()
        self.doc_l3_text = tk.Text(self.tab_doc, height=4, width=70)
        self.doc_l3_text.insert(tk.END, DOCTRINE_TIER_HINT)
        self.doc_l3_text.pack()

        tk.Button(root, text="Save NPC Specification", command=self.save_yaml, bg="#2c3e50", fg="white", height=2).pack(fill="x", padx=10, pady=10)

    def get_list(self, folder):
        if not os.path.exists(folder): return []
        return sorted(f.replace('.yaml', '').replace('.yml', '') for f in os.listdir(folder) if f.endswith(('.yaml', '.yml')))

    def parse_tier(self, text_widget, label):
        """Parses an optional tier box; returns None when empty/comments-only."""
        raw = text_widget.get("1.0", "end-1c")
        try:
            parsed = yaml.safe_load(raw)
        except yaml.YAMLError as e:
            raise ValueError(f"{label} is not valid YAML: {e}")
        return parsed or None

    def save_yaml(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "NPC Name is required.")
            return

        try:
            merc_r1 = self.parse_tier(self.merc_r1_text, "Mercenary Rank 1")
            merc_r2 = self.parse_tier(self.merc_r2_text, "Mercenary Rank 2")
            merc_r3 = self.parse_tier(self.merc_r3_text, "Mercenary Rank 3")
            doc_l2 = self.parse_tier(self.doc_l2_text, "Doctrine Level 2")
            doc_l3 = self.parse_tier(self.doc_l3_text, "Doctrine Level 3")
        except ValueError as e:
            messagebox.showerror("YAML Error", str(e))
            return

        if not merc_r1:
            messagebox.showerror("Error", "Mercenary Rank 1 is required — it is the default pattern every player can meet.")
            return
        if not self.doc_profile_entry.get().strip():
            messagebox.showerror("Error", "Doctrine Level 1 Nav/Terrain Profile is required.")
            return

        mercenary = {'Rank1': merc_r1}
        if merc_r2: mercenary['Rank2'] = merc_r2
        if merc_r3: mercenary['Rank3'] = merc_r3

        level1 = {
            'Profile': self.doc_profile_entry.get().strip(),
            'AggroRadius': int(self.doc_aggro_entry.get() or 0),
            'LeashRadius': int(self.doc_leash_entry.get() or 0),
            'ResetBehavior': self.doc_reset_entry.get().strip()
        }
        if self.doc_behavior_entry.get().strip():
            level1['Behavior'] = self.doc_behavior_entry.get().strip()

        doctrine = {'Level1': level1}
        if doc_l2: doctrine['Level2'] = doc_l2
        if doc_l3: doctrine['Level3'] = doc_l3

        data = {
            'Identity': {
                'Name': name,
                'Intent': self.intent_entry.get(),
                'TemplateRef': self.template_cb.get() or None
            },
            'EngagementProfile': {
                'Telegraphed': self.telegraphed.get(),
                'Interactive': self.interactive.get(),
                'FailureSeverity': self.severity_cb.get()
            },
            'RankProfile': {
                'PartyResolution': self.party_res_cb.get(),
                'Adventurer': {
                    'LootCurve': self.loot_entry.get(),
                    'Tier': int(self.tier_spin.get())
                },
                'Mercenary': mercenary,
                'Doctrine': doctrine
            }
        }

        filename = name.replace(" ", "_") or "NewNPC"
        if not os.path.exists("NPCs"): os.makedirs("NPCs")
        with open(f"NPCs/{filename}.yaml", 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        messagebox.showinfo("Success", f"NPC {filename} saved with RankProfile ({len(mercenary)} Mercenary tier(s), {len(doctrine)} Doctrine tier(s)).")

if __name__ == "__main__":
    root = tk.Tk()
    app = NPCCreatorApp(root)
    root.mainloop()
