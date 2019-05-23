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
from pathlib import Path

import bpy
import bpy.types
from bpy.types import Operator
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper


def load_gse_exported_project(path: str):
    from .project_schema import Project
    with open(path, 'r') as f:
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
    "category": "Import-Export"
}


class OperatorImportGES(Operator, ImportHelper):
    bl_idname = "import_scene.ges"
    bl_label = "Import Google Earth Studio scene"
    bl_options = {'PRESET', 'UNDO'}

    filename: StringProperty(
        name="File name",
        description="JSON export to load into Blender",
        subtype='FILE_PATH')
    filter_glob: StringProperty(default="*.json;*.txt", options={'HIDDEN'})

    def execute(self, ctx: bpy.types.Context):
        data = self.as_keywords()
        filepath = data.get("filepath")
        export = load_gse_exported_project(filepath)
        self.import_project(ctx, export.data)
        return {'FINISHED'}

    def import_project(self, ctx: bpy.types.Context,
                       data: 'project_schema.ProjectTuple'):
        scn: bpy.types.Scene = ctx.scene
        render: bpy.types.RenderSettings = scn.render
        scn.frame_start = 0
        scn.frame_end = data.numFrames
        render.fps = data.frameRate
        render.resolution_x = data.width
        render.resolution_y = data.height


def menu_func_import(self, context: bpy.types.Context):
    self.layout.operator(
        OperatorImportGES.bl_idname, text="Google Earth Studio (.json)")


def register():
    try:
        import pip
        import os
        import subprocess
        import sys
        blender_exe = Path(sys.executable).resolve().absolute()
        pip_exe = Path(blender_exe / "../2.80/python/bin/pip").resolve()
        requirements_file = Path(__file__) / "../requirements.txt"
        subprocess.call([
            str(pip_exe.resolve()), "install", "-r",
            str(requirements_file.resolve())
        ])
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
