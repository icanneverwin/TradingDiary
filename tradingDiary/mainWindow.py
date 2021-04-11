
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
  QComboBox,
  QDialog, 
  QHBoxLayout,
  QLabel,
  QListWidget,
  QListWidgetItem,
  QMainWindow,
  QSizePolicy,
  QStackedLayout,
  QStackedWidget,
  QWidget,
  QAbstractItemView,
  QPushButton,
  QTableView,
  QVBoxLayout
)

from functools import partial
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QPoint, QRect, QSize, Qt

import sys

from .model import OpenInterestModel, cotModel, ViewSymbolModel
from .process_to_db import delta_upld
from .dialogs import AddSymbolDialog
from .database import get_symbols

from tradingDiary.views.forecast_window import ForeCastWindow


class openInterestUI(QWidget):

  def __init__(self):
    super().__init__()
    self.setupUI()


  def setupUI(self):

    self.setWindowTitle('Open Interest')

    self.setGeometry(450, 200, 669, 600)
    self.setFixedWidth(669)
    #self.setMinimumHeight = 600
    self.oiMainLayout = QVBoxLayout()
    self.oiButtonLayout = QHBoxLayout()

    self.oiComboBox = QComboBox()

    #self.oiComboBox.addItems(['AUD','BRL','BTC','GBP','CAD','EUR','JPY','MXN','NZD','RUB','CHF','NG','CL','XAU','XAG'])
    self.oiComboBox.addItems(get_symbols())
    self.oiComboBox.setMinimumWidth(70)
    self.oiComboBox.setCurrentIndex(5)

    self.oiInitUpld = QPushButton()
    self.oiInitUpld.setText('Upload latest data')
    self.oiInitUpld.setMinimumWidth(100)
    

    # configure table model
    self.openInterestModel = OpenInterestModel(self.oiComboBox.currentText())
    self.table = QTableView()
    self.table.setModel(self.openInterestModel.model)
    self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

    # set column width
    self.table.setColumnWidth(0, 60)
    self.table.setColumnWidth(1, 180)
    self.table.setColumnWidth(2, 70)
    self.table.setColumnWidth(3, 70)
    self.table.setColumnWidth(4, 70)
    self.table.setColumnWidth(5, 86)
    self.table.setColumnWidth(6, 70)

    #self.table.horizontalHeader().setStretchLastSection(True)

    # add widgets
    self.oiButtonLayout.addWidget(self.oiComboBox)
    self.oiButtonLayout.addStretch()
    self.oiButtonLayout.addWidget(self.oiInitUpld)
    self.oiMainLayout.addLayout(self.oiButtonLayout)
    self.oiMainLayout.addWidget(self.table)
    self.setLayout(self.oiMainLayout)

    # change contents of tableview once combobox symbol is changed
    self.oiComboBox.currentIndexChanged.connect(self.onChanged)

    #self.oiInitUpld.clicked.connect(self.uploadOI)


  def onChanged(self):
    self.openInterestModel.setSymbol(self.oiComboBox.currentText())
    self.openInterestModel.setModel()
    self.table.setModel(self.openInterestModel.model)
    self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
   

class cotUI(QWidget):

  def __init__(self):
    super().__init__()
    self.setupUI()


  def setupUI(self):

    self.setWindowTitle('Commitment of Traders')
    self.setGeometry(450, 200, 764, 600)
    self.setFixedWidth(764)
    #self.height = 600
    self.cotlayout = QVBoxLayout()

    self.cotSymbol = QComboBox()
    #self.cotSymbol.addItems(['AUD','BRL','BTC','GBP','CAD','EUR','JPY','MXN','NZD','RUB','CHF','NG','CL','XAU','XAG'])
    self.cotSymbol.addItems(get_symbols())
    self.cotSymbol.setCurrentIndex(6)

    self.cotModel = cotModel(self.cotSymbol.currentText())
    self.table = QTableView()
    self.table.setModel(self.cotModel.model)
    self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
    #self.table.horizontalHeader().setStretchLastSection(True)

    # set column width
    self.table.setColumnWidth(0, 60)
    self.table.setColumnWidth(1, 70)
    self.table.setColumnWidth(2, 70)
    self.table.setColumnWidth(3, 70)
    self.table.setColumnWidth(4, 70)
    self.table.setColumnWidth(5, 70)
    self.table.setColumnWidth(6, 80)
    self.table.setColumnWidth(7, 84)
    self.table.setColumnWidth(8, 60)
    self.table.setColumnWidth(9, 60)

    self.cotlayout.addWidget(self.cotSymbol)
    self.cotlayout.addWidget(self.table)
    
    self.setLayout(self.cotlayout)

    self.cotSymbol.currentIndexChanged.connect(self.onChanged)
  

  def onChanged(self):
    self.cotModel.setSymbol(self.cotSymbol.currentText())
    self.cotModel.setModel()
    self.table.setModel(self.cotModel.model)
    self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
    #self.table.horizontalHeader().setStretchLastSection(True)



class Window(QMainWindow):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.setupUI()


  def setupUI(self):
    self.setWindowTitle("Trading Diary")
    self.setGeometry(300, 150, 1200, 800)
    self.centralWidget = QWidget()
    self.centralWidget.setStyleSheet("background-color: rgb(180, 180, 180);")
    self.setCentralWidget(self.centralWidget)
    self.mainLayout = QHBoxLayout()
    self.centralWidget.setLayout(self.mainLayout)

    self.setupLeftMenu()
    self.setupRightArea()
    self.sysOptionsMainWindow()
    self.addForecastWindow()

    # initialize OI/COT window classes
    self.win_OI = None
    self.win_COT = None
    #self.win_OI = openInterestUI()
    #self.win_COT = cotUI()
    #self.OIdataButton.clicked.connect(self.showOIWindow)
    #self.OIdataButton.clicked.connect(self.toggleOIWindow)
    #self.COTdataButton.clicked.connect(self.toggleCOTWindow)

    #self.OIdataButton.clicked.connect(lambda checked: self.toggle_window(self.win_OI))
    #self.COTdataButton.clicked.connect(lambda checked: self.toggle_window(self.win_COT))

    

    self.OIdataButton.clicked.connect(self.toggle_OI_window)
    self.COTdataButton.clicked.connect(self.toggle_COT_window)
    self.CheckUpdatesButton.clicked.connect(self.get_updates)
    self.SystemOptions.clicked.connect(partial(self.switchStackedPage, 1))
    self.BriefDealsButton.clicked.connect(partial(self.switchStackedPage, 2))
  

  def setupLeftMenu(self):

    leftMenuLayout = QVBoxLayout()

    self.OIdataButton = QPushButton()
    self.COTdataButton = QPushButton()
    self.BriefDealsButton = QPushButton()
    self.ActiveTradesButton = QPushButton()
    self.TradesHistoryButton = QPushButton()
    self.SystemOptions = QPushButton()
    self.CheckUpdatesButton = QPushButton()

    self.OIdataButton.setText('Open Interest')
    self.COTdataButton.setText('COT Reports')
    self.BriefDealsButton.setText('Trading Plans')
    self.ActiveTradesButton.setText('Active Trades')
    self.TradesHistoryButton.setText('Trade History')
    self.SystemOptions.setText('Options')
    self.CheckUpdatesButton.setText('Upload New Reports')

    self.OIdataButton.setMinimumHeight(70)
    self.COTdataButton.setMinimumHeight(70)
    self.BriefDealsButton.setMinimumHeight(70)
    self.ActiveTradesButton.setMinimumHeight(70)
    self.TradesHistoryButton.setMinimumHeight(70)
    self.SystemOptions.setMinimumHeight(70)
    self.CheckUpdatesButton.setMinimumHeight(70)

    leftMenuLayout.addWidget(self.OIdataButton)
    leftMenuLayout.addWidget(self.COTdataButton)
    leftMenuLayout.addWidget(self.BriefDealsButton)
    leftMenuLayout.addWidget(self.ActiveTradesButton)
    leftMenuLayout.addWidget(self.TradesHistoryButton)
    leftMenuLayout.addWidget(self.SystemOptions)
    leftMenuLayout.addStretch()
    leftMenuLayout.addWidget(self.CheckUpdatesButton)

    self.mainLayout.addLayout(leftMenuLayout)


  def setupRightArea(self):
    self.stackedLayout = QStackedLayout()

    # create main page
    self.MainPageWidget = QWidget()
    self.MainPageLayout = QHBoxLayout()

    # label
    self.mainLabel = QLabel(self, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
    self.mainLabel.setText('Welcome to the Trading Dairy')
    self.mainLabel.setStyleSheet(" font-size: 48px; font-family: Verdana;")
    self.MainPageLayout.addWidget(self.mainLabel)

    # set internal layout
    self.MainPageWidget.setLayout(self.MainPageLayout)

    # add mainpage widget to stacked layout
    self.stackedLayout.addWidget(self.MainPageWidget)

    # add stacked layout to main layout
    self.mainLayout.addLayout(self.stackedLayout)

  
  def sysOptionsMainWindow(self):
    """
      
      Options window

    """

    # main window setup
    self.SysOpsMainWidget = QWidget()
    self.SysOpsMainLayout = QHBoxLayout()
    self.SysOpsMainWidget.setLayout(self.SysOpsMainLayout)

    # setup list widget and its items
    self.SysOpsListWidget = QListWidget()
    self.SysOpsListWidget.setFixedWidth(205)

    SysOpsAboutLWI = QListWidgetItem(self.SysOpsListWidget)
    SysOpsAboutLWI.setText('About')
    SysOpsAboutLWI.setSizeHint(QSize(200, 30))

    SysOpsViewSymbolsLWI = QListWidgetItem(self.SysOpsListWidget)
    SysOpsViewSymbolsLWI.setText('View Symbols')
    SysOpsViewSymbolsLWI.setSizeHint(QSize(200, 30))

    self.SysOpsStackedWidget = QStackedWidget()

    self.SysOpsMainLayout.addWidget(self.SysOpsListWidget)
    self.SysOpsMainLayout.addWidget(self.SysOpsStackedWidget)

    self.stackedLayout.addWidget(self.SysOpsMainWidget)

    self.sysOptionsAboutWindow()
    self.sysOptionsViewSymbolWindow()

    self.SysOpsListWidget.currentRowChanged.connect(self.switchSysOpsStackedPage)


  def sysOptionsAboutWindow(self):

    AboutMainWidget = QWidget()
    AboutMainLayout = QHBoxLayout()
    AboutMainWidget.setLayout(AboutMainLayout)

    AboutLabel = QLabel()
    AboutLabel.setText('This is Trading Diary')
    AboutMainLayout.addWidget(AboutLabel)

    self.SysOpsStackedWidget.addWidget(AboutMainWidget)


  def sysOptionsViewSymbolWindow(self):

    ViewSymbolMainWidget = QWidget()
    ViewSymbolLayout = QHBoxLayout()
    ViewSymbolMainWidget.setLayout(ViewSymbolLayout)

    self.ViewSymbolModelTable = ViewSymbolModel()
    self.ViewSymbolTable = QTableView()
    self.ViewSymbolTable.setModel(self.ViewSymbolModelTable.model)
    self.ViewSymbolTable.setSelectionBehavior(QAbstractItemView.SelectRows)

    self.ViewSymbolTable.setColumnWidth(0, 70)
    self.ViewSymbolTable.setColumnWidth(1, 300)
    self.ViewSymbolTable.horizontalHeader().setStretchLastSection(True)

    # setup buttons
    ViewSymbolButtonLayout = QVBoxLayout()

    ViewSymbolAddButton = QPushButton()
    ViewSymbolAddButton.setText('Add..')
    ViewSymbolAddButton.setMinimumWidth(70)

    ViewSymbolAddButton.clicked.connect(self.openAddSymbolDialog)

    ViewSymbolDelButton = QPushButton()
    ViewSymbolDelButton.setText('Delete row')
    ViewSymbolDelButton.setMinimumWidth(70)

    ViewSymbolButtonLayout.addWidget(ViewSymbolAddButton)
    ViewSymbolButtonLayout.addWidget(ViewSymbolDelButton)

    ViewSymbolLayout.addWidget(self.ViewSymbolTable)
    ViewSymbolLayout.addLayout(ViewSymbolButtonLayout)

    self.SysOpsStackedWidget.addWidget(ViewSymbolMainWidget)

  
  def openAddSymbolDialog(self):
    dialog = AddSymbolDialog()
    if dialog.exec() == QDialog.Accepted:
      print(dialog.data)
      self.ViewSymbolModelTable.insertSymbol(dialog.data)
      self.ViewSymbolTable.resizeColumnsToContents()


  def switchSysOpsStackedPage(self, index):
    self.SysOpsStackedWidget.setCurrentIndex(index)

  
  def switchStackedPage(self, index):
    self.stackedLayout.setCurrentIndex(index)


  def toggle_OI_window(self):
    if self.win_OI == None:
      self.win_OI = openInterestUI()
      self.win_OI.show()
    else:
      if self.win_OI.isVisible():
        self.win_OI.hide()
      else:
        self.win_OI.show()


  def toggle_COT_window(self):
    if self.win_COT == None:
      self.win_COT = cotUI()
      self.win_COT.show()
    else:
      if self.win_COT.isVisible():
        self.win_COT.hide()
      else:
        self.win_COT.show()

    
  def get_updates(self):
    delta_upld()


  def toggle_window(self, window):
    if window.isVisible():
      window.hide()
    else:
      window.show()


  def addForecastWindow(self):
    self.win_Forecast = ForeCastWindow()
    self.stackedLayout.addWidget(self.win_Forecast)
