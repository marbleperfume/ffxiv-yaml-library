import tkinter as tk
from tkinter import ttk, messagebox
import yaml, os
from expression_library import add_to_expression_library, ExpressionSelectorModal


class DialogueCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dialogue & Cutscene Creator")
        self.root.geometry("560x950")

        # --- Identity ---
        tk.Label(root, text="Dialogue Key (e.g. Dialogue.Chef.Crem.Courier.Seq0.Assignment):").pack()
        self.key_entry = tk.Entry(root, width=50); self.key_entry.pack()

        tk.Label(root, text="Scene (short description):").pack()
        self.scene_entry = tk.Entry(root, width=50); self.scene_entry.pack()

        # --- Participants ---
        tk.Label(root, text="Participants:").pack()
        self.participants_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=6, width=50, exportselection=False)
        for p in ["Player", "Commonfolk"] + self.get_list("NPCs"):
            self.participants_listbox.insert(tk.END, p)
        self.participants_listbox.pack()

        custom_frame = tk.Frame(root); custom_frame.pack(pady=2)
        tk.Label(custom_frame, text="Add Custom Participant:").pack(side="left")
        self.custom_participant_entry = tk.Entry(custom_frame, width=30); self.custom_participant_entry.pack(side="left", padx=5)
        tk.Button(custom_frame, text="Add", command=self.add_custom_participant).pack(side="left")

        # --- Cutscene Fields ---
        tk.Label(root, text="Level Sequence Ref (blank if not a cutscene):").pack()
        self.seq_ref_entry = tk.Entry(root, width=50); self.seq_ref_entry.pack()

        tk.Label(root, text="POV (blank if not a cutscene):").pack()
        self.pov_entry = tk.Entry(root, width=50); self.pov_entry.pack()

        # --- Lines ---
        lines_frame = tk.LabelFrame(root, text="Lines (YAML list of Speaker/Text/ExpressionTag/VOPath)")
        lines_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.lines_text = tk.Text(lines_frame, height=14, width=60)
        self.lines_text.insert(tk.END,
            "- Speaker: NPC.Friendly.MalachiteCity.Crem\n"
            "  Text: \"Line text here.\"\n"
            "  ExpressionTag: \"\"\n"
            "  VOPath: \"\"\n")
        self.lines_text.pack(fill="both", expand=True)

        tk.Button(root, text="Browse Expression Tags (inserts at cursor)", command=self.open_expression_modal).pack(pady=5)

        # --- Narrative ---
        tk.Label(root, text="Narrative Intent:").pack()
        self.intent_text = tk.Text(root, height=3, width=50); self.intent_text.pack()

        tk.Button(root, text="Save Dialogue", command=self.save_yaml, height=2, width=20, bg="#2c3e50", fg="white").pack(pady=15)

    def get_list(self, folder):
        if not os.path.exists(folder): return []
        return sorted(f.replace('.yaml', '').replace('.yml', '') for f in os.listdir(folder) if f.endswith(('.yaml', '.yml')))

    def add_custom_participant(self):
        p = self.custom_participant_entry.get().strip()
        if p:
            self.participants_listbox.insert(tk.END, p)
            self.participants_listbox.select_set(tk.END)
            self.custom_participant_entry.delete(0, tk.END)

    def open_expression_modal(self):
        ExpressionSelectorModal(self.root, self.insert_expression_tag)

    def insert_expression_tag(self, tag):
        self.lines_text.insert(tk.INSERT, tag)

    def save_yaml(self):
        key = self.key_entry.get().strip()
        if not key:
            messagebox.showerror("Error", "Dialogue Key is required.")
            return

        try:
            lines = yaml.safe_load(self.lines_text.get("1.0", "end-1c")) or []
        except yaml.YAMLError as e:
            messagebox.showerror("YAML Error", f"Lines field is not valid YAML: {e}")
            return

        if not os.path.exists("Dialogue"): os.makedirs("Dialogue")

        data = {
            'Key': key,
            'Scene': self.scene_entry.get(),
            'Participants': [self.participants_listbox.get(i) for i in self.participants_listbox.curselection()],
            'LevelSequenceRef': self.seq_ref_entry.get(),
            'POV': self.pov_entry.get(),
            'Lines': lines,
            'NarrativeIntent': self.intent_text.get("1.0", "end-1c")
        }

        with open(f"Dialogue/{key}.yaml", 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        messagebox.showinfo("Success", f"Dialogue '{key}' saved.")


if __name__ == "__main__":
    root = tk.Tk()
    app = DialogueCreatorApp(root)
    root.mainloop()
