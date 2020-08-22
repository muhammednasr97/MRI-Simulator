from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QApplication
from PyQt5.QtGui import QPixmap
from MN_MRI import Ui_Form
import cv2
import numpy as np
from PIL import Image
from PIL.ImageQt import ImageQt
import sys
import time

image = []
rows, ccol, crow, cols, i, x, loop = [0, 0, 0, 0, 0, 0, 1]
pause = True

class ApplicationWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pb_browse.clicked.connect(self.button_clicked)
        self.ui.pb_resume.clicked.connect(self.resume)
        self.ui.spinBox.valueChanged.connect(self.spin_box)
        self.ui.pb_start.clicked.connect(self.forier)
        self.ui.pb_pause.clicked.connect(self.play_pause)
        self.ui.pb_resume.setEnabled(False)
        self.ui.pb_start.setEnabled(False)
        self.ui.pb_pause.setEnabled(False)

    def button_clicked(self):

        fileName, _filter = QFileDialog.getOpenFileName(self,
         "Title", "Default File")

        if fileName:
            global image, rows, cols, ccol, crow
            image = cv2.imread(fileName, 0)
            if type(image) == np.ndarray:
                rows, cols = image.shape
                crow, ccol = rows / 2, cols / 2
                print(fileName)
                print(_filter)

                if rows == 512 and cols == 512 or rows == 128 and cols == 128:
                    trans = Image.fromarray(image)
                    res = ImageQt(trans).scaled(321, 271)
                    self.ui.lab_original.setPixmap(QPixmap.fromImage(res))
                    self.ui.lab_Fourier.clear()
                    self.ui.pb_start.setEnabled(True)

                    global i
                    i = 0
                    self.ui.progressBar.setValue(0)
                else:
                    QMessageBox.information(self, 'Message', 'The selected photo should be 128×128 or 512×512')
            else:
                QMessageBox.information(self, 'Message', 'The selected photo should be 128×128 or 512×512')


    def spin_box(self):
        global x
        x = self.ui.spinBox.value()

    def play_pause(self):
        global pause
        self.ui.pb_resume.setEnabled(True)
        pause = False

    def resume(self):
        global pause
        if pause == False:
            pause = True
            self.forier()

    def forier(self):
        self.ui.pb_resume.setEnabled(True)
        self.ui.pb_pause.setEnabled(True)
        global image, ccol, crow, rows, cols,pause, i, loop, x
        rows, cols = image.shape
        crow, ccol = rows / 2, cols / 2

        while (i < int(cols / 2)+x)and loop == 1:

            if pause:

                f = np.fft.fft2(image)
                fshift = np.fft.fftshift(f)
                fshift[int(crow - i):int(crow + i), int(ccol - i):int(ccol + i)] = 0
                magnitude_spectrum = 20 * np.log(np.abs(fshift))
                magnitude_spectrum = np.asarray(magnitude_spectrum, dtype=np.uint8)
                trans = Image.fromarray(magnitude_spectrum)
                res = ImageQt(trans).scaled(321, 271)
                self.ui.lab_Fourier.setPixmap(QPixmap.fromImage(res))

                f_ishift = np.fft.ifftshift(fshift)
                img_back = np.fft.ifft2(f_ishift)
                img_back = np.abs(img_back)
                img_back = np.asarray(img_back, dtype=np.uint8)
                original_image = Image.fromarray(img_back)
                res = ImageQt(original_image).scaled(321, 271)
                self.ui.lab_original.setPixmap(QPixmap.fromImage(res))
                i=i+x

                self.ui.progressBar.setMaximum((cols / 2) - (cols / 2) % x)
                self.ui.progressBar.setProperty("value", i)

                QApplication.processEvents()
                time.sleep(0.001)
            else:
                break

        if pause and loop == 1:
            i = 0
            loop = 2

        if pause:

            while (i < int(cols / 2)+x) and loop == 2:

                if pause:

                    f = np.fft.fft2(image)
                    fshift = np.fft.fftshift(f)
                    self.box(i, i, fshift, rows, cols)
                    magnitude_spectrum = 20 * np.log(np.abs(fshift))
                    magnitude_spectrum = np.asarray(magnitude_spectrum, dtype=np.uint8)
                    trans = Image.fromarray(magnitude_spectrum)
                    res = ImageQt(trans).scaled(321, 271)
                    self.ui.lab_Fourier.setPixmap(QPixmap.fromImage(res))

                    f_ishift = np.fft.ifftshift(fshift)
                    img_back = np.fft.ifft2(f_ishift)
                    img_back = np.abs(img_back)
                    img_back = np.asarray(img_back, dtype=np.uint8)
                    original_image = Image.fromarray(img_back)
                    res = ImageQt(original_image).scaled(321, 271)
                    self.ui.lab_original.setPixmap(QPixmap.fromImage(res))
                    i = i + x
                    self.ui.progressBar.setMaximum((cols / 2) - (cols / 2) % x)
                    self.ui.progressBar.setProperty("value", i)

                    QApplication.processEvents()
                    time.sleep(0.001)

                else:
                   break

            if pause and loop == 2:
                i = 0
                loop = 1
                self.ui.pb_resume.setEnabled(False)
                self.ui.pb_pause.setEnabled(False)
       # self.ui.pb_resume.setEnabled(False)

    def box(self, cwidth, rwidth, img, imgwidth, imgheight):
        img[0:rwidth, 0:] = 0
        img[imgheight - rwidth:imgheight, 0:] = 0
        img[0:, 0:cwidth] = 0
        img[0:, imgwidth - cwidth:imgwidth] = 0
        return img


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
