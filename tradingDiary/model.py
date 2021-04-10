# tradingDairy/model.py

from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel, QSqlTableModel

class OpenInterestModel:
  def __init__(self, symbol):
    self.symbol = symbol
    #self.model = self._createModel()
    self.model = self._createModelSymbol(self.symbol)

  #@staticmethod
  def _createModel(self):
    self.oi_get_query = QSqlQuery()
    self.oi_get_query.prepare("""select symbol
                                  ,desc
                                  ,substr(oi_date, 1,4) || '-' || substr(oi_date, 5,2) || '-' || substr(oi_date,7,2)
                                  ,globex_volume
                                  ,volume
                                  ,open_interest
                                  ,change
                             from oi_reports
                            where symbol = "EUR"
                            order by cast(oi_date as int) desc
                            ;
                        """)
    #oi_get_query.addBindValue(symbol)
    self.oi_get_query.exec()
    queryModel = QSqlQueryModel()
    queryModel.setQuery(self.oi_get_query)

    headers = ['Symbol', 'Description', 'Date', 'Globex', 'Volume', 'Open Interest', 'Change']

    for columnIndex, header in enumerate(headers):
      queryModel.setHeaderData(columnIndex, Qt.Horizontal, header)
    return queryModel
  

  #@staticmethod
  def _createModelSymbol(self, symbol):
    self.oi_get_query = QSqlQuery()
    self.oi_get_query.prepare("""select symbol
                                  ,desc
                                  ,substr(oi_date, 1,4) || '-' || substr(oi_date, 5,2) || '-' || substr(oi_date,7,2)
                                  ,globex_volume
                                  ,volume
                                  ,open_interest
                                  ,change
                             from oi_reports
                            where symbol = ?
                            order by cast(oi_date as int) desc
                            ;
                        """)

    self.oi_get_query.addBindValue(symbol)
    self.oi_get_query.exec()
    queryModel = QSqlQueryModel()
    queryModel.setQuery(self.oi_get_query)

    headers = ['Symbol', 'Description', 'Date', 'Globex', 'Volume', 'Open Interest', 'Change']

    for columnIndex, header in enumerate(headers):
      queryModel.setHeaderData(columnIndex, Qt.Horizontal, header)
    return queryModel


  def setSymbol(self, symbol):
    self.symbol = symbol


  def setModel(self):
    self.model = self._createModelSymbol(self.symbol)

  
  def disableQuery(self):

    if self.oi_get_query.isActive():
      self.oi_get_query.finish()
  
  def enableQuery(self):
    self.oi_get_query.exec()



class cotModel:
  def __init__(self, symbol):
    self.symbol = symbol
    #self.model = self._createModel()
    self.model = self._createModelSymbol(self.symbol)


  @staticmethod
  def _createModelSymbol(symbol):
    cot_get_query = QSqlQuery()
    cot_get_query.prepare("""select symbol
                                   ,substr(cot_date, 1,4) || '-' || substr(cot_date, 5,2) || '-' || substr(cot_date,7,2)
                                   ,OI_ALL
                                   ,CHANGE_OI
                                   ,NONCOMM_POS_LONG
                                   ,NONCOMM_POS_SHORT
                                   ,CHANGE_NONCOMM_LONG
                                   ,CHANGE_NONCOMM_SHORT
                                   ,PCT_OI_NONCOMM_LONG
                                   ,PCT_OI_NONCOMM_SHORT
                             from cot_reports
                            where symbol = ?
                            order by cast(cot_date as int) desc
                            ;
                        """)

    cot_get_query.addBindValue(symbol)
    cot_get_query.exec()
    queryModel = QSqlQueryModel()
    queryModel.setQuery(cot_get_query)

    headers = ['Symbol', 'Date', 'Total OI', 'Change OI', 'Total Long', 'Total Short', 'Change Long', 'Change Short', '% Long', '% Short']

    for columnIndex, header in enumerate(headers):
      queryModel.setHeaderData(columnIndex, Qt.Horizontal, header)
    return queryModel

  def setSymbol(self, symbol):
    self.symbol = symbol


  def setModel(self):
    self.model = self._createModelSymbol(self.symbol)



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