import os


class BasisControl(object):
    def __init__(self):
        self.widget = None
        self.dataObj = None

    def do(self, widget, dataObj):
        self.initWidget(widget)
        self.initData(dataObj)

    def initWidget(self, widget):
        self.widget = widget

    def initData(self, dataObj):
        self.dataObj = dataObj

    def setData(self, updateInfo):
        if self.dataObj:
            self.dataObj.setDataVal(updateInfo)

    def getDataVal(self, specKey, defVal=None):
        outVal = defVal
        if self.dataObj:
            outVal = self.dataObj.getDataVal(specKey, defVal=defVal)
            
        return outVal
