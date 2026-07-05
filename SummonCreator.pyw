import tkinter as tk
from tkinter import ttk, messagebox
import yaml, os

def get_condition_files():
    if not os.path.exists("Conditions"): return ["None"]
    files = [f.replace(".yaml", "") for f in os.listdir("Conditions") if f.endswith(".yaml")]
    return ["None"] + sorted(files)

class SummonCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Summon/Bound Entity Suite")
        self.root.geometry("450x850")

        tk.Label(root, text="Summon Name:").pack(); self.name_entry = tk.Entry(root, width=40); self.name_entry.pack()
        
        tk.Label(root, text="Required Condition:").pack()
        self.cond_cb = ttk.Combobox(root, values=get_condition_files(), state="readonly"); self.cond_cb.pack()

        # Attributes Block for Summons
        attr_frame = tk.LabelFrame(root, text="Summon Attributes (Scaling)")
        attr_frame.pack(fill="x", padx=10, pady=10)
        
        self.stats = {}
        for stat in ["Strength", "Stamina", "Speed", "MAG (Shields/Dmg)", "MED (Healing)"]:
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
        self.tags_listbox = tk.Listbox(root, height=4, width=40); self.tags_listbox.pack()
        tk.Button(root, text="Add Tag", command=self.add_tag).pack()
        
        tk.Button(root, text="Save Summon Spec", command=self.save_yaml, bg="#2ecc71").pack(pady=20)

    def add_tag(self):
        tag = self.tag_entry.get().strip()
        if tag: self.tags_listbox.insert(tk.END, tag); self.tag_entry.delete(0, tk.END)

    def save_yaml(self):
        data = {
            'Name': self.name_entry.get(),
            'RequiredCondition': self.cond_cb.get(),
            'Attributes': {k.split(" ")[0]: float(v.get()) for k, v in self.stats.items()},
            'AI': {'Behavior': self.ai_entry.get()},
            'Lifecycle': {'Duration': float(self.dur_entry.get())},
            'Tags': list(self.tags_listbox.get(0, tk.END))
        }
        if not os.path.exists("Summons"): os.makedirs("Summons")
        with open(f"Summons/{self.name_entry.get().replace(' ','_')}.yaml", 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        messagebox.showinfo("Success", "Summon registered.")

if __name__ == "__main__":
    root = tk.Tk()
    SummonCreatorApp(root)
    root.mainloop()