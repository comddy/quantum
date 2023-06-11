from view.Ui_Prediction_Dialog_1 import Ui_Dialog
from PyQt5.QtWidgets import QDialog
import pandas as pd
from QuantumSpear.QuantumFinance import QuantumFinance
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets

class PredictionDialog1(QDialog):
    """Employee dialog."""
    def __init__(self, filepath, parent=None):
        super().__init__(parent)
        # Create an instance of the GUI
        self.ui = Ui_Dialog()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)
        df = pd.read_excel(filepath)
        beginDate = [int(i) for i in df.iloc[0,0].strftime('%Y-%m-%d').split('-')]
        endDate = [int(i) for i in df.iloc[-1,0].strftime('%Y-%m-%d').split('-')]
        self.ui.dateEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(beginDate[0], beginDate[1], beginDate[2]), QtCore.QTime(0, 0, 0)))
        self.ui.dateEdit.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(beginDate[0], beginDate[1], beginDate[2]), QtCore.QTime(0, 0, 0)))
        self.ui.dateEdit.setMaximumDateTime(QtCore.QDateTime(QtCore.QDate(endDate[0], endDate[1], endDate[2]), QtCore.QTime(0, 0, 0)))
        
        self.ui.dateEdit_2.setDateTime(QtCore.QDateTime(QtCore.QDate(endDate[0], endDate[1], endDate[2]), QtCore.QTime(0, 0, 0)))
        self.ui.dateEdit_2.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(beginDate[0], beginDate[1], beginDate[2]), QtCore.QTime(0, 0, 0)))
        self.ui.dateEdit_2.setMaximumDateTime(QtCore.QDateTime(QtCore.QDate(endDate[0], endDate[1], endDate[2]), QtCore.QTime(0, 0, 0)))
        self.setWindowTitle("设置计算时间段")  # Set the window title.  This is optional.  It is only here for show() compatibility.  If you
        # self.ui.btnOk.clicked.connect(self.start)
        self.ui.pushButton.clicked.connect(self.close)



