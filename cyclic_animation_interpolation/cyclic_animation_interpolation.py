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
    "name": "Cyclic animation interpolation",
    "description": "Interpolates the entire animation cycle taking the extremes into account",
    "author": "aravergar",
    "email": "aravergar@gmail.com",
    "version": (1, 0),
    "blender": (2, 76, 0),
    "location": "Key > Interpolate Cycle",
    "warning": "",
    "category": "Add Curve"
}

import bpy

def selectedfcurves(obj):
    """Select fcurves from active object

    Args:
        obj (Object): Active object from the context

    Returns:
        fcurves_sel (Collection): Collection of selected fcurves
    """
    fcurves_sel = []
    for i, fc in enumerate(obj.animation_data.action.fcurves):
        if fc.select:
            fcurves_sel.append(fc)
    return fcurves_sel

def main(context):
    """Interpolates the fcurves around the first and last keyframes

    Args:
        context (Context): Context of the application
    """
    obj = context.active_object
    fcurves = selectedfcurves(obj)
    for fcurve in fcurves:
        # Extraction of the keyframes of the fcurve
        keyframes = fcurve.keyframe_points.values()
        key_left = keyframes[1]
        key_first = keyframes[0]
        key_right = keyframes[-2]
        key_last = keyframes[-1]
        left_co = key_first.co[0]-(key_last.co[0]-key_right.co[0])
        right_co = key_last.co[0]+(key_first.co[0]+key_left.co[0])
        # Insertion of the next-to-last and second keyframes before and after the active range
        fcurve.keyframe_points.insert(left_co, key_right.co[1])
        fcurve.keyframe_points.insert(right_co, key_left.co[1])
        fcurve.update()
        keyframes = fcurve.keyframe_points.values()
        # Removal of the aforementioned keyframes. Fast removal enabled, so the interpolation remains.
        right = keyframes[-1]
        fcurve.keyframe_points.remove(right, True)
        left = keyframes[0]
        fcurve.keyframe_points.remove(left, True)

class GRAPH_OT_interpolate(bpy.types.Operator):
    bl_idname = "graph.interpolate_cyclic_animation"
    bl_label = "Interpolate Cyclic Animation"

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
