# coding:utf-8
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QMouseEvent
from PyQt5.QtWidgets import QApplication, QWidget
from view.Ui_Main import Ui_Form
from Invest import InvestInterface
from FuturePrice import FuturePriceInterface

        

class MainWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Quantum Spear")
        self.invest = InvestInterface()
        self.futurePrice = FuturePriceInterface()
        self.frame1.mousePressEvent = lambda a0: self.toggle_window(self.invest)
        self.frame2.mousePressEvent = lambda a0: self.toggle_window(self.futurePrice)

    def toggle_window(self,window):
        if window.isVisible():
            window.hide()
        else:
            window.show()
    
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        sys.exit(0)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap('resource/loading.gif'))
    splash.show()
    splash.showMessage('正在加载...')
    w = MainWindow()
    # w.setWindowFlags(w.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
    w.show()
    # w.setWindowFlags(w.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
    splash.close()
    app.exec_()

