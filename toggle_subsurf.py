import bpy

bl_info = {
    "name": "toggle_subsurf",
    "description": "toggle and control subsurf modifier",
    "author": "Michitaka Inoue",
    "version": (0, 2, 0),
    "blender": (3, 2, 1),
    "warning": "",
    "wiki_url": "",
    "category": ""
    }


class MIU_OT_higher_subdiv(bpy.types.Operator):
    bl_idname = "object.miu_ot_higher_subdiv"
    bl_label = "Subdiv+"
    bl_options = {'UNDO'}

    def execute(self, context):
        sel = bpy.context.selected_objects
        for i in sel:

            # Set active object
            bpy.context.view_layer.objects.active = i

            mods = [m for m in i.modifiers]
            found = False
            for mod in mods:
                if mod.type == 'SUBSURF':
                    mod.levels = mod.levels + 1
                    found = True
                    break

            if not found:
                bpy.ops.object.modifier_add(type='SUBSURF')

        return {'FINISHED'}


class MIU_OT_lower_subdiv(bpy.types.Operator):
    bl_idname = "object.miu_ot_lower_subdiv"
    bl_label = "Subdiv-"
    bl_options = {'UNDO'}

    def execute(self, context):
        sel = bpy.context.selected_objects
        for i in sel:

            bpy.context.view_layer.objects.active = i
            mods = [m for m in i.modifiers]

            for mod in mods:
                if mod.type == 'SUBSURF':
                    mod.levels = mod.levels - 1
                    break

        return {'FINISHED'}


classes = (
    MIU_OT_higher_subdiv,
    MIU_OT_lower_subdiv
)

addon_keymaps = []


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type = 'EMPTY')
    kmi = km.keymap_items.new(MIU_OT_higher_subdiv.bl_idname, 'NUMPAD_PLUS', 'PRESS')
    kmi2 = km.keymap_items.new(MIU_OT_lower_subdiv.bl_idname, 'NUMPAD_MINUS', 'PRESS')

    addon_keymaps.append((km, kmi))
    addon_keymaps.append((km, kmi2))


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
