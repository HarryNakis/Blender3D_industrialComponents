bl_info = {
    "name": "New Conveyor",
    "author": "Harry Nakis",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Linear Conveyor",
    "description": "Adds a new Linear Conveyor",
    "warning": "",
    "wiki_url": "",
    "category": "Add Linear Conveyor",
}


import bpy
from bpy.types import Operator
from bpy_extras.object_utils import AddObjectHelper, object_data_add


def CreateSimpleMaterial(name, color, intensity):
    # Create a simple material 
    simpleMaterial = bpy.data.materials.new(name)
    simpleMaterial.diffuse_color = color
    simpleMaterial.specular_intensity = intensity
    return simpleMaterial


def add_object(self, context):
    
    cy_radius = self.conv_cylinder_radius

    # Calculations
    conv_cylinders = int(round(self.conv_length / (cy_radius*2*1.1)))+1
    pitch = self.conv_length / (conv_cylinders-1)
    thickness = self.conv_width/20
    half_width = self.conv_width/2

    leg_number = int(self.conv_length)-1
    if int(self.conv_length)>0:
        leg_distance = self.conv_length / int(self.conv_length)

    # Create materials for rollers and legs
    mat_frame   = CreateSimpleMaterial ( "rollers",[0.214041, 0.214041, 0.214041, 1] ,0.5)
    mat_rollers = CreateSimpleMaterial ( "frame",[1, 1, 1, 1] ,1)



    # Deselect all objects 
    bpy.ops.object.select_all(action='DESELECT')
    
    # Conveyor rollers
    if self.conv_roller:
        for j in range (0, conv_cylinders-1):
            #Create Cylinder
            bpy.ops.mesh.primitive_cylinder_add(vertices=26, radius=cy_radius, depth=self.conv_width, location=(j*pitch+cy_radius, 0, 0), rotation=(1.5708, 0, 0))
            cyl = bpy.context.active_object
            cyl.name = ( "Cylinder"+str(j) )
            # Assign the color to the cylinders
            bpy.context.object.data.materials.append(mat_rollers)

        for j in range (0, conv_cylinders-1):
            bpy.data.objects["Cylinder"+str(j)].select_set(True)
        
       
             
    else:
        bpy.ops.mesh.primitive_cylinder_add(vertices=26, radius=cy_radius, depth=self.conv_width, location=(cy_radius, 0, 0), rotation=(1.5708, 0, 0))
        bpy.context.object.data.materials.append(mat_rollers)
        cyl = bpy.context.active_object
        cyl.name = ( "Cylinder1" )
        bpy.ops.mesh.primitive_cylinder_add(vertices=26, radius=cy_radius, depth=self.conv_width, location=((conv_cylinders-2)*pitch+cy_radius, 0, 0), rotation=(1.5708, 0, 0))
        bpy.context.object.data.materials.append(mat_rollers)
        cyl = bpy.context.active_object
        cyl.name = ( "Cylinder2" )
        bpy.ops.mesh.primitive_cube_add(location=( self.conv_length/2, 0, 0), size =1)
        cyl = bpy.context.active_object
        cyl.name = ( "cube1" )

        bpy.context.object.data.materials.append(mat_rollers)
        bpy.ops.transform.resize(value=( self.conv_length-(cy_radius*2), self.conv_width, cy_radius*2))
        bpy.context.object.data.materials.append(mat_rollers)
        
        bpy.data.objects["Cylinder1"].select_set(True)
        bpy.data.objects["Cylinder2"].select_set(True)  
        bpy.data.objects["cube1"].select_set(True)
                 
         
    # Join all rollers    
    bpy.ops.object.join()   
                         
    cyl = bpy.context.active_object
    cyl.name = ("rollers")     
    

    # Side 1
    bpy.ops.mesh.primitive_cube_add(location=( self.conv_length/2, half_width, 0), size =1)
    bpy.ops.transform.resize(value=( self.conv_length, thickness, cy_radius*2.3))
    bpy.context.object.data.materials.append(mat_frame)
    obj = bpy.context.active_object
    obj.name = ( "side1" )
    
    # Side 2
    bpy.ops.mesh.primitive_cube_add(location=( self.conv_length/2, -half_width, 0), size =1)
    bpy.ops.transform.resize(value=( self.conv_length, thickness, cy_radius*2.3))
    bpy.context.object.data.materials.append(mat_frame)
    obj = bpy.context.active_object
    obj.name = ( "side2" )

    
    
    # left Leg 1
    bpy.ops.mesh.primitive_cube_add(location=( thickness*2, half_width+thickness/2, -self.conv_leg_length/2), size =1)
    bpy.ops.transform.resize(value=( thickness, thickness, self.conv_leg_length))
    bpy.context.object.data.materials.append(mat_frame)
    obj = bpy.context.active_object
    obj.name = ( "FirstLeftleg1" )

    # left Leg 2
    bpy.ops.mesh.primitive_cube_add(location=( self.conv_length-(thickness*2), half_width+thickness/2, -self.conv_leg_length/2), size =1)
    bpy.ops.transform.resize(value=( thickness, thickness, self.conv_leg_length))
    bpy.context.object.data.materials.append(mat_frame)
    obj = bpy.context.active_object
    obj.name = ( "FirstLeftleg2" )

    # Right Leg 3
    bpy.ops.mesh.primitive_cube_add(location=( thickness*2, -half_width-thickness/2, -self.conv_leg_length/2), size =1)
    bpy.ops.transform.resize(value=( thickness, thickness, self.conv_leg_length))
    bpy.context.object.data.materials.append(mat_frame)
    obj = bpy.context.active_object
    obj.name = ( "Endrightleg1" )

    # Right Leg 4
    bpy.ops.mesh.primitive_cube_add(location=( self.conv_length-(thickness*2), -half_width-thickness/2, -self.conv_leg_length/2), size =1)
    bpy.ops.transform.resize(value=( thickness, thickness, self.conv_leg_length))
    bpy.context.object.data.materials.append(mat_frame)
    obj = bpy.context.active_object
    obj.name = ( "Endrightleg2" )



    # Middle legs. 1 every meter
    for k in range (1, leg_number+1):
        # left Leg 1
        bpy.ops.mesh.primitive_cube_add( location = ((k*leg_distance), half_width+thickness/2, -self.conv_leg_length/2), size =1)
        bpy.ops.transform.resize(value=( thickness, thickness, self.conv_leg_length))
        bpy.context.object.data.materials.append(mat_frame)
        cyl = bpy.context.active_object
        cyl.name = ( "leftleg"+str(k) )        

        # left Leg 3
        bpy.ops.mesh.primitive_cube_add( location = ((k*leg_distance), -half_width-thickness/2, -self.conv_leg_length/2), size =1)
        bpy.ops.transform.resize(value=( thickness, thickness, self.conv_leg_length))
        bpy.context.object.data.materials.append(mat_frame)
        cyl = bpy.context.active_object
        cyl.name = ( "rightleg"+str(k) )        


    # Join sides and legs
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects["side1"].select_set(True)
    bpy.data.objects["side2"].select_set(True)
    bpy.data.objects["FirstLeftleg1"].select_set(True)
    bpy.data.objects["FirstLeftleg2"].select_set(True)
    bpy.data.objects["Endrightleg1"].select_set(True)
    bpy.data.objects["Endrightleg2"].select_set(True)        


    for k in range (1, leg_number+1):
        bpy.data.objects["leftleg"+str(k)].select_set(True)
        bpy.data.objects["rightleg"+str(k)].select_set(True)


    bpy.ops.object.join()
    legs = bpy.context.active_object
    legs.name = ("legs")
    
    
    # Joing the whole conveyor
    bpy.data.objects["rollers"].select_set(True)
    bpy.data.objects["legs"].select_set(True)
    bpy.ops.object.join()

    #Elevate object by the height of legs    
    bpy.ops.transform.translate(value=(0, 0, self.conv_leg_length), orient_type='GLOBAL')

    
    bpy.ops.object.select_all(action='DESELECT')





    
class OBJECT_OT_add_object(Operator):
    """Create a new Linear conveyor"""
    bl_idname = "mesh.add_object"
    bl_label = "Add Linear Conveyor Object"
    bl_options = {'REGISTER', 'UNDO'}

    
    conv_roller          : bpy.props.BoolProperty(name="Roller Conveyor" ,default=1)
    conv_width           : bpy.props.FloatProperty(name="Width" ,default=1, min=0.1, max=4.0)
    conv_length          : bpy.props.FloatProperty(name="Length" ,default=2, min=0.5, max=10.0)
    conv_cylinder_radius : bpy.props.FloatProperty(name="Cylinder radius" ,default=0.03, min=0.01, max=0.5)
    conv_leg_length      : bpy.props.FloatProperty(name="Legs Length" ,default=0.5, min=0.02, max=2.0)



    def execute(self, context):
        add_object(self, context)
        return {'FINISHED'}


# Registration

def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Add Linear Conveyor",
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
