import json
import os
import yaml # Ensure you have PyYAML installed

def get_full_attribute_data(caller_file):
    """
    Fetches the schema from JSON and the base character values from YAML.
    Now looks for both files inside the 'Attributes' folder.
    """
    script_dir = os.path.dirname(os.path.abspath(caller_file))
    attr_dir = os.path.join(script_dir, "Attributes")
    
    # Paths - both are now inside the Attributes directory
    json_path = os.path.join(attr_dir, "attributes.json")
    yaml_path = os.path.join(attr_dir, "Base_Attributes.yaml")
    
    # 1. Load Schema (JSON)
    schema = {}
    if os.path.exists(json_path):
        try:
            with open(json_path, "r") as f:
                schema = json.load(f)
        except: pass

    # 2. Load Base Data (YAML)
    base_data = {}
    if os.path.exists(yaml_path):
        try:
            with open(yaml_path, "r") as f:
                data = yaml.safe_load(f)
                # Extract the 'Attributes' section specifically
                if data and 'Base_Character' in data:
                    base_data = data['Base_Character'].get('Attributes', {})
        except: pass
        
    return schema, base_data