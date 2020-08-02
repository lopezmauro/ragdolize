
from ..math_utils import Vector

class Force(object):
    def solve(self):
        raise NotImplementedError

class ConstantForce(Force):
    def __init__(self, partciles, vector=[0,0,0], strenght=1.0):
        self._partciles = partciles
        self._vector = Vector(vector)
        self._strenght = float(strenght)

    def solve(self):
        for each in self._partciles:
            each.addForce(self._vector * self._strenght)

class Gravity(ConstantForce):
    def __init__(self, partciles, strenght=.1):
        super(Gravity, self).__init__(partciles,[0,-1,0] ,strenght)