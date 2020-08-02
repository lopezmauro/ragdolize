from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore


def labeledWidget(parent, layout, widgetInst, label, pixmap=None, siconSize=40):
    wid = QtWidgets.QWidget(parent)
    lay = QtWidgets.QHBoxLayout(wid)
    lay.setContentsMargins(1, 1, 1, 1)
    label =  QtWidgets.QLabel(label)
    if pixmap is None:
        lay.addWidget(label)
    else:
        lay1 = QtWidgets.QHBoxLayout(wid)
        lay1.setContentsMargins(0, 0, 0, 0)
        lay1.setSpacing(5)
        icon =  QtWidgets.QLabel(label)
        pixmap = QtGui.QPixmap(pixmap);
        pixmap = pixmap.scaled(siconSize, siconSize, QtCore.Qt.KeepAspectRatio) 
        icon.setPixmap(pixmap)
        lay1.addWidget(icon)
        lay1.addWidget(label)
        lay.addLayout(lay1)
    currW = widgetInst(wid)
    lay.addWidget(currW)
    wid.setLayout(lay)
    lay.setStretch(0,0)
    lay.setStretch(1,1)
    lay.setSpacing(15)
    layout.addWidget(wid)
    return currW

class QHLine(QtWidgets.QFrame):
    def __init__(self, parent):
        super(QHLine, self).__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)


class QVLine(QtWidgets.QFrame):
    def __init__(self, parent):
        super(QVLine, self).__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.VLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)

class QCustomSlider(QtWidgets.QWidget):
    def __init__(self, sliderOrientation=None):
        super(QCustomSlider, self).__init__()
        self._slider = QtWidgets.QSlider(sliderOrientation)

        self.setLayout(QtWidgets.QVBoxLayout())

        self._labelTicksWidget = QtWidgets.QWidget(self)
        self._labelTicksWidget.setLayout(QtWidgets.QHBoxLayout())
        self._labelTicksWidget.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self._slider)
        self.layout().addWidget(self._labelTicksWidget)

    def setOrientation(self, orientation):
        self._slider.setOrientation(orientation)

    def setTickLabels(self, listWithLabels):
        lengthOfList = range(len(listWithLabels))
        mid = lengthOfList[(len(lengthOfList)-1)//2:(len(lengthOfList)+2)//2]
        defaultAligmens = QtCore.Qt.AlignLeft
        for index, label in enumerate(listWithLabels):
            label = QtWidgets.QLabel(str(label))
            label.setContentsMargins(0, 0, 0, 0)
            if index in mid:
                label.setAlignment(QtCore.Qt.AlignCenter)
                defaultAligmens = QtCore.Qt.AlignRight
            else:
                label.setAlignment(defaultAligmens)
            self._labelTicksWidget.layout().addWidget(label)

    def setRange(self, mini, maxi):
        self._slider.setRange(mini, maxi)

    def setPageStep(self, value):
        self._slider.setPageStep(value)

    def setTickInterval(self, value):
        self._slider.setTickInterval(value)

    def setTickPosition(self, position):
        self._slider.setTickPosition(position)