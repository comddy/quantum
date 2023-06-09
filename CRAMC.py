# coding:utf-8
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget
from view.Ui_CRAMC import Ui_Form
import pandas as pd
from core.CRAMAAlgorithm import calculate_portfolio_var_cvar
from CRAMCResult import Draw
import random

class Thread(QtCore.QThread):

    trigger = QtCore.pyqtSignal()

    def __init__(self, func, todo:str=None) -> None:
        super(Thread, self).__init__()
        self.func = func
        self.todo = todo

    def run(self):
        res = self.func()
        if self.todo == 'graph':
            self.trigger.emit()

class CRAMCInterface(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("CRAMC")
        self.calcProgressBar.setRange(0,0)
        self.calcProgressBar.hide()

        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)		#设置策略为自定义菜单
        self.tableView.customContextMenuRequested.connect(self.ContextMenu)	#菜单内容回应信号槽
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch) #表头自适应铺满
        self.tableView.verticalHeader().setVisible(False) #竖直表头不可见
        self.tableView.setShowGrid(False) # 网格线条不可见
        self.tableView.horizontalHeader().setHighlightSections(False) #表头不塌
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.comboBox.addItems(['Pr(default)', 'Pr(CCC)', 'Pr(B)', 'Pr(BB)','Pr(BBB)','Pr(A)','Pr(AA)','Pr(AAA)',\
            'L(default)','L(CCC)','L(B)','L(BB)','L(BBB)','L(A)','L(AA)','L(AAA)'
            ])
        
        self.initData()

        self.resetBtn.clicked.connect(lambda: (self.listModel.clear(), self.startCalcBtn.setDisabled(True)))
        self.startCalcBtn.clicked.connect(self.startCalc)
    def showResult(self, d=None):
        self.draw = Draw()
        self.draw.show()
    def startCalc(self):
        def task():
            rank = self.comboBox.currentText()
            choosen = []
            sum_value = 0
            print(self.listModel.all())
            for idx in self.listModel.all():
                row = self.data.iloc[int(idx)-1]
                choosen.append({'Value':row['Value'],
                       'vol':random.uniform(0, 0.1),
                       'p_0':row[rank],
                       'rho':row['Beta (Sensitivity to Credit Driver)'],
                       'recovery_rate':row['Expected Recovery Rate'],
                       'notional': row['Value']})
                sum_value += row['Value']
                
            portfolios = {
                'name': 'A',
                'allocations': [round(i['Value']/sum_value, 6) for i in choosen],
                'assets': choosen
            }
            num_simulations = 10000
            z_max = 10
            calculate_portfolio_var_cvar(portfolios, num_simulations, z_max)
            
        self.calcThread = Thread(task, 'graph')
        self.calcThread.trigger.connect(self.showResult)
        self.calcThread.started.connect(lambda:(self.setDisabled(True),self.calcProgressBar.show()))
        self.calcThread.finished.connect(lambda:(self.setDisabled(False),self.calcProgressBar.hide()))
        self.calcThread.start() 		# 执行任务的线程程序。


    def initData(self):		#初始化数据，画网格，画出计算单元格条纹，画计算
        self.listModel = ListModel([])
        self.listView.setModel(self.listModel)

        self.data = pd.read_csv('data/cramc/data.csv')
        data = self.data.iloc[:,[0,1,2,4]].values.tolist()
        tableModel = TableModel(data)
        self.tableView.setModel(tableModel)

    def listAdd(self, val):
        if not self.listModel.contain(val):
            self.listModel.add(val)
            count = self.listModel.rowCount(0)
            if count >= 3:
                self.startCalcBtn.setDisabled(False)

    def ContextMenu(self):
        self.tableView.contextMenu = QtWidgets.QMenu()             #初始化tableView菜单
        actionAdd = self.tableView.contextMenu.addAction(u"添加")        #添加菜单内容
        
        pos = self.tableView.mapFromGlobal(QtGui.QCursor.pos())		#获取表格中鼠标坐标
        col = self.tableView.columnAt(pos.x())					#根据鼠标坐标获取列号
        row = self.tableView.currentIndex().row()               #获取行号
        model = self.tableView.model()
        Temp = model.item(row)                     #根据行号列号获取内容

        actionAdd.triggered.connect(lambda: self.listAdd(Temp))
        self.tableView.contextMenu.popup(QtGui.QCursor.pos())	         #根据鼠标坐标显示右击菜单
        self.tableView.contextMenu.show()
        

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        self._header = ['Counterparty ID', 'Credit Risk Driver', 'Beta', 'Value']

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value, float):
                return round(value, 2)
            else:
                return value
        if role == Qt.ForegroundRole:
            value = self._data[index.row()][index.column()]
            
        # if role == Qt.DecorationRole:
        #     value = self._data.iloc[index.row()][index.column()]
        #     if(index.column() == self.columnCount(index.column())-1):
        #         return QPixmap("resource/images/icons/Add_black.svg")
        if role == Qt.TextAlignmentRole:
            #if(index.column() == self.columnCount(index.column())-1):
            return Qt.AlignHCenter

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def item(self, r, c):
        return self._data[r][c]
    
    def item(self, r):
        return self._data[r]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._header[section])


class ListModel(QtCore.QAbstractListModel):
    def __init__(self, data=None):
        super(ListModel, self).__init__()
        self._data = data or []
        self._showData = []
        
    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._showData[index.row()]
    def add(self, val):
        self._data.append(val)
        self._showData.append(val[0])
        self.layoutChanged.emit()
    
    def remove(self, index):
        self._data.pop(index)
        self.layoutChanged.emit()
    
    def clear(self):
        self._data = []
        self._showData = []
        self.layoutChanged.emit()

    def item(self, index):
        return self._data[index]

    def contain(self, item):
        if item[0] in self._showData:
            return True
        else:
            return False

    def all(self):
        return self._showData

    def rowCount(self, index):
        return len(self._data)