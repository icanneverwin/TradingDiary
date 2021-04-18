from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel

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