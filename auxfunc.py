"""
Auxiliary functions for config Blender scene and save render

JCA
"""
from sys import path
from os.path import join, realpath, split, abspath
import json
import bpy
from sys import argv
import re

script_path, _ = split(realpath(__file__))
path.append(script_path)

def render_save(filepath):
    """Render and save with mask"""
    

    scn = bpy.data.scenes["Scene"]

    # Setting computing device
    scn.cycles.device = 'GPU'
    prefs = bpy.context.preferences
    prefs.addons['cycles'].preferences.get_devices()
    cprefs = prefs.addons['cycles'].preferences
    print(cprefs)
    # Attempt to set GPU device types if available
    for compute_device_type in ('CUDA', 'OPENCL', 'NONE'):
        try:
            cprefs.compute_device_type = compute_device_type
            print('Device found', compute_device_type)
            break
        except TypeError:
            pass
    # Enable all CPU and GPU devices
    for device in cprefs.devices:
        if not re.match('intel', device.name, re.I):
            print('Activating', device)
            device.use = True #if conf_default['compute_device'] == 'gpu' else False
        else:
            device.use = False #if conf_default['compute_device'] == 'cpu' else False

    # Save render in the same location of .blend file
    save_path = '//'
    n = 123
    filename = join(save_path, str(n))

    bpy.context.scene.render.filepath = filename + '.png'
    # bpy.data.scenes["Scene"].node_tree.nodes['File Output'].file_slots[0].path = filepath + '_mask'
    bpy.ops.render.render(write_still=True)  # render and save

# Run this script from wrapper
render_save(argv[1])