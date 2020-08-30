# -*- coding: utf-8 -*-
"""Particle system complex rigs

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
import logging
import simulation
import particles
import constraints

class ChainSimulation(simulation.Simulation):
    """particle chain rig created using two set of particles, one static following 
    the base animation and another set of fully dynamic particles. And a spring contraint
    between them making the simulated particles follow the static ones
    """
    def __init__(self, basePositions, followBase=True):
        super(ChainSimulation, self).__init__()
        self.basePositions = basePositions
        self.followBase = followBase
        self.baseParticles = list()
        self.simParticles = list()
        self.springs = list()
        self.linkRope = None
        self.particlesMap = dict()
        self.setup()
    
    def setup(self):
        self.clear()
        self.baseParticles = list()
        self.simParticles = list()
        for each in self.basePositions:
            p = particles.Particle(each)
            p.setPinned()
            self.addParticle(p)
            self.baseParticles.append(p)
            p1 = particles.Particle(each)
            self.simParticles.append(p1)
            self.addParticle(p1)
        if self.followBase:
            for baseP, ropeP in zip(self.baseParticles, self.simParticles):
                spring = constraints.ParticleSpring(baseP, ropeP, 
                                                springStiffnes=1.0,
                                                springDamping=.8)

                self.springs.append(spring)
                self.addConstraint(spring)
        else:
            spring = constraints.ParticleSpring(self.baseParticles[0], self.simParticles[0], 
                                                springStiffnes=1.0,
                                                springDamping=1.0)

            self.springs.append(spring)
            self.addConstraint(spring)
        if len(self.simParticles) > 1:
            ropePart = [self.baseParticles[0]] + self.simParticles[1:]
            self.linkRope = constraints.ParticlesRope(ropePart, 50)
            self.addConstraint(self.linkRope)

    def setRigidity(self, stifnessList):
        for spring, stiff in zip(self.springs, stifnessList):
            spring.setStiffnes(stiff)

    def setElasticity(self, elasticityList):
        self.linkRope.setDamping(elasticityList)

    def setMasses(self, massesList):
        for particle, mass in zip(self.simParticles, massesList):
            particle.setMass(mass)
    
    def setRestLenght(self, lengthList):
        for spring, legth in zip(self.springs, lengthList):
            spring.setRestLenght(legth)
    
    def setBasePosition(self, positionList):
        for part, pos in zip(self.baseParticles, positionList):
            part.setPosition(pos)

    def getSimulatedPosition(self):
        return [a.getPosition() for a in self.simParticles]
    
    def getBasePosition(self):
        return [a.getPosition() for a in self.baseParticles]

    def reset(self):
        for i, each in enumerate(self.basePositions):
            self.baseParticles[i].setPosition(each)
            self.simParticles[i].setPosition(each)

