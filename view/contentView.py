try:
    from PySide2 import QtGui
    from PySide2 import QtCore
except:
    from PySide import QtGui
    from PySide import QtCore

import basisView
from functools import partial
import buttonView

class dc(object):
    def __init__(self):
        self.data = {
            #'picFile': '/Users/wujiajian/Desktop/pipeline-1.jpg',
            'picFile': 'D:/a.png',
            'fileName': 'a_sdfadsfefewfwfewecdwcwcwtex.ma',
            'descStr': 'i am a test, i am a test,i am a testi am a test,,i am a testi am a test',
            'fileType': 'Maya Look File',
            'version': 'v001',
            'tipKeys': ['fileName', 'fileType', 'version', 'descStr'],
            'funcKeys': ['', 'efew', 'ereip'],
            'funcInfo': {},
            'outInfoKeys': ['fileName', 'fileType']
        }
        
    def getDataVal(self, key, defVal=None):
        return self.data.get(key, defVal)

    def setData(self, updateInfo):
        self.data.update(updateInfo)


class ContentView(basisView.BasisView):
    def __init__(self, parent=None):
        super(ContentView, self).__init__(parent)

    def buildElements(self):
        self.contLW = QtGui.QListWidget()
        self.verionLW = QtGui.QListWidget()

        #self.contLO = QtGui.QBoxLayout()
        return
        
    def buildWidget(self):
        self.mainLO.addWidget(self.contLW, 0, 0, 10, 5)
        v = buttonView.ButtonView()
        v.do(self.dataCtrl)
        self.mainLO.addWidget(v, 0, 5)
        self.mainLO.addWidget(self.verionLW, 1, 5, 9, 1)
        self.setLayout(self.mainLO)

        self.contLW.setResizeMode(QtGui.QListView.Adjust)
        self.contLW.setSpacing(2)
        self.contLW.setViewMode(QtGui.QListView.IconMode)
        self.contLW.setUniformItemSizes(True)

        self.verionLW.setFixedWidth(200)

    def connectFunc(self):
        self.contLW.itemClicked.connect(self.diao)

    def initContent(self):
        for i in range(5):
            #'''
            #picmap = QtGui.QPixmap()
            #picmap.load('D:/a.png')
            #icon = QtGui.QIcon(picmap)
            #item = QtGui.QListWidgetItem(icon, 'idao')
            item = QtGui.QListWidgetItem()
            item.setSizeHint(QtCore.QSize(200, 220))
            self.contLW.addItem(item)
            #'''
            v = buttonView.ButtonView()
            v.do(self.dataCtrl)
            #self.mainLO.addWidget(v)
            self.contLW.setItemWidget(item, v)
            #'''

    def diao(self, item):
        print item

        popMenu = QtGui.QMenu()
        item.setMenu(popMenu)
        menu.addAction('asdfadf', self.printInfo)

    def printInfo(self):
        print 'getefdsq'

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    ctrl = dc()
    v = ContentView()
    v.do(ctrl)
    v.show()
    app.exec_()        
            
