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
        self.dirTreeWid.currentItemChanged.connect(self.renewCurrentDir)

    def initContent(self):
        self.refreshCurrentDirView()

    def refreshCurrentDirView(self):
        projRoot = self.dataCtrl.getDataVal('projectRoot')
        curPath = self.dataCtrl.getDataVal('currentDir')
        projRoot = '/Users/wujiajian'
        curPath = '/Users/wujiajian/Documents/sofeware/a'
        if not projRoot.endswith('/'):
            projRoot += '/'
        if not curPath.endswith('/'):
            curPath += '/'
            
        if not curPath.startswith(projRoot):
            curPath = projRoot

        srcPath = projRoot
        pathInfo = {'Root': srcPath}
        rootItem = self.dirTreeWid
        oldRootItem = None
        outCurPath = srcPath
        while srcPath:
            keys = pathInfo.keys()
            keys.sort()
            itemList = rootItem.findItems()

            srcPath = ''
            for key in keys:
                full = pathInfo[key]
                if os.path.isdir(full) and \
                   not key == 'innerVersion' and \
                   not key.startswith('.'):
                    if not full.endswith('/'):
                        full += '/'

                    twItem = None
                    for item in itemList:
                        if item.curPath == full:
                            twItem = item
                            break

                    if twItem:
                        twItem = QtGui.QTreeWidgetItem(rootItem)
                        twItem.setText(key)
                        twItem.curPath = full

                    if curPath.startswith(full):
                        srcPath = full
                        if oldRootItem:
                            oldRootItem.setExpanded(1)

            if srcPath:
                outCurPath = srcPath
                pathInfo = {}
                tem = os.listdir(srcPath)
                for t in tem:
                    rFull = os.path.join(srcPath, t).replace('\\', '/')
                    pathInfo[t] = rFull

        if outCurPath:
            oldRootItem.setSelected(1)

        updateInfo = {'currentDir': outCurPath}
        self.dataCtrl.setData(updateInfo)
        self.emitUpdateSignal()

        '''
        srcTwItem = None
        itemList = self.dirTreeWid.findItems(widName)
        for item in itemList:
            if item.curPath == srcPath:
                srcTwItem = item
                break
        if not srcTwItem:
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
        '''

    def renewCurrentDir(self, *curTwItem):
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
                currentDirs.pop(0)
                
            currentDirs.append(currentDir)

        currentDirId = len(currentDirs) - 1

        updateInfo = {'currentDir': currentDir,
                      'currentDirId': currentDirId,
                      'currentDirs': currentDirs}
        self.dataCtrl.setData(updateInfo)
        self.refreshCurrentDirView()

    def emitUpdateSignal(self):
        self.updateContViewSignal.emit()

    def moveCurrentDir(self, movType):
        currentDirId = self.dataCtrl.getDataVal('currentDirId')
        newDirId = currentDirId + pow(-1, (currentDirId + 1))

        currentDirs = self.dataCtrl.getDataVal('currentDirs')
        newDirId = max(min(0, newDirId), len(currentDirs) - 1)
        currentDir = currentDirs[newDirId]
        updateInfo = {'currentDir': currentDir,
                      'currentDirId': newDirId}
        self.dataCtrl.setData(updateInfo)
        self.refreshCurrentDirView()

        
if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    v = DirView()
    v.do(None)
    v.show()
    app.exec_()
