import os
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
import ui_utils
import ramp
import widgets
from maya import cmds

from ..physics import rigs
from ..physics import forces
from ..physics import colliders
from ..math_utils import Vector
from ..maya_utils import maya_body
from ..maya_utils import context
from ..maya_utils import animation
from ..maya_utils import transforms

iconsDir = r'D:\dev\fakeDyn\ui\icons'

class RagdolizeUI(QtWidgets.QWidget):
    def __init__(self, parent=ui_utils.maya_main_window()):
        super(RagdolizeUI, self).__init__(parent)
        self.setupUi()
        self.setDefaultValues()


    def setupUi(self):
        self.setWindowTitle("Radgollize Controls UI")
        self.setWindowFlags(QtCore.Qt.Tool)
        self.resize(300, 400) # re-size the window
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        # layout
        self.setLayout(self.mainLayout)
        self.gravSpin = widgets.labeledWidget(self, self.mainLayout,
                                               QtWidgets.QDoubleSpinBox, "Gravity",
                                               os.path.join(iconsDir,'gravity.png'))
        self.dampSpin = widgets.labeledWidget(self, self.mainLayout,
                                               QtWidgets.QDoubleSpinBox, "Damping",
                                               os.path.join(iconsDir,'damping.png'))
        # Create follow gradient control
        followGrp = QtWidgets.QFrame(self)
        followGrp.setFrameShape(QtWidgets.QFrame.StyledPanel)
        followLay = QtWidgets.QVBoxLayout(self)
        followLay.setContentsMargins(1, 1, 1, 1)
        widgets.labeledWidget(followGrp, followLay, widgets.QHLine, "Follow Goal",
                                            os.path.join(iconsDir,'attraction.png'),
                                            30)
        self.followRamp = ramp.RampWidget()
        followLay.addWidget(self.followRamp)
        self.detachMult = widgets.labeledWidget(followGrp, followLay, QtWidgets.QDoubleSpinBox,
                                            "Detach multiply")
        followGrp.setLayout(followLay)
        self.mainLayout.addWidget(followGrp)
        # Create rigifity gradient control
        rigidityGrp = QtWidgets.QFrame(self)
        rigidityGrp.setFrameShape(QtWidgets.QFrame.StyledPanel)
        rigidityLay = QtWidgets.QVBoxLayout(self)
        rigidityLay.setContentsMargins(1, 1, 1, 1)
        widgets.labeledWidget(rigidityGrp, rigidityLay, widgets.QHLine, "Rigidity",
                                            os.path.join(iconsDir,'rigidity.png'),
                                            30)
        self.rigidityRamp = ramp.RampWidget()
        rigidityLay.addWidget(self.rigidityRamp)
        rigidityGrp.setLayout(rigidityLay)

        self.mainLayout.addWidget(rigidityGrp)

        self.layerCombo = widgets.labeledWidget(self, self.mainLayout, QtWidgets.QComboBox, "AnimLayer",
                                            os.path.join(iconsDir,'layers.png'))
        self.layerCombo.addItem('Dynamics')
        self.slider = widgets.labeledWidget(self, self.mainLayout, widgets.QCustomSlider,
                                            "Simplify Anim Curve",
                                            os.path.join(iconsDir,'simplify.png'))
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setTickLabels((0,.5,1))
        self.slider.setTickInterval(.1)
        self.slider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.doitBtn = QtWidgets.QPushButton(self, 'Ragdollize')
        self.doitBtn.setIcon(QtGui.QIcon(os.path.join(iconsDir,'dynamic.png')))
        self.doitBtn.setText("Ragdollize")
        self.doitBtn.setIconSize(QtCore.QSize(50,50))
        self.mainLayout.addWidget(self.doitBtn)

        self.doitBtn.clicked.connect(self.doit)

    def setDefaultValues(self):
        self.gravSpin.setValue(.1)
        self.gravSpin.setSingleStep(.01)
        self.dampSpin.setValue(.97)
        self.dampSpin.setSingleStep(.01)
        self.followRamp.setValue([(1,0,3),(0,1,3)])
        self.detachMult.setValue(1)
        self.dampSpin.setSingleStep(.1)
        self.rigidityRamp.setValue([(1,0,3),(.1,1,3)])


    def getUIValues(self, rampPoints):
        result = dict()
        result['gravity'] = self.gravSpin.value()
        result['damping'] = self.dampSpin.value()
        attractionValues = list()
        for point in rampPoints:
            attractionValues.append(self.followRamp.getValueAtPoint(point))
        result['follow'] = [(1-a)*self.detachMult.value() for a in attractionValues]
        result['rigidity'] = list()
        for point in rampPoints:
            result['rigidity'].append(self.rigidityRamp.getValueAtPoint(point))
        return result

    def doit(self):
        controls = cmds.ls(sl=1)
        rampPoints = [float(a)/(len(controls)-1) for a in range(len(controls))]
        dynValues = self.getUIValues(rampPoints)
        fameRange = (int(cmds.playbackOptions(q=1, min=1)), int(cmds.playbackOptions(q=1, max=1)))
        animDict = animation.getNodesPosInRange(controls, fameRange)
        positionList = list()
        for control in controls:
            positionList.append(animDict.get(control)[0])
        sim = rigs.ChainSimulation(positionList)
        simPos = sim.getSimulatedPosition()
        sim.setRestLenght(dynValues.get('follow'))
        sim.setRigidity(dynValues.get('rigidity'))
        sim.setDamping(dynValues.get('damping'))
        baseName = 'simulated{}'
        grav = forces.Gravity(sim.getParticles(), dynValues.get('gravity'))
        sim.addForce(grav)
        coll = colliders.GroundCollider(sim.getParticles(),bouncinnes=0.5)
        #sim.addCollider(coll)
        prevPosList = positionList[:]
        for f in range(*fameRange):
            sim.setBasePosition(prevPosList)
            sim.simulate()
            simPositions = sim.getSimulatedPosition()
            positionList = list()
            for i, control in enumerate(controls):
                if len(animDict.get(control)) > f:
                    positionList.append(animDict.get(control)[f])
                else:
                    positionList.append(prevPosList[i]) 
            prevPosList = positionList[:]
            cmds.currentTime(f)
            for i, control in enumerate(controls):
                pos = transforms.getLocalTranslation(control, simPositions[i])
                cmds.setKeyframe(control, v=pos[0], at='translateX',t=[f,f])
                cmds.setKeyframe(control, v=pos[1], at='translateY',t=[f,f])
                cmds.setKeyframe(control, v=pos[2], at='translateZ',t=[f,f])
                if i< len(controls)-1:
                    currPos = cmds.xform(control, q=1, ws=1, t=1)
                    worldRot = transforms.getAimRotation(currPos, simPositions[i+1])
                    rot = transforms.getLocalRotation(control, worldRot)
                else:
                    worldRot = transforms.getAimRotation(simPositions[i], simPositions[i-1], aim=(-1,0,0))
                    rot = transforms.getLocalRotation(control, worldRot)
                    rot=[a*2 for a in rot]
                cmds.setKeyframe(control, v=rot[0], at='rotateX',t=[f,f])
                cmds.setKeyframe(control, v=rot[1], at='rotateY',t=[f,f])
                cmds.setKeyframe(control, v=rot[2], at='rotateZ',t=[f,f])


