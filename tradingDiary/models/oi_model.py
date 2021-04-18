# tradingDairy/model.py

from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel

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


