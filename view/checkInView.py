from alQt import QtGui
from alQt import QtCore

import cmpView
import basisView


class CheckInView(QtGui.QDialog, basisView.BasisView):
    updateContViewSignal = QtCore.Signal()
    
    def __init__(self, parent=None):
        super(CheckInView, self).__init__(parent)

    def buildElements(self):
        super(CheckInView, self).buildElements()

        self.diffLabel = QtGui.QLabel('Compare Different:')
        self.cmpView = cmpView.CmpView()
        self.cmpView.do(self.dataCtrl)

        self.nextBtn = QtGui.QPushButton('Next')

        self.descLabel = QtGui.QLabel('Description:')
        self.picLabel = QtGui.QLabel()
        self.picmap = QtGui.QPixmap()
        self.descTE = QtGui.QTextEdit()
        self.screenBtn = QtGui.QPushButton('Screen Shot')
        self.publishBtn = QtGui.QPushButton('Publish')

    def buildWidget(self):
        super(CheckInView, self).buildWidget()

        self.mainLO.addWidget(self.diffLabel, 0, 0, 1, 2, self.centerAlign)
        self.mainLO.addWidget(self.cmpView, 1, 0, 1, 2)
        self.mainLO.addWidget(self.nextBtn, 2, 1)
        
        self.picLabel.setFixedSize(300, 225)

        self.setWindowTitle('Check in Window')

    def connectFunc(self):
        self.nextBtn.clicked.connect(self.renewWidget)
        self.screenBtn.clicked.connect(self.takeScreenShot)
        self.publishBtn.clicked.connect(self.publishFile)

    def renewWidget(self):
        self.diffLabel.hide()
        self.diffLabel.close()
        self.cmpView.hide()
        self.cmpView.close()
        self.nextBtn.hide()
        self.nextBtn.close()

        self.mainLO.addWidget(self.descLabel, 0, 0, 1, 2, self.centerAlign)
        self.mainLO.addWidget(self.picLabel, 1, 0)
        self.mainLO.addWidget(self.descTE, 1, 1)
        self.mainLO.addWidget(self.screenBtn, 2, 0)
        self.mainLO.addWidget(self.publishBtn, 2, 1)

    def initCmpContent(self, diffInfo):
        self.cmpView.initCmpContent(diffInfo)

    def takeScreenShot(self):
        temPic = self.dataCtrl.takeCurrentAppScreenShot()
        updateInfo = {'outputTemPic': temPic}
        self.dataCtrl.setData(updateInfo)
        
        self.picmap.load(temPic)
        self.picLabel.setPixmap(self.picmap)
        self.picLabel.setScaledContents(1)

    def publishFile(self):
        desc = str(self.descTE.toPlainText())
        temPic = self.dataCtrl.getDataVal('outputTemPic', '')
        updateInfo = {'outputDescStr': desc,
                      'outputTemPic': temPic}
        self.dataCtrl.setData(updateInfo)
        self.dataCtrl.checkInFile()
        self.buildUpNotificationView()
        self.emitUpdateContentViewSignal()
        self.close()

    def emitUpdateContentViewSignal(self):
        self.updateContViewSignal.emit()
        
    def buildUpNotificationView(self):
        checkInOutputInfo = self.dataCtrl.getDataVal('checkInOutputInfo')
        subject = checkInOutputInfo['subject']
        mess = checkInOutputInfo['mess']
        QtGui.QMessageBox.warning(self, subject, mess)

    def closeEvent(self, qevent):
        self.clearCheckInData()

    def clearCheckInData(self):
        updateInfo = {'outputTemFile': '',
                      'outputTemPic': '',
                      'outputDetailInfo': {},
                      'outputFileName': '',
                      'checkInOutputInfo': {}}
        self.dataCtrl.setData(updateInfo)

    def reject(self):
        self.clearCheckInData()
        super(CheckInView, self).reject()
