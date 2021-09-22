import bpy

bl_info = {
    "name": "maya_delete",
    "description": "delete components like maya",
    "author": "Michitaka Inoue",
    "version": (0, 1, 2),
    "blender": (2, 80, 0),
    "warning": "",
    "wiki_url": "",
    "category": ""
    }


class MIU_OT_maya_delete(bpy.types.Operator):
    bl_idname = "object.miu_ot_maya_delete"
    bl_label = "Group"
    bl_options = {'UNDO'}

    def execute(self, context):

        object_mode = bpy.context.active_object.mode
        active_object = bpy.context.active_object.type

        if active_object == 'MESH':
            if object_mode == 'EDIT':
                edit_mode = tuple(bpy.context.tool_settings.mesh_select_mode)
                if edit_mode[0] is True:
                    # vertex
                    bpy.ops.mesh.dissolve_verts()
                elif edit_mode[1] is True:
                    # edge
                    bpy.ops.mesh.dissolve_edges()
                elif edit_mode[2] is True:
                    # face
                    bpy.ops.mesh.delete(type='FACE')
        else:
            bpy.ops.object.delete(use_global=False, confirm=False)

        return {'FINISHED'}


classes = (
    MIU_OT_maya_delete,
)

addon_keymaps = []


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(
        name='Mesh', space_type='EMPTY')
    kmi = km.keymap_items.new(MIU_OT_maya_delete.bl_idname, 'X', 'PRESS')
    addon_keymaps.append((km, kmi))


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    km = kc.keymaps['Mesh']

    for km, kmi, in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()


if __name__ == "__main__":
    register()
