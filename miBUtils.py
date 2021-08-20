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

            if len(parents) == 1:
                loc.parent = list(parents)[0]

        return {'FINISHED'}


classes = (
    MIU_OT_maya_group,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
