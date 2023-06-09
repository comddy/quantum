# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget
from view.Ui_FutureResult import Ui_Dialog
from PyQt5.QtWidgets import QDialog


class FutureResult(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("期权计算结果")


