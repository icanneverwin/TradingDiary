from PyQt5.QtWidgets import (
  QDialog,
  QDialogButtonBox,
  QFormLayout,
  QLineEdit,
  QMessageBox,
  QVBoxLayout
)

from PyQt5.QtCore import Qt


class AddSymbolDialog(QDialog):
  
  def __init__(self, parent=None):
    super().__init__(parent=parent)
    self.setWindowTitle('Add Symbol')
    self.setMinimumWidth(500)
    self.mainLayout = QVBoxLayout()
    self.setLayout(self.mainLayout)
    self.data = None

    self.setupUI()

  
  def setupUI(self):

    # create line edits for data fields
    self.symbolName = QLineEdit()
    self.symbolName.setObjectName('symbol_name')
    self.symbolDescOI = QLineEdit()
    self.symbolDescOI.setObjectName('symbol_desc_oi')
    self.symbolDescCOT = QLineEdit()
    self.symbolDescCOT.setObjectName('symbol_desc_cot')

    # create layout and add line edits to it
    layout = QFormLayout(self)
    layout.addRow("Symbol:", self.symbolName)
    layout.addRow("OI Desc:", self.symbolDescOI)
    layout.addRow("COT Desc:", self.symbolDescCOT)
    self.mainLayout.addLayout(layout)

    # add default "add" / "cancel" button to Dialog window
    self.buttonsBox = QDialogButtonBox(self)
    self.buttonsBox.setOrientation(Qt.Horizontal)
    self.buttonsBox.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

    self.buttonsBox.accepted.connect(self.addSymbol)
    self.buttonsBox.rejected.connect(self.reject)
    self.mainLayout.addWidget(self.buttonsBox)
  

  def addSymbol(self):

    self.data = list()
    for field in (self.symbolName, self.symbolDescOI, self.symbolDescCOT):
      if not field.text():
        QMessageBox.critical(
          self,
          "Error!",
          f"You must provide a correct record {field.objectName()}",
        )
        self.data = None
      self.data.append(field.text())
    
    if not self.data:
      return
    
    super().accept()