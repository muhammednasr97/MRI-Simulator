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
rows, ccol, crow, cols, counter, step, loop= [0, 0, 0, 0, 0, 0, 1]
pause = True
class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pb_browse.clicked.connect(self.Browse)
        self.ui.pb_resume.clicked.connect(self.Resume)
        self.ui.pb_start.clicked.connect(self.FFT_IFFT)
        self.ui.pb_pause.clicked.connect(self.Pause)
        self.ui.spinBox.valueChanged.connect(self.Spin_Box)
        
    def Browse(self):

        fileName, _filter = QFileDialog.getOpenFileName(self,
         "Title", "Default File", "Photos Files (*.png);;Photos Files (*.jpg)")

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
                else:
                    QMessageBox.information(self, 'Message', 'The selected photo should be 128×128 or 512×512')
            else:
                QMessageBox.information(self, 'Message', 'File is not image')
            

                
               
    
            
            
    def Outer_Frame(self, cwidth, rwidth, img, imgwidth, imgheight):
        img[0:rwidth, 0:] = 0
        img[imgheight - rwidth:imgheight, 0:] = 0
        img[0:, 0:cwidth] = 0
        img[0:, imgwidth - cwidth:imgwidth] = 0
        return img

    def Spin_Box(self):
        global Step
        Step = self.ui.spinBox.value()

    def Pause(self):
        global pause
        pause=False
        
    def Resume(self):
        global pause
        if pause==False:
            pause = True
            self.FFT_IFFT()


    def FFT_IFFT(self):
        global image, ccol, crow, rows, cols, pause, Counter, loop
        rows, cols = image.shape
        crow, ccol = rows / 2, cols / 2
        progress=0
        #Counter < int(cols/2)+Step
        
        while ( (Counter < int(cols/2)+Step ) and loop == 1 ):
            if pause:
                Counter = Counter + Step
                if Counter > int(cols/2):
                    if progress < 100:
                        Counter = int(cols/2)
                    else:
                        break
                progress = round(Counter*(100/int(cols/2)))  
                
                #self.ui.progressBar.setMaximum(cols/2)
                self.ui.progressBar.setProperty("value", progress)

# Fourier transform & shift ll low freq                
                f = np.fft.fft2(image)
                fshift = np.fft.fftshift(f)
# Outer_Frame function ---> btsfar mn bara l gowa                
                self.Outer_Frame(Counter, Counter, fshift, rows, cols)
                magnitude_spectrum = 20 * np.log(np.abs(fshift))
                magnitude_spectrum = np.asarray(magnitude_spectrum, dtype=np.uint8)
                trans = Image.fromarray(magnitude_spectrum)
                res = ImageQt(trans).scaled(321, 271)
                self.ui.lab_Fourier.setPixmap(QPixmap.fromImage(res))
# 3aks ll shift b3d kda bn3ml inverse                
                f_ishift = np.fft.ifftshift(fshift)
                img_back = np.fft.ifft2(f_ishift)
                img_back = np.abs(img_back)
                img_back = np.asarray(img_back, dtype=np.uint8)
                original_image = Image.fromarray(img_back)
                res = ImageQt(original_image).scaled(321, 271)
                self.ui.lab_original.setPixmap(QPixmap.fromImage(res))
                #Counter = Counter + Step
                QApplication.processEvents()
                time.sleep(0.1)
               
            else:
                break
            
        if pause and loop==1:
            Counter=0
            loop=2
        
        if pause:

            while( (Counter < int(cols/2)+Step ) and loop==2 ):
                if pause:
                    Counter = Counter + Step
                    if Counter > int(cols/2):
                        if progress < 100:
                            Counter = int(cols/2)
                        else:
                            continue
                    progress = round(Counter*(100/int(cols/2)))
                    #self.ui.progressBar.setMaximum(cols/2)
                    self.ui.progressBar.setProperty("value",progress)
# Fourier transform & shift ll low freq   
                    f = np.fft.fft2(image)
                    fshift = np.fft.fftshift(f)
# bn3ml tsfer mn gowa l bara
                    fshift[int(crow - Counter):int(crow + Counter), int(ccol - Counter):int(ccol + Counter)] = 0
                    magnitude_spectrum = 20 * np.log(np.abs(fshift))
                    magnitude_spectrum = np.asarray(magnitude_spectrum, dtype=np.uint8)
                    trans = Image.fromarray(magnitude_spectrum)
                    res = ImageQt(trans).scaled(321, 271)
                    self.ui.lab_Fourier.setPixmap(QPixmap.fromImage(res))
# 3aks ll shift b3d kda bn3ml inverse
                    f_ishift = np.fft.ifftshift(fshift)
                    img_back = np.fft.ifft2(f_ishift)
                    img_back = np.abs(img_back)
                    img_back = np.asarray(img_back, dtype=np.uint8)
                    original_image = Image.fromarray(img_back)
                    res = ImageQt(original_image).scaled(321, 271)
                    self.ui.lab_original.setPixmap(QPixmap.fromImage(res))
                    #Counter=Counter+Step
                    QApplication.processEvents()
                    time.sleep(0.1)
                    
                else :
                   break
               
        if pause and loop==2:
            Counter=0
            loop=1       
                
def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
