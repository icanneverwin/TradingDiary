from PyQt5.QtWidgets import (
  QAbstractItemView,
  QHBoxLayout,
  QStackedWidget,
  QTableView,
  QVBoxLayout,
  QPushButton,
  QWidget
)

from tradingDiary.models.forecast_model import NewForecastModel


class ForeCastWindow(QStackedWidget):
  def __init__(self):
    super().__init__()
    self.setupUI()


  def setupUI(self):
    self.setWindowTitle('Plans for tomorrow')
    self.forecastView()
    self.setCurrentIndex(1)


  def forecastView(self):
    self.forecastViewWidget = QWidget()
    self.forecastMainLayout = QHBoxLayout()
    self.forecastViewWidget.setLayout(self.forecastMainLayout)
    self.setForecastTable()
    self.setButtonsLayout()
    self.addWidget(self.forecastViewWidget)


  def setForecastTable(self):
    self.forecastModel = NewForecastModel()
    self.forecastTable = QTableView()
    self.forecastTable.setModel(self.forecastModel.model)
    self.forecastTable.setSelectionBehavior(QAbstractItemView.SelectRows)
    self.forecastTable.setColumnWidth(0,70)
    self.forecastTable.horizontalHeader().setStretchLastSection(True)

    #directionCombobox = QComboBox()
    #directionCombobox.addItems('UP', 'DOWN', 'FLAT')
    #self.forecastTable.setItemDelegateForColumn(2, directionCombobox)
    self.forecastMainLayout.addWidget(self.forecastTable)

  
  def setButtonsLayout(self):
    buttonLayout = QVBoxLayout()
    self.newRecordButton = QPushButton('Insert New Record')
    self.delRecord = QPushButton('Delete Record')
    self.historyButton = QPushButton('View History')
    buttonLayout.addWidget(self.newRecordButton)
    buttonLayout.addWidget(self.delRecord)
    buttonLayout.addWidget(self.historyButton)
  
    self.forecastMainLayout.addLayout(buttonLayout)
    self.setAddButton()
    self.setDelButton()


  def setAddButton(self):
    self.newRecordButton.clicked.connect(self.forecastModel.insertEmptyRecord)


  def setDelButton(self):
    self.delRecord.clicked.connect(self.forecastModel.deleteRecord)


if __name__ == "__main__":
  from PyQt5.QtWidgets import QApplication
  import sys
    
  from tradingDiary.models.forecast_model import NewForecastModel
  app = QApplication(sys.argv)
  win = ForeCastWindow()
  win.show()
  sys.exit(app.exec_())







    

  
