import math, extramath, vector
from enum import Enum

class vectortype(Enum):
    XY = 'XY'
    RTHETA = 'RTHETA'


class Vector(object):
    
    def __init__(self, coords, mode):
        if mode == vectortype.RTHETA:
            self.r = coords[0]
            self.theta = coords[1]
            self.x = self.r * math.cos(math.radians(self.theta))
            self.y = self.r * math.sin(math.radians(self.theta))
        else:
            self.x = coords[0]
            self.y = coords[1]
            self.r = extramath.dist([0,0], [self.x, self.y])
            self.theta = math.atan2(self.y, self.x)
    
    def __mul__(self, scalar):
        return vector.Vector((self.x * scalar, self.y * scalar), vectortype.XY)
    
    def __add__(self, othervector):
        return vector.Vector((self.x + othervector.x, self.y + othervector.y), vectortype.XY)