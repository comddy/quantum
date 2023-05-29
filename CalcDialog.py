from view.Ui_CalcDialog import Ui_Dialog
from PyQt5.QtWidgets import QDialog
import pandas as pd
from QuantumSpear.QuantumFinance import QuantumFinance


class CalcDialog(QDialog):
    """Employee dialog."""
    def __init__(self, parent=None):
        super().__init__(parent)
        # Create an instance of the GUI
        self.ui = Ui_Dialog()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)
        self.setWindowTitle("开始计算")  # Set the window title.  This is optional.  It is only here for show() compatibility.  If you
        # self.ui.btnOk.clicked.connect(self.start)
        self.ui.btnCancel.clicked.connect(self.close)
        self.ui.comboBox.addItems(['均衡性', '激进型', '保守型'])
        self.score = [0.5,0.7,0.3]
        
    