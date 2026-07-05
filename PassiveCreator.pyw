import tkinter as tk
from tkinter import messagebox, ttk
import yaml, os

class PassiveCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Passive/Status Architect")
        self.root.geometry("450x950")

        # Identity
        tk.Label(root, text="Passive Name:").pack(); self.name_entry = tk.Entry(root, width=40); self.name_entry.pack()
        tk.Label(root, text="UE5 Context Tag:").pack(); self.ue5_entry = tk.Entry(root, width=40); self.ue5_entry.pack()
        
        # Cleanse Logic
        tk.Label(root, text="Cleanse Requirement (Standard/Contact/Mechanic):").pack()
        self.cleanse_req = ttk.Combobox(root, values=["Standard", "Contact", "Mechanic"], state="readonly")
        self.cleanse_req.current(0)
        self.cleanse_req.pack()
        
        # Pillar & Logic
        tk.Label(root, text="Pillar Affinity:").pack()
        self.pillar_cb = ttk.Combobox(root, values=["Adventurer", "Mercenary", "Strategy"], state="readonly")
        self.pillar_cb.pack()

        # Triggers for Engine
        tk.Label(root, text="Audio Trigger (Asset Path/Name):").pack(); self.audio_entry = tk.Entry(root, width=40); self.audio_entry.pack()
        tk.Label(root, text="Visual Trigger (Asset Path/Name):").pack(); self.visual_entry = tk.Entry(root, width=40); self.visual_entry.pack()

        # Duration & Meta
        tk.Label(root, text="Duration (Seconds):").pack()
        self.duration_spin = tk.Spinbox(root, from_=0, to=999, increment=0.5)
        self.duration_spin.pack()
        
        self.cleanse_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Is Cleanseable", variable=self.cleanse_var).pack(pady=5)

        # Stacking Logic
        stack_frame = tk.LabelFrame(root, text="Stacking Behavior")
        stack_frame.pack(fill="x", padx=10, pady=5)
        self.stack_var = tk.BooleanVar(value=False)
        tk.Checkbutton(stack_frame, text="Is Stackable", variable=self.stack_var).pack()
        tk.Label(stack_frame, text="Max Stacks:").pack()
        self.max_stack_spin = tk.Spinbox(stack_frame, from_=1, to=99)
        self.max_stack_spin.pack()

        # Intents
        tk.Label(root, text="Gameplay Goal:").pack()
        self.gameplay_text = tk.Text(root, height=4, width=40); self.gameplay_text.pack()
        tk.Label(root, text="Narrative Intent:").pack()
        self.narrative_text = tk.Text(root, height=4, width=40); self.narrative_text.pack()

        tk.Button(root, text="Save Passive", command=self.save_yaml, height=2, width=20).pack(pady=20)

    def save_yaml(self):
        if not os.path.exists("Passives"): os.makedirs("Passives")
        data = {
            'Name': self.name_entry.get(),
            'UE5_Context': self.ue5_entry.get(),
            'PillarAffinity': self.pillar_cb.get(),
            'AudioTrigger': self.audio_entry.get(),
            'VisualTrigger': self.visual_entry.get(),
            'Duration': float(self.duration_spin.get()),
            'IsCleanseable': self.cleanse_var.get(),
            'CleanseRequirement': self.cleanse_req.get(),
            'Stacking': {
                'IsStackable': self.stack_var.get(),
                'MaxStacks': int(self.max_stack_spin.get()) if self.stack_var.get() else 1
            },
            'GameplayGoal': self.gameplay_text.get("1.0", "end-1c"),
            'NarrativeIntent': self.narrative_text.get("1.0", "end-1c")
        }
        filename = self.name_entry.get().replace(' ', '_')
        with open(f"Passives/{filename}.yaml", 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        messagebox.showinfo("Success", f"Passive '{self.name_entry.get()}' saved.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PassiveCreatorApp(root)
    root.mainloop()