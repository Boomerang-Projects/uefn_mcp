import unreal

asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
mel = unreal.MaterialEditingLibrary
sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

base_mat = unreal.EditorAssetLibrary.load_asset('/LuckyBlockPillars/Materials/M_PillarBase.M_PillarBase')
if not base_mat:
    unreal.log_error("Base material not found! Run create_color_material.py first.")
else:
    colors = [
        ("Pink",    (0.85, 0.25, 0.45)),
        ("Purple",  (0.45, 0.10, 0.75)),
        ("Blue",    (0.10, 0.30, 0.80)),
        ("Cyan",    (0.10, 0.65, 0.75)),
        ("Green",   (0.10, 0.65, 0.25)),
        ("Yellow",  (0.85, 0.80, 0.10)),
        ("Orange",  (0.85, 0.40, 0.05)),
        ("Red",     (0.80, 0.10, 0.10)),
        ("Magenta", (0.80, 0.10, 0.70)),
        ("SkyBlue", (0.15, 0.55, 0.80)),
        ("Lime",    (0.45, 0.75, 0.10)),
        ("Rose",    (0.80, 0.25, 0.40)),
        ("Indigo",  (0.20, 0.10, 0.70)),
        ("Mint",    (0.10, 0.70, 0.50)),
        ("Gold",    (0.80, 0.65, 0.10)),
        ("Violet",  (0.55, 0.10, 0.80)),
        ("DarkPink",    (0.50, 0.08, 0.22)),
        ("DarkPurple",  (0.25, 0.03, 0.45)),
        ("DarkBlue",    (0.04, 0.12, 0.50)),
        ("DarkCyan",    (0.04, 0.35, 0.42)),
        ("DarkGreen",   (0.04, 0.35, 0.10)),
        ("DarkYellow",  (0.50, 0.45, 0.03)),
        ("DarkOrange",  (0.55, 0.22, 0.02)),
        ("DarkRed",     (0.50, 0.04, 0.04)),
        ("DarkMagenta", (0.50, 0.04, 0.42)),
        ("DarkSkyBlue", (0.06, 0.28, 0.50)),
        ("DarkLime",    (0.22, 0.42, 0.04)),
        ("DarkRose",    (0.50, 0.10, 0.20)),
        ("DarkIndigo",  (0.08, 0.03, 0.42)),
        ("DarkMint",    (0.04, 0.40, 0.28)),
        ("DarkGold",    (0.50, 0.38, 0.03)),
        ("DarkViolet",  (0.30, 0.04, 0.50)),
    ]

    pillars = sorted(
        [a for a in sub.get_all_level_actors() if a.get_actor_label().startswith('LB_Pillar_')],
        key=lambda a: a.get_actor_label()
    )
    unreal.log(f"Found {len(pillars)} pillars")

    mic_factory = unreal.MaterialInstanceConstantFactoryNew()
    colored = 0

    for i, actor in enumerate(pillars):
        comps = actor.get_components_by_class(unreal.StaticMeshComponent)
        if not comps:
            unreal.log(f"Pillar {i} ({actor.get_actor_label()}): no StaticMeshComponent found")
            continue

        comp = comps[0]
        num_slots = comp.get_num_materials()
        unreal.log(f"Pillar {i} ({actor.get_actor_label()}): {num_slots} material slot(s)")

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

        # Apply to ALL material slots
        for slot in range(num_slots):
            comp.set_material(slot, mic)

        colored += 1
        unreal.log(f"  -> {color_name} applied to {num_slots} slot(s)")

    unreal.log(f"Done! Colored {colored} pillars")
