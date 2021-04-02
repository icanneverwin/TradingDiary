# tradingDairy/model.py

from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel

class OpenInterestModel:
  def __init__(self):
    #self.symbol = symbol
    self.model = self._createModel()

  @staticmethod
  def _createModel():
    oi_get_query = QSqlQuery()
    oi_get_query.prepare("""select symbol
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
    oi_get_query.exec()
    queryModel = QSqlQueryModel()
    queryModel.setQuery(oi_get_query)

    headers = ['Symbol', 'Description', 'Date', 'Globex', 'Volume', 'Open Interest', 'Change']

    for columnIndex, header in enumerate(headers):
      queryModel.setHeaderData(columnIndex, Qt.Horizontal, header)
    #queryModel.setHeaderData(0, Qt.Horizontal, 'Symbol')
    #queryModel.setHeaderData(1, Qt.Horizontal, 'Description')
    #queryModel.setHeaderData(2, Qt.Horizontal, 'Date')
    #queryModel.setHeaderData(3, Qt.Horizontal, 'Globex')
    #queryModel.setHeaderData(4, Qt.Horizontal, 'Volume')
    #queryModel.setHeaderData(5, Qt.Horizontal, 'Open Interest')
    #queryModel.setHeaderData(6, Qt.Horizontal, 'Change')
    return queryModel

