import tkinter as tk
from tkinter import ttk, messagebox
import yaml, os
from tag_library import add_to_tag_library, TagSelectorModal

class ConditionCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Condition Logic Creator")
        self.root.geometry("500x950") # Expanded to fit new tabs

        # --- Global Condition Data ---
        tk.Label(root, text="Condition Name (Key):").pack(pady=2)
        self.name_entry = tk.Entry(root, width=40); self.name_entry.pack()

        tk.Label(root, text="Duration (seconds, 0 for infinite):").pack(pady=2)
        self.duration_spin = tk.Spinbox(root, from_=0, to=99999, width=38); self.duration_spin.pack()

        # --- Tabs for Logic Intent ---
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, fill="both", expand=True)

        self.tab_quest = ttk.Frame(self.notebook); self.notebook.add(self.tab_quest, text="Quest")
        self.tab_inventory = ttk.Frame(self.notebook); self.notebook.add(self.tab_inventory, text="Inventory")
        self.tab_player = ttk.Frame(self.notebook); self.notebook.add(self.tab_player, text="Player/Stat")
        self.tab_world = ttk.Frame(self.notebook); self.notebook.add(self.tab_world, text="World")
        self.tab_buff = ttk.Frame(self.notebook); self.notebook.add(self.tab_buff, text="Buff")
        self.tab_combo = ttk.Frame(self.notebook); self.notebook.add(self.tab_combo, text="Combo")

        # --- Tab Inputs ---
        # Quest
        tk.Label(self.tab_quest, text="Quest ID:").pack(); self.q_id = tk.Entry(self.tab_quest); self.q_id.pack()
        tk.Label(self.tab_quest, text="Required State:").pack(); self.q_val = tk.Entry(self.tab_quest); self.q_val.pack()
        
        # Inventory
        tk.Label(self.tab_inventory, text="Item ID:").pack(); self.i_id = tk.Entry(self.tab_inventory); self.i_id.pack()
        tk.Label(self.tab_inventory, text="Minimum Quantity:").pack(); self.i_val = tk.Entry(self.tab_inventory); self.i_val.pack()
        
        # Player/Stat
        tk.Label(self.tab_player, text="Stat Name:").pack(); self.s_id = tk.Entry(self.tab_player); self.s_id.pack()
        tk.Label(self.tab_player, text="Threshold:").pack(); self.s_val = tk.Entry(self.tab_player); self.s_val.pack()
        
        # World
        tk.Label(self.tab_world, text="World Event Key:").pack(); self.w_id = tk.Entry(self.tab_world); self.w_id.pack()
        tk.Label(self.tab_world, text="Status (e.g. Active):").pack(); self.w_val = tk.Entry(self.tab_world); self.w_val.pack()

        # Buff
        tk.Label(self.tab_buff, text="Buff ID:").pack(); self.b_id = tk.Entry(self.tab_buff); self.b_id.pack()
        tk.Label(self.tab_buff, text="Stacks Required:").pack(); self.b_val = tk.Entry(self.tab_buff); self.b_val.pack()

        # Combo
        tk.Label(self.tab_combo, text="Previous Skill ID:").pack(); self.c_id = tk.Entry(self.tab_combo); self.c_id.pack()
        tk.Label(self.tab_combo, text="Window (s):").pack(); self.c_val = tk.Entry(self.tab_combo); self.c_val.pack()

        # --- Tags ---
        restrict_frame = tk.LabelFrame(root, text="Reference Tags")
        restrict_frame.pack(fill="x", padx=10, pady=15)
        self.tag_entry = tk.Entry(restrict_frame, width=40); self.tag_entry.pack()
        btn_frame = tk.Frame(restrict_frame); btn_frame.pack()
        tk.Button(btn_frame, text="Add Tag", command=self.add_tag).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Tag List", command=self.open_tag_modal).pack(side="left", padx=2)
        self.tags_listbox = tk.Listbox(restrict_frame, height=4, width=40); self.tags_listbox.pack()
        tk.Button(restrict_frame, text="Remove Selected", command=self.remove_tag).pack()

        tk.Button(root, text="Save Condition", command=self.save_yaml, height=2, width=20, bg="#2c3e50", fg="white").pack(pady=20)

    def add_tag(self):
        tag = self.tag_entry.get().strip()
        if tag: self.tags_listbox.insert(tk.END, tag); add_to_tag_library(tag); self.tag_entry.delete(0, tk.END)
    
    def open_tag_modal(self):
        TagSelectorModal(self.root, self.add_tags_from_modal)

    def add_tags_from_modal(self, tags):
        for tag in tags:
            if tag not in list(self.tags_listbox.get(0, tk.END)): self.tags_listbox.insert(tk.END, tag)

    def remove_tag(self):
        selection = self.tags_listbox.curselection()
        if selection: self.tags_listbox.delete(selection)

    def save_yaml(self):
        name = self.name_entry.get().strip()
        if not name: messagebox.showerror("Error", "Name required."); return
        
        current_tab = self.notebook.tab(self.notebook.select(), "text")
        # Logic mapping
        mapping = {"Quest": (self.q_id, self.q_val), "Inventory": (self.i_id, self.i_val), 
                   "Player/Stat": (self.s_id, self.s_val), "World": (self.w_id, self.w_val),
                   "Buff": (self.b_id, self.b_val), "Combo": (self.c_id, self.c_val)}
        
        target, val = mapping[current_tab][0].get(), mapping[current_tab][1].get()

        if not os.path.exists("Conditions"): os.makedirs("Conditions")
        data = {
            'ConditionName': name,
            'Category': current_tab,
            'Target': target,
            'RequiredValue': val,
            'Duration': int(self.duration_spin.get()),
            'Tags': list(self.tags_listbox.get(0, tk.END))
        }
        with open(f"Conditions/{name.replace(' ', '_')}.yaml", 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        messagebox.showinfo("Success", f"'{name}' saved as {current_tab} condition.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConditionCreatorApp(root)
    root.mainloop()