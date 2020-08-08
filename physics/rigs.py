import logging
import simulation
import particles
import constraints


class ChainSimulation(simulation.Simulation):
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
        self.linkRope = constraints.ParticlesRope(self.simParticles, 50, .1)
        self.addConstraint(self.linkRope)

    def setRigidity(self, stifnessList):
        for spring, stiff in zip(self.springs, stifnessList):
            spring.setStiffnes(stiff)

    def setElasticity(self, elasticityList):
        self.linkRope.setRigidity(elasticityList)

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

    def reset(self):
        for i, each in enumerate(self.basePositions):
            self.baseParticles[i].setPosition(each)
            self.simParticles[i].setPosition(each)

