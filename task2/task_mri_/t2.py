# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 't2.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(850, 630)
        self.comboBox_sp = QtWidgets.QComboBox(Form)
        self.comboBox_sp.setGeometry(QtCore.QRect(360, 540, 101, 22))
        self.comboBox_sp.setObjectName("comboBox_sp")
        self.comboBox_sp.addItem("")
        self.comboBox_sp.addItem("")
        self.comboBox_sp.addItem("")
        self.comboBox_sp.addItem("")
        self.spinBox_TR = QtWidgets.QSpinBox(Form)
        self.spinBox_TR.setGeometry(QtCore.QRect(490, 540, 42, 22))
        self.spinBox_TR.setObjectName("spinBox_TR")
        self.spinBox_FA = QtWidgets.QSpinBox(Form)
        self.spinBox_FA.setGeometry(QtCore.QRect(630, 540, 42, 22))
        self.spinBox_FA.setObjectName("spinBox_FA")
        self.spinBox_time = QtWidgets.QSpinBox(Form)
        self.spinBox_time.setGeometry(QtCore.QRect(490, 500, 42, 22))
        self.spinBox_time.setObjectName("spinBox_time")
        self.spinBox_TE = QtWidgets.QSpinBox(Form)
        self.spinBox_TE.setGeometry(QtCore.QRect(560, 540, 42, 22))
        self.spinBox_TE.setObjectName("spinBox_TE")
        self.phantom2 = QtWidgets.QLabel(Form)
        self.phantom2.setGeometry(QtCore.QRect(20, 320, 320, 280))
        self.phantom2.setAlignment(QtCore.Qt.AlignCenter)
        self.phantom2.setObjectName("phantom2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(360, 500, 101, 23))
        self.pushButton.setObjectName("pushButton")
        self.phantom1 = QtWidgets.QLabel(Form)
        self.phantom1.setGeometry(QtCore.QRect(20, 30, 320, 280))
        self.phantom1.setAlignment(QtCore.Qt.AlignCenter)
        self.phantom1.setObjectName("phantom1")
        self.graphicsView_t1_2 = PlotWidget(Form)
        self.graphicsView_t1_2.setGeometry(QtCore.QRect(370, 31, 461, 211))
        self.graphicsView_t1_2.setObjectName("graphicsView_t1_2")
        self.graphicsView_t2 = PlotWidget(Form)
        self.graphicsView_t2.setGeometry(QtCore.QRect(370, 260, 461, 211))
        self.graphicsView_t2.setObjectName("graphicsView_t2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.comboBox_sp.setItemText(0, _translate("Form", "O.Array"))
        self.comboBox_sp.setItemText(1, _translate("Form", "T1"))
        self.comboBox_sp.setItemText(2, _translate("Form", "T2"))
        self.comboBox_sp.setItemText(3, _translate("Form", "PD"))
        self.phantom2.setText(_translate("Form", "phantom"))
        self.pushButton.setText(_translate("Form", "Browse"))
        self.phantom1.setText(_translate("Form", "phantom"))

from pyqtgraph import PlotWidget
