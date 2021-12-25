import bpy
import numpy as np
import os
import random
import time 
import json



start = time.time() 
start_image = 0
end_image = 12
false_list = [16,31,33,38,48,64,72,73,78,87,163,188]
for img_id in false_list:   #range(start_image, end_image):  
      
    if os.path.isfile("/home/nhan/longpipe_annotation.json"):
        with open('/home/nhan/longpipe_annotation.json', 'r') as file:
            annotation = json.load(file)
    else:
        annotation = {"time": [], "num_images": []}
        
    pi = np.pi
    # box dimension
#    box = bpy.data.objects["box"]
#    box.dimensions = [0.3, 0.4, 0.15]
#    plane1 = bpy.data.objects["Plane1"]
#    plane1.dimensions = [0.3, 0.4, 2.0]
    # Light settings
    light = bpy.data.objects["Light"]
    light.rotation_euler[0] = np.random.choice(range(-10,10,2))/180*pi  #radian   [-45,45]
    light.rotation_euler[1] = np.random.choice(range(-10,10,2))/180*pi 
    light.data.energy = 0.5*random.random() + 1.0
    light.data.color = (1,1,1)
    light_paras = [light.rotation_euler[0], light.rotation_euler[1],
                   light.data.energy] 
   
    # Camera settings
    camera = bpy.data.objects["Camera"]
    camera.rotation_euler[0] = np.random.choice(range(-4,5))/180*pi  # [-10,10]
    camera.rotation_euler[1] = np.random.choice(range(-4,5))/180*pi
    camera.rotation_euler[2] = np.random.choice(range(-180,180))/180*pi
    camera.location[0] = 0.0 + 0.08*random.uniform(-1.0, 1.0) 
    camera.location[1] = 0.0 + 0.08*random.uniform(-1.0, 1.0) 
    camera.location[2] = 1.0 + 0.1*random.uniform(-1.0, 1.5)   
    camera_paras = [camera.location[0], camera.location[1],
                    camera.location[2], camera.rotation_euler[0],  
                    camera.rotation_euler[1], camera.rotation_euler[2]
                    ]
    # Rigid body simulation
    bpy.ops.object.select_all( action='DESELECT' )
    bpy.ops.rigidbody.world_remove()
    #bpy.ops.rigidbody.world_add()

    bpy.ops.object.select_all( action='DESELECT' )
    plane = bpy.data.objects["Plane"]
    plane.select_set(True) #bpy.data.objects["Plane"].select_set(True)
    bpy.context.view_layer.objects.active = plane
    bpy.ops.rigidbody.object_add(type='PASSIVE')
    plane.rigid_body.type = 'PASSIVE'
    plane.rigid_body.friction = 0.6
    plane.rigid_body.restitution = 0.0
    bpy.ops.object.select_all( action='DESELECT' )

    plane1 = bpy.data.objects["Plane1"]
    plane1.select_set(True) #bpy.data.objects["Plane"].select_set(True)
    bpy.context.view_layer.objects.active = plane1
    bpy.ops.rigidbody.object_add(type='PASSIVE')
    bpy.ops.rigidbody.shape_change(type='MESH')
    plane1.rigid_body.type = 'PASSIVE'
    plane1.rigid_body.friction = 0.3
    plane1.rigid_body.restitution = 0.2    
    plane1.rigid_body.collision_margin = 0.0
    bpy.ops.object.select_all( action='DESELECT' )

    box = bpy.data.objects["box"]
    box.select_set(True) #bpy.data.objects["Plane"].select_set(True)
    bpy.context.view_layer.objects.active = box
    bpy.ops.rigidbody.object_add(type='PASSIVE')
    bpy.ops.rigidbody.shape_change(type='MESH')
    box.rigid_body.type = 'PASSIVE'
    box.rigid_body.friction = 0.3
    box.rigid_body.restitution = 0.2    
    box.rigid_body.collision_margin = 0.0
    bpy.ops.object.select_all( action='DESELECT' )    

    #Create Particle system 
    cube = bpy.data.objects["Cube"]
    bpy.context.view_layer.objects.active = cube
    #bpy.ops.object.particle_system_add()
    if len(cube.particle_systems) == 0:
        cube.modifiers.new("part1", type='PARTICLE_SYSTEM')  # PipeI
 
    ## Setting PipeI particle system
    part1 = cube.particle_systems[0]  
    ### setting
    settings = part1.settings
    num_I = np.random.choice(range(5,25))
    part1.settings.count = num_I
    part1.settings.frame_end = 1
    part1.settings.lifetime = 250
    part1.settings.emit_from = 'VOLUME'
    part1.settings.distribution = 'RAND' 
    part1.settings.use_even_distribution = True
    part1.settings.use_rotations = True 
    part1.settings.rotation_factor_random = random.random()
    part1.settings.physics_type = 'NEWTON'
    part1.settings.render_type = 'OBJECT'
    part1.settings.particle_size = 1.0
    part1.settings.instance_object = bpy.data.objects["PipeI"]
    part1.settings.normal_factor = 0
    part1.settings.phase_factor = random.random()
    part1.settings.phase_factor_random = random.random()
    part1.settings.use_dynamic_rotation = True
    
 
    ## Generate particle system
    bpy.data.objects["Cube"].select_set(True)
    bpy.context.view_layer.objects.active = cube
    bpy.ops.object.duplicates_make_real()   # PipeI
    bpy.ops.object.select_all( action='DESELECT' )
    bpy.data.objects["Cube"].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects["Cube"]
    bpy.ops.object.particle_system_remove() # PipeI
    
    bpy.ops.object.select_all( action='DESELECT' ) 
    bpy.ops.object.select_pattern(pattern="Pipe?.*")
    bpy.ops.object.move_to_collection( collection_index=0, is_new=True, new_collection_name='Pipesystem' ) # new collection
    bpy.ops.object.select_all( action='DESELECT' )

    for obj in bpy.data.collections['Pipesystem'].all_objects:
        obj.select_set(True) 
        bpy.context.view_layer.objects.active = obj
        bpy.ops.rigidbody.object_add(type='ACTIVE')
    #bpy.ops.rigidbody.objects_add(type='ACTIVE')
    for obj in bpy.data.collections['Pipesystem'].all_objects:    #bpy.data.collections['Pipesystem']
        obj.rigid_body.type = 'ACTIVE'
        obj.rigid_body.friction = 0.8    
        obj.rigid_body.mass = 1.0
        obj.rigid_body.linear_damping = 0.4
        obj.rigid_body.angular_damping = 0.3   
    #bpy.ops.rigidbody.objects_add(type='ACTIVE')
    bpy.ops.object.select_all( action='DESELECT' )
    bpy.ops.nla.bake(frame_start=1, frame_end=150, bake_types={'OBJECT'})
    bpy.ops.screen.animation_play()
    bpy.ops.screen.animation_cancel(restore_frame=True)
    bpy.context.scene.frame_set(120)
    bpy.ops.object.select_all( action='DESELECT' )
        
    # Prepare background for plane
    bg = np.random.choice(os.listdir('/home/nhan/bg'))
    image = bpy.data.images.load('/home/nhan/bg/' + bg)
    bpy.data.materials['bg'].node_tree.nodes['Image Texture'].image = image
    
    # Prepare background for box
    box_bg = np.random.choice(os.listdir('/home/nhan/paper'))
    image_box = bpy.data.images.load('/home/nhan/paper/' + box_bg)
    bpy.data.materials['box'].node_tree.nodes['Image Texture'].image = image_box
    
    # Texture for Pipe 
    texture_dir = np.random.choice(os.listdir('/home/nhan/pvctexture'))
    texture = bpy.data.images.load('/home/nhan/pvctexture/' + texture_dir)
    bpy.data.materials['piperdk'].node_tree.nodes['Image Texture'].image = texture
    
    # Create Pass Index
    list_objects = []  # record order of objects 
    bpy.ops.object.select_all(action='DESELECT') # Deselect all objects
    for obj1 in bpy.data.collections['Pipesystem'].all_objects:
        obj1.select_set(True)
    start_index = 1
    for obj2 in bpy.context.selected_objects:
        if obj2.name.startswith("PipeI"):
            list_objects.append("PipeI")
          
        obj2.pass_index = start_index
        start_index +=1
    bpy.ops.object.select_all(action='DESELECT') # Deselect all objects

    #Compositing Mode - Create Mask
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    links = tree.links

    ## clear default nodes
    for node in tree.nodes:
        tree.nodes.remove(node)
    render_layer = tree.nodes.new(type='CompositorNodeRLayers')
    render_layer.location = 0,0
    output_file = tree.nodes.new(type='CompositorNodeOutputFile')
    output_file.location = 800,0
    output_file.base_path = '/home/nhan/longpipe_dataset'
    output_file.file_slots.remove(output_file.inputs[0])
    output_file.file_slots.new("Image_" + str(img_id))
    name_mask = "Image_" + str(img_id) + "_mask"
    output_file.file_slots.new(name_mask)
    output_file.file_slots[name_mask].format.color_mode = 'BW'
    links.new(render_layer.outputs[0], output_file.inputs[0])
    
    mul_nodes = []
    for i in range(len(bpy.data.collections['Pipesystem'].all_objects)):
        mask = tree.nodes.new(type='CompositorNodeIDMask')
        mask.location = 250,-80*(i+1)
        mask.index = i+1
        mul_node = tree.nodes.new(type='CompositorNodeMath')
        mul_node.location = 450,-80*(i+1)
        mul_node.operation = 'MULTIPLY'
        mul_node.inputs[1].default_value = (i+1)/255 
        mul_nodes.append(mul_node)
        links.new(render_layer.outputs[3], mask.inputs[0])
        links.new(mask.outputs[0], mul_node.inputs[0])
    
    add_nodes = []        
    for i in range(len(bpy.data.collections['Pipesystem'].all_objects)-1):
        add_node = tree.nodes.new(type='CompositorNodeMath')
        add_node.location = 650,-100*(i+1)
        add_node.operation = 'ADD'
        add_nodes.append(add_node)
    for i in range(len(bpy.data.collections['Pipesystem'].all_objects)-1):
        if i == 0:
            links.new(mul_nodes[0].outputs[0], add_nodes[i].inputs[0])
            links.new(mul_nodes[1].outputs[0], add_nodes[i].inputs[1])
        else:
            links.new(add_nodes[i-1].outputs[0], add_nodes[i].inputs[0])
            links.new(mul_nodes[i+1].outputs[0], add_nodes[i].inputs[1])
    links.new(add_nodes[-1].outputs[0], output_file.inputs[1])

    annotation_one_image = {"filename": "Image_" + str(img_id) + ".png",
                            "maskimage": "Image_" + str(img_id) + "_mask.png",          
                            "num_objects": len(bpy.data.collections['Pipesystem'].all_objects),
                            "num_masks": len(bpy.data.collections['Pipesystem'].all_objects),
                            "objects": list_objects,
                            "camera": camera_paras, 
                            "light": light_paras,
                            }
    annotation[img_id] = annotation_one_image 
    with open('/home/nhan/longpipe_annotation.json', 'w') as file:
        json.dump(annotation, file)
    

    # Render
    bpy.ops.render.render(write_still = True)

    collection = bpy.data.collections.get('Pipesystem')
    bpy.data.collections.remove(collection)
end = time.time()


with open('/home/nhan/longpipe_annotation.json', 'r') as file:
    annotation = json.load(file)
annotation["time"].append(end - start)
annotation["num_images"].append(end_image - start_image)

with open('/home/nhan/longpipe_annotation.json', 'w') as file:
    json.dump(annotation, file)



