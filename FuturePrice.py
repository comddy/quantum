from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from view.Ui_FuturePrice import Ui_Form
from typing import List
from core.FutureAlgorithm import FutureAlgorithm
from FutureResult import FutureResult

class Thread(QtCore.QThread):

    trigger = QtCore.pyqtSignal(list)

    def __init__(self, func, todo:str=None) -> None:
        super(Thread, self).__init__()
        self.func = func
        self.todo = todo

    def run(self):
        res = self.func()
        self.trigger.emit(res)

class FuturePriceInterface(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("量子期权定价")
        self.labelStartPrice.setText(f'{self.input1.text()}（元）')
        self.input1.textChanged.connect(self.handleTextChanged)
        self.startCalcBtn.clicked.connect(self.startCalc)
        self.calcProgressBar.hide()

    def showResult(self, r:List):
        self.futureResult = FutureResult()
        r = [round(i, 4) for i in r]
        self.futureResult.ui.r1.setText(str(r[0]))
        self.futureResult.ui.r2.setText(str(r[1]))
        self.futureResult.ui.r3.setText(str(r[2]))
        self.futureResult.ui.r4.setText(str(r[3]))
        self.futureResult.exec()

    def startCalc(self):
        def task():
            val = [self.input1.value(), int(self.input2.value()*30), self.input3.value()/100, self.input4.value()/100]
            print(val)
            future = FutureAlgorithm(val[0], val[1],val[2],val[3])
            res = future.run()
            return res
        self.calcThread = Thread(task)
        self.calcThread.trigger.connect(self.showResult)
        self.calcThread.started.connect(lambda:(self.setDisabled(True),self.calcProgressBar.show()))
        self.calcThread.finished.connect(lambda:(self.setDisabled(False),self.calcProgressBar.hide()))
        self.calcThread.start() 		# 执行任务的线程程序。

    def handleTextChanged(self):
        self.labelStartPrice.setText(f'{self.input1.text()}（元）')

