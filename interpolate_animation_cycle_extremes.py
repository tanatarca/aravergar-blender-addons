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
    "name": "Interpolate animation cycle extremes",
    "description": "Interpolates the entire animation cycle taking the extremes into account",
    "author": "aravergar",
    "version": (0, 1),
    "blender": (2, 76, 0),
    "location": "Key > Interpolate Cycle",
    "warning": "",
    "category": "Add Curve"
}

import bpy
#from bpy.props import *

def selectedfcurves(obj):
    fcurves_sel = []
    for i, fc in enumerate(obj.animation_data.action.fcurves):
        if fc.select:
            fcurves_sel.append(fc)
    return fcurves_sel

def main(context):
    obj = context.active_object
    fcurves = selectedfcurves(obj)
    for fcurve in fcurves:
        keyframes = fcurve.keyframe_points.values()
        key_left = keyframes[1]
        key_first = keyframes[0]
        key_right = keyframes[-2]
        key_last = keyframes[-1]
        left_co = key_first.co[0]-(key_last.co[0]-key_right.co[0])
        right_co = key_last.co[0]+(key_first.co[0]+key_left.co[0])
        fcurve.keyframe_points.insert(left_co, key_right.co[1])
        fcurve.keyframe_points.insert(right_co, key_left.co[1])
        keyframes = fcurve.keyframe_points.values()
        left = keyframes[0]
        right = keyframes[-1]
        #left = fcurve.keyframe_points.get(left_co)
        #right = fcurve.keyframe_points.get(right_co)
        fcurve.keyframe_points.remove(left, True)
        fcurve.keyframe_points.remove(right, True)

class GRAPH_OT_interpolate(bpy.types.Operator):
    bl_idname = "graph.interpolate_animation_cycle_extremes"
    bl_label = "Interpolate Animation Cycle Extremes"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}

def menu_func(self, context):
 	self.layout.operator(GRAPH_OT_interpolate.bl_idname)
    #self.layout.operator("Interpolate Animation Cycle Extremes")

#################################################
#### REGISTER ###################################
#################################################
def register():
    bpy.utils.register_module(__name__)

    bpy.types.GRAPH_MT_channel.append(menu_func)

def unregister():
    bpy.types.GRAPH_MT_channel.remove(menu_func)

    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
