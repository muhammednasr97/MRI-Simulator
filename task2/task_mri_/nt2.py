# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nt2.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(566, 433)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.graphicsView_t1 = PlotWidget(self.tab)
        self.graphicsView_t1.setObjectName("graphicsView_t1")
        self.gridLayout_2.addWidget(self.graphicsView_t1, 0, 3, 1, 3)
        self.graphicsView_t2 = PlotWidget(self.tab)
        self.graphicsView_t2.setObjectName("graphicsView_t2")
        self.gridLayout_2.addWidget(self.graphicsView_t2, 1, 3, 1, 3)
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 2, 0, 1, 1)
        self.comboBox_sp = QtWidgets.QComboBox(self.tab)
        self.comboBox_sp.setObjectName("comboBox_sp")
        self.comboBox_sp.addItem("")
        self.comboBox_sp.addItem("")
        self.comboBox_sp.addItem("")
        self.comboBox_sp.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_sp, 2, 1, 1, 1)
        self.spinBox_TR = QtWidgets.QSpinBox(self.tab)
        self.spinBox_TR.setObjectName("spinBox_TR")
        self.gridLayout_2.addWidget(self.spinBox_TR, 2, 2, 1, 1)
        self.spinBox_TE = QtWidgets.QSpinBox(self.tab)
        self.spinBox_TE.setObjectName("spinBox_TE")
        self.gridLayout_2.addWidget(self.spinBox_TE, 2, 3, 1, 1)
        self.spinBox_FA = QtWidgets.QSpinBox(self.tab)
        self.spinBox_FA.setObjectName("spinBox_FA")
        self.gridLayout_2.addWidget(self.spinBox_FA, 2, 4, 1, 1)
        self.spinBox_time = QtWidgets.QSpinBox(self.tab)
        self.spinBox_time.setObjectName("spinBox_time")
        self.gridLayout_2.addWidget(self.spinBox_time, 2, 5, 1, 1)
        self.phantom1 = QtWidgets.QLabel(self.tab)
        self.phantom1.setScaledContents(True)
        self.phantom1.setAlignment(QtCore.Qt.AlignCenter)
        self.phantom1.setObjectName("phantom1")
        self.gridLayout_2.addWidget(self.phantom1, 0, 0, 1, 3)
        self.phantom2 = QtWidgets.QLabel(self.tab)
        self.phantom2.setScaledContents(True)
        self.phantom2.setAlignment(QtCore.Qt.AlignCenter)
        self.phantom2.setObjectName("phantom2")
        self.gridLayout_2.addWidget(self.phantom2, 1, 0, 1, 3)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.i = QtWidgets.QLabel(self.tab_2)
        self.i.setScaledContents(True)
        self.i.setAlignment(QtCore.Qt.AlignCenter)
        self.i.setObjectName("i")
        self.gridLayout_3.addWidget(self.i, 0, 0, 1, 1)
        self.kspace = QtWidgets.QLabel(self.tab_2)
        self.kspace.setScaledContents(True)
        self.kspace.setAlignment(QtCore.Qt.AlignCenter)
        self.kspace.setObjectName("kspace")
        self.gridLayout_3.addWidget(self.kspace, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Browse"))
        self.comboBox_sp.setItemText(0, _translate("Form", "O.Array"))
        self.comboBox_sp.setItemText(1, _translate("Form", "T1"))
        self.comboBox_sp.setItemText(2, _translate("Form", "T2"))
        self.comboBox_sp.setItemText(3, _translate("Form", "PD"))
        self.phantom1.setText(_translate("Form", "phantom1"))
        self.phantom2.setText(_translate("Form", "phantom2"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Tab 1"))
        self.i.setText(_translate("Form", "image"))
        self.kspace.setText(_translate("Form", "Kspace"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Tab 2"))


from pyqtgraph import PlotWidget
