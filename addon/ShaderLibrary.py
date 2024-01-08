'''
Created on 08.01.2024

@author: Abdelmaw
'''



bl_info = {
    "name": "Shader Library",
    "author": "Abdelmawla Saeed Rizk abdelmawla.rizk@uni-paderborn.de",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "Right side panel > VIEW_3D > Shader Library",
    "description": "Shader Library to easily shade material "
}


register_List =[]
import bpy

class ShaderMainPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the auto Shader"""
    bl_label = "Shader Library"
    bl_idname =  "SHADER_PT_MAINPANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Add Shader'

    def draw(self, context):
        layout = self.layout

 
        # Big render button
        
        row = layout.row()
        row.label(text="select a shader to be added")
        row.operator('shader.diamond_operator')


register_List.append(ShaderMainPanel) 



class SHDER_OT_DIAMONMD(bpy.types.Operator):
    bl_label = "Diamond"
    bl_idname =  'shader.diamond_operator' 
    
    def execute(self, context ) :
        
        material_diamond = bpy.data.materials.new(name = "Diamond")
        material_diamond.use_nodes = True
        material_diamond.node_tree.nodes.remove(material_diamond.node_tree.nodes.get('Principled BSDF'))
        
        
        matewrial_output = material_diamond.node_tree.nodes.get('Material Output')
        matewrial_output.location = (-400,0)
 

        glass1_node = material_diamond.node_tree.nodes.new('ShaderNodeBsdfGlass')
        glass1_node.location = (-600,0)
        
        glass1_node.inputs[0].default_value = (1, 0, 0, 1)
        glass1_node.inputs[2].default_value = 1.450


 
        glass2_node = material_diamond.node_tree.nodes.new('ShaderNodeBsdfGlass')
        glass2_node.location = (-600,-150)
        
        glass2_node.inputs[0].default_value = (0, 1, 0, 1)
        glass2_node.inputs[2].default_value = 1.450
        
        
        glass3_node = material_diamond.node_tree.nodes.new('ShaderNodeBsdfGlass')
        glass3_node.location = (-600,-30)
        
        glass3_node.inputs[0].default_value = (0, 0, 1, 1)
        glass3_node.inputs[2].default_value = 1.450
        

        glass4_node = material_diamond.node_tree.nodes.new('ShaderNodeBsdfGlass')
        glass4_node.location = (-150,-150)
        
        glass4_node.inputs[0].default_value = (1, 1, 1, 1)
        glass4_node.inputs[2].default_value = 1.450

 

        Add1_node = material_diamond.node_tree.nodes.new('ShaderNodeAddShader')
        Add1_node.location = (-400,-50)
        Add1_node.label = "Add 1"
        Add1_node.hide = True
        Add1_node.select  = False


        Add2_node = material_diamond.node_tree.nodes.new('ShaderNodeAddShader')
        Add2_node.location = (-100, 0)
        Add2_node.label = "Add 2"
        Add2_node.hide = True
        Add2_node.select  = False
        
 
        mix_node = material_diamond.node_tree.nodes.new('ShaderNodeMixShader')
        mix_node.location = (200, 0)
        mix_node.select  = False 
        
        material_diamond.node_tree.links.new(glass1_node.outputs[0] ,Add1_node.inputs[0] )       
        material_diamond.node_tree.links.new(glass2_node.outputs[0] ,Add1_node.inputs[1] )
        
        material_diamond.node_tree.links.new(Add1_node.outputs[0] ,Add2_node.inputs[0] )        
        material_diamond.node_tree.links.new(glass3_node.outputs[0] ,Add2_node.inputs[1] )
        
        material_diamond.node_tree.links.new( Add2_node.outputs[0] , mix_node.inputs[1]  )
        material_diamond.node_tree.links.new( glass4_node.outputs[0] , mix_node.inputs[2]  )        
        
        material_diamond.node_tree.links.new( mix_node.outputs[0] , matewrial_output.inputs[0]  )  
        
 
        bpy.context.object.active_material = material_diamond
                         
        #return bpy.types.Operator.execute(self, context)   
        return {'FINISHED'}

register_List.append(SHDER_OT_DIAMONMD) 

def register():
    for cl in register_List:
        bpy.utils.register_class(cl)
 


def unregister():
    for cl in register_List:
        bpy.utils.unregister_class(cl)
 


if __name__ == "__main__":
    register()
    