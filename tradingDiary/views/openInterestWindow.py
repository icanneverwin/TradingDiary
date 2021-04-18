from PyQt5.QtWidgets import (
  QWidget,
  QVBoxLayout,
  QHBoxLayout,
  QPushButton,
  QTableView,
  QComboBox,
  QAbstractItemView
)

from tradingDiary.db.database import get_symbols
from tradingDiary.models.oi_model import OpenInterestModel

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