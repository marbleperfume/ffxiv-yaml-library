import tkinter as tk
from tkinter import ttk, messagebox
import yaml, os

class LootTableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Loot Table Architect")
        self.root.geometry("480x650")

        tk.Label(root, text="Loot Table Name (e.g. Boss_01_Loot):").pack(pady=5)
        self.table_cb = ttk.Combobox(root, values=self.get_table_names(), width=37)
        self.table_cb.pack()
        tk.Button(root, text="Load Existing Table", command=self.load_table).pack(pady=5)

        # --- Entry composer ---
        entry_frame = tk.LabelFrame(root, text="Add Entry")
        entry_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(entry_frame, text="Item from Registry:").pack(pady=2)
        self.item_cb = ttk.Combobox(entry_frame, values=self.get_item_keys(), state="readonly", width=37)
        self.item_cb.pack()

        tk.Label(entry_frame, text="Drop Rate (0.0 - 1.0):").pack(pady=2)
        self.rate_spin = tk.Spinbox(entry_frame, from_=0.0, to=1.0, increment=0.01)
        self.rate_spin.pack()

        tk.Button(entry_frame, text="Add Entry", command=self.add_entry).pack(pady=5)

        # --- Current table contents ---
        tk.Label(root, text="Table Entries:").pack(pady=(10, 2))
        self.entries_listbox = tk.Listbox(root, height=10, width=55, exportselection=False)
        self.entries_listbox.pack(padx=10)
        tk.Button(root, text="Remove Selected Entry", command=self.remove_entry).pack(pady=5)

        tk.Button(root, text="Save Loot Table", command=self.save_yaml, height=2, width=20, bg="#2c3e50", fg="white").pack(pady=15)

    def get_table_names(self):
        if not os.path.exists("Loot"): return []
        return sorted(f.replace('.yaml', '') for f in os.listdir("Loot") if f.endswith(('.yaml', '.yml')))

    def get_item_keys(self):
        folder = "Items"
        if not os.path.exists(folder): return []
        keys = []
        for fname in os.listdir(folder):
            if not fname.endswith(('.yaml', '.yml')): continue
            try:
                with open(os.path.join(folder, fname)) as f:
                    data = yaml.safe_load(f) or {}
                keys.append(data.get('Key', fname.rsplit('.', 1)[0]))
            except Exception:
                keys.append(fname.rsplit('.', 1)[0])
        return sorted(keys)

    def load_table(self):
        table = self.table_cb.get().strip()
        path = f"Loot/{table}.yaml"
        if not table or not os.path.exists(path):
            messagebox.showerror("Error", f"No table file found at {path}")
            return
        with open(path) as f:
            data = yaml.safe_load(f) or {}
        self.entries_listbox.delete(0, tk.END)
        for entry in data.get('Entries', []):
            self.entries_listbox.insert(tk.END, f"{entry['ItemKey']} | {entry['DropRate']}")

    def add_entry(self):
        item = self.item_cb.get()
        if not item:
            messagebox.showerror("Error", "Select an item first.")
            return
        self.entries_listbox.insert(tk.END, f"{item} | {float(self.rate_spin.get())}")

    def remove_entry(self):
        selection = self.entries_listbox.curselection()
        if selection: self.entries_listbox.delete(selection)

    def save_yaml(self):
        table = self.table_cb.get().strip()
        if not table:
            messagebox.showerror("Error", "Table name is required.")
            return
        if self.entries_listbox.size() == 0:
            messagebox.showerror("Error", "Table has no entries.")
            return

        entries = []
        for i in range(self.entries_listbox.size()):
            item_key, rate = self.entries_listbox.get(i).rsplit(" | ", 1)
            entries.append({'ItemKey': item_key, 'DropRate': float(rate)})

        if not os.path.exists("Loot"): os.makedirs("Loot")
        data = {'TableName': table, 'Entries': entries}
        with open(f"Loot/{table}.yaml", 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

        self.table_cb['values'] = self.get_table_names()
        messagebox.showinfo("Success", f"Loot table '{table}' saved with {len(entries)} entries.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LootTableApp(root)
    root.mainloop()
