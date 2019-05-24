from collections import namedtuple
from dataclasses import dataclass
from typing import List

import mathutils


@dataclass
class CFrame:
    fov: float
    matrix: mathutils.Matrix


@dataclass
class TPoint:
    position: mathutils.Vector
    name: str
    visible: bool


@dataclass
class ProjectKlass:
    name: str
    width: int
    height: int
    frameRate: int
    numFrames: int
    durationSeconds: float
    cameraFrames: List[CFrame]
    trackPoints: List[TPoint]
