import sys
import os
import yaml
import json # Added this
from PyQt6.QtWidgets import (QApplication, QMainWindow, QDockWidget,
                             QTabWidget, QWidget, QVBoxLayout, QFormLayout,
                             QLabel, QTreeView, QListWidget, QLineEdit,
                             QScrollArea, QGroupBox, QMessageBox, QInputDialog, QDialog,
                             QHBoxLayout, QPushButton, QAbstractItemView, QSizePolicy,
                             QFileDialog) # Added these
from PyQt6.QtGui import QAction, QFileSystemModel
from PyQt6.QtCore import Qt, QDir

# Target the project directory this script lives in
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

class TagPickerDialog(QDialog):
    def __init__(self, current_tags, available_tags, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Assign Linkages (Tags / Keys)")
        self.setMinimumSize(400, 500)
        
        self.layout = QVBoxLayout(self)
        
        # Search filter
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search for tags or keys...")
        self.search_bar.textChanged.connect(self.filter_list)
        self.layout.addWidget(self.search_bar)
        
        # Multi-select list
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.layout.addWidget(self.list_widget)
        
        # Populate the list and highlight already selected items
        for tag in sorted(available_tags):
            item = self.list_widget.addItem(tag)
            
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.text() in current_tags:
                item.setSelected(True)
                
        # Buttons
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Apply Linkages")
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        self.layout.addLayout(btn_layout)

    def filter_list(self, text):
        """Hides items that don't match the search text."""
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    def get_selected_tags(self):
        """Returns a list of strings currently selected."""
        return [item.text() for item in self.list_widget.selectedItems()]
        
class YamlEditorTab(QWidget):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.yaml_data = {}
        self.relational_keys = []
        
        self.layout = QVBoxLayout(self)
        
        # --- NEW BUTTON LAYOUT ---
        btn_layout = QHBoxLayout()
        
        self.add_prop_btn = QPushButton("Add New Property")
        self.add_prop_btn.clicked.connect(self.add_new_property)
        
        self.save_btn = QPushButton("💾 Save File")
        self.save_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.save_btn.clicked.connect(self.save_file)
        
        btn_layout.addWidget(self.add_prop_btn)
        btn_layout.addWidget(self.save_btn)
        self.layout.addLayout(btn_layout)
        # -------------------------
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.form_layout = QFormLayout(self.scroll_content)
        
        self.load_yaml()
        
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)

    def load_yaml(self):
        try:
            with open(self.file_path, 'r') as f:
                self.yaml_data = yaml.safe_load(f) or {}
            self.refresh_form()
            self.extract_relations()
        except Exception as e:
            self.form_layout.addRow(QLabel(f"Error loading YAML:\n{str(e)}"))

    def add_new_property(self):
        key_name, ok = QInputDialog.getText(self, "Add Property", "Enter new key name:")
        if ok and key_name:
            if key_name not in self.yaml_data:
                self.yaml_data[key_name] = "" 
                self.refresh_form()
            else:
                QMessageBox.warning(self, "Error", "Property already exists.")

    def refresh_form(self):
        while self.form_layout.count():
            child = self.form_layout.takeAt(0)
            if child.widget(): child.widget().deleteLater()
        self.build_form("", self.yaml_data, self.form_layout)

    def build_form(self, prefix, data, layout):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    group_box = QGroupBox(key)
                    group_layout = QFormLayout()
                    self.build_form(f"{prefix}{key}.", value, group_layout)
                    group_box.setLayout(group_layout)
                    layout.addRow(group_box)
                elif isinstance(value, list):
                    list_layout = QHBoxLayout()
                    list_layout.setContentsMargins(0, 0, 0, 0)
                    
                    str_value = ", ".join(str(v) for v in value)
                    line_edit = QLineEdit(str_value)
                    
                    # Fix for image_f0d2a1.png: Force expanding policy
                    line_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                    
                    line_edit.textChanged.connect(lambda t, k=key: self.yaml_data.update({k: [x.strip() for x in t.split(",") if x.strip()]}))
                    
                    pick_btn = QPushButton("🔍 Pick")
                    pick_btn.setFixedWidth(60)
                    pick_btn.clicked.connect(lambda checked, le=line_edit: self.open_tag_picker(le))
                    
                    list_layout.addWidget(line_edit)
                    list_layout.addWidget(pick_btn)
                    layout.addRow(QLabel(key + " (List):"), list_layout)
                else:
                    line_edit = QLineEdit(str(value))
                    line_edit.textChanged.connect(lambda t, k=key: self.yaml_data.update({k: t}))
                    layout.addRow(QLabel(key + ":"), line_edit)

    def open_tag_picker(self, line_edit_widget):
        current_tags = [t.strip() for t in line_edit_widget.text().split(",") if t.strip()]
        available_tags = self.window().get_global_registry() if hasattr(self.window(), 'get_global_registry') else []
        dialog = TagPickerDialog(current_tags, available_tags, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            line_edit_widget.setText(", ".join(dialog.get_selected_tags()))

    def extract_relations(self):
        self.relational_keys.clear()
        def scan(data):
            if isinstance(data, dict):
                for k, v in data.items():
                    if k in ["Tags", "AssignedSkills", "LootRegistry", "Actors", "EquippedAttire", "Titles", "Passives"]:
                        if isinstance(v, list):
                            for item in v:
                                if isinstance(item, str): self.relational_keys.append(item)
                                elif isinstance(item, dict) and "ItemKey" in item: self.relational_keys.append(item["ItemKey"])
                    scan(v)
            elif isinstance(data, list):
                for v in data: scan(v)
        scan(self.yaml_data)

    def save_file(self):
        try:
            with open(self.file_path, 'w') as f:
                yaml.dump(self.yaml_data, f, default_flow_style=False, sort_keys=False)
            self.extract_relations()
            QMessageBox.information(self, "Success", "File saved successfully.")
            return True
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Could not save file:\n{str(e)}")
            return False


class UnifiedDesignHub(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unified RPG Design Hub (UE5 Relational Data)")
        self.setGeometry(100, 100, 1200, 800)
        
        self.setup_menu()
        self.setup_central_workspace()
        self.setup_left_dock()
        self.setup_right_dock()
        
    def get_global_registry(self):
        """Scans the project library to build a live list of valid Keys."""
        registry = set()
        
        if os.path.exists(PROJECT_DIR):
            for root, dirs, files in os.walk(PROJECT_DIR):
                for file in files:
                    if file.endswith((".yaml", ".yml")):
                        # Treat the filename (minus extension) as a valid key
                        base_key = os.path.splitext(file)[0]
                        registry.add(base_key)
                        
                        # Optionally: You could also parse the files here to extract inner tags, 
                        # but for performance, matching filenames to UE5 GameplayTags is highly efficient.
                        
        return list(registry)

    def setup_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New YAML Spec", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.create_new_yaml)
        
        save_action = QAction("Save Current Tab", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_current_tab)
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        
        file_menu.addAction(new_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

    def setup_central_workspace(self):
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_relational_inspector)
        self.setCentralWidget(self.tabs)

    def close_tab(self, index):
        self.tabs.removeTab(index)

    def setup_left_dock(self):
        left_dock = QDockWidget("Project Explorer", self)
        left_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        
        self.project_tree = QTreeView()
        self.file_model = QFileSystemModel()
        root_path = PROJECT_DIR if os.path.exists(PROJECT_DIR) else QDir.currentPath()
        self.file_model.setRootPath(root_path)
        
        self.file_model.setNameFilters(["*.yaml", "*.yml"])
        self.file_model.setNameFilterDisables(False)
        self.file_model.setFilter(QDir.Filter.AllDirs | QDir.Filter.NoDotAndDotDot | QDir.Filter.Files)

        self.project_tree.setModel(self.file_model)
        self.project_tree.setRootIndex(self.file_model.index(root_path))
        
        self.project_tree.setColumnHidden(1, True); self.project_tree.setColumnHidden(2, True); self.project_tree.setColumnHidden(3, True)
        self.project_tree.setHeaderHidden(True)
        self.project_tree.doubleClicked.connect(self.on_tree_double_click)
        
        dock_widget = QWidget(); layout = QVBoxLayout(); layout.setContentsMargins(2, 2, 2, 2); layout.addWidget(self.project_tree); dock_widget.setLayout(layout)
        left_dock.setWidget(dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, left_dock)

    def on_tree_double_click(self, index):
        file_path = self.file_model.filePath(index)
        if os.path.isfile(file_path):
            file_name = os.path.basename(file_path)
            for i in range(self.tabs.count()):
                if self.tabs.tabText(i) == file_name:
                    self.tabs.setCurrentIndex(i)
                    return
            editor = YamlEditorTab(file_path)
            self.tabs.addTab(editor, file_name)
            self.tabs.setCurrentIndex(self.tabs.count() - 1)

    def setup_right_dock(self):
        right_dock = QDockWidget("Relational Inspector", self)
        self.relationship_list = QListWidget()
        self.relationship_list.addItem("No active file.")
        
        dock_widget = QWidget(); layout = QVBoxLayout(); layout.addWidget(QLabel("Active Tag Linkages:")); layout.addWidget(self.relationship_list); dock_widget.setLayout(layout)
        right_dock.setWidget(dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, right_dock)

    def update_relational_inspector(self, index):
        self.relationship_list.clear()
        if index == -1:
            self.relationship_list.addItem("No active file.")
            return
        current_widget = self.tabs.widget(index)
        if isinstance(current_widget, YamlEditorTab):
            if current_widget.relational_keys:
                for key in current_widget.relational_keys: self.relationship_list.addItem(key)
            else: self.relationship_list.addItem("No outgoing string linkages found.")

    def save_current_tab(self):
        """Triggers the save function on the currently open YamlEditorTab."""
        index = self.tabs.currentIndex()
        if index != -1:
            current_widget = self.tabs.widget(index)
            if isinstance(current_widget, YamlEditorTab):
                if current_widget.save_file():
                    self.statusBar().showMessage(f"Saved {self.tabs.tabText(index)} successfully.", 3000)
                    self.update_relational_inspector(index)

    def create_new_yaml(self):
        categories = ["Classes", "Conditions", "Items", "NPCs", "Passives", "Skills"]
        # The 'True' flag at the end makes this input box editable
        category, ok = QInputDialog.getItem(self, "New YAML Spec", "Select or Type Category:", categories, 0, True)
        
        if ok and category:
            name, ok_name = QInputDialog.getText(self, "New YAML Spec", f"Enter Key/Name for new {category} (e.g., Skill.Combat.Strike):")
            if ok_name and name:
                target_dir = os.path.join(PROJECT_DIR, category)
                if not os.path.exists(target_dir): os.makedirs(target_dir)
                file_path = os.path.join(target_dir, f"{name}.yaml")
                
                template_data = {"Key": name, "Name": name.split(".")[-1], "Tags": [f"Tag.{category}.General"], "Definition": {}}
                
                try:
                    with open(file_path, 'w') as f:
                        yaml.dump(template_data, f, default_flow_style=False, sort_keys=False)
                    self.statusBar().showMessage(f"Created {name}.yaml", 3000)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Could not create file:\n{str(e)}")

    def export_project_relationships(self):
        """
        Scans all YAML files in the library and builds a lightweight JSON map 
        of Name/Key relationships for LLM context and UE5 tag validation.
        """
        if not os.path.exists(PROJECT_DIR):
            QMessageBox.warning(self, "Export Failed", f"Project directory not found:\n{PROJECT_DIR}")
            return
            
        unified_schema = {
            "Races": {}, "Classes": {}, "Skills": {}, "Characters": {},
            "NPCs": {}, "Items": {}, "Conditions": {}, "Passives": {}
        }
        
        # Walk through the entire YAML Library directory
        for root, dirs, files in os.walk(PROJECT_DIR):
            for file in files:
                if file.endswith((".yaml", ".yml")):
                    filepath = os.path.join(root, file)
                    category = os.path.basename(root) # e.g., "Skills", "NPCs"
                    
                    try:
                        with open(filepath, 'r') as f:
                            data = yaml.safe_load(f)
                            
                        if not data or "Key" not in data:
                            continue # Skip invalid files
                            
                        # Extract only relational/functional data, strip heavy text strings
                        key = data["Key"]
                        lightweight_entry = {
                            "Tags": data.get("Tags", []),
                        }
                        
                        # Grab specific functional bindings based on what exists in the file
                        if "AssignedSkills" in data: lightweight_entry["AssignedSkills"] = data["AssignedSkills"]
                        if "LootRegistry" in data: lightweight_entry["LootRegistry"] = [item.get("ItemKey") for item in data["LootRegistry"] if isinstance(item, dict)]
                        if "Actors" in data: lightweight_entry["Actors"] = data["Actors"]
                        if "EquippedAttire" in data: lightweight_entry["EquippedAttire"] = data["EquippedAttire"]
                        if "Titles" in data: lightweight_entry["Titles"] = data["Titles"]
                        if "Passives" in data: lightweight_entry["Passives"] = data["Passives"]
                        
                        # Add to the appropriate category in our master map
                        if category in unified_schema:
                            unified_schema[category][key] = lightweight_entry
                        else:
                            # If it's a new subfolder we didn't explicitly track, catch it
                            unified_schema[category] = {key: lightweight_entry}
                            
                    except Exception as e:
                        print(f"Failed to parse {file} during export: {e}")

        # Save the result
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Project Context", os.path.join(PROJECT_DIR, "Project_Relationships.json"), "JSON Files (*.json)")
        
        if save_path:
            try:
                with open(save_path, 'w') as f:
                    json.dump(unified_schema, f, indent=2)
                self.statusBar().showMessage("Project successfully exported to JSON.", 5000)
                QMessageBox.information(self, "Export Complete", "LLM Context Map generated successfully. You can now provide this JSON file to an AI to give it complete visibility of your game's data structure.")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Failed to save JSON:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = UnifiedDesignHub()
    window.show()
    sys.exit(app.exec())