from enum import Enum
from collections import namedtuple
import math

class ConeTypes(Enum):
    blue = 0
    yellow = 1
    orange = 2

Cone = namedtuple('Cone', 'x y type')

Point = namedtuple('Point', 'x y')

RefPoint = namedtuple('RefPoint', 'x y vel')

Controls = namedtuple('Controls', 'steering throttle')


def transform_vector(pt, x, y, angle):
    return (x + math.cos(angle)*pt[0] - math.sin(angle)*pt[1], y + math.sin(angle)*pt[0] + math.cos(angle)*pt[1])

class CarState():
    """ Struct to contain state params
    """
    def __init__(self):
        self.x_pos = 0.0
        self.y_pos = 0.0
        self.velocity = 0.0
        self.accel = 0.0
        self.yaw = 0.0

def norm(pt1, pt2):
    return math.sqrt((pt1.x - pt2.x)**2 + (pt1.y - pt2.y)**2)

def load_track_cones(csv_path):
    track = []
    with open(csv_path, 'r') as track_file:
        for line in track_file.readlines():
            x, y, typ = line.strip().split(",")
            track.append(Cone(float(x), float(y), int(typ)))
    return track

def clamp(x, min_x, max_x):
    return min(max(x, min_x), max_x)

def wrap_angle(angle_in):
    if angle_in > math.pi:
        angle_in -= 2*math.pi
    elif angle_in < -math.pi:
        angle_in += 2*math.pi
    return angle_in