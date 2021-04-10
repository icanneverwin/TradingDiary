# tradingDiary/database.py

"""This module provided a database connection."""

#from .db_config import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

#def createConnection(databaseName):
#  connection = QSqlDatabase.addDatabase("QSQLITE")
#  connection.setDatabaseName(databaseName)
#
#  if not connection.open():
#    QMessageBox.warning(
#      None,
#      "Trading Diary",
#      f"Database Error: {connection.lastError().text()}",
#    )
#    return False
#
#  #db = QSqlDatabase.database()
#  #print(db.tables())
# 
#  return True

class TradeDiaryDB():

  def __init__(self):
    self.dbType = 'QSQLITE'
    self.dbFilePath = "E:\\Forex\\cme_reports\\trading.db"
    self.dbUserName = ""
    self.dbPassword = ""
    self.create_connection()
    self.execQuery = QSqlQuery()

    # create tables if not exists
    self.create_tables()

  
  def create_connection(self):
    self.db = QSqlDatabase.addDatabase(self.dbType)
    self.db.setUserName(self.dbUserName)
    self.db.setPassword(self.dbPassword)
    self.db.setDatabaseName(self.dbFilePath)

    if not self.db.open():
      QMessageBox.warning(
        None,
        "Trading Diary",
        f"Database Error: {self.db.lastError().text()}"
        )
      return False

  def check_connection(self):
    return self.db.open()

  
  def _exec(self, query):
    try:
      self.execQuery.prepare(query)
      self.execQuery.exec()
    except Exception as err:
      print(f"Error: {err} \nQuery: {self.execQuery.executedQuery()}")

  
  def _exec2(self, query, *args):
    try:
      self.execQuery.prepare(query)
      if len(args) != 0:
        for bindValue in args:
          self.execQuery.addBindValue(bindValue)
      self.execQuery.exec()
    except Exception as err:
      print(f"Error while executing query:\n {err} \nQuery: {self.execQuery.executedQuery()}")
    
    

  def _finish(self):
    self.execQuery.finish()
  

  def create_tables(self):

    create_table_sql = {
      "oi_reports": """ CREATE TABLE IF NOT EXISTS oi_reports (
                            SYMBOL text NOT NULL,
                            DESC text NOT NULL,
                            OI_DATE text NOT NULL,
                            GLOBEX_VOLUME int NOT NULL,
                            VOLUME int NOT NULL,
                            OPEN_INTEREST int NOT NULL,
                            CHANGE int NOT NULL,
                            PRELIMINARY_IND TEXT NOT NULL,
                            PRIMARY KEY (SYMBOL, OI_DATE)
                          );
                      """,
      "cot_reports": """ CREATE TABLE IF NOT EXISTS cot_reports (
                              SYMBOL text NOT NULL,
                              COT_DATE text NOT NULL,
                              OI_ALL int NOT NULL,
                              NONCOMM_POS_LONG int NOT NULL,
                              NONCOMM_POS_SHORT int NOT NULL,
                              COMM_POS_LONG int NOT NULL,
                              COMM_POS_SHORT int NOT NULL,
                              CHANGE_OI int NOT NULL,
                              CHANGE_NONCOMM_LONG int NOT NULL,
                              CHANGE_NONCOMM_SHORT int NOT NULL,
                              CHANGE_COMM_LONG int NOT NULL,
                              CHANGE_COMM_SHORT int NOT NULL,
                              PCT_OI_NONCOMM_LONG real NOT NULL,
                              PCT_OI_NONCOMM_SHORT real NOT NULL,
                              PCT_OI_COMM_LONG real NOT NULL,
                              PCT_OI_COMM_SHORT real NOT NULL,
                              
                              PRIMARY KEY (SYMBOL, COT_DATE)
                            );
                        """,
      "symbols": """ CREATE TABLE IF NOT EXISTS symbols (
                          SYMBOL text NOT NULL,
                          OI_DESC text NOT NULL,
                          COT_DESC text NOT NULL,

                          PRIMARY KEY (SYMBOL)
                        );
                  """
    }
    db_check = {
      "oi_reports": "select count(name) from sqlite_master where type = 'table' and name = 'oi_reports'",
      "cot_reports": "select count(name) from sqlite_master where type = 'table' and name = 'cot_reports'",
      "symbols": "select count(name) from sqlite_master where type = 'table' and name = 'symbols'"
    }

    if self.db.isOpen():
      for table, query in db_check.items():
        self._exec(query)
        self.execQuery.first()
        if self.execQuery.value(0) == 1:
          print(f">>>>TABLE: {table.upper()} already exists")
        else:
          self._finish()
          self._exec(create_table_sql[table])
          print(f">>>>TABLE: {table.upper()} is created")


  def get_table_list(self):
    return self.db.tables()

####################################################################################################
# SELECT
####################################################################################################

  def check_oi_preliminary(self, row_data):
    query = "select count(*) from oi_reports where symbol = ? and oi_date = ? and preliminary_ind = 'Y'"
    self._exec2(query, *row_data)
    self.execQuery.first()
    return self.execQuery.value(0)


  def get_latest_oi(self, row_data):
    query = "select max(cast(oi_date as int)) from oi_reports where symbol = ?"
    self._exec2(query, *row_data)
    self.execQuery.first()
    return self.execQuery.value(0)


  def get_latest_cot(self, row_data):
    query = "select max(cast(oi_date as int)) from oi_reports where symbol = ?"
    self._exec2(query, *row_data)
    self.execQuery.first()
    return self.execQuery.value(0)

####################################################################################################
# INSERT
####################################################################################################

  def bulk_insert_cot_data(self, row_data):
    query = """insert into cot_reports (symbol
                                        ,cot_date
                                        ,oi_all
                                        ,noncomm_pos_long
                                        ,noncomm_pos_short
                                        ,comm_pos_long
                                        ,comm_pos_short
                                        ,change_oi
                                        ,change_noncomm_long
                                        ,change_noncomm_short
                                        ,change_comm_long
                                        ,change_comm_short
                                        ,pct_oi_noncomm_long
                                        ,pct_oi_noncomm_short
                                        ,pct_oi_comm_long
                                        ,pct_oi_comm_short
                                        )
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    
    record_count = 0    
    for row in range(len(row_data)):
      self._exec2(query, *row)
      self._finish()
      record_count += 1
      if record_count % 100 == 0:
        print(f">>>>{record_count} rows inserted")
    self.db.commit()
    print(f">>>>{record_count} inserted")


  def bulk_insert_oi_data(self, row_data):
    query = """insert into oi_reports (symbol
                                      ,desc
                                      ,oi_date
                                      ,globex_volume
                                      ,volume
                                      ,open_interest
                                      ,change
                                      ,preliminary_ind)
                values (?, ?, ?, ?, ?, ?, ?, ?)"""
    
    record_count = 0    
    for row in range(len(row_data)):
      self._exec2(query, *row)
      record_count += 1
      if record_count % 100 == 0:
        print(f">>>>{record_count} rows inserted")
    self.db.commit()
    print(f">>>>{record_count} inserted")


  def insert_oi_data(self, row_data):
    query = """insert into oi_reports (symbol
                                      ,desc
                                      ,oi_date
                                      ,globex_volume
                                      ,volume
                                      ,open_interest
                                      ,change
                                      ,preliminary_ind)
                values (?, ?, ?, ?, ?, ?, ?, ?)"""
    self._exec2(query, *row_data)
    self.db.commit()
    print(f">>>>row {row_data} was inserted successfully")


  def insert_cot_data(self, row_data):
    query = """insert into cot_reports (symbol
                                        ,cot_date
                                        ,oi_all
                                        ,noncomm_pos_long
                                        ,noncomm_pos_short
                                        ,comm_pos_long
                                        ,comm_pos_short
                                        ,change_oi
                                        ,change_noncomm_long
                                        ,change_noncomm_short
                                        ,change_comm_long
                                        ,change_comm_short
                                        ,pct_oi_noncomm_long
                                        ,pct_oi_noncomm_short
                                        ,pct_oi_comm_long
                                        ,pct_oi_comm_short
                                        )
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    self._exec2(query, *row_data)
    self.db.commit()
    print(f">>>>row {row_data} was inserted successfully")

####################################################################################################
# DELETE
####################################################################################################

  def delete_cot_rec(self, row_data):
    query = "delete from cot_reports where symbol = ? and cot_date = ?"
    self._exec2(query, *row_data)
    self.db.commit()
    print(f">>>>row {row_data} was deleted successfully")


  def delete_oi_rec(self, row_data):
    query = "delete from oi_reports where symbol = ? and oi_date = ?"
    self._exec2(query, *row_data)
    self.db.commit()
    print(f">>>>row {row_data} was deleted successfully")


  def update_oi_record(self, row_data):
    query = """update oi_reports
                  set globex_volume = ?
                     ,volume = ?
                     ,open_interest = ?
                     ,change = ?
                     ,preliminary_ind = ?
                where symbol = ?
                  and oi_date = ?        
              """
    self._exec2(query, *row_data)
    self.db.commit()
    print(f">>>>row {row_data} has been updated.")



####################################################################################################
# SELECT
####################################################################################################



def get_symbols():
  query = "select symbol from symbols order by symbol"
  get_symbols_query = QSqlQuery()
  get_symbols_query.prepare(query)
  get_symbols_query.exec()
  data = list()
  while get_symbols_query.next():
    data.append(get_symbols_query.value(0))
  return data

if __name__ == '__main__':
   db = TradeDiaryDB()
   print(db.get_table_list())

   symbols = db.get_symbols()

   for symbol in symbols:
     print(symbol)