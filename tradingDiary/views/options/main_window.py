from PyQt5.QtWidgets import (
  QHBoxLayout,
  QListWidget,
  QListWidgetItem,
  QStackedWidget,
  QWidget
)

from PyQt5.QtCore import QSize, Qt
from tradingDiary.views.dialogs.addsymbol import AddSymbolDialog
from tradingDiary.views.options.about_window import optionsAboutWindow
from tradingDiary.views.options.config_symbol_window import optionsViewSymbolWindow

  
class sysOptionsMainWindow(QWidget):

  def __init__(self):
    super().__init__()
    self.mainLayout = QHBoxLayout()
    self.setLayout(self.mainLayout)
    self.setupUI()


  def setupUI(self):
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

    self.mainLayout.addWidget(self.SysOpsListWidget)
    self.mainLayout.addWidget(self.SysOpsStackedWidget)

    self.sysOptionsAboutWindow()
    self.sysOptionsViewSymbolWindow()

    self.SysOpsListWidget.currentRowChanged.connect(self.switchSysOpsStackedPage)


  def sysOptionsAboutWindow(self):
    self.AboutMainWidget = optionsAboutWindow()
    self.SysOpsStackedWidget.addWidget(self.AboutMainWidget)


  def sysOptionsViewSymbolWindow(self):
    self.ViewSymbolMainWidget = optionsViewSymbolWindow()
    self.SysOpsStackedWidget.addWidget(self.ViewSymbolMainWidget)


  def switchSysOpsStackedPage(self, index):
    self.SysOpsStackedWidget.setCurrentIndex(index)