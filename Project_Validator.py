import os
import yaml
import glob

errors = []

def err(msg):
    errors.append(msg)
    print(f"[ERROR] {msg}")

def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f) or {}

def get_race_library():
    """Flattened subrace list from Races/Race_Library.yaml (all categories,
    including Monsters -- NPCs may legally carry monster races)."""
    path = os.path.join("Races", "Race_Library.yaml")
    if not os.path.exists(path): return []
    races = []
    for members in load_yaml(path).values():
        if isinstance(members, list):
            races.extend(members)
    return races

def get_zone_keys():
    """Region + Town keys from Zones/Zone_Library.yaml, for Location checks."""
    path = os.path.join("Zones", "Zone_Library.yaml")
    if not os.path.exists(path): return set()
    data = load_yaml(path)
    keys = set()
    for section in ("Regions", "Towns"):
        keys.update((data.get(section) or {}).keys())
    return keys

def get_enhancement_keys():
    """Key field from every Enhancements/*.yaml file."""
    keys = set()
    for f in glob.glob("Enhancements/*.yaml"):
        try:
            data = load_yaml(f)
        except Exception:
            continue
        if data.get('Key'):
            keys.add(data['Key'])
    return keys

def get_skill_registry():
    """Key -> parsed data for every Skills/*.yaml file."""
    registry = {}
    for f in glob.glob("Skills/*.yaml"):
        try:
            data = load_yaml(f)
        except Exception:
            continue
        if data.get('Key'):
            registry[data['Key']] = data
    return registry

def check_race_bonus_skills(skill_registry):
    """Every Race BonusSkills entry must resolve to a real Skill, and if that
    skill declares RaceRestrictions, the granting race must be on the list --
    a race shouldn't be handed a skill its own restrictions forbid it."""
    for f in glob.glob("Races/*.yaml"):
        if os.path.basename(f) == "Race_Library.yaml": continue
        try:
            data = load_yaml(f)
        except Exception as e:
            err(f"{f}: unparseable YAML ({e})")
            continue
        definition = data.get('Definition') or {}
        subrace = definition.get('Subrace')
        for skill_key in (definition.get('BonusSkills') or []):
            if skill_key not in skill_registry:
                err(f"{f} BonusSkills references missing Skill: {skill_key}")
                continue
            race_restrictions = skill_registry[skill_key].get('RaceRestrictions')
            if race_restrictions and subrace and subrace not in race_restrictions:
                err(f"{f} grants '{skill_key}' as a BonusSkill, but that skill's "
                    f"RaceRestrictions {race_restrictions} doesn't include '{subrace}'")

def check_region_enhancements(zone_data):
    """Every Region.Enhancement.TrackRef must resolve to a real Enhancements/*.yaml Key."""
    enhancement_keys = get_enhancement_keys()
    for region_name, region in (zone_data.get('Regions') or {}).items():
        if not isinstance(region, dict): continue
        enhancement = region.get('Enhancement')
        if not enhancement: continue
        track_ref = enhancement.get('TrackRef')
        if not track_ref:
            err(f"Zones/Zone_Library.yaml Region '{region_name}' declares Enhancement without a TrackRef")
        elif track_ref not in enhancement_keys:
            err(f"Zones/Zone_Library.yaml Region '{region_name}' TrackRef '{track_ref}' "
                "not found in Enhancements/*.yaml")

def check_rank_profile(npc_file, profile):
    """Enforces the contract in Ranks/Rank_System.yaml: required Rank1/Level1,
    valid Inherit chains, LoreSource on every KnowledgeCheck."""
    mercenary = profile.get('Mercenary') or {}
    if not mercenary.get('Rank1'):
        err(f"{npc_file}: RankProfile.Mercenary.Rank1 is required (default pattern)")

    doctrine = profile.get('Doctrine') or {}
    if not doctrine.get('Level1'):
        err(f"{npc_file}: RankProfile.Doctrine.Level1 is required (default pattern)")

    tier_order = ["Level1", "Level2", "Level3"]
    for tier_name, tier in doctrine.items():
        if not isinstance(tier, dict): continue

        inherit = tier.get('Inherit')
        if inherit is not None:
            if inherit not in doctrine:
                err(f"{npc_file}: Doctrine.{tier_name} inherits '{inherit}' which is not defined")
            elif inherit not in tier_order or tier_name not in tier_order:
                err(f"{npc_file}: Doctrine.{tier_name} inherit '{inherit}' is not a known tier name")
            elif tier_order.index(inherit) >= tier_order.index(tier_name):
                err(f"{npc_file}: Doctrine.{tier_name} must inherit a LOWER tier, not '{inherit}'")

        for kc in (tier.get('KnowledgeChecks') or []):
            if not isinstance(kc, dict) or not kc.get('LoreSource'):
                mech = kc.get('Mechanic', '?') if isinstance(kc, dict) else kc
                err(f"{npc_file}: Doctrine.{tier_name} KnowledgeCheck '{mech}' has no LoreSource "
                    "(external-knowledge checks must be a declared, deliberate choice)")

def validate_project():
    print("--- Running Data Integrity Check ---")

    class_list = [os.path.basename(f).replace(".yaml", "") for f in glob.glob("Classes/*.yaml")]
    race_specs = [os.path.basename(f).replace(".yaml", "") for f in glob.glob("Races/*.yaml")]
    race_library = get_race_library()
    zone_keys = get_zone_keys()

    zone_lib_path = os.path.join("Zones", "Zone_Library.yaml")
    if os.path.exists(zone_lib_path):
        check_region_enhancements(load_yaml(zone_lib_path))

    check_race_bonus_skills(get_skill_registry())

    for npc_file in glob.glob("NPCs/**/*.yaml", recursive=True):
        try:
            data = load_yaml(npc_file)
        except Exception as e:
            err(f"{npc_file}: unparseable YAML ({e})")
            continue

        # Legacy Identity.Race/Class refs (file-name based specs)
        race_ref = data.get('Identity', {}).get('Race')
        class_ref = data.get('Identity', {}).get('Class')
        if race_ref and race_ref not in race_specs:
            err(f"{npc_file} references missing Race spec: {race_ref}")
        if class_ref and class_ref not in class_list:
            err(f"{npc_file} references missing Class: {class_ref}")

        # RaceKey against the race library (includes Monsters category)
        race_key = data.get('RaceKey')
        if race_key and race_library and race_key not in race_library:
            err(f"{npc_file} RaceKey '{race_key}' not in Races/Race_Library.yaml")

        # Location zone segment against Zone_Library Regions/Towns
        location = data.get('Location')
        if isinstance(location, str) and location.startswith("Zone."):
            parts = location.split(".")
            if len(parts) > 1 and zone_keys and parts[1] not in zone_keys:
                err(f"{npc_file} Location '{location}' references unknown zone '{parts[1]}'")

        # Rank pipeline contract
        if 'RankProfile' in data:
            check_rank_profile(npc_file, data['RankProfile'] or {})
        if 'RankScaling' in data:
            err(f"{npc_file} uses legacy 'RankScaling' -- migrate to 'RankProfile' "
                "(see Ranks/Rank_System.yaml)")

    print("--- Integrity Check Complete ---")
    if errors:
        print(f"FAILED: {len(errors)} error(s).")
    else:
        print("PASSED: no integrity errors.")
    return len(errors)

if __name__ == "__main__":
    raise SystemExit(1 if validate_project() else 0)
