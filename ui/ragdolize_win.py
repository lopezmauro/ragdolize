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

dir_path = os.path.dirname(os.path.realpath(__file__))
iconsDir = os.path.join(dir_path, 'icons')

DYNLAYER = 'dynamics'
NEWLAYER = 'NewLayer...'
SLIDERMULT = 10.0
class RagdolizeUI(QtWidgets.QWidget):
    def __init__(self, parent=ui_utils.maya_main_window()):
        super(RagdolizeUI, self).__init__(parent)
        self.setupUi()
        self.populateLayerCombo()
        self.setDefaultValues()
        


    def setupUi(self):
        self.setWindowTitle("Radgollize Controls UI")
        self.setWindowFlags(QtCore.Qt.Tool)
        self.resize(300, 400) # re-size the window
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        # layout
        self.setLayout(self.mainLayout)
        print '>>>', iconsDir
        self.gravSpin = widgets.labeledWidget(self, self.mainLayout,
                                               QtWidgets.QDoubleSpinBox, "Gravity",
                                               os.path.join(iconsDir,'gravity.png'))
        self.dampSpin = widgets.labeledWidget(self, self.mainLayout,
                                               QtWidgets.QDoubleSpinBox, "Damping",
                                               os.path.join(iconsDir,'damping.png'))
        # Create follow gradient control
        self.followGrp = QtWidgets.QGroupBox(self)
        #self.followGrp.setFrameShape(QtWidgets.QFrame.StyledPanel)
        
        followMainLay = QtWidgets.QVBoxLayout(self)
        followMainLay.setContentsMargins(1, 1, 1, 1)
        followTitleLay = QtWidgets.QHBoxLayout(self)
        followTitleLay.setContentsMargins(0, 0, 0, 0)
        self.followCBx = QtWidgets.QCheckBox()
        self.followCBx.stateChanged.connect(self.diableFollowFrame)
        followTitleLay.addWidget(self.followCBx)
        self.goalTitle = widgets.labeledWidget(self.followGrp, followTitleLay, widgets.QHLine, "Follow Base Anim",
                                            os.path.join(iconsDir,'attraction.png'),
                                            30)
        followMainLay.addLayout(followTitleLay)
        self.followWidg = QtWidgets.QWidget(self.followGrp)
        followLay = QtWidgets.QVBoxLayout(self.followGrp)
        followLay.setContentsMargins(0, 0, 0, 0)
        followLay.setSpacing(0)
        self.followRamp = ramp.RampWidget()
        followLay.addWidget(self.followRamp)
        self.detachMult = widgets.labeledWidget(self.followWidg, followLay, QtWidgets.QDoubleSpinBox,
                                            "Detach multiply")
        # Create rigidity gradient control
        widgets.labeledWidget(self.followWidg, followLay, widgets.QHLine, "Rigidity",
                                            os.path.join(iconsDir,'rigidity.png'),
                                            30)
        self.rigidityRamp = ramp.RampWidget()
        followLay.addWidget(self.rigidityRamp)


        self.followWidg.setLayout(followLay)
        followMainLay.addWidget(self.followWidg)
        self.followGrp.setLayout(followMainLay)
        self.mainLayout.addWidget(self.followGrp)
        # Create mass gradient control
        massGrp = QtWidgets.QGroupBox(self)
        #massGrp.setFrameShape(QtWidgets.QFrame.StyledPanel)
        massLay = QtWidgets.QVBoxLayout(self)
        massLay.setContentsMargins(1, 1, 1, 1)
        widgets.labeledWidget(massGrp, massLay, widgets.QHLine, "Mass",
                                            os.path.join(iconsDir,'mass.png'),
                                            30)
        self.massRamp = ramp.RampWidget()
        massLay.addWidget(self.massRamp)
        self.massMult = widgets.labeledWidget(massGrp, massLay, QtWidgets.QDoubleSpinBox,
                                            "Mass multiply")
        massLay.addWidget(self.massMult)
        massGrp.setLayout(massLay)
        self.mainLayout.addWidget(massGrp)
        self.layerCombo = widgets.labeledWidget(self, self.mainLayout, QtWidgets.QComboBox, "AnimLayer",
                                            os.path.join(iconsDir,'layers.png'))
        self.layerCombo.currentIndexChanged.connect(self.addNewLayer)
        self.checkBoxesLayout = QtWidgets.QHBoxLayout(self)
        self.rotationCbx = QtWidgets.QCheckBox("Enable Rotations")
        self.checkBoxesLayout.addWidget(self.rotationCbx)
        self.cleanAnimation = QtWidgets.QCheckBox("Clean Anim layer")
        self.cleanAnimation.setChecked(True)
        self.checkBoxesLayout.addWidget(self.cleanAnimation)
        self.mainLayout.addLayout(self.checkBoxesLayout)
        self.doitBtn = QtWidgets.QPushButton(self, 'Ragdollize')
        self.doitBtn.setIcon(QtGui.QIcon(os.path.join(iconsDir,'dynamic.png')))
        self.doitBtn.setText("Ragdollize")
        self.doitBtn.setIconSize(QtCore.QSize(50,50))
        self.mainLayout.addWidget(self.doitBtn)
        self.simplify_sld = widgets.labeledWidget(self, self.mainLayout, widgets.QCustomSlider,
                                            "Simplify Anim Curve",
                                            os.path.join(iconsDir,'simplify.png'))
        self.simplify_sld.setOrientation(QtCore.Qt.Horizontal)
        self.simplify_sld.setMinimum(0)
        self.simplify_sld.setMaximum(SLIDERMULT)
        self.simplify_sld.setSingleStep(1)
        self.simplify_sld.setTickInterval(1)
        self.simplify_sld.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.simplify_sld.sliderReleased.connect(self.simplifyAnimationCurves)
        self.doitBtn.clicked.connect(self.doit)

    def populateLayerCombo(self):
        animationLayer = cmds.ls(type='animLayer')
        if not DYNLAYER in animationLayer:
            animationLayer.append(DYNLAYER)
        animationLayer.append(NEWLAYER)
        self.layerCombo.clear()
        for layer in animationLayer:
            self.layerCombo.addItem(layer)
        
    def diableFollowFrame(self, value):
        if value:
            self.followWidg.setVisible(True)
        else:
            self.followWidg.setVisible(False)
        return
        if value:
            self.goalTitle.setEnabled(True)
            self.followWidg.setEnabled(True)
        else:
            self.goalTitle.setEnabled(False)
            self.followWidg.setEnabled(False)

    def addNewLayer(self):
        if str(self.layerCombo.currentText()) != NEWLAYER:
            return
        text, ok = QtWidgets.QInputDialog.getText(self, 'New Layer', 
                                                  'Enter layer name:')
        if ok:
            layer = animation.createAnimLayer(text)
        else:
            layer = DYNLAYER
        self.populateLayerCombo()
        self.layerCombo.setCurrentIndex(self.layerCombo.findText(layer))

    def setDefaultValues(self):
        self.followCBx.setChecked(True)
        self.gravSpin.setValue(9.8)
        self.gravSpin.setSingleStep(.1)
        self.dampSpin.setValue(.97)
        self.dampSpin.setSingleStep(.01)
        self.followRamp.setValue([(1,0,3),(0,1,3)])
        self.detachMult.setValue(1)
        self.dampSpin.setSingleStep(.1)
        self.rigidityRamp.setValue([(1,0,3),(.1,1,3)])
        self.massRamp.setValue([(.5,0,3),(.6,1,3)])
        self.massMult.setValue(2)
        self.layerCombo.setCurrentIndex(self.layerCombo.findText(DYNLAYER))
        self.simplify_sld.setValue(SLIDERMULT)

    def doit(self):
        controls = cmds.ls(sl=1)
        rampPoints = [float(a)/(len(controls)-1) for a in range(len(controls))]
        gravity = self.gravSpin.value()/10
        damping = self.dampSpin.value()
        attractionValues = self.followRamp.getValueAtPoints(rampPoints)
        follow = [(1-a)*self.detachMult.value() for a in attractionValues]
        rigidity = self.rigidityRamp.getValueAtPoints(rampPoints)
        animLayer = self.layerCombo.currentText()
        massesRamp = self.massRamp.getValueAtPoints(rampPoints)
        masses = [a*self.massMult.value() for a in massesRamp]
        doRotations = self.rotationCbx.isChecked()
        followBase = self.followCBx.isChecked()
        fameRange = (int(cmds.playbackOptions(q=1, min=1)), int(cmds.playbackOptions(q=1, max=1)))
        if self.cleanAnimation.isChecked():
            #clear layer animation
            animation.createAnimLayer(animLayer, controls)
            for node in controls:
                for animCurve in animation.getLayerAnimCurves(node, animLayer):
                    animation.clearAnimCurve(animCurve)
        #get control world animation fomr all layers
        animDict = animation.getNodesPosInRange(controls, fameRange)
        positionList = list()
        for control in controls:
            positionList.append(animDict.get(control)[0])
        dynSystem = self.createDynSystem(positionList,
                                         follow,
                                         rigidity,
                                         damping,
                                         gravity,
                                         masses,
                                         followBase)
        self.createSymKeys(controls,
                           fameRange,
                           animLayer,
                           dynSystem,
                           animDict,
                           doRotations)
        for control in controls:
            for animCurve in animation.getLayerAnimCurves(control, animLayer):
                animation.cacheCurvePoints(animCurve)

    def createDynSystem(self, positionList, follow, rigidity, damping, gravity, masses, followBase):
        sim = rigs.ChainSimulation(positionList, followBase)
        sim.setRestLenght(follow)
        sim.setRigidity(rigidity)
        sim.setDamping(damping)
        grav = forces.Gravity(sim.getParticles(),gravity)
        sim.addForce(grav)
        sim.setMasses(masses)
        # coll = colliders.GroundCollider(sim.getParticles(),bouncinnes=0.5)
        return sim

    def simplifyAnimationCurves(self):
        animLayer = self.layerCombo.currentText()
        epsilon = 1.0-self.simplify_sld.value()/SLIDERMULT
        selection = cmds.ls(sl=1)
        for node in selection:
            for animCurve in animation.getLayerAnimCurves(node, animLayer):
                animation.simplyfyAnimCurve(animCurve, epsilon)

    def createSymKeys(self, controls, fameRange, animLayer, dynSystem, animDict, doRotations=True):
        prevPosList = dynSystem.getSimulatedPosition()
        for f in range(*fameRange):
            dynSystem.setBasePosition(prevPosList)
            dynSystem.simulate()
            simPositions = dynSystem.getSimulatedPosition()
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
                if not doRotations:
                    continue
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
