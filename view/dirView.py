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

class dc(object):
    def __init__(self):
        self.data = {
            'projectRoot': '/Users/wujiajian',
            'currentDir': '/Users/wujiajian/Documents/sofeware/a'
        }
        
    def getDataVal(self, key, defVal=None):
        return self.data.get(key, defVal)

    def setData(self, updateInfo):
        self.data.update(updateInfo)

class DirView(basisView.BasisView):
    updateContViewSignal = QtCore.Signal()
    
    def __init__(self, parent=None):
        super(DirView, self).__init__(parent)

    def buildElements(self):
        super(DirView, self).buildElements()
        
        self.backwardBtn = QtGui.QPushButton('<-')
        self.forwardBtn = QtGui.QPushButton('->')
        self.dirTreeWid = QtGui.QTreeWidget(parent=self)
        self.selModel = self.dirTreeWid.selectionModel()

    def buildWidget(self):
        super(DirView, self).buildWidget()

        self.mainLO.addWidget(self.mainFrame)
        
        self.frameLO.addWidget(self.backwardBtn, 0, 0)
        self.frameLO.addWidget(self.forwardBtn, 0, 1)
        self.frameLO.addWidget(self.dirTreeWid, 1, 0, 10, 2)

        self.dirTreeWid.setHeaderHidden(1)
        self.dirTreeWid.setMinimumHeight(200)

        self.frameLO.setRowStretch(0, 0)
        self.frameLO.setRowStretch(1, 0)
        
        # self.setFixedWidth(250)

    def connectFunc(self):
        self.backwardBtn.clicked.connect(partial(self.moveCurrentDir, 1))
        self.forwardBtn.clicked.connect(partial(self.moveCurrentDir, 0))
        self.dirTreeWid.itemClicked.connect(self.renewCurrentDir)

    def initContent(self):
        self.refreshCurrentDirView()

    def refreshCurrentDirView(self):
        projRoot = self.dataCtrl.getDataVal('projectRoot')
        curPath = self.dataCtrl.getDataVal('currentDir')

        if not projRoot.endswith('/'):
            projRoot += '/'
        if not curPath.endswith('/'):
            curPath += '/'
            
        if not curPath.startswith(projRoot):
            curPath = projRoot

        self.selModel.clearSelection()
        srcPath = projRoot
        pathInfo = {'Root': srcPath}
        rootItem = self.dirTreeWid
        oldRootItem = None
        outCurPath = srcPath
        while srcPath:
            keys = pathInfo.keys()
            keys.sort()
            itemList = []
            if isinstance(rootItem, QtGui.QTreeWidget):
                topNum = rootItem.topLevelItemCount()
                for i in range(topNum):
                    item = rootItem.topLevelItem(i)
                    itemList.append(item)
            else:
                chdNum = rootItem.childCount()
                for i in range(chdNum):
                    item = rootItem.child(i)
                    itemList.append(item)

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

                    if not twItem:
                        twItem = QtGui.QTreeWidgetItem(rootItem)
                        twItem.setText(0, key)
                        twItem.curPath = full

                    if curPath.startswith(full):
                        srcPath = full
                        if oldRootItem:
                            oldRootItem.setExpanded(1)

                        oldRootItem = twItem

            if srcPath:
                rootItem = oldRootItem
                outCurPath = srcPath
                pathInfo = {}
                tem = os.listdir(srcPath)
                for t in tem:
                    rFull = os.path.join(srcPath, t).replace('\\', '/')
                    pathInfo[t] = rFull

        if oldRootItem:
            oldRootItem.setSelected(1)

        updateInfo = {'currentDir': outCurPath}
        self.dataCtrl.setData(updateInfo)
        self.emitUpdateSignal()

    def renewCurrentDir(self, curTwItem, actId):
        if not curTwItem:
            return
        
        currentDir = curTwItem.curPath
        oriCurrentDir = self.dataCtrl.getDataVal('currentDir')
        currentDirs = self.dataCtrl.getDataVal('currentDirs', [oriCurrentDir])
        
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
        newDirId = currentDirId + pow(-1, movType)
        
        currentDirs = self.dataCtrl.getDataVal('currentDirs')
        newDirId = min(max(0, newDirId), len(currentDirs) - 1)

        currentDir = currentDirs[newDirId]
        updateInfo = {'currentDir': currentDir,
                      'currentDirId': newDirId}

        self.dataCtrl.setData(updateInfo)
        self.refreshCurrentDirView()

        
if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    ctrl = dc()
    v = DirView()
    v.do(ctrl)
    v.show()
    app.exec_()
