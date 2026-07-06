# --- AUTO-INJECTED CONFIG ---
import sys
import os
# BASE_DIR: C:\Users\Marcos Colon\Desktop\Design route\FF14 project\YAML Library\
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "Attributes"))
from attr_loader import get_full_attribute_data
# ----------------------------

import tkinter as tk
from tkinter import messagebox, ttk
import yaml

class ClassCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Class Design Suite (Regulated)")
        self.root.geometry("650x900")
        
        # Paths
        self.races_dir = os.path.join(BASE_DIR, "Races")
        self.classes_dir = os.path.join(BASE_DIR, "Classes")
        
        # Load Schema
        self.schema, self.base_data = get_full_attribute_data(__file__)

        # --- PREVIEW: FINISHED CLASSES ---
        tk.Label(root, text="Finished Classes (Race_Class.yaml Preview)", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        self.tree = ttk.Treeview(root, columns=("Race", "Class"), show="headings", height=8)
        self.tree.heading("Race", text="Race"); self.tree.heading("Class", text="Class")
        self.tree.column("Race", width=200); self.tree.column("Class", width=200)
        self.tree.pack(fill="x", padx=20, pady=5)
        self.refresh_preview()

        # --- Input Fields with Lock Toggles ---
        self.lock_race = tk.BooleanVar()
        self.lock_class = tk.BooleanVar()
        self.lock_attr = tk.BooleanVar()

        # Race Row (multi-select: pick every race this class is unlocked for,
        # one Race_Class.yaml is generated per selected race)
        frame_r = tk.Frame(root); frame_r.pack(pady=(10,0))
        tk.Label(frame_r, text="Races (racially locked — select all allowed):").pack(side="left")
        self.race_listbox = tk.Listbox(frame_r, selectmode=tk.MULTIPLE, height=6, width=40, exportselection=False)
        for race in self.get_race_options():
            self.race_listbox.insert(tk.END, race)
        self.race_listbox.pack(side="left", padx=5)
        tk.Checkbutton(frame_r, text="Lock", variable=self.lock_race).pack(side="left")

        # Class Row
        frame_c = tk.Frame(root); frame_c.pack(pady=(10,0))
        tk.Label(frame_c, text="Class (Class_Library.yaml):").pack(side="left")
        self.class_cb = ttk.Combobox(frame_c, values=self.get_class_options(), width=30, state="readonly")
        self.class_cb.pack(side="left", padx=5)
        tk.Checkbutton(frame_c, text="Lock", variable=self.lock_class).pack(side="left")

        # Attribute Row
        frame_a = tk.Frame(root); frame_a.pack(pady=(10,0))
        tk.Label(frame_a, text="Main Attribute:").pack(side="left")
        self.attr_cb = ttk.Combobox(frame_a, values=list(self.schema.keys()), width=35, state="readonly")
        self.attr_cb.pack(side="left", padx=5)
        tk.Checkbutton(frame_a, text="Lock", variable=self.lock_attr).pack(side="left")

        # Non-locked Fields
        tk.Label(root, text="Role:").pack(pady=(10,0))
        self.role_entry = tk.Entry(root, width=50); self.role_entry.pack()

        tk.Label(root, text="Narrative Intent:").pack(pady=(10,0))
        self.narr_entry = tk.Entry(root, width=60); self.narr_entry.pack()

        tk.Button(root, text="Save Race_Class.yaml", command=self.save_yaml, bg="#27ae60", fg="white", height=2, width=30).pack(pady=20)

    def get_race_options(self):
        lib_path = os.path.join(self.races_dir, "Race_Library.yaml")
        try:
            with open(lib_path, 'r') as f:
                data = yaml.safe_load(f)
                races = []
                # Monsters get race entries for NPC tagging/validation, but are
                # not valid targets for class kits, so exclude them here.
                for broad, members in data.items():
                    if broad == "Monsters": continue
                    races.extend(members)
                return races
        except Exception: return ["ERROR: Missing Races/Race_Library.yaml"]

    def get_class_options(self):
        # Look in Classes directory per image_bbc4b6.png
        lib_path = os.path.join(self.classes_dir, "Class_Library.yaml")
        try:
            with open(lib_path, 'r') as f:
                data = yaml.safe_load(f)
                all_classes = []
                for tier in data.values(): all_classes.extend(tier)
                return all_classes
        except Exception: return ["ERROR: Missing Classes/Class_Library.yaml"]

    def refresh_preview(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        if not os.path.exists(self.classes_dir): return
        
        for f in os.listdir(self.classes_dir):
            if f.endswith(".yaml") and f != "Class_Library.yaml":
                parts = f.replace(".yaml", "").split("_")
                if len(parts) >= 2:
                    self.tree.insert("", "end", values=(parts[0], parts[1]))

    def save_yaml(self):
        races = [self.race_listbox.get(i) for i in self.race_listbox.curselection()]
        cls = self.class_cb.get()
        if not races or "ERROR" in races[0] or "ERROR" in cls or not cls:
            messagebox.showerror("Error", "Select at least one Race and a Class (check library files).")
            return

        saved = []
        for race in races:
            data = {
                'Definition': {
                    'Race': race,
                    'Class': cls,
                    'MainAttribute': self.attr_cb.get(),
                    'Role': self.role_entry.get(),
                    'Intent': self.narr_entry.get()
                }
            }
            filename = os.path.join(self.classes_dir, f"{race}_{cls}.yaml")
            with open(filename, 'w') as f:
                yaml.dump(data, f, default_flow_style=False)
            saved.append(f"{race}_{cls}.yaml")

        # Post-save clearing logic based on locks
        if not self.lock_race.get(): self.race_listbox.selection_clear(0, tk.END)
        if not self.lock_class.get(): self.class_cb.set("")
        if not self.lock_attr.get(): self.attr_cb.set("")

        self.role_entry.delete(0, tk.END)
        self.narr_entry.delete(0, tk.END)

        self.refresh_preview()
        messagebox.showinfo("Success", "Saved:\n" + "\n".join(saved))

if __name__ == "__main__":
    root = tk.Tk()
    app = ClassCreatorApp(root)
    root.mainloop()