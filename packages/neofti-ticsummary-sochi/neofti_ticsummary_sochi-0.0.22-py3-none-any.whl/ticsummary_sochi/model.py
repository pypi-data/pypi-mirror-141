from ticsummary_sochi.ui.mainWindow import *
from ticsummary_sochi.readerCSV import *
from ticsummary_sochi.handlerData import *
from ticsummary_sochi.readerFiles import *
from ticsummary_sochi.dataWriter import *
import os 


class Model():
    def __init__(self):
        self.mainWindow = MainWindow()
        self.mainWindow.show()
        self.mainWindow.ui.pushButtonOpenFolder.clicked.connect(self.openFolder)
        self.mainWindow.ui.comboBoxListFiles.currentIndexChanged.connect(self.setIndexData)
        self.mainWindow.ui.pushButtonExportData.clicked.connect(self.exportData)
    def openFolder(self):
        path = self.mainWindow.showExistingFolderDialog(os.curdir)
        if (path !=""):
            self.path = path
            self.filesList = readListFilesInFolder(self.path)
            self.mainWindow.setFileLists(self.filesList)
            self.mainWindow.setMode(ModeInterface.OPENFOLDER)
            self.mainWindow.setPath(path)
    def setIndexData(self, id:int):
        resultRead = readCSV("{0}/{1}".format(self.path, self.filesList[id]))
        
        self.resultProcess = processDataByMatrix(resultRead.matrix,resultRead.timeSlice)
        
        self.mainWindow.setDataMCP(self.resultProcess.mcp,self.resultProcess.time[1])  
        self.mainWindow.setDataCounter(self.resultProcess.scRightUp,self.resultProcess.scLeftUp,self.resultProcess.scRightBottom,self.resultProcess.scLeftBottom,self.resultProcess.scCenter,self.resultProcess.time)
    def exportData(self):
        fileName = self.mainWindow.getSaveFile()
        if fileName != '': writeData('{0}.csv'.format(fileName), self.resultProcess)