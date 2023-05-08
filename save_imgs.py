import numpy as np
import bpy
import os
import cv2

# save dir
output_dir = "C:\\Users\\USER\\Desktop\\dltpu\\blender\\test\\target16"

# fringe images path
fringe_dir = 'C:\\Users\\USER\\Desktop\\dltpu\\blender\\pattern\\pattern_18_18_bin'
fringe_imgs = os.listdir(fringe_dir)

# Camera Setting
camera = bpy.data.objects['Camera']
scene = bpy.context.scene
scene.camera = camera

# Render Setting
scene.render.image_settings.file_format = 'PNG'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    
os.chdir(output_dir)

filepath = os.path.join(output_dir, "{:02d}.png")
bpy.context.scene.cycles.device = 'GPU'

# Fringe Pattern Projection
for i, f_img in enumerate(fringe_imgs):
    f_img_path = os.path.join(fringe_dir, f_img)
    # bpy.ops.image.open(filepath=f_img_path, directory=fringe_dir, files=[{"name": f_img, "name": f_img}], relative_path=True, show_multiview=False)
    bpy.data.images['02.bmp'].filepath = f_img_path

    # Render & Save Image
    bpy.ops.render.render()
    bpy.data.images["Render Result"].save_render(filepath.format(i))
    # if (i == len(fringe_imgs) -1):
    #     bpy.data.images["Render Result"].save_render(filepath.format(i + 2))