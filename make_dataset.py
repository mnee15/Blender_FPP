import os
import bpy
import cv2
import numpy as np

start = 0
end = 100

wrk_dir = "C:\\Users\\USER\\Desktop\\dltpu\\blender"
os.chdir(wrk_dir)

camera = bpy.data.objects['Camera']

# object path
object_dir = "C:\\Users\\USER\\Desktop\\3D_dataset\\1K"
object_lst = os.listdir(object_dir)

# fringe images path
fringe_path = 'C:\\Users\\USER\\Desktop\\dltpu\\blender\\pattern\\pattern_dl'
fringe_imgs = os.listdir(fringe_path)

# captured images path
cimg_path = "C:\\Users\\USER\\Desktop\\dltpu\\data"

# prepare the scene to capture the poses images
scene = bpy.context.scene
scene.camera = camera

scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.cycles.device = 'GPU'
os.chdir(cimg_path)

translation_val = (-0.65, 0.0, 0)
max_height = 0.532

prev = ''
for i, object_name in enumerate(object_lst[start:end]):
    tmp = os.path.join(cimg_path, "{:03d}".format(i + start))
    savepath = os.path.join(tmp, "{:02d}.png")
    filepath = os.path.join(object_dir, object_name)

    if not os.path.exists(tmp):
        os.makedirs(tmp)
    os.chdir(tmp)

    if (len(prev)):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[prev].select_set(True)
        bpy.ops.object.delete()
        
     # import object & set scale
    bpy.ops.import_mesh.stl(filepath=filepath, filter_glob="*.stl",  files=[{"name":object_name, "name":object_name}], directory=object_dir)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[object_name[:-4]].select_set(True)
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="MEDIAN")
    dim_x, dim_y, dim_z = bpy.context.selected_objects[0].dimensions
    max_dim = max(dim_x, dim_y, dim_z)
    r = max_height / max_dim
    resize_val = (r, r, r)
    
    tmp = np.random.rand(3,1)
    tmp = tmp if np.random.rand(1)[0] >-0.5 else -tmp
    if (max_dim == dim_x):
        rotation_val = (-1.5708 + tmp[0], tmp[1], 1.5708 + tmp[2])
        
    elif (max_dim == dim_y):
        rotation_val = (-3.1415 + tmp[0], tmp[1], 1.5708 + tmp[2])
        
    elif (max_dim == dim_z):
        rotation_val = (-1.5708 + tmp[0], 1.5708 + tmp[2], 3.1415 + tmp[2])
        
    bpy.context.object.scale = resize_val
    bpy.context.object.location = translation_val
    bpy.context.object.rotation_euler = rotation_val
    
    for j, fimg in enumerate(fringe_imgs):
        f_img_path = os.path.join(fringe_path, fimg)
        bpy.data.images['06.bmp'].filepath = f_img_path

        bpy.ops.render.render()
        bpy.data.images["Render Result"].save_render(savepath.format(j))

    prev = object_name[:-4]
