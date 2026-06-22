import unreal

# Place a large flat Kill Volume just below the pillar bases (Z=0)
# Covers the full arena: pillars span -4096 to +4096

world = unreal.EditorLevelLibrary.get_editor_world()
sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

# Try to spawn a KillZVolume (built-in Unreal kill volume)
kill_class = unreal.KillZVolume

location = unreal.Vector(0, 0, -50)    # just below pillar bases at Z=0
rotation = unreal.Rotator(0, 0, 0)

actor = unreal.EditorLevelLibrary.spawn_actor_from_class(kill_class, location, rotation)

if actor:
    actor.set_actor_label("LB_KillFloor")
    # Scale it: X/Y cover the arena (10000 units wide), Z is thin (100 units)
    actor.set_actor_scale3d(unreal.Vector(100, 100, 1))
    unreal.log("Kill floor placed at Z=-300, scale 100x100x1")
else:
    unreal.log_error("Failed to spawn KillZVolume — try placing a Damage Volume manually from UEFN UI")
