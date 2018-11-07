import os
try:
    from PySide2 import QtGui
    from PySide2 import QtCore
except:
    from PySide import QtGui
    from PySide import QtCore

# from . import basisView
import basisView
from functools import partial

class DirView(basisView.BasisView):
    updateContViewSignal = QtCore.Signal()
    
    def __init__(self, parent=None):
        super(DirView, self).__init__(parent)

    def do(self, dataCtrl):
        super(DirView, self).do(dataCtrl)

    def buildElements(self):
        self.forwardBtn = QtGui.QPushButton('Forward')
        self.backwardBtn = QtGui.QPushButton('Backward')
        self.dirTreeWid = QtGui.QTreeWidget(parent=self)

    def buildWidget(self):
        self.mainLO.addWidget(self.forwardBtn, 0, 0)
        self.mainLO.addWidget(self.backwardBtn, 0, 1)
        self.mainLO.addWidget(self.dirTreeWid, 10, 0, 10, 2)

        self.setLayout(self.mainLO)

    def connectFunc(self):
        self.forwardBtn.clicked.connect(partial(self.moveCurrentDir, 0))
        self.backwardBtn.clicked.connect(partial(self.moveCurrentDir, 1))
        self.dirTreeWid.currentItemChanged.connect(self.refreshCurrentDir)

    def initContent(self):
        projRoot = self.dataCtrl.getDataVal('projectRoot')
        curPath = self.dataCtrl.gentDataVal('currentDir')
        projRoot = '/Users/wujiajian'
        curPath = '/Users/wujiajian/Documents/sofeware/a'
        if not projRoot.endswith('/'):
            projRoot += '/'
        if not curPath.endswith('/'):
            curPath += '/'
            
        if not curPath.startswith(projRoot):
            curPath = projRoot

        srcPath = projRoot
        widName = 'Root'
        srcTwItem = QtGui.QTreeWidgetItem(self.dirTreeWid)
        srcTwItem.setText(0, widName)
        srcTwItem.curPath = projRoot
        outCurPath = ''
        while srcPath:
            tem = os.listdir(srcPath)
            expand = 0
            outTwItem = None
            outPath = ''
            for t in tem:
                full = os.path.join(srcPath, t).replace('\\', '/')
                if os.path.isdir(full) and \
                   not t == 'innerVersion' and \
                   not t.startswith('.'):
                    expand = 1
                    if not full.endswith('/'):
                        full += '/'

                    twItem = QtGui.QTreeWidgetItem(srcTwItem)
                    twItem.setText(0, t)
                    twItem.curPath = full
                    if curPath.startswith(full):
                        outTwItem = twItem
                        outPath = full

            if expand:
                srcTwItem.setExpanded(1)

            if outPath:
                srcPath = outPath
                srcTwItem = outTwItem
                outCurPath = srcPath
            else:
                srcPath = ''

        updateInfo = {'currentDir': outCurPath}
        self.dataCtrl.setData(updateInfo)

        self.emitUpdateSignal()

    def emitUpdateSignal(self):
        self.updateContViewSignal.emit()

    def moveCurrentDir(self, movType):
        currentDir = self.dataCtrl.getDataVal('currentDir')
        currentDirs = self.dataCtrl.getDataVal('currentDirs', [currentDir])
        currentDirId = self.dataCtrl.getDataVal('currentDirId', 0)

        if movType == 0:
            currentDirId = max(0, currentDirId - 1)
        else:
            currentDirId = min(max(0, len(currentDirs) - 1), currentDirId + 1)

        currentDir = currentDirs[currentDirId]
        updateInfo = {'currentDir': currentDir,
                      'currentDirId': currentDirId}
        self.dataCtrl.setData(updateInfo)

    def refreshCurrentDir(self, *curTwItem):
        if not curTwItem:
            return
        
        currentDir = curTwItem.curPath
        currentDirs = self.dataCtrl.getDataVal('currentDirs')
        
        if currentDir in currentDirs:
            curId = currentDirs.index(currentDir)
            currentDirs.pop(curId)
            currentDirs.append(currentDir)
        else:
            if len(currentDirs) >= 10:
                currentDirs.pop()
                
            currentDirs.append(currentDir)

        updateInfo = {'currentDir': currentDir,
                      'currentDirs': currentDirs}
        self.dataCtrl.setData(updateInfo)

        self.refreshCurrentDirView(curTwItem)

    def refreshCurrentDir(self, curTwItem):
        currentDir = self.dataCtrl.getDataVal('currentDir')
        if not os.path.isdir(currentDir):
            currentDirs = self.dataCtrl.getDataVal('currentDirs')
            currentDirs.pop()
            currentDir = currentDirs[-1]

            updateInfo = {'currentDir': currentDir,
                          'currentDirs': currentDirs}
            self.dataCtrl.setData(updateInfo)
            self.refreshCurrentDir()
            

        
        
        
        

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    v = DirView()
    v.do(None)
    v.show()
    app.exec_()
