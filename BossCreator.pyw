import tkinter as tk
from tkinter import messagebox, ttk
import yaml, os

class BossCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Boss Encounter Architecture")
        self.root.geometry("550x850")

        tk.Label(root, text="Boss Name:").pack(pady=2)
        self.name_entry = tk.Entry(root, width=50); self.name_entry.pack()

        # --- Identity Links (so the boss resolves to real character/skill/loot data) ---
        link_frame = tk.LabelFrame(root, text="Identity & Data Links")
        link_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(link_frame, text="Character Template (optional — leave blank for a flat boss):").pack()
        self.template_cb = ttk.Combobox(link_frame, values=[""] + self.get_list("Characters"), state="readonly", width=45)
        self.template_cb.current(0)
        self.template_cb.pack()

        tk.Label(link_frame, text="Assigned Skills:").pack()
        self.skills_listbox = tk.Listbox(link_frame, selectmode=tk.MULTIPLE, height=5, width=48, exportselection=False)
        for skill in self.get_list("Skills"):
            self.skills_listbox.insert(tk.END, skill)
        self.skills_listbox.pack()

        tk.Label(link_frame, text="Loot Table:").pack()
        self.loot_cb = ttk.Combobox(link_frame, values=["None"] + self.get_list("Loot"), state="readonly", width=45)
        self.loot_cb.current(0)
        self.loot_cb.pack()

        # --- Health vs DPS Timeline Expectations ---
        time_frame = tk.LabelFrame(root, text="Encounter Math (FF14 Style DPS vs Health)")
        time_frame.pack(fill="x", padx=10, pady=10)
        tk.Label(time_frame, text="Expected Encounter Duration (Minutes):").pack()
        self.dur_entry = tk.Entry(time_frame, width=15); self.dur_entry.insert(0, "5.0"); self.dur_entry.pack()
        tk.Label(time_frame, text="Target Base Health (Placeholder):").pack()
        self.hp_entry = tk.Entry(time_frame, width=15); self.hp_entry.insert(0, "100000"); self.hp_entry.pack()

        # --- Triggers ---
        phase_frame = tk.LabelFrame(root, text="Phase Triggers")
        phase_frame.pack(fill="x", padx=10, pady=10)
        tk.Label(phase_frame, text="Phase 2 Condition Trigger (Name/Key):").pack()
        self.p2_entry = tk.Entry(phase_frame, width=40); self.p2_entry.pack()
        tk.Label(phase_frame, text="Phase 3 Condition Trigger (Name/Key):").pack()
        self.p3_entry = tk.Entry(phase_frame, width=40); self.p3_entry.pack()

        # --- Mercenary & Animation Scaling ---
        merc_frame = tk.LabelFrame(root, text="Mechanic Scaling")
        merc_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(merc_frame, text="VFX/Anim Tier (1-3):").pack()
        self.tier_spin = tk.Spinbox(merc_frame, from_=1, to=3, width=10); self.tier_spin.pack()

        tk.Label(merc_frame, text="Rank 1 Macro Mechanic Name:").pack()
        self.r1_entry = tk.Entry(merc_frame, width=40); self.r1_entry.pack()
        
        tk.Label(merc_frame, text="Rank 2+ Micro-Punish Logic (Before Macro):").pack()
        self.r2_text = tk.Text(merc_frame, height=3, width=40); self.r2_text.pack()

        tk.Button(root, text="Save Boss Architecture", command=self.save_yaml, height=2, width=30, bg="#c0392b", fg="white").pack(pady=20)

    def get_list(self, folder):
        if not os.path.exists(folder): return []
        return sorted(f.replace('.yaml', '').replace('.yml', '') for f in os.listdir(folder) if f.endswith(('.yaml', '.yml')))

    def save_yaml(self):
        name = self.name_entry.get().strip()
        if not name: return messagebox.showerror("Error", "Name required.")

        data = {
            'Identity': {
                'Key': f"NPC.Boss.{name.replace(' ', '.')}",
                'Name': name,
                'TemplateRef': self.template_cb.get() or None
            },
            'AssignedSkills': [self.skills_listbox.get(i) for i in self.skills_listbox.curselection()],
            'LootTable': self.loot_cb.get() if self.loot_cb.get() != "None" else None,
            'EncounterMath': {
                'ExpectedDurationMinutes': float(self.dur_entry.get()),
                'BaseHealthPlaceholder': int(self.hp_entry.get())
            },
            'PhaseLogic': {
                'Phase2Trigger': self.p2_entry.get(),
                'Phase3Trigger': self.p3_entry.get()
            },
            'MechanicScaling': {
                'AnimTier': int(self.tier_spin.get()),
                'Rank1_MacroMechanic': self.r1_entry.get(),
                'Rank2_MicroPunish': self.r2_text.get("1.0", "end-1c").strip()
            }
        }
        
        if not os.path.exists("NPCs/Bosses"): os.makedirs("NPCs/Bosses")
        with open(f"NPCs/Bosses/{name.replace(' ', '_')}.yaml", 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        messagebox.showinfo("Success", "Boss Saved.")

if __name__ == "__main__":
    root = tk.Tk()
    BossCreatorApp(root)
    root.mainloop()