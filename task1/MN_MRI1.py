from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap
from MN_MRI import Ui_Form
import cv2
import numpy as np
from dialog_box import Ui_Dialog

import sys


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # self.ui.pb_browse.setIcon(self.Ui.QtGui.QIcon('123.jpg'))
        self.ui.pb_browse.clicked.connect(self.button_clicked)

def box(cwidth, rwidth, fileName, imgwidth, imgheight):
    fileName[0:rwidth, 0:] = 0
    fileName[imgheight - rwidth:imgheight, 0:] = 0
    fileName[0:, 0:cwidth] = 0
    fileName[0:, imgwidth - cwidth:imgwidth] = 0
    return fileName
    def button_clicked(self):
         fileName, _filter = QFileDialog.getOpenFileName(self, "Title", "Default File",
                                                        "Photos Files (*.jpg);;Photos Files (*.png)" )

    if fileName:
        print(fileName)
        print(_filter)
            # self.ui.lab_original=QLabel(self)
            # self.ui.lab_original.setPixmap(QPixmap(fileName))
            # self.ui.lab_original.setGeometry(20,10,311,271)
        pixmap = QPixmap(fileName)
        image = cv2.imread(fileName, 0)
        rows, cols = image.shape
# lable= pixmap.scaled(int(pixmap.height()), int(pixmap.width()), QtCore.Qt.KeepAspectRatio)
        if rows == 512 and cols == 512 or rows==128 and cols==128 :
# pixmap = pixmap.scaled(int(pixmap.height()), int(pixmap.width()), QtCore.Qt.KeepAspectRatio)
            self.ui.lab_original.setPixmap(pixmap)
        else:
            QMessageBox.information(self, 'Message', 'The selected photo should be 128×128 or 512×512')


#self.ui.message_box()

        for i in range(int(cols / 2)):
            rows, cols = image.shape
            crow, ccol = rows / 2, cols / 2
            f = np.fft.fft2(fileName)
            fshift = np.fft.fftshift(f)
            fshift[int(crow - i):int(crow + i), int(ccol - i):int(ccol + i)] = 0
            magnitude_spectrum = 20 * np.log(np.abs(fshift))


        f = np.fft.fft2(fileName)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = 20 * np.log(np.abs(fshift))


        for i in range(int(cols / 2)):
            crow, ccol = rows / 2, cols / 2
            f = np.fft.fft2(fileName)
            fshift = np.fft.fftshift(f)
            fshift = box(i, i, fshift, rows, cols)
            magnitude_spectrum = 20 * np.log(np.abs(fshift))








#def message_box(self):
#message=QMessageBox.information(self, 'Message', 'The selected photo should be 128 or 512', QMessageBox.yes|QMessageBox.No)



# dialog_box = QtWidgets.QDialog()
# ui = Ui_Dialog()
# ui.setupUi(dialog_box)
# dialog_box.show()
# dialog_box.exec_()

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
