import sqlite3
import sys
from sqlite3 import Error
from .db_config import *
class TradingDB():
  def __init__(self, path_to_db) -> None:
    self.conn = None
    try:
      self.conn = sqlite3.connect(path_to_db)
      print("=======================================================================================")
      print(f"Connected to SQLITE3 database: DB Path - {path_to_db}, DB Version - {sqlite3.version}")
      print("=======================================================================================")
    except Error as err:
      print(f">>>>error: {err}")

    print("Initializing database configuration")
    if self.conn is not None:
      #for table, query in db_config.db_check.items():
      for table, query in db_check.items():
        try:
          self.cur = self.conn.cursor()
          self.cur.execute(query)
          if self.cur.fetchone()[0] == 1:
            print(f">>>>TABLE: {table.upper()} already exists")
          else:
            #self.cur.execute(db_config.create_table_sql[table])
            self.cur.execute(create_table_sql[table])
            print(f">>>>TABLE: {table.upper()} is created")
        except Error as err:
          print(f">>>>error: {err}")
    print("=======================================================================================")


  def get_oi_symbol(self, symbol):
    query = """select symbol
                     ,desc
                     ,substr(oi_date, 1,4) || '-' || substr(oi_date, 5,2) || '-' || substr(oi_date,7,2)
                     ,globex_volume
                     ,volume
                     ,open_interest
                     ,change
                     ,preliminary_ind
                 from oi_reports 
                where symbol = ? order by cast(oi_date as int) desc"""
    try:
      self.cur.execute(query, symbol)
    except Error as err:
      print(f">>>>error while fetching data from oi_reports table, symbol = {symbol}\n {err}")
    return self.cur.fetchall()
  

  def check_oi_exists(self, row_data):
    query = "select count(*) from oi_reports where symbol = ? and oi_date = ?"
    try:
      self.cur.execute(query, row_data)
    except Error as err:
      print(f">>>>error while fetching data from oi_reports, row_data = {row_data}\n {err}")
      sys.exit(3)
    return self.cur.fetchone()


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
    try:
      self.cur.execute(query, row_data)
      self.conn.commit()
      print(f">>>>row {row_data} was inserted successfully")
    except Error as err:
      print(f">>>>error while inserting data to oi_reports table\n row_data = {row_data}\n {err}")
    


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
    try:
      self.cur.execute(query, row_data)
      self.conn.commit()
      print(f">>>>row {row_data} was inserted successfully")
    except Error as err:
      print(f">>>>error while inserting data to cot_reports table\n row_data = {row_data}\n {err}")


  def get_cot_symbol(self, symbol):
    query = """select symbol
                     ,substr(cot_date, 1,4) || '-' || substr(cot_date, 5,2) || '-' || substr(cot_date,7,2)
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
                 from cot_reports 
                where symbol = ? order by cast(cot_date as int) desc"""
    try:
      self.cur.execute(query, symbol)
    except Error as err:
      print(f">>>>error while fetching data from cot_reports table, symbol = {symbol}\n {err}")
    return self.cur.fetchall()
  

  def check_cot_exists(self, row_data):
    query = "select count(*) from cot_reports where symbol = ? and cot_date = ?"
    try:
      self.cur.execute(query, row_data)
    except Error as err:
      print(f">>>>error while fetching data from cot_reports, row_data = {row_data}\n {err}")
    return self.cur.fetchone()

  
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
      try:
        self.cur.execute(query, row_data[row])
        record_count += 1
        if record_count % 100 == 0:
          print(f">>>>{record_count} rows inserted")
      except Error as err:
        print(f">>>>error while inserting data to cot_reports table\n row_data = {row_data[row]}\n {err}")
    
    self.conn.commit()
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
      try:
        self.cur.execute(query, row_data[row])
        record_count += 1
      except Error as err:
        print(f">>>>error while inserting data to oi_reports table\n row_data = {row_data[row]}\n {err}")
    self.conn.commit()
    print(f">>>>{record_count} inserted")

  
  def get_latest_cot(self, symbol):
    query = "select max(cast(cot_date as int)) from cot_reports where symbol = ?"
    try:
      self.cur.execute(query, symbol)
    except Error as err:
      print(f">>>>error while retrieving the latest date from COT_REPORTS table for symbol {symbol[0]}\n {err}")
    return self.cur.fetchone()[0]
    
  
  def get_latest_oi(self, symbol):
    query = "select max(cast(oi_date as int)) from oi_reports where symbol = ?"
    try:
      self.cur.execute(query, symbol)
    except Error as err:
      print(f">>>>error while retrieving the latest date from OI_REPORTS table for symbol {symbol[0]}\n {err}")
    return self.cur.fetchone()[0]

  
  def delete_cot_rec(self, row_data):
    query = "delete from cot_reports where symbol = ? and cot_date = ?"
    try:
      self.cur.execute(query, row_data)
      self.conn.commit()
      print(f">>>>data for symbol = {row_data[0]} and cot_date = {row_data[1]} deleted from COT_REPORTS successfully")
    except Error as err:
      print(f">>>>error while deleting row {row_data} from COT_REPORTS table\n {err}")


  def delete_oi_rec(self, row_data):
    query = "delete from oi_reports where symbol = ? and oi_date = ?"
    try:
      self.cur.execute(query, row_data)
      self.conn.commit()
      print(f">>>>data for symbol = {row_data[0]} and cot_date = {row_data[1]} deleted from OI_REPORTS successfully")
    except Error as err:
      print(f">>>>error while deleting row {row_data} from COT_REPORTS table\n {err}")


  def get_cot_rec(self, row_data):
    query = "select * from cot_reports where symbol = ? and cot_date = ?"
    try:
      self.cur.execute(query, row_data)
    except Error as err:
      print(f">>>>error while deleting row {row_data} from COT_REPORTS table\n {err}")
    return self.cur.fetchone()

  
  def get_oi_rec(self, row_data):
    query = "select * from oi_reports where symbol = ? and oi_date = ?"
    try:
      self.cur.execute(query, row_data)
    except Error as err:
      print(f">>>>error while deleting row {row_data} from OI_REPORTS table\n {err}")
    return self.cur.fetchone()
  

  def check_oi_preliminary(self, row_data):
    query = "select count(*) from oi_reports where symbol = ? and oi_date = ? and preliminary_ind = 'Y'"
    try:
      self.cur.execute(query, row_data)
    except Error as err:
      print(f">>>>error while checking preliminary report from OI_REPORTS table for symbol {row_data[0]} and oi_date {row_data[1]}\n {err}")
    return self.cur.fetchone()[0]


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
    try:
      self.cur.execute(query, row_data)
      self.conn.commit()
      print(f">>>>row {row_data} has been updated.")
    except Error as err:
      print(f">>>>error while updating record in DB {row_data}\n {err}")


  def drop_oi_table(self):
    query = "drop table if exists oi_reports"
    try:
      self.cur.execute(query)
      self.conn.commit
      print(f">>>>table oi_reports was removed.")
    except Error as err:
      print(f">>>>error while dropping table oi_reports\n {err}")
    
 
if __name__ == '__main__':

  #create_connection(r"E:\Forex\cme_reports\trading.db")
  #new_db = TradingDB(r"E:\Forex\cme_reports\trading.db")

  #oi_row = ('AUD','Australian Dollar Futures', '20210312', 131904, 132270, 154035, 2869)
  #TradingDB.insert_oi_data(new_db, oi_row)
  #record = TradingDB.get_oi_symbol(new_db, ('AUD',))
  #print(record)

  #check_rec = TradingDB.check_oi_exists(new_db, ('AUD', '20210312'))
  #if check_rec[0] == 1:
  #  print("record exists")
  #else:
  #  print("record not exists")
  #
  #cot_row = ( 'CL', 
  #            'CRUDE OIL, LIGHT SWEET - NEW YORK MERCANTILE EXCHANGE',
  #            '210316',
  #            3236873,
  #            686345,
  #            111651,
  #            1099364,
  #            1728485,
  #            66376,
  #            -7933,
  #            3518,
  #            30269,
  #            15751,
  #            21.2,
  #            3.4,
  #            34.0,
  #            53.4
  #          )
  #TradingDB.insert_cot_data(new_db, cot_row)
  #
  #
  #cot_rec = TradingDB.get_cot_symbol(new_db, ('CL',))
  #print(cot_rec)

  db_path = 'E:\\Forex\\cme_reports\\trading.db'
  new_db = TradingDB(db_path)
  #record = new_db.get_oi_symbol(('EUR',))
  #record = TradingDB.get_cot_symbol(new_db, ('CL',))

  #db_max_date = new_db.get_latest_oi(('EUR',))
  #print(db_max_date)

  print(new_db.get_oi_rec(('EUR', '20210324')))
  print(new_db.get_oi_symbol(('EUR',)))
  #new_db.delete_oi_rec(('EUR', '20210324'))

  #for i in range(len(record)):
  #  print(record[i])
  #latest_date = new_db.get_latest_cot(('EUR',))
  #print(latest_date)


  #################################################################
  # test cot_delta_upld
  #################################################################

  #new_db.delete_cot_rec(('AUD', '20210316'))
  #new_db.delete_cot_rec(('AUD', '20210309'))
  #new_db.delete_cot_rec(('AUD', '20210302'))
  #new_db.delete_cot_rec(('MXN', '20210316'))

  #print(new_db.get_cot_rec(('AUD', '20210316')))
  #################################################################
  # test oi_delta_upld
  #################################################################

  #latest_date = new_db.get_latest_oi(('EUR',))
  #print(latest_date)

  #new_db.drop_oi_table()





  
  
