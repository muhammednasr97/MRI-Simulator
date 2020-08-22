from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QFileDialog, QLabel, QMessageBox, QApplication
from PyQt5.QtGui import QPixmap
from MN_MRI import Ui_Form
from matplotlib import pyplot as plt
import cv2
import subprocess
import numpy as np
from PIL import Image
from PIL.ImageQt import ImageQt
import sys
import time
from threading import Thread
import threading


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # self.ui.threadclass=threadclass()
        #  self.ui.threadclass.start()
        # self.ui.pb_browse.setIcon(self.Ui.QtGui.QIcon('123.jpg'))
        self.ui.pb_browse.clicked.connect(self.button_clicked)
        # self.ui.pb_start.clicked.connect(self.forier)

        # thread = threading.Thread(target=self.progressbar)
        # thread.start()

    def button_clicked(self):
        fileName, _filter = QFileDialog.getOpenFileName(self, "Title", "Default File",
                                                        "Photos Files (*.png);;Photos Files (*.jpg)")

        if fileName:
            image = cv2.imread(fileName, 0)
            rows, cols = image.shape
            crow, ccol = rows / 2, cols / 2
            print(fileName)
            print(_filter)

            if (rows == 512 and cols == 512 or rows == 128 and cols == 128):
                trans = Image.fromarray(image)
                res = ImageQt(trans)
                self.ui.lab_original.setPixmap(QPixmap.fromImage(res))

                self.ui.pb_browse.setEnabled(False)
                for i in range(int(cols / 2)):
                    f = np.fft.fft2(image)
                    fshift = np.fft.fftshift(f)
                    self.box(i, i, fshift, rows, cols)
                    magnitude_spectrum = 20 * np.log(np.abs(fshift))
                    magnitude_spectrum = np.asarray(magnitude_spectrum, dtype=np.uint8)
                    trans = Image.fromarray(magnitude_spectrum)
                    res = ImageQt(trans).scaled(321,271)
                    self.ui.lab_Forier.setPixmap(QPixmap.fromImage(res))

                    f_ishift = np.fft.ifftshift(fshift)
                    img_back = np.fft.ifft2(f_ishift)
                    img_back = np.abs(img_back)
                    img_back = np.asarray(img_back, dtype=np.uint8)
                    original_image = Image.fromarray(img_back)
                    res = ImageQt(original_image).scaled(321,271)
                    self.ui.lab_original.setPixmap(QPixmap.fromImage(res))

                    QApplication.processEvents()
                    time.sleep(0.001)


                for i in range(int(cols / 2)):
                    f = np.fft.fft2(image)
                    fshift = np.fft.fftshift(f)
                    fshift[int(crow - i):int(crow + i), int(ccol - i):int(ccol + i)] = 0
                    magnitude_spectrum = 20 * np.log(np.abs(fshift))
                    magnitude_spectrum = np.asarray(magnitude_spectrum, dtype=np.uint8)
                    trans = Image.fromarray(magnitude_spectrum)
                    res = ImageQt(trans).scaled(321,271)
                    self.ui.lab_Forier.setPixmap(QPixmap.fromImage(res))

                    f_ishift = np.fft.ifftshift(fshift)
                    img_back = np.fft.ifft2(f_ishift)
                    img_back = np.abs(img_back)
                    img_back = np.asarray(img_back, dtype=np.uint8)
                    original_image = Image.fromarray(img_back)
                    res = ImageQt(original_image).scaled(321,271)
                    self.ui.lab_original.setPixmap(QPixmap.fromImage(res))

                    QApplication.processEvents()
                    time.sleep(0.001)






            else:
                QMessageBox.information(self, 'Message', 'The selected photo should be 128×128 or 512×512')
            self.ui.pb_browse.setEnabled(True)
    # def progressbar(self):
    #     val=count
    #     self.ui.progressBar.setValue(val)

    def box(self, cwidth, rwidth, img, imgwidth, imgheight):
        img[0:rwidth, 0:] = 0
        img[imgheight - rwidth:imgheight, 0:] = 0
        img[0:, 0:cwidth] = 0
        img[0:, imgwidth - cwidth:imgwidth] = 0
        return img
"""
    def download(self):
        self.completed = 0

        while self.completed < 100:
            self.completed += 100/512
            self.progressBar.setValue(self.completed)
     
    def progressbar(self):
    for i in range(65):
        count = i
        count = count + 1
        val=count
        self.ui.progressBar.setValue(val)        

class threadclass(QtCore.QThread):
    def __init__(self,parent=None):
        super(threadclass, self).__init__(parent)

    def run(self):
        time.sleep(.01)
        progressbar


class QThread1(QtCore.QThread):
    sig1 = pyqtSignal(str)
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
    def run(self):
        #self.running = True
       # while self.running:
        self.sig1.emit(progressbar)
        time.sleep(1)
"""

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
