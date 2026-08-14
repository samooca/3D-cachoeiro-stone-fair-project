import math
from pathlib import Path

import bpy
from mathutils import Vector


PROJECT = Path(r"C:\Iven\Feiras & Eventos\3d")
OUTPUT = PROJECT / "hunyuan_multiview_consistent"
OUTPUT.mkdir(parents=True, exist_ok=True)


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        for block in list(datablocks):
            if block.users == 0:
                datablocks.remove(block)


def material(name, color, roughness=0.55, metallic=0.0, emission=None, strength=0.0):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    if emission is not None:
        bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
        bsdf.inputs["Emission Strength"].default_value = strength
    return mat


def add_box(name, location, scale, mat, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = (scale[0] / 2, scale[1] / 2, scale[2] / 2)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        modifier = obj.modifiers.new("Soft edges", "BEVEL")
        modifier.width = bevel
        modifier.segments = 3
    obj.data.materials.append(mat)
    return obj


def add_cylinder(name, location, radius, depth, mat, vertices=24, scale=(1, 1, 1), rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=location, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    return obj


def add_uv_sphere(name, location, scale, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    return obj


def add_chair(name, x, y, rotation_z):
    root = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(root)
    root.location = (x, y, 0)
    root.rotation_euler.z = rotation_z

    parts = []
    parts.append(add_box(f"{name}_seat", (0, 0, 0.55), (0.72, 0.72, 0.10), wood, 0.05))
    for lx in (-0.28, 0.28):
        for ly in (-0.28, 0.28):
            parts.append(add_box(f"{name}_leg", (lx, ly, 0.28), (0.07, 0.07, 0.55), wood, 0.02))
    parts.append(add_box(f"{name}_back_frame", (0, 0.31, 1.08), (0.72, 0.07, 0.88), wood, 0.04))
    parts.append(add_box(f"{name}_cane", (0, 0.265, 1.08), (0.56, 0.025, 0.64), cane, 0.03))
    for part in parts:
        part.parent = root


def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def add_camera(name, location, target=(0, 0, 1.7), ortho_scale=8.4):
    data = bpy.data.cameras.new(name)
    data.type = "ORTHO"
    data.ortho_scale = ortho_scale
    data.lens = 50
    camera = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(camera)
    camera.location = location
    look_at(camera, target)
    return camera


clear_scene()

# Materials derived from the supplied renders.
limestone = material("Limestone Beige", (0.78, 0.72, 0.61), 0.66)
floor_mat = material("Ivory Floor", (0.88, 0.84, 0.75), 0.50)
green_stone = material("Bookmatched Green Stone", (0.18, 0.24, 0.14), 0.38)
white = material("Warm White Structure", (0.92, 0.90, 0.84), 0.35)
wood = material("Light Oak", (0.55, 0.36, 0.18), 0.55)
cane = material("Natural Cane", (0.72, 0.58, 0.37), 0.72)
plant = material("Tropical Green", (0.08, 0.28, 0.055), 0.55)
stem = material("Plant Stem", (0.05, 0.18, 0.035), 0.65)
dark = material("Dark Stone", (0.08, 0.09, 0.075), 0.42)
light_emission = material("Warm LED", (0.94, 0.75, 0.48), 0.25, emission=(1.0, 0.63, 0.28), strength=4.0)

# Fixed architectural shell, in metres. Front is -Y and rear is +Y.
add_box("Floor_Base", (0, 0, 0.08), (12.0, 7.0, 0.16), floor_mat, 0.03)
add_box("Rear_Wall", (0, 3.43, 2.05), (12.0, 0.18, 4.10), limestone, 0.02)
add_box("Left_Wall", (-5.91, 0, 2.05), (0.18, 7.0, 4.10), limestone, 0.02)
add_box("Right_Rear_Wall", (5.91, 2.35, 2.05), (0.18, 2.15, 4.10), limestone, 0.02)
add_box("Right_Partition", (5.00, -1.05, 1.85), (0.22, 2.65, 3.70), limestone, 0.03)

# Overhead frame and roof opening.
add_box("Front_Header", (0, -3.36, 4.02), (12.0, 0.30, 0.32), white, 0.02)
add_box("Rear_Header", (0, 3.28, 4.02), (12.0, 0.30, 0.32), white, 0.02)
add_box("Left_Header", (-5.82, 0, 4.02), (0.30, 6.7, 0.32), white, 0.02)
add_box("Right_Header", (5.82, 0, 4.02), (0.30, 6.7, 0.32), white, 0.02)

# Signature green rear panel.
add_box("Green_Stone_Panel", (-2.55, 3.30, 2.10), (3.25, 0.12, 3.75), green_stone, 0.01)

# Central sample counter and its eight fixed samples.
add_box("Sample_Counter", (1.65, -1.55, 0.63), (4.90, 1.15, 1.10), limestone, 0.06)
add_box("Counter_LED", (1.65, -1.55, 0.12), (4.55, 0.08, 0.05), light_emission, 0.01)
sample_colors = [limestone, white, green_stone, dark, limestone, green_stone, white, dark]
for index, sample_mat in enumerate(sample_colors):
    x = -0.25 + index * 0.55
    add_box(f"Stone_Sample_{index + 1:02d}", (x, -1.55, 1.205), (0.43, 0.72, 0.07), sample_mat, 0.025)

# Long planter behind the counter.
add_box("Planter", (1.65, 0.70, 0.70), (4.75, 1.05, 1.25), limestone, 0.05)
plant_positions = [
    (-0.25, 0.55, 2.15, 0.62, 1.05), (0.35, 0.77, 2.32, 0.70, 1.18),
    (0.95, 0.56, 2.18, 0.64, 1.00), (1.55, 0.80, 2.42, 0.76, 1.25),
    (2.15, 0.52, 2.22, 0.66, 1.06), (2.75, 0.78, 2.34, 0.72, 1.20),
    (3.35, 0.56, 2.16, 0.64, 1.05),
]
for index, (x, y, z, sx, sz) in enumerate(plant_positions):
    add_cylinder(f"Plant_Stem_{index:02d}", (x, y, 1.75), 0.035, 1.55, stem, vertices=10)
    leaf = add_uv_sphere(f"Plant_Leaf_{index:02d}", (x, y, z), (sx, 0.18, sz), plant)
    leaf.rotation_euler.z = math.radians((-18 + index * 11) % 35 - 17)
    # Smaller low foliage, deterministic and tied to the same coordinates.
    add_uv_sphere(f"Plant_Low_{index:02d}", (x + 0.12, y - 0.15, 1.48), (0.42, 0.20, 0.32), plant)

# Meeting table on the left, long axis along depth as in the plan.
add_box("Meeting_Table_Top", (-3.15, 0.35, 1.32), (1.95, 4.35, 0.18), limestone, 0.32)
for level in range(7):
    z = 0.25 + level * 0.15
    radius = 0.64 + (0.08 if level % 2 == 0 else -0.03)
    pedestal = add_cylinder(
        f"Table_Pedestal_{level:02d}",
        (-3.15 + (0.04 if level % 2 else -0.03), 0.35, z),
        radius,
        0.14,
        limestone,
        vertices=12,
        scale=(1.0, 0.78, 1.0),
    )
    pedestal.rotation_euler.z = math.radians(level * 13)

# Exactly six chairs, three on each side of the table.
chair_y = (-1.05, 0.35, 1.75)
for idx, y in enumerate(chair_y):
    add_chair(f"Chair_Left_{idx + 1}", -4.45, y, math.radians(-90))
    add_chair(f"Chair_Right_{idx + 1}", -1.85, y, math.radians(90))

# V-shaped pendant array above the table. Every cylinder has a fixed coordinate.
for index in range(22):
    t = index / 21.0
    x = -4.70 + t * 3.10
    y = 0.35
    tip_z = 2.25 + abs(t - 0.5) * 1.30
    add_cylinder(f"Pendant_{index + 1:02d}", (x, y, tip_z), 0.035, 0.26, light_emission, vertices=12)
    add_cylinder(f"Pendant_Cable_{index + 1:02d}", (x, y, (tip_z + 4.0) / 2), 0.008, 4.0 - tip_z, white, vertices=8)

# Linear wall lights and right partition spot accents.
add_box("Left_Wall_Light_A", (-5.77, -1.05, 2.20), (0.035, 0.12, 1.35), light_emission, 0.01)
add_box("Left_Wall_Light_B", (-5.77, 1.25, 2.20), (0.035, 0.12, 1.35), light_emission, 0.01)
for y in (-1.65, -0.55):
    add_uv_sphere("Right_Spot", (4.86, y, 2.85), (0.04, 0.07, 0.04), light_emission)

# Cameras: one common target, identical orthographic scale and exact 90-degree azimuth steps.
cameras = {
    "front": add_camera("Camera_Front", (0, -20, 2.05), target=(0, 0, 2.05), ortho_scale=6.40),
    "left": add_camera("Camera_Left", (-20, 0, 2.05), target=(0, 0, 2.05), ortho_scale=6.40),
    "back": add_camera("Camera_Back", (0, 20, 2.05), target=(0, 0, 2.05), ortho_scale=6.40),
    "right": add_camera("Camera_Right", (20, 0, 2.05), target=(0, 0, 2.05), ortho_scale=6.40),
}

# Neutral lighting and background optimized for CLIP Vision conditioning.
world = bpy.context.scene.world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.78, 0.78, 0.78, 1.0)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.8

for name, location, energy, size in (
    ("Key_Area", (0, -5, 9), 1700, 7.0),
    ("Fill_Area", (5, 2, 6), 1100, 5.0),
    ("Rear_Area", (-4, 5, 6), 900, 4.0),
):
    light_data = bpy.data.lights.new(name, "AREA")
    light_data.energy = energy
    light_data.shape = "DISK"
    light_data.size = size
    light_obj = bpy.data.objects.new(name, light_data)
    bpy.context.collection.objects.link(light_obj)
    light_obj.location = location
    look_at(light_obj, (0, 0, 1.0))

scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 2048
scene.render.resolution_y = 1024
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.render.film_transparent = False
scene.render.image_settings.color_depth = "8"
scene.render.film_transparent = False
scene.view_settings.look = "AgX - Medium High Contrast"
scene.render.resolution_percentage = 100

# Store source references and project notes inside the .blend.
for ref_name in ("ref1.png", "ref2.png", "stand_1.jpeg", "stand_3.jpeg", "ChatGPT Image 14 de ago. de 2026, 12_18_06.png"):
    ref_path = PROJECT / ref_name
    if ref_path.exists():
        image = bpy.data.images.load(str(ref_path), check_existing=True)
        image.pack()

notes = bpy.data.texts.new("README_MULTIVIEW")
notes.write(
    "Stand blockout criado a partir das referências do projeto.\n"
    "Unidades: metros. Front=-Y, Back=+Y, Left=-X, Right=+X.\n"
    "As quatro câmeras usam a mesma escala ortográfica e alvo.\n"
    "A geometria traseira não observada foi mantida conservadora.\n"
)

blend_path = OUTPUT / "iven_stone_stand_multiview.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))

output_names = {
    "front": "3d_hunyuan3d_multiview_to_model_front_image.png",
    "left": "3d_hunyuan3d_multiview_to_model_left_image.png",
    "back": "3d_hunyuan3d_multiview_to_model_back_image.png",
    "right": "3d_hunyuan3d_multiview_to_model_right_image.png",
}
for view_name in ("front", "left", "back", "right"):
    scene.camera = cameras[view_name]
    scene.render.filepath = str(OUTPUT / output_names[view_name])
    bpy.ops.render.render(write_still=True)
    print(f"RENDERED {view_name} {scene.render.filepath}")

bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
print(f"BLEND_SAVED {blend_path}")
