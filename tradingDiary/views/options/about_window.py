from PyQt5.QtWidgets import (
  QHBoxLayout,
  QLabel,
  QWidget
)

class optionsAboutWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.mainLayout = QHBoxLayout()
    self.setLayout(self.mainLayout)
    AboutLabel = QLabel()
    AboutLabel.setText('This is Trading Diary')
    self.mainLayout.addWidget(AboutLabel)