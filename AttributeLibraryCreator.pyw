import tkinter as tk
from tkinter import messagebox
import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "Attributes"))

from attr_loader import get_full_attribute_data

class AttributeLibApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attribute Library (Source of Truth)")
        self.root.geometry("700x700")

        # --- Path Anchoring & Folder Creation ---
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.attr_dir = os.path.join(self.script_dir, "Attributes")
        
        # Ensure the Attributes folder exists
        os.makedirs(self.attr_dir, exist_ok=True)
        
        # Define paths within the new folder
        self.json_path = os.path.join(self.attr_dir, "attributes.json")
        self.txt_path = os.path.join(self.script_dir, "Attribute_Library.txt")

        # --- First Run Logic ---
        self.ensure_json_exists()

        # --- UI Layout: Entry Fields ---
        input_frame = tk.LabelFrame(root, text="Attribute Definition")
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Attribute Name:").pack()
        self.name_entry = tk.Entry(input_frame, width=50)
        self.name_entry.pack()

        tk.Label(input_frame, text="Default Initialization Value:").pack()
        self.default_entry = tk.Entry(input_frame, width=10)
        self.default_entry.pack()

        tk.Label(input_frame, text="Intent / Gear Scaling Logic:").pack()
        self.intent_text = tk.Text(input_frame, height=5, width=50)
        self.intent_text.pack(pady=5)

        tk.Button(input_frame, text="Add/Update Attribute", command=self.save_data, 
                  bg="#2980b9", fg="white", width=30).pack(pady=10)

        # --- UI Layout: Preview Window ---
        preview_frame = tk.LabelFrame(root, text="Current Attributes Preview")
        preview_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.preview_text = tk.Text(preview_frame, height=15, width=60, state='disabled', bg="#f0f0f0")
        self.preview_text.pack(fill="both", expand=True, padx=5, pady=5)

        self.update_preview()

    def ensure_json_exists(self):
        if not os.path.exists(self.json_path):
            with open(self.json_path, 'w') as f:
                json.dump({}, f)

    def update_preview(self):
        self.preview_text.config(state='normal')
        self.preview_text.delete("1.0", "end")
        
        self.preview_text.tag_config("key", foreground="#2980b9", font=("Consolas", 10, "bold"))
        self.preview_text.tag_config("val", foreground="#27ae60", font=("Consolas", 10))

        if not os.path.exists(self.json_path):
            self.preview_text.insert("1.0", "Error: attributes.json not found.")
        else:
            try:
                with open(self.json_path, "r") as f:
                    data = json.load(f)
                    pretty_json = json.dumps(data, indent=4)
                    for line in pretty_json.splitlines():
                        if ":" in line:
                            key, val = line.split(":", 1)
                            self.preview_text.insert("end", key + ":", "key")
                            self.preview_text.insert("end", val + "\n", "val")
                        else:
                            self.preview_text.insert("end", line + "\n")
            except (json.JSONDecodeError, IOError):
                self.preview_text.insert("end", "Error: Failed to parse attributes.json")
        
        self.preview_text.config(state='disabled')

    def save_data(self):
        name = self.name_entry.get().strip().upper()
        default_val = self.default_entry.get().strip()
        intent = self.intent_text.get("1.0", "end-1c").strip()

        if not name or not default_val:
            messagebox.showerror("Error", "Name and Default Value are required.")
            return

        with open(self.txt_path, "a") as f:
            f.write(f"ATTRIBUTE: {name}\nDEFAULT: {default_val}\nINTENT: {intent}\n" + "-"*50 + "\n\n")

        data = {}
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, "r") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = {}
        
        data[name] = {"default": default_val, "intent": intent}
        
        with open(self.json_path, "w") as f:
            json.dump(data, f, indent=4)
        
        self.update_preview()
        messagebox.showinfo("Success", f"Added {name} to library.")
        self.name_entry.delete(0, 'end')
        self.default_entry.delete(0, 'end')
        self.intent_text.delete("1.0", 'end')

if __name__ == "__main__":
    root = tk.Tk()
    app = AttributeLibApp(root)
    root.mainloop()