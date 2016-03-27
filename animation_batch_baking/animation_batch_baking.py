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
    "version": (1, 0),
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
    
    # Groups actions under the same animation name in a defaultdict
    for act in actions:
        anim = act.name.split("-")[0]
        d[anim].append(act)
        actions.remove(act)
        for a in actions[:]:
            if a.name.split("-")[0] == anim:
                d[anim].append(a)
                actions.remove(a)
    
    names = []
    for name in d: # Recorre las animaciones
        num = len(d[name])
        for i in range(num): # Recorre las acciones de cada animación para añadirlas a la pila NLA
            obj.animation_data.action = d[name][i]
            actName = obj.animation_data.action.name
            obj.animation_data.action.name += "_OLD"
            
            bpy.ops.nla.actionclip_add(action = obj.animation_data.action.name) # Add the actions of the same animation to the NLA stack
            bpy.ops.nla.action_unlink()
        
        for i in range(num): # Recorre las acciones de cada animación para bakear sus curvas
            for fc in d[name][i].fcurves: # Iterate the action fcurves for bone selecting
                b = fc.data_path.split("\"")[1]
                obj.pose.bones.get(b).bone.select = True
            
            actName = d[name][i].name
            actName = actName[:-4]
            print("voy a bakear "+actName)
            
            mark_actions()
            
            
            # Bake
            bpy.ops.nla.bake(frame_start = context.scene.frame_start, frame_end = context.scene.frame_end, visual_keying = True)
            
            # Lower level bake call
            #~ bpy_extras.anim_utils.bake_action(context.scene.frame_start,
                                    #~ context.scene.frame_end,
                                    #~ frame_step=1,
                                    #~ only_selected=True,
                                    #~ do_object='POSE',
                                    #~ do_visual_keying=True,
                                    #~ do_constraint_clear=False,
                                    #~ do_parents_clear=False,
                                    #~ do_clean=True,
                                    #~ action = bpy.data.actions[actName]
                                    #~ )
            
            # Naming of baked action
            action = get_unmarked_action()
            if action is not None:
                print ("Se supone que hay alguna accion sin tagear.")
                action.name = actName
                action.use_fake_user = True
            
            for fc in d[name][i].fcurves: # Iterate action fcurves for bone deselecting
                b = fc.data_path.split("\"")[1]
                obj.pose.bones.get(b).bone.select = False
            bpy.ops.nla.action_unlink(True)

        bpy.ops.nla.delete()
        for i in range(num):
            bpy.data.actions[d[name][i].name].use_fake_user = False
            bpy.data.actions[d[name][i].name].user_clear
            bpy.ops.nla.action_unlink(True)
            
            bpy.data.actions.remove(action = d[name][i])
        bpy.ops.nla.tracks_delete()

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

