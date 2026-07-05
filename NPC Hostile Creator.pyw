import tkinter as tk
from tkinter import messagebox, ttk
import yaml, os

class HostileNPCCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Hostile NPC Creator")
        self.root.geometry("500x600")
        
        tk.Label(root, text="Name:").pack(); self.name_entry = tk.Entry(root); self.name_entry.pack()
        tk.Label(root, text="Failure Severity:").pack()
        self.sev_cb = ttk.Combobox(root, values=["None", "Respawn", "Reset"])
        self.sev_cb.pack()

        # Pillar Logic
        self.merc_level = tk.Spinbox(root, from_=1, to=3)
        tk.Label(root, text="Mercenary Commitment (1-3):").pack(); self.merc_level.pack()

        tk.Label(root, text="Character Template (optional — leave blank for a flat NPC):").pack()
        self.template_cb = ttk.Combobox(root, values=[""] + self.get_list("Characters"), state="readonly", width=37)
        self.template_cb.current(0)
        self.template_cb.pack()

        tk.Button(root, text="Save Hostile", command=self.save_yaml).pack(pady=20)

    def get_list(self, folder):
        if not os.path.exists(folder): return []
        return [f.replace('.yaml', '') for f in os.listdir(folder)]

    def save_yaml(self):
        if not os.path.exists("NPCs/Hostile"): os.makedirs("NPCs/Hostile")
        data = {
            'Name': self.name_entry.get(),
            'Severity': self.sev_cb.get(),
            'MercenaryLevel': self.merc_level.get(),
            'TemplateRef': self.template_cb.get() or None
        }
        with open(f"NPCs/Hostile/{self.name_entry.get().replace(' ', '_')}.yaml", 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        messagebox.showinfo("Success", "Hostile NPC Saved.")

if __name__ == "__main__":
    root = tk.Tk()
    app = HostileNPCCreator(root)
    root.mainloop()