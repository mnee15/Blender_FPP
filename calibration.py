import os
import bpy
import cv2
import numpy as np

board_path = "acircleboard.svg"
calibr_xml_path = "calibr_poses.xml"

wrk_dir = "C:\\Users\\USER\\Desktop\\dltpu\\blender"
os.chdir(wrk_dir)

# board_path = os.path.join(wrk_dir, board_path)
# calibr_xml_path = os.path.join(wrk_dir, calibr_xml_path)

camera = bpy.data.objects['Camera']

# 01. remove SVG collection
collection = bpy.data.collections.get(board_path)
if collection:
    print('the calibration patters is already loaded')
else:
    bpy.ops.import_curve.svg(filepath=board_path)
    collection = bpy.data.collections.get(board_path)

for obj in collection.objects:
    bpy.data.objects.remove(obj, do_unlink=True)

bpy.data.collections.remove(collection)

# 02. import calibration pattern
bpy.ops.import_curve.svg(filepath=board_path)

# 03. deselect nothing, select all curves, join
bpy.ops.object.select_all(action='DESELECT')
# bpy.ops.object.select_by_type(type='CURVE')

curves = bpy.data.collections[board_path].all_objects
for obj in curves:
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.convert(target='MESH')

bpy.ops.object.join()
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
calibr_pattern = bpy.data.collections[board_path].all_objects[0]

# fringe images path.
fringe_path = 'C:\\Users\\USER\\Desktop\\dltpu\\blender\\pattern\\pattern_18_18_bin'
fringe_imgs = os.listdir(fringe_path)

# projector calibration captured images path
cimg_path = "C:\\Users\\USER\\Desktop\\dltpu\\blender\\calibration\\calibration7"
if not os.path.exists(cimg_path):
    os.makedirs(cimg_path)

# 04. read XML file.
poses_xml = cv2.FileStorage(calibr_xml_path, cv2.FILE_STORAGE_READ)
poses = poses_xml.getNode("calibr_poses").mat()
nposes = np.shape(poses)[0]

# 05. we prepare the scene to capture the poses images
scene = bpy.context.scene
scene.camera = camera

scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.cycles.device = 'GPU'
os.chdir(cimg_path)

for pos in range(nposes):
    tmp = os.path.join(cimg_path, "P{:02d}".format(pos))
    filepath = os.path.join(tmp, "{:02d}.png")
    if not os.path.exists(tmp):
        os.makedirs(tmp)
        
    os.chdir(tmp)

    for i, fimg in enumerate(fringe_imgs):
        calibr_pattern.location = poses[pos, 0:3]
        calibr_pattern.rotation_euler = poses[pos, 3:6]

        f_img_path = os.path.join(fringe_path, fimg)
        bpy.data.images['08.bmp'].filepath = f_img_path

        bpy.ops.render.render()
        bpy.data.images["Render Result"].save_render(filepath.format(i))
