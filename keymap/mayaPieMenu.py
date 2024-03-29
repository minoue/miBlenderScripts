import bpy
from bpy.types import Menu


bl_info = {
    "name": "MayaPieMenu",
    "description": "View Modes",
    "author": "Michitaka Inoue",
    "version": (0, 2, 5),
    "blender": (2, 80, 0),
    "warning": "",
    "wiki_url": "",
    "category": "3d View"
    }


def getMode():
    selected_objects = bpy.context.selected_objects
    if len(selected_objects) == 0:
        return

    object_mode = bpy.context.active_object.mode
    active_object = bpy.context.active_object.type

    if object_mode == "OBJECT":
        if active_object == "MESH":
            return "OBJECT"
        elif active_object == "EMPTY":
            return "EMPTY"
        else:
            return None
    else:
        if active_object == "MESH":
            edit_mode = tuple(bpy.context.tool_settings.mesh_select_mode)
            if edit_mode[0] is True:
                return "VERTEX"
            elif edit_mode[1] is True:
                return "EDGE"
            elif edit_mode[2] is True:
                return "FACE"
        elif active_object == "CURVE":
            return "EDIT"
        elif active_object == "SURFACE":
            return "EDIT"


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


class MPM_OT_uvVertex_mode(bpy.types.Operator):
    bl_idname = "object.mpm_ot_uvvertex_mode"
    bl_label = "UV Vertex Mode"

    def execute(self, context):
        bpy.context.scene.tool_settings.uv_select_mode = 'VERTEX'
        return {'FINISHED'}


class MPM_OT_uvEdge_mode(bpy.types.Operator):
    bl_idname = "object.mpm_ot_uvedge_mode"
    bl_label = "UV Edge Mode"

    def execute(self, context):
        bpy.context.scene.tool_settings.uv_select_mode = 'EDGE'
        return {'FINISHED'}


class MPM_OT_uvFace_mode(bpy.types.Operator):
    bl_idname = "object.mpm_ot_uvface_mode"
    bl_label = "UV Face Mode"

    def execute(self, context):
        bpy.context.scene.tool_settings.uv_select_mode = 'FACE'
        return {'FINISHED'}


class MPM_OT_object_mode(bpy.types.Operator):
    bl_idname = "object.mpm_ot_object_mode"
    bl_label = "Object Mode"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}


class MPM_OT_edit_mode(bpy.types.Operator):
    bl_idname = "object.mpm_ot_edit_mode"
    bl_label = "Edit Mode"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
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

        obj = bpy.context.object

        if bpy.context.area.type == "IMAGE_EDITOR":
            self.uv_menu(pie)
        else:
            if obj.type == "MESH":
                self.mesh_menu(pie)
            elif obj.type == "CURVE":
                self.curve_menu(pie)
            elif obj.type == "SURFACE":
                self.surface_menu(pie)
            elif obj.type == "GPENCIL":
                self.gpen_menu(pie)
            else:
                self.default_menu(pie, obj.type)

    def default_menu(self, pie, typ):

        # 9:00
        pie.column()

        # 3:00
        menu_type = "{} Context Menu".format(typ)
        pie.operator("wm.call_menu", text=menu_type).name = "VIEW3D_MT_object_context_menu" 

        # 6:00
        pie.column()

        # 12:00
        pie.column()

        # 10:30
        pie.column()

        # 1:30
        pie.column()

        # 7:30
        pie.column()

        # 4:30
        pie.column()

    def mesh_menu(self, pie):

        mode = getMode()

        # 9:00
        pie.operator("object.mpm_ot_vertex_mode", icon="VERTEXSEL")

        # 3:00
        if mode == "OBJECT":
            pie.operator(
                "wm.call_menu",
                text="Object Context Menu",
                icon="CUBE").name = "VIEW3D_MT_object_context_menu"
        elif mode == "EDGE":
            pie.operator(
                "wm.call_menu",
                text="Edge Context Menu",
                icon="EDGESEL").name = "VIEW3D_MT_edit_mesh_context_menu"
        elif mode == "FACE":
            pie.operator(
                "wm.call_menu",
                text="Face Context Menu",
                icon="FACESEL").name = "VIEW3D_MT_edit_mesh_context_menu"
        else:
            pie.operator(
                "wm.call_menu",
                text="Vertex Context Menu",
                icon="VERTEXSEL").name = "VIEW3D_MT_edit_mesh_context_menu"

        # 6:00
        pie.operator("object.mpm_ot_face_mode", icon="FACESEL")

        # 12:00
        pie.operator("object.mpm_ot_edge_mode", icon="EDGESEL")

        # 10:30
        pie.column()

        # 1:30
        pie.operator("object.mpm_ot_object_mode", icon="CUBE")

        # 7:30
        pie.operator("view3d.localview")
        # pie.column()

        # 4:30
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
        sub_menu1.operator(
            "object.mpm_ot_dummy_command", text=bpy.context.area.type, icon="BLENDER")
        sub_menu1.operator(
            "object.mpm_ot_dummy_command", text="cmd", icon="BLENDER")

        left_box2 = bottom.column()
        left_box2.separator()
        left_box2.separator()
        left_box2.separator()
        left_box2.separator()
        left_box2.separator()
        left_box2.separator()
        sub_menu2 = left_box2.box()
        sub_menu2.operator(
            "object.mpm_ot_dummy_command", text="cmd", icon="BLENDER")
        sub_menu2.operator(
            "object.mpm_ot_dummy_command", text="cmd", icon="BLENDER")

        overlay = bpy.context.space_data.overlay

        # Top submenus
        top = pie.column()
        top_menu = top.box().row()
        top_menu.operator(
            "object.mpm_ot_localview",
            text="Isolate Selected",
            icon="HIDE_OFF")
        top_menu.prop(overlay, 'show_wireframes', text="Wireframe On Shaded")
        top_menu.operator(
            "object.mpm_ot_dummy_command", text="cmd A", icon="BLENDER")
        top_menu.operator(
            "object.mpm_ot_dummy_command", text="cmd B", icon="BLENDER")
        top.separator()
        top.separator()
        top.separator()
        top.separator()
        top.separator()

    def curve_menu(self, pie):

        mode = getMode()

        # 9:00
        pie.operator("object.mpm_ot_edit_mode", icon="CURVE_PATH")

        # 3:00
        if mode == "OBJECT":
            pie.operator(
                "wm.call_menu",
                text="Curve Context Menu",
                icon="CURVE_DATA").name = "VIEW3D_MT_object_context_menu"
        else:
            pie.operator(
                "wm.call_menu",
                text="Edit Curve Context Menu",
                icon="CURVE_DATA").name = "VIEW3D_MT_edit_curve_context_menu"
        # 6:00
        pie.column()

        # 12:00
        pie.column()

        # 10:30
        pie.column()

        # 1:30
        pie.operator("object.mpm_ot_object_mode", icon="OUTLINER_OB_CURVE")

        # 7:30
        pie.column()

        # 4:30
        pie.column()

    def surface_menu(self, pie):

        mode = getMode()

        # 9:00
        pie.operator("object.mpm_ot_edit_mode", icon="OUTLINER_DATA_SURFACE")

        # 3:00
        if mode == "OBJECT":
            pie.operator(
                "wm.call_menu",
                text="Surface Context Menu",
                icon="OUTLINER_OB_SURFACE").name = "VIEW3D_MT_object_context_menu"
        else:
            pie.operator(
                "wm.call_menu",
                text="Edit Surface Context Menu",
                icon="OUTLINER_OB_SURFACE").name = "VIEW3D_MT_edit_curve_context_menu"
        # 6:00
        pie.column()

        # 12:00
        pie.column()

        # 10:30
        pie.column()

        # 1:30
        pie.operator("object.mpm_ot_object_mode", icon="OUTLINER_OB_SURFACE")

        # 7:30
        pie.column()

        # 4:30
        pie.column()

    def gpen_menu(self, pie):

        mode = getMode()

        # 9:00
        pie.operator("object.mpm_ot_edit_mode", icon="CURVE_PATH")

        # 3:00
        if mode == "OBJECT":
            pie.operator(
                "wm.call_menu",
                text="GreasePencil Context Menu",
                icon="CUBE").name = "VIEW3D_MT_object_context_menu"
        else:
            pie.operator(
                "wm.call_menu",
                text="Edit GreasePencil Context Menu",
                icon="CUBE").name = "VIEW3D_MT_edit_curve_context_menu"
        # 6:00
        pie.column()

        # 12:00
        pie.column()

        # 10:30
        pie.column()

        # 1:30
        pie.operator("object.mpm_ot_object_mode", icon="CUBE")

        # 7:30
        pie.column()

        # 4:30
        pie.column()

    def uv_menu(self, pie):

        mode = getMode()

        # 9:00
        pie.operator("object.mpm_ot_uvvertex_mode", icon="VERTEXSEL")

        # 3:00
        pie.operator("wm.call_menu", text="UV Context Menu", icon="CUBE").name = "IMAGE_MT_uvs_context_menu"

        # 6:00
        pie.operator("object.mpm_ot_uvface_mode", icon="FACESEL")

        # 12:00
        pie.operator("object.mpm_ot_uvedge_mode", icon="EDGESEL")

        # 10:30
        pie.column()

        # 1:30
        pie.column()

        # 7:30
        pie.column()

        # 4:30
        pie.column()


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
    MPM_OT_uvVertex_mode,
    MPM_OT_uvEdge_mode,
    MPM_OT_uvFace_mode,
    MPM_OT_object_mode,
    MPM_OT_edit_mode,
    MPM_OT_move,
    MPM_OT_rotate,
    MPM_OT_scale,
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
