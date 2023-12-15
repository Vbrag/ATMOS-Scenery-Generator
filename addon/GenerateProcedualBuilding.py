import contextlib
import bpy
import bmesh
import math
import mathutils
import numpy
import os
import random
from array import *


import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, currentdir) 

import  osm_map as  osm_map



@contextlib.contextmanager
def transfer_bmesh_edit_mode(mesh_obj):
    bm_module = bmesh.from_edit_mesh(mesh_obj.data)
    yield bm_module
    bm_module.free()
    
@contextlib.contextmanager
def transfer_bmesh_object_mode(mesh_obj):
    bm_module = bmesh.new()
    bm_module.from_mesh(mesh_obj.data, face_normals=False, vertex_normals=True)
    yield bm_module
    bm_module.free()
    
@contextlib.contextmanager
def transfer_bmesh(mesh_obj):
    if bpy.context.mode == "OBJECT":
        with transfer_bmesh_object_mode(mesh_obj) as bm_module:
            yield bm_module
    elif bpy.context.mode == "EDIT_MESH":
        with transfer_bmesh_edit_mode(mesh_obj) as bm_module:
            yield bm_module
    else:
        print("invalid mode")
        
@contextlib.contextmanager
def copy_bmesh_edit_mode(mesh_obj_source, mesh_obj_target):
    bm_copy = bmesh.from_edit_mesh(mesh_obj_source.data)
    yield bm
    #bm_copy.normal_update()
    bmesh.update_edit_mesh(mesh_obj_target.data)
    bm_copy.free()
    
@contextlib.contextmanager
def copy_bmesh_object_mode(mesh_obj_source, mesh_obj_target):
    bm_copy = bmesh.new()
    bm_copy.from_mesh(mesh_obj_source.data, face_normals=False, vertex_normals=True)
    yield bm
    #bm_copy.normal_update()
    bm_copy.to_mesh(mesh_obj_target.data)
    mesh_obj_target.data.update()
    bm_copy.free()
    
@contextlib.contextmanager
def copy_bmesh(mesh_obj_source, mesh_obj_target):
    if bpy.context.mode == "OBJECT":
        with copy_bmesh_object_mode(mesh_obj_source, mesh_obj_target) as bm_copy:
            yield bm_copy
    elif bpy.context.mode == "EDIT_MESH":
        with copy_bmesh_edit_mode(mesh_obj_source, mesh_obj_target) as bm_copy:
            yield bm_copy
    else:
        print("invalid mode")
        
@contextlib.contextmanager
def get_bmesh_edit_mode(mesh_obj):
    bm = bmesh.from_edit_mesh(mesh_obj.data)
    yield bm
    #bm.normal_update()
    bmesh.update_edit_mesh(mesh_obj.data)
    bm.free()
    
@contextlib.contextmanager
def get_bmesh_object_mode(mesh_obj):
    bm = bmesh.new()
    bm.from_mesh(mesh_obj.data, face_normals=False, vertex_normals=True)
    yield bm
    #bm.normal_update()
    bm.to_mesh(mesh_obj.data)
    mesh_obj.data.update()
    bm.free()
    
@contextlib.contextmanager
def get_bmesh(mesh_obj):
    if bpy.context.mode == "OBJECT":
        with get_bmesh_object_mode(mesh_obj) as bm:
            yield bm
    elif bpy.context.mode == "EDIT_MESH":
        with get_bmesh_edit_mode(mesh_obj) as bm:
            yield bm
    else:
        print("invalid mode")
    
def create_custom_mesh(objname, coords, height):
    # Define arrays for holding data    
    myvertex = []
    #myface = []
    myfaces = []
    for vert_counter in range(len(coords)):
        myvertex.extend([(coords[vert_counter][0], coords[vert_counter][1], height)])
        #myface.append(vert_counter)

    # Create all Faces
    myface = [range(len(coords))] # [(0, 1, 3, 2)]
    myfaces.extend(myface)
    
    mymesh = bpy.data.meshes.new(objname)

    myobject = bpy.data.objects.new(objname, mymesh)

    bpy.context.scene.collection.objects.link(myobject)
    
    # Generate mesh data
    mymesh.from_pydata(myvertex, [], myfaces)
    # Calculate the edges
    mymesh.update(calc_edges=True)

    return myobject

def findClockwiseAngle(vector_a, vector_b):
    # using cross-product formula
    return math.asin((vector_a.x * vector_b.y - vector_a.y * vector_b.x)/(vector_a.length()*vector_b.length()))
    # the dot-product formula, left here just for comparison (does not return angles in the desired range)
    # return math.degrees(math.acos((self.a * other.a + self.b * other.b)/(self.length()*other.length())))

def calculate_inner_angle(coordinates):
    inner_angle = 0
    for counter in range(len(coordinates) - 1):
        #inner_angle += math.atan2(coordinates[counter + 1][1], coordinates[counter + 1][0]) - math.atan2(coordinates[counter][1], coordinates[counter][0])
        if counter > 0:
            vector_a = mathutils.Vector((coordinates[counter][0] - coordinates[counter-1][0], coordinates[counter][1] - coordinates[counter - 1][1]))
            vector_b = mathutils.Vector((coordinates[counter + 1][0] - coordinates[counter][0], coordinates[counter + 1][1] - coordinates[counter][1]))
        else:
            vector_a = mathutils.Vector((coordinates[counter][0] - coordinates[len(coordinates)-2][0], coordinates[counter][1] - coordinates[len(coordinates)-2][1]))
            vector_b = mathutils.Vector((coordinates[counter + 1][0] - coordinates[counter][0], coordinates[counter + 1][1] - coordinates[counter][1]))

        inner_angle += vector_a.angle_signed(vector_b)
        #inner_angle += findClockwiseAngle(vector_a, vector_b)
    return inner_angle

for obj in bpy.context.scene.objects:
    bpy.data.objects.remove(obj, do_unlink=True)

for myCol in bpy.data.collections:
    bpy.data.collections.remove(myCol)

modular_assets_collection = bpy.data.collections.new("")
modular_assets_collection.name = "modular_assets_collection"
bpy.context.scene.collection.children.link(modular_assets_collection)

ground_floor_collection = bpy.data.collections.new("")
ground_floor_collection.name = "ground_floor_collection"
ground_floor_walls_collection = bpy.data.collections.new("")
ground_floor_walls_collection.name = "ground_floor_walls_collection"
ground_floor_pillars_collection = bpy.data.collections.new("")
ground_floor_pillars_collection.name = "ground_floor_pillars_collection"
modular_assets_collection.children.link(ground_floor_collection)
ground_floor_collection.children.link(ground_floor_walls_collection)
ground_floor_collection.children.link(ground_floor_pillars_collection)

middle_floor_collection = bpy.data.collections.new("")
middle_floor_collection.name = "middle_floor_collection"
middle_floor_walls_collection = bpy.data.collections.new("")
middle_floor_walls_collection.name = "middle_floor_walls_collection"
middle_floor_pillars_collection = bpy.data.collections.new("")
middle_floor_pillars_collection.name = "middle_floor_pillars_collection"
modular_assets_collection.children.link(middle_floor_collection)
middle_floor_collection.children.link(middle_floor_walls_collection)
middle_floor_collection.children.link(middle_floor_pillars_collection)

top_floor_collection = bpy.data.collections.new("")
top_floor_collection.name = "top_floor_collection"
top_floor_trim_collection = bpy.data.collections.new("")
top_floor_trim_collection.name = "top_floor_trim_collection"
top_floor_pillars_collection = bpy.data.collections.new("")
top_floor_pillars_collection.name = "top_floor_pillars_collection"
modular_assets_collection.children.link(top_floor_collection)
top_floor_collection.children.link(top_floor_trim_collection)
top_floor_collection.children.link(top_floor_pillars_collection)

unidentified_collection = bpy.data.collections.new("")
unidentified_collection.name = "unidentified_collection"
modular_assets_collection.children.link(unidentified_collection)

# Import FBX
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'buildify_1.0_assets.fbx')
Osmfilename = os.path.join(dirname, './Data/WesternTor_2.osm')


bpy.ops.import_scene.fbx( filepath = filename )

# If there ARE objects selected then act on all objects
if bpy.context.selected_objects != []:
    for obj in bpy.context.selected_objects:
        for other_col in obj.users_collection:
            other_col.objects.unlink(obj)
        categories = obj.name.split("_")
        # print(categories)
        if 'ground' in categories:
            if 'wall' in categories:
                ground_floor_walls_collection.objects.link(obj)
            elif 'pillar' in categories:
                ground_floor_pillars_collection.objects.link(obj)
        elif 'middle' in categories:
            if 'wall' in categories:
                middle_floor_walls_collection.objects.link(obj)
            elif 'pillar' in categories:
                middle_floor_pillars_collection.objects.link(obj)
        elif 'trim' in categories or 'trimm' in categories:
            if 'trimm' in categories:
                top_floor_trim_collection.objects.link(obj)
            elif 'pillar' in categories:
                top_floor_pillars_collection.objects.link(obj)
        else:
            unidentified_collection.objects.link(obj)

collectionCounter = -1
for collection in bpy.data.collections:
    objCounter = -1
    for obj in collection.objects:
        objCounter += 1
        if objCounter == 0:
            collectionCounter += 1
        obj.location = (objCounter * 3.5, 30 + collectionCounter * 3.0, 0.0)
        
# settings
module_width = 3.0
module_height = 3.0





def doBuilding(cross_section_co ,number_of_floors ):

    if (cross_section_co[0][0] != cross_section_co[len(cross_section_co)-1][0] or cross_section_co[0][1] != cross_section_co[len(cross_section_co)-1][1]):
            cross_section_co.append(cross_section_co[0])

    inner_angle = calculate_inner_angle(cross_section_co)
    
    if inner_angle < 0:
        normal_dir_scale = -1
    else:
        normal_dir_scale = 1

    current_building_obj = create_custom_mesh("building obj " + str(building_counter), cross_section_co, number_of_floors  * module_height)
    temporary_mesh = bpy.data.meshes.new( "temporary mesh" )
    temporary_obj = bpy.data.objects.new( "temporary obj" , temporary_mesh)

    with get_bmesh(current_building_obj) as bm:
        # neccessary for indexing
        if hasattr(bm.verts, "ensure_lookup_table"): 
            bm.verts.ensure_lookup_table()

        number_of_edges = len(cross_section_co)-1
        # loop through boundy edges
        #for edge_temporary in outer_edges:
        for edge_counter in range(number_of_edges):
            edge_start = mathutils.Vector((cross_section_co[edge_counter][0],cross_section_co[edge_counter][1], 0)) # edge_temporary.verts[0].co
            edge_end = mathutils.Vector((cross_section_co[edge_counter + 1][0],cross_section_co[edge_counter + 1][1], 0))  # edge_temporary.verts[1].co
            # calculate number of edges and scale modules to fit the edge length
            edge_length = numpy.linalg.norm(edge_end - edge_start)
            #print(edge_length)
            edge_tangent = (edge_end - edge_start) / edge_length
            assets_on_edge = math.floor(edge_length / module_width)
            #print(assets_on_edge)
            scaled_module_width = edge_length / max(assets_on_edge, 1.0)
            #print(scaled_module_width)
            edge_normal = normal_dir_scale * mathutils.Vector((-edge_tangent.y, edge_tangent.x, 0.0)) # numpy.cross(edge_tangent, mathutils.Vector((0.0, 0.0, 1.0)))
            rotation_angle = math.atan2(edge_normal.y, edge_normal.x)
            rotation_Z = mathutils.Matrix.Rotation(math.pi / 2 + rotation_angle, 4, 'Z') # angle(edge_normal, mathutils.Vector((0.0,-1.0,0.0)))
            
            # loop through floors
            for floor_count in range(number_of_floors  + 1 ):
                # for each module on this edge
                for module_count in range(assets_on_edge):
                    # calculate module position on edge
                    position = edge_start + edge_tangent * scaled_module_width * (module_count + 0.5)
                    position.z += floor_count * module_height

                    # select collection based on floor_count
                    if floor_count == 0:
                        collection_name = "ground_floor_walls_collection"
                    elif floor_count < number_of_floors :
                        collection_name = "middle_floor_walls_collection"
                    else:
                        collection_name = "top_floor_trim_collection"
                    
                    collection = bpy.data.collections.get(collection_name)
                    
                    # randomly select module from the collection
                    random_index = random.randint(0, len(collection.objects)-1)
                    modular_asset = collection.objects[random_index]

                    material_mapping = {}
                    # collect unique materials from module
                    for asset_material_index in range( len( modular_asset.data.materials ) ):
                    
                        asset_material = modular_asset.data.materials[ asset_material_index ]
                        building_has_material = False
                        
                        for building_material_index in range( len( current_building_obj.data.materials ) ):
                            building_material = current_building_obj.data.materials[ building_material_index ]
                            if asset_material.name == building_material.name:
                                building_has_material = True
                                material_mapping[ "mat_" + str(asset_material_index) ] = building_material_index
                                break
                            
                        if not building_has_material:
                            material_mapping[ "mat_" + str(asset_material_index) ] = len( current_building_obj.data.materials )
                            current_building_obj.data.materials.append(asset_material)

                    center = sum((mathutils.Vector(b) for b in modular_asset.bound_box), mathutils.Vector())
                    center /= 8
                    # add module mesh to building mesh                
                    bm_copy = bmesh.new()
                    bm_copy.from_mesh(modular_asset.data, face_normals=False, vertex_normals=True)
                    #print("number of vertices: " + str(len(bm_copy.verts)))
                    for vert_module in bm_copy.verts:
                        vert_module.co.x *= scaled_module_width / module_width
                        vert_module.co.y *= scaled_module_width / module_width

                    bmesh.ops.rotate(bm_copy, cent=center, matrix=rotation_Z, verts=bm_copy.verts)

                    for vert_module in bm_copy.verts:
                        vert_module.co += position - mathutils.Vector((center.x, center.y, 0.0))
                    
                    for face_module in bm_copy.faces:
                        face_module.material_index = material_mapping[ "mat_" + str(face_module.material_index) ] # material_mapping[face_module.material_index]
                        #print(str(material_mapping[ "mat_" + str(0) ]))

                    #bm_copy.normal_update()
                    bm_copy.to_mesh(temporary_obj.data)
                    temporary_obj.data.update()
                    bm_copy.free()
                    bm.from_mesh( temporary_obj.data, face_normals=False, vertex_normals=True)
                    bm.verts.index_update()

        for faces in bm.faces:
            faces.smooth = False



number_of_floorsdict = {}
number_of_floorsdict[0] = 7
number_of_floorsdict[1] = 3
 


# add dummy cross section (to be changed with cross section form osm data)
cross_sections = {}
cross_sections[0] = [(-20,-20),(-20,20), (40,20), (40,-20), (10,-20), (10,-10), (-10,-10),(-10,-20), (-20,-20)]
cross_sections[1] = [(-40,-20), (-30,-20),(-30,10), (-40,10)]
 
 

for building_counter in range(len(cross_sections)):
 
    cross_section_co = cross_sections[building_counter]
    number_of_floors = number_of_floorsdict[building_counter]

    doBuilding(cross_section_co, number_of_floors)


 

