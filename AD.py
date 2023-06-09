# coding:utf-8
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget
from view.Ui_AD import Ui_Form
from core.AbnomalDetcationCode.anomaly_detection import anomaly_detection
import pandas as pd



class ADInterface(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self) 
        self.setWindowTitle("用户异常行为检测")
        self.init_data()
        self.startCalcBtn.clicked.connect(self.startCalc)
        self.calcProgressBar.hide()
    
    def startCalc(self):
        def task():
            threshold = self.doubleSpinBox.value()
            anomaly_detection(threshold=threshold)
            self.init_data()
        
        self.calcThread = Thread(task)
        # self.calcThread.trigger.connect(self.showResult)
        self.calcThread.started.connect(lambda:(self.setDisabled(True),self.calcProgressBar.show()))
        self.calcThread.finished.connect(lambda:(self.setDisabled(False),self.calcProgressBar.hide()))
        self.calcThread.start() 		# 执行任务的线程程序。

    def init_data(self):
        normal_data = pd.read_csv('core/AbnomalDetcationCode/classified_data.csv')
        normalTableModel = TableModel(normal_data.values.tolist())
        abnormal_data = pd.read_csv('core/AbnomalDetcationCode/out_of_threshold_data.csv')
        abnormalTableModel = TableModel(abnormal_data.values.tolist())
        self.init_table(self.normalTableView)
        self.init_table(self.abnormalTableView)
        self.normalTableView.setModel(normalTableModel)
        self.abnormalTableView.setModel(abnormalTableModel)

    def init_table(self, table):
        # table.setContextMenuPolicy(Qt.CustomContextMenu)		#设置策略为自定义菜单
        # table.customContextMenuRequested.connect(self.ContextMenu)	#菜单内容回应信号槽
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch) #表头自适应铺满
        table.verticalHeader().setVisible(False) #竖直表头不可见
        table.setShowGrid(False) # 网格线条不可见
        table.horizontalHeader().setHighlightSections(False) #表头不塌
        table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        self._header = ['序号','特征1','特征2','判别器预测']

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data[index.row()][index.column()]
            if index.column() >= 1:
                return round(value, 4)
            else:
                return value

        if role == Qt.TextAlignmentRole:
            #if(index.column() == self.columnCount(index.column())-1):
            return Qt.AlignHCenter

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        if(len(self._data) > 0):
            return len(self._data[0])
        else:
            return 0

    def item(self, r, c):
        return self._data[r][c]
    
    def item(self, r):
        return self._data[r]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._header[section])

class Thread(QtCore.QThread):

    def __init__(self, func) -> None:
        super(Thread, self).__init__()
        self.func = func

    def run(self):
        self.func()