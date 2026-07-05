import tkinter as tk
from tkinter import messagebox, ttk
import yaml, os

class NPCCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AAA NPC Architect: Lethality & Pillar Suite")
        self.root.geometry("650x850")

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

        # --- Pillar Tabs ---
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # 1. Adventurer Pillar
        self.tab_adv = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_adv, text="Adventurer (Loot)")
        tk.Label(self.tab_adv, text="Loot Table ID:").pack(); self.loot_entry = tk.Entry(self.tab_adv); self.loot_entry.pack()
        tk.Label(self.tab_adv, text="Progression Tier (1-5):").pack(); self.tier_spin = tk.Spinbox(self.tab_adv, from_=1, to=5); self.tier_spin.pack()

        # 2. Mercenary Pillar
        self.tab_merc = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_merc, text="Mercenary (Counter-play)")
        tk.Label(self.tab_merc, text="Commitment Level (1-3):").pack()
        self.commit_spin = tk.Spinbox(self.tab_merc, from_=1, to=3); self.commit_spin.pack()
        tk.Label(self.tab_merc, text="Interrupt Window (sec):").pack(); self.int_win_entry = tk.Entry(self.tab_merc); self.int_win_entry.pack()
        tk.Label(self.tab_merc, text="Scramble Tax (Description):").pack(); self.scramble_entry = tk.Entry(self.tab_merc, width=60); self.scramble_entry.pack()

        # 3. Strategy Pillar
        self.tab_strat = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_strat, text="Strategy (Tactics)")
        tk.Label(self.tab_strat, text="Formation Plan:").pack(); self.plan_entry = tk.Entry(self.tab_strat, width=50); self.plan_entry.pack()
        tk.Label(self.tab_strat, text="Environmental/Status Effects:").pack(); self.status_entry = tk.Entry(self.tab_strat, width=50); self.status_entry.pack()
        self.retreat_var = tk.BooleanVar()
        tk.Checkbutton(self.tab_strat, text="Allows Retreat/Invuln Cycles", variable=self.retreat_var).pack()

        tk.Button(root, text="Save NPC Specification", command=self.save_yaml, bg="#2c3e50", fg="white", height=2).pack(fill="x", padx=10, pady=10)

    def get_list(self, folder):
        if not os.path.exists(folder): return []
        return [f.replace('.yaml', '') for f in os.listdir(folder)]

    def save_yaml(self):
        data = {
            'Identity': {
                'Name': self.name_entry.get(),
                'Intent': self.intent_entry.get(),
                'TemplateRef': self.template_cb.get() or None
            },
            'EngagementProfile': {
                'Telegraphed': self.telegraphed.get(),
                'Interactive': self.interactive.get(),
                'FailureSeverity': self.severity_cb.get() # Now captures your design nuance
            },
            'AdventurerPillar': {'LootTable': self.loot_entry.get(), 'Tier': int(self.tier_spin.get())},
            'MercenaryPillar': {
                'CommitmentLevel': int(self.commit_spin.get()),
                'InterruptWindow': self.int_win_entry.get(),
                'ScrambleTax': self.scramble_entry.get()
            },
            'StrategyPillar': {
                'Formation': self.plan_entry.get(),
                'Status': self.status_entry.get().split(','),
                'SupportsRetreat': self.retreat_var.get()
            }
        }
        name = self.name_entry.get().replace(" ", "_") or "NewNPC"
        if not os.path.exists("NPCs"): os.makedirs("NPCs")
        with open(f"NPCs/{name}.yaml", 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        messagebox.showinfo("Success", f"NPC {name} serialized with {self.severity_cb.get()} severity.")

if __name__ == "__main__":
    root = tk.Tk()
    app = NPCCreatorApp(root)
    root.mainloop()