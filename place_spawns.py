import unreal

sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
world = unreal.EditorLevelLibrary.get_editor_world()
actors = sub.get_all_level_actors()

# Delete all existing spawn points
removed = 0
for a in actors:
    cls = a.get_class().get_name()
    lbl = a.get_actor_label().lower()
    if 'playerstart' in cls.lower() or 'spawnpad' in cls.lower() or 'spawn' in lbl:
        a.destroy_actor()
        removed += 1
unreal.log(f"Removed {removed} existing spawn points")

# Get pillars and their top Z from bounds
pillars = [a for a in sub.get_all_level_actors() if a.get_actor_label().startswith('LB_Pillar_')]
if not pillars:
    unreal.log_error("No pillars found!")
else:
    # Get top Z from first pillar bounds
    sample = pillars[0]
    bounds = sample.get_actor_bounds(False)
    origin_z = bounds[0].z
    extent_z = bounds[1].z
    top_z = origin_z + extent_z
    unreal.log(f"Pillar top Z: {top_z:.1f} (origin:{origin_z:.1f} extent:{extent_z:.1f})")

    placed = 0
    for pillar in pillars:
        loc = pillar.get_actor_location()
        spawn_loc = unreal.Vector(loc.x, loc.y, top_z)
        spawn = sub.spawn_actor_from_class(unreal.PlayerStart, spawn_loc)
        if spawn:
            spawn.set_actor_label(f"SpawnPad_{pillar.get_actor_label()}")
            placed += 1

    unreal.log(f"Placed {placed} spawn points at Z={top_z:.1f}")
