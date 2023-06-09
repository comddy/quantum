# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\zhuima\Desktop\quantum\ui\Invest.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setEnabled(True)
        Form.resize(970, 440)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(970, 440))
        Form.setMaximumSize(QtCore.QSize(970, 440))
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 20, 151, 23))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(660, 20, 120, 23))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setGeometry(QtCore.QRect(11, 60, 589, 20))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.label_2 = QtWidgets.QLabel(self.splitter)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.splitter)
        self.label_3.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.label_3.setObjectName("label_3")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(11, 88, 641, 341))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.bondBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.bondBtn.setObjectName("bondBtn")
        self.gridLayout.addWidget(self.bondBtn, 0, 2, 1, 1)
        self.stockBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.stockBtn.setObjectName("stockBtn")
        self.gridLayout.addWidget(self.stockBtn, 0, 1, 1, 1)
        self.masBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.masBtn.setObjectName("masBtn")
        self.gridLayout.addWidget(self.masBtn, 1, 4, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.layoutWidget)
        self.progressBar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 3, 0, 1, 5)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)
        self.tableView = QtWidgets.QTableView(self.layoutWidget)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 2, 0, 1, 5)
        self.createBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.createBtn.setObjectName("createBtn")
        self.gridLayout.addWidget(self.createBtn, 1, 2, 1, 1)
        self.mainBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.mainBtn.setObjectName("mainBtn")
        self.gridLayout.addWidget(self.mainBtn, 1, 1, 1, 1)
        self.futureBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.futureBtn.setObjectName("futureBtn")
        self.gridLayout.addWidget(self.futureBtn, 0, 3, 1, 1)
        self.scBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.scBtn.setObjectName("scBtn")
        self.gridLayout.addWidget(self.scBtn, 1, 3, 1, 1)
        self.listView = QtWidgets.QListView(Form)
        self.listView.setGeometry(QtCore.QRect(660, 60, 301, 311))
        self.listView.setObjectName("listView")
        self.resetBtn = QtWidgets.QPushButton(Form)
        self.resetBtn.setGeometry(QtCore.QRect(680, 380, 121, 51))
        self.resetBtn.setObjectName("resetBtn")
        self.startCalcBtn = QtWidgets.QPushButton(Form)
        self.startCalcBtn.setEnabled(False)
        self.startCalcBtn.setGeometry(QtCore.QRect(830, 380, 121, 51))
        self.startCalcBtn.setObjectName("startCalcBtn")
        self.calcProgressBar = QtWidgets.QProgressBar(Form)
        self.calcProgressBar.setGeometry(QtCore.QRect(170, 180, 639, 23))
        self.calcProgressBar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.calcProgressBar.setProperty("value", 24)
        self.calcProgressBar.setTextVisible(False)
        self.calcProgressBar.setObjectName("calcProgressBar")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "投资组合优化"))
        self.label_7.setText(_translate("Form", "已添加股票"))
        self.label_2.setText(_translate("Form", "添加股票组合"))
        self.label_3.setText(_translate("Form", "添加4只股票可启动程序，最多添加8只。（相关数据截止于2023年4月1日）"))
        self.bondBtn.setText(_translate("Form", "债券"))
        self.stockBtn.setText(_translate("Form", "股票"))
        self.masBtn.setText(_translate("Form", "中小板"))
        self.label_5.setText(_translate("Form", "投资品类"))
        self.label_6.setText(_translate("Form", "品类细分"))
        self.createBtn.setText(_translate("Form", "创业板"))
        self.mainBtn.setText(_translate("Form", "主板"))
        self.futureBtn.setText(_translate("Form", "期货"))
        self.scBtn.setText(_translate("Form", "科创板"))
        self.resetBtn.setText(_translate("Form", "重置"))
        self.startCalcBtn.setText(_translate("Form", "开始计算"))
