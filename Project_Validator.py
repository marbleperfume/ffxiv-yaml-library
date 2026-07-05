import os
import yaml
import glob

def validate_project():
    print("--- Running Data Integrity Check ---")
    
    # 1. Load all available IDs
    class_list = [os.path.basename(f).replace(".yaml", "") for f in glob.glob("Classes/*.yaml")]
    race_list = [os.path.basename(f).replace(".yaml", "") for f in glob.glob("Races/*.yaml")]
    condition_list = [os.path.basename(f).replace(".yaml", "") for f in glob.glob("Conditions/*.yaml")]
    
    # 2. Check NPC Dependencies
    for npc_file in glob.glob("NPCs/*.yaml"):
        with open(npc_file, 'r') as f:
            data = yaml.safe_load(f)
            
        race_ref = data.get('Identity', {}).get('Race')
        class_ref = data.get('Identity', {}).get('Class')
        
        if race_ref and race_ref not in race_list:
            print(f"[ERROR] NPC {npc_file} references missing Race: {race_ref}")
        if class_ref and class_ref not in class_list:
            print(f"[ERROR] NPC {npc_file} references missing Class: {class_ref}")

    # 3. Check Equipment Dependencies
    for eq_file in glob.glob("Equipment/*.yaml"):
        with open(eq_file, 'r') as f:
            data = yaml.safe_load(f)
        # Add logic here to check if Attributes exist in Attribute_Library.txt
        # etc...

    print("--- Integrity Check Complete ---")

if __name__ == "__main__":
    validate_project()