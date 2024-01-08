# ##### BEGIN LICENSE BLOCK #####
#
#  Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0) 
#
#  This work is licensed under the Creative Commons
#  Attribution-NonCommercial-NoDerivatives 4.0 International License. 
#
#  To view a copy of this license,
#  visit http://creativecommons.org/licenses/by-nc-nd/4.0/.
#
# ##### END LICENSE BLOCK #####

bl_info = {
    "name": "Text Tool",
    "author": "Darkfall",
    "version": (1, 3),
    "blender": (2, 80, 0),
    "location": "View3D > UI > Text Tool Tab",
    "description": "Adds a new Text Object with user defined properties, Typewriter / Scrolling Text Animation, Radial Curve tool",
    "warning": "",
    "wiki_url": "",
    "category": "Add Text",
}

import bpy
from bpy.types import (Panel, Operator)


class OBJECT_PT_TextTool(Panel):
    bl_label = " "
    bl_idname = "OBJECT_PT_texttool"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Text Tool"
    
    def draw_header(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Text Tool", icon= 'EVENT_T')
    

    def draw(self, context):
        layout = self.layout

        
        layout.label(text= "Click the button to add text to")
        layout.label(text= "the 3D View.")
        
        
        row = layout.split(factor= 0.45)
        row.label(text= "")
        row.operator("wm.textopbasic", text= "Text Tool", icon= 'OUTLINER_OB_FONT')
        
        row = layout.split(factor= 0.45)
        row.label(text= "")
        row.operator("wm.textopcurveradial", text= "Radial Curve", icon= 'CURVE_BEZCIRCLE')
        
        row = layout.row()
        row.operator("wm.textopcurveradialborder", text= "Radial Border Tool", icon= 'CURVE_NCIRCLE')
        
        
        





class OBJECT_PT_Spacing(Panel):
    bl_label = "Spacing"
    bl_idname = "OBJECT_PT_spacing"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Text Tool"
    bl_parentid = "OBJECT_PT_texttool"
    bl_options = {"DEFAULT_CLOSED"}
    
    
    @classmethod
    def poll(cls, context):
        return (context.object != None)
    
    def draw(self, context):
        layout = self.layout
        text = context.object.data
        
        
        
        row = layout.row()
        row.label(text= "Set the Spacing Options")
        
        
        row = layout.row()
        row = layout.split(factor= 0.45)
        row.label(text= "Offset X")
        row.prop(text, "offset_x", text= "")
        
        row = layout.split(factor= 0.45)
        row.label(text= "           Y")
        row.prop(text, "offset_y", text= "")
        
        row = layout.row()
        
        row = layout.split(factor= 0.45)
        row.label(text= "Character:")
        row.prop(text, "space_character", text= "")

        row = layout.split(factor= 0.45)
        row.label(text= "Word:")
        row.prop(text, "space_word", text= "")
        
        row = layout.split(factor= 0.45)
        row.label(text= "Line:")
        row.prop(text, "space_line", text= "")
        


class OBJECT_PT_Animations(Panel):
    bl_label = "Animations"
    bl_idname = "OBJECT_PT_Animation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Text Tool"
    bl_parentid = "OBJECT_PT_texttool"
    bl_options = {"DEFAULT_CLOSED"}

    
    def draw(self, context):
        layout = self.layout
        
        layout.separator(factor=1)
        layout.label(text= "Select your Text then add an")
        layout.label(text= "Animated Effect.")
        layout.separator(factor=1)
        layout.operator("wm.textoptypewriter", text= "Typewriter / Scrolling Text", icon= 'TRACKING_FORWARDS_SINGLE')
        
        
            



class WM_OT_textOpBasic(Operator):
    """Open the Text Tool Dialog Box"""
    bl_idname = "wm.textopbasic"
    bl_label = "                            Text Tool Operator"
    

    
    text : bpy.props.StringProperty(name="", default="")
    scale : bpy.props.FloatProperty(name= "", default= 1)
    rotation : bpy.props.BoolProperty(name= "Orientation", default= False)
    center : bpy.props.BoolProperty(name= "Alignment", default= False)
    extrude : bpy.props.BoolProperty(name= "Extrude", default= False)
    extrude_amount : bpy.props.FloatProperty(name= "Extrude Amount", default= 0.06)
    italic : bpy.props.BoolProperty(name= "Auto Italic", default = False)
    options : bpy.props.BoolProperty(name= "Options", default = False)
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
        
    def draw(self, context):
        layout = self.layout
        layout.separator(factor= 1)
        
        row = layout.row()
        row.label(text= "Enter Text:", icon = 'FILE_TEXT')
        row.prop(self, "text")
        
        row = layout.row()
        row.label(text= "Scale:", icon = 'EMPTY_ARROWS')
        row.prop(self, "scale")
        
        layout.separator(factor= 1)
        
        box = layout.box()
        
        row = box.row()
        row.prop(self, "options")
        if self.options == True:
        
            row = box.row()
            row = box.row()
            row.prop(self, "italic")
            if self.italic == True:
                row.label(text= "Italic: Enabled", icon = 'ITALIC')
            else: 
                row.label(text= "Italic: Not Enabled", icon = 'DRIVER_DISTANCE')
                    
            row = box.row()
            row.prop(self, "rotation")
            if self.rotation == True:
                row.label(text= "Orientation: Z UP", icon= 'EMPTY_SINGLE_ARROW')
            else:
                row.label(text= "Orientation: Default", icon= 'ARROW_LEFTRIGHT')
                    
            
            
            row = box.row()
            row.prop(self, "center")
            if self.center == True:
                row.label(text= "Alignment: Center", icon= 'ALIGN_CENTER')
            else:
                row.label(text= "Alignment: Default", icon= 'ALIGN_LEFT')
            
            
            
            row = box.row()
            row.prop(self, "extrude")
            if self.extrude == True:
                row.prop(self, "extrude_amount")
            
        layout.separator(factor= 1)    
            
        

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
            
        if self.italic == True:
            bpy.context.object.data.shear = 0.38
        
        bpy.context.object.name = self.text + " : (font)"    
    
        return {'FINISHED'}

    



class WM_OT_textOpCurve_Radial(Operator):
    """Open the Curve Text Tool Dialog Box"""
    bl_idname = "wm.textopcurveradial"
    bl_label = "                 Text Tool Operator (Radial Curve)"
    

    
    text : bpy.props.StringProperty(name="", default="")
    scale : bpy.props.FloatProperty(name= "", default= 1)
    rotation : bpy.props.BoolProperty(name= "Orientation", default= False)
    extrude : bpy.props.BoolProperty(name= "Extrude", default= False)
    extrude_amount : bpy.props.FloatProperty(name= "Extrude Amount", default= 0.06)
    flip : bpy.props.BoolProperty(name= "Text Position", default= False)
    options : bpy.props.BoolProperty(name= "Options", default = False)
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
        
    def draw(self, context):
        layout = self.layout
        layout.separator(factor= 1)
        
        row = layout.row()
        row.label(text= "Enter Text:", icon = 'FILE_TEXT')
        row.prop(self, "text")
        
        row = layout.row()
        row.label(text= "Scale:", icon = 'EMPTY_ARROWS')
        row.prop(self, "scale")
        
        layout.separator(factor= 1)
        
        box = layout.box()
        row = box.row()
        row.prop(self, "options")
        if self.options == True:
            row = box.row()
            row = box.row()
            row.prop(self, "flip")
            if self.flip == True:
                row.label(text= "Text on Bottom", icon= 'MOD_CURVE')
            else:
                row.label(text= "Text on Top", icon= 'SPHERECURVE')
                    
            
            
            
            row = box.row()
            row.prop(self, "extrude")
            if self.extrude == True:
                row.prop(self, "extrude_amount")
            
        layout.separator(factor= 1)    
            
        

    def execute(self, context):
        
        t = self.text
        s = self.scale
        e = self.extrude
        ea = self.extrude_amount
        f = self.flip
        
        bpy.ops.curve.primitive_bezier_circle_add()
        obj1 = bpy.context.object
        obj1.name= "Radial Rotation Curve"
        obj1.scale[0] = 3.5
        obj1.scale[1] = 3.5
        obj1.scale[2] = 3.5
        
        

        
        bpy.ops.object.text_add(enter_editmode=True)
        font1 = bpy.context.object
        bpy.ops.font.delete(type='PREVIOUS_WORD')
        bpy.ops.font.text_insert(text= t)
        bpy.ops.object.editmode_toggle()
        bpy.context.object.data.size = s
        

            
            


        
            
        if e == True:
            bpy.context.object.data.extrude = ea
            
        
        bpy.context.object.name = self.text + " : (font)"
        
        bpy.ops.object.modifier_add(type='CURVE')
        bpy.context.object.modifiers["Curve"].object = obj1
           
        
        if f == True:
            bpy.context.object.data.offset_x = -1.48
            bpy.context.object.data.offset_y = -0.98
            bpy.context.object.rotation_euler[0] = 3.14159
            bpy.context.object.rotation_euler[1] = 3.14159



        else:
            bpy.context.object.data.offset_x = 9.48
            bpy.context.object.data.offset_y = 0.37
    
        
        

        return {'FINISHED'}






class WM_OT_textOpCurve_Radial_Border(Operator):
    """Open the Curve Text Tool Dialog Box"""
    bl_idname = "wm.textopcurveradialborder"
    bl_label = "                 Text Tool Operator (Radial Border)"
    

    preset_enum : bpy.props.EnumProperty(
        name="",
        description="Select a Style to be used.",
        items=[ ('OP1', "Solid Line ________", ""),
                ('OP2', "Dots .........", ""),
                ('OP3', "Arrows  ^^^^^^^", ""),
                ('OP4', "Circles  OoOoOoOoOoOo", ""),
               ]
        )
        
    text : bpy.props.StringProperty(name = "")
    use_custom : bpy.props.BoolProperty(name = "Use Custom Character")
        
    
    
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
        
    def draw(self, context):
        layout = self.layout
        layout.separator(factor= 1)
        
        row = layout.row()
        row.label(text= "Select Border Style:", icon = 'RESTRICT_SELECT_OFF')
        row = layout.row()
        if self.use_custom != True:
            row.prop(self, "preset_enum")   
        
        layout.separator(factor= 1)
        
        box = layout.box()
        row = box.row()
        row.prop(self, "use_custom")
        if self.use_custom == True: 
            row = box.row()
            row.label(text= "Enter Character:")
            row.prop(self, "text")
            row = box.row()

        
            
            
        layout.separator(factor= 1)    
            
        

    def execute(self, context):
        
        
        bpy.ops.curve.primitive_bezier_circle_add()
        obj = bpy.context.object
        obj.name= "Radial Rotation Curve"
        obj.scale[0] = 3.5
        obj.scale[1] = 3.5
        obj.scale[2] = 3.5
        
        

        
        bpy.ops.object.text_add(enter_editmode=True)
        font = bpy.context.object
        bpy.ops.font.delete(type='PREVIOUS_WORD')
        
        if self.use_custom == True:
            bpy.ops.font.text_insert(text= self.text)
            
        else:    
            if self.preset_enum == 'OP1':
                bpy.ops.font.text_insert(text= "_")
                font.data.offset_y = -7.23

                
                
            if self.preset_enum == 'OP2':
                bpy.ops.font.text_insert(text= ".")
                

                bpy.context.object.data.offset_y = -7.23

      
            if self.preset_enum == 'OP3':
                bpy.ops.font.text_insert(text= "^")
                bpy.context.object.data.space_character = 0.907
                bpy.context.object.data.offset_y = -0.2
            
            if self.preset_enum == 'OP4':
                bpy.ops.font.text_insert(text= "Oo")
                bpy.context.object.data.space_character = 0.907
                bpy.context.object.data.offset_y = -0.2
                bpy.context.object.data.size = 0.3985
            
            

        
        
        bpy.ops.object.editmode_toggle()
        
        

            
        
        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.object.modifiers["Array"].fit_type = 'FIT_CURVE'

        bpy.context.object.modifiers["Array"].curve = obj


        
        bpy.ops.object.modifier_add(type='CURVE')
        bpy.context.object.modifiers["Curve"].object = obj
        
        if self.preset_enum == 'OP2':
            
            bpy.context.object.modifiers["Array"].relative_offset_displace[0] = 1.696
            
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)


        return {'FINISHED'}

















class WM_OT_textOpTypewriter(Operator):
    """Open the Typewriter / Scrolling Text Dialog Box. Note: The Text will be Converted to a Mesh"""
    bl_idname = "wm.textoptypewriter"
    bl_label = "             Text Tool Operator (Typewriter Effect)"
    

    
    
    start_frame : bpy.props.IntProperty(name= "", default= 1)
    anim_duration : bpy.props.IntProperty(name= "", default= 25)
    
    
    
    
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
        
    def draw(self, context):
        layout = self.layout
        layout.separator(factor= 1)
        
        
        row = layout.row()
        row.label(text= "Start Frame:", icon = 'FRAME_NEXT')
        row.prop(self, "start_frame")
        
        row = layout.row()
        row.label(text= "Duration (frames):", icon = 'TIME')
        row.prop(self, "anim_duration")
        
        layout.separator(factor= 2)
                    
        

    def execute(self, context):   
            
        obj = bpy.context.object    
        
        bpy.ops.object.convert(target='MESH')
        bpy.ops.object.modifier_add(type='BUILD')
        obj.modifiers["Build"].frame_start = self.start_frame
        obj.modifiers["Build"].frame_duration = self.anim_duration

        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.sort_elements(type='VIEW_XAXIS', elements={'FACE'})
        bpy.ops.object.editmode_toggle()
        
        return {'FINISHED'}









classes = [OBJECT_PT_TextTool, OBJECT_PT_Animations, OBJECT_PT_Spacing, WM_OT_textOpBasic, WM_OT_textOpCurve_Radial, WM_OT_textOpTypewriter, WM_OT_textOpCurve_Radial_Border]



def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()