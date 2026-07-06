import tkinter as tk
from tkinter import ttk, messagebox
import yaml, os

class FriendlyNPCCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Friendly NPC Architect")
        self.root.geometry("500x950")

        # --- Identity & Role ---
        tk.Label(root, text="NPC Name:").pack(); self.name_entry = tk.Entry(root, width=40); self.name_entry.pack()
        tk.Label(root, text="Unique NPC ID:").pack(); self.id_entry = tk.Entry(root, width=40); self.id_entry.pack()
        
        tk.Label(root, text="NPC Role:").pack()
        self.role_cb = ttk.Combobox(root, values=["Townsperson", "Shopkeeper", "QuestGiver", "Vendor", "Static"], state="readonly")
        self.role_cb.current(0)
        self.role_cb.pack()

        # --- Placement & Conditions ---
        tk.Label(root, text="Zone Tag (Location):").pack(); self.zone_entry = tk.Entry(root, width=40); self.zone_entry.pack()
        tk.Label(root, text="Required Quest ID (Leave blank for Always Active):").pack(); self.quest_entry = tk.Entry(root, width=40); self.quest_entry.pack()

        # --- Shop Items (Linked to Registry) ---
        tk.Label(root, text="Select Shop Inventory (Only for Shopkeepers/Vendors):").pack()
        self.item_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=5, width=40, exportselection=False)
        self.item_listbox.pack()
        for item in self.get_registry_list("Items"):
            self.item_listbox.insert(tk.END, item)

        tk.Label(root, text="Character Template (optional — leave blank for a flat NPC):").pack()
        self.template_cb = ttk.Combobox(root, values=[""] + self.get_registry_list("Characters"), state="readonly", width=37)
        self.template_cb.current(0)
        self.template_cb.pack()

        # --- Narrative & Banter ---
        tk.Label(root, text="Narrative Intent:").pack()
        self.intent_text = tk.Text(root, height=3, width=40); self.intent_text.pack()

        tk.Label(root, text="Banter Sets (YAML Format):").pack()
        self.banter_text = tk.Text(root, height=8, width=40)
        self.banter_text.insert(tk.END, "Default:\n  - Hello there!\nTITLE_KHAGAN:\n  - Hail, Khagan!")
        self.banter_text.pack()

        tk.Button(root, text="Save NPC", command=self.save_yaml, height=2, width=20, bg="#2c3e50", fg="white").pack(pady=20)

    def get_registry_list(self, folder):
        if not os.path.exists(folder): return []
        return [f.replace('.yaml', '') for f in os.listdir(folder)]

    def save_yaml(self):
        npc_id = self.id_entry.get().strip()
        if not npc_id:
            messagebox.showerror("Error", "NPC ID is required.")
            return

        # Default to 'None' if quest entry is blank
        spawn_cond = self.quest_entry.get().strip() or "None"
        
        if not os.path.exists("NPCs"): os.makedirs("NPCs")
        
        data = {
            'Name': self.name_entry.get(),
            'NPC_ID': npc_id,
            'Role': self.role_cb.get(),
            'Location': self.zone_entry.get(),
            'SpawnCondition': spawn_cond,
            'ShopInventory': [self.item_listbox.get(i) for i in self.item_listbox.curselection()],
            'TemplateRef': self.template_cb.get() or None,
            'NarrativeIntent': self.intent_text.get("1.0", "end-1c"),
            'BanterSets': yaml.safe_load(self.banter_text.get("1.0", "end-1c"))
        }
        
        with open(f"NPCs/{npc_id}.yaml", 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        messagebox.showinfo("Success", f"NPC '{npc_id}' saved.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FriendlyNPCCreatorApp(root)
    root.mainloop()