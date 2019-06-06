# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import json
import math
import mathutils
from pathlib import Path
from typing import List, Tuple

import bpy
import bpy.types
from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper

from . import project_types, utils


def load_gse_exported_project(path: str):
    from .project_schema import Project

    with open(path, "r") as f:
        data = json.load(f)
    project = Project()
    result = project.load(data)
    print(result)
    return result


bl_info = {
    "name": "Import Google Earth Studio",
    "author": "Nathan Graule",
    "description": "Import Google Earth Studio data into Blender",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "Import",
    "warning": "This import addon is a WIP.",
    "category": "Import-Export",
}


class OperatorImportGES(Operator, ImportHelper):
    bl_idname = "import_scene.ges"
    bl_label = "Import Google Earth Studio scene"
    bl_options = {"PRESET", "UNDO"}

    filename: StringProperty(name="File name", description="JSON export to load into Blender", subtype="FILE_PATH")
    filter_glob: StringProperty(default="*.json;*.txt", options={"HIDDEN"})
    new_scene: BoolProperty(name="Create new scene", default=True, description="Create a new scene when importing data")

    def execute(self, ctx: bpy.types.Context):
        data = self.as_keywords()
        filepath = data.get("filepath")
        export = load_gse_exported_project(filepath)
        project: project_types.ProjectKlass = export.data
        if self.new_scene:
            scn = bpy.data.scenes.new(name=f"{project.name} - Google Earth Studio")
        else:
            scn = bpy.context.window.scene
        self.import_project(ctx, scn, project)
        if self.new_scene:
            bpy.context.window.scene = scn
        return {"FINISHED"}

    def import_project(self, ctx: bpy.types.Context, scn: bpy.types.Scene, data: project_types.ProjectKlass):
        render: bpy.types.RenderSettings = scn.render
        scn.frame_start = 0
        scn.frame_end = data.numFrames
        render.fps = data.frameRate
        render.resolution_x = data.width
        render.resolution_y = data.height

        self.import_camera(scn, data.cameraFrames)

        for tp in data.trackPoints:
            self.import_trackpoint(ctx, scn, tp)

    def import_trackpoint(self, ctx: bpy.types.Context, scn: bpy.types.Scene, trackpoint: project_types.TPoint):
        o: bpy.types.Object = bpy.data.objects.new(trackpoint.name, None)
        o.location = mathutils.Vector([a * b for a, b in zip(trackpoint.position, (1, 1, -1))])
        o.show_name = True
        scn.collection.objects.link(o)

    def import_camera(self, scn: bpy.types.Scene, camdata: List[project_types.CFrame]):
        cam: bpy.types.Camera = bpy.data.cameras.new("GES Camera")
        cam_o: bpy.types.Object = bpy.data.objects.new("GES Camera", cam)

        for i, frame in enumerate(camdata):  # type: Tuple[int, project_types.CFrame]
            frame_idx = i + scn.frame_start
            cam.angle = frame.fov
            cam_o.matrix_world = frame.matrix
            utils.correct_ges_rotation(cam_o.rotation_euler)

            cam_o.keyframe_insert(data_path="location", index=-1, frame=frame_idx)
            cam_o.keyframe_insert(data_path="rotation_euler", index=-1, frame=frame_idx)
            cam.keyframe_insert(data_path="lens", frame=frame_idx)

            obj: bpy.types.Object = bpy.data.objects.new(f"frame {i}", None)
            obj.matrix_world = cam_o.matrix_world
            utils.correct_ges_rotation(obj.rotation_euler)
            obj.empty_display_type = "ARROWS"
            scn.collection.objects.link(obj)
        scn.collection.objects.link(cam_o)


def menu_func_import(self, context: bpy.types.Context):
    self.layout.operator(OperatorImportGES.bl_idname, text="Google Earth Studio (.json)")


def register():
    try:
        import pip
        import os
        import subprocess
        import sys

        blender_exe = Path(sys.executable).resolve().absolute()
        pip_exe = Path(blender_exe / "../2.80/python/bin/pip").resolve()
        requirements_file = Path(__file__) / "../requirements.txt"
        subprocess.call([str(pip_exe.resolve()), "install", "-r", str(requirements_file.resolve())])
    except ImportError:
        try:
            import ensurepip

            ensurepip.bootstrap(upgrade=True, default_pip=True)
            return register()
        except ImportError:
            raise RuntimeError("Could not import pip")

    bpy.utils.register_class(OperatorImportGES)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(OperatorImportGES)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
