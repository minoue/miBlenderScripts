# https://blender.stackexchange.com/questions/9200/how-to-make-object-a-a-parent-of-object-b-via-blenders-python-api

import bpy

bl_info = {
    "name": "maya_group",
    "description": "group objects like maya",
    "author": "Michitaka Inoue",
    "version": (0, 1, 2),
    "blender": (2, 80, 0),
    "warning": "",
    "wiki_url": "",
    "category": ""
    }


class MIU_OT_maya_group(bpy.types.Operator):
    bl_idname = "object.miu_ot_maya_group"
    bl_label = "Group"
    bl_options = {'UNDO'}

    def execute(self, context):

        sel = bpy.context.selected_objects

        if sel:
            # Craete new empty
            bpy.ops.object.empty_add(type='PLAIN_AXES')
            empty = bpy.context.selected_objects[0]
            
            # 
            parents = set([i.parent for i in sel])

            bpy.context.view_layer.objects.active = empty

            # Parent selected objects to the newly crated empty plain axis
            for i in sel:
                i.select_set(True)
                bpy.ops.object.parent_set(keep_transform=True)

            # If selected objects are located in a same hierarchy, parent the empty axis back 
            # to the original parent
            if len(parents) == 1:
                grandparent = list(parents)[0]
                if grandparent is not None:
                    empty.parent = grandparent
                    empty.matrix_parent_inverse = grandparent.matrix_world.inverted()
                
        return {'FINISHED'}


classes = (
    MIU_OT_maya_group,
)

addon_keymaps = []


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type = 'EMPTY')
    kmi = km.keymap_items.new(MIU_OT_maya_group.bl_idname, 'G', 'PRESS', ctrl=True)
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
