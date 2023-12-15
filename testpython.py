

import bpy

print("hi")

bpy.ops.mesh.primitive_cube_add(size= 4)

cubepbj = bpy.context.active_action

cubepbj.location.z = 5
