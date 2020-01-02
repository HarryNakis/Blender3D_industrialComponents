bl_info = {
    "name": "New Curved Conveyor",
    "author": "Harry Nakis",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Curved Conveyor",
    "description": "Adds a new Curved Conveyor",
    "warning": "",
    "wiki_url": "",
    "category": "Add Curved Conveyor",
}


import bpy
from bpy.types import Operator
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from math import pi


def CreateSimpleMaterial(name, color, intensity):
    # Create a simple material 
    simpleMaterial = bpy.data.materials.new(name)
    simpleMaterial.diffuse_color = color
    simpleMaterial.specular_intensity = intensity
    return simpleMaterial


def my_spin(leg_number, spin_angle):
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.spin(steps=leg_number ,dupli=True, angle=spin_angle, use_auto_merge=False, center=(0, 0, 0), axis=(0, 0, 1))
    bpy.ops.object.editmode_toggle()


def my_spin_extrude(spin_steps, spin_angle):
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.spin(steps=spin_steps, angle=spin_angle, center=(0, 0, 0), axis=(-0, -0, -1))
    bpy.ops.object.editmode_toggle()
    
    
def add_object(self, context):
    
    cy_radius = self.conv_cylinder_radius
    conv_length = 2*pi* (self.rot_distance+self.conv_width)*(self.conv_angle/360)

    # Calculations
    conv_cylinders = int(round(conv_length / (cy_radius*2*2) ))  
    thickness = self.conv_width/20
    leg_number = int(self.conv_angle/45)+1
    conv_z_angle = (pi * self.conv_angle / 180)


    # Create materials for rollers and legs
    mat_frame   = CreateSimpleMaterial ( "rollers",[0.214041, 0.214041, 0.214041, 1] ,0.5)
    mat_rollers = CreateSimpleMaterial ( "frame",[1, 1, 1, 1] ,1)
    

    # --- CREATE ANGLE CONVEYOR ---

    # Conveyor rollers     
    bpy.ops.mesh.primitive_cylinder_add(vertices=26, radius=cy_radius, depth=self.conv_width, location=(0, -self.rot_distance-(self.conv_width/2), 0), rotation=(1.5708, 0, 0))
    my_spin(conv_cylinders, -conv_z_angle+(pi * 1.5 / 180) )        

    # Assign the color to the cylinders
    bpy.context.object.data.materials.append(mat_rollers)
    
    obj = bpy.context.active_object
    obj.name = ( "rollers" )

    
    

    # Side rail 1
    bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(-cy_radius, -self.rot_distance, 0), rotation=(0, 1.5708, 0), size =1)
    bpy.ops.transform.resize(value=( 0, thickness, cy_radius*2.3))
    my_spin_extrude(conv_cylinders, conv_z_angle+(pi * 2 / 180))
    bpy.context.object.data.materials.append(mat_frame)
    obj = bpy.context.active_object
    obj.name = ( "side1" )
    

    # Side rail 2
    bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(-cy_radius, -self.rot_distance-self.conv_width, 0), rotation=(0, 1.5708, 0), size =1)
    bpy.ops.transform.resize(value=( 0, thickness, cy_radius*2.3))
    my_spin_extrude(conv_cylinders, conv_z_angle+(pi * 1 / 180) )
    bpy.context.object.data.materials.append(mat_frame)
    obj = bpy.context.active_object
    obj.name = ( "side2" )
        
        
    
    # left Legs
    bpy.ops.mesh.primitive_cube_add(location=( 0, -self.rot_distance+thickness/2, -self.conv_leg_length/2), size =1)
    bpy.ops.transform.resize(value=( thickness, thickness, self.conv_leg_length))
    my_spin(leg_number, -conv_z_angle+(pi * 1.5 / 180))
    bpy.context.object.data.materials.append(mat_frame)
    obj = bpy.context.active_object
    obj.name = ( "leg1" )
    

    # Right Legs
    bpy.ops.mesh.primitive_cube_add(location=( 0, -self.rot_distance-self.conv_width-thickness/2, -self.conv_leg_length/2), size =1)
    bpy.ops.transform.resize(value=( thickness, thickness, self.conv_leg_length))
    my_spin(leg_number, -conv_z_angle+(pi * 1.5 / 180))
    bpy.context.object.data.materials.append(mat_frame)
    obj = bpy.context.active_object
    obj.name = ( "leg2" )



    # Join sides and legs
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects["rollers"].select_set(True)
    bpy.data.objects["side1"].select_set(True)
    bpy.data.objects["side2"].select_set(True)
    bpy.data.objects["leg1"].select_set(True)
    bpy.data.objects["leg2"].select_set(True)


    bpy.ops.object.join()
    legs = bpy.context.active_object
    legs.name = ("CurvedConveyor")
    
    bpy.ops.transform.translate(value=(0, 0, self.conv_leg_length), orient_type='GLOBAL')
    

    # Deselect all objects 
    bpy.ops.object.select_all(action='DESELECT')








class OBJECT_OT_add_object(Operator):
    """Create a new curved conveyor"""
    bl_idname = "mesh.add_angle_conveyor"
    bl_label = "Add curved Conveyor Object"
    bl_options = {'REGISTER', 'UNDO'}

    
    #conv_roller          : bpy.props.BoolProperty(name="Roller Conveyor" ,default=1)

    conv_angle           : bpy.props.FloatProperty(name="Angle" ,default=90, min=10, max=180)
    rot_distance         : bpy.props.FloatProperty(name="Rotation Distance" ,default=1, min=0.1, max=4.0)
    conv_width           : bpy.props.FloatProperty(name="Width" ,default=1, min=0.1, max=4.0)
    conv_cylinder_radius : bpy.props.FloatProperty(name="Cylinder radius" ,default=0.03, min=0.01, max=0.5)
    conv_leg_length      : bpy.props.FloatProperty(name="Legs Length" ,default=0.5, min=0.02, max=2.0)



    def execute(self, context):
        add_object(self, context)
        return {'FINISHED'}


# Registration

def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Add curved Conveyor",
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
