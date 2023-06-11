from view.Ui_Prediction_Dialog_2 import Ui_Dialog
from PyQt5.QtWidgets import QDialog
import pandas as pd
from QuantumSpear.QuantumFinance import QuantumFinance


class PredictionDialog2(QDialog):
    """Employee dialog."""
    def __init__(self, parent=None):
        super().__init__(parent)
        # Create an instance of the GUI
        self.ui = Ui_Dialog()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)
        self.setWindowTitle("预测结果")  # Set the window title.  This is optional.  It is only here for show() compatibility.  If you
        # self.ui.btnOk.clicked.connect(self.start)
