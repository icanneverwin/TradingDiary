
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

#from .model import OpenInterestModel, cotModel, ViewSymbolModel
from tradingDiary.views.openInterestWindow import openInterestUI
from tradingDiary.views.cotWindow import cotUI
from tradingDiary.db.process_to_db import delta_upld
from tradingDiary.views.dialogs.addsymbol import AddSymbolDialog
from tradingDiary.views.forecast_window import ForeCastWindow
from tradingDiary.models.view_symbol_model import ViewSymbolModel
from tradingDiary.views.options.main_window import sysOptionsMainWindow


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
    #self.sysOptionsMainWindow()
    self.addForecastWindow()
    self.addOptionsWindow()

    # initialize OI/COT window classes
    self.win_OI = None
    self.win_COT = None  

    self.OIdataButton.clicked.connect(self.toggle_OI_window)
    self.COTdataButton.clicked.connect(self.toggle_COT_window)
    self.CheckUpdatesButton.clicked.connect(self.get_updates)
    self.BriefDealsButton.clicked.connect(partial(self.switchStackedPage, 1))
    self.SystemOptions.clicked.connect(partial(self.switchStackedPage, 2))
  

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

  
  def addOptionsWindow(self):
    self.optionsWindow = sysOptionsMainWindow()
    self.stackedLayout.addWidget(self.optionsWindow)