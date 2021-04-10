import os
import sys
import datetime
from tradingDiary import db
#from . import db, parse_report, download_cme
from . import database, parse_report, download_cme
import config


def oi_init_upld(db_object):
  print('==========================================================================')
  print('========================PROCESSING OPEN INTEREST REPORTS==================')
  print('==========================================================================')

  #root_path = 'E:\\Forex\\cme_reports\\oi_reports'
  reports_path = config.report_path + '\\oi_reports'
  oi_report_types = ['equity', 'agricultural', 'energy', 'forex', 'metals']
  #oi_report_types = ['metals']
  print(oi_report_types)
  for dir in oi_report_types:
    oi_list = []
    # get list of files
    file_list = os.listdir(reports_path + '\\' + dir)
    #print(f"list of {dir} files is {file_list}")

    # for each file
    for file in file_list:
      filename = reports_path + '\\' + dir + '\\' + file

      # parse data
      for symbol_desc in config.oi_desc_symbol.keys():
        oi_list.extend(parse_report.get_oi_data(filename, symbol_desc))
      
      # if not empty, then process to DB
    if oi_list:
      #print(f"DATA FOR DIR {dir} = {oi_list}")
      # process all items in the list
      print(f"Inserting data for [{dir}] into oi_reports table")
      db_object.bulk_insert_oi_data(oi_list)
    


def cot_init_upld(db_object):

  print('==========================================================================')
  print('===========================PROCESSING COT REPORTS=========================')
  print('==========================================================================')
  #root_path = 'E:\\Forex\\cme_reports\\cot_reports'
  reports_path = config.report_path + '\\cot_reports'
  # get list of files
  file_list = os.listdir(reports_path)
  print(file_list)
  for file in file_list:
    print('==========================================================================')

    # for each file
    filepath = reports_path + '\\' + file
    cot_list = []
    if os.path.isfile(filepath):
      print(f"File {filepath} exists, processing...")
      
      cot_list.extend(parse_report.get_cot_data(filepath, None, None))
      # get dates from the file
      #for symbol in config.symbols:
      #  cot_dates = parse_report.get_dates_from_cot(filepath, symbol)
      #  for process_date in cot_dates:
      #    cot_list.extend(parse_report.get_cot_data(filepath, process_date, symbol))
    else:
       print(f"File {filepath} not exists")
        
    # if not empty, then process to DB
    if cot_list:
      print(f"Inserting data for {file} into cot_reports table")
      db_object.bulk_insert_cot_data(cot_list)


def cot_delta_upld(db_object):

  curr_year = datetime.datetime.now().year

  for symbol in config.symbols:
    # get the latest date from xls
    db_max_date = db_object.get_latest_cot((symbol,))
    print(db_max_date, symbol)
    start_year = int(str(db_max_date)[0:4])
    
    # process all xls files per each symbol / year 
    for year in range(start_year, curr_year + 1):
      print("======================================================================================")
      print(f"[{symbol}] - start year = {year}, db_max_date = {db_max_date}")

      # check if file exists
      cot_report = config.report_path + '\\cot_reports\\deacom_xls_' + str(year) + '.xls'
      if os.path.isfile(cot_report):
        print(f"File {cot_report} exists, processing...")

        file_dates = parse_report.get_dates_from_cot(cot_report, symbol)
        xls_max_date = max([int(item) for item in file_dates])

        # align xls date to yyyymmdd date format
        if int(str(xls_max_date)[0:2]) > 90: # 1990 - 1999
          cot_prefix = 19
        else:                       # 2000 - 2089
          cot_prefix = 20
        
        check_date = int(str(cot_prefix) + str(xls_max_date))
        #print(f"[{symbol}] - {file_dates} ###### max_date = {xls_max_date}")
        #print(f"db_max_date = {db_max_date}, check_date = {check_date}")

        if int(db_max_date) < check_date:

          # process data to DB
          for process_date in file_dates:
            if int(str(cot_prefix) + process_date) > int(db_max_date):
              print(f"###[{symbol}] processing date {process_date}")
              cot_row = parse_report.get_cot_data(cot_report, process_date, symbol)

              if cot_row:
                print(f"Inserting record {cot_row} to COT_REPORTS table")
                db_object.insert_cot_data(cot_row[0])
          
        else:
          print(f"[{symbol} - all data exists in DB")

      else:
        print(f"File {cot_report} not found")


def oi_delta_upld(db_object):

  # process each symbol
  for symbol in config.symbols:
    print("======================================================================================")
    xls_folder = config.report_path + '\\oi_reports\\' + config.oi_mapping[symbol]
    xls_date = download_cme.parse_date(download_cme.find_latest_file(xls_folder))
    db_max_date = db_object.get_latest_oi((symbol,))
    curr_date = datetime.datetime.now().date().strftime('%Y%m%d')

    print(f"[{symbol}]: db_max_date = {db_max_date}")
    
    # process each date starting from OI DB date till current date
    for i_date in range(int(db_max_date), int(curr_date) + 1):
      
      # set up path for preliminary OI report and final OI report
      xls_prelim_file = xls_folder + '\\' + 'oi_' + config.oi_mapping[symbol] + '_P_' + str(i_date) + '.xls'
      xls_base_file = xls_folder + '\\' + 'oi_' + config.oi_mapping[symbol] + '_' + str(i_date) + '.xls'

      prelim_file_ind = False
      base_file_ind = False

      # checking if preliminary or final report exist
      if os.path.isfile(xls_prelim_file):
        prelim_file_ind = True
        temp_file = xls_prelim_file
      elif os.path.isfile(xls_base_file):
        base_file_ind = True
        temp_file = xls_base_file
      else:
        print(f"File for date {i_date} is not found, continue...")
        continue

      oi_row = parse_report.get_oi_data(temp_file, config.oi_symbol_desc[symbol])
      if not oi_row:
        print(f"oi_row: {oi_row[0]} is empty, continue...")
        continue
      else:
        # check if the latest record in DB is preliminary
        if i_date == int(db_max_date):
          # if extracted DB record is preliminary
          prelim_ind = db_object.check_oi_preliminary((symbol, str(i_date)))
          if prelim_ind != 0:
            # record is preliminary, check if file is preliminary or not
            #print("here")
            if prelim_file_ind:
              # nothing to update
              print(f"Data: {oi_row[0]} already exists in DB from preliminary report: {temp_file}")
              continue
            elif base_file_ind:
              # we need to update OI values of existing record
              update_row = (oi_row[0][3], # globex volume
                            oi_row[0][4], # volume
                            oi_row[0][5], # open interest
                            oi_row[0][6], # change in open interest
                            oi_row[0][7], # preliminary ind
                            oi_row[0][0], # symbol
                            oi_row[0][2]) # oi date
              db_object.update_oi_record(update_row)
          else:
            print(f"Data: {oi_row[0]} already exists in DB from final report: {temp_file}")
        else:
          # if i_date != db_max_date -> insert new record
          db_object.insert_oi_data(oi_row[0])


def init_upld():

  # Uploading reports
  try:
    print(f"Downloading OI reports to {config.report_path} directory")
    download_cme.oi_download('init') 
    print("==========================================================================")
  except:
    print(f"Error while uploading OI reports\n {sys.exc_info()[0]}")

  try:
    print(f"Downloading COT reports to {config.report_path} directory")
    download_cme.cot_download('init') 
    print("==========================================================================")
  except Exception as err:
    print(f"Error while uploading COT reports\n ERROR: {err}")

  
  # initiating DB
  trading_db = database.TradeDiaryDB(config.db_path)

  if trading_db:
    # try to insert OI data to DB
    try:
      print(f"Inserting OI data to DB {config.db_path}")
      oi_delta_upld(trading_db)
      print("==========================================================================")
    except:
      print(f"Error while inserting OI data to DB\n {sys.exc_info()[0]}")
    
    # try to insert COT data to DB
    try:
      print(f"Inserting COT data to DB {config.db_path}")
      cot_init_upld(trading_db)
      print("==========================================================================")
    except Exception as err:
      print(f"Error while inserting COT data to DB\n ERROR: {err}")


def delta_upld():

  # uploading reports
  try:
    print(f"Downloading OI reports to {config.report_path} directory")
    download_cme.oi_download('delta') 
    print("==========================================================================")
  except Exception as err:
    print(f"Error while uploading OI reports\n ERROR: {err}")

  try:
    print(f"Downloading COT reports to {config.report_path} directory")
    download_cme.cot_download('delta') 
    print("==========================================================================")
  except Exception as err:
    print(f"Error while uploading COT reports\n ERROR: {err}")

  
  # initiating DB
  #trading_db = db.TradingDB(config.db_path)
  trading_db = database.TradeDiaryDB()

  if trading_db:
    # try to insert OI data to DB
    try:
      print(f"Inserting OI data to DB {config.db_path}")
      oi_delta_upld(trading_db)
      print("==========================================================================")
    except Exception as err:
      print(f"Error while inserting OI data to DB\n ERROR: {err}")
    
    # try to insert COT data to DB
    try:
      print(f"Inserting COT data to DB {config.db_path}")
      cot_delta_upld(trading_db)
      print("==========================================================================")
    except Exception as err:
      print(f"Error while inserting COT data to DB\n ERROR: {err}")



def delta_oi_upld():

  # uploading reports
  try:
    print(f"Downloading OI reports to {config.report_path} directory")
    download_cme.oi_download('delta') 
    print("==========================================================================")
  except Exception as err:
    print(f"Error while uploading OI reports\n ERROR: {err}")
  
  # initiating DB
  #trading_db = db.TradingDB(config.db_path)
  trading_db = database.TradeDiaryDB()

  if trading_db:
    # try to insert OI data to DB
    try:
      print(f"Inserting OI data to DB {config.db_path}")
      oi_delta_upld(trading_db)
      print("==========================================================================")
    except Exception as err:
      print(f"Error while inserting OI data to DB\n ERROR: {err}")


def delta_cot_upld():

  try:
    print(f"Downloading COT reports to {config.report_path} directory")
    download_cme.cot_download('delta') 
    print("==========================================================================")
  except Exception as err:
    print(f"Error while uploading COT reports\n ERROR: {err}")

  # initiating DB
  #trading_db = db.TradingDB(config.db_path)
  trading_db = database.TradeDiaryDB()

  if trading_db:    
    # try to insert COT data to DB
    try:
      print(f"Inserting COT data to DB {config.db_path}")
      cot_delta_upld(trading_db)
      print("==========================================================================")
    except Exception as err:
      print(f"Error while inserting COT data to DB\n ERROR: {err}")


if __name__ == '__main__':
  #oi_init_upld()
  #cot_init_upld()

  #print(datetime.datetime.now().date())
  #print(type(datetime.datetime.now().year))

  #cot_delta_upld()

  #oi_delta_upld(trade_db)
  #curr_date = datetime.datetime.now().date().strftime('%Y%m%d')
  #print(type(curr_date))

  delta_upld()

  # https://www.cmegroup.com/CmeWS/exp/voiProductsViewExport.ctl?media=xls&tradeDate=20210325&assetClassId=8&reportType=F&excluded=CEE,CEU,KCB
  # https://www.cmegroup.com/CmeWS/exp/voiProductsViewExport.ctl?media=xls&tradeDate=20210201&assetClassId=4&reportType=F&excluded=CEE,CEU,KCB