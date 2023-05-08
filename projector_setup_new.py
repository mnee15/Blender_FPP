import bpy
from math import radians
from bpy_extras import image_utils

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Clear all elementes (lights, cameras, movies).
lights = bpy.data.lights
for lt in lights:
    bpy.data.lights.remove(lt)

movies = bpy.data.movieclips
for mc in movies:
    bpy.data.movieclips.remove(mc)

cameras = bpy.data.cameras
for cm in cameras:
    bpy.data.cameras.remove(cm)

images = bpy.data.images
for im in images:
    bpy.data.images.remove(im)

# camera parameters.
focal_length = 48
camera_posx = 0
camera_posy = 0
camera_posz = 0
camera_rotx = 90
camera_roty = 0
camera_rotz = 90
camera_resolution_x = 640
camera_resolution_y = 480

# projector parameters.
projector_posx = -0.12
projector_posy = 0.045
projector_posz = 0
projector_rotx = 90
projector_roty = 0
projector_rotz = 94.2894
throw_ratio = 1.13

projector_power = 15 # if sinusoidal pattern
# projector_power = 12 # if binary
# obj distance = -1.245m

# camera setup.
bpy.ops.object.camera_add()
camera = bpy.data.objects['Camera']
camera.data.lens = focal_length
camera.location[0] = camera_posx
camera.location[1] = camera_posy
camera.location[2] = camera_posz
camera.rotation_euler[0] = radians(camera_rotx)
camera.rotation_euler[1] = radians(camera_roty)
camera.rotation_euler[2] = radians(camera_rotz)
bpy.context.scene.render.resolution_x = camera_resolution_x
bpy.context.scene.render.resolution_y = camera_resolution_y
bpy.context.object.proj_settings.power = projector_power

# projector setup.
bpy.ops.projector.create()
bpy.ops.projector.switch_to_cycles()
projector = bpy.data.objects['Projector']
projector.proj_settings.projected_texture = 'custom_texture'
projector.proj_settings.throw_ratio = throw_ratio
projector.proj_settings.power = projector_power
projector.location[0] = projector_posx
projector.location[1] = projector_posy
projector.location[2] = projector_posz
projector.rotation_euler[0] = radians(projector_rotx)
projector.rotation_euler[1] = radians(projector_roty)
projector.rotation_euler[2] = radians(projector_rotz)


# world background = black
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)
