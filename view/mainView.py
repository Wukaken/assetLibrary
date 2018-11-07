try:
    from PySide2 import QtGui
    from PySide2 import QtCore
except:
    from PySide import QtGui
    from PySide import QtCore

from . import basisView    
from . import rootView    
from . import dirView
from . import contentView
from . import funcView

    
class MainView(basisView.BasisView):
    def __init__(self, parent=None):
        super(MainView, self).__init__(parent)

    def do(self, dataCtrl):
        super(MainView, self).do(dataCtrl)

        self.connectSignal()

    def buildElements(self):
        self.rootObj = rootView.RootView()
        self.dirObj = dirView.DirView()
        self.contObj = contentView.ContentView()
        self.funcObj = funcView.FuncView()
        
        self.rootObj.do()
        self.dirObj.do()
        self.contObj.do()
        self.funcObj.do()

    def buildWidget(self):
        self.mainLO.addWidget(self.rootObj.getMainWid(), 0, 0, 1, 4)
        self.mainLO.addWidget(self.dirObj.getMainWid(), 10, 0)
        self.mainLO.addWidget(self.contObj.getMainWid(), 10, 1, 31, 3)
        self.mainLO.addWidget(self.funcObj.getMainWid(), 30, 1, 1, 1)

    def connectFunc(self):
        return

    def initContent(self):
        return

    def connectSignal(self):
        self.rootObj.updateDirViewSignal.connect(self.dirObj.initContent)
        self.dirObj.updateContViewSignal.connect(self.contObj.initContent)

    def closeEvent(self, qevent):
        if self.dataCtrl:
            self.dataCtrl.outputPresetDataFile()
