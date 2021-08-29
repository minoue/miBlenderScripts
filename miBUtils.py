import bpy

bl_info = {
    "name": "mi_blender_utils",
    "description": "small utilies",
    "author": "Michitaka Inoue",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "warning": "",
    "wiki_url": "",
    "category": ""
    }


class MIU_OT_maya_group(bpy.types.Operator):
    bl_idname = "object.miu_ot_maya_group"
    bl_label = "Group"

    def execute(self, context):

        sel = bpy.context.selected_objects

        if sel:
            bpy.ops.object.empty_add(type='PLAIN_AXES')
            loc = bpy.context.selected_objects[0]
            parents = set([i.parent for i in sel])
            parent = sel[0].parent

            for i in sel:
                i.parent = loc
                i.matrix_parent_inverse = loc.matrix_world.inverted()

            if len(parents) == 1:
                loc.parent = list(parents)[0]

        return {'FINISHED'}


class MIU_OT_higher_subdiv(bpy.types.Operator):
    bl_idname = "object.miu_ot_higher_subdiv"
    bl_label = "Subdiv+"

    def execute(self, context):
        sel = bpy.context.selected_objects
        for i in sel:

            # Set active object
            bpy.context.view_layer.objects.active = i

            mods = [m.type for m in i.modifiers]
            if 'SUBSURF' in mods:
                # If subsurf modifier exists, add +1
                currentLevel = i.modifiers['Subdivision'].levels
                newLevel = currentLevel + 1
                i.modifiers['Subdivision'].levels = newLevel
            else:
                # otherwise, add new subsurf modifier
                bpy.ops.object.modifier_add(type='SUBSURF')

        return {'FINISHED'}


class MIU_OT_lower_subdiv(bpy.types.Operator):
    bl_idname = "object.miu_ot_lower_subdiv"
    bl_label = "Subdiv-"

    def execute(self, context):
        sel = bpy.context.selected_objects
        for i in sel:
            mods = [m.type for m in i.modifiers]
            bpy.context.view_layer.objects.active = i
            if 'SUBSURF' in mods:
                currentLevel = i.modifiers['Subdivision'].levels
                newLevel = currentLevel - 1
                i.modifiers['Subdivision'].levels = newLevel
            else:
                bpy.ops.object.modifier_add(type='SUBSURF')

        return {'FINISHED'}


classes = (
    MIU_OT_maya_group,
    MIU_OT_higher_subdiv,
    MIU_OT_lower_subdiv
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
