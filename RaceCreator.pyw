# --- AUTO-INJECTED CONFIG ---
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "Attributes"))
from attr_loader import get_full_attribute_data
# ----------------------------

import tkinter as tk
from tkinter import messagebox, ttk
import yaml

class RaceCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AAA Race Design Suite")
        self.root.geometry("600x950")
        
        # Load Schema and Base Data
        self.schema, self.base_data = get_full_attribute_data(__file__)

        # --- PREVIEW TABLE (Master Race Library) ---
        tk.Label(root, text="Master Race Library Preview", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        
        self.tree = ttk.Treeview(root, columns=("Broad", "Subrace"), show="headings", height=8)
        self.tree.heading("Broad", text="Broad Category")
        self.tree.heading("Subrace", text="Subrace")
        self.tree.column("Broad", width=200)
        self.tree.column("Subrace", width=200)
        self.tree.pack(fill="x", padx=20, pady=5)
        
        self.load_and_populate_library()

        # --- UI Fields ---
        tk.Label(root, text="Parent Category:").pack(pady=(10, 0))
        self.parent_cb = ttk.Combobox(root, values=["Landwin", "Noct Aurorus", "Wanderers", "Linfree", "Depth Dead"], width=47, state="readonly")
        self.parent_cb.pack()

        tk.Label(root, text="Subrace Name:").pack()
        self.subrace_entry = tk.Entry(root, width=50); self.subrace_entry.pack()

        tk.Label(root, text="Narrative Intent:").pack()
        self.narr_entry = tk.Entry(root, width=50); self.narr_entry.pack()

        tk.Label(root, text="Mesh Path:").pack()
        self.mesh_entry = tk.Entry(root, width=50); self.mesh_entry.pack()

        tk.Label(root, text="Anim Set ID:").pack()
        self.anim_entry = tk.Entry(root, width=50); self.anim_entry.pack()

        tk.Label(root, text="Banned Tags (Name/Key, comma separated):").pack()
        self.ban_entry = tk.Entry(root, width=50); self.ban_entry.pack()

        # --- Bonus Skills (racial AbilitySet, orthogonal to Class kit) ---
        tk.Label(root, text="Bonus Skills (granted by race, independent of Class):").pack(pady=(10, 0))
        self.bonus_skills_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=5, width=55, exportselection=False)
        for skill in self.get_list("Skills"):
            self.bonus_skills_listbox.insert(tk.END, skill)
        self.bonus_skills_listbox.pack()

        # --- Attribute Modifiers ---
        tk.Label(root, text="--- Attribute Modifiers ---", font=("Arial", 10, "bold")).pack(pady=10)
        
        self.stats = {}
        for stat, details in self.schema.items():
            frame = tk.Frame(root)
            frame.pack(fill="x", padx=100, pady=2)
            tk.Label(frame, text=stat, width=15, anchor="e").pack(side="left")
            
            default_val = self.base_data.get(stat.capitalize(), details.get("default", "0"))
            
            entry = tk.Entry(frame, width=10)
            entry.insert(0, str(default_val))
            entry.pack(side="left", padx=10)
            self.stats[stat] = entry

        tk.Button(root, text="Save AAA Race Spec", command=self.save_yaml, bg="#2c3e50", fg="white", height=2, width=30).pack(pady=20)

    def get_list(self, folder):
        if not os.path.exists(folder): return []
        return sorted(f.replace('.yaml', '').replace('.yml', '') for f in os.listdir(folder) if f.endswith(('.yaml', '.yml')))

    def load_and_populate_library(self):
        """Loads data from Races/Race_Library.yaml and populates the Treeview."""
        lib_path = os.path.join(os.path.dirname(__file__), "Races", "Race_Library.yaml")
        
        if not os.path.exists(lib_path):
            self.tree.insert("", "end", values=("Error", "Library file missing"))
            return

        try:
            with open(lib_path, 'r') as f:
                data = yaml.safe_load(f)
                for broad, subraces in data.items():
                    for sub in subraces:
                        self.tree.insert("", "end", values=(broad, sub))
        except Exception as e:
            messagebox.showerror("Library Error", f"Failed to load Race_Library.yaml: {e}")

    def save_yaml(self):
        subrace = self.subrace_entry.get().strip()
        parent = self.parent_cb.get()
        if not subrace or not parent:
            messagebox.showerror("Error", "Parent and Subrace Name are required.")
            return

        # Ensure directory exists
        if not os.path.exists("Races"): os.makedirs("Races")
        
        filename = f"{parent}_{subrace}.yaml".replace(" ", "_")
        stat_data = {stat: int(entry.get()) for stat, entry in self.stats.items()}

        data = {
            'Intent': {'Narrative': self.narr_entry.get()},
            'Definition': {
                'ParentCategory': parent,
                'Subrace': subrace,
                'AttributeModifiers': stat_data,
                'Assets': {'Mesh': self.mesh_entry.get(), 'AnimSet': self.anim_entry.get()},
                'Restrictions': {'BannedTags': [b.strip() for b in self.ban_entry.get().split(',') if b.strip()]},
                'BonusSkills': [self.bonus_skills_listbox.get(i) for i in self.bonus_skills_listbox.curselection()]
            }
        }
        
        with open(f"Races/{filename}", 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
            
        messagebox.showinfo("Success", f"Spec Saved: {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RaceCreatorApp(root)
    root.mainloop()