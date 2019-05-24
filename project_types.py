from collections import namedtuple

VectorTuple = namedtuple("Vector", ['x', 'y', 'z'])
CFrameTuple = namedtuple("CameraFrame",
                         ['position', 'rotation', 'fovVertical'])
TPointTuple = namedtuple("TrackPoint", ['position', 'name', 'visible'])
ProjectTuple = namedtuple("Project", [
    'name', 'width', 'height', 'frameRate', 'numFrames', 'durationSeconds',
    'cameraFrames', 'trackPoints'
])
