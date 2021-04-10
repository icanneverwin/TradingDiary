from xlrd import open_workbook
import os
import re
from .download_cme import preliminary_check
import config

def get_date(filepath: str) -> str:
  """extract date from filename (OI reports)

  Args:
      filepath (str): absolute path of a file

  Returns:
      str: date string
  """

  basename = os.path.basename(filepath)
  return re.search(r'.*_([0-9]*)\.xls', basename).group(1)


def get_oi_data(filepath: str, oi_symbol_desc: str) -> list:
  """parses OI reports and extracts list of sets per each Futures from the provided file
      Format:
              [(
                Symbol,
                Name of futures,
                Report Date,
                Globex Volume,
                Volume,
                Open Interest,
                Change in Open Interest,
                Preliminary Indicator
              )]

  Args:
      filepath (str): absolute file path

  Returns:
      list: list of sets per each futures
  """
  oi_list = list()
  oi_date = get_date(filepath)

  if os.path.isfile(filepath):
    if preliminary_check(filepath):
      preliminary_ind = 'Y'
    else:
      preliminary_ind = 'N'

    wb = open_workbook(filepath)
    xls = wb.sheet_by_index(0)
    for row_index in range(xls.nrows):
      #if xls.cell_value(rowx=row_index, colx=0) in oi_desc_symbol.keys():
      if xls.cell_value(rowx=row_index, colx=0) == oi_symbol_desc:
        oi_list.append((config.oi_desc_symbol[xls.cell_value(rowx=row_index, colx=0)],  # Symbol
                        xls.cell_value(rowx=row_index, colx=0),                         # Name
                        oi_date,                                                        # Date of the extracted file
                        int(xls.cell_value(rowx=row_index, colx=2).replace(',', '')),   # Globex Volume 
                        int(xls.cell_value(rowx=row_index, colx=5).replace(',', '')),   # Volume
                        int(xls.cell_value(rowx=row_index, colx=6).replace(',', '')),   # Open Interest
                        int(xls.cell_value(rowx=row_index, colx=7).replace(',', '')),   # Change in Open Interest
                        preliminary_ind
                      ))
  else:
    print(f"File {filepath} is not found")
  
  return oi_list



def get_cot_data(filepath: str, cot_date: str, symbol: str) -> list:
  """parses COT report and extracts data for the provided date and configured futures name.
    Format:
          [(
            COT Date,
            Market_and_Exchange_Names,
            Symbol,
            Open_Interest_All,
            NonComm_Positions_Long_All,
            NonComm_Positions_Short_All,
            Comm_Positions_Long_All,
            Comm_Positions_Short_All,
            Change_in_Open_Interest_All,
            Change_in_NonComm_Long_All,
            Change_in_NonComm_Short_All,
            Change_in_Comm_Long_All,
            Change_in_Comm_Short_All,
            Pct_of_OI_NonComm_Long_All,
            Pct_of_OI_NonComm_Short_All,
            Pct_of_OI_Comm_Long_All,
            Pct_of_OI_Comm_Short_All,
          )]

  Args:
      filepath (str): Absolute path to the file
      cot_date (str): COT date

  Returns:
      list: list of sets per each futures
  """
  
  cot_list = list()
  # choose either bulk or single path
  bulk_process = False
  if symbol is None and cot_date is None:
    symbol_desc_list = config.cot_futures_list
    bulk_process = True
  else:
    symbol_desc_list = config.cot_futures[symbol]

    # add first to digit to year
    if int(cot_date[0:2]) > 90: # 1990 - 1999
      cot_prefix = 19
    else:                       # 2000 - 2089
      cot_prefix = 20
  
  if os.path.isfile(filepath):
    wb = open_workbook(filepath)
    xls = wb.sheet_by_index(0)
    for row_index in range(xls.nrows):
      if (xls.cell_value(rowx=row_index, colx=0)) in symbol_desc_list:
        if bulk_process == False:
          if str(int(xls.cell_value(rowx=row_index, colx=1))) == cot_date or xls.cell_value(rowx=row_index, colx=1) == cot_date:
            # add first 2 year digits            
            cot_list.append(( symbol,                                                                                                   # Symbol    
                              #cot_futures_dict[xls.cell_value(rowx=row_index, colx=0)],                                                # Symbol
                              #xls.cell_value(rowx=row_index, colx=0),                                                                  # Market_and_Exchange_Names
                              str(cot_prefix) + cot_date,                                                                               # cot date
                              int(xls.cell_value(rowx=row_index, colx=7))     if xls.cell_value(rowx=row_index, colx=7)   != '' else 0, # Open_Interest_All
                              int(xls.cell_value(rowx=row_index, colx=8))     if xls.cell_value(rowx=row_index, colx=8)   != '' else 0, # NonComm_Positions_Long_All
                              int(xls.cell_value(rowx=row_index, colx=9))     if xls.cell_value(rowx=row_index, colx=9)   != '' else 0, # NonComm_Positions_Short_All
                              int(xls.cell_value(rowx=row_index, colx=11))    if xls.cell_value(rowx=row_index, colx=11)  != '' else 0, # Comm_Positions_Long_All
                              int(xls.cell_value(rowx=row_index, colx=12))    if xls.cell_value(rowx=row_index, colx=12)  != '' else 0, # Comm_Positions_Short_All
                              int(xls.cell_value(rowx=row_index, colx=37))    if xls.cell_value(rowx=row_index, colx=37)  != '' else 0, # Change_in_Open_Interest_All
                              int(xls.cell_value(rowx=row_index, colx=38))    if xls.cell_value(rowx=row_index, colx=38)  != '' else 0, # Change_in_NonComm_Long_All
                              int(xls.cell_value(rowx=row_index, colx=39))    if xls.cell_value(rowx=row_index, colx=39)  != '' else 0, # Change_in_NonComm_Short_All
                              int(xls.cell_value(rowx=row_index, colx=41))    if xls.cell_value(rowx=row_index, colx=41)  != '' else 0, # Change_in_Comm_Long_All
                              int(xls.cell_value(rowx=row_index, colx=42))    if xls.cell_value(rowx=row_index, colx=42)  != '' else 0, # Change_in_Comm_Short_All
                              float(xls.cell_value(rowx=row_index, colx=48))  if xls.cell_value(rowx=row_index, colx=48)  != '' else 0, # Pct_of_OI_NonComm_Long_All
                              float(xls.cell_value(rowx=row_index, colx=49))  if xls.cell_value(rowx=row_index, colx=49)  != '' else 0, # Pct_of_OI_NonComm_Short_All
                              float(xls.cell_value(rowx=row_index, colx=51))  if xls.cell_value(rowx=row_index, colx=51)  != '' else 0, # Pct_of_OI_Comm_Long_All
                              float(xls.cell_value(rowx=row_index, colx=52))  if xls.cell_value(rowx=row_index, colx=52)  != '' else 0, # Pct_of_OI_Comm_Short_All
                            ))
        else:
          if str(xls.cell_value(rowx=row_index, colx=1))[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8']:
            # 2000 - 2089
            cot_prefix = 20
          else:
            # 1990 - 1999
            cot_prefix = 19
          cot_list.append(( config.cot_futures_dict[xls.cell_value(rowx=row_index, colx=0)],                                          # Symbol    
                            #cot_futures_dict[xls.cell_value(rowx=row_index, colx=0)],                                                # Symbol
                            #xls.cell_value(rowx=row_index, colx=0),                                                                  # Market_and_Exchange_Names
                            str(cot_prefix) + str(xls.cell_value(rowx=row_index, colx=1)),                                            # cot date
                            int(xls.cell_value(rowx=row_index, colx=7))     if xls.cell_value(rowx=row_index, colx=7)   != '' else 0, # Open_Interest_All
                            int(xls.cell_value(rowx=row_index, colx=8))     if xls.cell_value(rowx=row_index, colx=8)   != '' else 0, # NonComm_Positions_Long_All
                            int(xls.cell_value(rowx=row_index, colx=9))     if xls.cell_value(rowx=row_index, colx=9)   != '' else 0, # NonComm_Positions_Short_All
                            int(xls.cell_value(rowx=row_index, colx=11))    if xls.cell_value(rowx=row_index, colx=11)  != '' else 0, # Comm_Positions_Long_All
                            int(xls.cell_value(rowx=row_index, colx=12))    if xls.cell_value(rowx=row_index, colx=12)  != '' else 0, # Comm_Positions_Short_All
                            int(xls.cell_value(rowx=row_index, colx=37))    if xls.cell_value(rowx=row_index, colx=37)  != '' else 0, # Change_in_Open_Interest_All
                            int(xls.cell_value(rowx=row_index, colx=38))    if xls.cell_value(rowx=row_index, colx=38)  != '' else 0, # Change_in_NonComm_Long_All
                            int(xls.cell_value(rowx=row_index, colx=39))    if xls.cell_value(rowx=row_index, colx=39)  != '' else 0, # Change_in_NonComm_Short_All
                            int(xls.cell_value(rowx=row_index, colx=41))    if xls.cell_value(rowx=row_index, colx=41)  != '' else 0, # Change_in_Comm_Long_All
                            int(xls.cell_value(rowx=row_index, colx=42))    if xls.cell_value(rowx=row_index, colx=42)  != '' else 0, # Change_in_Comm_Short_All
                            float(xls.cell_value(rowx=row_index, colx=48))  if xls.cell_value(rowx=row_index, colx=48)  != '' else 0, # Pct_of_OI_NonComm_Long_All
                            float(xls.cell_value(rowx=row_index, colx=49))  if xls.cell_value(rowx=row_index, colx=49)  != '' else 0, # Pct_of_OI_NonComm_Short_All
                            float(xls.cell_value(rowx=row_index, colx=51))  if xls.cell_value(rowx=row_index, colx=51)  != '' else 0, # Pct_of_OI_Comm_Long_All
                            float(xls.cell_value(rowx=row_index, colx=52))  if xls.cell_value(rowx=row_index, colx=52)  != '' else 0, # Pct_of_OI_Comm_Short_All
                          ))

  else:
    print(f"File {filepath} is not found")

  return cot_list


def get_dates_from_cot(filepath: str, symbol: str) -> set:

  dates = set()
  if os.path.isfile(filepath):
    wb = open_workbook(filepath)
    xls = wb.sheet_by_index(0)

    for row_index in range(xls.nrows):
      if row_index == 0:
        continue
      
      if (xls.cell_value(rowx=row_index, colx=0)) in config.cot_futures[symbol]:
        if isinstance(xls.cell_value(rowx=row_index, colx=1), float):
          date_str = str(int((xls.cell_value(rowx=row_index, colx=1))))
        else:
          date_str = xls.cell_value(rowx=row_index, colx=1)
      
        if date_str[0] == "'":
          dates.add(date_str[1:])
        else:
          dates.add(date_str)

  return dates




if __name__== '__main__':

  #oi_file = r"E:\Forex\cme_reports\oi_reports\forex\oi_forex_20210312.xls"
  #print(get_oi_data(oi_file))


  cot_file = r"E:\Forex\cme_reports\cot_reports\deacom_xls_1998.xls"
  
  
  #cot_out = get_cot_data(cot_file, '171205')
  #for i in range(len(cot_out)):
  #  print(cot_out[i])
  
  print(get_dates_from_cot(cot_file))