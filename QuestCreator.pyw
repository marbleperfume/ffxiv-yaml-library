import tkinter as tk
from tkinter import ttk, messagebox
import yaml, os

class QuestCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quest Creator: Advanced Pipeline")
        self.root.geometry("560x1000")

        # --- Core Pipeline Fields ---
        tk.Label(root, text="Pipeline ID:").pack(); self.pipe_entry = tk.Entry(root, width=40); self.pipe_entry.pack()
        tk.Label(root, text="Sequence Index:").pack(); self.seq_spin = tk.Spinbox(root, from_=0, to=999); self.seq_spin.pack()
        tk.Label(root, text="Quest ID:").pack(); self.quest_entry = tk.Entry(root, width=40); self.quest_entry.pack()

        tk.Label(root, text="Step Type:").pack()
        self.step_type_cb = ttk.Combobox(root, values=["QuestGiver", "Delivery", "Dialogue", "Gather", "Cutscene", "Custom"], state="readonly")
        self.step_type_cb.current(0)
        self.step_type_cb.pack()

        tk.Label(root, text="Action Type:").pack()
        self.action_cb = ttk.Combobox(root, values=["Spawn", "Despawn", "Move", "Dialogue_Override", "Shop_Unlock", "PlayCutscene", "PlayEmote"], state="readonly")
        self.action_cb.pack()

        # --- Tabs ---
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_targets = ttk.Frame(self.notebook); self.notebook.add(self.tab_targets, text="Targets")
        self.tab_flow = ttk.Frame(self.notebook); self.notebook.add(self.tab_flow, text="Flow Control")
        self.tab_reward = ttk.Frame(self.notebook); self.notebook.add(self.tab_reward, text="Reward")

        # --- Targets Tab ---
        tk.Label(self.tab_targets, text="Target NPCs:").pack()
        self.npc_listbox = tk.Listbox(self.tab_targets, selectmode=tk.MULTIPLE, height=6, width=45, exportselection=False)
        for npc in self.get_list("NPCs"): self.npc_listbox.insert(tk.END, npc)
        self.npc_listbox.pack()

        tk.Label(self.tab_targets, text="Target NPC Group:").pack()
        self.npc_group_cb = ttk.Combobox(self.tab_targets, values=["None"] + self.get_list("NPCGroups"), state="readonly", width=42)
        self.npc_group_cb.current(0)
        self.npc_group_cb.pack()

        tk.Label(self.tab_targets, text="Dialogue Ref:").pack()
        self.dialogue_cb = ttk.Combobox(self.tab_targets, values=["None"] + self.get_list("Dialogue"), state="readonly", width=42)
        self.dialogue_cb.current(0)
        self.dialogue_cb.pack()

        tk.Label(self.tab_targets, text="Grant Item (delivery payload):").pack()
        self.grant_item_cb = ttk.Combobox(self.tab_targets, values=["None"] + self.get_list("Items"), state="readonly", width=42)
        self.grant_item_cb.current(0)
        self.grant_item_cb.pack()

        # --- Flow Control Tab ---
        tk.Label(self.tab_flow, text="Requires Flag (blank if none):").pack()
        self.requires_flag_entry = tk.Entry(self.tab_flow, width=45); self.requires_flag_entry.pack()

        tk.Label(self.tab_flow, text="On Complete: Sets Flag (blank if none):").pack()
        self.sets_flag_entry = tk.Entry(self.tab_flow, width=45); self.sets_flag_entry.pack()

        tk.Label(self.tab_flow, text="Conditions (by ConditionName):").pack()
        self.conditions_listbox = tk.Listbox(self.tab_flow, selectmode=tk.MULTIPLE, height=5, width=45, exportselection=False)
        for cond in self.get_condition_names(): self.conditions_listbox.insert(tk.END, cond)
        self.conditions_listbox.pack()

        tk.Label(self.tab_flow, text="Branches (YAML list, optional):").pack()
        self.branches_text = tk.Text(self.tab_flow, height=6, width=50)
        self.branches_text.insert(tk.END, "# - Condition: TargetTag == Tag.Race.Tryll\n#   Effect: TriggerStereotypeBarrier(...)")
        self.branches_text.pack()

        # --- Reward Tab ---
        tk.Label(self.tab_reward, text="Grant Title:").pack()
        self.title_cb = ttk.Combobox(self.tab_reward, values=["None"] + self.get_list("Titles"), state="readonly", width=42)
        self.title_cb.current(0)
        self.title_cb.pack()

        tk.Label(self.tab_reward, text="Grant Item:").pack()
        self.item_cb = ttk.Combobox(self.tab_reward, values=["None"] + self.get_list("Items"), state="readonly", width=42)
        self.item_cb.current(0)
        self.item_cb.pack()

        tk.Label(self.tab_reward, text="Copper:").pack()
        self.copper_spin = tk.Spinbox(self.tab_reward, from_=0, to=999999, width=43); self.copper_spin.pack()

        tk.Label(self.tab_reward, text="Reputation Faction:").pack()
        self.reputation_cb = ttk.Combobox(self.tab_reward, values=["None"] + self.get_reputation_factions(), state="readonly", width=42)
        self.reputation_cb.current(0)
        self.reputation_cb.pack()

        tk.Label(self.tab_reward, text="Reputation Amount:").pack()
        self.reputation_spin = tk.Spinbox(self.tab_reward, from_=0, to=999999, width=43); self.reputation_spin.pack()

        # --- Narrative ---
        tk.Label(root, text="Narrative Intent:").pack()
        self.intent_text = tk.Text(root, height=4, width=45); self.intent_text.pack()

        tk.Button(root, text="Save Quest Step", command=self.save_yaml, height=2, width=20, bg="#2c3e50", fg="white").pack(pady=20)

    def get_list(self, folder):
        if not os.path.exists(folder): return []
        return sorted(f.replace('.yaml', '').replace('.yml', '') for f in os.listdir(folder) if f.endswith(('.yaml', '.yml')))

    def get_condition_names(self):
        folder = "Conditions"
        if not os.path.exists(folder): return []
        names = []
        for fname in os.listdir(folder):
            if not fname.endswith(('.yaml', '.yml')): continue
            try:
                with open(os.path.join(folder, fname)) as f:
                    data = yaml.safe_load(f) or {}
                if 'ConditionName' in data:
                    names.append(data['ConditionName'])
            except Exception:
                continue
        return sorted(names)

    def get_reputation_factions(self):
        folder = "Reputation"
        if not os.path.exists(folder): return []
        names = []
        for fname in os.listdir(folder):
            if not fname.endswith(('.yaml', '.yml')): continue
            try:
                with open(os.path.join(folder, fname)) as f:
                    data = yaml.safe_load(f) or {}
                if 'FactionName' in data:
                    names.append(data['FactionName'])
            except Exception:
                continue
        return sorted(names)

    def save_yaml(self):
        q_id = self.quest_entry.get().strip()
        pipeline_id = self.pipe_entry.get().strip()
        if not q_id or not pipeline_id:
            messagebox.showerror("Error", "Pipeline ID and Quest ID are required.")
            return

        try:
            branches = yaml.safe_load(self.branches_text.get("1.0", "end-1c")) or []
        except yaml.YAMLError as e:
            messagebox.showerror("YAML Error", f"Branches field is not valid YAML: {e}")
            return

        if not os.path.exists("Quests"): os.makedirs("Quests")

        reputation_faction = self.reputation_cb.get()
        requires_flag = self.requires_flag_entry.get().strip()
        sets_flag = self.sets_flag_entry.get().strip()

        data = {
            'PipelineID': pipeline_id,
            'SequenceIndex': int(self.seq_spin.get()),
            'QuestID': q_id,
            'StepType': self.step_type_cb.get(),
            'TargetNPCs': [self.npc_listbox.get(i) for i in self.npc_listbox.curselection()],
            'TargetNPCGroup': self.npc_group_cb.get() if self.npc_group_cb.get() != "None" else None,
            'Action': self.action_cb.get(),
            'DialogueRef': self.dialogue_cb.get() if self.dialogue_cb.get() != "None" else None,
            'GrantItem': self.grant_item_cb.get() if self.grant_item_cb.get() != "None" else None,
            'RequiresFlag': requires_flag or None,
            'OnComplete': {'SetsFlag': sets_flag} if sets_flag else None,
            'Conditions': [self.conditions_listbox.get(i) for i in self.conditions_listbox.curselection()],
            'Branches': branches,
            'Reward': {
                'TitleID': self.title_cb.get() if self.title_cb.get() != "None" else None,
                'ItemID': self.item_cb.get() if self.item_cb.get() != "None" else None,
                'Copper': int(self.copper_spin.get()),
                'Reputation': {
                    'Faction': reputation_faction,
                    'Amount': int(self.reputation_spin.get())
                } if reputation_faction != "None" else None
            },
            'NarrativeIntent': self.intent_text.get("1.0", "end-1c")
        }

        filename = f"{pipeline_id}_Seq{self.seq_spin.get()}"
        with open(f"Quests/{filename}.yaml", 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        messagebox.showinfo("Success", f"Step '{filename}' saved.")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuestCreatorApp(root)
    root.mainloop()
