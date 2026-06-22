import unreal

sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

# Find the Mutator Zone
mz = next((a for a in sub.get_all_level_actors() if a.get_actor_label() == "Mutator Zone"), None)

if mz:
    # Center it at 0,0 and place just below pillar base (Z=-100)
    mz.set_actor_location(unreal.Vector(0, 0, -100), False, False)
    # Scale to cover entire arena: pillars go from -4096 to +4096
    # Zone Width/Depth/Height are in the device settings, but we can scale the actor
    # Scale of 100 = 10000 units wide (covers -5000 to +5000)
    mz.set_actor_scale3d(unreal.Vector(100, 100, 1))
    unreal.log("Mutator Zone positioned: Location(0,0,-100), Scale(100,100,1)")
else:
    unreal.log_error("Mutator Zone not found in level")
