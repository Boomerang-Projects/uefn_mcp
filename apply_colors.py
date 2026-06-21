import unreal

asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
mel = unreal.MaterialEditingLibrary
sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

base_mat = unreal.EditorAssetLibrary.load_asset('/LuckyBlockPillars/Materials/M_PillarBase.M_PillarBase')
if not base_mat:
    unreal.log_error("Base material not found! Run create_color_material.py first.")
else:
    colors = [
        ("Pink",    (1.0, 0.0, 0.5)),
        ("Purple",  (0.6, 0.0, 1.0)),
        ("Blue",    (0.0, 0.4, 1.0)),
        ("Cyan",    (0.0, 1.0, 0.9)),
        ("Green",   (0.0, 1.0, 0.2)),
        ("Yellow",  (1.0, 1.0, 0.0)),
        ("Orange",  (1.0, 0.4, 0.0)),
        ("Red",     (1.0, 0.0, 0.0)),
        ("Magenta", (1.0, 0.0, 1.0)),
        ("SkyBlue", (0.0, 0.7, 1.0)),
        ("Lime",    (0.5, 1.0, 0.0)),
        ("Rose",    (1.0, 0.2, 0.5)),
        ("Indigo",  (0.2, 0.0, 1.0)),
        ("Mint",    (0.0, 1.0, 0.5)),
        ("Gold",    (1.0, 0.8, 0.0)),
        ("Violet",  (0.7, 0.0, 1.0)),
    ]

    pillars = sorted(
        [a for a in sub.get_all_level_actors() if a.get_actor_label().startswith('LB_Pillar_')],
        key=lambda a: a.get_actor_label()
    )

    mic_factory = unreal.MaterialInstanceConstantFactoryNew()
    colored = 0

    for i, actor in enumerate(pillars):
        comp = actor.get_components_by_class(unreal.StaticMeshComponent)
        if not comp:
            continue

        color_name, (r, g, b) = colors[i % len(colors)]
        mic_name = f'MI_Pillar_{color_name}'
        mic_path = f'/LuckyBlockPillars/Materials/{mic_name}'

        if unreal.EditorAssetLibrary.does_asset_exist(mic_path + '.' + mic_name):
            mic = unreal.EditorAssetLibrary.load_asset(mic_path)
        else:
            mic = asset_tools.create_asset(mic_name, '/LuckyBlockPillars/Materials', unreal.MaterialInstanceConstant, mic_factory)
            mel.set_material_instance_parent(mic, base_mat)

        mel.set_material_instance_vector_parameter_value(mic, 'Color', unreal.LinearColor(r, g, b, 1.0))
        unreal.EditorAssetLibrary.save_asset(mic_path)

        comp[0].set_material(0, mic)
        colored += 1
        unreal.log(f"Pillar {i}: {color_name} ({r},{g},{b})")

    unreal.log(f"Done! Colored {colored} pillars")
