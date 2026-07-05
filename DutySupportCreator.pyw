import tkinter as tk
from tkinter import ttk
import yaml, os

class TutorialNPCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tutorial NPC / Duty Support Creator")
        self.root.geometry("500x500")

        tk.Label(root, text="Mentor Name:").pack(); self.name_entry = tk.Entry(root); self.name_entry.pack()
        tk.Label(root, text="Test Pillar (Which rank to test?):").pack()
        self.pillar_cb = ttk.Combobox(root, values=["Mercenary", "Strategy"])
        self.pillar_cb.pack()

        tk.Label(root, text="Lesson Intent:").pack()
        self.intent_text = tk.Text(root, height=4, width=40); self.intent_text.pack()

        tk.Button(root, text="Create Lesson", command=self.save_yaml).pack(pady=20)

    def save_yaml(self):
        data = {
            'NPCName': self.name_entry.get(),
            'TestSubject': self.pillar_cb.get(),
            'LessonIntent': self.intent_text.get("1.0", "end-1c")
        }
        if not os.path.exists("Tutorials"): os.makedirs("Tutorials")
        with open(f"Tutorials/{self.name_entry.get()}.yaml", 'w') as f:
            yaml.dump(data, f)

if __name__ == "__main__":
    root = tk.Tk()
    app = TutorialNPCApp(root)
    root.mainloop()