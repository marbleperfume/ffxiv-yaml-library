import tkinter as tk
from tkinter import ttk, messagebox
import yaml, os

class QuestCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quest Creator: Advanced Pipeline")
        self.root.geometry("500x900")

        # --- Existing Pipeline Fields ---
        tk.Label(root, text="Pipeline ID:").pack(); self.pipe_entry = tk.Entry(root, width=40); self.pipe_entry.pack()
        tk.Label(root, text="Sequence Index:").pack(); self.seq_spin = tk.Spinbox(root, from_=0, to=999); self.seq_spin.pack()
        tk.Label(root, text="Quest ID:").pack(); self.quest_entry = tk.Entry(root, width=40); self.quest_entry.pack()

        # --- NPC Interaction ---
        tk.Label(root, text="Target NPC ID:").pack()
        self.npc_cb = ttk.Combobox(root, values=self.get_list("NPCs"), state="readonly", width=37)
        self.npc_cb.pack()
        
        tk.Label(root, text="Action Type:").pack()
        self.action_cb = ttk.Combobox(root, values=["Spawn", "Despawn", "Move", "Dialogue_Override", "Shop_Unlock"], state="readonly")
        self.action_cb.pack()

        # --- Rewards/Modifications ---
        tk.Label(root, text="Grant Title:").pack()
        self.title_cb = ttk.Combobox(root, values=["None"] + self.get_list("Titles"), state="readonly", width=37)
        self.title_cb.current(0)
        self.title_cb.pack()
        
        tk.Label(root, text="Grant Item:").pack()
        self.item_cb = ttk.Combobox(root, values=["None"] + self.get_list("Items"), state="readonly", width=37)
        self.item_cb.current(0)
        self.item_cb.pack()

        # --- Narrative ---
        tk.Label(root, text="Narrative Intent:").pack()
        self.intent_text = tk.Text(root, height=4, width=40); self.intent_text.pack()

        tk.Button(root, text="Save Quest Step", command=self.save_yaml, height=2, width=20, bg="#2c3e50", fg="white").pack(pady=20)

    def get_list(self, folder):
        if not os.path.exists(folder): return []
        return [f.replace('.yaml', '') for f in os.listdir(folder)]

    def save_yaml(self):
        q_id = self.quest_entry.get().strip()
        if not q_id:
            messagebox.showerror("Error", "Quest ID is required.")
            return

        if not os.path.exists("Quests"): os.makedirs("Quests")
        
        data = {
            'PipelineID': self.pipe_entry.get(),
            'SequenceIndex': int(self.seq_spin.get()),
            'QuestID': q_id,
            'TargetNPC': self.npc_cb.get(),
            'Action': self.action_cb.get(),
            'Reward': {
                'TitleID': self.title_cb.get() if self.title_cb.get() != "None" else None,
                'ItemID': self.item_cb.get() if self.item_cb.get() != "None" else None
            },
            'NarrativeIntent': self.intent_text.get("1.0", "end-1c")
        }
        
        # Save filename by PipelineID and Sequence for easy ordering
        filename = f"{self.pipe_entry.get()}_Seq{self.seq_spin.get()}"
        with open(f"Quests/{filename}.yaml", 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        messagebox.showinfo("Success", f"Step '{filename}' saved.")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuestCreatorApp(root)
    root.mainloop()