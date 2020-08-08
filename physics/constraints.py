class Constraint(object):
    def solve(self):
        raise NotImplementedError

class ParticleLink(Constraint):
    def __init__(self, particleA, particleB, damping=.9):
        self._particleA = particleA
        self._particleB = particleB
        self._damping = float(damping)
        self._restLenght = self.getdistance()

    def setDamping(self, damping):
        if damping <=0:
            damping = 0
        self._damping = float(damping)

    def setRestLenght(self, lenght):
        self._restLenght = float(lenght)

    def getRestLeght(self):
        return self._restLenght

    def getdistance(self):
        relativePos = self._particleB.getPosition() - self._particleA.getPosition() 
        return relativePos.magnitude()
    
    def solve(self):

        if self._particleA.isPinned() and self._particleB.isPinned():
            return
        relativePos = self._particleB.getPosition() - self._particleA.getPosition()
        distance = relativePos.magnitude()
        direction = relativePos.normalize()
        difference = abs(distance - self._restLenght)
        if distance == self._restLenght:
            direction *=0 
        elif (distance > self._restLenght):
            direction *= -1
        offset = .05
        if self._particleA.isPinned() or self._particleB.isPinned():
            offset = 1.0
        movement = direction * difference * self._damping
        if not self._particleA.isPinned():
            self._particleA.addPosition(-movement*offset)
            
        if not self._particleB.isPinned():
            self._particleB.addPosition(movement*offset)

class ParticleSpring(Constraint):
    def __init__(self, particleA, particleB, springStiffnes=.1, springDamping=.8):
        self._particleA = particleA
        self._particleB = particleB
        self._springStiffnes = float(springStiffnes)
        self._springDamping = float(springDamping)
        self._restLenght = self.getdistance()

    def setRestLenght(self, lenght):
        self._restLenght = float(lenght)

    def setStiffnes(self, stiffness):
        self._springStiffnes = float(stiffness)

    def getRestLeght(self):
        return self._restLenght

    def getdistance(self):
        relativePos = self._particleB.getPosition() - self._particleA.getPosition() 
        return relativePos.magnitude()
    
    def solve(self):
        if self._particleA.isPinned() and self._particleB.isPinned():
            return
        if self.getRestLeght() == 0:
            self._particleB.setPosition(self._particleA.getPosition())
            return
        springVector = self._particleB.getPosition() - self._particleA.getPosition()    # Vector Between The Two Masses
        r = springVector.magnitude()               # Distance Between The Two Masses
        tension = r - self.getRestLeght() # curren lenght vs rest lenght
        if tension <= 0: #avoid sqash repulsion
            return
        # The Spring Force Is Added To The Force      
        direction = (springVector / r) # unit vector for representing just the directional vector between the masses
        force = -direction * tension * self._springStiffnes
        #force += -(self.mass1.vel - self.mass2.vel) * self.frictionConstant       # The Friction Force Is Added To The force
        #self._particleA.addPosition(force)                    # Force Is Applied To mass1
        self._particleB.addPosition(force*self._springDamping)


class ParticlesRope(Constraint):
    def __init__(self, particles, iterations=20, damping=.9):
        self._particles = particles
        self._iterations = iterations
        self._damping = damping
        self._links = list()
        self.setup()

    def setup(self):
        self.link = list()
        self._particles[0].setPinned(True)
        for i, particle in enumerate(self._particles[:-1]):
            self._links.append(ParticleLink(particle,self._particles[i+1], self._damping))

    def solve(self):
        for i in range(self._iterations):
            for link in self._links:
                link.solve()

    def setRigidity(self, dampingList):
        for link, stiff in zip(self._links, dampingList):
            if stiff>1:
                stiff = 1
            elif stiff<.01:
                stiff = .01
            link.setDamping(stiff)
