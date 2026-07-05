import tkinter as tk
from tkinter import messagebox
import yaml, os

class TitleRegistryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Title Registry Architect")
        self.root.geometry("400x400")

        tk.Label(root, text="Title ID (e.g. TITLE_KHAGAN):").pack(pady=5)
        self.id_entry = tk.Entry(root, width=40); self.id_entry.pack()

        tk.Label(root, text="Display Name (e.g. Khagan):").pack(pady=5)
        self.name_entry = tk.Entry(root, width=40); self.name_entry.pack()

        tk.Label(root, text="Flavor Text / Lore:").pack(pady=5)
        self.flavor_text = tk.Text(root, height=4, width=40); self.flavor_text.pack()

        tk.Button(root, text="Register Title", command=self.save_yaml, height=2, width=20).pack(pady=20)

    def save_yaml(self):
        tid = self.id_entry.get().strip()
        if not tid: return
        if not os.path.exists("Titles"): os.makedirs("Titles")
        
        data = {
            'TitleID': tid,
            'DisplayName': self.name_entry.get(),
            'FlavorText': self.flavor_text.get("1.0", "end-1c")
        }
        with open(f"Titles/{tid}.yaml", 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        messagebox.showinfo("Success", f"Title '{tid}' registered.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TitleRegistryApp(root)
    root.mainloop()