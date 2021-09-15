# https://blenderartists.org/t/move-parent-origin-only/1281091

import bpy
from mathutils import Vector

bl_info = {
    "name": "maya_group_centerPivot",
    "description": "center pivot for empty groups",
    "author": "Michitaka Inoue",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "warning": "",
    "wiki_url": "",
    "category": ""
    }


class MIU_OT_maya_group_centerPivot(bpy.types.Operator):
    bl_idname = "object.miu_ot_maya_center_pivot"
    bl_label = "Center Group"
    bl_options = {'UNDO'}

    def execute(self, context):

        def getAllDecendents(obj, result):
            if not obj.children:
                # if no children
                result.append(obj)

            for child in obj.children:
                result.append(child)
                for c in child.children:
                    getAllDecendents(c, result)

        ts = bpy.context.scene.tool_settings
        og_settings = (
            ts.use_transform_skip_children, ts.use_transform_data_origin)

        sel = bpy.context.selected_objects

        if not sel:
            return {'FINISHED'}

        for i in sel:
            if i.type == 'EMPTY':

                result = []
                getAllDecendents(i, result)

                meshes = [mesh for mesh in result if mesh.type == 'MESH']

                x = []
                y = []
                z = []

                for m in meshes:
                    bb_verts = [Vector(v) for v in m.bound_box]
                    M = m.matrix_world
                    bb_world_verts = [M @ v for v in bb_verts]

                    for v in bb_world_verts:
                        x.append(v.x)
                        y.append(v.y)
                        z.append(v.z)

                x_max = max(x)
                x_min = min(x)
                y_max = max(y)
                y_min = min(y)
                z_max = max(z)
                z_min = min(z)

                x_mid = (x_max + x_min) / 2
                y_mid = (y_max + y_min) / 2
                z_mid = (z_max + z_min) / 2

                pivot = Vector((x_mid, y_mid, z_mid))

                # Change value to move parents
                ts.use_transform_skip_children = True
                # ts.use_transform_data_origin = True

                current_location_world = sel[0].matrix_world.translation

                displacement = pivot - current_location_world

                bpy.ops.transform.translate(value=displacement)

        # revert to original values after execution is done
        ts.use_transform_skip_children = og_settings[0]
        ts.use_transform_data_origin = og_settings[1]

        return {'FINISHED'}


classes = (
    MIU_OT_maya_group_centerPivot,
)

addon_keymaps = []


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(
        name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new(
        MIU_OT_maya_group_centerPivot.bl_idname,
        'C',
        'PRESS',
        ctrl=True,
        shift=True)
    addon_keymaps.append((km, kmi))


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    km = kc.keymaps['Object Mode']

    for km, kmi, in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()


if __name__ == "__main__":
    register()
