
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

 



register_List= []


class OpenBrowserOSM(bpy.types.Operator):
    bl_idname = "open.browser_osm"
    bl_label = "get OSM file"

    filepath = bpy.props.StringProperty(subtype="FILE_PATH") 
    #somewhere to remember the address of the file


    def execute(self, context):
        display = "filepath= "+ str(self.filepath  )
        print(display) #Prints to console  
        #Window>>>Toggle systen console

        return {'FINISHED'}

    def invoke(self, context, event): # See comments at end  [1]

        context.window_manager.fileselect_add(self) 
        #Open browser, take reference to 'self' 
        #read the path to selected file, 
        #put path in declared string type data structure self.filepath

        return {'RUNNING_MODAL'}  
        # Tells Blender to hang on for the slow user input


bpy.utils.register_class(OpenBrowserOSM) 
#Tell Blender this exists and should be used

class OpenBrowserAssets(bpy.types.Operator):
    bl_idname = "open.browser_assets"
    bl_label = "get Assets file"

    filepath = bpy.props.StringProperty(subtype="FILE_PATH") 
    #somewhere to remember the address of the file


    def execute(self, context):
        scanFile(self.filepath)
        display = "filepath= "+ str(self.filepath   )
        print(display) #Prints to console  
        #Window>>>Toggle systen console

        return {'FINISHED'}

    def invoke(self, context, event): # See comments at end  [1]

        context.window_manager.fileselect_add(self) 
        #Open browser, take reference to 'self' 
        #read the path to selected file, 
        #put path in declared string type data structure self.filepath

        return {'RUNNING_MODAL'}  
        # Tells Blender to hang on for the slow user input


bpy.utils.register_class(OpenBrowserAssets) 
#Tell Blender this exists and should be used

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
    bl_idname = __name__#"PT_UniPaderpornRtm"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Scenery Generator new"

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
        layout.label(text="OSM File")
        row = layout.row()
        row.scale_y = 1.0
        row.operator( "open.browser_osm"  )

        layout.label(text="Assets File")
        row = layout.row()
        row.scale_y = 1.0
        row.operator( "open.browser_assets"  )


        layout.label(text="")
        row = layout.row()
        row.scale_y = 2.0
        row.operator( "object.import_building_operator",  icon = "WORLD_DATA" )


register_List.append(LayoutPanel) 

def register():
    for cl in register_List:
        bpy.utils.register_class(cl)
 


def unregister():
    for cl in register_List:
        bpy.utils.unregister_class(cl)
 


if __name__ == "__main__":
    register()
    