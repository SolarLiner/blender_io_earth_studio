import math
import mathutils

from marshmallow import Schema, fields, post_load

from .project_types import CFrame, TPoint, ProjectKlass


class Vector(Schema):
    x = fields.Float()
    y = fields.Float()
    z = fields.Float()

    @post_load
    def make_object(self, data):
        x, y, z = data["x"], data["y"], data["z"]
        return mathutils.Vector((x, y, z))


class Euler(Schema):
    x = fields.Float()
    y = fields.Float()
    z = fields.Float()

    @post_load
    def make_object(self, data):
        rot = data["x"], data["y"], data["z"]
        return mathutils.Euler(map(math.radians, rot), "XYZ")


class CameraFrame(Schema):
    position = fields.Nested(Vector)
    rotation = fields.Nested(Euler)
    fovVertical = fields.Integer()

    @post_load
    def make_object(self, data):
        eul: mathutils.Euler = data["rotation"]
        corr = mathutils.Quaternion((0, 0, -1), math.radians(90))
        mat_rot: mathutils.Matrix = eul.to_matrix()  # @ corr.to_matrix()
        mat_loc: mathutils.Matrix = mathutils.Matrix.Translation(data["position"])
        return CFrame(fov=data["fovVertical"], matrix=mat_loc @ mat_rot.to_4x4())


class TrackPoint(Schema):
    position = fields.Nested(Vector)
    name = fields.Str()
    visible = fields.Bool()

    @post_load
    def make_object(self, data):
        return TPoint(**data)


class Project(Schema):
    name = fields.Str()
    width = fields.Integer()
    height = fields.Integer()
    frameRate = fields.Integer()
    numFrames = fields.Integer()
    durationSeconds = fields.Float()
    cameraFrames = fields.List(fields.Nested(CameraFrame))
    trackPoints = fields.List(fields.Nested(TrackPoint))

    @post_load
    def make_object(self, data):
        return ProjectKlass(**data)
