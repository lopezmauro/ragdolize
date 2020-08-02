from ..math_utils import Vector

class Particle(object):
    def __init__(self, pos=[0,0,0], mass=1.0, damping=.99):
        self._position = Vector(pos)
        self._damping = float(damping)
        self._mass = float(mass)
        self._oldPosition = Vector(pos)
        self._pinned = False
        self._accumForce = Vector([0,0,0])
        self._bounciness = float(1.0)

    @property
    def position(self):
        return self._position

    @property
    def damping(self):
        return self._damping

    @property
    def mass(self):
        return self._mass

    @property
    def oldPosition(self):
        return self._oldPosition

    @property
    def pinned(self):
        return self._pinned

    @property
    def accumForce(self):
        return self._accumForce

    @property
    def bounciness(self):
        return self._bounciness

    def addForce(self, force):
        self._accumForce += Vector(force)

    def clearForces(self):
        self._accumForce = Vector([0,0,0])

    def updatePoint(self):
        if self._pinned:
            return
        velocity = ((self._position - self._oldPosition) * self._damping)
        self._oldPosition = Vector(self._position)
        self._position += velocity 
        self._position += (self._accumForce /self._mass)
        self.clearForces()

    def addPosition(self, vector):
        self._position = self._position + Vector(vector)

    def getPosition(self):
        return self._position

    def setPosition(self, position):
        self._position = Vector(position)

    def getMass(self):
        return self._mass
    
    def setMass(self, mass):
        self._mass = float(mass)

    def getPrevPosition(self):
        return self._oldPosition

    def setPrevPosition(self, pos):
        self._oldPosition = Vector(pos)

    def setPinned(self, value=True):
        self._pinned = value

    def isPinned(self):
        return self._pinned
    
    def setDamping(self, value):
        self._damping = float(value)

    def getDamping(self):
        return self._damping

    def setBounciness(self, value):
        self._bounciness = float(value)

    def getBounciness(self):
        return self._bounciness

