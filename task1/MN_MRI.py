# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MN_MRI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(678, 435)
        Form.setMinimumSize(QtCore.QSize(678, 435))
        Form.setMaximumSize(QtCore.QSize(678, 435))
        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setGeometry(QtCore.QRect(20, 380, 651, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.lab_original = QtWidgets.QLabel(Form)
        self.lab_original.setGeometry(QtCore.QRect(10, 20, 321, 271))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lab_original.setFont(font)
        self.lab_original.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_original.setObjectName("lab_original")
        self.lab_Fourier = QtWidgets.QLabel(Form)
        self.lab_Fourier.setGeometry(QtCore.QRect(340, 20, 321, 271))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lab_Fourier.setFont(font)
        self.lab_Fourier.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_Fourier.setObjectName("lab_Fourier")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(20, 310, 621, 51))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pb_browse = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pb_browse.setFont(font)
        self.pb_browse.setObjectName("pb_browse")
        self.horizontalLayout.addWidget(self.pb_browse)
        self.spinBox = QtWidgets.QSpinBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox.sizePolicy().hasHeightForWidth())
        self.spinBox.setSizePolicy(sizePolicy)
        self.spinBox.setMinimum(0)
        self.spinBox.setMaximum(64)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        self.pb_start = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pb_start.setFont(font)
        self.pb_start.setObjectName("pb_start")
        self.horizontalLayout.addWidget(self.pb_start)
        self.pb_pause = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pb_pause.setFont(font)
        self.pb_pause.setObjectName("pb_pause")
        self.horizontalLayout.addWidget(self.pb_pause)
        self.pb_resume = QtWidgets.QPushButton(self.widget)
        self.pb_resume.setObjectName("pb_resume")
        self.horizontalLayout.addWidget(self.pb_resume)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lab_original.setText(_translate("Form", "Orignal Photo"))
        self.lab_Fourier.setText(_translate("Form", "Fourier"))
        self.pb_browse.setText(_translate("Form", "Browse"))
        self.pb_start.setText(_translate("Form", "Start"))
        self.pb_pause.setText(_translate("Form", "Pause"))
        self.pb_resume.setText(_translate("Form", "Resume"))

