import tkinter as tk
from tkinter import ttk, messagebox
import yaml, os

# --- Helper Logic ---
if not os.path.exists("tags"): os.makedirs("tags")
if not os.path.exists("Skills"): os.makedirs("Skills")

def add_to_tag_library(new_tag):
    if new_tag and not os.path.exists("tags/tag_library.txt"):
        with open("tags/tag_library.txt", "w") as f: f.write(new_tag + "\n")
    elif new_tag:
        with open("tags/tag_library.txt", "a") as f: f.write(new_tag + "\n")

class SkillCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Methodical Skill Creator")
        self.root.geometry("500x1100")

        # --- Identity ---
        tk.Label(root, text="Skill Name (Key):").pack(pady=2)
        self.name_entry = tk.Entry(root, width=40)
        self.name_entry.pack()
        self.name_entry.bind("<FocusOut>", self.auto_generate_tags)

        # --- Gameplay Mechanics (Formerly Skill Specifics) ---
        mech_frame = tk.LabelFrame(root, text="Gameplay Mechanics")
        mech_frame.pack(fill="x", padx=10, pady=5)
        
        # Target Type
        tk.Label(mech_frame, text="Targeting Type:").pack()
        self.target_cb = ttk.Combobox(mech_frame, values=["Target", "Self", "Area_Circle", "Area_Cone"], state="readonly")
        self.target_cb.pack()

        # Numeric Values
        tk.Label(mech_frame, text="Potency:").pack()
        self.potency_spin = tk.Spinbox(mech_frame, from_=0, to=5000, increment=5)
        self.potency_spin.pack()

        tk.Label(mech_frame, text="Range:").pack()
        self.range_spin = tk.Spinbox(mech_frame, from_=0, to=500, increment=5)
        self.range_spin.pack()

        tk.Label(mech_frame, text="Cast Time (s):").pack()
        self.cast_spin = tk.Spinbox(mech_frame, from_=0, to=10, increment=0.1)
        self.cast_spin.pack()

        tk.Label(mech_frame, text="Resource Cost:").pack()
        self.cost_spin = tk.Spinbox(mech_frame, from_=0, to=1000, increment=1)
        self.cost_spin.pack()

        # --- Assets ---
        asset_frame = tk.LabelFrame(root, text="Visual Assets")
        asset_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(asset_frame, text="Animation Path:").pack()
        self.anim_entry = tk.Entry(asset_frame, width=40); self.anim_entry.pack()
        tk.Label(asset_frame, text="VFX Path:").pack()
        self.vfx_entry = tk.Entry(asset_frame, width=40); self.vfx_entry.pack()

        # --- Tag Management ---
        tag_frame = tk.LabelFrame(root, text="Skill Tags")
        tag_frame.pack(fill="x", padx=10, pady=5)
        self.tags_listbox = tk.Listbox(tag_frame, height=4, width=40)
        self.tags_listbox.pack()
        tk.Button(tag_frame, text="Remove Selected", command=lambda: self.tags_listbox.delete(tk.ANCHOR)).pack()

        tk.Button(root, text="Save Skill", command=self.save_yaml, height=2, width=20, bg="#2c3e50", fg="white").pack(pady=20)

    def auto_generate_tags(self, event=None):
        name = self.name_entry.get().strip()
        if name:
            suggestion = f"Skill.Combat.{name.replace(' ', '.')}"
            if suggestion not in list(self.tags_listbox.get(0, tk.END)):
                self.tags_listbox.insert(tk.END, suggestion)
                add_to_tag_library(suggestion)

    def save_yaml(self):
        name = self.name_entry.get().strip()
        if not name: messagebox.showerror("Error", "Name required."); return
        
        data = {
            'Key': f"Skill.Combat.{name.replace(' ', '.')}",
            'Mechanics': {
                'Targeting': self.target_cb.get(),
                'Potency': float(self.potency_spin.get()),
                'Range': float(self.range_spin.get()),
                'CastTime': float(self.cast_spin.get()),
                'Cost': int(self.cost_spin.get())
            },
            'Assets': {'Animation': self.anim_entry.get(), 'VFX': self.vfx_entry.get()},
            'Tags': list(self.tags_listbox.get(0, tk.END))
        }
        
        with open(f"Skills/{name.replace(' ', '_')}.yaml", 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        messagebox.showinfo("Success", f"Skill '{name}' registered.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SkillCreatorApp(root)
    root.mainloop()