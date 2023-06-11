from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from view.Ui_Prediction import Ui_Form
# from CalcDialog import CalcDialog
from Prediction_Dialog_1 import PredictionDialog1
from Prediction_Dialog_2 import PredictionDialog2
import pandas as pd
import numpy as np
import os
from QuantumSpear.QuantumFinance import QuantumFinance
from CalcResult import ResultGraph, PieChartDialog, Example
from time import sleep

import sys, os, csv
sys.path.append('.\queueing-rnn-master\examples')
sys.path.append('.\queueing-rnn-master')
from stock_price_qrnn import stock_price_qrnn


import pandas as pd
from datetime import datetime

class Stock_Forecast(QtCore.QThread):
    def __init__(self,name,input_file_path,start_time,end_time,cache_save_path,type_name,type_id,png_save_path):
        super().__init__()
        self.name=name
        self.input_file_path=input_file_path
        self.start_time=start_time
        self.end_time=end_time
        self.cache_save_path=cache_save_path
        self.type_name = type_name
        self.type_id=type_id
        self.png_save_path=png_save_path

    def convert_date_format(self,file_path):
        # 读取csv文件
        df = pd.read_csv(file_path)
        # 将Date列转换为datetime类型，并格式化为mm/dd/yyyy的格式
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%m/%d/%Y')
        # 将数据写入csv文件
        df.to_csv(file_path, index=False)

    def split_csv_file(self,input_file_path, start_time, end_time, train_file_path, test_file_path):
        # 读取csv文件
        file_extension = os.path.splitext(input_file_path)[1]
        # 根据文件扩展名读取文件
        if file_extension == '.csv':
            df = pd.read_csv(input_file_path)
        elif file_extension == '.xlsx':
            df = pd.read_excel(input_file_path)
        else:
            raise ValueError('Unsupported file type: {}'.format(file_extension))
        # # 将Date列转换为datetime类型
        # df['date'] = pd.to_datetime(df['date'])
        # 将Date列转换为datetime类型，并格式化为月/日/年的格式
        df['date'] = pd.to_datetime(df['date'])

        # 根据开始时间和结束时间筛选数据
        df = df[(df['date'] >= start_time) & (df['date'] <= end_time)]
        # 随机打乱数据
        df = df.sample(frac=1).reset_index(drop=True)
        df['volume'] = 0
        # 计算训练集和测试集的切分点
        split_point = int(len(df) * 0.8)
        # 将数据切分为训练集和测试集
        train_df = df[:split_point]
        train_df = train_df.sort_values(by=['date'])
        test_df = df[split_point:]
        test_df = test_df.sort_values(by=['date'])
        # 将训练集和测试集写入csv文件
        train_df.to_csv(train_file_path, index=False)
        test_df.to_csv(test_file_path, index=False)
        self.convert_date_format(train_file_path)
        self.convert_date_format(test_file_path)

    def parse_time(self,date_str, date_format='%Y-%m-%d'):
        # 将时间形参转换为datetime类型
        date_obj = datetime.strptime(date_str, date_format)
        return date_obj

    def count_csv_rows(self,file_path):
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            # 跳过表头行
            next(reader)
            # 计算行数
            row_count = sum(1 for row in reader)
        # print(f"文件{file_path}的行数为:{row_count}")
        return row_count

    def type_name_conversion(self,type_name):

        if type == "开盘价":
            str = "open"
            return str
        elif type == "最高价":
            str="high"
            return str
        elif type == "最低价":
            str="low"
            return str
        elif type == "收盘价":
            str="close"
            return str



    def run(self):

        start_time = self.parse_time(self.start_time)

        end_time = self.parse_time(self.end_time)
        run_path = os.getcwd()
        self.input_file_path=run_path +self.input_file_path
        self.cache_save_path=run_path +self.cache_save_path
        self.png_save_path=run_path+self.png_save_path

        self.split_csv_file(self.input_file_path, start_time, end_time,f"{self.cache_save_path}train.csv",f"{self.cache_save_path}test.csv")
        # from script.queueing_rnn_master.examples.stock_price_qrnn import stock_price_qrnn

        # def stock_price_qrnn(name,train_path,train_num,test_path,test_num,type,type_number,save_path):
        
        if self.type_name == "开盘价":
            self.type_name = "open"

        elif self.type_name == "最高价":
            self.type_name="high"

        elif self.type_name == "最低价":
            self.type_name="low"

        elif self.type_name == "收盘价":
            self.type_name="close"


        stock_price_qrnn(self.name,f"{self.cache_save_path}train.csv", self.count_csv_rows(f"{self.cache_save_path}train.csv"),f"{self.cache_save_path}test.csv", self.count_csv_rows(f"{self.cache_save_path}test.csv") + 60, self.type_name,self.type_id+2,self.png_save_path)

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
            # if(index.column() == self.columnCount(index.column())-1):
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


class PredictionInterface(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnActiveStyle = "background-color:#4d85ff;color:white;"
        self.stockType = "main"
        self.df = pd.read_excel("./data/invest/A股股票.xlsx", converters={'code': str})
        self.setWindowTitle("股票价格预测")
        self.stock_id=""
        self.stock_name=""
        self.pushButton.clicked.connect(self.startCalc)  # 调用Dialog1
        self.calcProgressBar.hide()

        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)  # 设置策略为自定义菜单
        self.tableView.customContextMenuRequested.connect(self.ContextMenu)  # 菜单内容回应信号槽
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)  # 表头自适应铺满
        self.tableView.verticalHeader().setVisible(False)  # 竖直表头不可见
        self.tableView.setShowGrid(False)  # 网格线条不可见
        self.tableView.horizontalHeader().setHighlightSections(False)  # 表头不塌
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.initData()  # 导入数据
        self.comboBox.addItems(['开盘价', '最高价', '最低价','收盘价'])

    def startCalc(self):
        self.PredDialog = PredictionDialog1(f"./data/invest/{self.stockType}/{self.stock_id}.xlsx")
        self.PredDialog.ui.pushButton.clicked.connect(lambda: self.start(self.PredDialog))
        self.PredDialog.exec_()

    def initData(self):
        self.lastBtn_clicked()

    def lastBtn_clicked(self):
        self.tableView.setDisabled(True)

        def task():
            data = pd.read_excel(f'./data/invest/{self.stockType}.xlsx', converters={'股票代码': str})
            # print(data)
            data = data.values.tolist()
            # print("转换后:")
            # print(data)
            tableModel = TableModel(data)
            self.tableView.setModel(tableModel)
            # print(dir(self.tableView))
            self.tableView.setDisabled(False)

        self.thread = Thread(task)

        self.thread.start()  # 执行任务的线程程序

        # self.StockForecast = Stock_Forecast()
        # self.thread.started.connect(lambda:self.progressBar.show())
        # self.thread.finished.connect(lambda:self.progressBar.hide())
        #
        # self.StockForecast.start()  # 执行任务的线程程序。

    def ContextMenu(self):
        self.tableView.contextMenu = QtWidgets.QMenu()  # 初始化tableView菜单
        actionAdd = self.tableView.contextMenu.addAction(u"选择")  # 添加菜单内容

        pos = self.tableView.mapFromGlobal(QtGui.QCursor.pos())  # 获取表格中鼠标坐标
        col = self.tableView.columnAt(pos.x())  # 根据鼠标坐标获取列号
        row = self.tableView.currentIndex().row()  # 获取行号
        model = self.tableView.model()
        # print("model="+model)
        Temp = model.item(row)  # 根据行号列号获取内容
        # print("Temp=" + Temp)
        Temp.append(self.stockType)
        actionAdd.triggered.connect(lambda: self.chooseStock(Temp))
        self.tableView.contextMenu.popup(QtGui.QCursor.pos())  # 根据鼠标坐标显示右击菜单
        self.tableView.contextMenu.show()

    def chooseStock(self, val):
        self.stock_id=val[1]
        self.stock_name=val[2]
        self.lineEdit.setText(val[2])

    def start(self, w):
        w.close()

        self.start_time=self.PredDialog.ui.dateEdit.date().toString("yyyy-MM-dd")#获取开始时间
        self.end_time=self.PredDialog.ui.dateEdit_2.date().toString("yyyy-MM-dd")#获取结束时间
        self.stockType_name = self.comboBox.currentText()  # 获取选项文本
        self.stockType_id=self.comboBox.currentIndex()#获取类型序号
        self.png_save_path=f"./data/Cache/"

        self.StockForecast=Stock_Forecast(name=self.stock_name,input_file_path=f"./data/invest/{self.stockType}/{self.stock_id}.xlsx",start_time=self.start_time,end_time=self.end_time,cache_save_path=f"./data/Cache/",type_name=self.stockType_name,type_id=self.stockType_id,png_save_path=self.png_save_path)
        self.StockForecast.start()
        self.StockForecast.started.connect(lambda:(self.setDisabled(True),self.calcProgressBar.show()))
        self.StockForecast.finished.connect(lambda:(self.run_Dialog2(),self.setDisabled(False),self.calcProgressBar.hide()))

    def run_Dialog2(self):
        self.PredDialog_2=PredictionDialog2()
        png_save_path=os.getcwd() +self.png_save_path
        Stock_Price_Training_Loss_img = os.path.abspath(png_save_path+"Stock_Price_Training_Loss.png")
        Stocking_Price_Test_Set_img = os.path.abspath(png_save_path + "Stocking_Price_Test_Set.png")
        Sharing_Data_Training_Set_img = os.path.abspath(png_save_path + "Sharing_Data_Training_Set.png")
        image1 = QtGui.QPixmap(Stock_Price_Training_Loss_img).scaled(600, 400)
        image2 = QtGui.QPixmap(Stocking_Price_Test_Set_img).scaled(600, 400)
        image3 = QtGui.QPixmap(Sharing_Data_Training_Set_img).scaled(600, 400)
        self.PredDialog_2.ui.label.setPixmap(image1)
        self.PredDialog_2.ui.label_2.setPixmap(image2)
        self.PredDialog_2.ui.label_3.setPixmap(image3)
        self.PredDialog_2.show()


