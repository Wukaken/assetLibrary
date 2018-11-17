import os
try:
    from PySide2 import QtGui
    from PySide2 import QtCore
except:
    from PySide import QtGui
    from PySide import QtCore
    
from . import basisView


class RootView(basisView.BasisView):
    updateDirViewSignal = QtCore.Signal()
    
    def __init__(self, parent=None):
        super(RootView, self).__init__(parent)

    def buildElements(self):
        self.label = QtGui.QLabel('Project Root:')
        self.projPathLE = QtGui.QLineEdit()
        self.specBtn = QtGui.QPushButton('Browse')

    def buildWidget(self):
        self.mainLO.addWidget(self.label, 0, 0)
        self.mainLO.addWidget(self.projPathLE, 0, 1, 1, 2)
        self.mainLO.addWidget(self.specBtn, 0, 3)

        self.setLayout(self.mainLO)

    def connectFunc(self):
        self.specBtn.clicked.connect(self.specProjPath)

    def specProjPath(self):
        defaultDir = os.path.expanduser('~')
        oriDir = self.dataCtrl.getDataVal(
            'projectRoot', defaultDir)
        newDir = QtGui.QFileDialog.getExistingDirectory(
            self, "Choose Project Root", oriDir)
        newDir = newDir.replace('\\', '/')
        if os.path.isdir(newDir) and not newDir == oriDir:
            updateInfo = {'projectRoot': newDir}
            self.dataCtrl.setData(updateInfo)

            self.initContent()

            self.emitUpdateSignal()

    def initContent(self):
        rootDir = self.dataCtrl.getDataVal('projectRoot')
        self.projPathLE.setText(rootDir)

    def emitUpdateSignal(self):
        self.updateDirViewSignal.emit()
