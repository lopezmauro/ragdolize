import os
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from maya import cmds

import ui_utils
import ramp
import widgets
import resources

from ..physics import rigs
from ..physics import forces
from ..physics import colliders
from ..math_utils import Vector
from ..maya_utils import maya_body
from ..maya_utils import context
from ..maya_utils import animation
from ..maya_utils import transforms

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
        gravWidg, self.gravSpin = widgets.labeledWidget(QtWidgets.QDoubleSpinBox, 
                                                   self,
                                                   "Gravity",
                                                   ':/icons/gravity.png')
        self.mainLayout.addWidget(gravWidg)
        dampWidg, self.dampSpin = widgets.labeledWidget(QtWidgets.QDoubleSpinBox, 
                                              self,
                                              "Damping",
                                              ':/icons/damping.png')
        self.mainLayout.addWidget(dampWidg)
        # Create follow gradient control
        self.followGrp = widgets.CollapsibleGroup(self, "Follow Base Anim", ':/icons/attraction.png')
        self.followCBx = QtWidgets.QCheckBox("Follow base animation")
        self.followCBx.stateChanged.connect(self.diableFollowFrame)
        self.followGrp.addWidget(self.followCBx)
        
        self.followRamp = ramp.RampWidget()
        self.followGrp.addWidget(self.followRamp)
        detachWidg, self.detachMult = widgets.labeledWidget(QtWidgets.QDoubleSpinBox, self.followGrp,
                                                "Detach multiply")
        self.followGrp.addWidget(detachWidg)
        # Create rigidity gradient control
        rigTitleWidg = widgets.labeledWidget(widgets.QHLine, self.followGrp, "Rigidity",
                                            ':/icons/rigidity.png', 30)[0]
        self.followGrp.addWidget(rigTitleWidg)
        self.rigidityRamp = ramp.RampWidget()
        self.followGrp.addWidget(self.rigidityRamp)
        self.mainLayout.addWidget(self.followGrp)

        # Create elasticity gradient control

        self.elasticityGrp = widgets.CollapsibleGroup(self, "elasticity", ':/icons/elasticity.png')
        self.elasticityRamp = ramp.RampWidget()
        self.elasticityGrp.addWidget(self.elasticityRamp)
        elasticityWidg, self.elasticityMult = widgets.labeledWidget(QtWidgets.QDoubleSpinBox, self.elasticityGrp,
                                            "elasticity multiply")
        
        self.elasticityGrp.addWidget(elasticityWidg)
        self.mainLayout.addWidget(self.elasticityGrp)

        # Create mass gradient control

        self.massGrp = widgets.CollapsibleGroup(self, "Mass", ':/icons/mass.png')
        self.massRamp = ramp.RampWidget()
        self.massGrp.addWidget(self.massRamp)
        massWidg, self.massMult = widgets.labeledWidget(QtWidgets.QDoubleSpinBox, self.massGrp,
                                            "Mass multiply")
        
        self.massGrp.addWidget(massWidg)
        self.mainLayout.addWidget(self.massGrp)
        layerWidg, self.layerCombo = widgets.labeledWidget(QtWidgets.QComboBox, self, "AnimLayer",
                                            ':/icons/layers.png')
        self.mainLayout.addWidget(layerWidg)
        self.layerCombo.currentIndexChanged.connect(self.addNewLayer)
        self.checkBoxesLayout = QtWidgets.QHBoxLayout(self)
        self.rotationCbx = QtWidgets.QCheckBox("Enable Rotations")
        self.checkBoxesLayout.addWidget(self.rotationCbx)
        self.cleanAnimation = QtWidgets.QCheckBox("Clean Anim layer")
        self.cleanAnimation.setChecked(True)
        self.checkBoxesLayout.addWidget(self.cleanAnimation)
        self.mainLayout.addLayout(self.checkBoxesLayout)
        self.doitBtn = QtWidgets.QPushButton(self, 'Ragdollize')
        self.doitBtn.setIcon(QtGui.QIcon(':/icons/dynamic.png'))
        self.doitBtn.setText("Ragdollize")
        self.doitBtn.setIconSize(QtCore.QSize(50,50))
        self.mainLayout.addWidget(self.doitBtn)
        simplifyWidg, self.simplify_sld = widgets.labeledWidget( widgets.QCustomSlider, self,
                                            "Simplify Anim Curve",
                                            ':/icons/simplify.png')
        self.mainLayout.addWidget(simplifyWidg)
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
            self.followRamp.setEnabled(True)
            self.detachMult.setEnabled(True)
            self.rigidityRamp.setEnabled(True)
        else:
            self.followRamp.setEnabled(False)
            self.detachMult.setEnabled(False)
            self.rigidityRamp.setEnabled(False)

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
        self.elasticityRamp.setValue([(0,0,3),(.1,1,3)])
        self.massRamp.setValue([(.5,0,3),(.6,1,3)])
        self.massMult.setValue(2)
        self.layerCombo.setCurrentIndex(self.layerCombo.findText(DYNLAYER))
        self.simplify_sld.setValue(SLIDERMULT)
        self.elasticityGrp.setCollapsed(True)
        self.massGrp.setCollapsed(True)

    def doit(self):
        controls = cmds.ls(sl=1)
        rampPoints = [float(a)/(len(controls)-1) for a in range(len(controls))]
        gravity = self.gravSpin.value()/10
        damping = self.dampSpin.value()
        attractionValues = self.followRamp.getValueAtPoints(rampPoints)
        follow = [(1-a)*self.detachMult.value() for a in attractionValues]
        rigidity = self.rigidityRamp.getValueAtPoints(rampPoints)
        elasticity = [1-a for a in self.elasticityRamp.getValueAtPoints(rampPoints)]
        massesRamp = self.massRamp.getValueAtPoints(rampPoints)
        masses = [a*self.massMult.value() for a in massesRamp]
        animLayer = self.layerCombo.currentText()
        doRotations = self.rotationCbx.isChecked()
        followBase = self.followCBx.isChecked()
        fameRange = (int(cmds.playbackOptions(q=1, min=1)), int(cmds.playbackOptions(q=1, max=1)))
        animation.createAnimLayer(animLayer, controls)
        if self.cleanAnimation.isChecked():
            #clear layer animation
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
                                         elasticity,
                                         damping,
                                         gravity,
                                         masses,
                                         followBase)
        self.createSymKeys(controls,
                           fameRange,
                           dynSystem,
                           animDict,
                           doRotations)
        for control in controls:
            for animCurve in animation.getLayerAnimCurves(control, animLayer):
                animation.cacheCurvePoints(animCurve)

    def createDynSystem(self, positionList, follow, rigidity, elasticity, damping, gravity, masses, followBase):
        sim = rigs.ChainSimulation(positionList, followBase)
        sim.setRestLenght(follow)
        sim.setRigidity(rigidity)
        sim.setElasticity(elasticity)
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

    def createSymKeys(self, controls, fameRange, dynSystem, animDict, doRotations=True):
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
                pos = transforms.getLocalTranslation(control, simPositions[i], f)
                cmds.setKeyframe(control, v=pos[0], at='translateX',t=[f,f])
                cmds.setKeyframe(control, v=pos[1], at='translateY',t=[f,f])
                cmds.setKeyframe(control, v=pos[2], at='translateZ',t=[f,f])
                if not doRotations:
                    continue
                if i< len(controls)-1:
                    worldRot = transforms.getAimRotation(simPositions[i], simPositions[i+1])
                    rot = transforms.getLocalRotation(control, worldRot, f)
                else:
                    worldRot = transforms.getAimRotation(simPositions[i], simPositions[i-1], aim=(-1,0,0))
                    rot = transforms.getLocalRotation(control, worldRot, f)
                cmds.setKeyframe(control, v=rot[0], at='rotateX',t=[f,f])
                cmds.setKeyframe(control, v=rot[1], at='rotateY',t=[f,f])
                cmds.setKeyframe(control, v=rot[2], at='rotateZ',t=[f,f])
