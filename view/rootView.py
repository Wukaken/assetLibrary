from alQt import QtGui
from alQt import QtCore
    
from . import basisView


class RootView(basisView.BasisView):
    updateDirViewSignal = QtCore.Signal()
    
    def __init__(self, parent=None):
        super(RootView, self).__init__(parent)

    def buildElements(self):
        super(RootView, self).buildElements()
        
        self.label = QtGui.QLabel('Project Root:')
        self.projPathLE = QtGui.QLineEdit()
        self.specBtn = QtGui.QPushButton('Browse')

    def buildWidget(self):
        super(RootView, self).buildWidget()
        
        self.mainLO.setRowStretch(0, 0)
        self.mainLO.addWidget(self.mainFrame)
        
        self.frameLO.addWidget(self.label, 0, 0)
        self.frameLO.addWidget(self.projPathLE, 0, 1)
        self.frameLO.addWidget(self.specBtn, 0, 2)
        self.frameLO.setColumnStretch(0, 0)
        self.frameLO.setColumnStretch(1, 1)
        self.frameLO.setColumnStretch(2, 0)

    def connectFunc(self):
        self.specBtn.clicked.connect(self.browseProjPath)
        self.projPathLE.returnPressed.connect(self.specProjPath)

    def browseProjPath(self):
        oriDir = self.dataCtrl.getDataVal('projectRoot')
        newDir = QtGui.QFileDialog.getExistingDirectory(
            self, "Choose Project Root", oriDir)
        if newDir:
            newDir = newDir.replace('\\', '/')
            updateInfo = {'newProjectRoot': newDir}
            self.dataCtrl.setData(updateInfo)
            self.renewProjPath()

    def specProjPath(self):
        newDir = str(self.projPathLE.text())
        if os.path.isdir(newDir):
            newDir = newDir.replace('\\', '/')
            updateInfo = {'newProjectRoot': newDir}
            self.dataCtrl.setData(updateInfo)
            self.renewProjPath()

    def renewProjPath(self):
        oriProjDir = self.dataCtrl.getDataVal('projectRoot')
        newProjDir = self.dataCtrl.getDataVal('newProjectRoot')
        if newProjDir and not newProjDir == oriProjDir:
            updateInfo = {'projectRoot': newProjDir,
                          'currentDir': newProjDir,
                          'currentDirs': [newProjDir],
                          'currentDirId': 0}
            self.dataCtrl.setData(updateInfo)
            self.initContent()

            self.emitUpdateSignal()

    def initContent(self):
        rootDir = self.dataCtrl.getDataVal('projectRoot')
        self.projPathLE.setText(rootDir)

    def emitUpdateSignal(self):
        self.updateDirViewSignal.emit()
