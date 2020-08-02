import simulation
import forces
import particles
import constraints
import collisions
import numpy as np
import random
sim = simulation.Simulation()
for i in range(1):
    x = i*2
    y = 10
    p = particles.Particle([x,y,0])
    p.setPrevPosition([x+random.uniform(-1, 1),y+random.uniform(-1, 1),0])
    '''
    if x == 0:
        p.setPinned()
    else:
        link = constraints.ParticleLink(p, sim.getParticles()[-1])
        sim.addConstraint(link)
    '''
    sim.addParticle(p)

grav = forces.Gravity(sim.getParticles(), 0.5)
sim.addForce(grav)
coll = collisions.GroundCollisions(sim.getParticles(), .2)
sim.addCollisions(coll)

for x in range(100):
    sim.simulate()
    for i, each in enumerate(sim.getParticles()):
        print (f'>>{i}: {np.round(each.getPosition())}')
