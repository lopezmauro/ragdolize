import particles
import forces
import constraints
import colliders

class Simulation(object):

    def __init__(self):
        self._particles = list()
        self._forces = list()
        self._constaints = list()
        self._colliders = list()
        self._iterations = 5
        self._damping = float(1)

    def clear(self):
        self._particles = list()
        self._forces = list()
        self._constaints = list()
        self._colliders = list()

    def addParticle(self, particle):
        if not isinstance(particle, particles.Particle):
            raise ValueError('{} is not instance of {}'.format(particle, particles.Particle))
        self._particles.append(particle)

    def setDamping(self, value):
        self._damping = float(value)
        for part in self._particles:
            part.setDamping(self._damping)

    def setIterations(self, iterations):
        self._iterations = int(iterations)

    def addParticles(self, particles):
        for each in particles:
            self.addParticle(each)

    def getParticles(self):
        return self._particles

    def getParticle(self, index):
        return self._particles[index]

    def addForce(self, force):
        if not isinstance(force, forces.Force):
            raise ValueError('{} is not instance of {}'.format(force, forces.Force))
        self._forces.append(force)

    def getForces(self):
        return self._forces

    def addConstraint(self, constraint):
        if not isinstance(constraint, constraints.Constraint):
            raise ValueError('{} is not instance of {}'.format(constraint, constraints.Constraint))
        self._constaints.append(constraint)
    
    def getAllConstraint(self):
        return self._constaints

    def addCollider(self, collider):
        if not isinstance(collider, colliders.Collider):
            raise ValueError('{} is not instance of {}'.format(collider, colliders.Collider))
        self._colliders.append(collider)
    
    def addColliders(self):
        return self._colliders

    def simulate(self):
        for force in self._forces:
            force.solve()

        for particle in self._particles:
            particle.updatePoint()

        for constaint in self._constaints:
            constaint.solve()
        #collision resolver
        for collision in self._colliders:
            collision.solve()

