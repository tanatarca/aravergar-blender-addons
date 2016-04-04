# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Animation Batch Baking",
    "description": "Batch bakes the actions of the object, clearing all bone constraints, for compatibility with JMonkeyEngine 3",
    "author": "aravergar",
    "email": "aravergar@gmail.com",
    "version": (1, 2),
    "blender": (2, 76, 2),
    "location": "NLA Editor > Edit > Animation Batch Baking",
    "warning": "",
    "category": "Animation"
}

if "bpy" in locals():
    import imp
    if "anim_utils" in locals():
        imp.reload(anim_utils)

import bpy
import bpy_extras.anim_utils
from collections import defaultdict

def mark_actions():
    for action in bpy.data.actions:
        action.tag = True

def get_unmarked_action():
    print ("hay acciones sin tagear?")
    for action in bpy.data.actions:
        if action.tag != True:
            print("hay una accion sin tagear!!")
            return action
    print ("pos no")
    return None

def main(context):
    """Batch bakes the animations of the selected object and removes its constraints

    Args:
        context (Context): Context of the application
    """
    obj = context.active_object
    actions = list(bpy.data.actions)
    d = defaultdict(list)
    
    # Groups actions under the same animation name
    # in a defaultdict IF the name specifies this object
    if obj.name == "Person":
        person = True
    else:
        person = False
    for act in actions:
        print("Action: "+act.name+", range = "+str(act.frame_range.x)+" "+str(act.frame_range.y))
        anim = act.name # anim = [X.X]_Anim-channel_000
        print("anim = "+anim)
        if ((person == True) and (len(anim.split("_")) != 2)) or ((person == False) and (len(anim.split("_")) == 2)):
            d[anim] = act
            print(anim+" removed")

    
    names = []
    for name in d:
        obj.animation_data.action = d[name]
        actName = obj.animation_data.action.name
        obj.animation_data.action.name += "_OLD"
        
        for fc in obj.animation_data.action.fcurves:
            b = fc.data_path.split("\"")[1]
            obj.pose.bones.get(b).bone.select = True
            
        print("voy a bakear "+actName)
        mark_actions()
        
        # Bake
        bpy.ops.nla.bake(frame_start = int(d[name].frame_range.x), frame_end = int(d[name].frame_range.y), visual_keying = True)
        
        # Naming of baked action
        action = get_unmarked_action()
        if action is not None:
            print ("Se supone que hay alguna accion sin tagear.")
            action.name = actName
            action.use_fake_user = True
        
        for fc in obj.animation_data.action.fcurves: # Iterate action fcurves for bone deselecting
            b = fc.data_path.split("\"")[1]
            obj.pose.bones.get(b).bone.select = False

        bpy.data.actions[d[name].name].use_fake_user = False
        bpy.data.actions[d[name].name].user_clear

        bpy.data.actions.remove(action = d[name])

class VIEW3D_OT_bake(bpy.types.Operator):
    bl_idname = "object.animation_batch_baking"
    bl_label = "Animation Batch Baking"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}

def menu_func(self, context):
 	self.layout.operator(VIEW3D_OT_bake.bl_idname)

#################################################
#### REGISTER ###################################
#################################################
def register():
    bpy.utils.register_module(__name__)
    bpy.types.NLA_MT_edit.append(menu_func)

def unregister():
    bpy.types.NLA_MT_edit.remove(menu_func)
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

