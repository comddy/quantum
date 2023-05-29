from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from view.Ui_FuturePrice import Ui_Form

class FuturePriceInterface(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.labelStartPrice.setText(f'{self.input1.text()}（元）')
        self.input1.textChanged.connect(self.handleTextChanged)

    def handleTextChanged(self):
        self.labelStartPrice.setText(f'{self.input1.text()}（元）')

