import unreal

sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
world = unreal.EditorLevelLibrary.get_editor_world()

template = next((a for a in sub.get_all_level_actors() if a.get_actor_label().startswith('LB_Pillar_')), None)
if not template:
    unreal.log_error("No LB_Pillar found to use as template")
else:
    template.set_actor_label('LB_Pillar_TEMPLATE')
    template.set_actor_location(unreal.Vector(99999, 99999, 0), False, False)

    for a in sub.get_all_level_actors():
        lbl = a.get_actor_label()
        if lbl.startswith('LB_Pillar_') and lbl != 'LB_Pillar_TEMPLATE':
            a.destroy_actor()

    spacing = 2048  # 4 tiles center-to-center (1 tile pillar + 3 tiles gap)
    grid = 5
    half = (grid - 1) * spacing // 2  # 4096

    placed = 0
    for row in range(grid):
        for col in range(grid):
            if row == 0 or row == grid-1 or col == 0 or col == grid-1:
                x = -half + col * spacing
                y = -half + row * spacing
                dupes = sub.duplicate_actors([template], world)
                if dupes:
                    dupes[0].set_actor_location(unreal.Vector(x, y, 0), False, False)
                    dupes[0].set_actor_label('LB_Pillar_' + str(row) + '_' + str(col))
                    placed += 1

    template.destroy_actor()
    unreal.log("Placed " + str(placed) + " pillars | spacing 2048 | positions: -4096 to 4096")
