try:
    from PySide2 import QtGui
    from PySide2 import QtCore
except:
    from PySide import QtGui
    from PySide import QtCore

from . import basisView
from . import cmpView
from . import contentView
from . import dirView
from . import funcView
from . import rootView
from . import typeView


class MainView(basisView.BasisView):
    def __init__(self, parent=None):
        super(MainView, self).__init__(parent)

    def do(self, dataCtrl):
        super(MainView, self).do(dataCtrl)

        self.connectSignal()

    def buildElements(self):
        projRoot = self.dataCtrl.getDataVal('projectRoot')
        curPath = self.dataCtrl.getDataVal('currentDir')
        print projRoot
        print curPath
        self.rootWid = rootView.RootView()
        self.dirWid = dirView.DirView()
        self.funcWid = funcView.FuncView()
        self.typeView = typeView.TypeView()
        self.contentView = contentView.ContentView()
        self.cmpView = cmpView.CmpView()

        self.rootWid.do(self.dataCtrl)
        self.dirWid.do(self.dataCtrl)
        self.funcWid.do(self.dataCtrl)
        self.typeView.do(self.dataCtrl)
        self.contentView.do(self.dataCtrl)
        self.cmpView.do(self.dataCtrl)

    def buildWidget(self):
        self.mainLO.addWidget(self.rootWid, 0, 0, 1, 4)
        
        self.mainLO.addWidget(self.dirWid, 10, 0)
        self.mainLO.addWidget(self.funcWid, 11, 0)
        self.mainLO.addWidget(self.typeWid, 12, 0)
        self.mainLO.addWidget(self.contentView, 10, 1, 1, 3)
        self.mainLO.addWidget(self.cmpView, 10, 3, 2, 3)

    def connectFunc(self):
        return

    def initContent(self):
        return

    def connectSignal(self):
        return
        #self.rootObj.updateDirViewSignal.connect(self.dirObj.initContent)
        #self.dirObj.updateContViewSignal.connect(self.contObj.initContent)

    def closeEvent(self, qevent):
        if self.dataCtrl:
            self.dataCtrl.outputPresetDataFile()
