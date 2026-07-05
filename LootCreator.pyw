import tkinter as tk
from tkinter import ttk, messagebox
import yaml, os

class LootCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Loot Table Architect")
        self.root.geometry("450x500")

        tk.Label(root, text="Select Item from Registry:").pack(pady=5)
        self.item_cb = ttk.Combobox(root, values=self.get_list("Items"), state="readonly", width=37)
        self.item_cb.pack()

        tk.Label(root, text="Drop Rate (0.0 - 1.0):").pack(pady=5)
        self.rate_spin = tk.Spinbox(root, from_=0.0, to=1.0, increment=0.01)
        self.rate_spin.pack()

        tk.Label(root, text="Source Table (e.g. Boss_01_Loot):").pack(pady=5)
        self.source_entry = tk.Entry(root, width=40); self.source_entry.pack()

        tk.Button(root, text="Save Loot Entry", command=self.save_yaml, height=2, width=20).pack(pady=20)

    def get_list(self, folder):
        if not os.path.exists(folder): return []
        return [f.replace('.yaml', '') for f in os.listdir(folder)]

    def save_yaml(self):
        item = self.item_cb.get()
        if not item: return
        
        if not os.path.exists("Loot"): os.makedirs("Loot")
        
        data = {
            'ItemName': item,
            'DropRate': float(self.rate_spin.get()),
            'SourceTable': self.source_entry.get()
        }
        
        filename = f"{self.source_entry.get()}_{item}"
        with open(f"Loot/{filename}.yaml", 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        messagebox.showinfo("Success", f"Loot '{item}' added to {self.source_entry.get()}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LootCreatorApp(root)
    root.mainloop()