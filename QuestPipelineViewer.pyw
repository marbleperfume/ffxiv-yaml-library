import tkinter as tk
from tkinter import ttk
import yaml, os, glob

class QuestPipelineViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pipeline Flow Visualizer")
        self.root.geometry("600x600")

        # Treeview to display the hierarchy
        self.tree = ttk.Treeview(root, columns=("Index", "Intent"), show="tree headings")
        self.tree.heading("#0", text="Pipeline / Quest ID")
        self.tree.heading("Index", text="Index")
        self.tree.heading("Intent", text="Narrative Intent")
        self.tree.column("Index", width=50)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Button(root, text="Refresh Pipelines", command=self.load_data).pack(pady=10)
        self.load_data()

    def load_data(self):
        # Clear existing
        for i in self.tree.get_children(): self.tree.delete(i)
        
        pipelines = {}
        for f in glob.glob("Quests/*.yaml"):
            with open(f, 'r') as file:
                data = yaml.safe_load(file)
                pid = data['PipelineID']
                if pid not in pipelines: pipelines[pid] = []
                pipelines[pid].append((data['SequenceIndex'], os.path.basename(f), data.get('NarrativeIntent', '')))

        # Sort and populate
        for pid in sorted(pipelines.keys()):
            node = self.tree.insert("", "end", text=pid, open=True)
            for idx, name, intent in sorted(pipelines[pid]):
                self.tree.insert(node, "end", text=name, values=(idx, intent))

if __name__ == "__main__":
    root = tk.Tk()
    app = QuestPipelineViewer(root)
    root.mainloop()