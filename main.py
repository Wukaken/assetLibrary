import os
from model import mainModel
from control import mainControl


class Main(object):
    def __init__(self, inJson, inDict=None, parent=None, viewInit=1, assignPreset=1):
        self.wid = None
        self.parent = parent
        self.inJson = inJson
        self.inDict = inDict
        self.viewInit = viewInit

        self.mainKey = 'assetLibPreset'
        self.appDir = os.path.join(os.path.expanduser('~'), self.mainKey)
        if not os.path.isdir(self.appDir):
            os.makedirs(self.appDir)

        self.presetJson = os.path.join(self.appDir, '%s.json' % self.mainKey)
        
    def initInfo(self):
        if self.viewInit:
            from view import mainView
            self.wid = mainView.MainView(self.parent)

        self.ctrl = mainControl.MainControl()
        self.dataObj = mainModel.MainModel(
            self.inJson, inData=self.inDict, presetJson=self.presetJson)
        self.ctrl.do(self.wid, self.dataObj)

        mayaInit = 1
        try:
            from maya import cmds
        except:
            mayaInit = 0

        updateInfo = {'mayaInit': mayaInit}
        self.ctrl.setData(updateInfo)

    def do(self):
        self.initInfo()
        self.showUp()

    def showUp(self):
        if self.wid:
            self.wid.do(self.ctrl)
            self.wid.show()
            
    def getWidget(self):
        return self.wid

    def getControl(self):
        return self.ctrl

    def getModel(self):
        return self.dataObj


def buildAssetLibInMaya():
    from maya import OpenMayaUI as omui
    from alQt import QtGui
    ptr = omui.MQtUtil.mainWindow()
    try:
        from shiboken import wrapInstance
    except:
        from shiboken2 import wrapInstance

    name = 'AssetLibraryWindow'
    ptr = omui.MQtUtil.findControl(name)
    if ptr:
        wid = wrapInstance(long(ptr), QtGui.QWidget)
        if not wid.isHidden():
            wid.close()

    mainPtr = omui.MQtUtil.mainWindow()
    parent = wrapInstance(long(mainPtr), QtGui.QWidget)
    m = Main('', {}, parent=parent)
    m.do()


if __name__ == '__main__':
    import sys
    from alQt import QtGui
    
    app = QtGui.QApplication(sys.argv)
    m = Main('', {})
    m.do()
    app.exec_()
