bl_info = {
    "name": "New Fence",
    "author": "Harry Nakis",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > Factory > New fence",
    "description": "Adds a new fence",
    "warning": "",
    "wiki_url": "",
    "category": "Add Fence",
}


import bpy
from bpy.types import Operator
from bpy_extras.object_utils import AddObjectHelper, object_data_add



def NameActiveObject(name, index, increase=False):
    # Create a simple material 
    obj = bpy.context.active_object
    obj.name = ( name+str(index) )

    if increase:
        index += 1    
    return  index



def CreateSimpleMaterial(name, color, intensity):
    # Create a simple material 
    simpleMaterial = bpy.data.materials.new(name)
    simpleMaterial.diffuse_color = color
    simpleMaterial.specular_intensity = intensity
    return simpleMaterial



def add_object(self, context):
    
    # Calculations
    poles = int(round(self.length))+1
    pitch =  self.length /(poles -1)
    thickness = self.thickness #0.05 #self.conv_width/20
    leg_length = self.leg_height


    # Create materials for rollers and legs
    mat_frame   = CreateSimpleMaterial ( "rollers",[1, 1, 0, 1] ,0.5)
    mat_rollers = CreateSimpleMaterial ( "frame",[0, 0, 0, 1] ,1)


    #-------------------------------------------------------------

    # Create Vertical Poles
    for j in range (0, poles):
        #Create Cylinder
        bpy.ops.mesh.primitive_cube_add(location=( (j*pitch), 0, self.height/2-leg_length/2), size =1)
        bpy.ops.transform.resize(value=( thickness, thickness, self.height+leg_length))
        bpy.context.object.data.materials.append(mat_frame)
        NameActiveObject("pole", j)
        #obj = bpy.context.active_object
        #obj.name = ( "pole"+str(j) )
        
        #Create platesk
        bpy.ops.mesh.primitive_cube_add(location=( (j*pitch), 0, -leg_length), size =1)
        bpy.ops.transform.resize(value=( thickness*4, thickness*4, 0.015))
        bpy.context.object.data.materials.append(mat_frame)
        NameActiveObject("plate", j)

        

    # Select & join
    for j in range (0, poles):
        bpy.data.objects["pole"+str(j)].select_set(True)
        bpy.data.objects["plate"+str(j)].select_set(True)        
    bpy.ops.object.join()
    obj = bpy.context.active_object
    obj.name = ( "poles1" )
 
    #-------------------------------------------------------------
    
    grid_num = 1
    for j in range (0, poles-1):
        
        bpy.ops.mesh.primitive_cube_add(location=( (j*pitch)+(thickness-thickness/4), 0, self.height/2), size =1)
        bpy.ops.transform.resize(value=( thickness/2, thickness/2, self.height))
        bpy.context.object.data.materials.append(mat_rollers) 
        grid_num = NameActiveObject("grid", grid_num, True)

        bpy.ops.mesh.primitive_cube_add(location=( (j*pitch)+pitch-(thickness-thickness/4), 0, self.height/2), size =1)
        bpy.ops.transform.resize(value=( thickness/2, thickness/2, self.height))      
        bpy.context.object.data.materials.append(mat_rollers)
        grid_num = NameActiveObject("grid", grid_num, True)
        #obj = bpy.context.active_object
        #obj.name = ( "grid"+str(grid_num) )             
        #grid_num += 1
        
        
        for k in range (1, 11):
            bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=thickness*0.1, depth=self.height, location=((j*pitch)+(k*(pitch/12))+thickness*0.6, 0, self.height/2), rotation=(0, 0, 0))
            # Assign the color to the cylinders
            bpy.context.object.data.materials.append(mat_rollers)
            grid_num = NameActiveObject("grid", grid_num, True)
                
                

        # Horizontal 1
        bpy.ops.mesh.primitive_cube_add(location=( (j*pitch)+pitch/2, 0, 0), size =1)
        bpy.ops.transform.resize(value=( pitch-thickness, thickness/2, thickness/2))
        bpy.context.object.data.materials.append(mat_rollers)
        grid_num = NameActiveObject("grid", grid_num, True)

                    
        # Horizontal 2
        bpy.ops.mesh.primitive_cube_add(location=( (j*pitch)+pitch/2, 0, self.height/2), size =1)
        bpy.ops.transform.resize(value=( pitch-thickness, thickness/2, thickness/2))
        bpy.context.object.data.materials.append(mat_rollers)
        grid_num = NameActiveObject("grid", grid_num, True)

                
        # Horizontal 3
        bpy.ops.mesh.primitive_cube_add(location=( (j*pitch)+pitch/2, 0, self.height-thickness/4), size =1)
        bpy.ops.transform.resize(value=( pitch-thickness, thickness/2, thickness/2))
        bpy.context.object.data.materials.append(mat_rollers)
        grid_num = NameActiveObject("grid", grid_num, True)

        
        
    # Deselect all objects 
    #bpy.ops.object.select_all(action='DESELECT')                

    # Select & join
    for j in range (1, grid_num-1):
        bpy.data.objects["grid"+str(j)].select_set(True)
    bpy.ops.object.join()    
    obj = bpy.context.active_object
    obj.name = ( "planes" )
       

    #a = bpy.data.objects['poles1']
    #b = bpy.data.objects['planes']
    #parent_object = bpy.data.objects.new('parent_object', None)
    #bpy.context.scene.collection.objects.link(parent_object)
    #a.parent = parent_object
    #b.parent = parent_object
    #bpy.context.view_layer.update()


    # Join All objects
    #bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects["poles1"].select_set(True)
    bpy.data.objects["planes"].select_set(True)
    bpy.ops.object.join()
    obj = bpy.context.active_object
    obj.name = ( "fence" )


    #Elevate object by the height of legs    
    bpy.ops.transform.translate(value=(0, 0, leg_length), orient_type='GLOBAL')
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
    bpy.ops.object.select_all(action='DESELECT')





    
class OBJECT_OT_add_object(Operator):
    """Create a fence"""
    bl_idname = "mesh.add_fence"
    bl_label = "Add fence Object"
    bl_category = 'Factory'
    bl_options = {'REGISTER', 'UNDO'}

    
    height          : bpy.props.FloatProperty(name="Height" ,default=2, min=0.5, max=4.0)
    leg_height      : bpy.props.FloatProperty(name="Leg Height" ,default=0.2, min=0.1, max=0.5)
    length          : bpy.props.FloatProperty(name="Length" ,default=2, min=1, max=10.0)
    thickness       : bpy.props.FloatProperty(name="Thickness" ,default=0.05, min=0.05, max=0.1)



    def execute(self, context):
        add_object(self, context)
        return {'FINISHED'}


# Registration
def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Add Fence",
        icon='PLUGIN')


# This allows you to right click on a button and link to documentation
def add_object_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),
    )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)



if __name__ == "__main__":
    register()
