try:
    from PySide2 import QtGui
    from PySide2 import QtCore
except:
    from PySide import QtGui
    from PySide import QtCore

import basisView
import checkInView


class FuncView(basisView.BasisView):
    updateContViewSignal = QtCore.Signal()
    
    def __init__(self, parent=None):
        super(FuncView, self).__init__(parent)

    def buildElements(self):
        super(FuncView, self).buildElements()
        self.ftLabel = QtGui.QLabel('File Type:')
        self.ftCB = QtGui.QComboBox()

        self.fnLabel = QtGui.QLabel('File Name:')
        self.fnLE = QtGui.QLineEdit()
        self.autoCfgBtn = QtGui.QPushButton('Auto Config')

        self.mailLabel = QtGui.QLabel('Mail List:')
        self.mailTE = QtGui.QTextEdit()
        self.chkInBtn = QtGui.QPushButton('Check In')

        self.setMlBtn = QtGui.QPushButton('Set Mail List')

    def buildWidget(self):
        super(FuncView, self).buildWidget()
        self.mainLO.addWidget(self.mainFrame)
        
        self.frameLO.addWidget(self.titleLabel, 0, 0, 1, 2, self.centerAlign)
        
        self.frameLO.addWidget(self.ftLabel, 1, 0)
        self.frameLO.addWidget(self.ftCB, 1, 1, 1)

        self.frameLO.addWidget(self.fnLabel, 2, 0)
        self.frameLO.addWidget(self.fnLE, 2, 1)

        self.frameLO.addWidget(self.chkInBtn, 3, 0)
        self.frameLO.addWidget(self.autoCfgBtn, 3, 1)

        self.frameLO.addWidget(self.mailLabel, 4, 0, self.centerAlign)
        self.frameLO.addWidget(self.setMlBtn, 4, 1)
        self.frameLO.addWidget(self.mailTE, 5, 0, 3, 2)

        self.frameLO.setRowStretch(4, 1)
        self.titleLabel.setText('Function')

    def connectFunc(self):
        self.setMlBtn.clicked.connect(self.renewMailList)
        self.autoCfgBtn.clicked.connect(self.autoConfig)
        self.ftCB.currentIndexChanged.connect(self.renewFileType)
        self.chkInBtn.clicked.connect(self.checkInFile)

    def initContent(self):
        fileTypes = self.dataCtrl.getDataVal('fileTypes')
        fileType = self.dataCtrl.getDataVal('fileType')
        self.ftCB.addItems(fileTypes)
        ftId = 0
        if fileType in fileTypes:
            ftId = fileTypes.index(fileType)
            
        self.ftCB.setCurrentIndex(ftId)

        mailList = self.dataCtrl.getDataVal('mailList', [])
        mailStr = '\n'.join(mailList)
        self.mailTE.setText(mailStr)
        '''
        mayaInit = self.dataCtrl.getDataVal('mayaInit')
        if not mayaInit:
            self.chkInBtn.setEnabled(0)
        '''

    def renewMailList(self):
        mailStr = self.mailTE.toPlainText()
        mailList = []
        if '\r\n' in mailStr:
            mailList = mailStr.split('\r\n')
        else:
            mailList = mailStr.split('\n')

        updateInfo = {'mailList': mailList}
        self.dataCtrl.setData(updateInfo)

    def autoConfig(self):
        detailFileName = self.dataCtrl.getDataVal('detailFileName')
        detailFileType = self.dataCtrl.getDataVal('detailFileType')
        if not detailFileName or not detailFileType:
            return
        
        fileTypes = self.dataCtrl.getDataVal('fileTypes')
        fileTypeId = fileTypes.index(detailFileType)
        self.fnLE.setText(detailFileName)
        self.ftCB.setCurrentIndex(fileTypeId)

    def renewFileType(self, ftId):
        fileType = str(self.ftCB.itemText(ftId))
        updateInfo = {'fileType': fileType}
        self.dataCtrl.setData(updateInfo)

    def checkInFile(self):
        outputFileName = str(self.fnLE.text())
        outputFileType = str(self.ftCB.currentText())
        updateInfo = {'outputFileName': outputFileName,
                      'outputFileType': outputFileType}
        self.dataCtrl.setData(updateInfo)

        rec = self.dataCtrl.validOutputCheck()
        status = rec[0]
        if status:
            mess = rec[1]
            self.buildUpCheckInFailView(mess)
        else:
            diffInfo = self.dataCtrl.doCheckInCompare()
            self.buildUpCheckInView(diffInfo)
        
    def buildUpCheckInFailView(self, mess):
        title = 'Check In Error'
        QtGui.QMessageBox.warning(self, title, mess)

    def buildUpCheckInView(self, diffInfo):
        ciV = checkInView.CheckInView(self)
        ciV.do(self.dataCtrl)
        ciV.setWindowModality(QtCore.Qt.ApplicationModal)

        ciV.updateContViewSignal.connect(self.emitUpdateContentViewSignal)
        ciV.show()

    def emitUpdateContentViewSignal(self):
        self.updateContViewSignal.emit()
