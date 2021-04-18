
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel

class ViewSymbolModel():
  def __init__(self):
    self.model = self._createModel()

  @staticmethod
  def _createModel():
    tableModel = QSqlTableModel()
    tableModel.setTable("symbols")
    tableModel.setSort(0, Qt.SortOrder(0))
    tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)
    tableModel.select()

    headers = ("Symbol", "OI Description", "COT Description")
    for index, column in enumerate(headers):
      tableModel.setHeaderData(index, Qt.Horizontal, column)
    return tableModel

  
  def insertSymbol(self, data):

    rows = self.model.rowCount()
    self.model.insertRows(rows, 1)
    for column, field in enumerate(data):
      self.model.setData(self.model.index(rows, column), field)
    self.model.submitAll()
    self.model.select()