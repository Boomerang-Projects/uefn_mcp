import unreal

sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
spacing = 2048
half = 4096

# Get Z from a correctly-placed pillar (not the moved one)
ref_z = 0
for a in sub.get_all_level_actors():
    lbl = a.get_actor_label()
    if lbl.startswith('LB_Pillar_') and lbl != 'LB_Pillar_3_0':
        parts = lbl.split('_')
        if len(parts) == 4:
            ref_z = a.get_actor_location().z
            break

unreal.log(f"Reference Z: {ref_z}")

fixed = 0
for a in sub.get_all_level_actors():
    lbl = a.get_actor_label()
    if not lbl.startswith('LB_Pillar_'):
        continue
    parts = lbl.split('_')
    if len(parts) != 4:
        continue
    try:
        row = int(parts[2])
        col = int(parts[3])
    except:
        continue
    correct_x = -half + col * spacing
    correct_y = -half + row * spacing
    current = a.get_actor_location()
    if abs(current.x - correct_x) > 1 or abs(current.y - correct_y) > 1 or abs(current.z - ref_z) > 1:
        a.set_actor_location(unreal.Vector(correct_x, correct_y, ref_z), False, False)
        unreal.log(f"Fixed {lbl}: ({current.x:.0f},{current.y:.0f},{current.z:.0f}) -> ({correct_x},{correct_y},{ref_z})")
        fixed += 1

unreal.log(f"Snapped {fixed} pillar(s) to correct grid positions")
