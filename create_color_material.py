import unreal

asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
mel = unreal.MaterialEditingLibrary
sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

MAT_PATH = '/LuckyBlockPillars/Materials'
BASE_MAT_NAME = 'M_PillarBase'
base_mat_full = f'{MAT_PATH}/{BASE_MAT_NAME}'

# Create or load base material
if unreal.EditorAssetLibrary.does_asset_exist(base_mat_full + '.' + BASE_MAT_NAME):
    base_mat = unreal.EditorAssetLibrary.load_asset(base_mat_full)
    unreal.log("Loaded existing base material")
else:
    factory = unreal.MaterialFactoryNew()
    base_mat = asset_tools.create_asset(BASE_MAT_NAME, MAT_PATH, unreal.Material, factory)
    unreal.log(f"Created base material: {base_mat}")

    # Add a VectorParameter node for color
    color_param = mel.create_material_expression(base_mat, unreal.MaterialExpressionVectorParameter, -300, 0)
    color_param.set_editor_property('parameter_name', 'Color')
    color_param.set_editor_property('default_value', unreal.LinearColor(1.0, 0.0, 0.5, 1.0))

    # Connect to BaseColor and Emissive for bright look
    mel.connect_material_property(color_param, 'RGB', unreal.MaterialProperty.MP_BASE_COLOR)
    mel.connect_material_property(color_param, 'RGB', unreal.MaterialProperty.MP_EMISSIVE_COLOR)

    mel.recompile_material(base_mat)
    unreal.EditorAssetLibrary.save_asset(base_mat_full)
    unreal.log("Base material created and saved")

unreal.log(f"Base mat ready: {base_mat.get_path_name()}")
