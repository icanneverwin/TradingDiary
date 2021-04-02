from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
  QComboBox, QHBoxLayout, QHeaderView, 
  QMainWindow, 
  QWidget,
  QAbstractItemView,
  QPushButton,
  QTableView,
  QVBoxLayout
)

from PyQt5.QtCore import Qt

from .model import OpenInterestModel

class Window(QMainWindow):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.setWindowTitle("Trading Diary")
    self.setGeometry(300, 150, 1200, 800)
    self.centralWidget = QWidget()
    self.setCentralWidget(self.centralWidget)
    self.layout = QHBoxLayout()
    self.centralWidget.setLayout(self.layout)

    self.openInterestModel = OpenInterestModel()
    self.setupUI()
  
  def setupUI(self):

    self.OIdataButton = QPushButton('Open Interest')
    self.COTdataButton = QPushButton('COT Reports')
    self.BriefDealsButton = QPushButton('Tomorrow')
    self.ActiveTradesButton = QPushButton('Active Trades')
    self.TradesHistoryButton = QPushButton('Trade History')

    menuLayout = QVBoxLayout()
    #menuLayout.setAlignment(Qt.AlignLeft)
    #menuLayout.setDirection(0)
    menuLayout.addWidget(self.OIdataButton)
    menuLayout.addWidget(self.COTdataButton)
    menuLayout.addWidget(self.BriefDealsButton)
    menuLayout.addWidget(self.ActiveTradesButton)
    menuLayout.addWidget(self.TradesHistoryButton)

    
    self.OISymbol = QComboBox()
    self.OISymbol.addItems(['AUD','BRL','BTC','GBP','CAD','EUR','JPY','MXN','NZD','RUB','CHF','NG','CL','XAU','XAG'])

    self.table = QTableView()
    self.table.setModel(self.openInterestModel.model)
    self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

    #self.table.resizeColumnsToContents()
    #self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
    self.table.horizontalHeader().setStretchLastSection(True)
    #self.table.horizontalHeader().sectionResizeMode(QHeaderView.Stretch)

    
    activeWindow = QVBoxLayout()
    activeWindow.addWidget(self.OISymbol)
    activeWindow.addWidget(self.table)
    #self.layout.addWidget(self.OISymbol)
    self.layout.addLayout(menuLayout)
    #self.layout.addWidget(self.table)
    self.layout.addLayout(activeWindow)
