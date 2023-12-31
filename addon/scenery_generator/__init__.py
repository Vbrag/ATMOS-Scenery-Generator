
bl_info = {
    "name": "Scenery Generator new",
    "author": "Abdelmawla Saeed Rizk abdelmawla.rizk@uni-paderborn.de",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "Right side panel > VIEW_3D > Scenery_Model Generator",
    "description": "import terrain with OpenStreetMap and Google 3D cities, to generate 3d environment "
}



import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty

 


from . import scenery 


print("all ok")
register_List= []


class OpenBrowserOSM(bpy.types.Operator):
    bl_idname = "open.browser_osm"
    bl_label = "get OSM file"

    filepath : bpy.props.StringProperty(subtype="FILE_PATH") 
    #somewhere to remember the address of the file
    
    
    # @classmethod
    # def poll(cls, context):
    #     return context.object is not None
    #

    def execute(self, context):
        file = open(self.filepath, 'w')
        file.write("Hello World "   )
        print(self.filepath)
        
        return {'FINISHED'}

    def invoke(self, context, event): # See comments at end  [1]

        context.window_manager.fileselect_add(self) 
        #Open browser, take reference to 'self' 
        #read the path to selected file, 
        #put path in declared string type data structure self.filepath

        return {'RUNNING_MODAL'}  
        # Tells Blender to hang on for the slow user input


 

 
register_List.append(OpenBrowserOSM)

 
# class AddonPreferences(AddonPreferences): 
#     # this must match the add-on name, use '__package__'
#     # when defining this in a submodule of a python package.
#     bl_idname =   __name__
#
#     filepath: StringProperty(
#         name="Data Path",
#         subtype='FILE_PATH',
#     )
#     # number: IntProperty(
#     #     name="Example Number",
#     #     default=4,
#     # )
#     # boolean: BoolProperty(
#     #     name="Example Boolean",
#     #     default=False,
#     # )
#
#     def draw(self, context):
#         layout = self.layout
#         layout.label(text="This is a preferences view for our add-on")
#         layout.prop(self, "filepath")
#         #layout.prop(self, "number")
#         #layout.prop(self, "boolean")
#
#
# register_List.append(AddonPreferences)


class ImportBuildingsOperator( Operator):
    """Tooltip"""
    bl_idname = "object.import_building_operator"
    bl_label = "Import Buildings"

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


 
register_List.append(ImportBuildingsOperator)    
    
class LayoutPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = " Scenery  Generator new"
    bl_idname =  "LayoutPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Scenery Generator new"

    def draw(self, context):
        layout = self.layout

 
        # Big render button
        layout.label(text="OSM File")
        row = layout.row()
        row.scale_y = 1.0
        row.operator( "open.browser_osm"  )

        layout.label(text="Assets File")
        row = layout.row()
        row.scale_y = 1.0
        row.operator( "open.browser_osm"  )


        layout.label(text="")
        row = layout.row()
        row.scale_y = 2.0
        row.operator( "object.import_building_operator",  icon = "WORLD_DATA" )


register_List.append(LayoutPanel) 







class LayoutPanelB(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = " Scenery  Generator new B"
    bl_idname =  "LayoutPanelB"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Scenery Generator new"
    bl_parent_id = "LayoutPanel"
    bl_options = {"DEFAULT_CLOSED"}
    

    def draw(self, context):
        layout = self.layout
 
        # Big render button
        layout.label(text="OSM File")
        row = layout.row()
        row.scale_y = 1.0
        row.operator( "open.browser_osm"  )

        layout.label(text="Assets File")
        row = layout.row()
        row.scale_y = 1.0
        row.operator( "open.browser_osm"  )


        layout.label(text="")
        row = layout.row()
        row.scale_y = 2.0
        row.operator( "object.import_building_operator",  icon = "WORLD_DATA" )


register_List.append(LayoutPanelB) 











def register():
    for cl in register_List:
        bpy.utils.register_class(cl)
 


def unregister():
    for cl in register_List:
        bpy.utils.unregister_class(cl)
 


if __name__ == "__main__":
    register()
    