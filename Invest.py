from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from view.Ui_Invest import Ui_Form
from CalcDialog import CalcDialog
import pandas as pd
import numpy as np
import os
from QuantumSpear.QuantumFinance import QuantumFinance
from CalcResult import ResultGraph, PieChartDialog, Example
from time import sleep

class Thread(QtCore.QThread):

    trigger = QtCore.pyqtSignal(dict)

    def __init__(self, func, todo:str=None) -> None:
        super(Thread, self).__init__()
        self.func = func
        self.todo = todo

    def run(self):
        res = self.func()
        if self.todo == 'graph':
            self.trigger.emit(res)
        

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
        self._showData.append(val[2])
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
        if item[2] in self._showData:
            return True
        else:
            return False

    def all(self):
        return self._data

    def rowCount(self, index):
        return len(self._data)

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        self._header = ['序号', '股票代码', '股票名称', '涨幅']

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value, float):
                return f"{str(value)}%"
            else:
                return str(value)
        if role == Qt.ForegroundRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value, float):
                if value < 0:
                    return QtGui.QColor('green')
                else:
                    return QtGui.QColor('red')
            
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

class InvestInterface(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnActiveStyle = "background-color:#4d85ff;color:white;"
        self.stockType = "main"
        self.month = 3
        self.df = pd.read_excel("data/invest/A股股票.xlsx", converters={'code':str})
        self.setWindowTitle("Invest")
        self.progressBar.setRange(0,0)
        self.calcProgressBar.setRange(0,0)
        self.calcProgressBar.hide()
        self.startCalcBtn.clicked.connect(self.startCalc)   # start button clicked, start calculation process.

        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)		#设置策略为自定义菜单
        self.tableView.customContextMenuRequested.connect(self.ContextMenu)	#菜单内容回应信号槽
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch) #表头自适应铺满
        self.tableView.verticalHeader().setVisible(False) #竖直表头不可见
        self.tableView.setShowGrid(False) # 网格线条不可见
        self.tableView.horizontalHeader().setHighlightSections(False) #表头不塌
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        
        self.initData()
        
        
        self.listModel.dataChanged.connect(self.listView.update)
        self.resetBtn.clicked.connect(lambda: (self.listModel.clear(), self.startCalcBtn.setDisabled(True)))
        self.initStyle()
    def startCalc(self):
        self.calcDialog = CalcDialog()
        self.calcDialog.ui.btnOk.clicked.connect(lambda:self.start(self.calcDialog)) # close button clicked, close the window.
        self.calcDialog.exec()

    def showResult(self, d):
        data = {}
        names = [i[2] for i in self.listModel.all()]
        for name,value in dict(zip(names,d.values())).items():
            if value != '0%':
                value = round(float(value.replace('%','')),2) # remove % sign from value.
                data[name] = str(value)+'%'
        self.result_graph = Example(data)
        self.result_graph.show()
        # sleep(5)

    def start(self, w):
        w.close()
        # self.showResult({'深科技': '0%', '深圳能源': '0%', '深深房Ａ': '0%', '神州数码': '50.0%'})
        def task():
            data = self.listModel.all()
            columns = []
            profit_rate = []
            for idx, item in enumerate(data):
                columns.append(item[2]) #股票名
                profit_rate.append(item[3]/100)
                if idx == 0:
                    df = pd.read_excel(f'data/invest/{item[-1]}/{item[1]}.xlsx')
                else:
                    df = pd.concat([df,pd.read_excel(f'data/invest/{item[-1]}/{item[1]}.xlsx')[['close']]], axis=1)
            receive = df['close'].pct_change().dropna() # 计算收益率
            cov = receive.cov() # 计算协方差
            # cov = cov.values.tolist()
            calcData = {
                'Number': len(data),
                'Project_Name': columns,
                'Profit_rates': profit_rate,
                'Risk_Matrix': cov.values
            }
            risk_factor = self.calcDialog.score[self.calcDialog.ui.comboBox.currentIndex()]
            g = self.calcDialog.ui.spinBox.value()
            qf = QuantumFinance(return_rate=np.array(calcData['Profit_rates']),risk_matrix=calcData['Risk_Matrix'],num_assets=calcData['Number'],global_seed=10,risk_factor=risk_factor,g=g)
            qf.solve()
            # qf.run(reps=2) #使用run方法 
            # problem.explain_result()
            self.calcProgressBar.hide()
            # print(problem.answer_dict)
            return qf.result_dict
            
        self.calcThread = Thread(task, 'graph')
        self.calcThread.trigger.connect(self.showResult)
        self.calcThread.started.connect(lambda:(self.setDisabled(True),self.calcProgressBar.show()))
        self.calcThread.finished.connect(lambda:(self.setDisabled(False),self.calcProgressBar.hide()))
        self.calcThread.start() 		# 执行任务的线程程序。
        

    def initData(self):
        self.listModel = ListModel([])
        self.listView.setModel(self.listModel)
        self.lastBtn_clicked()

    def initStyle(self):
        self.stockBtn.setStyleSheet(self.btnActiveStyle)
        self.mainBtn.setStyleSheet(self.btnActiveStyle)

        self.bondBtn.setDisabled(True)
        self.futureBtn.setDisabled(True)
        self.createBtn.clicked.connect(lambda:self.changeType('create'))
        self.scBtn.clicked.connect(lambda:self.changeType('sc'))
        self.masBtn.clicked.connect(lambda:self.changeType('mas'))
        self.mainBtn.clicked.connect(lambda:self.changeType('main'))
    def changeType(self,type):
        if self.stockType == type:return
        self.stockType = type
        self.createBtn.setStyleSheet("")
        self.scBtn.setStyleSheet("")
        self.masBtn.setStyleSheet("")
        self.mainBtn.setStyleSheet("")
        self.stockType = type
        self.lastBtn_clicked()
        if type == 'create':
            self.createBtn.setStyleSheet(self.btnActiveStyle)
        elif type == 'sc':
            self.scBtn.setStyleSheet(self.btnActiveStyle)
        elif type == 'mas':
            self.masBtn.setStyleSheet(self.btnActiveStyle)
        else:
            self.mainBtn.setStyleSheet(self.btnActiveStyle)

    def lastBtn_clicked(self):
        self.tableView.setDisabled(True)
        # self.listModel.clear()

        def task():
            data = pd.read_excel(f'./data/invest/{self.stockType}.xlsx', converters={'股票代码':str})
            data = data.values.tolist()
            tableModel = TableModel(data)
            self.tableView.setModel(tableModel)
            # print(dir(self.tableView))
            self.tableView.setDisabled(False)
        self.thread = Thread(task)
        self.thread.started.connect(lambda:self.progressBar.show())
        self.thread.finished.connect(lambda:self.progressBar.hide())
        self.thread.start() 		# 执行任务的线程程序。



    def listAdd(self, val):
        if not self.listModel.contain(val):
            count = self.listModel.rowCount(0)
            if count < 8:
                self.listModel.add(val)
            count = self.listModel.rowCount(0)
            if count >= 4:
                self.startCalcBtn.setDisabled(False)

    def ContextMenu(self):
        self.tableView.contextMenu = QtWidgets.QMenu()             #初始化tableView菜单
        actionAdd = self.tableView.contextMenu.addAction(u"添加")        #添加菜单内容
        
        pos = self.tableView.mapFromGlobal(QtGui.QCursor.pos())		#获取表格中鼠标坐标
        col = self.tableView.columnAt(pos.x())					#根据鼠标坐标获取列号
        row = self.tableView.currentIndex().row()               #获取行号
        model = self.tableView.model()
        Temp = model.item(row)                     #根据行号列号获取内容
        Temp.append(self.stockType)
        actionAdd.triggered.connect(lambda: self.listAdd(Temp))
        self.tableView.contextMenu.popup(QtGui.QCursor.pos())	         #根据鼠标坐标显示右击菜单
        self.tableView.contextMenu.show()
        # print(Temp)
        # if(it == 0):											#根据列号不同,显示不同的右击菜单
        #     action1 = self.tableView.contextMenu.addAction(u"添加设备")
        #     action2 = self.tableView.contextMenu.addAction(u"修改设备名称")
        #     action3 = self.tableView.contextMenu.addAction(u"删除设备")
        #     action1.triggered.connect(lambda:self.InsertEquiSlot(Temp))
        #     action2.triggered.connect(lambda:self.ChangeEquiSlot(Temp))
        #     action3.triggered.connect(lambda:self.DeleteEquiSlot(Temp))
        # elif(it == 1):
        #     action1 = self.tableView.contextMenu.addAction(u"添加设备型号")
        #     action2 = self.tableView.contextMenu.addAction(u"修改设备型号")
        #     action3 = self.tableView.contextMenu.addAction(u"删除设备型号")
        #     action1.triggered.connect(lambda:self.InsertEquiModelSlot(Temp))
        #     action2.triggered.connect(lambda:self.ChangeEquiModelSlot(Temp))
        #     action3.triggered.connect(lambda:self.DeleteEquiModelSlot(Temp))