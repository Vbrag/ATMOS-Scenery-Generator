
bl_info = {
    "name": "ATMOS Scenery_Model Generator",
    "author": "Abdelmawla Saeed Rizk abdelmawla.rizk@uni-paderborn.de",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "Right side panel > VIEW_3D > Scenery_Model Generator",
    "description": "import terrain with OpenStreetMap and Google 3D cities, to generate 3d environment "
}



import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty

import requests 
import   zipfile 

terrainUrl = "https://s3.amazonaws.com/elevation-tiles-prod/skadi/%s/%s"


def download_url(url, save_path, chunk_size=128):

    print("download : " +  url)
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)



register_List= []


class AddonPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname =   __name__

    filepath: StringProperty(
        name="Data Path",
        subtype='FILE_PATH',
    )
    # number: IntProperty(
    #     name="Example Number",
    #     default=4,
    # )
    # boolean: BoolProperty(
    #     name="Example Boolean",
    #     default=False,
    # )

    def draw(self, context):
        layout = self.layout
        layout.label(text="This is a preferences view for our add-on")
        layout.prop(self, "filepath")
        #layout.prop(self, "number")
        #layout.prop(self, "boolean")
 

register_List.append(AddonPreferences)


class ImportTerrainOperator( Operator):
    """Tooltip"""
    bl_idname = "object.import_terrain_operator"
    bl_label = "Import Terrain"

    #@classmethod
    #def poll(cls, context):
    #    return context.active_object is not None

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(2, 0, 0), scale=(1, 1, 1))
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 2, 0), scale=(1, 1, 1))
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, -2, 0), scale=(1, 1, 1))
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(-2, 0, 0), scale=(1, 1, 1))

        #preferences = context.preferences
        #addon_prefs = preferences.addons[ __name__].preferences
        
        path = "C:\\Users\\abdel\\Documents\\OpenStreetMaps\\"
        
        info = path #("Path: %s" %(addon_prefs.filepath)) # , Number: %d, Boolean %r , addon_prefs.number, addon_prefs.boolean

        self.report({'INFO'}, info)
        print(info)





        return {'FINISHED'}


 
register_List.append(ImportTerrainOperator)    
    
class LayoutPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "ATMOS Scenery_Model Generator"
    bl_idname = __name__#"PT_UniPaderpornRtm"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Scenery_Model Generator"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        """
        # Create a simple row.
        layout.label(text=" Simple Row:")

        row = layout.row()
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")

        # Create an row where the buttons are aligned to each other.
        layout.label(text=" Aligned Row:")

        row = layout.row(align=True)
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")

        # Create two columns, by using a split layout.
        split = layout.split()

        # First column
        col = split.column()
        col.label(text="Column One:")
        col.prop(scene, "frame_end")
        col.prop(scene, "frame_start")

        # Second column, aligned
        col = split.column(align=True)
        col.label(text="Column Two:")
        col.prop(scene, "frame_start")
        col.prop(scene, "frame_end")
        # Different sizes in a row
        layout.label(text="Different button sizes:")
        row = layout.row(align=True)
        row.operator("render.render")

        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("render.render")

        row.operator("render.render")

        
        """
        
        # Big render button
        layout.label(text="Big Button:")
        row = layout.row()
        row.scale_y = 2.0
        row.operator( "object.import_terrain_operator",  icon = "WORLD_DATA" )

register_List.append(LayoutPanel) 

def register():
    for cl in register_List:
        bpy.utils.register_class(cl)
 


def unregister():
    for cl in register_List:
        bpy.utils.unregister_class(cl)
 


if __name__ == "__main__":
    register()
