# villa_blockout_template.py
# Run in Blender: Scripting tab > New > paste > Run Script (Alt+P).
# ONE scene, several cameras (one per shot), color-coded flat boxes.
# Builds an illustrative one-floor villa: house, roof, pergola with 4 columns,
# pool, dining table with pendant lamps, chairs, sofa group, lounger, trees.
# Sizes are in metres and are ILLUSTRATIVE, not real architectural data.
# Safe to run again: it only deletes what it created before.
import os

import bmesh
import bpy

# ------------------------------------------------------------- PARAMETERS
# Main volume of the house (x, y, z)
HOUSE_W, HOUSE_D, HOUSE_H = 14.0, 6.0, 3.2
# Stone terrace in front of the house
TERRACE_D = 5.0
# Pool, in front of the terrace
POOL_W, POOL_D = 11.0, 3.5
# Covered dining area, left side of the terrace
PERGOLA_W, PERGOLA_D = 6.0, 4.0
FPS = 24
# Seedance 2.5 makes clips of 4 to 30 seconds, so a shot is 4 s by default
SHOT_SECONDS = 4
# 9:16 for phones. Use 1920, 1080 for 16:9
RES_X, RES_Y = 1080, 1920
# 24-35 keeps vertical lines straight
FOCAL_MM = 28
# One entry per shot: name, camera start, camera end, look-at start, look-at end
# Eye height about 1.5 m. One slow gesture per shot.
SHOTS = [
    ("pool_push", (-4.5, -12.0, 1.4), (-3.0, -9.5, 1.4),
     (-3.5, -2.2, 1.0), (-3.5, -2.2, 1.0)),
    ("sofa_push", (6.5, -9.0, 1.4), (5.5, -6.2, 1.2),
     (3.8, -2.2, 0.8), (3.8, -2.2, 0.8)),
    ("lounger_corner", (7.5, -7.0, 1.0), (6.8, -6.0, 0.9),
     (2.0, -4.6, 0.4), (2.0, -4.6, 0.4)),
    ("dining_interior", (-0.5, -1.0, 1.5), (-1.8, -1.6, 1.4),
     (-4.5, -2.2, 0.8), (-4.5, -2.2, 0.8)),
]
# Empty = folder "villa_blockout" in your home folder
OUTPUT_DIR = ""
# ---------------------------------------------------------------------------

COLLECTIONS = ["Structure", "Water", "Seating", "Vegetation", "Lights", "Camera"]
# Flat, clearly different colors (R, G, B). An image or video model reads them
# as separate things: grey = architecture, turquoise = water, red = furniture,
# purple = chairs, blue = small objects, green = plants.
COLORS = {
    "wall": (0.85, 0.85, 0.85),
    "floor": (0.62, 0.60, 0.57),
    "water": (0.25, 0.80, 0.80),
    "sofa": (0.80, 0.08, 0.05),
    "chair": (0.45, 0.15, 0.70),
    "small": (0.10, 0.20, 0.80),
    "plant": (0.15, 0.65, 0.15),
    "lamp": (0.95, 0.95, 0.95),
}


def collection(name):
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)
    return col


def clear_previous():
    # only remove what an earlier run of this script made
    for name in COLLECTIONS:
        col = bpy.data.collections.get(name)
        if col:
            for ob in list(col.objects):
                bpy.data.objects.remove(ob, do_unlink=True)
    scene = bpy.context.scene
    for marker in list(scene.timeline_markers):
        if marker.name.startswith("shot_"):
            scene.timeline_markers.remove(marker)


def flat_material(key):
    name = "blk_" + key
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    rgb = COLORS[key]
    # the color the preview render uses
    mat.diffuse_color = (rgb[0], rgb[1], rgb[2], 1.0)
    # also set the shader color, if available
    try:
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        node = next((n for n in nodes if n.type == "BSDF_PRINCIPLED"), None)
        if node:
            node.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
    except Exception as exc:
        print("material nodes skipped:", exc)
    return mat


def add_object(name, mesh, col, loc, mat):
    ob = bpy.data.objects.new(name, mesh)
    ob.location = loc
    ob.data.materials.append(mat)
    col.objects.link(ob)
    return ob


def box(name, col_name, size, loc, color):
    """size = full (x, y, z); loc = CENTER of the box."""
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bm.to_mesh(mesh)
    bm.free()
    ob = add_object(name, mesh, collection(col_name), loc, flat_material(color))
    ob.scale = size
    return ob


def cylinder(name, col_name, diameter, height, loc, color, top_diameter=None):
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    d1 = diameter
    d2 = diameter if top_diameter is None else top_diameter
    # newer Blender versions take radius, some versions take diameter
    try:
        bmesh.ops.create_cone(bm, cap_ends=True, segments=16,
                              radius1=d1 / 2, radius2=d2 / 2, depth=height)
    except TypeError:
        bmesh.ops.create_cone(bm, cap_ends=True, segments=16,
                              diameter1=d1, diameter2=d2, depth=height)
    bm.to_mesh(mesh)
    bm.free()
    return add_object(name, mesh, collection(col_name), loc, flat_material(color))


def ball(name, col_name, diameter, loc, color):
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    try:
        bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=10, radius=diameter / 2)
    except TypeError:
        bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=10, diameter=diameter)
    bm.to_mesh(mesh)
    bm.free()
    return add_object(name, mesh, collection(col_name), loc, flat_material(color))


def build_structure():
    x_left = -HOUSE_W / 2
    # ground slab, top surface at z = 0
    total_d = TERRACE_D + POOL_D + 3.0
    box("Ground", "Structure", (HOUSE_W + 8, HOUSE_D + total_d + 4, 0.2),
        (0, (HOUSE_D - total_d) / 2, -0.1), "floor")
    # house (back of the plot, front face at y = 0)
    box("House", "Structure", (HOUSE_W, HOUSE_D, HOUSE_H),
        (0, HOUSE_D / 2, HOUSE_H / 2), "wall")
    # flat roof with an overhang
    box("Roof", "Structure", (HOUSE_W + 1.0, HOUSE_D + 1.0, 0.25),
        (0, HOUSE_D / 2, HOUSE_H + 0.125), "wall")
    # pergola over the dining area (4 columns + roof slab)
    px = x_left + PERGOLA_W / 2 + 0.5
    py = -PERGOLA_D / 2 - 0.2
    for i, (sx, sy) in enumerate([(-1, -1), (1, -1), (-1, 1), (1, 1)]):
        cx = px + sx * (PERGOLA_W / 2 - 0.2)
        cy = py + sy * (PERGOLA_D / 2 - 0.2)
        cylinder("Column_%d" % (i + 1), "Structure", 0.3, 2.8, (cx, cy, 1.4), "wall")
    box("PergolaRoof", "Structure", (PERGOLA_W, PERGOLA_D, 0.15),
        (px, py, 2.875), "wall")
    return px, py


def build_water():
    py = -(TERRACE_D + POOL_D / 2)
    box("Pool", "Water", (POOL_W, POOL_D, 0.1), (0.5, py, -0.04), "water")


def build_seating(px, py):
    box("DiningTable", "Seating", (3.0, 1.0, 0.75), (px, py, 0.375), "sofa")
    for i in range(3):
        for side in (-1, 1):
            box("Chair_%d_%d" % (i, side), "Seating", (0.5, 0.5, 0.45),
                (px - 1.0 + i * 1.0, py + side * 0.9, 0.225), "chair")
    # pendant lamps above the table
    for i in range(2):
        cylinder("Lamp_%d" % i, "Lights", 0.5, 0.45,
                 (px - 0.8 + i * 1.6, py, 2.4), "lamp", top_diameter=0.15)
    # sofa group on the right side of the terrace
    sx, sy = HOUSE_W / 2 - 3.2, -2.2
    box("SofaBack", "Seating", (4.0, 0.9, 0.9), (sx, sy + 1.1, 0.45), "sofa")
    box("SofaSide", "Seating", (0.9, 2.6, 0.9), (sx + 1.55, sy, 0.45), "sofa")
    box("CoffeeTable", "Seating", (1.4, 0.8, 0.4),
        (sx - 0.2, sy - 0.3, 0.2), "sofa")
    box("SmallObject", "Seating", (0.4, 0.4, 0.5), (sx - 0.2, sy - 0.3, 0.65), "small")
    # lounger near the pool edge, with a folded towel
    box("Lounger", "Seating", (2.0, 0.8, 0.4), (2.0, -4.6, 0.2), "sofa")
    box("Towel", "Seating", (0.5, 0.4, 0.12), (2.6, -4.6, 0.46), "small")


def build_vegetation():
    spots = [(-8.5, -5.0), (-8.0, 1.0), (8.5, -4.0),
             (9.0, 2.0), (-3.0, 10.0), (4.0, 10.0)]
    for i, (x, y) in enumerate(spots):
        cylinder("Trunk_%d" % i, "Vegetation", 0.3, 1.5, (x, y, 0.75), "floor")
        ball("Crown_%d" % i, "Vegetation", 2.4, (x, y, 2.4), "plant")


def build_cameras():
    scene = bpy.context.scene
    col = collection("Camera")
    frames = int(FPS * SHOT_SECONDS)
    for index, (name, c_start, c_end, l_start, l_end) in enumerate(SHOTS):
        f_start = 1 + index * frames
        f_end = f_start + frames - 1
        cam_data = bpy.data.cameras.get("cam_" + name) or bpy.data.cameras.new("cam_" + name)
        cam_data.lens = FOCAL_MM
        cam = bpy.data.objects.new("cam_" + name, cam_data)
        col.objects.link(cam)
        # an empty object that this camera looks at
        target = bpy.data.objects.new("look_" + name, None)
        target.empty_display_type = "PLAIN_AXES"
        col.objects.link(target)
        try:
            track = cam.constraints.new(type="TRACK_TO")
            track.target = target
            track.track_axis = "TRACK_NEGATIVE_Z"
            track.up_axis = "UP_Y"
        except Exception as exc:
            print("track-to constraint failed:", exc)
        for frame, pos, look in ((f_start, c_start, l_start), (f_end, c_end, l_end)):
            cam.location = pos
            target.location = look
            # Bezier keyframes = ease in and ease out
            cam.keyframe_insert(data_path="location", frame=frame)
            target.keyframe_insert(data_path="location", frame=frame)
        # a timeline marker bound to the camera switches cameras at the cut
        marker = scene.timeline_markers.new("shot_" + name, frame=f_start)
        marker.camera = cam
        if index == 0:
            scene.camera = cam
    scene.frame_start, scene.frame_end, scene.render.fps = 1, frames * len(SHOTS), FPS


def preview_settings():
    scene = bpy.context.scene
    scene.render.resolution_x, scene.render.resolution_y = RES_X, RES_Y
    scene.render.resolution_percentage = 100
    # light sky color behind the boxes
    try:
        if scene.world is None:
            scene.world = bpy.data.worlds.new("BlockoutWorld")
        scene.world.color = (0.88, 0.92, 0.97)
    except Exception as exc:
        print("world color skipped:", exc)
    # fast flat preview. Other engines stay possible.
    try:
        scene.render.engine = "BLENDER_WORKBENCH"
        shading = scene.display.shading
        shading.light = "STUDIO"
        shading.color_type = "MATERIAL"
    except Exception as exc:
        print("could not set the Workbench engine:", exc)
    out = OUTPUT_DIR or os.path.join(os.path.expanduser("~"), "villa_blockout")
    scene.render.filepath = os.path.join(out, "blockout_")
    # MP4 if this Blender allows it, otherwise a PNG sequence (always works)
    try:
        img = scene.render.image_settings
        if hasattr(img, "media_type"):
            img.media_type = "VIDEO"
        img.file_format = "FFMPEG"
        scene.render.ffmpeg.format = "MPEG4"
        scene.render.ffmpeg.codec = "H264"
        print("Output: MP4 in", out)
    except Exception as exc:
        try:
            scene.render.image_settings.file_format = "PNG"
        except Exception:
            pass
        print("MP4 not available (%s). Output: PNG frames in %s" % (exc, out))


clear_previous()
pergola_x, pergola_y = build_structure()
build_water()
build_seating(pergola_x, pergola_y)
build_vegetation()
build_cameras()
preview_settings()
print("Blockout done: %d shots of %d s. Space = preview." % (len(SHOTS), SHOT_SECONDS))
