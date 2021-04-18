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
from tradingDiary.models.cot_model import cotModel


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

