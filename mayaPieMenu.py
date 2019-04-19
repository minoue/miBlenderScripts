import bpy
from bpy.types import Menu

bl_info = {
    "name": "MayaPieMenu",
    "description": "View Modes",
    "author": "Michitaka Inoue",
    "version": (0, 1, 1),
    "blender": (2, 80, 0),
    # "location": "Right",
    "warning": "",
    "wiki_url": "",
    "category": "3d View"
    }


def getMode():
    object_mode = bpy.context.active_object.mode
    if object_mode == "OBJECT":
        return "OBJECT"
    else:
        edit_mode = tuple(bpy.context.tool_settings.mesh_select_mode)
        if edit_mode[0] is True:
            return "VERTEX"
        elif edit_mode[1] is True:
            return "EDGE"
        elif edit_mode[2] is True:
            return "FACE"


class MPM_OT_higher_subdiv(bpy.types.Operator):
    bl_idname = "object.mpm_ot_higher_subdiv"
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


class MPM_OT_lower_subdiv(bpy.types.Operator):
    bl_idname = "object.mpm_ot_lower_subdiv"
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


class MPM_OT_dummy_command(bpy.types.Operator):
    bl_idname = "object.mpm_ot_dummy_command"
    bl_label = ""

    def execute(self, context):
        return {'FINISHED'}


class MPM_OT_vertex_mode(bpy.types.Operator):
    bl_idname = "object.mpm_ot_vertex_mode"
    bl_label = "Vertex Mode"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="VERT")
        return {'FINISHED'}


class MPM_OT_edge_mode(bpy.types.Operator):
    bl_idname = "object.mpm_ot_edge_mode"
    bl_label = "Edge Mode"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="EDGE")
        return {'FINISHED'}


class MPM_OT_face_mode(bpy.types.Operator):
    bl_idname = "object.mpm_ot_face_mode"
    bl_label = "Face Mode"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="FACE")
        return {'FINISHED'}


class MPM_OT_object_mode(bpy.types.Operator):
    bl_idname = "object.mpm_ot_object_mode"
    bl_label = "Object Mode"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}


class MPM_OT_move(bpy.types.Operator):
    bl_idname = "object.mpm_ot_move"
    bl_label = ""

    def execute(self, context):
        bpy.ops.wm.tool_set_by_name(name="Move")
        return {'FINISHED'}


class MPM_OT_rotate(bpy.types.Operator):
    bl_idname = "object.mpm_ot_rotate"
    bl_label = ""

    def execute(self, context):
        bpy.ops.wm.tool_set_by_name(name="Rotate")
        return {'FINISHED'}


class MPM_OT_scale(bpy.types.Operator):
    bl_idname = "object.mpm_ot_scale"
    bl_label = ""

    def execute(self, context):
        bpy.ops.wm.tool_set_by_name(name="Scale")
        return {'FINISHED'}


class VIEW3D_MT_maya_pie_menu(Menu):
    bl_label = "View"
    bl_idname = "VIEW3D_MT_maya_pie_menu"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()

        # 9:00
        pie.operator("object.mpm_ot_vertex_mode")

        # 3:00
        mode = getMode()
        if mode == "VERTEX":
            pie.operator("wm.call_menu", text="Vertex Context Menu").name = "VIEW3D_MT_edit_mesh_vertices"
        elif mode == "EDGE":
            pie.operator("wm.call_menu",text="Edge Context Menu").name = "VIEW3D_MT_edit_mesh_edges"
        elif mode == "FACE":
            pie.operator("wm.call_menu",text="Face Context Menu").name = "VIEW3D_MT_edit_mesh_faces"
        else:
            pie.operator("wm.call_menu",text="Object Context Menu").name = "VIEW3D_MT_object_specials"

        # 6:00
        pie.operator("object.mpm_ot_face_mode")

        # 12:00
        pie.operator("object.mpm_ot_edge_mode")

        # 10:30
        pie.operator("object.mpm_ot_dummy_command", text="")

        # 1:30
        pie.operator("object.mpm_ot_object_mode")

        # 7:30
        pie.operator("object.mpm_ot_higher_subdiv")

        # 4:30
        pie.operator("object.mpm_ot_lower_subdiv")


classes = (
    VIEW3D_MT_maya_pie_menu,
    MPM_OT_dummy_command,
    MPM_OT_vertex_mode,
    MPM_OT_edge_mode,
    MPM_OT_face_mode,
    MPM_OT_object_mode,
    MPM_OT_move,
    MPM_OT_rotate,
    MPM_OT_scale,
    MPM_OT_higher_subdiv,
    MPM_OT_lower_subdiv,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
