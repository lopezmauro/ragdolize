from maya import cmds
from maya.api import OpenMaya as om

class Body(object):
    def __init__(self, name, position=None, rotation=None):
        self.name = name
        self.setup()
        if position:
            cmds.xform(self.name, ws=1, t=position)
        if rotation:
            cmds.xform(self.name, ws=1, ro=rotation)
        self._position = cmds.xform(self.name, q=1, ws=1, t=1)
        self._rotation = cmds.xform(self.name, q=1, ws=1, ro=1)
        self._matrix = cmds.xform(self.name, q=1, ws=1, m=1)

    def setup(self):
        pass

    @property
    def position(self):
        self._position = cmds.xform(self.name, q=1, ws=1, t=1)
        return self._position

    @position.setter
    def position(self, pos):
        self._position = om.MVector(pos)
        cmds.xform(self.name, ws=1, t=pos)

    @property
    def rotation(self):
        self._rotation = cmds.xform(self.name, q=1, ws=1, ro=1)
        return self._rotation

    @rotation.setter
    def rotation(self, rotation):
        self._rotation = om.MVector(rotation)
        cmds.xform(self.name, ws=1, ro=rotation)

    @property
    def matrix(self):
        self._matrix = cmds.xform(self.name, q=1, ws=1, m=1)
        return self._matrix

    @matrix.setter
    def matrix(self, matrix):
        cmds.xform(self.name, ws=1, m=matrix)


class Sphere(Body):
    def __init__(self, name, position, radius=0.1):
        self.radius = radius
        super(Sphere, self).__init__(name, position)


    def setup(self):
        self.name = cmds.polySphere(radius=self.radius, n=self.name)[0]


class Cube(Body):
    def __init__(self, name, position, radius=0.2):
        self.radius = radius
        super(Cube, self).__init__(name, position)


    def setup(self):
        self.name = cmds.polyCube(w=self.radius, h=self.radius, d=self.radius, n=self.name)[0]



class Segment(Body):
    def __init__(self, position, radius, length):
        super(Segment, self).__init__(position, radius)
        self.length = length
