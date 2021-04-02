# tradingDiary/database.py

"""This module provided a database connection."""

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase

def createConnection(databaseName):
  connection = QSqlDatabase.addDatabase("QSQLITE")
  connection.setDatabaseName(databaseName)

  if not connection.open():
    QMessageBox.warning(
      None,
      "Trading Diary",
      f"Database Error: {connection.lastError().text()}",
    )
    return False

  #db = QSqlDatabase.database()
  #print(db.tables())
 
  return True



