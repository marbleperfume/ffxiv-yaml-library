import tkinter as tk
from tkinter import ttk, messagebox
import yaml, os
from tag_library import add_to_tag_library, TagSelectorModal

class UnifiedItemRegistryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unified Item & Equipment Registry")
        self.root.geometry("550x1100")

        # --- Identity ---
        tk.Label(root, text="Item Name (Key):").pack(pady=2)
        self.name_entry = tk.Entry(root, width=40); self.name_entry.pack()

        tk.Label(root, text="Category:").pack(pady=2)
        self.cat_cb = ttk.Combobox(root, values=["Equipment", "Attire", "Minion", "Music", "Consumable", "Material"], state="readonly")
        self.cat_cb.pack()

        tk.Label(root, text="Rarity:").pack(pady=2)
        self.rarity_cb = ttk.Combobox(root, values=["Common", "Uncommon", "Rare", "Epic", "Legendary", "Unique"], state="readonly")
        self.rarity_cb.pack()

        # --- Stacking Logic ---
        stack_frame = tk.LabelFrame(root, text="Stacking Behavior")
        stack_frame.pack(fill="x", padx=10, pady=5)
        self.stack_var = tk.BooleanVar(value=False)
        tk.Checkbutton(stack_frame, text="Is Stackable", variable=self.stack_var).pack()
        tk.Label(stack_frame, text="Max Stacks:").pack()
        self.max_stack_spin = tk.Spinbox(stack_frame, from_=1, to=999); self.max_stack_spin.pack()

        # --- Equipment, Stats & Restrictions ---
        equip_frame = tk.LabelFrame(root, text="Equipment Data & Stats")
        equip_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(equip_frame, text="Slot:").pack()
        self.slot_cb = ttk.Combobox(equip_frame, values=["None", "Weapon", "Head", "Torso", "Arms", "Legs", "Feet", "Accessory"], state="readonly")
        self.slot_cb.pack()
        
        # Stat Inputs
        stats_subframe = tk.Frame(equip_frame)
        stats_subframe.pack(pady=5)
        self.stat_entries = {}
        for stat in ["Atk", "Def", "MAG", "MED"]:
            f = tk.Frame(stats_subframe)
            f.pack(side="left", padx=5)
            tk.Label(f, text=stat).pack()
            e = tk.Entry(f, width=6); e.insert(0, "0"); e.pack()
            self.stat_entries[stat] = e

        tk.Label(equip_frame, text="Restriction Tags:").pack()
        self.tag_entry = tk.Entry(equip_frame, width=40); self.tag_entry.pack()
        
        btn_frame = tk.Frame(equip_frame)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Add Tag", command=self.add_tag).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Tag List", command=self.open_tag_modal).pack(side="left", padx=2)
        
        self.tags_listbox = tk.Listbox(equip_frame, height=4, width=40, exportselection=False)
        self.tags_listbox.pack()
        tk.Button(equip_frame, text="Remove Selected", command=self.remove_tag).pack()

        # --- Metadata ---
        tk.Label(root, text="Icon/Asset Path:").pack(pady=2)
        self.icon_entry = tk.Entry(root, width=40); self.icon_entry.pack()

        tk.Label(root, text="Description:").pack(pady=2)
        self.desc_text = tk.Text(root, height=4, width=40); self.desc_text.pack()

        tk.Button(root, text="Register Item/Equipment", command=self.save_yaml, height=2, width=30, bg="#2c3e50", fg="white").pack(pady=20)

    def add_tag(self):
        tag = self.tag_entry.get().strip()
        if tag: 
            self.tags_listbox.insert(tk.END, tag)
            add_to_tag_library(tag)
            self.tag_entry.delete(0, tk.END)
    
    def open_tag_modal(self):
        TagSelectorModal(self.root, self.add_tags_from_modal)

    def add_tags_from_modal(self, tags):
        for tag in tags:
            current_tags = list(self.tags_listbox.get(0, tk.END))
            if tag not in current_tags:
                self.tags_listbox.insert(tk.END, tag)

    def remove_tag(self):
        selection = self.tags_listbox.curselection()
        if selection: self.tags_listbox.delete(selection)

    def save_yaml(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Item Name is required.")
            return

        if not os.path.exists("Items"): os.makedirs("Items")
        
        data = {
            'Name': name,
            'Category': self.cat_cb.get(),
            'Rarity': self.rarity_cb.get(),
            'Stacking': {
                'IsStackable': self.stack_var.get(),
                'MaxStacks': int(self.max_stack_spin.get()) if self.stack_var.get() else 1
            },
            'EquipmentData': {
                'Slot': self.slot_cb.get(),
                'Stats': {k: int(v.get()) for k, v in self.stat_entries.items()},
                'RestrictionTags': list(self.tags_listbox.get(0, tk.END))
            },
            'IconPath': self.icon_entry.get(),
            'Description': self.desc_text.get("1.0", "end-1c")
        }
        
        with open(f"Items/{name.replace(' ', '_')}.yaml", 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        messagebox.showinfo("Success", f"'{name}' registered to Item Registry.")

if __name__ == "__main__":
    root = tk.Tk()
    app = UnifiedItemRegistryApp(root)
    root.mainloop()