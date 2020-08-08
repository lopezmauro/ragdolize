from ui import ragdolize_win
import sys
from pySide import QtGui
app = QtGui.QApplication(sys.argv)
widg = ragdolize_win.RagdolizeUI()
widg.show()
sys.exit(app.exec_())