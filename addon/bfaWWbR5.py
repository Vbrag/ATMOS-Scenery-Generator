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
    "name": "Shader Library",
    "author": "Darkfall",
    "version": (1, 9),
    "blender": (2, 90, 1),
    "location": "View3D > Toolshelf",
    "description": "Select from the Various Different Shaders, and they will be addded to your selected object",
    "warning": "",
    "wiki_url": "",
    "category": "Add Shader",
}

import bpy
from bpy.types import (Panel, Operator, Menu, PropertyGroup)
from bpy.props import (PointerProperty, FloatProperty, FloatVectorProperty, BoolProperty, BoolVectorProperty, StringProperty, IntProperty, EnumProperty)

class ShaderLibraryProperties(PropertyGroup):
    
    planet_type: EnumProperty(
        name="Planet Type:",
        description="Select A Planet Type.",
        items=[ ('OP2', "Continental World", "An Earth-like Planet"),
                ('OP3', "Dust World", "A Barren Planet"),
                ('OP4', "Moon", "A Moon"),
                ('OP5', "Rocky World", "A Rocky Planet"),
                ('OP6', "Stars", "Uhm, Stars!"),
                ('OP7', "Golden World", "A Sci-fi Planet with a Golden Theme"),
                ('OP8', "Icy World", "An Icy Planet"),
               ]
        )

class ShaderMainPanel(Panel):
    bl_label = " "
    bl_idname = "SHADER_PT_MAINPANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Shader Library'

    def draw_header(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="The Shader Library", icon= 'NODE_MATERIAL')
        
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row = layout.row()
        row.label(text= "Select a Shader to be added.")
        row = layout.row()
        #row.label(text= "(Press Shift F - for Shortcut)")
        row.label(text= "                                           (ver 1.09)")

class SubPanelCosmic(Panel):
    bl_label = "Cosmic Shaders"
    bl_idname = "SHADER_PT_COSMICSHADERS"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Shader Library'
    bl_parent_id = 'SHADER_PT_MAINPANEL'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        
        layout.scale_y = 1.1
        row = layout.row()
        row.label(text= "Select a Cosmic Shader.")
        row = layout.row()
        row.prop(mytool, "planet_type")
        row = layout.row()
        row.operator("wm.cosmicop", icon= 'WORLD', text= "Add Cosmic Shader")
        row = layout.row()

class SubPanelPreciousMetals(Panel):
    bl_label = "Gemstones"
    bl_idname = "SHADER_PT_PRECIOUSMETALS"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Shader Library'
    bl_parent_id = 'SHADER_PT_MAINPANEL'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.1
        row = layout.row()
        row.label(text= "Select a Gemstone Shader.")
        row = layout.row()
        row.operator("wm.diamondop", icon= 'DECORATE_ANIMATE', text= "Diamond")
        row = layout.row()

class SubPanelMaterials(Panel):
    bl_label = "Materials"
    bl_idname = "SHADER_PT_MATERIALS"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Shader Library'
    bl_parent_id = 'SHADER_PT_MAINPANEL'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.1
        row = layout.row()
        row.label(text= "Select a Basic Material Shader.")
        row = layout.row()
        row = layout.row()
        row.operator("wm.leatherop", icon= 'OUTLINER_OB_SURFACE', text= "Leather")
        row = layout.row()
        row.operator("shader.brick_operator", icon= 'MOD_BUILD', text= "Brick")

class SubPanelMetals(Panel):
    bl_label = "Metallics"
    bl_idname = "SHADER_PT_METALS"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Shader Library'
    bl_parent_id = 'SHADER_PT_MAINPANEL'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.1
        row = layout.row()
        row.label(text= "Select a Basic Metallic Shader.")
        row = layout.row()
        row = layout.row()
        row.operator('shader.gold_operator', icon= 'KEYTYPE_KEYFRAME_VEC')
        row.operator('shader.silver_operator', icon= 'HANDLETYPE_FREE_VEC')
        row.operator('shader.copper_operator', icon= 'KEYTYPE_EXTREME_VEC')
        row = layout.row()
        row.operator('shader.scifigold_operator', icon= 'COLORSET_09_VEC')

class SubPanelStylized(Panel):
    bl_label = "Stylized"
    bl_idname = "SHADER_PT_STYLIZED"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Shader Library'
    bl_parent_id = 'SHADER_PT_MAINPANEL'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.1
        row = layout.row()
        row.label(text= "Select a Stylized Shader.")
        row = layout.row()
        row.operator("shader.cloud_operator", icon= 'OUTLINER_DATA_VOLUME', text= "Clouds")
        row = layout.row()
        row.operator("wm.ghostop", icon= 'GHOST_ENABLED', text= "Ghost")
        row.operator("wm.hologramop", icon= 'USER', text= "Hologram")
        row = layout.row()
        row.operator("wm.neonop", icon= 'PARTICLE_PATH', text= "Neon")
        row = layout.row()
        row.operator("wm.potionop", icon= 'SORTTIME', text= "Stylized Potion")
        row = layout.row()

class SHADER_OT_COSMIC(Operator):
    """Open the Cosmic Shader Dialog box"""
    bl_label = "             Cosmic Operator"
    bl_idname = "wm.cosmicop"
    bl_options = {'REGISTER', 'UNDO'}
    
    col1 : FloatVectorProperty(name='Color Tint',subtype='COLOR_GAMMA',size=4,default=(1,1,1,1), min= 0, max= 1)
    v_col : FloatVectorProperty(name='Variation Col',subtype='COLOR_GAMMA',size=4, default=(0.181135, 1, 0.0857819, 1), min= 0, max= 1)
    v_bool : BoolProperty(default= False, name= "Enable Color Variation Options")
    v_scale : FloatProperty(default= 8, name= "Variation Size", min= 5, max= 10 )
    atmos : BoolProperty(default= True, name= "Enable Atmospheric Glow")
    m_atmos : BoolProperty(default= True, name= "Enable Atmospheric Glow")
    land_scale : FloatProperty(default= 5)
    land_hue : FloatProperty(default= 0.5, min= 0, max= 1)
    land_sat : FloatProperty(default= 1, min= 0, max= 1)
    d_hue : FloatProperty(default= 0.5, min= 0, max= 1)
    cloud_bool : BoolProperty(default= False, name= "Enable Clouds")
    cloud_scale : FloatProperty(default= 55.400, name= "Cloud Size")
    cloud_vis : FloatProperty(default= 1, name= "Cloud Visibility", min= 0, max= 1)
    atmos_glow : FloatProperty(default= 6.500)
    atmos_col : FloatVectorProperty(default= (0, 0.141263, 0.904661, 1), name='Atmos Color',subtype='COLOR_GAMMA',size=4, min= 0, max= 1)
    d_atmos_col : FloatVectorProperty(default= (0.552012, 0.130136, 0.0451862, 1), name='Atmos Color',subtype='COLOR_GAMMA',size=4)
    d_atmos_glow : FloatProperty(default= 6.500)
    m_atmos_col : FloatVectorProperty(default= (1,1,1,1), name='Atmos Color',subtype='COLOR_GAMMA',size=4, min= 0, max= 1)
    m_atmos_glow : FloatProperty(default= 1.05)
    star_scale : FloatProperty(default= 614)
    m_macro_scale : FloatProperty(default= 8.6, description= "Scale the Macro Surface Detail")
    m_micro_scale : FloatProperty(default= 7.6, description= "Scale the Micro Surface Detail")
    m_seed : FloatProperty(default= 0.5, description= "Generate a Random Variation based of this seed value")
    star_coverage : FloatProperty(default= 0.674, min=0.628, max= 1)
    water_lvl : FloatProperty(default= 0.492, min= 0.35, max= 0.515)
    stripe_amount : FloatProperty(default= 3.500, min= 0, max= 30)
    shadow_bool : BoolProperty(default= False, name= "Enable Shadow")
    m_shadow_bool : BoolProperty(default= False, name= "Enable Shadow", description= "Enable a Shadow simulating Day/Night")
    city_bool : BoolProperty(default= False, name= "Enable City Lights")
    city_lights : FloatProperty(default= 21.980, name= "Scale")
    city_brightness : FloatProperty(default= 7.9, name= "Light Strength")
    shadow_coverage : FloatProperty(default= 0, min= -1, max= 1)
    shadow_vis : FloatProperty(default= 0.962, min= 0.3, max= 1)
    m_shadow_coverage : FloatProperty(default= 0.5, min= 0.046, max= 1)
    m_shadow_vis : FloatProperty(default= 0.962, min= 0.3, max= 1)
    r_scale : FloatProperty(default= 7, min= 1, max= 20, name= "Scale")
    r_soften : FloatProperty(default= 0.150, min= 0, max= 1, name= "Soften Landmass")
    r_land_height : FloatProperty(default= 0.337, min= 0.041, max= 0.4)
    r_land_col1 : FloatVectorProperty(name='Color 1',subtype='COLOR_GAMMA',size=4,default=(0.38643, 0.0953075, 0.0251869, 1), min= 0, max= 1)
    r_land_col2 : FloatVectorProperty(name='Color 2',subtype='COLOR_GAMMA',size=4,default=(1, 0.533275, 0.0666201, 1), min= 0, max= 1)
    r_land_col3 : FloatVectorProperty(name='Color 3',subtype='COLOR_GAMMA',size=4,default=(1, 0.930111, 0.428691, 1), min= 0, max= 1)
    r_land_col4 : FloatVectorProperty(name='Color 4',subtype='COLOR_GAMMA',size=4,default=(0.991102, 1, 0.366253, 1), min= 0, max= 1)
    r_water_col : FloatVectorProperty(name='Water Color',subtype='COLOR_GAMMA',size=4,default=(0.144129, 0.0802198, 0, 1), min= 0, max= 1)
    r_atmos : BoolProperty(default= True, name= "Enable Atmospheric Glow")
    r_atmos_col : FloatVectorProperty(default= (0.513397, 0.30397, 0.118823, 1), name='Atmos Color',subtype='COLOR_GAMMA',size=4, min= 0, max= 1)
    r_atmos_glow : FloatProperty(default= 1.280)
    g_scale : FloatProperty(default= 4.861, min= 1, max= 20, name= "Scale")
    g_soften : FloatProperty(default= 0.318, min= 0, max= 1, name= "Soften Landmass")
    g_land_height : FloatProperty(default= 0.154, min= 0.041, max= 0.4)
    g_land_col1 : FloatVectorProperty(name='Color 1',subtype='COLOR_GAMMA',size=4,default=(0.198069, 0.0953075, 0.0703601, 1), min= 0, max= 1)
    g_land_col2 : FloatVectorProperty(name='Color 2',subtype='COLOR_GAMMA',size=4,default=(0.48515, 0.238398, 0.0648033, 1), min= 0, max= 1)
    g_land_col3 : FloatVectorProperty(name='Color 3',subtype='COLOR_GAMMA',size=4,default=(1, 0.467784, 0.066626, 1), min= 0, max= 1)
    g_land_col4 : FloatVectorProperty(name='Color 4',subtype='COLOR_GAMMA',size=4,default=(1, 0.745404, 0.23074, 1), min= 0, max= 1)
    g_water_col : FloatVectorProperty(name='Water Color',subtype='COLOR_GAMMA',size=4,default=(0.144129, 0.0802198, 0, 1), min= 0, max= 1)
    g_atmos : BoolProperty(default= True, name= "Enable Atmospheric Glow")
    g_atmos_col : FloatVectorProperty(default= (1, 0.693872, 0.212231, 1), name='Atmos Color',subtype='COLOR_GAMMA',size=4, min= 0, max= 1)
    g_atmos_glow : FloatProperty(default= 2.420)
    i_scale : FloatProperty(default= 3.692, min= 1, max= 20, name= "Scale")
    i_soften : FloatProperty(default= 0.238, min= 0, max= 1, name= "Soften Landmass")
    i_land_height : FloatProperty(default= 0.238, min= 0.041, max= 0.4)
    i_land_col1 : FloatVectorProperty(name='Color 1',subtype='COLOR_GAMMA',size=4,default=(0.00334653, 0.0152085, 0.0975874, 1), min= 0, max= 1)
    i_land_col2 : FloatVectorProperty(name='Color 2',subtype='COLOR_GAMMA',size=4,default=(0.0409151, 0.304987, 0.48515, 1), min= 0, max= 1)
    i_land_col3 : FloatVectorProperty(name='Color 3',subtype='COLOR_GAMMA',size=4,default=(0.381326, 0.527115, 1, 1), min= 0, max= 1)
    i_land_col4 : FloatVectorProperty(name='Color 4',subtype='COLOR_GAMMA',size=4,default=(0.745404, 0.991102, 1, 1), min= 0, max= 1)
    i_water_col : FloatVectorProperty(name='Water Color',subtype='COLOR_GAMMA',size=4,default=(0.0122865, 0.0343398, 0.0802199, 1), min= 0, max= 1)
    i_atmos : BoolProperty(default= True, name= "Enable Atmospheric Glow")
    i_atmos_col : FloatVectorProperty(default= (0.0761853, 0.456411, 1, 1), name='Atmos Color',subtype='COLOR_GAMMA',size=4, min= 0, max= 1)
    i_atmos_glow : FloatProperty(default= 2.420)
    c_shader_type : EnumProperty(
        name="Shader Type:",
        description="Select a Shader Type",
        items=[ ('OP1', "Emission", ""),
                ('OP2', "Principled", ""),
               ]
        )
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        
        if mytool.planet_type == 'OP2':
            layout.prop(self, "c_shader_type", text= "Shader Type", expand= True)
            layout.prop(self, "land_hue", slider= True, text= "Land Hue")
            layout.prop(self, "land_sat", slider= True, text= "Land Saturation")
            layout.prop(self, "land_scale", text= "Land Scale")
            layout.prop(self, "water_lvl", slider= True, text= "Water Level")
            layout.prop(self, "v_bool")
            if self.v_bool == True:
                layout.prop(self, "v_col")
                layout.prop(self, "v_scale", slider= True)
            layout.prop(self, "shadow_bool")
            if self.shadow_bool == True:
                layout.prop(self, "shadow_coverage", slider= True, text= "Shadow Position")
                layout.prop(self, "shadow_vis", slider= True, text= "Shadow Visibility")
                layout.prop(self, "city_bool")
                if self.city_bool == True:
                    layout.prop(self, "city_lights")
                    layout.prop(self, "city_brightness")         
            layout.prop(self, "atmos")
            if self.atmos == True:
                layout.prop(self, "atmos_col", text= "Atmos Color")
                layout.prop(self, "atmos_glow", text= "Glow Amount")
            layout.prop(self, "cloud_bool")    
            if self.cloud_bool == True:
                layout.prop(self, "cloud_scale")
                layout.prop(self, "cloud_vis", slider= True)
        
        if mytool.planet_type == 'OP3':
            layout.prop(self, "d_hue", text= "Planet Hue", slider= True)
            layout.prop(self, "stripe_amount", text= "Stripe Amount", slider= True)
            layout.prop(self, "atmos")
            if self.atmos == True:
                layout.prop(self, "d_atmos_col", text= "Atmos Color")
                layout.prop(self, "d_atmos_glow", text= "Glow Amount")    
                
        if mytool.planet_type == 'OP4':
            layout.prop(self, "m_seed", text= "Seed")
            layout.prop(self, "m_macro_scale", text= "Moon Macro Scale")
            layout.prop(self, "m_micro_scale", text= "Moon Micro Scale")
            layout.prop(self, "m_atmos")
            if self.m_atmos == True:
                layout.prop(self, "m_atmos_col", text= "Atmos Color")
                layout.prop(self, "m_atmos_glow", text= "Glow Amount")
            layout.prop(self, "m_shadow_bool")
            if self.m_shadow_bool == True:
                layout.prop(self, "m_shadow_coverage", text= "Shdow Position", slider= True)
                layout.prop(self, "m_shadow_vis", text= "Shdow Visibility", slider= True)
                 
        if mytool.planet_type == 'OP5':
            layout.prop(self, "r_scale", text= "Noise Scale", slider= True)
            layout.prop(self, "r_land_height", text= "Land Height", slider= True)
            layout.prop(self, "r_land_col1", text= "Land Color 1")
            layout.prop(self, "r_land_col2", text= "Land Color 2")
            layout.prop(self, "r_land_col3", text= "Land Color 3")
            layout.prop(self, "r_land_col4", text= "Land Color 4")
            layout.prop(self, "r_water_col", text= "Water Color")
            layout.prop(self, "r_soften", text= "Soften Noise Pattern", slider= True)
            layout.prop(self, "r_atmos", text= "Enable Atmospheric Glow")
            if self.r_atmos == True:
                layout.prop(self, "r_atmos_col", text= "Amospheric Color")
                layout.prop(self, "r_atmos_glow", text= "Atmos Strength")
        
        if mytool.planet_type == 'OP6':
            layout.prop(self, "star_scale", text= "Star Scale")
            layout.prop(self, "star_coverage", slider= True, text= "Star Density")
            
        if mytool.planet_type == 'OP7':
            layout.prop(self, "g_scale", text= "Noise Scale", slider= True)
            layout.prop(self, "g_land_height", text= "Land Height", slider= True)
            layout.prop(self, "g_land_col1", text= "Land Color 1")
            layout.prop(self, "g_land_col2", text= "Land Color 2")
            layout.prop(self, "g_land_col3", text= "Land Color 3")
            layout.prop(self, "g_land_col4", text= "Land Color 4")
            layout.prop(self, "g_water_col", text= "Water Color")
            layout.prop(self, "g_soften", text= "Soften Noise Pattern", slider= True)
            layout.prop(self, "g_atmos", text= "Enable Atmospheric Glow")
            if self.g_atmos == True:
                layout.prop(self, "g_atmos_col", text= "Amospheric Color")
                layout.prop(self, "g_atmos_glow", text= "Atmos Strength") 
        
        if mytool.planet_type == 'OP8':
            layout.prop(self, "i_scale", text= "Noise Scale", slider= True)
            layout.prop(self, "i_land_height", text= "Land Height", slider= True)
            layout.prop(self, "i_land_col1", text= "Land Color 1")
            layout.prop(self, "i_land_col2", text= "Land Color 2")
            layout.prop(self, "i_land_col3", text= "Land Color 3")
            layout.prop(self, "i_land_col4", text= "Land Color 4")
            layout.prop(self, "i_water_col", text= "Water Color")
            layout.prop(self, "i_soften", text= "Soften Noise Pattern", slider= True)
            layout.prop(self, "i_atmos", text= "Enable Atmospheric Glow")
            if self.i_atmos == True:
                layout.prop(self, "i_atmos_col", text= "Amospheric Color")
                layout.prop(self, "i_atmos_glow", text= "Atmos Strength")         
                        
    
    def execute(self, context):
        c = self.col1
        cv = self.cloud_vis
        scene = context.scene
        mytool = scene.my_tool
        
        if mytool.planet_type == 'OP1':
            material_cosmic = bpy.data.materials.new(name= "Coming Soon")
            material_cosmic.use_nodes = True
            material_cosmic.node_tree.nodes.remove(material_cosmic.node_tree.nodes.get('Principled BSDF'))
            material_output = material_cosmic.node_tree.nodes.get('Material Output')
            material_output.location = (1000,0)
            glass1_node = material_cosmic.node_tree.nodes.new('ShaderNodeBsdfGlass')
            glass1_node.location = (-600,0)
            glass1_node.inputs[0].default_value = (1, 0, 0, 1)
            glass1_node.inputs[2].default_value = 1.446
            #material_cosmic.node_tree.links.new(glass1_node.outputs[0], add1_node.inputs[0])
            #material_cosmic.node_tree.links.new(mix1_node.outputs[0], material_output.inputs[0])
            bpy.context.object.active_material = material_cosmic
            bpy.context.object.active_material.diffuse_color = c
            bpy.context.object.active_material.metallic = 0.3
        
        if mytool.planet_type == 'OP2':
            if self.c_shader_type== 'OP1':
                material_cosmic2 = bpy.data.materials.new(name= "Continental")
                material_cosmic2.use_nodes = True
                material_cosmic2.node_tree.nodes.remove(material_cosmic2.node_tree.nodes.get('Principled BSDF'))
                material_output = material_cosmic2.node_tree.nodes.get('Material Output')
                material_output.location = (3200,0)
                noise1_node = material_cosmic2.node_tree.nodes.new('ShaderNodeTexNoise')
                noise1_node.location = (-1000,0)
                noise1_node.inputs[2].default_value = self.land_scale
                noise1_node.inputs[3].default_value = 16
                noise1_node.inputs[4].default_value = 0.848
                noise1_node.inputs[5].default_value = 0
                noise2_node = material_cosmic2.node_tree.nodes.new('ShaderNodeTexNoise')
                noise2_node.location = (-800, 0)
                noise2_node.inputs[2].default_value = 12.5
                noise2_node.inputs[3].default_value = 2
                noise2_node.inputs[4].default_value = 0.890
                noise2_node.inputs[5].default_value = 0
                cr1_node = material_cosmic2.node_tree.nodes.new('ShaderNodeValToRGB')
                cr1_node.location = (-900, -200)
                cr1_node.color_ramp.elements[0].position= 0.133
                cr1_node.color_ramp.elements[1].position= self.water_lvl
                cr1_node.color_ramp.elements.new(position= 0.516)
                cr2_node = material_cosmic2.node_tree.nodes.new('ShaderNodeValToRGB')
                cr2_node.location = (-650, -200)
                cr2_node.color_ramp.elements[0].position= 0.505
                cr2_node.color_ramp.elements[1].position= 0.650
                mixrgb_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMixRGB')
                mixrgb_node.location = (-600, 0)
                mixrgb_node.inputs[2].default_value = (0, 0.0202886, 0.502886, 1)
                multiply_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMixRGB')
                multiply_node.location = (-400, 200)
                multiply_node.blend_type = 'BURN'
                multiply_node.inputs[2].default_value = (0.391573, 0.799103, 0, 1)
                hue_node = material_cosmic2.node_tree.nodes.new('ShaderNodeHueSaturation')
                hue_node.location = (800, 100)
                hue_node.inputs[0].default_value = self.land_hue
                hue_node.inputs[1].default_value = self.land_sat
                cr3_node = material_cosmic2.node_tree.nodes.new('ShaderNodeValToRGB')
                cr3_node.location = (-400, -200)
                cr3_node.color_ramp.elements[0].position= 0.402
                cr3_node.color_ramp.elements[1].position= 0.418
                overlay_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMixRGB')
                overlay_node.location = (1000, 0)
                overlay_node.blend_type = 'LIGHTEN'
                overlay_node.inputs[2].default_value = (0, 0.0152085, 0.0528607, 1)
                dark_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMixRGB')
                dark_node.location = (1200, 0)
                dark_node.blend_type = 'DARKEN'
                dark_node.inputs[2].default_value = (0,0,0,1)
                dark_node.use_clamp = True
                if self.shadow_bool == False:
                    dark_node.mute= True
                grad1_node = material_cosmic2.node_tree.nodes.new('ShaderNodeTexGradient')
                grad1_node.location= (800, 500)
                mapping2_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMapping')
                mapping2_node.location = (600, 500)
                mapping2_node.inputs[1].default_value[0] = self.shadow_coverage
                mapping2_node.inputs[3].default_value[0] = 1
                mapping2_node.inputs[3].default_value[1] = 1
                mapping2_node.inputs[3].default_value[2] = 1
                coord2_node = material_cosmic2.node_tree.nodes.new('ShaderNodeTexCoord')
                coord2_node.location = (400, 500)
                sv = self.shadow_vis
                cr7_node = material_cosmic2.node_tree.nodes.new('ShaderNodeValToRGB')
                cr7_node.location = (1200, 300)
                cr7_node.color_ramp.elements[0].position= 0.096
                cr7_node.color_ramp.elements[1].position= 0.551
                cr7_node.color_ramp.elements[1].color= (sv, sv, sv, 1)
                cr8_node = material_cosmic2.node_tree.nodes.new('ShaderNodeValToRGB')
                cr8_node.location = (1400, 500)
                cr8_node.color_ramp.elements[0].position= 0.421
                cr8_node.color_ramp.elements[1].position= 0.435
                cr8_node.color_ramp.elements[0].color= (1,1,1,1)
                cr8_node.color_ramp.elements[1].color= (0,0,0,1)
                math2_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMath')
                math2_node.location = (1700, 600)
                math2_node.operation = 'SUBTRACT'
                math3_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMath')
                math3_node.location = (1500, 700)
                math3_node.operation = 'MULTIPLY'
                math4_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMath')
                math4_node.location = (900, 900)
                math4_node.operation = 'MULTIPLY'
                cr9_node = material_cosmic2.node_tree.nodes.new('ShaderNodeValToRGB')
                cr9_node.location = (600, 900)
                cr9_node.color_ramp.elements[0].position= 0.598
                cr9_node.color_ramp.elements[1].position= 0.606
                noise4_node = material_cosmic2.node_tree.nodes.new('ShaderNodeTexNoise')
                noise4_node.location = (400, 900)
                noise4_node.inputs[2].default_value = 96.100
                noise4_node.inputs[3].default_value = 2
                noise4_node.inputs[4].default_value = 1
                noise4_node.inputs[5].default_value = 2.4
                math5_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMath')
                math5_node.location = (200, 900)
                math5_node.operation = 'ADD'
                musgrave2_node = material_cosmic2.node_tree.nodes.new('ShaderNodeTexMusgrave')
                musgrave2_node.location = (0, 1000)
                musgrave2_node.inputs[2].default_value = self.city_lights
                musgrave2_node.inputs[3].default_value = 2
                musgrave2_node.inputs[4].default_value = 2
                musgrave2_node.inputs[5].default_value = 2
                musgrave3_node = material_cosmic2.node_tree.nodes.new('ShaderNodeTexMusgrave')
                musgrave3_node.location = (0, 800)
                musgrave3_node.inputs[2].default_value = -5.80
                musgrave3_node.inputs[3].default_value = 2
                musgrave3_node.inputs[4].default_value = 9.2
                musgrave3_node.inputs[5].default_value = 9.8
                mixs3_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMixShader')
                mixs3_node.location = (3000, 0)
                if self.city_bool == False:
                    mixs3_node.mute= True
                emiss4_node = material_cosmic2.node_tree.nodes.new('ShaderNodeEmission')
                emiss4_node.location = (2800, -200)
                emiss4_node.inputs[1].default_value = self.city_brightness
                mixrgb3_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMixRGB')
                mixrgb3_node.location = (2600, -200)
                mixrgb3_node.inputs[2].default_value = (1, 0.694074, 0.220557, 1)
                cr10_node = material_cosmic2.node_tree.nodes.new('ShaderNodeValToRGB')
                cr10_node.location = (2800, 500)
                cr10_node.color_ramp.elements[1].position= 0.027
                emiss1_node = material_cosmic2.node_tree.nodes.new('ShaderNodeEmission')
                emiss1_node.location = (1700, 200)
                emiss1_node.inputs[1].default_value = 2.800
                emiss2_node = material_cosmic2.node_tree.nodes.new('ShaderNodeEmission')
                emiss2_node.location = (1900, -200)
                emiss2_node.inputs[0].default_value = self.atmos_col
                emiss2_node.inputs[1].default_value = self.atmos_glow
                emiss3_node = material_cosmic2.node_tree.nodes.new('ShaderNodeEmission')
                emiss3_node.location = (1900, 0)
                emiss3_node.inputs[0].default_value = (1, 1, 1, 1)
                emiss3_node.inputs[1].default_value = 6.500
                mixs2_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMixShader')
                mixs2_node.location = (2500, 0)
                if self.cloud_bool == False:
                    mixs2_node.mute= True
                lweight_node = material_cosmic2.node_tree.nodes.new('ShaderNodeLayerWeight')
                lweight_node.location = (2200, 400)
                lweight_node.inputs[0].default_value = 0.370
                cr4_node = material_cosmic2.node_tree.nodes.new('ShaderNodeValToRGB')
                cr4_node.location = (2500, 400)
                cr4_node.color_ramp.elements[0].position= 0.056739
                mixs_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMixShader')
                mixs_node.location = (2700, 0)
                if self.atmos == False: 
                    mixs_node.mute= True
                cr5_node = material_cosmic2.node_tree.nodes.new('ShaderNodeValToRGB')
                cr5_node.location = (-400, -500)
                cr5_node.color_ramp.elements[0].position= 0.540761
                cr5_node.color_ramp.elements[1].position= 0.769022
                cr5_node.color_ramp.elements[1].color = (cv, cv, cv, cv)
                noise3_node = material_cosmic2.node_tree.nodes.new('ShaderNodeTexNoise')
                noise3_node.location = (-600, -500)
                noise3_node.inputs[2].default_value = self.cloud_scale
                noise3_node.inputs[3].default_value = 7.100
                noise3_node.inputs[4].default_value = 0.995
                noise3_node.inputs[5].default_value = 0.8
                mapping_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMapping')
                mapping_node.location = (-800, -500)
                mapping_node.inputs[3].default_value[0] = 0.18
                mapping_node.inputs[3].default_value[1] = 0.18
                mapping_node.inputs[3].default_value[2] = 0.18
                coord_node = material_cosmic2.node_tree.nodes.new('ShaderNodeTexCoord')
                coord_node.location = (-1000, -500)
                mixrgb2_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMixRGB')
                mixrgb2_node.location = (600, 0)
                mixrgb2_node.inputs[2].default_value = self.v_col
                math_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMath')
                math_node.location = (400, 0)
                math_node.operation = 'MULTIPLY'
                musgrave1_node = material_cosmic2.node_tree.nodes.new('ShaderNodeTexMusgrave')
                musgrave1_node.location = (200, -200)
                musgrave1_node.inputs[2].default_value = self.v_scale
                musgrave1_node.inputs[3].default_value = 16
                musgrave1_node.inputs[4].default_value = 0.030
                musgrave1_node.inputs[5].default_value = 1.2
                musgrave1_node.musgrave_type = 'MULTIFRACTAL'
                cr6_node = material_cosmic2.node_tree.nodes.new('ShaderNodeValToRGB')
                cr6_node.location = (200, 200)
                cr6_node.color_ramp.elements[0].position= 0.092
                cr6_node.color_ramp.elements[1].position= 0.122
                bw_node = material_cosmic2.node_tree.nodes.new('ShaderNodeRGBToBW')
                bw_node.location = (0, 200)
                link = material_cosmic2.node_tree.links.new
                link(mixrgb3_node.outputs[0], emiss4_node.inputs[0])
                link(overlay_node.outputs[0], dark_node.inputs[1])
                link(math2_node.outputs[0], mixrgb3_node.inputs[1])
                link(math2_node.outputs[0], cr10_node.inputs[0])
                link(math4_node.outputs[0], math3_node.inputs[0])
                link(math5_node.outputs[0], math4_node.inputs[1])
                link(cr9_node.outputs[0], math4_node.inputs[0])
                link(noise4_node.outputs[0], cr9_node.inputs[0])
                link(math5_node.outputs[0], noise4_node.inputs[1])
                link(musgrave3_node.outputs[0], math5_node.inputs[1])
                link(musgrave2_node.outputs[0], math5_node.inputs[0])
                link(cr6_node.outputs[0], math3_node.inputs[1])
                link(math3_node.outputs[0], math2_node.inputs[0])
                link(cr8_node.outputs[0], math2_node.inputs[1])
                link(grad1_node.outputs[0], cr8_node.inputs[0])
                link(cr10_node.outputs[0], mixs3_node.inputs[0])
                link(emiss4_node.outputs[0], mixs3_node.inputs[2])
                link(mixs_node.outputs[0], mixs3_node.inputs[1])
                link(coord2_node.outputs[0], mapping2_node.inputs[0])
                link(mapping2_node.outputs[0], grad1_node.inputs[0])
                link(grad1_node.outputs[0], cr7_node.inputs[0])
                link(dark_node.outputs[0], emiss1_node.inputs[0])
                link(cr7_node.outputs[0], dark_node.inputs[0])
                link(math_node.outputs[0], mixrgb2_node.inputs[0])
                link(cr6_node.outputs[0], math_node.inputs[0])
                link(musgrave1_node.outputs[0], math_node.inputs[1])
                link(bw_node.outputs[0], cr6_node.inputs[0])
                link(math_node.outputs[0], mixrgb2_node.inputs[0])
                link(multiply_node.outputs[0], bw_node.inputs[0])
                link(multiply_node.outputs[0], mixrgb2_node.inputs[1])
                link(emiss1_node.outputs[0], mixs2_node.inputs[1])
                link(emiss3_node.outputs[0], mixs2_node.inputs[2])
                link(mixs2_node.outputs[0], mixs_node.inputs[1])
                link(emiss2_node.outputs[0], mixs_node.inputs[2])
                link(cr5_node.outputs[0], mixs2_node.inputs[0])
                link(noise3_node.outputs[0], cr5_node.inputs[0])
                link(mapping_node.outputs[0], noise3_node.inputs[0])
                link(coord_node.outputs[0], mapping_node.inputs[0])
                link(cr4_node.outputs[0], mixs_node.inputs[0])
                link(lweight_node.outputs[0], cr4_node.inputs[0])
                link(dark_node.outputs[0], emiss1_node.inputs[0])
                link(mixrgb2_node.outputs[0], hue_node.inputs[4])
                link(hue_node.outputs[0], overlay_node.inputs[1])
                link(cr3_node.outputs[0], overlay_node.inputs[0])
                link(mixrgb_node.outputs[0], multiply_node.inputs[1])
                link(noise2_node.outputs[0], multiply_node.inputs[0])
                link(cr2_node.outputs[0], mixrgb_node.inputs[1])
                link(noise1_node.outputs[0], mixrgb_node.inputs[0])
                link(noise2_node.outputs[0], cr2_node.inputs[0])
                link(noise2_node.outputs[0], cr3_node.inputs[0])
                link(cr1_node.outputs[0], noise2_node.inputs[0])
                link(noise1_node.outputs[0], cr1_node.inputs[0])
                link(mixs3_node.outputs[0], material_output.inputs[0])
                bpy.context.object.active_material = material_cosmic2
                bpy.context.object.active_material.diffuse_color = (0, 1, 0, 1)
                bpy.context.object.active_material.metallic = 0.3
            else:
                material_cosmic2 = bpy.data.materials.new(name= "Continental")
                material_cosmic2.use_nodes = True
                bdsf_node = material_cosmic2.node_tree.nodes.get('Principled BSDF')
                bdsf_node.location = (1700, 200)
                material_output = material_cosmic2.node_tree.nodes.get('Material Output')
                cr11_node = material_cosmic2.node_tree.nodes.new('ShaderNodeValToRGB')
                cr11_node.location = (1600, 200)
                cr11_node.color_ramp.elements[0].color= (0.527,0.527,0.527,1)
                bw2_node = material_cosmic2.node_tree.nodes.new('ShaderNodeRGBToBW')
                bw2_node.location = (1500, 200)
                bump_node = material_cosmic2.node_tree.nodes.new('ShaderNodeBump')
                bump_node.location = (1500, 0)
                material_output.location = (3200,0)
                noise1_node = material_cosmic2.node_tree.nodes.new('ShaderNodeTexNoise')
                noise1_node.location = (-1000,0)
                noise1_node.inputs[2].default_value = self.land_scale
                noise1_node.inputs[3].default_value = 16
                noise1_node.inputs[4].default_value = 0.848
                noise1_node.inputs[5].default_value = 0
                noise2_node = material_cosmic2.node_tree.nodes.new('ShaderNodeTexNoise')
                noise2_node.location = (-800, 0)
                noise2_node.inputs[2].default_value = 12.5
                noise2_node.inputs[3].default_value = 2
                noise2_node.inputs[4].default_value = 0.890
                noise2_node.inputs[5].default_value = 0
                cr1_node = material_cosmic2.node_tree.nodes.new('ShaderNodeValToRGB')
                cr1_node.location = (-900, -200)
                cr1_node.color_ramp.elements[0].position= 0.133
                cr1_node.color_ramp.elements[1].position= self.water_lvl
                cr1_node.color_ramp.elements.new(position= 0.516)
                cr2_node = material_cosmic2.node_tree.nodes.new('ShaderNodeValToRGB')
                cr2_node.location = (-650, -200)
                cr2_node.color_ramp.elements[0].position= 0.505
                cr2_node.color_ramp.elements[1].position= 0.650
                mixrgb_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMixRGB')
                mixrgb_node.location = (-600, 0)
                mixrgb_node.inputs[2].default_value = (0, 0.0202886, 0.502886, 1)
                multiply_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMixRGB')
                multiply_node.location = (-400, 200)
                multiply_node.blend_type = 'BURN'
                multiply_node.inputs[2].default_value = (0.391573, 0.799103, 0, 1)
                hue_node = material_cosmic2.node_tree.nodes.new('ShaderNodeHueSaturation')
                hue_node.location = (800, 100)
                hue_node.inputs[0].default_value = self.land_hue
                hue_node.inputs[1].default_value = self.land_sat
                cr3_node = material_cosmic2.node_tree.nodes.new('ShaderNodeValToRGB')
                cr3_node.location = (-400, -200)
                cr3_node.color_ramp.elements[0].position= 0.402
                cr3_node.color_ramp.elements[1].position= 0.418
                overlay_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMixRGB')
                overlay_node.location = (1000, 0)
                overlay_node.blend_type = 'LIGHTEN'
                overlay_node.inputs[2].default_value = (0, 0.0152085, 0.0528607, 1)
                dark_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMixRGB')
                dark_node.location = (1200, 0)
                dark_node.blend_type = 'DARKEN'
                dark_node.inputs[2].default_value = (0,0,0,1)
                dark_node.use_clamp = True
                if self.shadow_bool == False:
                    dark_node.mute= True
                grad1_node = material_cosmic2.node_tree.nodes.new('ShaderNodeTexGradient')
                grad1_node.location= (800, 500)
                mapping2_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMapping')
                mapping2_node.location = (600, 500)
                mapping2_node.inputs[1].default_value[0] = self.shadow_coverage
                mapping2_node.inputs[3].default_value[0] = 1
                mapping2_node.inputs[3].default_value[1] = 1
                mapping2_node.inputs[3].default_value[2] = 1
                coord2_node = material_cosmic2.node_tree.nodes.new('ShaderNodeTexCoord')
                coord2_node.location = (400, 500)
                sv = self.shadow_vis
                cr7_node = material_cosmic2.node_tree.nodes.new('ShaderNodeValToRGB')
                cr7_node.location = (1200, 300)
                cr7_node.color_ramp.elements[0].position= 0.096
                cr7_node.color_ramp.elements[1].position= 0.551
                cr7_node.color_ramp.elements[1].color= (sv, sv, sv, 1)
                cr8_node = material_cosmic2.node_tree.nodes.new('ShaderNodeValToRGB')
                cr8_node.location = (1400, 500)
                cr8_node.color_ramp.elements[0].position= 0.421
                cr8_node.color_ramp.elements[1].position= 0.435
                cr8_node.color_ramp.elements[0].color= (1,1,1,1)
                cr8_node.color_ramp.elements[1].color= (0,0,0,1)
                math2_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMath')
                math2_node.location = (1700, 600)
                math2_node.operation = 'SUBTRACT'
                math3_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMath')
                math3_node.location = (1500, 700)
                math3_node.operation = 'MULTIPLY'
                math4_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMath')
                math4_node.location = (900, 900)
                math4_node.operation = 'MULTIPLY'
                cr9_node = material_cosmic2.node_tree.nodes.new('ShaderNodeValToRGB')
                cr9_node.location = (600, 900)
                cr9_node.color_ramp.elements[0].position= 0.598
                cr9_node.color_ramp.elements[1].position= 0.606
                noise4_node = material_cosmic2.node_tree.nodes.new('ShaderNodeTexNoise')
                noise4_node.location = (400, 900)
                noise4_node.inputs[2].default_value = 96.100
                noise4_node.inputs[3].default_value = 2
                noise4_node.inputs[4].default_value = 1
                noise4_node.inputs[5].default_value = 2.4
                math5_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMath')
                math5_node.location = (200, 900)
                math5_node.operation = 'ADD'
                musgrave2_node = material_cosmic2.node_tree.nodes.new('ShaderNodeTexMusgrave')
                musgrave2_node.location = (0, 1000)
                musgrave2_node.inputs[2].default_value = self.city_lights
                musgrave2_node.inputs[3].default_value = 2
                musgrave2_node.inputs[4].default_value = 2
                musgrave2_node.inputs[5].default_value = 2
                musgrave3_node = material_cosmic2.node_tree.nodes.new('ShaderNodeTexMusgrave')
                musgrave3_node.location = (0, 800)
                musgrave3_node.inputs[2].default_value = -5.80
                musgrave3_node.inputs[3].default_value = 2
                musgrave3_node.inputs[4].default_value = 9.2
                musgrave3_node.inputs[5].default_value = 9.8
                mixs3_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMixShader')
                mixs3_node.location = (3000, 0)
                if self.city_bool == False:
                    mixs3_node.mute= True
                emiss4_node = material_cosmic2.node_tree.nodes.new('ShaderNodeEmission')
                emiss4_node.location = (2800, -200)
                emiss4_node.inputs[1].default_value = self.city_brightness
                mixrgb3_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMixRGB')
                mixrgb3_node.location = (2600, -200)
                mixrgb3_node.inputs[2].default_value = (1, 0.694074, 0.220557, 1)
                cr10_node = material_cosmic2.node_tree.nodes.new('ShaderNodeValToRGB')
                cr10_node.location = (2800, 500)
                cr10_node.color_ramp.elements[1].position= 0.027
                emiss2_node = material_cosmic2.node_tree.nodes.new('ShaderNodeEmission')
                emiss2_node.location = (1900, -200)
                emiss2_node.inputs[0].default_value = self.atmos_col
                emiss2_node.inputs[1].default_value = self.atmos_glow
                emiss3_node = material_cosmic2.node_tree.nodes.new('ShaderNodeEmission')
                emiss3_node.location = (1900, 0)
                emiss3_node.inputs[0].default_value = (1, 1, 1, 1)
                emiss3_node.inputs[1].default_value = 6.500
                mixs2_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMixShader')
                mixs2_node.location = (2500, 0)
                if self.cloud_bool == False:
                    mixs2_node.mute= True
                lweight_node = material_cosmic2.node_tree.nodes.new('ShaderNodeLayerWeight')
                lweight_node.location = (2200, 400)
                lweight_node.inputs[0].default_value = 0.160
                cr4_node = material_cosmic2.node_tree.nodes.new('ShaderNodeValToRGB')
                cr4_node.location = (2500, 400)
                cr4_node.color_ramp.elements[0].position= 0.005435
                mixs_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMixShader')
                mixs_node.location = (2700, 0)
                if self.atmos == False: 
                    mixs_node.mute= True
                cr5_node = material_cosmic2.node_tree.nodes.new('ShaderNodeValToRGB')
                cr5_node.location = (-400, -500)
                cr5_node.color_ramp.elements[0].position= 0.540761
                cr5_node.color_ramp.elements[1].position= 0.769022
                cr5_node.color_ramp.elements[1].color = (cv, cv, cv, cv)
                noise3_node = material_cosmic2.node_tree.nodes.new('ShaderNodeTexNoise')
                noise3_node.location = (-600, -500)
                noise3_node.inputs[2].default_value = self.cloud_scale
                noise3_node.inputs[3].default_value = 7.100
                noise3_node.inputs[4].default_value = 0.995
                noise3_node.inputs[5].default_value = 0.8
                mapping_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMapping')
                mapping_node.location = (-800, -500)
                mapping_node.inputs[3].default_value[0] = 0.18
                mapping_node.inputs[3].default_value[1] = 0.18
                mapping_node.inputs[3].default_value[2] = 0.18
                coord_node = material_cosmic2.node_tree.nodes.new('ShaderNodeTexCoord')
                coord_node.location = (-1000, -500)
                mixrgb2_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMixRGB')
                mixrgb2_node.location = (600, 0)
                mixrgb2_node.inputs[2].default_value = self.v_col
                math_node = material_cosmic2.node_tree.nodes.new('ShaderNodeMath')
                math_node.location = (400, 0)
                math_node.operation = 'MULTIPLY'
                musgrave1_node = material_cosmic2.node_tree.nodes.new('ShaderNodeTexMusgrave')
                musgrave1_node.location = (200, -200)
                musgrave1_node.inputs[2].default_value = self.v_scale
                musgrave1_node.inputs[3].default_value = 16
                musgrave1_node.inputs[4].default_value = 0.030
                musgrave1_node.inputs[5].default_value = 1.2
                musgrave1_node.musgrave_type = 'MULTIFRACTAL'
                cr6_node = material_cosmic2.node_tree.nodes.new('ShaderNodeValToRGB')
                cr6_node.location = (200, 200)
                cr6_node.color_ramp.elements[0].position= 0.092
                cr6_node.color_ramp.elements[1].position= 0.122
                bw_node = material_cosmic2.node_tree.nodes.new('ShaderNodeRGBToBW')
                bw_node.location = (0, 200)
                link = material_cosmic2.node_tree.links.new
                link(mixrgb3_node.outputs[0], emiss4_node.inputs[0])
                link(overlay_node.outputs[0], dark_node.inputs[1])
                link(math2_node.outputs[0], mixrgb3_node.inputs[1])
                link(math2_node.outputs[0], cr10_node.inputs[0])
                link(math4_node.outputs[0], math3_node.inputs[0])
                link(math5_node.outputs[0], math4_node.inputs[1])
                link(cr9_node.outputs[0], math4_node.inputs[0])
                link(noise4_node.outputs[0], cr9_node.inputs[0])
                link(math5_node.outputs[0], noise4_node.inputs[1])
                link(musgrave3_node.outputs[0], math5_node.inputs[1])
                link(musgrave2_node.outputs[0], math5_node.inputs[0])
                link(cr6_node.outputs[0], math3_node.inputs[1])
                link(math3_node.outputs[0], math2_node.inputs[0])
                link(cr8_node.outputs[0], math2_node.inputs[1])
                link(grad1_node.outputs[0], cr8_node.inputs[0])
                link(cr10_node.outputs[0], mixs3_node.inputs[0])
                link(emiss4_node.outputs[0], mixs3_node.inputs[2])
                link(mixs_node.outputs[0], mixs3_node.inputs[1])
                link(coord2_node.outputs[0], mapping2_node.inputs[0])
                link(mapping2_node.outputs[0], grad1_node.inputs[0])
                link(grad1_node.outputs[0], cr7_node.inputs[0])
                link(dark_node.outputs[0], bdsf_node.inputs[0])
                link(cr11_node.outputs[0], bdsf_node.inputs[7])
                link(bump_node.outputs[0], bdsf_node.inputs[19])
                link(dark_node.outputs[0], bdsf_node.inputs[0])
                link(dark_node.outputs[0], bw2_node.inputs[0])
                link(bw2_node.outputs[0], cr11_node.inputs[0])
                link(dark_node.outputs[0], bump_node.inputs[2])
                link(cr7_node.outputs[0], dark_node.inputs[0])
                link(math_node.outputs[0], mixrgb2_node.inputs[0])
                link(cr6_node.outputs[0], math_node.inputs[0])
                link(musgrave1_node.outputs[0], math_node.inputs[1])
                link(bw_node.outputs[0], cr6_node.inputs[0])
                link(math_node.outputs[0], mixrgb2_node.inputs[0])
                link(multiply_node.outputs[0], bw_node.inputs[0])
                link(multiply_node.outputs[0], mixrgb2_node.inputs[1])
                link(bdsf_node.outputs[0], mixs2_node.inputs[1])
                link(emiss3_node.outputs[0], mixs2_node.inputs[2])
                link(mixs2_node.outputs[0], mixs_node.inputs[1])
                link(emiss2_node.outputs[0], mixs_node.inputs[2])
                link(cr5_node.outputs[0], mixs2_node.inputs[0])
                link(noise3_node.outputs[0], cr5_node.inputs[0])
                link(mapping_node.outputs[0], noise3_node.inputs[0])
                link(coord_node.outputs[0], mapping_node.inputs[0])
                link(cr4_node.outputs[0], mixs_node.inputs[0])
                link(lweight_node.outputs[0], cr4_node.inputs[0])
                link(mixrgb2_node.outputs[0], hue_node.inputs[4])
                link(hue_node.outputs[0], overlay_node.inputs[1])
                link(cr3_node.outputs[0], overlay_node.inputs[0])
                link(mixrgb_node.outputs[0], multiply_node.inputs[1])
                link(noise2_node.outputs[0], multiply_node.inputs[0])
                link(cr2_node.outputs[0], mixrgb_node.inputs[1])
                link(noise1_node.outputs[0], mixrgb_node.inputs[0])
                link(noise2_node.outputs[0], cr2_node.inputs[0])
                link(noise2_node.outputs[0], cr3_node.inputs[0])
                link(cr1_node.outputs[0], noise2_node.inputs[0])
                link(noise1_node.outputs[0], cr1_node.inputs[0])
                link(mixs3_node.outputs[0], material_output.inputs[0])
                bpy.context.object.active_material = material_cosmic2
                bpy.context.object.active_material.diffuse_color = (0, 1, 0, 1)
                bpy.context.object.active_material.metallic = 0.3
                
        if mytool.planet_type == 'OP3':
            material_cosmic3 = bpy.data.materials.new(name= "Dust World")
            material_cosmic3.use_nodes = True
            material_cosmic3.node_tree.nodes.remove(material_cosmic3.node_tree.nodes.get('Principled BSDF'))
            material_output = material_cosmic3.node_tree.nodes.get('Material Output')
            material_output.location = (1000,0)
            cr1_node = material_cosmic3.node_tree.nodes.new('ShaderNodeValToRGB')
            cr1_node.location = (-300, 500)
            cr1_node.color_ramp.elements[0].position= 0.858544
            cr1_node.color_ramp.elements[1].position= 0.970109
            magic_node = material_cosmic3.node_tree.nodes.new('ShaderNodeTexMagic')
            magic_node.location = (-500, 500)
            magic_node.inputs[1].default_value = self.stripe_amount
            magic_node.inputs[2].default_value = 0.130
            magic_node.turbulence_depth = 1
            mapping_node = material_cosmic3.node_tree.nodes.new('ShaderNodeMapping')
            mapping_node.location = (-700, 500)
            mapping_node.inputs[2].default_value[0] = -42.4
            mapping_node.inputs[2].default_value[1] = 47.6
            mapping_node.inputs[2].default_value[2] = 0
            mapping_node.inputs[3].default_value[0] = 0.6
            coord_node = material_cosmic3.node_tree.nodes.new('ShaderNodeTexCoord')
            coord_node.location = (-900, 500)
            voronoi_node = material_cosmic3.node_tree.nodes.new('ShaderNodeTexVoronoi')
            voronoi_node.location = (-700, 0)
            voronoi_node.feature = 'SMOOTH_F1'
            voronoi_node.distance = 'CHEBYCHEV'
            voronoi_node.inputs[2].default_value = 21.690
            voronoi_node.inputs[3].default_value = 1
            voronoi_node.inputs[4].default_value = 1
            mapping2_node = material_cosmic3.node_tree.nodes.new('ShaderNodeMapping')
            mapping2_node.location = (-900, 0)
            mapping2_node.inputs[3].default_value[0] = 0.140
            coord2_node = material_cosmic3.node_tree.nodes.new('ShaderNodeTexCoord')
            coord2_node.location = (-1100, 0)
            bw_node = material_cosmic3.node_tree.nodes.new('ShaderNodeRGBToBW')
            bw_node.location = (-550, 0)
            multiply1_node = material_cosmic3.node_tree.nodes.new('ShaderNodeMixRGB')
            multiply1_node.location = (-400, 200)
            multiply1_node.inputs[0].default_value = 1
            multiply1_node.inputs[2].default_value = (0.552012, 0.130136, 0.0451862, 1)
            multiply1_node.blend_type= 'MULTIPLY'
            multiply2_node = material_cosmic3.node_tree.nodes.new('ShaderNodeMixRGB')
            multiply2_node.location = (-400, -200)
            multiply2_node.inputs[0].default_value = 1
            multiply2_node.inputs[2].default_value = (0.187821, 0.0684782, 0, 1)
            multiply2_node.blend_type= 'MULTIPLY'
            mixrgb_node = material_cosmic3.node_tree.nodes.new('ShaderNodeMixRGB')
            mixrgb_node.location = (-200, 0)
            overlay_node = material_cosmic3.node_tree.nodes.new('ShaderNodeMixRGB')
            overlay_node.location = (0, 0)
            overlay_node.inputs[0].default_value = 0.595
            overlay_node.blend_type= 'OVERLAY'
            darken_node = material_cosmic3.node_tree.nodes.new('ShaderNodeMixRGB')
            darken_node.location = (200, 0)
            darken_node.inputs[2].default_value = (0.035037, 0.0133497, 0.00550307, 1)
            darken_node.blend_type= 'MULTIPLY'
            noise1_node = material_cosmic3.node_tree.nodes.new('ShaderNodeTexNoise')
            noise1_node.location = (0, -200)
            noise1_node.inputs[2].default_value = 8.600
            noise1_node.inputs[3].default_value = 16
            noise1_node.inputs[4].default_value = 0.830
            noise1_node.inputs[5].default_value = 0
            cr3_node = material_cosmic3.node_tree.nodes.new('ShaderNodeValToRGB')
            cr3_node.location = (200, -200)
            cr3_node.color_ramp.elements[0].position= 0.366848
            cr3_node.color_ramp.elements[1].position= 0.608695
            hue_node = material_cosmic3.node_tree.nodes.new('ShaderNodeHueSaturation')
            hue_node.location = (400, 200)
            hue_node.inputs[0].default_value = self.d_hue
            emiss1_node = material_cosmic3.node_tree.nodes.new('ShaderNodeEmission')
            emiss1_node.location = (600, 200)
            emiss1_node.inputs[1].default_value = 2.800
            emiss2_node = material_cosmic3.node_tree.nodes.new('ShaderNodeEmission')
            emiss2_node.location = (600, -200)
            emiss2_node.inputs[0].default_value = self.d_atmos_col
            emiss2_node.inputs[1].default_value = self.d_atmos_glow
            lweight_node = material_cosmic3.node_tree.nodes.new('ShaderNodeLayerWeight')
            lweight_node.location = (200, 400)
            lweight_node.inputs[0].default_value= 0.160
            mixs_node = material_cosmic3.node_tree.nodes.new('ShaderNodeMixShader')
            mixs_node.location = (800, 0)
            if self.atmos == False: 
                mixs_node.mute= True
            cr2_node = material_cosmic3.node_tree.nodes.new('ShaderNodeValToRGB')
            cr2_node.location = (500, 400)
            cr2_node.color_ramp.elements[0].position= 0.013587
            cr2_node.color_ramp.elements[1].position= 1
            link = material_cosmic3.node_tree.links.new
            link(voronoi_node.outputs[0], mixrgb_node.inputs[0])
            link(mixrgb_node.outputs[0], overlay_node.inputs[1])
            link(voronoi_node.outputs[0], mapping_node.inputs[0])
            link(mapping2_node.outputs[0], voronoi_node.inputs[0])
            link(coord2_node.outputs[0], mapping2_node.inputs[0])
            link(bw_node.outputs[0], multiply2_node.inputs[1])
            link(bw_node.outputs[0], multiply1_node.inputs[1])
            link(voronoi_node.outputs[1], bw_node.inputs[0])
            link(coord_node.outputs[0], mapping_node.inputs[0])
            link(mapping_node.outputs[0], magic_node.inputs[0])
            link(magic_node.outputs[0], cr1_node.inputs[0])
            link(cr1_node.outputs[0], overlay_node.inputs[2])
            link(multiply2_node.outputs[0], mixrgb_node.inputs[2])
            link(multiply1_node.outputs[0], mixrgb_node.inputs[1])
            link(overlay_node.outputs[0], darken_node.inputs[1])
            link(cr3_node.outputs[0], darken_node.inputs[0])
            link(darken_node.outputs[0], hue_node.inputs[4])
            link(hue_node.outputs[0], emiss1_node.inputs[0])
            link(noise1_node.outputs[0], cr3_node.inputs[0])
            link(lweight_node.outputs[0], cr2_node.inputs[0])
            link(cr2_node.outputs[0], mixs_node.inputs[0])
            link(emiss2_node.outputs[0], mixs_node.inputs[2])
            link(emiss1_node.outputs[0], mixs_node.inputs[1])
            link(mixs_node.outputs[0], material_output.inputs[0])
            bpy.context.object.active_material = material_cosmic3
            bpy.context.object.active_material.diffuse_color = (1, 0.3, 0.004, 1)
            bpy.context.object.active_material.metallic = 0.3
            
        if mytool.planet_type == 'OP4':
            material_cosmic4 = bpy.data.materials.new(name= "Moon")
            material_cosmic4.use_nodes = True
            material_cosmic4.node_tree.nodes.remove(material_cosmic4.node_tree.nodes.get('Principled BSDF'))
            material_output = material_cosmic4.node_tree.nodes.get('Material Output')
            material_output.location = (1000,0)
            mus1_node = material_cosmic4.node_tree.nodes.new('ShaderNodeTexMusgrave')
            mus1_node.location = (-1600,400)
            mus1_node.musgrave_type= 'MULTIFRACTAL'
            mus1_node.inputs[2].default_value = self.m_macro_scale
            mus1_node.inputs[3].default_value = 16
            mus1_node.inputs[4].default_value = 0.720
            mus1_node.inputs[5].default_value = 2.610
            mus2_node = material_cosmic4.node_tree.nodes.new('ShaderNodeTexMusgrave')
            mus2_node.location = (-1400,400)
            mus2_node.musgrave_dimensions = '4D'
            mus2_node.musgrave_type= 'MULTIFRACTAL'
            mus2_node.inputs[1].default_value = self.m_seed
            mus2_node.inputs[2].default_value = 0.740
            mus2_node.inputs[3].default_value = 16
            mus2_node.inputs[4].default_value = 0.350
            mus2_node.inputs[5].default_value = 2.610
            mus3_node = material_cosmic4.node_tree.nodes.new('ShaderNodeTexMusgrave')
            mus3_node.location = (-1200,400)
            mus3_node.musgrave_dimensions = '4D'
            mus3_node.inputs[1].default_value = 0
            mus3_node.inputs[2].default_value = 6.990
            mus3_node.inputs[3].default_value = 12
            mus3_node.inputs[4].default_value = 6.830
            mus3_node.inputs[5].default_value = 2
            cr1_node = material_cosmic4.node_tree.nodes.new('ShaderNodeValToRGB')
            cr1_node.location = (-1000, 400)
            cr1_node.color_ramp.elements[0].position= 0
            cr1_node.color_ramp.elements.new(position= 0.035)
            cr1_node.color_ramp.elements[1].color= (1,1,1,1)
            mus4_node = material_cosmic4.node_tree.nodes.new('ShaderNodeTexMusgrave')
            mus4_node.location = (-1600,-400)
            mus4_node.musgrave_type= 'MULTIFRACTAL'
            mus4_node.inputs[2].default_value = self.m_micro_scale
            mus4_node.inputs[3].default_value = 16
            mus4_node.inputs[4].default_value = 0.900
            mus4_node.inputs[5].default_value = 1.400
            mus5_node = material_cosmic4.node_tree.nodes.new('ShaderNodeTexMusgrave')
            mus5_node.location = (-1400,-400)
            mus5_node.musgrave_type= 'HETERO_TERRAIN'
            mus5_node.inputs[2].default_value = 19.00
            mus5_node.inputs[3].default_value = 16
            mus5_node.inputs[4].default_value = 2.000
            mus5_node.inputs[5].default_value = 1.4
            cr2_node = material_cosmic4.node_tree.nodes.new('ShaderNodeValToRGB')
            cr2_node.location = (-1200, -400)
            cr2_node.color_ramp.elements[1].position= 0.057
            cr2_node.color_ramp.elements[1].color= (0.421482, 0.421482, 0.421482, 1)
            screen_node = material_cosmic4.node_tree.nodes.new('ShaderNodeMixRGB')
            screen_node.location = (-1000, -400)
            screen_node.blend_type = 'SCREEN'            
            screen_node.inputs[2].default_value = (0.391528, 0.391528, 0.391528, 1)
            screen_node.use_clamp = True
            multiply_node = material_cosmic4.node_tree.nodes.new('ShaderNodeMixRGB')
            multiply_node.location = (-800, -0)
            multiply_node.blend_type = 'MULTIPLY'
            multiply_node.inputs[2].default_value = (0,0,0,1)
            multiply_node.use_clamp = True
            grad1_node = material_cosmic4.node_tree.nodes.new('ShaderNodeTexGradient')
            grad1_node.location= (-600, 200)
            sv = self.m_shadow_vis
            cr3_node = material_cosmic4.node_tree.nodes.new('ShaderNodeValToRGB')
            cr3_node.location = (-400, 200)
            cr3_node.color_ramp.elements[1].position= self.m_shadow_coverage
            cr3_node.color_ramp.elements[1].color= (sv, sv, sv, 1)
            dark_node = material_cosmic4.node_tree.nodes.new('ShaderNodeMixRGB')
            dark_node.location = (-200, 0)
            dark_node.blend_type = 'MULTIPLY'
            dark_node.inputs[2].default_value = (0,0,0,1)
            dark_node.use_clamp = True
            if self.m_shadow_bool == False:
                dark_node.mute= True
            emiss1_node = material_cosmic4.node_tree.nodes.new('ShaderNodeEmission')
            emiss1_node.location = (0, 200)
            emiss1_node.inputs[1].default_value = 3
            emiss2_node = material_cosmic4.node_tree.nodes.new('ShaderNodeEmission')
            emiss2_node.location = (0, -200)
            emiss2_node.inputs[0].default_value = self.m_atmos_col
            emiss2_node.inputs[1].default_value = self.m_atmos_glow
            lweight_node = material_cosmic4.node_tree.nodes.new('ShaderNodeLayerWeight')
            lweight_node.location = (400, 400)
            lweight_node.inputs[0].default_value = 0.570
            cr4_node = material_cosmic4.node_tree.nodes.new('ShaderNodeValToRGB')
            cr4_node.location = (600, 400)
            cr4_node.color_ramp.elements[0].position= 0.158
            cr4_node.color_ramp.elements[1].position= 0.416
            mixs_node = material_cosmic4.node_tree.nodes.new('ShaderNodeMixShader')
            mixs_node.location = (800, 0)
            if self.m_atmos == False: 
                mixs_node.mute= True
            link = material_cosmic4.node_tree.links.new
            link(mus1_node.outputs[0], mus2_node.inputs[0])
            link(mus2_node.outputs[0], mus3_node.inputs[0])
            link(mus4_node.outputs[0], mus5_node.inputs[0])
            link(mus3_node.outputs[0], cr1_node.inputs[0])
            link(mus5_node.outputs[0], cr2_node.inputs[0])
            link(cr1_node.outputs[0], multiply_node.inputs[0])
            link(cr2_node.outputs[0], screen_node.inputs[1])
            link(screen_node.outputs[0], multiply_node.inputs[1])
            link(grad1_node.outputs[0], cr3_node.inputs[0])
            link(cr3_node.outputs[0], dark_node.inputs[0])
            link(multiply_node.outputs[0], dark_node.inputs[1])
            link(dark_node.outputs[0], emiss1_node.inputs[0])
            link(emiss1_node.outputs[0], mixs_node.inputs[1])
            link(emiss2_node.outputs[0], mixs_node.inputs[2])
            link(cr4_node.outputs[0], mixs_node.inputs[0])
            link(lweight_node.outputs[0], cr4_node.inputs[0])
            link(mixs_node.outputs[0], material_output.inputs[0])
            bpy.context.object.active_material = material_cosmic4
            bpy.context.object.active_material.metallic = 0.3
            
        if mytool.planet_type == 'OP5':
            material_cosmic5 = bpy.data.materials.new(name= "Rocky Planet")
            material_cosmic5.use_nodes = True
            bsdf_node = material_cosmic5.node_tree.nodes.get('Principled BSDF')
            bsdf_node.location = (400, 0)
            material_output = material_cosmic5.node_tree.nodes.get('Material Output')
            material_output.location = (1000, 0)
            mus_node = material_cosmic5.node_tree.nodes.new('ShaderNodeTexMusgrave')
            mus_node.location = (-1400, 0)
            mus_node.musgrave_type = 'RIDGED_MULTIFRACTAL'
            mus_node.inputs[2].default_value = self.r_scale
            mus_node.inputs[3].default_value = 20
            mus_node.inputs[4].default_value = self.r_soften
            mus_node.inputs[5].default_value = 2.830
            mus_node.inputs[6].default_value = 0
            mus_node.inputs[7].default_value = 12.870
            cr1_node = material_cosmic5.node_tree.nodes.new('ShaderNodeValToRGB')
            cr1_node.location = (-1200, 200)
            cr1_node.color_ramp.elements[1].position= 0.005
            lh = self.r_land_height
            cr2_node = material_cosmic5.node_tree.nodes.new('ShaderNodeValToRGB')
            cr2_node.location = (-1200, -200)
            cr2_node.color_ramp.elements[0].color= (0.071, 0.071, 0.071, 1)
            cr2_node.color_ramp.elements.new(position= 0.337)
            cr2_node.color_ramp.elements[1].color = (lh, lh, lh, 1)
            cr2_node.color_ramp.elements[1].position = 0.856
            cr2_node.color_ramp.elements[2].color = (0.4, 0.4, 0.4, 1)
            math1_node = material_cosmic5.node_tree.nodes.new('ShaderNodeMath')
            math1_node.location= (-1000, 0)
            math1_node.operation= 'MULTIPLY'
            math1_node.use_clamp= True
            cr3_node = material_cosmic5.node_tree.nodes.new('ShaderNodeValToRGB')
            cr3_node.location = (-800, 200)
            cr3_node.color_ramp.elements[1].color= (0.059, 0.059, 0.059, 1)
            multiply1_node = material_cosmic5.node_tree.nodes.new('ShaderNodeMixRGB')
            multiply1_node.location = (-600, -200)
            multiply1_node.blend_type= 'MULTIPLY'
            multiply1_node.inputs[0].default_value= 0.860
            multiply1_node.inputs[2].default_value= (0.5691, 0.150605, 0, 1)
            c1 = self.r_land_col1
            c2 = self.r_land_col2
            c3 = self.r_land_col3
            c4 = self.r_land_col4
            cr4_node = material_cosmic5.node_tree.nodes.new('ShaderNodeValToRGB')
            cr4_node.location = (-600, -400)
            cr4_node.color_ramp.elements.new(position= 0.082)
            cr4_node.color_ramp.elements.new(position= 0.209)
            cr4_node.color_ramp.elements.new(position= 0.647)
            cr4_node.color_ramp.elements[1].color = c1
            cr4_node.color_ramp.elements[2].color = c2
            cr4_node.color_ramp.elements[3].color = c3
            cr4_node.color_ramp.elements[4].color = c4
            cr4_node.color_ramp.elements[3].position= 0.476
            cr4_node.color_ramp.elements[4].position= 0.647
            bump_node = material_cosmic5.node_tree.nodes.new('ShaderNodeBump')
            bump_node.location = (-600, -600)
            bump_node.inputs[1].default_value= 0.050
            mix1_node = material_cosmic5.node_tree.nodes.new('ShaderNodeMixRGB')
            mix1_node.location = (-400, -300)
            mix1_node.inputs[0].default_value= 0.440
            bw1_node = material_cosmic5.node_tree.nodes.new('ShaderNodeRGBToBW')
            bw1_node.location = (-200, -300)
            cr5_node = material_cosmic5.node_tree.nodes.new('ShaderNodeValToRGB')
            cr5_node.location = (0, -300)
            cr5_node.color_ramp.elements[1].position = 0.019
            mix2_node = material_cosmic5.node_tree.nodes.new('ShaderNodeMixRGB')
            mix2_node.location = (200, -100)
            mix2_node.inputs[1].default_value= self.r_water_col
            cr6_node = material_cosmic5.node_tree.nodes.new('ShaderNodeValToRGB')
            cr6_node.location = (200, -500)
            cr6_node.color_ramp.elements[0].color = (0.345, 0.345, 0.345, 1)
            lw_node = material_cosmic5.node_tree.nodes.new('ShaderNodeLayerWeight')
            lw_node.location = (600, 200)
            lw_node.inputs[0].default_value = 0.160
            cr7_node = material_cosmic5.node_tree.nodes.new('ShaderNodeValToRGB')
            cr7_node.location = (600, 400)
            cr7_node.color_ramp.elements[0].position = 0.005
            emiss1_node = material_cosmic5.node_tree.nodes.new('ShaderNodeEmission')
            emiss1_node.location = (600, -200)
            emiss1_node.inputs[0].default_value= self.r_atmos_col
            emiss1_node.inputs[1].default_value= self.r_atmos_glow
            mixs_node = material_cosmic5.node_tree.nodes.new('ShaderNodeMixShader')
            mixs_node.location = (800, 0)
            if self.r_atmos == False:
                mixs_node.mute= True
            link = material_cosmic5.node_tree.links.new
            link(mus_node.outputs[0], cr1_node.inputs[0])
            link(mus_node.outputs[0], cr2_node.inputs[0])
            link(mus_node.outputs[0], cr4_node.inputs[0])
            link(mus_node.outputs[0], bump_node.inputs[2])
            link(cr1_node.outputs[0], math1_node.inputs[0])
            link(cr2_node.outputs[0], math1_node.inputs[1])
            link(math1_node.outputs[0], cr3_node.inputs[0])
            link(math1_node.outputs[0], multiply1_node.inputs[1])
            link(multiply1_node.outputs[0], mix1_node.inputs[1])
            link(cr4_node.outputs[0], mix1_node.inputs[2])
            link(mix1_node.outputs[0], bw1_node.inputs[0])
            link(bw1_node.outputs[0], cr5_node.inputs[0])
            link(cr5_node.outputs[0], mix2_node.inputs[0])
            link(cr5_node.outputs[0], cr6_node.inputs[0])
            link(mix1_node.outputs[0], mix2_node.inputs[2])
            link(mix2_node.outputs[0], bsdf_node.inputs[0])
            link(cr6_node.outputs[0], bsdf_node.inputs[7])
            link(bump_node.outputs[0], bsdf_node.inputs[19])
            link(lw_node.outputs[0], cr7_node.inputs[0])
            link(cr7_node.outputs[0], mixs_node.inputs[0])
            link(emiss1_node.outputs[0], mixs_node.inputs[2])
            link(bsdf_node.outputs[0], mixs_node.inputs[1])
            link(cr3_node.outputs[0], material_output.inputs[2])
            link(mixs_node.outputs[0], material_output.inputs[0])
            bpy.context.object.active_material = material_cosmic5
            bpy.context.object.active_material.diffuse_color = (0.8, 0.225265, 0.0318058, 1)
            bpy.context.object.active_material.metallic = 0.3
            
        if mytool.planet_type == 'OP6':
            material_cosmic6 = bpy.data.materials.new(name= "Star Sphere")
            material_cosmic6.use_nodes = True
            material_cosmic6.node_tree.nodes.remove(material_cosmic6.node_tree.nodes.get('Principled BSDF'))
            material_output = material_cosmic6.node_tree.nodes.get('Material Output')
            material_output.location = (0,0)
            emiss_node = material_cosmic6.node_tree.nodes.new('ShaderNodeEmission')
            emiss_node.location = (-200,0)
            emiss_node.inputs[0].default_value = (1, 0, 0, 1)
            cr_node = material_cosmic6.node_tree.nodes.new('ShaderNodeValToRGB')
            cr_node.location = (-400,0)
            cr_node.color_ramp.elements[0].position = 0.624
            cr_node.color_ramp.elements[1].position = self.star_coverage
            noise_node = material_cosmic6.node_tree.nodes.new('ShaderNodeTexNoise')
            noise_node.location = (-600, 0)
            noise_node.inputs[2].default_value = self.star_scale
            noise_node.inputs[3].default_value = 16
            noise_node.inputs[4].default_value = 0.740
            noise_node.inputs[5].default_value = 0
            link = material_cosmic6.node_tree.links.new
            link(cr_node.outputs[0], emiss_node.inputs[0])
            link(noise_node.outputs[0], cr_node.inputs[0])
            link(emiss_node.outputs[0], material_output.inputs[0])
            bpy.context.object.active_material = material_cosmic6
            bpy.context.object.active_material.diffuse_color = (0, 0, 0, 1)
            bpy.context.object.active_material.metallic = 0.3 
            
        if mytool.planet_type == 'OP7':
            material_cosmic7 = bpy.data.materials.new(name= "Golden World")
            material_cosmic7.use_nodes = True
            bsdf_node = material_cosmic7.node_tree.nodes.get('Principled BSDF')
            bsdf_node.location = (400, 0)
            material_output = material_cosmic7.node_tree.nodes.get('Material Output')
            material_output.location = (1000, 0)
            mus_node = material_cosmic7.node_tree.nodes.new('ShaderNodeTexMusgrave')
            mus_node.location = (-1400, 0)
            mus_node.musgrave_type = 'RIDGED_MULTIFRACTAL'
            mus_node.inputs[2].default_value = self.g_scale
            mus_node.inputs[3].default_value = 20
            mus_node.inputs[4].default_value = self.g_soften
            mus_node.inputs[5].default_value = 2.310
            mus_node.inputs[6].default_value = -0.070
            mus_node.inputs[7].default_value = 10.010
            cr1_node = material_cosmic7.node_tree.nodes.new('ShaderNodeValToRGB')
            cr1_node.location = (-1200, 200)
            cr1_node.color_ramp.elements[1].position= 0.005
            lh = self.g_land_height
            cr2_node = material_cosmic7.node_tree.nodes.new('ShaderNodeValToRGB')
            cr2_node.location = (-1200, -200)
            cr2_node.color_ramp.elements[0].color= (0.071, 0.071, 0.071, 1)
            cr2_node.color_ramp.elements.new(position= 0.337)
            cr2_node.color_ramp.elements[1].color = (lh, lh, lh, 1)
            cr2_node.color_ramp.elements[2].color = (0.318, 0.318, 0.318, 1)
            math1_node = material_cosmic7.node_tree.nodes.new('ShaderNodeMath')
            math1_node.location= (-1000, 0)
            math1_node.operation= 'MULTIPLY'
            math1_node.use_clamp= True
            cr3_node = material_cosmic7.node_tree.nodes.new('ShaderNodeValToRGB')
            cr3_node.location = (-800, 200)
            cr3_node.color_ramp.elements[1].color= (0.059, 0.059, 0.059, 1)
            multiply1_node = material_cosmic7.node_tree.nodes.new('ShaderNodeMixRGB')
            multiply1_node.location = (-600, -200)
            multiply1_node.blend_type= 'MULTIPLY'
            multiply1_node.inputs[0].default_value= 1
            multiply1_node.inputs[2].default_value= (0.00856812, 0.0684782, 0.127438, 1)
            c1 = self.g_land_col1
            c2 = self.g_land_col2
            c3 = self.g_land_col3
            c4 = self.g_land_col4
            cr4_node = material_cosmic7.node_tree.nodes.new('ShaderNodeValToRGB')
            cr4_node.location = (-600, -400)
            cr4_node.color_ramp.elements.new(position= 0.041)
            cr4_node.color_ramp.elements.new(position= 0.098)
            cr4_node.color_ramp.elements.new(position= 0.275)
            cr4_node.color_ramp.elements[1].color = c1
            cr4_node.color_ramp.elements[2].color = c2
            cr4_node.color_ramp.elements[3].color = c3
            cr4_node.color_ramp.elements[3].position= 0.201
            cr4_node.color_ramp.elements[4].color = c4
            cr4_node.color_ramp.elements[4].position = 0.275
            math2_node = material_cosmic7.node_tree.nodes.new('ShaderNodeMath')
            math2_node.location= (-800, -400)
            math2_node.operation= 'MULTIPLY'
            math2_node.use_clamp= True
            noise_node = material_cosmic7.node_tree.nodes.new('ShaderNodeTexNoise')
            noise_node.location = (-1000, -600)
            noise_node.inputs[2].default_value = 19
            noise_node.inputs[3].default_value = 2
            noise_node.inputs[4].default_value = 0.5
            noise_node.inputs[5].default_value = 2.2
            bump_node = material_cosmic7.node_tree.nodes.new('ShaderNodeBump')
            bump_node.location = (-600, -600)
            bump_node.inputs[1].default_value= 0.050
            mix1_node = material_cosmic7.node_tree.nodes.new('ShaderNodeMixRGB')
            mix1_node.location = (-400, -300)
            mix1_node.inputs[0].default_value= 0.640
            bw1_node = material_cosmic7.node_tree.nodes.new('ShaderNodeRGBToBW')
            bw1_node.location = (-200, -300)
            cr5_node = material_cosmic7.node_tree.nodes.new('ShaderNodeValToRGB')
            cr5_node.location = (0, -300)
            cr5_node.color_ramp.elements[0].position = 0.079
            cr5_node.color_ramp.elements[1].position = 0.160
            mix2_node = material_cosmic7.node_tree.nodes.new('ShaderNodeMixRGB')
            mix2_node.location = (200, -100)
            mix2_node.inputs[1].default_value= self.g_water_col
            cr6_node = material_cosmic7.node_tree.nodes.new('ShaderNodeValToRGB')
            cr6_node.location = (200, -500)
            cr6_node.color_ramp.elements[0].color = (0.345, 0.345, 0.345, 1)
            lw_node = material_cosmic7.node_tree.nodes.new('ShaderNodeLayerWeight')
            lw_node.location = (600, 200)
            lw_node.inputs[0].default_value = 0.160
            cr7_node = material_cosmic7.node_tree.nodes.new('ShaderNodeValToRGB')
            cr7_node.location = (600, 400)
            cr7_node.color_ramp.elements[0].position = 0.005
            emiss1_node = material_cosmic7.node_tree.nodes.new('ShaderNodeEmission')
            emiss1_node.location = (600, -200)
            emiss1_node.inputs[0].default_value= self.g_atmos_col
            emiss1_node.inputs[1].default_value= self.g_atmos_glow
            mixs_node = material_cosmic7.node_tree.nodes.new('ShaderNodeMixShader')
            mixs_node.location = (800, 0)
            if self.g_atmos == False:
                mixs_node.mute= True
            link = material_cosmic7.node_tree.links.new
            link(mus_node.outputs[0], cr1_node.inputs[0])
            link(mus_node.outputs[0], cr2_node.inputs[0])
            link(mus_node.outputs[0], math2_node.inputs[0])
            link(math2_node.outputs[0], cr4_node.inputs[0])
            link(noise_node.outputs[0], math2_node.inputs[1])
            link(mus_node.outputs[0], bump_node.inputs[2])
            link(cr1_node.outputs[0], math1_node.inputs[0])
            link(cr2_node.outputs[0], math1_node.inputs[1])
            link(math1_node.outputs[0], cr3_node.inputs[0])
            link(math1_node.outputs[0], multiply1_node.inputs[1])
            link(multiply1_node.outputs[0], mix1_node.inputs[1])
            link(cr4_node.outputs[0], mix1_node.inputs[2])
            link(mix1_node.outputs[0], bw1_node.inputs[0])
            link(bw1_node.outputs[0], cr5_node.inputs[0])
            link(cr5_node.outputs[0], mix2_node.inputs[0])
            link(cr5_node.outputs[0], cr6_node.inputs[0])
            link(mix1_node.outputs[0], mix2_node.inputs[2])
            link(mix2_node.outputs[0], bsdf_node.inputs[0])
            link(cr6_node.outputs[0], bsdf_node.inputs[7])
            link(bump_node.outputs[0], bsdf_node.inputs[19])
            link(lw_node.outputs[0], cr7_node.inputs[0])
            link(cr7_node.outputs[0], mixs_node.inputs[0])
            link(emiss1_node.outputs[0], mixs_node.inputs[2])
            link(bsdf_node.outputs[0], mixs_node.inputs[1])
            link(cr3_node.outputs[0], material_output.inputs[2])
            link(mixs_node.outputs[0], material_output.inputs[0])
            bpy.context.object.active_material = material_cosmic7
            bpy.context.object.active_material.diffuse_color = (0.8, 0.517521, 0.0242545, 1)
            bpy.context.object.active_material.metallic = 0.3
            
        if mytool.planet_type == 'OP8':
            material_cosmic8 = bpy.data.materials.new(name= "Icy World")
            material_cosmic8.use_nodes = True
            bsdf_node = material_cosmic8.node_tree.nodes.get('Principled BSDF')
            bsdf_node.location = (400, 0)
            material_output = material_cosmic8.node_tree.nodes.get('Material Output')
            material_output.location = (1000, 0)
            mus_node = material_cosmic8.node_tree.nodes.new('ShaderNodeTexMusgrave')
            mus_node.location = (-1400, 0)
            mus_node.musgrave_type = 'RIDGED_MULTIFRACTAL'
            mus_node.inputs[2].default_value = self.i_scale
            mus_node.inputs[3].default_value = 90
            mus_node.inputs[4].default_value = self.i_soften
            mus_node.inputs[5].default_value = 2.910
            mus_node.inputs[6].default_value = -0.120
            mus_node.inputs[7].default_value = 10.010
            cr1_node = material_cosmic8.node_tree.nodes.new('ShaderNodeValToRGB')
            cr1_node.location = (-1200, 200)
            cr1_node.color_ramp.elements[1].position= 0.005
            lh = self.i_land_height
            cr2_node = material_cosmic8.node_tree.nodes.new('ShaderNodeValToRGB')
            cr2_node.location = (-1200, -200)
            cr2_node.color_ramp.elements[0].color= (0.071, 0.071, 0.071, 1)
            cr2_node.color_ramp.elements.new(position= 0.337)
            cr2_node.color_ramp.elements[1].color = (lh, lh, lh, 1)
            cr2_node.color_ramp.elements[2].color = (0.306, 0.306, 0.306, 1)
            math1_node = material_cosmic8.node_tree.nodes.new('ShaderNodeMath')
            math1_node.location= (-1000, 0)
            math1_node.operation= 'MULTIPLY'
            math1_node.use_clamp= True
            cr3_node = material_cosmic8.node_tree.nodes.new('ShaderNodeValToRGB')
            cr3_node.location = (-800, 200)
            cr3_node.color_ramp.elements[1].color= (0.059, 0.059, 0.059, 1)
            multiply1_node = material_cosmic8.node_tree.nodes.new('ShaderNodeMixRGB')
            multiply1_node.location = (-600, -200)
            multiply1_node.blend_type= 'MULTIPLY'
            multiply1_node.inputs[0].default_value= 1
            multiply1_node.inputs[2].default_value= (0.144129, 0.0231533, 0.00182117, 1)
            c1 = self.i_land_col1
            c2 = self.i_land_col2
            c3 = self.i_land_col3
            c4 = self.i_land_col4
            cr4_node = material_cosmic8.node_tree.nodes.new('ShaderNodeValToRGB')
            cr4_node.location = (-600, -400)
            cr4_node.color_ramp.elements.new(position= 0.041)
            cr4_node.color_ramp.elements.new(position= 0.098)
            cr4_node.color_ramp.elements.new(position= 0.275)
            cr4_node.color_ramp.elements[1].color = c1
            cr4_node.color_ramp.elements[2].color = c2
            cr4_node.color_ramp.elements[3].color = c3
            cr4_node.color_ramp.elements[3].position= 0.201
            cr4_node.color_ramp.elements[4].color = c4
            cr4_node.color_ramp.elements[4].position = 0.275
            math2_node = material_cosmic8.node_tree.nodes.new('ShaderNodeMath')
            math2_node.location= (-800, -400)
            math2_node.operation= 'MULTIPLY'
            math2_node.use_clamp= True
            noise_node = material_cosmic8.node_tree.nodes.new('ShaderNodeTexNoise')
            noise_node.location = (-1000, -600)
            noise_node.inputs[2].default_value = 19
            noise_node.inputs[3].default_value = 2
            noise_node.inputs[4].default_value = 0.5
            noise_node.inputs[5].default_value = 2.2
            bump_node = material_cosmic8.node_tree.nodes.new('ShaderNodeBump')
            bump_node.location = (-600, -600)
            bump_node.inputs[1].default_value= 0.050
            mix1_node = material_cosmic8.node_tree.nodes.new('ShaderNodeMixRGB')
            mix1_node.location = (-400, -300)
            mix1_node.inputs[0].default_value= 0.640
            bw1_node = material_cosmic8.node_tree.nodes.new('ShaderNodeRGBToBW')
            bw1_node.location = (-200, -300)
            cr5_node = material_cosmic8.node_tree.nodes.new('ShaderNodeValToRGB')
            cr5_node.location = (0, -300)
            cr5_node.color_ramp.elements[0].position = 0.079
            cr5_node.color_ramp.elements[1].position = 0.160
            mix2_node = material_cosmic8.node_tree.nodes.new('ShaderNodeMixRGB')
            mix2_node.location = (200, -100)
            mix2_node.inputs[1].default_value= self.i_water_col
            cr6_node = material_cosmic8.node_tree.nodes.new('ShaderNodeValToRGB')
            cr6_node.location = (200, -500)
            cr6_node.color_ramp.elements[0].color = (0.345, 0.345, 0.345, 1)
            lw_node = material_cosmic8.node_tree.nodes.new('ShaderNodeLayerWeight')
            lw_node.location = (600, 200)
            lw_node.inputs[0].default_value = 0.160
            cr7_node = material_cosmic8.node_tree.nodes.new('ShaderNodeValToRGB')
            cr7_node.location = (600, 400)
            cr7_node.color_ramp.elements[0].position = 0.005
            emiss1_node = material_cosmic8.node_tree.nodes.new('ShaderNodeEmission')
            emiss1_node.location = (600, -200)
            emiss1_node.inputs[0].default_value= self.i_atmos_col
            emiss1_node.inputs[1].default_value= self.i_atmos_glow
            mixs_node = material_cosmic8.node_tree.nodes.new('ShaderNodeMixShader')
            mixs_node.location = (800, 0)
            if self.i_atmos == False:
                mixs_node.mute= True
            link = material_cosmic8.node_tree.links.new
            link(mus_node.outputs[0], cr1_node.inputs[0])
            link(mus_node.outputs[0], cr2_node.inputs[0])
            link(mus_node.outputs[0], math2_node.inputs[0])
            link(math2_node.outputs[0], cr4_node.inputs[0])
            link(noise_node.outputs[0], math2_node.inputs[1])
            link(mus_node.outputs[0], bump_node.inputs[2])
            link(cr1_node.outputs[0], math1_node.inputs[0])
            link(cr2_node.outputs[0], math1_node.inputs[1])
            link(math1_node.outputs[0], cr3_node.inputs[0])
            link(math1_node.outputs[0], multiply1_node.inputs[1])
            link(multiply1_node.outputs[0], mix1_node.inputs[1])
            link(cr4_node.outputs[0], mix1_node.inputs[2])
            link(mix1_node.outputs[0], bw1_node.inputs[0])
            link(bw1_node.outputs[0], cr5_node.inputs[0])
            link(cr5_node.outputs[0], mix2_node.inputs[0])
            link(cr5_node.outputs[0], cr6_node.inputs[0])
            link(mix1_node.outputs[0], mix2_node.inputs[2])
            link(mix2_node.outputs[0], bsdf_node.inputs[0])
            link(cr6_node.outputs[0], bsdf_node.inputs[7])
            link(bump_node.outputs[0], bsdf_node.inputs[19])
            link(lw_node.outputs[0], cr7_node.inputs[0])
            link(cr7_node.outputs[0], mixs_node.inputs[0])
            link(emiss1_node.outputs[0], mixs_node.inputs[2])
            link(bsdf_node.outputs[0], mixs_node.inputs[1])
            link(cr3_node.outputs[0], material_output.inputs[2])
            link(mixs_node.outputs[0], material_output.inputs[0])
            bpy.context.object.active_material = material_cosmic8
            bpy.context.object.active_material.diffuse_color = (0.100548, 0.562905, 0.8, 1)
            bpy.context.object.active_material.metallic = 0.3
            
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width= 210)

class SHADER_OT_DIAMOND(Operator):
    """Open the Diamond Dialog box"""
    bl_label = "             Diamond Operator"
    bl_idname = "wm.diamondop"
    bl_options = {'REGISTER', 'UNDO'}
    
    col : FloatVectorProperty(name='Color Tint',subtype='COLOR_GAMMA',size=4,default=(1,1,1,1), min= 0, max= 1)
    
    def execute(self, context):
        c = self.col
        material_diamond = bpy.data.materials.new(name= "Diamond")
        material_diamond.use_nodes = True
        material_diamond.node_tree.nodes.remove(material_diamond.node_tree.nodes.get('Principled BSDF'))
        material_output = material_diamond.node_tree.nodes.get('Material Output')
        material_output.location = (400,0)
        glass1_node = material_diamond.node_tree.nodes.new('ShaderNodeBsdfGlass')
        glass1_node.location = (-600,0)
        glass1_node.inputs[0].default_value = (1, 0, 0, 1)
        glass1_node.inputs[2].default_value = 1.446
        glass2_node = material_diamond.node_tree.nodes.new('ShaderNodeBsdfGlass')
        glass2_node.location = (-600,-150)
        glass2_node.inputs[0].default_value = (0, 1, 0, 1)
        glass2_node.inputs[2].default_value = 1.450
        glass3_node = material_diamond.node_tree.nodes.new('ShaderNodeBsdfGlass')
        glass3_node.location = (-600,-300)
        glass3_node.inputs[0].default_value = (0, 0, 1, 1)
        glass3_node.inputs[2].default_value = 1.545        
        add1_node = material_diamond.node_tree.nodes.new('ShaderNodeAddShader')
        add1_node.location = (-400,-50)
        add1_node.label = "Add 1"
        add1_node.hide = True
        add1_node.select = False       
        add2_node = material_diamond.node_tree.nodes.new('ShaderNodeAddShader')
        add2_node.location = (-100,0)
        add2_node.label = "Add 2"
        add2_node.hide = True
        add2_node.select = False      
        glass4_node = material_diamond.node_tree.nodes.new('ShaderNodeBsdfGlass')
        glass4_node.location = (-150,-150)
        glass4_node.inputs[2].default_value = 1.450
        glass4_node.select = False      
        mix1_node = material_diamond.node_tree.nodes.new('ShaderNodeMixShader')
        mix1_node.location = (200,0)
        mix1_node.select = False
        material_diamond.node_tree.links.new(glass1_node.outputs[0], add1_node.inputs[0])
        material_diamond.node_tree.links.new(glass2_node.outputs[0], add1_node.inputs[1])
        material_diamond.node_tree.links.new(add1_node.outputs[0], add2_node.inputs[0])
        material_diamond.node_tree.links.new(glass3_node.outputs[0], add2_node.inputs[1])
        material_diamond.node_tree.links.new(add2_node.outputs[0], mix1_node.inputs[1])
        material_diamond.node_tree.links.new(glass4_node.outputs[0], mix1_node.inputs[2])
        material_diamond.node_tree.links.new(mix1_node.outputs[0], material_output.inputs[0])
        bpy.context.object.active_material = material_diamond
        bpy.context.object.active_material.diffuse_color = c
        bpy.context.object.active_material.metallic = 0.3
        if context.scene.render.engine == 'BLENDER_EEVEE':
            context.object.active_material.blend_method = 'HASHED'
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width= 210)


class SHADER_OT_GOLD(Operator):
    """Add the Basic Gold Shader to your selected Object."""
    bl_label = "Gold"
    bl_idname = 'shader.gold_operator'
    bl_options = {'REGISTER', 'UNDO'}
    
    roughness : FloatProperty(name='Roughness', default= 0.5, min= 0, max= 1)
    preset_bool : BoolProperty(name= "Set Roughness", default= False)
    
    def draw(self, context):
        layout= self.layout
        layout.separator(factor= 0.1)
        box = layout.box()
        box.prop(self, "preset_bool")
        if self.preset_bool == True:
            box.label(text= "0 - Glossy                              1 - Rough")
            box.prop(self, "roughness", slider= True)
        layout.separator(factor= 1)    
    
    def execute(self, context):
        r = self.roughness
        material_gold = bpy.data.materials.new(name= "Gold")
        material_gold.use_nodes = True
        material_output = material_gold.node_tree.nodes.get('Material Output')
        material_output.location = (600,0)
        material_output.select = False     
        rgb_node = material_gold.node_tree.nodes.new('ShaderNodeRGB')
        rgb_node.location = (0,-100)
        rgb_node.outputs[0].default_value = (1, 0.766, 0.336, 1)
        rgb_node.select = False
        rgb_node.hide = True
        principled = material_gold.node_tree.nodes.get('Principled BSDF')
        principled.location = (200,0)
        principled.select = False
        principled.inputs[4].default_value = 1
        principled.inputs[7].default_value = r
        material_gold.node_tree.links.new(rgb_node.outputs[0], principled.inputs[0])
        bpy.context.object.active_material = material_gold
        bpy.context.object.active_material.diffuse_color = (1, 0.766, 0.336, 1)
        bpy.context.object.active_material.metallic = 0.45082
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width= 210)


class SHADER_OT_SILVER(Operator):
    """Add the Basic Silver Shader to your selected Object."""
    bl_label = "Silver"
    bl_idname = 'shader.silver_operator'
    bl_options = {'REGISTER', 'UNDO'}
    
    roughness : FloatProperty(name='Roughness', default= 0.5, min= 0, max= 1)
    preset_bool : BoolProperty(name= "Set Roughness", default= False)
    
    def draw(self, context):
        layout= self.layout
        layout.separator(factor= 0.1)
        box = layout.box()
        box.prop(self, "preset_bool")
        if self.preset_bool == True:
            box.label(text= "0 - Glossy                              1 - Rough")
            box.prop(self, "roughness", slider= True)
        layout.separator(factor= 1)    
    
    def execute(self, context):
        r = self.roughness
        material_silver = bpy.data.materials.new(name= "Silver")
        material_silver.use_nodes = True
        material_output = material_silver.node_tree.nodes.get('Material Output')
        material_output.location = (600,0)
        material_output.select = False       
        rgb_node = material_silver.node_tree.nodes.new('ShaderNodeRGB')
        rgb_node.location = (0,-100)
        rgb_node.outputs[0].default_value = (0.972, 0.960, 0.915, 1)
        rgb_node.select = False
        rgb_node.hide = True
        principled = material_silver.node_tree.nodes.get('Principled BSDF')
        principled.location = (200,0)
        principled.select = False
        principled.inputs[4].default_value = 1.0
        principled.inputs[7].default_value = r
        material_silver.node_tree.links.new(rgb_node.outputs[0], principled.inputs[0])
        bpy.context.object.active_material = material_silver
        bpy.context.object.active_material.diffuse_color = (0.972, 0.960, 0.915, 1)
        bpy.context.object.active_material.metallic = 0.45082
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width= 210)


class SHADER_OT_COPPER(Operator):
    """Add the Basic Copper Shader to your selected Object."""
    bl_label = "Copper"
    bl_idname = 'shader.copper_operator'
    bl_options = {'REGISTER', 'UNDO'}
    
    roughness : FloatProperty(name='Roughness', default= 0.5, min= 0, max= 1)
    preset_bool : BoolProperty(name= "Set Roughness", default= False)
    
    def draw(self, context):
        layout= self.layout
        layout.separator(factor= 0.1)
        box = layout.box()
        box.prop(self, "preset_bool")
        if self.preset_bool == True:
            box.label(text= "0 - Glossy                              1 - Rough")
            box.prop(self, "roughness", slider= True)
        layout.separator(factor= 1)    
    
    def execute(self, context):
        r = self.roughness
        material_copper = bpy.data.materials.new(name= "Copper")
        material_copper.use_nodes = True
        material_output = material_copper.node_tree.nodes.get('Material Output')
        material_output.location = (600,0)
        material_output.select = False    
        rgb_node = material_copper.node_tree.nodes.new('ShaderNodeRGB')
        rgb_node.location = (0,-100)
        rgb_node.outputs[0].default_value = (0.955, 0.637, 0.538, 1)
        rgb_node.select = False
        rgb_node.hide = True
        principled = material_copper.node_tree.nodes.get('Principled BSDF')
        principled.location = (200,0)
        principled.select = False
        principled.inputs[4].default_value = 1.0
        principled.inputs[7].default_value = r
        material_copper.node_tree.links.new(rgb_node.outputs[0], principled.inputs[0])
        bpy.context.object.active_material = material_copper
        bpy.context.object.active_material.diffuse_color = (0.955, 0.637, 0.538, 1)
        bpy.context.object.active_material.metallic = 0.45082
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width= 210)


class WM_OT_ghostOp(Operator):
    """Open the Ghost Dialog box"""
    bl_label = "                  Ghost Operator"
    bl_idname = "wm.ghostop"
    bl_options = {'REGISTER', 'UNDO'}
    
    col1 : FloatVectorProperty(name='Outer Color',subtype='COLOR_GAMMA',size=4,default=(0.224322, 0.812741, 1, 1), min= 0, max= 1)
    col2 : FloatVectorProperty(name='Inner Color',subtype='COLOR_GAMMA',size=4,default=(0.137478, 0.345533, 1, 1), min= 0, max= 1)
    trans : FloatProperty(min= 0, max= 1, default= 0.5, description= "Transparancy Value. At 0 the Shader will still have some transparancy but at 1 the Shader will fully Transparent")
    enable_bool : BoolProperty(default= False, description= "This Option will add a subtle effect to the shader. The Whole Object will be Visible through itself.")
    
    def draw(self, context):
        layout = self.layout
        layout.separator(factor=2)
        layout.prop(self, "col1")
        layout.prop(self, "col2")
        layout.prop(self, "trans", text= "Transparency:", slider= True)
        if context.scene.render.engine == 'CYCLES':
            layout.separator(factor=0.5)
            box = layout.box()
            box.prop(self, "enable_bool", text= "Variant")
            if self.enable_bool == True:
                box.label(text= "This Option will add a subtle effect")
                box.label(text= "to the shader. ")
                box.label(text= "The Whole Object will be Visible.")
        layout.separator(factor=1)
    
    def execute(self, context):
        c1 = self.col1
        c2 = self.col2
        a = self.trans
        material_ghost = bpy.data.materials.new(name= "Ghost")
        material_ghost.use_nodes = True
        material_output = material_ghost.node_tree.nodes.get('Material Output')
        material_output.location = (1000,0)
        material_output.select = False
        material_ghost.node_tree.nodes.remove(material_ghost.node_tree.nodes.get('Principled BSDF'))       
        emiss_node = material_ghost.node_tree.nodes.new('ShaderNodeEmission')
        emiss_node.location = (-200,-90)
        emiss_node.inputs[0].default_value = c1
        emiss_node.inputs[1].default_value = 2
        emiss_node.select = False        
        trans_node = material_ghost.node_tree.nodes.new('ShaderNodeBsdfTransparent')
        trans_node.location = (-200,10)
        trans_node.inputs[0].default_value = c2
        trans_node.select = False       
        mix_node = material_ghost.node_tree.nodes.new('ShaderNodeMixShader')
        mix_node.location = (400,50)
        mix_node.select = False      
        layerw_node = material_ghost.node_tree.nodes.new('ShaderNodeLayerWeight')
        layerw_node.location = (0,150)
        layerw_node.inputs[0].default_value = 0.1
        layerw_node.select = False      
        math_node = material_ghost.node_tree.nodes.new('ShaderNodeMath')
        math_node.location = (200,100)
        math_node.inputs[0].default_value = 0.1
        math_node.select = False
        math_node.hide = True      
        mix2_node = material_ghost.node_tree.nodes.new('ShaderNodeMixShader')
        mix2_node.location = (800,50)
        mix2_node.select = False       
        trans2_node = material_ghost.node_tree.nodes.new('ShaderNodeBsdfTransparent')
        trans2_node.location = (500,-100)
        trans2_node.inputs[0].default_value = (1, 1, 1, 1)
        trans2_node.select = False      
        light_node = material_ghost.node_tree.nodes.new('ShaderNodeLightPath')
        light_node.location = (500,500)
        light_node.select = False
        colramp_node = material_ghost.node_tree.nodes.new('ShaderNodeValToRGB')
        colramp_node.location = (700, 200)
        colramp_node.select = False
        colramp_node.color_ramp.elements[0].color = (a, a, a, 1)
        if self.enable_bool == True:
            colramp_node.color_ramp.elements[1].color = (0.85, 0.85, 0.85, 1)
        material_ghost.node_tree.links.new(trans_node.outputs[0], mix_node.inputs[1])
        material_ghost.node_tree.links.new(emiss_node.outputs[0], mix_node.inputs[2])
        material_ghost.node_tree.links.new(layerw_node.outputs[0], math_node.inputs[0])
        material_ghost.node_tree.links.new(layerw_node.outputs[1], math_node.inputs[1])
        material_ghost.node_tree.links.new(math_node.outputs[0], mix_node.inputs[0])
        material_ghost.node_tree.links.new(mix_node.outputs[0], mix2_node.inputs[1])
        material_ghost.node_tree.links.new(trans2_node.outputs[0], mix2_node.inputs[2])
        material_ghost.node_tree.links.new(light_node.outputs[11], colramp_node.inputs[0])
        material_ghost.node_tree.links.new(colramp_node.outputs[0], mix2_node.inputs[0])
        material_ghost.node_tree.links.new(mix2_node.outputs[0], material_output.inputs[0])
        bpy.context.object.active_material = material_ghost
        bpy.context.object.active_material.diffuse_color = c1
        if context.scene.render.engine == 'BLENDER_EEVEE':
            context.object.active_material.blend_method = 'HASHED'
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width= 200)


class WM_OT_hologramOp(Operator):
    """Open the Hologram Dialog box"""
    bl_label = "       Hologram Operator"
    bl_idname = "wm.hologramop"
    bl_options = {'REGISTER', 'UNDO'}
    
    col1 : FloatVectorProperty(name='Color 1',subtype='COLOR_GAMMA',size=4,default=(0.0927682, 1, 0.566671, 1), min= 0, max= 1)
    col2 : FloatVectorProperty(name='Color 2',subtype='COLOR_GAMMA',size=4,default=(0.381055, 1, 0.697353, 1), min= 0, max= 1)
    wire_amount : FloatProperty(default= 0.050, min= 0, soft_max= 1)
    
    def draw(self, context):
        layout = self.layout
        layout.separator(factor=2)
        layout.prop(self, "col1")
        layout.prop(self, "col2")
        layout.prop(self, "wire_amount", slider= True, text= "Wireframe Size:")
        layout.separator(factor=1)
    
    def execute(self, context):
        c1 = self.col1
        c2 = self.col2
        material_hologram = bpy.data.materials.new(name= "Hologram")
        material_hologram.use_nodes = True
        material_output = material_hologram.node_tree.nodes.get('Material Output')
        material_output.location = (1000,0)
        material_output.select = False
        material_hologram.node_tree.nodes.remove(material_hologram.node_tree.nodes.get('Principled BSDF'))     
        emiss_node = material_hologram.node_tree.nodes.new('ShaderNodeEmission')
        emiss_node.location = (-200,-90)
        emiss_node.inputs[0].default_value = c1        
        emiss_node.inputs[1].default_value = 2
        emiss_node.select = False   
        trans1_node = material_hologram.node_tree.nodes.new('ShaderNodeBsdfTransparent')
        trans1_node.location = (-200,10)
        trans1_node.inputs[0].default_value = c2
        trans1_node.select = False      
        mix1_node = material_hologram.node_tree.nodes.new('ShaderNodeMixShader')
        mix1_node.location = (400,50)
        mix1_node.select = False        
        layerw_node = material_hologram.node_tree.nodes.new('ShaderNodeLayerWeight')
        layerw_node.location = (0,150)
        layerw_node.inputs[0].default_value = 0.1
        layerw_node.select = False       
        math_node = material_hologram.node_tree.nodes.new('ShaderNodeMath')
        math_node.location = (200,100)
        math_node.inputs[0].default_value = 0.1
        math_node.select = False
        math_node.hide = True       
        mix2_node = material_hologram.node_tree.nodes.new('ShaderNodeMixShader')
        mix2_node.location = (600,50)
        mix2_node.select = False      
        wire_node = material_hologram.node_tree.nodes.new('ShaderNodeWireframe')
        wire_node.location = (100,200)
        wire_node.select = False
        wire_node.use_pixel_size = True
        wire_node.inputs[0].default_value = self.wire_amount
        reroute = material_hologram.node_tree.nodes.new('NodeReroute')
        reroute.location = (-150,-90)
        material_hologram.node_tree.links.new(trans1_node.outputs[0], mix1_node.inputs[1])
        material_hologram.node_tree.links.new(emiss_node.outputs[0], reroute.inputs[0])
        material_hologram.node_tree.links.new(reroute.outputs[0], mix1_node.inputs[2])
        material_hologram.node_tree.links.new(reroute.outputs[0], mix2_node.inputs[2])
        material_hologram.node_tree.links.new(layerw_node.outputs[0], math_node.inputs[0])
        material_hologram.node_tree.links.new(layerw_node.outputs[1], math_node.inputs[1])
        material_hologram.node_tree.links.new(math_node.outputs[0], mix1_node.inputs[0])
        material_hologram.node_tree.links.new(mix1_node.outputs[0], mix2_node.inputs[1])
        material_hologram.node_tree.links.new(wire_node.outputs[0], mix2_node.inputs[0])
        material_hologram.node_tree.links.new(mix2_node.outputs[0], material_output.inputs[0])
        bpy.context.object.active_material = material_hologram
        bpy.context.object.active_material.diffuse_color = c1
        if context.scene.render.engine == 'BLENDER_EEVEE':
            context.object.active_material.blend_method = 'HASHED'
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width= 180)


class WM_OT_neonOp(Operator):
    """Open the Neon Dialog box"""
    bl_label = "         Neon Operator"
    bl_idname = "wm.neonop"
    bl_options = {'REGISTER', 'UNDO'}
    
    col : FloatVectorProperty(name='Color',subtype='COLOR_GAMMA',size=4,default=(0.269619, 0.601632, 0.8, 1), min= 0, max= 1)
    
    def execute(self, context):
        c = self.col
        cur_frame = bpy.context.scene.frame_current
        material_neon = bpy.data.materials.new(name= "Neon")
        material_neon.use_nodes = True
        tree = material_neon.node_tree
        material_neon.node_tree.nodes.remove(material_neon.node_tree.nodes.get('Principled BSDF'))
        material_output = material_neon.node_tree.nodes.get('Material Output')
        material_output.location = (400,0)
        emiss_node = material_neon.node_tree.nodes.new('ShaderNodeEmission')
        emiss_node.location = (200,0)
        emiss_node.inputs[0].default_value = c
        emiss_node.inputs[1].default_value = 1.5
        emiss_node.inputs[1].keyframe_insert("default_value", frame= cur_frame)
        data_path = f'nodes["{emiss_node.name}"].inputs[1].default_value'
        fcurves = tree.animation_data.action.fcurves
        fc = fcurves.find(data_path)
        if fc:
            new_mod = fc.modifiers.new('NOISE')
            new_mod.strength = 10
            new_mod.depth = 1
        material_neon.node_tree.links.new(emiss_node.outputs[0], material_output.inputs[0])
        bpy.context.object.active_material = material_neon
        bpy.context.object.active_material.diffuse_color = c
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width= 150)


class WM_OT_potionOp(Operator):
    """Open the Stylized Potion Dialog box"""
    bl_label = "                       Stylized Potion Operator"
    bl_idname = "wm.potionop"
    bl_options = {'REGISTER', 'UNDO'}
    
    col1 : FloatVectorProperty(name='',subtype='COLOR_GAMMA',size=4,default=(1, 0, 0.0018755, 1), min= 0, max= 1, description= "Select the First Color")
    col2 : FloatVectorProperty(name='',subtype='COLOR_GAMMA',size=4,default=(0.255103, 0, 0.000564289, 1), min= 0, max= 1, description= "Select the Second Color")
    animate : BoolProperty(name= "Animate Shader", default= False, description= "Enable the Animation for the Shader")
    start : IntProperty(name= "Start Frame", default = 0, description= "Set the Start Frame for your animation")
    end : IntProperty(name= "End Frame", default = 250, description= "Set the End Frame for your Animation")
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.separator(factor= 2)
        row= layout.row()
        split = row.split(factor= 0.7)
        split.label(text= "                                             Color 1: ")
        split.prop(self, "col1")
        row= layout.row()
        split = row.split(factor= 0.7)
        split.label(text= "                                             Color 2:" )
        split.prop(self, "col2")   
        row= layout.row()
        row.separator(factor= 2)
        box = layout.box()
        row = box.row()
        row.prop(self, "animate")
        if self.animate == False:
            row.label(text= "(Shader is Not Animated)")
        if self.animate == True:
            row.label(text= "(Shader is Animated)")  
            row = box.row()  
            box.prop(self, "start")
            box.prop(self, "end")
        layout.separator(factor= 1)
    
    def execute(self, context):
        s = self.start
        e = self.end
        c1 = self.col1
        c2 = self.col2
        a = self.animate
        m1 = " : (animated)" 
        if a == True:    
            material_potion = bpy.data.materials.new(name= "Stylized Potion" + m1)
        else:
            material_potion = bpy.data.materials.new(name= "Stylized Potion")    
        material_potion.use_nodes = True
        tree = material_potion.node_tree
        prin_node = material_potion.node_tree.nodes.get('Principled BSDF')
        prin_node.location = (200,0)
        prin_node.inputs[0].default_value = (0.8, 0.000897912, 0, 1)
        prin_node.inputs[3].default_value = (0.8, 0.1332, 0.0936454, 1)
        prin_node.inputs[7].default_value = 0.076
        prin_node.inputs[15].default_value = 0.947
        material_output = material_potion.node_tree.nodes.get('Material Output')
        material_output.location = (500,0)
        rgb1_node = material_potion.node_tree.nodes.new('ShaderNodeRGB')
        rgb1_node.location = (-200,0)
        rgb1_node.outputs[0].default_value = c1   
        rgb2_node = material_potion.node_tree.nodes.new('ShaderNodeRGB')
        rgb2_node.location = (-200,-200)
        rgb2_node.outputs[0].default_value = c2
        mix_node = material_potion.node_tree.nodes.new('ShaderNodeMixRGB')
        mix_node.location = (0,0)
        noise_node = material_potion.node_tree.nodes.new('ShaderNodeTexNoise')
        noise_node.location = (-500, 200)
        noise_node.inputs[2].default_value = 5
        noise_node.inputs[3].default_value = 5
        noise_node.inputs[5].default_value = 0.2
        if a == True:
            noise_node.inputs[5].keyframe_insert("default_value", frame= s-150)
            noise_node.inputs[5].default_value = 1.2
            noise_node.inputs[5].keyframe_insert("default_value", frame= e+50)
        ramp_node = material_potion.node_tree.nodes.new('ShaderNodeValToRGB')
        ramp_node.location = (-300, 200)
        ramp_node.color_ramp.elements[0].position = 0.454
        ramp_node.color_ramp.elements[1].position = 0.522
        link = material_potion.node_tree.links.new
        link(rgb1_node.outputs[0], mix_node.inputs[1])
        link(rgb2_node.outputs[0], mix_node.inputs[2])
        link(noise_node.outputs[0], ramp_node.inputs[0])
        link(ramp_node.outputs[0], mix_node.inputs[0])
        link(mix_node.outputs[0], prin_node.inputs[0])
        link(prin_node.outputs[0], material_output.inputs[0])
        bpy.context.object.active_material = material_potion
        bpy.context.object.active_material.diffuse_color = c1
        return {'FINISHED'}


class SHADER_OT_LEATHER(Operator):
    """Open the Leather Shader Dialog box"""
    bl_label = "             Leather Operator"
    bl_idname = "wm.leatherop"
    bl_options = {'REGISTER', 'UNDO'}
    
    col : FloatVectorProperty(name='Color',subtype='COLOR_GAMMA',size=4,default=(0.123239, 0.071147, 0.0570714, 1), min= 0, max= 1)
    
    def execute(self, context):
        c = self.col
        material_leather = bpy.data.materials.new(name= "Leather")
        material_leather.use_nodes = True
        principled = material_leather.node_tree.nodes.get('Principled BSDF')
        principled.inputs[0].default_value = c
        principled.inputs[5].default_value = 0.161
        principled.inputs[7].default_value = 0.367
        material_output = material_leather.node_tree.nodes.get('Material Output')
        material_output.location = (400,0)
        mus_node = material_leather.node_tree.nodes.new('ShaderNodeTexMusgrave')
        mus_node.location = (-600,0)
        mus_node.musgrave_type = 'MULTIFRACTAL'
        mus_node.inputs[2].default_value = 148
        mus_node.inputs[3].default_value = 12.6
        mus_node.inputs[4].default_value = 92
        mus_node.inputs[5].default_value = 2.3
        disp_node = material_leather.node_tree.nodes.new('ShaderNodeDisplacement')
        disp_node.location = (-400,0)
        disp_node.inputs[2].default_value= 0.190
        material_leather.node_tree.links.new(mus_node.outputs[0], disp_node.inputs[0])
        material_leather.node_tree.links.new(disp_node.outputs[0], material_output.inputs[2])
        bpy.context.object.active_material = material_leather
        bpy.context.object.active_material.diffuse_color = c
        bpy.context.object.active_material.metallic = 0.3
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width= 210)


class SHADER_OT_CLOUD(Operator):
    """Add the Basic Cloud Shader to your selected Object."""
    bl_label = "Cloud"
    bl_idname = 'shader.cloud_operator'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        material_cloud = bpy.data.materials.new(name= "Clouds")
        material_cloud.use_nodes = True
        material_output = material_cloud.node_tree.nodes.get('Material Output')
        material_output.location = (100,0)
        material_output.select = False
        material_cloud.node_tree.nodes.remove(material_cloud.node_tree.nodes.get('Principled BSDF'))
        volume_node = material_cloud.node_tree.nodes.new('ShaderNodeVolumePrincipled')
        volume_node.location = (-200,0)
        volume_node.select = False
        colramp_node = material_cloud.node_tree.nodes.new('ShaderNodeValToRGB')
        colramp_node.location = (-500,0)
        colramp_node.color_ramp.elements[0].position = 0.503798
        colramp_node.color_ramp.elements[1].position = 0.58481
        noise_node = material_cloud.node_tree.nodes.new('ShaderNodeTexNoise')
        noise_node.location = (-700,0)
        noise_node.inputs[2].default_value = 1
        noise_node.inputs[3].default_value = 20
        mapping_node = material_cloud.node_tree.nodes.new('ShaderNodeMapping')
        mapping_node.location = (-900, 0)
        coord_node = material_cloud.node_tree.nodes.new('ShaderNodeTexCoord')
        coord_node.location = (-1100,0)
        material_cloud.node_tree.links.new(colramp_node.outputs[0], volume_node.inputs[2])
        material_cloud.node_tree.links.new(noise_node.outputs[1], colramp_node.inputs[0])
        material_cloud.node_tree.links.new(mapping_node.outputs[0], noise_node.inputs[0])
        material_cloud.node_tree.links.new(coord_node.outputs[3], mapping_node.inputs[0])
        material_cloud.node_tree.links.new(volume_node.outputs[0], material_output.inputs[1])
        bpy.context.object.active_material = material_cloud
        return {'FINISHED'}


class SHADER_OT_SCIFIGOLD(Operator):
    """Add the Basic Scifi Gold Shader to your selected Object."""
    bl_label = "Sci-fi Gold"
    bl_idname = 'shader.scifigold_operator'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        material_scifigold = bpy.data.materials.new(name= "Sci-fi Gold")
        material_scifigold.use_nodes = True
        material_output = material_scifigold.node_tree.nodes.get('Material Output')
        material_output.location = (600,0)
        material_output.select = False      
        rgb_node = material_scifigold.node_tree.nodes.new('ShaderNodeRGB')
        rgb_node.location = (-200,0)
        rgb_node.outputs[0].default_value = (1, 0.766, 0.336, 1)
        rgb_node.select = False
        rgb_node.hide = True
        principled = material_scifigold.node_tree.nodes.get('Principled BSDF')
        principled.location = (200,0)
        principled.select = False
        principled.inputs[4].default_value = 1.0
        bump_node = material_scifigold.node_tree.nodes.new('ShaderNodeBump')
        bump_node.location = (0, -600)
        bump_node.inputs[0].default_value = 0.270
        brick_node = material_scifigold.node_tree.nodes.new('ShaderNodeTexBrick')
        brick_node.location = (-400, -600)
        noise_node = material_scifigold.node_tree.nodes.new('ShaderNodeTexNoise')
        noise_node.location = (-600, -800)
        colramp_node = material_scifigold.node_tree.nodes.new('ShaderNodeValToRGB')
        colramp_node.location = (-100, -300)
        colramp_node.color_ramp.elements[0].color = (0.293851, 0.293851, 0.293851, 1)
        colramp_node.color_ramp.elements[1].color = (0.373086, 0.373086, 0.373086, 1)
        mix_node = material_scifigold.node_tree.nodes.new('ShaderNodeMixRGB')
        mix_node.location = (0, 0)
        mix_node.blend_type = 'MULTIPLY'
        mix_node.inputs[2].default_value = (0.412679, 0.412679, 0.412679, 1)
        mix_node.use_clamp = True
        link = material_scifigold.node_tree.links.new
        link(mix_node.outputs[0], principled.inputs[0])
        link(rgb_node.outputs[0], mix_node.inputs[1])
        link(colramp_node.outputs[0], principled.inputs[7])
        link(bump_node.outputs[0], principled.inputs[19])
        link(brick_node.outputs[0], bump_node.inputs[2])
        link(brick_node.outputs[1], colramp_node.inputs[0])
        link(brick_node.outputs[1], mix_node.inputs[0])
        link(noise_node.outputs[0], brick_node.inputs[0])
        bpy.context.object.active_material = material_scifigold
        return {'FINISHED'}


class SHADER_OT_BRICK(Operator):
    """Add the Basic Brick Shader to your selected Object."""
    bl_label = "Brick"
    bl_idname = 'shader.brick_operator'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        material_brick = bpy.data.materials.new(name= "Brick")
        material_brick.use_nodes = True
        material_output = material_brick.node_tree.nodes.get('Material Output')
        material_output.location = (600,0)
        material_output.select = False       
        rgb_node = material_brick.node_tree.nodes.new('ShaderNodeRGB')
        rgb_node.location = (-400,0)
        rgb_node.outputs[0].default_value = (1, 0.90445, 0.70086, 1)
        rgb_node.select = False
        rgb_node.hide = True
        principled = material_brick.node_tree.nodes.get('Principled BSDF')
        principled.location = (200,0)
        principled.select = False
        principled.inputs[7].default_value = 0.796203
        bump_node = material_brick.node_tree.nodes.new('ShaderNodeBump')
        bump_node.location = (0, -600)
        bump_node.inputs[0].default_value = 0.5
        brick_node = material_brick.node_tree.nodes.new('ShaderNodeTexBrick')
        brick_node.location = (-400, -600)
        brick_node.inputs[4].default_value = 2.9
        brick_node.inputs[5].default_value = 0.01
        noise_node = material_brick.node_tree.nodes.new('ShaderNodeTexNoise')
        noise_node.location = (-400, -200)
        noise_node.inputs[1].default_value = -9.740
        noise_node.inputs[2].default_value = 4.5
        noise_node.inputs[3].default_value = 0
        mix_node = material_brick.node_tree.nodes.new('ShaderNodeMixRGB')
        mix_node.location = (0, 0)
        mix_node.blend_type = 'MULTIPLY'
        mix_node.inputs[2].default_value = (0.440389, 0.440389, 0.440389, 1)
        mix_node.use_clamp = True
        mix2_node = material_brick.node_tree.nodes.new('ShaderNodeMixRGB')
        mix2_node.location = (-200, 0)
        mix_node.use_clamp = True
        mix_node.inputs[0].default_value = 0.4
        coord_node = material_brick.node_tree.nodes.new('ShaderNodeTexCoord')
        coord_node.location = (-1000,-600)
        mapping_node = material_brick.node_tree.nodes.new('ShaderNodeMapping')
        mapping_node.location = (-800,-600)
        mapping_node.inputs[3].default_value[0] = 2.5
        mapping_node.inputs[3].default_value[1] = 2.5
        mapping_node.inputs[3].default_value[2] = 2.5
        link = material_brick.node_tree.links.new
        link(mix_node.outputs[0], principled.inputs[0])
        link(bump_node.outputs[0], principled.inputs[19])
        link(brick_node.outputs[0], bump_node.inputs[2])
        link(brick_node.outputs[1], mix_node.inputs[0])
        link(mapping_node.outputs[0], brick_node.inputs[0])
        link(coord_node.outputs[2], mapping_node.inputs[0])
        link(mix2_node.outputs[0], mix_node.inputs[1])
        link(rgb_node.outputs[0], mix2_node.inputs[1])
        link(noise_node.outputs[0], mix2_node.inputs[2])
        bpy.context.object.active_material = material_brick
        return {'FINISHED'}


class NODE_MT_materials(Menu):
    """The Materials section contains: Leather."""
    bl_label = "Materials"
    bl_idname = "node.mat_MT_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.leatherop", text= "Leather Shader", icon= 'OUTLINER_OB_SURFACE') 


class NODE_MT_metallics(Menu):
    """The Metallics section contains: Gold, Silver and Copper."""
    bl_label = "Metallics"
    bl_idname = "node.met_MT_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("shader.gold_operator", text= "Gold Shader", icon= 'KEYTYPE_KEYFRAME_VEC')
        layout.operator("shader.silver_operator", text= "Silver Shader", icon= 'HANDLETYPE_FREE_VEC')
        layout.operator("shader.copper_operator", text= "Copper Shader", icon= 'KEYTYPE_EXTREME_VEC')


class NODE_MT_gems(Menu):
    """The Gemstones section contains: The Diamond Shader."""
    bl_label = "Gemstones"
    bl_idname = "node.gem_MT_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.diamondop", text= "Diamond Shader", icon= 'DECORATE_ANIMATE')


class NODE_MT_stylized(Menu):
    """The Stylized section contains: The Ghost Shader, The Hologram Shader, The Neon Shader and the Stylized Potion Shader."""
    bl_label = "Stylized"
    bl_idname = "node.stylized_MT_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.ghostop", text= "Ghost Shader", icon= 'GHOST_ENABLED')   
        layout.operator("wm.hologramop", text= "Hologram Shader", icon= 'USER') 
        layout.operator("wm.neonop", text= "Neon Shader", icon= 'MOD_SMOOTH') 
        layout.operator("wm.potionop", text= "Potion Shader", icon= 'SORTTIME')      


class WM_OT_Shortcut(Operator):
    """Custom Operator"""
    bl_label = "Add Shader Menu"
    bl_idname = "wm.call_shader_menu"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.menu("node.gem_MT_menu")
        box.menu("node.mat_MT_menu")
        box.menu("node.met_MT_menu")
        box.menu("node.stylized_MT_menu")
        
    def execute(self, context):
        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


addon_keymaps = []

classes = [ShaderLibraryProperties, WM_OT_Shortcut, NODE_MT_gems, NODE_MT_materials, NODE_MT_metallics, NODE_MT_stylized, ShaderMainPanel, SubPanelCosmic, SubPanelMaterials, SubPanelMetals, SubPanelPreciousMetals, SubPanelStylized, SHADER_OT_LEATHER, SHADER_OT_DIAMOND, SHADER_OT_GOLD, SHADER_OT_SILVER, SHADER_OT_COPPER, SHADER_OT_CLOUD, SHADER_OT_SCIFIGOLD, SHADER_OT_BRICK, WM_OT_ghostOp, WM_OT_hologramOp, WM_OT_neonOp, WM_OT_potionOp, SHADER_OT_COSMIC]

  
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type= 'VIEW_3D')
        kmi = km.keymap_items.new("wm.call_shader_menu", type= 'F', value= 'PRESS', shift= True)
        addon_keymaps.append((km, kmi))
    bpy.types.Scene.my_tool = PointerProperty(type= ShaderLibraryProperties)    
    


def unregister():
    del bpy.types.Scene.my_tool
    for km,kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    for cls in classes:
        bpy.utils.unregister_class(cls)
        

if __name__ == "__main__":
    register()