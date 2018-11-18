try:
    from PySide2 import QtGui
    from PySide2 import QtCore
except:
    from PySide import QtGui
    from PySide import QtCore

import basisView
from functools import partial


class TypeView(basisView.BasisView):
    updateContViewSignal = QtCore.Signal()
    
    def __init__(self, parent=None):
        super(TypeView, self).__init__(parent)
        self.labelWidInfo = {}

    def buildElements(self):
        super(TypeView, self).buildElements()
        self.typeLW = QtGui.QListWidget()
        self.chkOnBtn = QtGui.QPushButton('Check On All')
        self.chkOffBtn = QtGui.QPushButton('Check Off All')

    def buildWidget(self):
        super(TypeView, self).buildWidget()

        self.mainLO.addWidget(self.mainFrame)
        
        self.frameLO.addWidget(self.titleLabel, 0, 0, 1, 2, self.centerAlign)
        self.frameLO.addWidget(self.typeLW, 1, 0, 1, 2)
        self.frameLO.addWidget(self.chkOnBtn, 2, 0)
        self.frameLO.addWidget(self.chkOffBtn, 2, 1)

    def connectFunc(self):
        self.chkOnBtn.clicked.connect(partial(self.checkStateChange, 1))
        self.chkOnBtn.clicked.connect(partial(self.checkStateChange, 0))

    def initContent(self):
        self.titleLabel.setText('File Type Filter')
        fileTypes = self.dataCtrl.getDataVal('fileTypes')
        activeFileTypes = self.dataCtrl.getDataVal('activeFileTypes')
        print fileTypes
        print activeFileTypes
        for fileType in fileTypes:
            item = QtGui.QListWidgetItem()
            ftCb = QtGui.QCheckBox(fileType, parent=self)
            if fileType in activeFileTypes:
                ftCb.setChecked(2)

            self.typeLW.addItem(item)
            self.typeLW.setItemWidget(item, ftCb)
            item.setToolTip('FileType: %s' % fileType)

            ftCb.stateChanged.connect(self.typeChangeFunc)

    def typeChangeFunc(self, i):
        itemCount = self.typeLW.count()
        curActiveFileTypes = []
        for i in range(itemCount):
            print i
            item = self.typeLW.item(i)
            cbWid = self.typeLW.itemWidget(item)
            if cbWid.isChecked():
                fileType = str(cbWid.text())
                print fileType
                curActiveFileTypes.append(fileType)

        oriActiveFileTypes = self.dataCtrl.getDataVal('activeFileTypes', [])
        print curActiveFileTypes
        print oriActiveFileTypes
        print 'diao'
        if set(oriActiveFileTypes) == set(curActiveFileTypes):
            updateInfo = {'activeFileTypes': curActiveFileTypes}
            self.dataCtrl.setData(updateInfo)
            
            self.dataCtrl.genFileContentInfo()
            self.emitUpdateSignal()

    def emitUpdateSignal(self):
        self.updateContViewSignal.emit()

    def checkStateChange(self, chkState):
        itemCount = self.typeLW.count()
        for i in range(itemCount):
            item = self.typeLW.item(i)
            cbWid = self.typeLW.itemWidget(item)
            cbWid.setChecked(chkState)
