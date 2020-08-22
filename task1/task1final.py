from PyQt5.QtWidgets import QFileDialog, QMessageBox, QApplication, QWidget
from PyQt5.QtGui import QPixmap
from MN_MRI import Ui_Form
import cv2
import numpy as np
import sys
import time
import qimage2ndarray

class Program(QWidget):

    def __init__(self):
        super(Program, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.image = []
        self.check = []
        self.rows, self.ccol, self.crow, self.rowX, self.colsX, self.cols, self.Step,\
        self.Counter, self.loop, self.pause = [0, 0, 0, 0, 0, 0, 0, 0, 1, True]

        self.ui.pb_browse.clicked.connect(self.Browse)
        self.ui.pb_resume.clicked.connect(self.Resume)
        self.ui.pb_start.clicked.connect(self.FFT_IFFT)
        self.ui.pb_pause.clicked.connect(self.Pause)
        self.ui.spinBox.valueChanged.connect(self.Spin_Box)
        self.ui.pb_resume.setEnabled(False)
        self.ui.pb_start.setEnabled(False)
        self.ui.pb_pause.setEnabled(False)
        
    def Browse(self):
        filename, _filter = QFileDialog.getOpenFileName(self,"Browse", "")
        if filename:
            self.check = cv2.imread(filename, 0)
            if type(self.check) == np.ndarray:
                self.rowsX, self.colsX = self.check.shape
                if self.rowsX == 512 and self.colsX == 512 or self.rowsX == 128 and self.colsX == 128:
                    self.image = self.check
                    self.rows = self.rowsX
                    self.cols = self.colsX
                    self.crow, self.ccol = self.rows / 2, self.cols / 2
                    print(filename)
                    print(_filter)

                    trans = qimage2ndarray.array2qimage(self.image)
                    res = QPixmap(trans).scaled(321, 271)
                    self.ui.lab_original.setPixmap(res)

                    self.Counter = 0
                    self.ui.progressBar.setValue(0)
                    self.ui.lab_Fourier.clear()
                    self.ui.pb_start.setEnabled(True)
                    self.ui.pb_resume.setEnabled(False)
                else:
                    QMessageBox.information(self, 'Message', 'The selected photo should be 128×128 or 512×512')


            else:
                QMessageBox.information(self, 'Message', "File should be image")

            
    def Outer_Frame(self, cwidth, rwidth, img, imgwidth, imgheight):
        img[0:rwidth, 0:] = 0
        img[imgheight - rwidth:imgheight, 0:] = 0
        img[0:, 0:cwidth] = 0
        img[0:, imgwidth - cwidth:imgwidth] = 0
        return img

    def Spin_Box(self):
        self.Step = self.ui.spinBox.value()

    def Pause(self):
        self.ui.pb_resume.setEnabled(True)
        self.pause = False

        
    def Resume(self):
        if self.pause == False:
            self.pause = True
            self.FFT_IFFT()


    def FFT_IFFT(self):
        self.pause = True
        self.ui.pb_start.setEnabled(False)
        self.ui.pb_pause.setEnabled(True)
        self.rows, self.cols = self.image.shape
        self.crow, self.ccol = self.rows / 2, self.cols / 2
        progress = 0

        while(self.Counter < int(self.cols/2)) and self.loop == 1:
            if self.pause:
                self.Counter = self.Counter + self.Step
                if self.Counter > int(self.cols/2):
                    if progress < 100:
                        self.Counter = int(self.cols/2)
                    else:
                        break
                    
                progress = round(self.Counter*(100/int(self.cols/2)))
                self.ui.progressBar.setProperty("value", progress)


                f = np.fft.fft2(self.image)
                fshift = np.fft.fftshift(f)               
                self.Outer_Frame(self.Counter, self.Counter, fshift, self.rows, self.cols)
                magnitude_spectrum = 20 * np.log(np.abs(fshift))
                trans = qimage2ndarray.array2qimage(magnitude_spectrum)
                res = QPixmap(trans).scaled(321, 271)
                self.ui.lab_Fourier.setPixmap(res)

                f_ishift = np.fft.ifftshift(fshift)
                img_back = np.fft.ifft2(f_ishift)
                img_back = np.abs(img_back)
                trans = qimage2ndarray.array2qimage(img_back)
                res = QPixmap(trans).scaled(321, 271)
                self.ui.lab_original.setPixmap(res)
                QApplication.processEvents()
                time.sleep(0.1)
               
            else:
                break
            
        if self.pause and self.loop == 1:
            self.Counter = 0
            self.loop = 2
        
        if self.pause:

            while(self.Counter < int(self.cols/2)) and self.loop == 2:
                if self.pause:
                    self.Counter = self.Counter + self.Step
                    if self.Counter > int(self.cols/2):
                        if progress < 100:
                            self.Counter = int(self.cols/2)
                        else:
                            break
                    progress = round(self.Counter*(100/int(self.cols/2)))
                    self.ui.progressBar.setProperty("value", progress)
                    
                    f = np.fft.fft2(self.image)
                    fshift = np.fft.fftshift(f)                    
                    fshift[int(self.crow - self.Counter):int(self.crow + self.Counter), int(self.ccol - self.Counter):int(self.ccol + self.Counter)] = 0
                    magnitude_spectrum = 20 * np.log(np.abs(fshift))
                    trans = qimage2ndarray.array2qimage(magnitude_spectrum)
                    res = QPixmap(trans).scaled(321, 271)
                    self.ui.lab_Fourier.setPixmap(res)

                    f_ishift = np.fft.ifftshift(fshift)
                    img_back = np.fft.ifft2(f_ishift)
                    img_back = np.abs(img_back)
                    trans = qimage2ndarray.array2qimage(img_back)
                    res = QPixmap(trans).scaled(321, 271)
                    self.ui.lab_original.setPixmap(res)
                    QApplication.processEvents()
                    time.sleep(0.1)
                    
                else:
                   break
               
        if self.pause and self.loop == 2:
            self.Counter = 0
            self.loop = 1
            self.ui.pb_resume.setEnabled(False)
            self.ui.pb_pause.setEnabled(False)
            self.ui.pb_start.setEnabled(True)

                
def main():
    app = QApplication(sys.argv)
    application = Program()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
