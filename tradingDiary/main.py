import sys
from tradingDiary.database import createConnection

from PyQt5.QtWidgets import QApplication
from .views import Window
from .database import createConnection

def main():
  app = QApplication(sys.argv)

  if not createConnection("E:\\Forex\\cme_reports\\trading.db"):
    sys.exit(1)

  win = Window()
  win.show()
  sys.exit(app.exec())