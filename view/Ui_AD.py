# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\zhuima\Desktop\quantum\ui\AD.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(617, 634)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 10, 131, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 300, 131, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.startCalcBtn = QtWidgets.QPushButton(Form)
        self.startCalcBtn.setGeometry(QtCore.QRect(480, 580, 111, 41))
        self.startCalcBtn.setObjectName("startCalcBtn")
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setGeometry(QtCore.QRect(320, 580, 141, 41))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.label_3 = QtWidgets.QLabel(self.splitter)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.splitter)
        self.doubleSpinBox.setDecimals(1)
        self.doubleSpinBox.setMinimum(0.2)
        self.doubleSpinBox.setMaximum(0.9)
        self.doubleSpinBox.setSingleStep(0.1)
        self.doubleSpinBox.setProperty("value", 0.3)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.calcProgressBar = QtWidgets.QProgressBar(Form)
        self.calcProgressBar.setGeometry(QtCore.QRect(120, 290, 411, 41))
        self.calcProgressBar.setMaximum(0)
        self.calcProgressBar.setProperty("value", -1)
        self.calcProgressBar.setFormat("")
        self.calcProgressBar.setObjectName("calcProgressBar")
        self.normalTableView = QtWidgets.QTableView(Form)
        self.normalTableView.setGeometry(QtCore.QRect(20, 50, 581, 231))
        self.normalTableView.setObjectName("normalTableView")
        self.abnormalTableView = QtWidgets.QTableView(Form)
        self.abnormalTableView.setGeometry(QtCore.QRect(20, 350, 581, 211))
        self.abnormalTableView.setObjectName("abnormalTableView")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "正常用户"))
        self.label_2.setText(_translate("Form", "异常用户"))
        self.startCalcBtn.setText(_translate("Form", "重新生成"))
        self.label_3.setText(_translate("Form", "阈值："))
