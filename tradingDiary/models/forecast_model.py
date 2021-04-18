from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel


class NewForecastModel():
  def __init__(self, ):
    self.model = self.createModel()

  @staticmethod
  def createModel():
    tableModel = QSqlTableModel()
    tableModel.setTable("forecast")
    #tableModel.setFilter(f"date = {filterdate}")
    tableModel.select()
    headers = ('Symbol', 'Date', 'H4', 'Day', 'OI_First', 'OI_Last', 'COT_First', 'COT_Last', 'H1', 'Comment')
    for index, column in enumerate(headers):
      tableModel.setHeaderData(index, Qt.Horizontal, column)
    return tableModel


  def insertEmptyRecord(self):
    rows = self.model.rowCount()
    columns = self.model.columnCount()
    self.model.insertRows(rows, 1)

    for column in range(columns):
      self.model.setData(self.model.index(rows, column), "")
    self.model.submitAll()
    self.model.select()

  
  def deleteRecord(self, row):
    self.model.removeRow(row)
    self.model.submitAll()
    self.model.select()