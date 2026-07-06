# --- AUTO-INJECTED CONFIG ---
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "Attributes"))
from attr_loader import get_full_attribute_data
# ----------------------------

import tkinter as tk
from tkinter import messagebox, ttk
import yaml

from tag_library import add_to_tag_library, TagSelectorModal


class CharacterCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Character Creation Template")
        self.root.geometry("600x1050")

        self.schema, _ = get_full_attribute_data(__file__)

        # --- Race / Class / Main Attribute ---
        tk.Label(root, text="Race:").pack()
        self.race_cb = ttk.Combobox(root, values=self.get_race_options(), width=45, state="readonly")
        self.race_cb.pack()

        tk.Label(root, text="Class:").pack()
        self.class_cb = ttk.Combobox(root, values=self.get_class_options(), width=45, state="readonly")
        self.class_cb.pack()

        tk.Label(root, text="Main Attribute:").pack()
        self.attr_cb = ttk.Combobox(root, values=list(self.schema.keys()), width=45, state="readonly")
        self.attr_cb.pack()

        tk.Label(root, text="Role:").pack()
        self.role_entry = tk.Entry(root, width=50); self.role_entry.pack()

        # --- Cosmetic ---
        tk.Label(root, text="--- Cosmetic ---", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        tk.Label(root, text="Gender:").pack()
        self.gender_entry = tk.Entry(root, width=50); self.gender_entry.pack()
        tk.Label(root, text="Appearance:").pack()
        self.appearance_entry = tk.Entry(root, width=50); self.appearance_entry.pack()
        tk.Label(root, text="Voice:").pack()
        self.voice_entry = tk.Entry(root, width=50); self.voice_entry.pack()

        # --- Loadout ---
        tk.Label(root, text="--- Loadout ---", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        self.attire_list = self.make_picker(root, "Equipped Attire:", "Attire")
        self.skills_list = self.make_picker(root, "Assigned Skills:", "Skills")
        self.titles_list = self.make_picker(root, "Titles:", "Titles")
        self.passives_list = self.make_picker(root, "Passives:", "Passives")

        # --- Player Pillar Ranks ---
        tk.Label(root, text="--- Player Pillar Ranks ---", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        self.adv_rank = self.make_rank_spin(root, "Adventurer Rank:")
        self.merc_rank = self.make_rank_spin(root, "Mercenary Rank:")
        self.strat_rank = self.make_rank_spin(root, "Strategy Rank:")

        # --- Tags ---
        tag_frame = tk.LabelFrame(root, text="Tags")
        tag_frame.pack(fill="x", padx=10, pady=10)
        self.tag_entry = tk.Entry(tag_frame, width=40); self.tag_entry.pack()
        btn_frame = tk.Frame(tag_frame); btn_frame.pack()
        tk.Button(btn_frame, text="Add Tag", command=self.add_tag).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Tag List", command=self.open_tag_modal).pack(side="left", padx=2)
        self.tags_listbox = tk.Listbox(tag_frame, height=4, width=40, exportselection=False); self.tags_listbox.pack()
        tk.Button(tag_frame, text="Remove Selected", command=self.remove_tag).pack()

        tk.Button(root, text="Save Character Template", command=self.save_yaml,
                  bg="#2c3e50", fg="white", height=2, width=30).pack(pady=20)

    def get_race_options(self):
        lib_path = os.path.join(os.path.dirname(__file__), "Races", "Race_Library.yaml")
        try:
            with open(lib_path, 'r') as f:
                data = yaml.safe_load(f)
                races = []
                # Monsters are excluded: character templates pair Race+Class,
                # and class kits are for playable/humanoid races only.
                for broad, members in data.items():
                    if broad == "Monsters": continue
                    races.extend(members)
                return races
        except Exception:
            return ["ERROR: Missing Races/Race_Library.yaml"]

    def get_class_options(self):
        lib_path = os.path.join(os.path.dirname(__file__), "Classes", "Class_Library.yaml")
        try:
            with open(lib_path, 'r') as f:
                data = yaml.safe_load(f)
                all_classes = []
                for tier in data.values(): all_classes.extend(tier)
                return all_classes
        except Exception:
            return ["ERROR: Missing Classes/Class_Library.yaml"]

    def get_list(self, folder):
        if not os.path.exists(folder): return []
        return [f.replace('.yaml', '') for f in os.listdir(folder)]

    def make_picker(self, root, label, folder):
        tk.Label(root, text=label).pack()
        listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=5, width=55, exportselection=False)
        for item in self.get_list(folder):
            listbox.insert(tk.END, item)
        listbox.pack()
        return listbox

    def make_rank_spin(self, root, label):
        tk.Label(root, text=label).pack()
        # Snapshot range is 1-3 (see Ranks/Rank_System.yaml)
        spin = tk.Spinbox(root, from_=1, to=3)
        spin.pack()
        return spin

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
            current_tags = list(self.tags_listbox.get(0, tk.END))
            if tag not in current_tags:
                self.tags_listbox.insert(tk.END, tag)

    def remove_tag(self):
        selection = self.tags_listbox.curselection()
        if selection: self.tags_listbox.delete(selection)

    def save_yaml(self):
        race = self.race_cb.get()
        cls = self.class_cb.get()
        if "ERROR" in race or "ERROR" in cls or not race or not cls:
            messagebox.showerror("Error", "Race and Class are required.")
            return

        if not os.path.exists("Characters"): os.makedirs("Characters")

        key = f"Character.{race}.{cls}"
        data = {
            'Key': key,
            'Name': '',
            'RaceKey': race,
            'ClassKey': cls,
            'MainAttribute': self.attr_cb.get(),
            'Role': self.role_entry.get(),
            'Gender': self.gender_entry.get(),
            'Appearance': self.appearance_entry.get(),
            'Voice': self.voice_entry.get(),
            'EquippedAttire': [self.attire_list.get(i) for i in self.attire_list.curselection()],
            'AssignedSkills': [self.skills_list.get(i) for i in self.skills_list.curselection()],
            'Titles': [self.titles_list.get(i) for i in self.titles_list.curselection()],
            'Passives': [self.passives_list.get(i) for i in self.passives_list.curselection()],
            'PlayerAdventurerRank': int(self.adv_rank.get()),
            'PlayerMercenaryRank': int(self.merc_rank.get()),
            'PlayerStrategyRank': int(self.strat_rank.get()),
            'Tags': list(self.tags_listbox.get(0, tk.END))
        }

        with open(f"Characters/{key}.yaml", 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        messagebox.showinfo("Success", f"Character Template Saved: {key}.yaml")


if __name__ == "__main__":
    root = tk.Tk()
    app = CharacterCreatorApp(root)
    root.mainloop()
