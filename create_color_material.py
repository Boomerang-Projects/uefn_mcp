import unreal

mel = unreal.MaterialEditingLibrary
MAT_PATH = '/LuckyBlockPillars/Materials'
BASE_MAT_NAME = 'M_PillarBase'
base_mat_full = f'{MAT_PATH}/{BASE_MAT_NAME}.{BASE_MAT_NAME}'

base_mat = unreal.EditorAssetLibrary.load_asset(base_mat_full)
if not base_mat:
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = unreal.MaterialFactoryNew()
    base_mat = asset_tools.create_asset(BASE_MAT_NAME, MAT_PATH, unreal.Material, factory)

# Clear all existing expressions
for expr in mel.get_material_expressions(base_mat):
    mel.delete_material_expression(base_mat, expr)

# Color parameter
color_param = mel.create_material_expression(base_mat, unreal.MaterialExpressionVectorParameter, -400, 0)
color_param.set_editor_property('parameter_name', 'Color')
color_param.set_editor_property('default_value', unreal.LinearColor(1.0, 0.0, 0.5, 1.0))

# Color -> BaseColor
mel.connect_material_property(color_param, 'RGB', unreal.MaterialProperty.MP_BASE_COLOR)

# Color * 1.5 -> EmissiveColor
emissive_scale = mel.create_material_expression(base_mat, unreal.MaterialExpressionMultiply, -200, 150)
scalar = mel.create_material_expression(base_mat, unreal.MaterialExpressionConstant, -400, 200)
scalar.set_editor_property('r', 1.5)
mel.connect_material_expressions(color_param, 'RGB', emissive_scale, 'A')
mel.connect_material_expressions(scalar, '', emissive_scale, 'B')
mel.connect_material_property(emissive_scale, '', unreal.MaterialProperty.MP_EMISSIVE_COLOR)

mel.recompile_material(base_mat)
unreal.EditorAssetLibrary.save_asset(f'{MAT_PATH}/{BASE_MAT_NAME}')
unreal.log("M_PillarBase: plain color + emissive (no texture) — testing colors first")
