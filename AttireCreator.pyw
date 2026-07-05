import tkinter as tk
from tkinter import ttk, messagebox
import yaml, os
from tag_library import add_to_tag_library, TagSelectorModal

class AttireCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attire Creator")
        self.root.geometry("500x900")

        # --- Identity ---
        tk.Label(root, text="Attire Name (Key):").pack(pady=2)
        self.name_entry = tk.Entry(root, width=40); self.name_entry.pack()

        # --- Attire Properties ---
        tk.Label(root, text="Slot:").pack()
        self.slot_cb = ttk.Combobox(root, values=["Head", "Body", "Hands", "Legs", "Feet"], state="readonly")
        self.slot_cb.pack()
        
        self.dyeable_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Is Dyeable", variable=self.dyeable_var).pack(pady=5)

        # --- Restrictions ---
        restrict_frame = tk.LabelFrame(root, text="Restriction Tags")
        restrict_frame.pack(fill="x", padx=10, pady=5)
        
        self.tag_entry = tk.Entry(restrict_frame, width=40); self.tag_entry.pack()
        
        btn_frame = tk.Frame(restrict_frame)
        btn_frame.pack()
        tk.Button(btn_frame, text="Add Tag", command=self.add_tag).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Tag List", command=self.open_tag_modal).pack(side="left", padx=2)
        
        self.tags_listbox = tk.Listbox(restrict_frame, height=4, width=40)
        self.tags_listbox.pack()
        tk.Button(restrict_frame, text="Remove Selected", command=self.remove_tag).pack()

        # --- Metadata ---
        tk.Label(root, text="Icon/Asset Path:").pack(pady=2)
        self.icon_entry = tk.Entry(root, width=40); self.icon_entry.pack()

        tk.Label(root, text="Description:").pack(pady=2)
        self.desc_text = tk.Text(root, height=4, width=40); self.desc_text.pack()

        tk.Button(root, text="Register Attire", command=self.save_yaml, height=2, width=20, bg="#2c3e50", fg="white").pack(pady=20)

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
            messagebox.showerror("Error", "Name is required.")
            return

        if not os.path.exists("Attire"): os.makedirs("Attire")
        
        data = {
            'Name': name,
            'Slot': self.slot_cb.get(),
            'IsDyeable': self.dyeable_var.get(),
            'RestrictionTags': list(self.tags_listbox.get(0, tk.END)),
            'IconPath': self.icon_entry.get(),
            'Description': self.desc_text.get("1.0", "end-1c")
        }
        
        with open(f"Attire/{name.replace(' ', '_')}.yaml", 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        messagebox.showinfo("Success", f"Attire '{name}' registered.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AttireCreatorApp(root)
    root.mainloop()