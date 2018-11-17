import os
from model import basisModel
from control import basisControl


class Main(object):
    def __init__(self, inJson, inDict=None, parent=None, viewInit=1, assignPreset=1):
        self.wid = None
        self.parent = parent
        self.inJson = inJson
        self.inDict = inDict
        self.viewInit = viewInit

        self.appDir = os.path.join(os.path.expanduser('~'), 'assetLib')
        if not os.path.isdir(self.appDir):
            os.makedirs(self.appDir)
        
    def initInfo(self):
        if self.viewInit:
            from view import mainView
            self.wid = mainView.MainView(self.parent)

        self.ctrl = basisControl.BasisControl()
        self.dataObj = basisModel.BasisModel(self.inJson, self.inDict)
        self.ctrl.do(self.wid, self.dataObj)

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
