import tkinter as tk
import os

_TAGS_DIR = os.path.dirname(os.path.abspath(__file__))


def get_tag_library():
    path = os.path.join(_TAGS_DIR, "tags", "tag_library.txt")
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return sorted([line.strip() for line in f if line.strip()])


def add_to_tag_library(new_tag):
    if not os.path.exists(os.path.join(_TAGS_DIR, "tags")):
        os.makedirs(os.path.join(_TAGS_DIR, "tags"))
    tags = get_tag_library()
    if new_tag and new_tag not in tags:
        with open(os.path.join(_TAGS_DIR, "tags", "tag_library.txt"), "a") as f:
            f.write(new_tag + "\n")


class TagSelectorModal:
    def __init__(self, parent, callback):
        self.modal = tk.Toplevel(parent)
        self.modal.title("Select Existing Tags")
        self.modal.geometry("300x400")
        self.callback = callback

        tk.Label(self.modal, text="Select Tags to Add:").pack(pady=5)
        self.listbox = tk.Listbox(self.modal, selectmode=tk.MULTIPLE, height=15)
        self.listbox.pack(fill="both", expand=True, padx=10)

        for tag in get_tag_library():
            self.listbox.insert(tk.END, tag)

        tk.Button(self.modal, text="Add Selected", command=self.submit).pack(pady=10)

    def submit(self):
        selected = [self.listbox.get(i) for i in self.listbox.curselection()]
        self.callback(selected)
        self.modal.destroy()
