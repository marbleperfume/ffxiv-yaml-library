# --- AUTO-INJECTED CONFIG ---
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "Attributes"))
from attr_loader import get_full_attribute_data
# ----------------------------

import tkinter as tk
from tkinter import ttk, messagebox
import yaml

def get_condition_names():
    if not os.path.exists("Conditions"): return ["None"]
    names = []
    for fname in os.listdir("Conditions"):
        if not fname.endswith(('.yaml', '.yml')): continue
        try:
            with open(os.path.join("Conditions", fname)) as f:
                data = yaml.safe_load(f) or {}
            names.append(data.get('ConditionName', fname.rsplit('.', 1)[0]))
        except Exception:
            names.append(fname.rsplit('.', 1)[0])
    return ["None"] + sorted(names)

class SummonCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Summon/Bound Entity Suite")
        self.root.geometry("450x900")

        self.schema, _ = get_full_attribute_data(__file__)

        tk.Label(root, text="Summon Name:").pack(); self.name_entry = tk.Entry(root, width=40); self.name_entry.pack()

        tk.Label(root, text="Required Condition:").pack()
        self.cond_cb = ttk.Combobox(root, values=get_condition_names(), state="readonly"); self.cond_cb.pack()

        # Attribute multipliers, keyed off the shared schema (Attributes/attributes.json)
        attr_frame = tk.LabelFrame(root, text="Summon Attribute Multipliers (x owner stat)")
        attr_frame.pack(fill="x", padx=10, pady=10)

        self.stats = {}
        for stat in self.schema.keys():
            frame = tk.Frame(attr_frame)
            frame.pack(fill="x", padx=50, pady=2)
            tk.Label(frame, text=stat, width=18, anchor="e").pack(side="left")
            entry = tk.Entry(frame, width=10); entry.insert(0, "1.0")
            entry.pack(side="left", padx=10)
            self.stats[stat] = entry

        tk.Label(root, text="AI Behavior:").pack(); self.ai_entry = tk.Entry(root, width=40); self.ai_entry.pack()
        tk.Label(root, text="Duration (0 for inf):").pack(); self.dur_entry = tk.Entry(root, width=10); self.dur_entry.insert(0, "30"); self.dur_entry.pack()

        tk.Label(root, text="Tags:").pack()
        self.tag_entry = tk.Entry(root, width=40); self.tag_entry.pack()
        self.tags_listbox = tk.Listbox(root, height=4, width=40, exportselection=False); self.tags_listbox.pack()
        tk.Button(root, text="Add Tag", command=self.add_tag).pack()

        tk.Button(root, text="Save Summon Spec", command=self.save_yaml, bg="#2ecc71").pack(pady=20)

    def add_tag(self):
        tag = self.tag_entry.get().strip()
        if tag: self.tags_listbox.insert(tk.END, tag); self.tag_entry.delete(0, tk.END)

    def save_yaml(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Name required.")
            return
        data = {
            'Name': name,
            'RequiredCondition': self.cond_cb.get(),
            'Attributes': {k: float(v.get()) for k, v in self.stats.items()},
            'AI': {'Behavior': self.ai_entry.get()},
            'Lifecycle': {'Duration': float(self.dur_entry.get())},
            'Tags': list(self.tags_listbox.get(0, tk.END))
        }
        if not os.path.exists("Summons"): os.makedirs("Summons")
        with open(f"Summons/{name.replace(' ','_')}.yaml", 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        messagebox.showinfo("Success", "Summon registered.")

if __name__ == "__main__":
    root = tk.Tk()
    SummonCreatorApp(root)
    root.mainloop()
