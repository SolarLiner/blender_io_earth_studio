import math
import mathutils


def correct_ges_rotation(rot: mathutils.Vector):
    rot.x += math.pi
    rot.y *= -1
    rot.z *= -1
