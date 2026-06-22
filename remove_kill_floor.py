import unreal

sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

removed = 0
for actor in sub.get_all_level_actors():
    if actor.get_actor_label() == "LB_KillFloor":
        actor.destroy_actor()
        removed += 1

unreal.log(f"Removed {removed} kill floor actor(s)")
