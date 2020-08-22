# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nu.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(697, 589)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(10, 450, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(9, 476, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.spinBox_TE = QtWidgets.QSpinBox(Form)
        self.spinBox_TE.setGeometry(QtCore.QRect(10, 510, 37, 20))
        self.spinBox_TE.setObjectName("spinBox_TE")
        self.spinBox_FA = QtWidgets.QSpinBox(Form)
        self.spinBox_FA.setGeometry(QtCore.QRect(10, 540, 37, 20))
        self.spinBox_FA.setObjectName("spinBox_FA")
        self.phantom1 = QtWidgets.QLabel(Form)
        self.phantom1.setGeometry(QtCore.QRect(9, 9, 261, 261))
        self.phantom1.setObjectName("phantom1")
        self.phantom2 = QtWidgets.QLabel(Form)
        self.phantom2.setGeometry(QtCore.QRect(420, 40, 251, 221))
        self.phantom2.setObjectName("phantom2")
        self.phantom3 = QtWidgets.QLabel(Form)
        self.phantom3.setGeometry(QtCore.QRect(210, 330, 321, 231))
        self.phantom3.setObjectName("phantom3")
        self.comboBox_sp = QtWidgets.QComboBox(Form)
        self.comboBox_sp.setGeometry(QtCore.QRect(100, 500, 69, 22))
        self.comboBox_sp.setObjectName("comboBox_sp")
        self.comboBox_sp.addItem("")
        self.comboBox_sp.addItem("")
        self.comboBox_sp.addItem("")
        self.comboBox_sp.addItem("")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "PushButton"))
        self.pushButton_2.setText(_translate("Form", "PushButton"))
        self.phantom1.setText(_translate("Form", "TextLabel"))
        self.phantom2.setText(_translate("Form", "TextLabel"))
        self.phantom3.setText(_translate("Form", "TextLabel"))
        self.comboBox_sp.setItemText(0, _translate("Form", "O.Array"))
        self.comboBox_sp.setItemText(1, _translate("Form", "T1"))
        self.comboBox_sp.setItemText(2, _translate("Form", "T2"))
        self.comboBox_sp.setItemText(3, _translate("Form", "PD"))


