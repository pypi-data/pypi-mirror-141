from PyQt6 import QtCore, QtGui, QtWidgets
from enum import Enum
import pyqtgraph as pg
from pyqtgraph.dockarea import DockArea, Dock
from ticsummary_sochi.ui.settingsColorBarDialog import *
import numpy as np
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutCentral = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayoutCentral.setObjectName("verticalLayoutCentral")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEditFolder = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditFolder.setObjectName("lineEditFolder")
        self.lineEditFolder.setReadOnly(True)
        self.horizontalLayout.addWidget(self.lineEditFolder)
        self.pushButtonOpenFolder = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonOpenFolder.setObjectName("pushButtonOpenFolder")
        self.horizontalLayout.addWidget(self.pushButtonOpenFolder)
        self.comboBoxListFiles = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxListFiles.setMinimumSize(QtCore.QSize(200, 0))
        self.comboBoxListFiles.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.NoInsert)
        self.comboBoxListFiles.setObjectName("comboBoxListFiles")
        self.horizontalLayout.addWidget(self.comboBoxListFiles)
        self.pushButtonExportData = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonExportData.setObjectName("pushButtonExportData")
        self.horizontalLayout.addWidget(self.pushButtonExportData)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayoutCentral.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Folder"))
        self.pushButtonOpenFolder.setText(_translate("MainWindow", "..."))
        self.pushButtonExportData.setText(_translate("MainWindow", "Export"))

class ModeInterface(Enum):
    DEFFAULT = (False,True,True,False,False)
    OPENFOLDER = (True,True,True,True,True)
    
    def __init__(self, plotEnabled:bool, lineEditEnabled:bool, pushButtonOpenFolderEnabled:bool, comboBoxListFilesEnabled:bool, pushButtonExportEnabled:bool):
        self.plotEnabled = plotEnabled
        self.lineEditEnabled = lineEditEnabled
        self.pushButtonOpenFolderEnabled = pushButtonOpenFolderEnabled
        self.comboBoxListFilesEnabled = comboBoxListFilesEnabled
        self.pushButtonExportEnabled = pushButtonExportEnabled

class ColorBarItemWithDoubleClick(pg.ColorBarItem):
    def __init__(self, *args, **kwargs):
        pg.ColorBarItem.__init__(self, *args, **kwargs)
        self.autoscale = True
        # creating a mouse double click event
    def mouseDoubleClickEvent(self, e):
        self.settingsDialog = SettingsColorBarDialog(*self.levels(),self.cmap.name,self.autoscale,self.__setNewparameter__)
        self.settingsDialog.show()
    def __setNewparameter__(self,max,min,cmapstr,autoscale):
        cmap = pg.colormap.get(cmapstr)
        self.setCmap(cmap)
        self._update_items()
        self.maxUser = max
        self.minUser = min
        self.autoscale=autoscale
        if autoscale:
            self.setLevels(values=(self.minImage,self.maxImage))
        else:
            self.setLevels(values=(min,max))
    def setMaxMinImage(self,min,max):
        self.minImage = min
        self.maxImage = max
        if self.autoscale:
            self.setLevels(values=(self.minImage,self.maxImage))
        else:
            self.setLevels(values=(self.minUser,self.maxUser))

class MainWindow():
    def __init__(self):
        self.mainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.mainWindow)
        
        self.labelAxisStyle = {'color': '#FFF', 'font-size': '14pt'}
        self.titlePlotStyle = {'color': '#FFF', 'font-size': '20pt'}
        
        self.dockAreaChart = DockArea()
        
        d1 = Dock("MCP profile", size=(1, 1))     ## give this dock the minimum possible size
        d2 = Dock("Counter line", size=(1, 1))
        d3 = Dock("Counter value", size=(1, 1))
        
        self.dockAreaChart.addDock(d1,"left")
        self.dockAreaChart.addDock(d2,"right")
        self.dockAreaChart.addDock(d3,"right",d2)
        self.dockAreaChart.moveDock(d2,"above",d3)
        
        self.layoutPlot = pg.GraphicsLayoutWidget(show=True)
        d1.addWidget(self.layoutPlot)
        self.colorMapPlot:pg.PlotItem = self.layoutPlot.addPlot(row=0,col=1,rowspan=1,colspan=1)
        self.intensityMapLinePlot = self.layoutPlot.addPlot(row=1,col=1,rowspan=1,colspan=1)
        self.intensityMapLinePlot.setXLink(self.colorMapPlot)
        self.intensityMapLinePlot.setMouseEnabled(False,False)
        self.projectionMapHistPlot:pg.PlotItem = self.layoutPlot.addPlot(row=0,col=2,rowspan=1,colspan=1)
        self.projectionMapHistPlot.setMouseEnabled(False,False)
        self.colorMapPlot.setYLink(self.projectionMapHistPlot)
        self.projectionMapHistPlot.setFixedWidth(150)
        self.histogramItem = pg.BarGraphItem(x0 = 0, y = (), height = 0.6, width=(), brush ='g')
        self.projectionMapHistPlot.addItem(self.histogramItem)
        self.cmap = pg.colormap.get('CET-L8')
        self.bar = ColorBarItemWithDoubleClick(
            interactive=True, colorMap=self.cmap)
        self.bar.setFixedWidth(40)
        font=QtGui.QFont()
        font.setPixelSize(10)
        self.colorMapPlot.getAxis("bottom").setTickFont(font)
        self.colorMapPlot.getAxis("left").setTickFont(font)
        self.colorMapPlot.getAxis("left").setWidth(70)
        self.bar.getAxis("right").setTickFont(font)
        self.image = pg.ImageItem()
        self.bar.setImageItem(self.image)
        self.colorMapPlot.addItem(self.image)
        self.layoutPlot.addItem(self.bar,0,0,2,1)
        self.setLabelPlotColorMap("MCP Profile", "time","sec","Channel","","Count","qty","Projection",'Count','qty','Channel','')
        self.setLabelLineIntensity("intensity","time", "sec", "Count", "qty" )
        self.__addPlotColorMap__((0,120,120),"Intensity",(0,120,120),'Projection')
        
        self.lineCounterPlot = pg.plot()
        self.lineCounterPlot.addLegend()
        self.lineCounterPlot.getAxis("bottom").setTickFont(font)
        self.lineCounterPlot.getAxis("left").setTickFont(font)
        d2.addWidget(self.lineCounterPlot)
        self.setLabelLineCounter("Counter", "time","sec","Count","qty")
        self.setterDatascCTLine = self.__addPlotLineByXY__(True, (255,0,0),"scCenter")
        self.setterDatascLBLine = self.__addPlotLineByXY__(False, (170,120,0),"scLeftBottom")
        self.setterDatascLULine = self.__addPlotLineByXY__(False, (20,200,20),"scLeftUp")
        self.setterDatascRULine = self.__addPlotLineByXY__(False, (0,255,50),"scRightUp")
        self.setterDatascRBLine = self.__addPlotLineByXY__(False, (0,120,120),"scRightBottom")
        #self.plotSetItemDatamcpIntensity = self.mainWindow.addPlotLineByXY(False, (0,0,255),"mcpIntensity")
        self.__addPlotColorMap__((0,120,120),"Intensity",(0,120,120),'Projection')
        
        self.viewBoxPlot = pg.plot()
        pos = np.array([
            [0,0],
            [10,0],
            [0,10],
            [10,10],
            [5,5]
            ])
        symbols = ['o','o','o','o','o']
        g = pg.GraphItem()
        g.setData(pos=pos,symbol=symbols,pxMode=False,size=2)
        self.viewBoxPlot.addItem(g)
        self.viewBoxPlot.setAspectLocked(1.0)
        font=QtGui.QFont()
        font.setPixelSize(20)
        self.scRUTextItem=pg.TextItem("")
        self.scRUTextItem.setFont(font)
        self.scLUTextItem=pg.TextItem("")
        self.scLUTextItem.setFont(font)
        self.scRBTextItem=pg.TextItem("")
        self.scRBTextItem.setFont(font)
        self.scLBTextItem=pg.TextItem("")
        self.scLBTextItem.setFont(font)
        self.scCTextItem=pg.TextItem("")
        self.scCTextItem.setFont(font)
        self.viewBoxPlot.addItem(self.scLBTextItem)
        self.scLBTextItem.setPos(*pos[0])
        self.viewBoxPlot.addItem(self.scRBTextItem)
        self.scRBTextItem.setPos(*pos[1])
        self.viewBoxPlot.addItem(self.scLUTextItem)
        self.scLUTextItem.setPos(*pos[2])
        self.viewBoxPlot.addItem(self.scRUTextItem)
        self.scRUTextItem.setPos(*pos[3])
        self.viewBoxPlot.addItem(self.scCTextItem)
        self.scCTextItem.setPos(*pos[4])
        d3.addWidget(self.viewBoxPlot)
        
        self.ui.verticalLayoutCentral.addWidget(self.dockAreaChart)
        self.setMode(ModeInterface.DEFFAULT)
    
    def setMode(self,mode:ModeInterface):
        self.layoutPlot.setEnabled(mode.plotEnabled)
        self.ui.lineEditFolder.setEnabled(mode.lineEditEnabled)
        self.ui.pushButtonOpenFolder.setEnabled(mode.pushButtonOpenFolderEnabled)
        self.ui.comboBoxListFiles.setEnabled(mode.comboBoxListFilesEnabled)
        self.ui.pushButtonExportData.setEnabled(mode.pushButtonExportEnabled)
    def show(self):
        self.mainWindow.show()
    def setFileLists(self, list:list):
        for file in list:
            self.ui.comboBoxListFiles.addItem(file)
    def __addPlotColorMap__(self,penIntensity,nameIntensity,penProjection,nameProjection):
        self.linePlotIntensityMcpitem:pg.PlotDataItem = self.intensityMapLinePlot.plot(pen=penIntensity,name=nameIntensity)
        self.histPlotProjectionMcpItem:pg.PlotDataItem = self.projectionMapHistPlot.plot(pen=penProjection,name=nameProjection)
        #self.bar._update_items()
    def __setDataInPlotColorMap__(self,data,scaleX, dataIntensityX, dataIntensityY,dataProjectionHist):
        
  
        # create horizontal list i.e x-axis
        
        self.histogramItem.setOpts(y=np.arange(.5,len(dataProjectionHist)+.5),width=dataProjectionHist)
        
        self.image.setImage(data)
        self.linePlotIntensityMcpitem.setData(x=dataIntensityX,y=dataIntensityY)
        tr = QtGui.QTransform()
        tr.scale(scaleX,1)
        self.image.setTransform(tr)
        self.bar._update_items()
        #self.colorMapPlot.getAxis('bottom').setScale(scaleX)
    def __addPlotLineByXY__(self,clear:bool, pen, name:str):
        #if (clear): self.linePlot.clear()
        d:pg.PlotDataItem = self.lineCounterPlot.plot(pen=pen, name=name)
        return lambda x,y: d.setData(x=x,y=y)
    def setDataMCP(self,data,scaleX):
        intensity = np.sum(data,axis=1)
        projection = np.transpose(data).sum(axis=1)
        self.__setDataInPlotColorMap__(data,scaleX,np.arange(0,len(data)*scaleX,scaleX),intensity,projection)
        self.bar.setMaxMinImage(np.min(data),np.max(data))
        
        
    def setDataCounter(self,scRU,scLU,scRB,scLB,scCT,x):
        self.setterDatascCTLine(x,scCT)
        self.setterDatascLBLine(x,scLB)
        self.setterDatascLULine(x,scLU)
        self.setterDatascRBLine(x,scRB)
        self.setterDatascRULine(x,scRU)
        self.scRUTextItem.setText(str(np.sum(scRU)))
        self.scLUTextItem.setText(str(np.sum(scLU)))
        self.scRBTextItem.setText(str(np.sum(scRB)))
        self.scLBTextItem.setText(str(np.sum(scLB)))
        self.scCTextItem.setText(str(np.sum(scCT)))
        
    def setLabelPlotColorMap(self,titlePlot, titleX, unitX, titleY, unitY, titleColorBar, unitColor,titleProjection, titleProjectionX, unitProjectionX, titleProjectionY, unitYProjection):
        self.colorMapPlot.setTitle(titlePlot, **self.titlePlotStyle)
        self.colorMapPlot.setLabel('left', titleY, units=unitY, **self.labelAxisStyle)
        self.colorMapPlot.setLabel('bottom', titleX, units=unitX, **self.labelAxisStyle)
        font=QtGui.QFont()
        font.setPixelSize(10)
        self.projectionMapHistPlot.setTitle(titleProjection,**self.labelAxisStyle)
        self.projectionMapHistPlot.setLabel('left',titleProjectionY,units=unitYProjection,**self.labelAxisStyle)
        self.projectionMapHistPlot.setLabel('bottom',titleProjectionX,units=unitProjectionX,**self.labelAxisStyle)
        #self.bar.setLabel('left', titleColorBar, units=unitColor, **self.labelAxisStyle)
    def setLabelLineIntensity(self, titlePlot, titleX, unitX, titleY, unitY):
        self.intensityMapLinePlot.setTitle(titlePlot, **self.titlePlotStyle)
        self.intensityMapLinePlot.setLabel('left', titleY, units=unitY, **self.labelAxisStyle)
        self.intensityMapLinePlot.setLabel('bottom', titleX, units=unitX, **self.labelAxisStyle)
    def setLabelLineCounter(self, titlePlot, titleX, unitX, titleY, unitY):
        self.lineCounterPlot.setTitle(titlePlot, **self.titlePlotStyle)
        self.lineCounterPlot.setLabel('left', titleY, units=unitY, **self.labelAxisStyle)
        self.lineCounterPlot.setLabel('bottom', titleX, units=unitX, **self.labelAxisStyle)
        
    def showExistingFolderDialog(self, path:str):
        return str(QtWidgets.QFileDialog.getExistingDirectory(parent=self.ui.centralwidget, directory=path))
    def getSaveFile(self):
        return str(QtWidgets.QFileDialog.getSaveFileName(self.mainWindow,directory=os.getcwd(),filter='CSV files (*.csv);')[0])
    def setPath(self,path:str):
        self.ui.lineEditFolder.setText(path)