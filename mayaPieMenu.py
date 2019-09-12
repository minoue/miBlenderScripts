import bpy
from bpy.types import Menu


bl_info = {
    "name": "MayaPieMenu",
    "description": "View Modes",
    "author": "Michitaka Inoue",
    "version": (0, 2, 1),
    "blender": (2, 80, 0),
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


class MPM_OT_localView(bpy.types.Operator):
    bl_idname = "object.mpm_ot_localview"
    bl_label = "Local View"

    def execute(self, context):
        bpy.ops.view3d.localview()
        return {'FINISHED'}


class VIEW3D_MT_maya_pie_menu(Menu):
    bl_label = "View"
    bl_idname = "VIEW3D_MT_maya_pie_menu"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()

        mode = getMode()

        # 9:00
        pie.operator("object.mpm_ot_vertex_mode")

        # 3:00
        if mode == "OBJECT":
            pie.operator(
                "wm.call_menu",
                text="Object Context Menu").name = "VIEW3D_MT_object_context_menu"
        elif mode == "EDGE":
            pie.operator(
                "wm.call_menu",
                text="Edge Context Menu").name = "VIEW3D_MT_edit_mesh_context_menu"
        elif mode == "FACE":
            pie.operator(
                "wm.call_menu",
                text="Face Context Menu").name = "VIEW3D_MT_edit_mesh_context_menu"
        else:
            pie.operator(
                "wm.call_menu",
                text="Vertex Context Menu").name = "VIEW3D_MT_edit_mesh_context_menu"

        # 6:00
        pie.operator("object.mpm_ot_face_mode")

        # 12:00
        pie.operator("object.mpm_ot_edge_mode")

        # 10:30
        pie.column()

        # 1:30
        pie.operator("object.mpm_ot_object_mode")

        # 7:30
        # pie.operator("object.mpm_ot_higher_subdiv")
        pie.column()

        # 4:30
        # pie.operator("object.mpm_ot_lower_subdiv")
        pie.column()

        pie.separator()
        pie.separator()

        # Bottom submenus
        bottom = pie.split().row()

        left_box1 = bottom.column()
        left_box1.separator()
        left_box1.separator()
        left_box1.separator()
        left_box1.separator()
        left_box1.separator()
        left_box1.separator()
        sub_menu1 = left_box1.box()
        sub_menu1.operator("object.mpm_ot_dummy_command", text="cmd")
        sub_menu1.operator("object.mpm_ot_dummy_command", text="cmd")
        sub_menu1.operator("object.mpm_ot_dummy_command", text="cmd")
        sub_menu1.operator("object.mpm_ot_dummy_command", text="cmd")

        left_box2 = bottom.column()
        left_box2.separator()
        left_box2.separator()
        left_box2.separator()
        left_box2.separator()
        left_box2.separator()
        left_box2.separator()
        sub_menu2 = left_box2.box()
        sub_menu2.operator("object.mpm_ot_dummy_command", text="cmd")
        sub_menu2.operator("object.mpm_ot_dummy_command", text="cmd")
        sub_menu2.operator("object.mpm_ot_dummy_command", text="cmd")
        sub_menu2.operator("object.mpm_ot_dummy_command", text="cmd")

        overlay = bpy.context.space_data.overlay

        # Top submenus
        top = pie.column()
        top_menu = top.box().row()
        top_menu.operator("object.mpm_ot_localview", text="Isolate Selected")
        top_menu.prop(overlay, 'show_wireframes', text="Wireframe On Shaded")
        top_menu.operator("object.mpm_ot_dummy_command", text="cmd A")
        top_menu.operator("object.mpm_ot_dummy_command", text="cmd B")
        top.separator()
        top.separator()
        top.separator()
        top.separator()
        top.separator()


class VIEW3D_MT_maya_pie_menu_shift(Menu):
    bl_label = "View"
    bl_idname = "VIEW3D_MT_maya_pie_menu_shift"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()

        # mode = getMode()

        # 9:00
        pie.operator("mesh.knife_tool", text="Knife")

        # 3:00
        pie.operator("object.mpm_ot_dummy_command", text="")

        # 6:00
        pie.operator("view3d.edit_mesh_extrude_move_normal", text="Extrude")

        # 12:00
        pie.operator("object.mpm_ot_dummy_command", text="")

        # 10:30
        pie.operator("object.mpm_ot_dummy_command", text="")

        # 1:30
        pie.operator("object.mpm_ot_dummy_command", text="")

        # 7:30
        pie.operator("object.mpm_ot_dummy_command", text="")

        # 4:30
        pie.operator("object.mpm_ot_dummy_command", text="")


classes = (
    VIEW3D_MT_maya_pie_menu,
    VIEW3D_MT_maya_pie_menu_shift,
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
    MPM_OT_localView,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
