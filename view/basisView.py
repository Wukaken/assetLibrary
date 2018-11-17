try:
    from PySide2 import QtGui
    from PySide2 import QtCore
except:
    from PySide import QtGui
    from PySide import QtCore

class BasisView(QtGui.QDialog):
    def __init__(self, parent=None):
        super(BasisView, self).__init__(parent)
        self.dataCtrl = None

    def getMainWid(self):
        return self

    def do(self, dataCtrl):
        self.initCtrl(dataCtrl)

        self.buildElements()
        self.buildLayout()
        self.buildWidget()

        self.connectFunc()
        self.initContent()

    def initCtrl(self, dataCtrl):
        self.dataCtrl = dataCtrl

    def buildElements(self):
        self.mainFrame = QtGui.QFrame()
        self.titleLabel = QtGui.QLabel()
        self.centerAlign = QtCore.Qt.Alignment(4)

    def buildLayout(self):
        self.mainLO = QtGui.QGridLayout()
        self.frameLO = QtGui.QGridLayout()

    def buildWidget(self):
        self.setLayout(self.mainLO)
        self.mainFrame.setFrameShape(QtGui.QFrame.Box)
        self.mainFrame.setLayout(self.frameLO)
        self.mainLO.setSpacing(3)
        self.mainLO.setContentsMargins(4, 2, 4, 4)
        self.frameLO.setSpacing(3)
        self.frameLO.setContentsMargins(3, 2, 3, 4)

    def connectFunc(self):
        return

    def initContent(self):
        return
