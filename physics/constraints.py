# -*- coding: utf-8 -*-
"""This module is mean to be used to get the main training data for train the model to be used on ml_rivets.mll node
This code is to be used on maya with numpy library

MIT License

Copyright (c) 2020 Mauro Lopez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFT
"""
class Constraint(object):
    """base particles constraint abstraction
    """
    def solve(self):
        """this method will be called for the dynamic system to solve the costraints
        between particles, this should be override by each Constraint instance
        """
        raise NotImplementedError

class ParticleLink(Constraint):
    """connect two particles together in order to preserve the fixed distance between them
    """
    def __init__(self, particleA, particleB, damping=.9):
        self._particleA = particleA
        self._particleB = particleB
        self._damping = float(damping)
        self._restLenght = self.getdistance()

    def setDamping(self, damping):
        """how much the linked particule folow without delay
        Args:
            damping (float): value between 0-1
        """
        if damping <=0:
            damping = 0
        self._damping = float(damping)

    def setRestLenght(self, lenght):
        """set fixed distance between the particles
        Args:
            lenght (float): distance between the particles
        """
        self._restLenght = float(lenght)

    def getRestLeght(self):
        """get fixed distance between particles
        Returns:
            float
        """
        return self._restLenght

    def getdistance(self):
        """get current distance between particles
        Returns:
            float
        """
        relativePos = self._particleB.getPosition() - self._particleA.getPosition() 
        return relativePos.magnitude()
    
    def solve(self):
        """move particules preserving the rest distance, if the particles are 
        more far away then the rest distnce it will pull them closer, and vice versa
        """
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
    """connect two particles together in order to preserve the fixed distance between them
    preserving the force created after get the fixed distance (streetch or compress force)
    and aplying that force to the second paricule making it bounce
    """
    def __init__(self, particleA, particleB, springStiffnes=.1, springDamping=.8):
        self._particleA = particleA
        self._particleB = particleB
        self._springStiffnes = float(springStiffnes)
        self._springDamping = float(springDamping)
        self._restLenght = self.getdistance()

    def setRestLenght(self, lenght):
        """set fixed distance between particles
        Returns:
            float
        """
        self._restLenght = float(lenght)

    def setStiffnes(self, stiffness):
        """set froce preservation value
        Returns:
            float
        """
        self._springStiffnes = float(stiffness)

    def getRestLeght(self):
        """get fixed distance between particles
        Returns:
            float
        """
        return self._restLenght

    def getdistance(self):
        """get current distance between particles
        Returns:
            float
        """
        relativePos = self._particleB.getPosition() - self._particleA.getPosition() 
        return relativePos.magnitude()
    
    def solve(self):
        """move particules preserving the rest distance, if the particles are 
        more far away then the rest distnce it will pull them closer, and vice versa
        then apply the bounce force to the second particule
        """
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
    """link several particules to create a rope
    """
    def __init__(self, particles, iterations=20, damping=.9):
        self._particles = particles
        self._iterations = iterations
        self._damping = damping
        self._links = list()
        self.setup()

    def setup(self):
        """create a link constrain between each particles
        """
        self.link = list()
        for i, particle in enumerate(self._particles[:-1]):
            self._links.append(ParticleLink(particle,self._particles[i+1], self._damping))

    def solve(self):
        """solve each link contraints through several iterations to reduce
        particle position error on each iteration
        """
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
