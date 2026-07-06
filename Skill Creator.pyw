import tkinter as tk
from tkinter import ttk, messagebox
import yaml, os
from tag_library import add_to_tag_library, TagSelectorModal

class SkillCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Skill Creator: GameplayAbility Suite")
        self.root.geometry("560x1050")

        # --- Identity ---
        tk.Label(root, text="Skill Name (Key becomes Skill.Combat.<Name>):").pack(pady=2)
        self.name_entry = tk.Entry(root, width=45)
        self.name_entry.pack()
        self.name_entry.bind("<FocusOut>", self.auto_generate_tags)

        tk.Label(root, text="Intent:").pack()
        self.intent_entry = tk.Entry(root, width=50); self.intent_entry.pack()

        tk.Label(root, text="Action Type (FFXIV recast model):").pack()
        self.action_type_cb = ttk.Combobox(root, values=["Weaponskill", "Spell", "Ability"], state="readonly")
        self.action_type_cb.current(0)
        self.action_type_cb.pack()

        self.move_cast_var = tk.BooleanVar(value=False)
        tk.Checkbutton(root, text="Can Cast While Moving", variable=self.move_cast_var).pack()

        # --- Tabs ---
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        tab_mech = ttk.Frame(self.notebook); self.notebook.add(tab_mech, text="Mechanics")
        tab_combo = ttk.Frame(self.notebook); self.notebook.add(tab_combo, text="Combo & Statuses")
        tab_restrict = ttk.Frame(self.notebook); self.notebook.add(tab_restrict, text="Classes & Assets")

        # --- Mechanics Tab ---
        tk.Label(tab_mech, text="Targeting Type:").pack()
        self.target_cb = ttk.Combobox(tab_mech, values=["Target", "Self", "Area_Circle", "Area_Cone"], state="readonly")
        self.target_cb.pack()

        tk.Label(tab_mech, text="Potency:").pack()
        self.potency_spin = tk.Spinbox(tab_mech, from_=0, to=5000, increment=5); self.potency_spin.pack()

        tk.Label(tab_mech, text="Range:").pack()
        self.range_spin = tk.Spinbox(tab_mech, from_=0, to=500, increment=5); self.range_spin.pack()

        tk.Label(tab_mech, text="Cast Time (s):").pack()
        self.cast_spin = tk.Spinbox(tab_mech, from_=0, to=10, increment=0.1); self.cast_spin.pack()

        tk.Label(tab_mech, text="Recast Time (s, cooldown):").pack()
        self.recast_spin = tk.Spinbox(tab_mech, from_=0, to=300, increment=0.5); self.recast_spin.pack()

        tk.Label(tab_mech, text="Max Charges:").pack()
        self.charges_spin = tk.Spinbox(tab_mech, from_=1, to=5); self.charges_spin.pack()

        tk.Label(tab_mech, text="Resource Type:").pack()
        self.resource_cb = ttk.Combobox(tab_mech, values=["None", "MagicCapacity", "Gauge", "HP"], state="readonly")
        self.resource_cb.current(0)
        self.resource_cb.pack()

        tk.Label(tab_mech, text="Resource Cost:").pack()
        self.cost_spin = tk.Spinbox(tab_mech, from_=0, to=10000, increment=1); self.cost_spin.pack()

        # --- Combo & Statuses Tab ---
        tk.Label(tab_combo, text="Combo From (previous skill in chain):").pack()
        self.combo_cb = ttk.Combobox(tab_combo, values=["None"] + self.get_skill_keys(), state="readonly", width=45)
        self.combo_cb.current(0)
        self.combo_cb.pack()

        tk.Label(tab_combo, text="Combo Window (s):").pack()
        self.combo_window_spin = tk.Spinbox(tab_combo, from_=0, to=60, increment=1)
        self.combo_window_spin.delete(0, "end"); self.combo_window_spin.insert(0, "30")
        self.combo_window_spin.pack()

        tk.Label(tab_combo, text="Combo Potency (replaces Potency when comboed):").pack()
        self.combo_potency_spin = tk.Spinbox(tab_combo, from_=0, to=5000, increment=5); self.combo_potency_spin.pack()

        tk.Label(tab_combo, text="Applies Statuses (from Passives/):").pack()
        self.status_listbox = tk.Listbox(tab_combo, selectmode=tk.MULTIPLE, height=6, width=45, exportselection=False)
        for status in self.get_list("Passives"):
            self.status_listbox.insert(tk.END, status)
        self.status_listbox.pack()

        # --- Classes & Assets Tab ---
        tk.Label(tab_restrict, text="Class Restrictions (empty = usable by all):").pack()
        self.class_listbox = tk.Listbox(tab_restrict, selectmode=tk.MULTIPLE, height=8, width=45, exportselection=False)
        for cls in self.get_class_options():
            self.class_listbox.insert(tk.END, cls)
        self.class_listbox.pack()

        tk.Label(tab_restrict, text="Animation Path:").pack()
        self.anim_entry = tk.Entry(tab_restrict, width=45); self.anim_entry.pack()
        tk.Label(tab_restrict, text="VFX Path:").pack()
        self.vfx_entry = tk.Entry(tab_restrict, width=45); self.vfx_entry.pack()

        # --- Tag Management ---
        tag_frame = tk.LabelFrame(root, text="Skill Tags")
        tag_frame.pack(fill="x", padx=10, pady=5)
        self.tag_entry = tk.Entry(tag_frame, width=40); self.tag_entry.pack()
        btn_frame = tk.Frame(tag_frame); btn_frame.pack()
        tk.Button(btn_frame, text="Add Tag", command=self.add_tag).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Tag List", command=self.open_tag_modal).pack(side="left", padx=2)
        self.tags_listbox = tk.Listbox(tag_frame, height=4, width=40, exportselection=False)
        self.tags_listbox.pack()
        tk.Button(tag_frame, text="Remove Selected", command=self.remove_tag).pack()

        tk.Button(root, text="Save Skill", command=self.save_yaml, height=2, width=20, bg="#2c3e50", fg="white").pack(pady=15)

    def get_list(self, folder):
        if not os.path.exists(folder): return []
        return sorted(f.replace('.yaml', '').replace('.yml', '') for f in os.listdir(folder) if f.endswith(('.yaml', '.yml')))

    def get_skill_keys(self):
        folder = "Skills"
        if not os.path.exists(folder): return []
        keys = []
        for fname in os.listdir(folder):
            if not fname.endswith(('.yaml', '.yml')): continue
            try:
                with open(os.path.join(folder, fname)) as f:
                    data = yaml.safe_load(f) or {}
                keys.append(data.get('Key', fname.rsplit('.', 1)[0]))
            except Exception:
                keys.append(fname.rsplit('.', 1)[0])
        return sorted(keys)

    def get_class_options(self):
        lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Classes", "Class_Library.yaml")
        try:
            with open(lib_path, 'r') as f:
                data = yaml.safe_load(f)
                all_classes = []
                for tier in data.values(): all_classes.extend(tier)
                return all_classes
        except Exception:
            return []

    def auto_generate_tags(self, event=None):
        name = self.name_entry.get().strip()
        if name:
            suggestion = f"Skill.Combat.{name.replace(' ', '.')}"
            if suggestion not in list(self.tags_listbox.get(0, tk.END)):
                self.tags_listbox.insert(tk.END, suggestion)
                add_to_tag_library(suggestion)

    def add_tag(self):
        tag = self.tag_entry.get().strip()
        if tag:
            self.tags_listbox.insert(tk.END, tag)
            add_to_tag_library(tag)
            self.tag_entry.delete(0, tk.END)

    def open_tag_modal(self):
        TagSelectorModal(self.root, self.add_tags_from_modal)

    def add_tags_from_modal(self, tags):
        for tag in tags:
            if tag not in list(self.tags_listbox.get(0, tk.END)):
                self.tags_listbox.insert(tk.END, tag)

    def remove_tag(self):
        selection = self.tags_listbox.curselection()
        if selection: self.tags_listbox.delete(selection)

    def save_yaml(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Name required.")
            return

        action_type = self.action_type_cb.get()
        combo_from = self.combo_cb.get()

        data = {
            'Key': f"Skill.Combat.{name.replace(' ', '.')}",
            'Name': name,
            'Intent': self.intent_entry.get(),
            'ActionType': action_type,
            'Tags': list(self.tags_listbox.get(0, tk.END)),
            'BaseState': {
                'Animation': self.anim_entry.get(),
                'VFX': self.vfx_entry.get(),
                'IsOGCD': action_type == "Ability",
                'CanCastWhileMoving': self.move_cast_var.get()
            },
            'Mechanics': {
                'Targeting': self.target_cb.get(),
                'Potency': float(self.potency_spin.get()),
                'Range': float(self.range_spin.get()),
                'CastTime': float(self.cast_spin.get()),
                'RecastTime': float(self.recast_spin.get()),
                'MaxCharges': int(self.charges_spin.get())
            },
            'Resource': {
                'Type': self.resource_cb.get(),
                'Cost': int(self.cost_spin.get())
            },
            'Combo': {
                'ComboFrom': combo_from,
                'WindowSeconds': float(self.combo_window_spin.get()),
                'ComboPotency': float(self.combo_potency_spin.get())
            } if combo_from != "None" else None,
            'AppliesStatuses': [self.status_listbox.get(i) for i in self.status_listbox.curselection()],
            'ClassRestrictions': [self.class_listbox.get(i) for i in self.class_listbox.curselection()]
        }

        if not os.path.exists("Skills"): os.makedirs("Skills")
        with open(f"Skills/{name.replace(' ', '_')}.yaml", 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        messagebox.showinfo("Success", f"Skill '{name}' registered.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SkillCreatorApp(root)
    root.mainloop()
