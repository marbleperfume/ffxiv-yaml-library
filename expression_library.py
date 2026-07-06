import tkinter as tk
import os

_EXPR_DIR = os.path.dirname(os.path.abspath(__file__))


def get_expression_library():
    path = os.path.join(_EXPR_DIR, "Expressions", "expression_library.txt")
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return sorted([line.strip() for line in f if line.strip()])


def add_to_expression_library(new_expr):
    if not os.path.exists(os.path.join(_EXPR_DIR, "Expressions")):
        os.makedirs(os.path.join(_EXPR_DIR, "Expressions"))
    exprs = get_expression_library()
    if new_expr and new_expr not in exprs:
        with open(os.path.join(_EXPR_DIR, "Expressions", "expression_library.txt"), "a") as f:
            f.write(new_expr + "\n")


class ExpressionSelectorModal:
    def __init__(self, parent, callback):
        self.modal = tk.Toplevel(parent)
        self.modal.title("Select Expression Tag")
        self.modal.geometry("300x400")
        self.callback = callback

        tk.Label(self.modal, text="Select an Expression:").pack(pady=5)
        self.listbox = tk.Listbox(self.modal, height=15, exportselection=False)
        self.listbox.pack(fill="both", expand=True, padx=10)

        for expr in get_expression_library():
            self.listbox.insert(tk.END, expr)

        tk.Button(self.modal, text="Insert Selected", command=self.submit).pack(pady=10)

    def submit(self):
        selection = self.listbox.curselection()
        if selection:
            self.callback(self.listbox.get(selection[0]))
        self.modal.destroy()
