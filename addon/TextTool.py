bl_info = {
    "name": "Text Tool",
    "author": "Darkfall",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > UI > Text Tool Tab",
    "description": "Adds a new Text Object with user defined properties",
    "warning": "",
    "wiki_url": "",
    "category": "Add Text",
}

import bpy


class OBJECT_PT_TextTool(bpy.types.Panel):
    bl_label = "Text Tool"
    bl_idname = "OBJECT_PT_texttool"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Text Tool"
    

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row = layout.row()
        row.label(text= "Click the button to add text to")
        row = layout.row()
        row.label(text= "the 3D View.")
        row = layout.row()
        row = layout.row()
        
        row = layout.split(factor= 0.45)
        row.label(text= "")
        row.operator("wm.textopbasic", text= "Add Text", icon= 'OUTLINER_OB_FONT')
        





class OBJECT_PT_Spacing(bpy.types.Panel):
    bl_label = "Spacing"
    bl_idname = "OBJECT_PT_spacing"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Text Tool"
    bl_parentid = "OBJECT_PT_texttool"
    bl_options = {"DEFAULT_CLOSED"}
    

    def draw(self, context):
        layout = self.layout
        text = context.object.data

        row = layout.row()
        row.label(text= "Set the Spacing Options")
        
        row = layout.split(factor= 0.45)
        row.label(text= "Character:")
        row.prop(text, "space_character", text= "")

        row = layout.split(factor= 0.45)
        row.label(text= "Word:")
        row.prop(text, "space_word", text= "")
        
        row = layout.split(factor= 0.45)
        row.label(text= "Line:")
        row.prop(text, "space_line", text= "")
        















class WM_OT_textOpBasic(bpy.types.Operator):
    """Open the Text Tool Dialog Box"""
    bl_idname = "wm.textopbasic"
    bl_label = "                            Text Tool Operator"
    

    
    text : bpy.props.StringProperty(name="Enter Text", default="")
    scale : bpy.props.FloatProperty(name= "Scale", default= 1)
    rotation : bpy.props.BoolProperty(name= "Z up", default= False)
    center : bpy.props.BoolProperty(name= "Center Origin", default= False)
    extrude : bpy.props.BoolProperty(name= "Extrude", default= False)
    extrude_amount : bpy.props.FloatProperty(name= "Extrude Amount", default= 0.06)
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
        
    
        

    def execute(self, context):
        
        t = self.text
        s = self.scale
        c = self.center
        e = self.extrude
        ea = self.extrude_amount
        r = self.rotation
        
        bpy.ops.object.text_add(enter_editmode=True)
        bpy.ops.font.delete(type='PREVIOUS_WORD')
        bpy.ops.font.text_insert(text= t)
        bpy.ops.object.editmode_toggle()
        bpy.context.object.data.size = s
        


        if r == True:
            bpy.context.object.rotation_euler[0] = 1.5708
                    
        if e == True:
            bpy.context.object.data.extrude = ea
        
        if c == True:
            bpy.context.object.data.align_x = 'CENTER'
            bpy.context.object.data.align_y = 'CENTER'


        return {'FINISHED'}

    





def register():
    bpy.utils.register_class(OBJECT_PT_TextTool)
    bpy.utils.register_class(OBJECT_PT_Spacing)
    bpy.utils.register_class(WM_OT_textOpBasic)


def unregister():
    bpy.utils.unregister_class(OBJECT_PT_TextTool)
    bpy.utils.unregister_class(OBJECT_PT_Spacing)
    bpy.utils.unregister_class(WM_OT_textOpBasic)


if __name__ == "__main__":
    register()