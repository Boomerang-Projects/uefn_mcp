import unreal

sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

colors = [
    (1.0, 0.0, 0.5),    # Hot Pink
    (0.6, 0.0, 1.0),    # Purple
    (0.0, 0.4, 1.0),    # Blue
    (0.0, 1.0, 0.8),    # Cyan
    (0.0, 1.0, 0.2),    # Green
    (1.0, 1.0, 0.0),    # Yellow
    (1.0, 0.5, 0.0),    # Orange
    (1.0, 0.0, 0.0),    # Red
    (1.0, 0.0, 1.0),    # Magenta
    (0.0, 0.8, 1.0),    # Sky Blue
    (0.5, 1.0, 0.0),    # Lime
    (1.0, 0.2, 0.6),    # Rose
    (0.2, 0.0, 1.0),    # Indigo
    (0.0, 1.0, 0.5),    # Mint
    (1.0, 0.8, 0.0),    # Gold
    (0.8, 0.0, 1.0),    # Violet
]

pillars = sorted(
    [a for a in sub.get_all_level_actors() if a.get_actor_label().startswith('LB_Pillar_')],
    key=lambda a: a.get_actor_label()
)

colored = 0
for i, actor in enumerate(pillars):
    comp = actor.get_components_by_class(unreal.StaticMeshComponent)
    if not comp:
        continue
    c = comp[0]
    r, g, b = colors[i % len(colors)]
    dmi = unreal.KismetMaterialLibrary.create_dynamic_material_instance(actor, c.get_material(0))
    if dmi:
        # Try common parameter names
        for param in ["Color", "BaseColor", "Tint", "ColorTint", "DiffuseColor"]:
            try:
                dmi.set_vector_parameter_value(param, unreal.LinearColor(r, g, b, 1.0))
            except:
                pass
        c.set_material(0, dmi)
        colored += 1

unreal.log(f"Applied dynamic materials to {colored} pillars")
