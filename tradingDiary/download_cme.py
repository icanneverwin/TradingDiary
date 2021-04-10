import requests
import os
import glob
import re
from datetime import datetime, date, timedelta
import zipfile
import config

### Daily FX Volume and Open Interest
# https://www.cmegroup.com/CmeWS/exp/voiProductsViewExport.ctl?media=xls&tradeDate=20210308&assetClassId=3&reportType=F&excluded=CEE,CEU,KCB

### Daily Energy Volume and Open Interest
# https://www.cmegroup.com/CmeWS/exp/voiProductsViewExport.ctl?media=xls&tradeDate=20210311&assetClassId=7&reportType=F&excluded=CEE,CEU,KCB


### Daily Agricultural Volume and Open Interest
# https://www.cmegroup.com/CmeWS/exp/voiProductsViewExport.ctl?media=xls&tradeDate=20210311&assetClassId=2&reportType=F&excluded=CEE,CEU,KCB

### Daily Equity Volume and Open Interest
# https://www.cmegroup.com/CmeWS/exp/voiProductsViewExport.ctl?media=xls&tradeDate=20210311&assetClassId=4&reportType=F&excluded=CEE,CEU,KCB


def check_dir(directory: str) -> bool:
    return True if os.path.exists(directory) else False

def find_latest_file(path: str):
  return max(glob.glob(path + '\\*'))


def parse_date(abs_path: str):
  date = re.search(r'.*_([0-9]*)\.xls', abs_path)
  return date.group(1)


def preliminary_check(abs_path: str):
  return False if abs_path.find('_P_') == -1 else True


def unarchive_remove(directory_path: str, zip_file: str, out_filename: str):

  # unarchive xls file and remove zip
  with zipfile.ZipFile(directory_path  + "\\" +  zip_file, 'r') as zip:
    extracted_filename = zip.namelist()[0]
    zip.extractall(directory_path)

  os.remove(directory_path  + "\\" +  zip_file)
  if extracted_filename != out_filename:
    print(f"Renaming extracted file {extracted_filename} to {out_filename}")
    os.rename(directory_path + "\\" + extracted_filename, directory_path + "\\" + out_filename)
  


def oi_download(dnld_type: str):
  """Download OI reports from https://www.cmegroup.com
     types: 
          1. init: initial download of reports (start_date must be set)
          2. delta: 
                    a. validates and finds missing reports data in E:\Forex\cme_reports\oi_reports
                    b. checks the latest report - if preliminary then removes and to downloads the final one
                    c. downloads remaining missing reports (exluding empty documents generated for weekends and holidays)

  Args:
      dnld_type (str): download type - "init" or "delta" 
  """

  oi_reports_dir = config.report_path + "\\oi_reports"
  dnld_count = 0
 
  ### 1. check and create directories in E:\Forex\cme_reports\oi_reports\<futures_type>
  # check if directories exist
  if not check_dir(oi_reports_dir):
    print(f"Directory {oi_reports_dir} not exists, creating...")
    os.mkdir(oi_reports_dir)
  
  for dir in config.oi_report_types.keys():
    if not check_dir(oi_reports_dir + '\\' + dir):
      print(f"Directory {oi_reports_dir}\{dir} not exists, creating...")
      os.mkdir(oi_reports_dir + '\\' + dir)

  ### 2. download all existing reports to each directory and name it as oi_<futures_type>_<yyyymmdd>.xls
  for report_key, report_value in config.oi_report_types.items():
    print("=============================================================================")
    print(f"Preparing reports download for {report_key}...")
    report_dir = oi_reports_dir + '\\' + report_key
    end_date = datetime.now().date()

    if dnld_type == "init":
      start_date = date(2021, 2, 1)

    elif dnld_type == "delta":
      # get the latest file in the folder
      latest_file = find_latest_file(report_dir)
      print(f">>The latest file in the folder \"{report_key}\" = {latest_file}")
      start_date = datetime.strptime(parse_date(latest_file), '%Y%m%d')
      start_date = start_date.date()

      # check if the latest file is a preliminary report
      if preliminary_check(latest_file):
        os.remove(latest_file)
      else:
        start_date = start_date + timedelta(days=1)
      
    # download reports starting from date (start_date)
    if start_date != end_date:
      for curr_date in [start_date+timedelta(days=x) for x in range((end_date-start_date).days + 1)]:
        
        if curr_date.weekday() < 5:
          xls_name = 'oi_' + str(report_key) + '_' + curr_date.strftime('%Y%m%d') + '.xls'
          url = config.oi_report_url \
                + curr_date.strftime('%Y%m%d') \
                + "&assetClassId=" \
                + str(report_value) \
                + "&reportType=F&excluded=CEE,CEU,KCB"
          #print(f"Downloading report from url {url}\n file: {report_dir + '/' + xls_name}")
          xls_data = requests.get(url, headers=config.headers)
          #print("report is requested")
          open(report_dir + "\\" + xls_name, 'wb').write(xls_data.content)
          #print("report is downloaded")
          # check if file is empty
          filesize = os.path.getsize(report_dir + '\\' + xls_name)
          if filesize == 8192:
            #print(f"file {report_dir + '/' + xls_name} is empty, checking preliminary report")
            # download preliminary report            
            url = config.oi_report_url \
                  + curr_date.strftime('%Y%m%d') \
                  + "&assetClassId=" \
                  + str(report_value) \
                  + "&reportType=P&excluded=CEE,CEU,KCB"
            os.remove(report_dir + '\\' + xls_name)
            xls_data = requests.get(url, headers=config.headers)
            xls_name = 'oi_' + str(report_key) + '_P_' + curr_date.strftime('%Y%m%d') + '.xls'
            open(report_dir + '\\' + xls_name, 'wb').write(xls_data.content)

            # if preliminary is empty then delete
            if os.path.getsize(report_dir + '\\' + xls_name) == 8192:
              os.remove(report_dir + '\\' + xls_name)
            else:
              print(f"Preliminary report {xls_name} is downloaded")
              dnld_count += 1
          else:
            print(f"Report {xls_name} downloaded")
            dnld_count += 1
    else:
      print("all reports are downloaded")

  print(f"[{dnld_count}] reports downloaded")

def cot_download(dnld_type: str):
  # 1. check and create directories in E:\Forex\cme_reports\cot_reports
  # 2. download all existing reports
  # 3. unzip xls files and remove archives

  cot_reports_dir = config.report_path + "\\cot_reports"
  start_year = 1995
  curr_year = datetime.now().year

  if not check_dir(cot_reports_dir):
    print(f"Directory {cot_reports_dir} not exists, creating...")
    os.mkdir(cot_reports_dir)

  if dnld_type == "init":
    for year in range(start_year, curr_year + 1):
      # download zip files
      if year < 2004:
        zip_filename = "deacom_xls_" + str(year) + ".zip"
      else:
        zip_filename = "dea_com_xls_" + str(year) + ".zip"
      
      xls_filename = "deacom_xls_" + str(year) + ".xls"
      
      url = config.cot_report_url + zip_filename
      print(f"Downloading {zip_filename}")
      zip_data = requests.get(url, headers=config.headers)
      open(cot_reports_dir + "\\" + zip_filename, "wb").write(zip_data.content)
      unarchive_remove(cot_reports_dir, zip_filename, xls_filename)
     
  elif dnld_type == "delta":
    
    # check if file for the current year already exists
    xls_filename = "deacom_xls_" + str(curr_year) + ".xls"
    if os.path.isfile(cot_reports_dir + "\\" + xls_filename):
      print(f"Removing existing excel file {xls_filename}")
      os.remove(cot_reports_dir + "\\" + xls_filename)
    
    # download new file
    zip_filename = "dea_com_xls_" + str(curr_year) + ".zip"
    url = config.cot_report_url + zip_filename
    print(f"Downloading {zip_filename}")
    zip_data = requests.get(url, headers=config.headers)
    open(cot_reports_dir + "\\" + zip_filename, "wb").write(zip_data.content)

    # unarchive and remove
    print(f"Unzipping and removing {zip_filename}")
    unarchive_remove(cot_reports_dir, zip_filename, xls_filename)


if __name__ == '__main__':
  #oi_download()

  #print(os.path.basename('E:\Forex\cme_reports\oi_reports\agricultural\oi_agricultural_20210313.xls'))
  #print(find_latest_file('E:\\Forex\\cme_reports\\oi_reports\\agricultural'))
  #parse_date('E:\Forex\cme_reports\oi_reports\energy\oi_energy_20210307.xls')

  #oi_download('delta')
  #print(type(os.path.getsize('E:\\Forex\\cme_reports\\oi_reports\\energy\\oi_energy_20210314.xls')))

  #print(datetime.today().weekday())
  #print(preliminary_check('E:\Forex\cme_reports\oi_reports\energy\oi_forex_20210312.xls'))

  #file = "E:\\Forex\\cme_reports\\cot_reports\\dea_com_xls_2021.zip"
  #zip_data = zipfile.ZipFile(file)
  #zipinfo = zip_data.namelist()[0]
  #print(zipinfo)


  #path = re.search(r'(.*)\\.*\.zip', "E:\\Forex\\cme_reports\\cot_reports\\dea_com_xls_2021reteer.zip")
  #print(path.group(1))

  #oi_download('delta')
  #print("==========================================================================================================================================")
  #cot_download("delta")

  #data = requests.get("https://www.cmegroup.com/CmeWS/exp/voiProductsViewExport.ctl?media=xls&tradeDate=20210325&assetClassId=8&reportType=F&excluded=CEE,CEU,KCB")
  #data = requests.get("https://www.cftc.gov/files/dea/history/deacom_xls_2004.zip")

  proxies = {
    'http': 'http://60.234.24.162:3128',
    'https': 'https://60.234.24.162:3128'
  }

  session = requests.Session()
  #session.proxies.update(proxies)
  session.auth = ('pilll2@bk.ru', 'Silent42466')
  data = session.get('https://www.cmegroup.com/CmeWS/exp/voiProductsViewExport.ctl?media=xls&tradeDate=20210323&assetClassId=8&reportType=F&excluded=CEE,CEU,KCB', \
    timeout=3, \
    headers = {'User-Agent': 'Mozilla/5.0'})

  #import urllib.request
  #response = urllib.request.urlretrieve('https://www.cmegroup.com/CmeWS/exp/voiProductsViewExport.ctl?media=xls&tradeDate=20210326&assetClassId=8&reportType=P&excluded=CEE,CEU,KCB', \
  #   headers={'User-Agent': 'Mozilla/5.0'})