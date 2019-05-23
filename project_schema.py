from collections import namedtuple
from typing import List

from marshmallow import Schema, fields, post_load

VectorTuple = namedtuple("Vector", ['x', 'y', 'z'])
CFrameTuple = namedtuple("CameraFrame",
                         ['position', 'rotation', 'fovVertical'])
TPointTuple = namedtuple("TrackPoint", ['position', 'name', 'visible'])
ProjectTuple = namedtuple("Project", [
    'name', 'width', 'height', 'frameRate', 'numFrames', 'durationSeconds',
    'cameraFrames', 'trackPoints'
])


class Vector(Schema):
    x = fields.Float()
    y = fields.Float()
    z = fields.Float()

    @post_load
    def make_object(self, data):
        return VectorTuple(**data)


class CameraFrame(Schema):
    position = fields.Nested(Vector)
    rotation = fields.Nested(Vector)
    fovVertical = fields.Integer()

    @post_load
    def make_object(self, data):
        return CFrameTuple(**data)


class TrackPoint(Schema):
    position = fields.Nested(Vector)
    name = fields.Str()
    visible = fields.Bool()

    @post_load
    def make_object(self, data):
        return TPointTuple(**data)


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
        return ProjectTuple(**data)
