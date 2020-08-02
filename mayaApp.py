import time
import random
import logging
from maya import cmds
from physics import rigs
from physics import forces
from physics import colliders
from math_utils import Vector
from maya_utils import maya_body
from maya_utils import context
from maya_utils import animation
from maya_utils import transforms

logging.basicConfig(level=logging.DEBUG)
def run():
    start_time = time.time()
    with context.SuspendRefresh():
        main()
    elapsed_time = time.time() - start_time
    print(Vector)
    print("simulation time {}".format(elapsed_time)) 

def createtestAnimation(numControls):
    mayaNodes = list()
    baseName = 'Control{}'
    for i in range(numControls):
        x = i*2
        y = 10
        z = 0 
        sphere = maya_body.Sphere(baseName.format(i), [x,y,z])
        mayaNodes.append(sphere)
    for f in range(50):
        for each in mayaNodes:
            currp = each.position
            if f>20:
                if f<30:
                    currp[1] -=1.0
                elif f<70:
                    currp[2] +=1.0
            each.position = currp
            cmds.setKeyframe(each.name, v=currp[0], at='translateX',t=[f,f])
            cmds.setKeyframe(each.name, v=currp[1], at='translateY',t=[f,f])
            cmds.setKeyframe(each.name, v=currp[2], at='translateZ',t=[f,f])
    return [a.name for a in mayaNodes]

def main():
    fameRange = (0, 100)
    cmds.file(new=1, f=1)
    cmds.playbackOptions(min=fameRange[0], max=fameRange[1])
    controls = createtestAnimation(5)
    animDict = animation.getNodesWorldMatrixInRange(controls, fameRange)
    positionList = list()
    for control in controls:
        positionList.append(animDict.get(control)[0])
    sim = rigs.ChainSimulation(positionList)
    simPos = sim.getSimulatedPosition()
    sim.setRestLenght([a for a in range(len(positionList))])
    sim.setRigidity([1.0,.8,.7,.6,.4,.2])
    baseName = 'simulated{}'
    simNodes = [maya_body.Cube(baseName.format(i), a) for i, a in enumerate(simPos)]
    grav = forces.Gravity(sim.getParticles())
    sim.addForce(grav)
    coll = colliders.GroundCollider(sim.getParticles(),bouncinnes=0.5)
    #sim.addCollider(coll)
    for f in range(*fameRange):
        positionList = list()
        for control in controls:
            positionList.append(animDict.get(control)[f])
        sim.setBasePosition(positionList)
        sim.simulate()
        simPositions = sim.getSimulatedPosition()
        for i in range(len(simNodes)):
            pos = transforms.getLocalTranslation(simNodes[i].name, simPositions[i])
            #pos = simPositions[i]
            #cmds.setKeyframe(simNodes[i].name, v=pos[0], at='translateX',t=[f,f])
            #cmds.setKeyframe(simNodes[i].name, v=pos[1], at='translateY',t=[f,f])
            #cmds.setKeyframe(simNodes[i].name, v=pos[2], at='translateZ',t=[f,f])
            if i< len(simNodes)-1:
                worldRot = transforms.getAimRotation(simPositions[i], simPositions[i+1])
            else:
                worldRot = transforms.getAimRotation(simPositions[i], simPositions[i-1], aim=(-1,0,0))
            rot = transforms.getLocalRotation(simNodes[i].name, worldRot)
            cmds.setKeyframe(simNodes[i].name, v=rot[0], at='rotateX',t=[f,f])
            cmds.setKeyframe(simNodes[i].name, v=rot[1], at='rotateY',t=[f,f])
            cmds.setKeyframe(simNodes[i].name, v=rot[2], at='rotateZ',t=[f,f])


