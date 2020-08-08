from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
import os
import resources

def labeledWidget(widgetInst, parent=None, label='', pixmap=None, siconSize=40):
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
    return wid, currW

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

class QCustomSlider(QtWidgets.QSlider):

    def paintEvent(self, event):
        QtWidgets.QSlider.paintEvent(self, event)
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.white))
        rect = self.geometry()
        curr_value = float(self.value()) / self.maximum()
        round_value = round(curr_value, 2)
        font_metrics = QtGui.QFontMetrics(self.font())
        font_height = font_metrics.height()
        horizontal_x_pos = 0
        horizontal_y_pos = rect.height() - font_height-3
        painter.drawText(QtCore.QPoint(horizontal_x_pos, horizontal_y_pos), str(round_value))

        numTicks = (self.maximum() - self.minimum())/self.tickInterval()

        if self.orientation() == QtCore.Qt.Horizontal:
            for i in range(numTicks+1):
                tickX = ((rect.width()/float(numTicks)) * i)
                if tickX >= rect.width():
                    tickX = rect.width()-2
                elif tickX == 0:
                    tickX = 2
                height = 5
                if i==0 or i==numTicks or i==numTicks/2:
                    height = 10
                painter.drawLine(tickX, rect.height(), tickX, rect.height()-height)

class CollapsibleGroup(QtWidgets.QGroupBox):

    def __init__(self, parent, title, iconPath):
        super(CollapsibleGroup, self).__init__(parent)
        mainLay = QtWidgets.QVBoxLayout(self)
        mainLay.setContentsMargins(1, 1, 1, 1)
        titleLay = QtWidgets.QHBoxLayout(self)
        titleLay.setContentsMargins(0, 0, 0, 0)
        self.collapsibleCBx = QtWidgets.QCheckBox()
        self.collapsibleCBx.setChecked(True)
        self.collapsibleCBx.stateChanged.connect(self.diableGroup)
        titleLay.addWidget(self.collapsibleCBx)
        titleWidg, self.title = labeledWidget(QHLine, 
                                            self,
                                            title,
                                            iconPath,
                                            30)
        titleLay.addWidget(titleWidg)
        mainLay.addLayout(titleLay)
        self.centerWidg = QtWidgets.QWidget(self)
        self.centerLay = QtWidgets.QVBoxLayout(self)
        self.centerLay.setContentsMargins(0, 0, 0, 0)
        self.centerLay.setSpacing(0)
        self.centerWidg.setLayout(self.centerLay)
        mainLay.addWidget(self.centerWidg)
        self.setLayout(mainLay)
        st = ""
        stream = QtCore.QFile(':styles/collapsibleGroup.qss')
        if stream.open(QtCore.QFile.ReadOnly):
            st = str(stream.readAll())
            stream.close()
        self.collapsibleCBx.setStyleSheet(st)

        
    def diableGroup(self, value):
        if value:
            self.title.setEnabled(True)
            self.centerWidg.setVisible(True)
        else:
            self.title.setEnabled(False)
            self.centerWidg.setVisible(False)
        self.adjustSize()
        self.window().adjustSize()
        return

    def isChecked(self):
        return self.collapsibleCBx.isChecked()

    def addWidget(self, widget):
        widget.setParent(self.centerWidg)
        self.centerLay.addWidget(widget)

    def setCollapsed(self, value=True):
        self.collapsibleCBx.setChecked(not value)

