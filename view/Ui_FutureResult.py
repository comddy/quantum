# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\zhuima\Desktop\quantum\ui\FutureResult.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(390, 220)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(390, 220))
        Dialog.setMaximumSize(QtCore.QSize(390, 220))
        Dialog.setSizeGripEnabled(True)
        Dialog.setModal(True)
        self.splitter = QtWidgets.QSplitter(Dialog)
        self.splitter.setGeometry(QtCore.QRect(40, 180, 201, 31))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.label_9 = QtWidgets.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(140, 10, 161, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 50, 231, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 90, 261, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 130, 201, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 170, 221, 31))
        self.label_4.setObjectName("label_4")
        self.r1 = QtWidgets.QLabel(Dialog)
        self.r1.setGeometry(QtCore.QRect(240, 50, 181, 31))
        self.r1.setObjectName("r1")
        self.r2 = QtWidgets.QLabel(Dialog)
        self.r2.setGeometry(QtCore.QRect(270, 90, 151, 31))
        self.r2.setObjectName("r2")
        self.r3 = QtWidgets.QLabel(Dialog)
        self.r3.setGeometry(QtCore.QRect(200, 130, 151, 31))
        self.r3.setObjectName("r3")
        self.r4 = QtWidgets.QLabel(Dialog)
        self.r4.setGeometry(QtCore.QRect(230, 170, 151, 31))
        self.r4.setObjectName("r4")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_9.setText(_translate("Dialog", "期权计算结果"))
        self.label.setText(_translate("Dialog", "自构建线路期权定价量子算法解："))
        self.label_2.setText(_translate("Dialog", "Qiskit内置算法期权定价量子算法解："))
        self.label_3.setText(_translate("Dialog", "期权delta风险参数数值解："))
        self.label_4.setText(_translate("Dialog", "期权delta风险参数量子算法解："))
        self.r1.setText(_translate("Dialog", "r1"))
        self.r2.setText(_translate("Dialog", "r2"))
        self.r3.setText(_translate("Dialog", "r3"))
        self.r4.setText(_translate("Dialog", "r4"))
