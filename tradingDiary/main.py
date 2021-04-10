import sys

from PyQt5.QtWidgets import QApplication
from .views import Window
#from .database import createConnection
from .database import TradeDiaryDB

def main():
  app = QApplication(sys.argv)

  db = TradeDiaryDB()
  if not db.check_connection():
    sys.exit(1)

  #if not createConnection("E:\\Forex\\cme_reports\\trading.db"):
  #  sys.exit(1)

  win = Window()
  win.show()
  sys.exit(app.exec())