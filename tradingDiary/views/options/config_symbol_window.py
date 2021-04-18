from PyQt5.QtWidgets import (
  QDialog, 
  QHBoxLayout,
  QWidget,
  QAbstractItemView,
  QPushButton,
  QTableView,
  QVBoxLayout
)

from tradingDiary.views.dialogs.addsymbol import AddSymbolDialog
from tradingDiary.models.view_symbol_model import ViewSymbolModel


class optionsViewSymbolWindow(QWidget):
  #def sysOptionsViewSymbolWindow(self):
  def __init__(self):
    super().__init__()
    self.mainLayout = QHBoxLayout()

    self.setLayout(self.mainLayout)

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

    self.mainLayout.addWidget(self.ViewSymbolTable)
    self.mainLayout.addLayout(ViewSymbolButtonLayout)

  
  def openAddSymbolDialog(self):
    dialog = AddSymbolDialog()
    if dialog.exec() == QDialog.Accepted:
      print(dialog.data)
      self.ViewSymbolModelTable.insertSymbol(dialog.data)
      self.ViewSymbolTable.resizeColumnsToContents()