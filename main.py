import os
from model import basisModel
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
        self.dataObj = basisModel.BasisModel(
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
    ptr = omui.MQtUtil.mainWindow()
    m = Main('', {}, parent=ptr)
    m.do()
    

if __name__ == '__main__':
    try:
        from PySide2 import QtGui
    except:
        from PySide import QtGui
    import sys
    
    app = QtGui.QApplication(sys.argv)
    m = Main('', {})
    m.do()
    app.exec_()
