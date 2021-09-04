# https://blender.stackexchange.com/questions/9200/how-to-make-object-a-a-parent-of-object-b-via-blenders-python-api

import bpy

bl_info = {
    "name": "mi_blender_utils",
    "description": "small utilies",
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


class MIU_OT_higher_subdiv(bpy.types.Operator):
    bl_idname = "object.miu_ot_higher_subdiv"
    bl_label = "Subdiv+"
    bl_options = {'UNDO'}

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
    bl_options = {'UNDO'}

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
