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


class MainView(QtGui.QDialog, basisView.BasisView):
    def __init__(self, parent=None):
        super(MainView, self).__init__(parent)

    def do(self, dataCtrl):
        super(MainView, self).do(dataCtrl)

        self.connectSignal()

    def buildElements(self):
        super(MainView, self).buildElements()
        
        self.rootWid = rootView.RootView()

        self.splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)

        self.leftWid = QtGui.QWidget()
        self.dirWid = dirView.DirView()
        self.funcWid = funcView.FuncView()
        self.typeWid = typeView.TypeView()
        
        self.contentWid = contentView.ContentView()
        self.cmpWid = cmpView.CmpView()
        
        self.rootWid.do(self.dataCtrl)
        self.dirWid.do(self.dataCtrl)
        self.funcWid.do(self.dataCtrl)
        self.typeWid.do(self.dataCtrl)
        self.contentWid.do(self.dataCtrl)
        self.cmpWid.do(self.dataCtrl)

    def buildLayout(self):
        super(MainView, self).buildLayout()
        self.leftLO = QtGui.QVBoxLayout()

    def buildWidget(self):
        super(MainView, self).buildWidget()
        
        self.mainLO.addWidget(self.rootWid, 0, 0)
        self.mainLO.addWidget(self.splitter, 1, 0)

        self.leftWid.setLayout(self.leftLO)
        self.leftLO.setSpacing(3)
        self.leftLO.setContentsMargins(4, 2, 4, 4)
        self.leftLO.addWidget(self.dirWid)
        self.leftLO.addWidget(self.funcWid)
        self.leftLO.addWidget(self.typeWid)

        self.splitter.addWidget(self.leftWid)
        self.splitter.addWidget(self.contentWid)
        self.splitter.addWidget(self.cmpWid)

        self.mainLO.setColumnStretch(0, 0)
        self.mainLO.setColumnStretch(1, 1)

    def connectSignal(self):
        self.rootWid.updateDirViewSignal.connect(self.dirWid.initContent)
        self.dirWid.updateContViewSignal.connect(self.contentWid.initContent)
        self.typeWid.updateContViewSignal.connect(self.contentWid.initContent)

    def closeEvent(self, qevent):
        if self.dataCtrl:
            self.dataCtrl.outputPresetDataFile()
