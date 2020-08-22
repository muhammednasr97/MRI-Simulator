from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QPixmap, QPainter, QPen
from nt2 import Ui_Form
import numpy as np
import sys
import time
import qimage2ndarray
from PIL import Image, ImageEnhance
import math


class Program(QWidget):
    def __init__(self):
        super(Program, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.image, self.t1_array, self.t2_array, self.pd_array, self.arr, self.fa, self.tr, self.te,\
        self.t1_value, self.t2_value, self.x, self.y, self.num, self.contrast_ratio, self.bright_ratio, \
        self.res, self.result,self.t11_array, self.size, self.draw, self.text\
            = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, True, '']
        self.ui.pushButton.clicked.connect(self.browse)
        self.ui.pushButton_2.clicked.connect(self.SSFP)
        self.ui.pushButton_2.setEnabled(False)
        self.ui.spinBox_TE.valueChanged.connect(self.time_eco)
        self.ui.spinBox_TR.valueChanged.connect(self.time_repeat)
        self.ui.spinBox_FA.valueChanged.connect(self.flib_angle)
        self.ui.comboBox_sp.activated[str].connect(self.current_text)
        self.ui.brightness.valueChanged.connect(self.slider_brightness)
        self.ui.contrast.valueChanged.connect(self.slider_contrast)
        self.ui.phantom1.mousePressEvent = self.position

    def time_repeat(self):  #changing the value of TR by spinbox
        self.tr = self.ui.spinBox_TR.value()

    def time_eco(self):     #changing the value of TE by spinbox
        self.te = self.ui.spinBox_TE.value()

    def flib_angle(self):   #changing the value of Flib angle by spinbox
        self.fa = self.ui.spinBox_FA.value()

    def browse(self):
        self.filename, _filter = QFileDialog.getOpenFileName(self, "Browse", "", "Filter -- Image Files (*.png *.jpg)")
        np.set_printoptions(threshold=np.inf)   #full array
        if self.filename:
            self.image = Image.open(self.filename).convert("L")
            self.arr = np.array(self.image)
            rows, cols = self.arr.shape
            if rows == self.size and cols == self.size:
                trans = qimage2ndarray.array2qimage(self.arr)
                self.res = QPixmap(trans)
                self.res.save("new_copy.png")
                self.ui.phantom1.setPixmap(self.res)
                self.phantom()
                self.ui.pushButton_2.setEnabled(True)
                #print(self.arr)
            else:
                QMessageBox.information(self, 'Message', 'The selected phantom should be the right size ')

    def phantom(self):
        self.t11_array = np.ones((self.size, self.size))
        self.t2_array = np.ones((self.size, self.size))
        self.pd_array = np.ones((self.size, self.size))
        i, j = self.arr.shape
        for v in range(i):
            for b in range(j):
                if self.arr[v][b] <= 29:
                    self.t11_array[v][b] = 400
                    self.t2_array[v][b] = 50
                    self.pd_array[v][b] = 400
                elif (self.arr[v][b] > 29) & (self.arr[v][b] <= 107):
                    self.t11_array[v][b] = 900
                    self.t2_array[v][b] = 130
                    self.pd_array[v][b] = 700
                elif self.arr[v][b] >= 107:
                    self.t11_array[v][b] = 1100
                    self.t2_array[v][b] = 230
                    self.pd_array[v][b] = 1000
        self.current_text()
        min = np.min(self.t11_array)
        max = np.max(self.t11_array)
        self.t1_array = [255 / (max - min)] * (self.t11_array - min)
        #print(self.t1_array)
    def current_text(self):
        self.text = (self.ui.comboBox_sp.currentText())
        if self.text == 'O.Array':
            self.transfer_show(self.arr)
        elif self.text == 'T1':
            self.transfer_show(self.t1_array)
        elif self.text == 'T2':
            self.transfer_show(self.t2_array)
        else:
            self.transfer_show(self.pd_array)

    def transfer_show(self, array):
        t1 = qimage2ndarray.array2qimage(array)
        res1 = QPixmap(t1)
        self.ui.phantom3.setPixmap(res1)
        return array

    def slider_brightness(self):
        self.bright_ratio = self.ui.brightness.value()
        self.brightness("new_copy.png")
        QApplication.processEvents()
        time.sleep(.001)

    def brightness(self, im):
        img = Image.open(im).convert("L")
        enhancer = ImageEnhance.Brightness(img)
        enhanced_im = enhancer.enhance(self.bright_ratio)
        enhanced_im.save("brightness_samole.png")
        self.result = QPixmap("brightness_samole.png")
        self.ui.phantom1.setPixmap(self.result)

    def slider_contrast(self):
        self.contrast_ratio = self.ui.contrast.value()
        self.contrast("brightness_samole.png")
        QApplication.processEvents()
        time.sleep(.001)

    def contrast(self, im):
        img = Image.open(im).convert("L")
        enhancer = ImageEnhance.Contrast(img)
        enhanced_im = enhancer.enhance(self.contrast_ratio)
        enhanced_im.save("contrast_sample.png")
        result = QPixmap("contrast_sample.png")
        self.ui.phantom1.setPixmap(result)

    def paintevent(self, img):
        painter = QPainter(img)
        painter.begin(self)
        pen = QPen(QtCore.Qt.red)
        painter.setPen(pen)
        painter.drawRect(self.x, self.y, 1, 1)
        self.ui.phantom1.setPixmap(img)
        painter.end()
        QApplication.processEvents()

    def position(self, event):
        a = self.ui.phantom1.frameGeometry().width()
        b = self.ui.phantom1.frameGeometry().height()
        self.x = int(event.pos().x() * self.size / a)
        self.y = int(event.pos().y()* self.size / b)
        print(self.x, self.y)
        self.t1_value = self.t11_array[self.x, self.y]
        self.t2_value = self.t2_array[self.x, self.y]
        print("t2_value", self.t2_value)
        print("t1_value", self.t1_value)
        if self.num <= 4:
            self.plot()
            self.paintevent(self.res)
            QApplication.processEvents()
        else:
            self.draw = False

    def plot(self):
        theta = np.radians(self.fa)
        Mo = ([[0], [0], [1]])
        arr1 = []
        arr2 = []
        c = np.cos(theta)
        s = np.sin(theta)
        t = 0
        while self.draw:
            for t in range(1000):
                decay = np.array([[np.exp(-t / self.t2_value), 0, 0], [0, np.exp(-t / self.t2_value), 0],
                                  [0, 0, (np.exp(-t / self.t1_value))]])
                flip = ([[c, 0, s], [0, 1, 0], [-s, 0, c]])
                ex2 = ([[0], [0], [1 - np.exp(-t / self.t1_value)]])
                out1 = np.dot(decay, flip)
                out2 = np.dot(out1, Mo)
                x, y, z = out2 + ex2
                arr1.extend(x)#########################
                arr2.extend(z)
                t = t+1

            if self.num == 0:
                self.ui.graphicsView_t1.plot(arr1, pen='b')
                self.ui.graphicsView_t2.plot(arr2, pen='b')
            elif self.num == 1:
                self.ui.graphicsView_t1.plot(arr1, pen='g')
                self.ui.graphicsView_t2.plot(arr2, pen='g')
            elif self.num == 2:
                self.ui.graphicsView_t1.plot(arr1, pen='r')
                self.ui.graphicsView_t2.plot(arr2, pen='r')
            elif self.num == 3:
                self.ui.graphicsView_t1.plot(arr1, pen='y')
                self.ui.graphicsView_t2.plot(arr2, pen='y')
            else:
                self.ui.graphicsView_t1.plot(arr1, pen='w')
                self.ui.graphicsView_t2.plot(arr2, pen='w')
            self.num = self.num + 1

            QApplication.processEvents()
            if t == 1000:
                break

    def kspace(self):
        theta = np.radians(self.fa)
        row, col = self.arr.shape
        phantom = np.zeros((row, col, 3))  # Creating phantom as a 3D array, each pixel has a vector
        KSpace = np.zeros((row, col), dtype=np.complex)  # creating K-space



        for i in range(row):  # All vectors are [0]
            for j in range(col):  # [0]
                phantom[i, j, 2] = 1  # [1]

        # rotation matrix around y-axis
        RF = ([[np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [-np.sin(theta), 0, np.cos(theta)]])

        for k in range(5):
            for i in range(row):
                for j in range(col):
                    dec = np.exp(-self.te / self.t2_array[i][j])
                    phantom[i, j, :] = np.dot(RF, phantom[i, j, :])  # Phantom after rotation around y-axis
                    phantom[i, j, :] = np.dot(dec, phantom[i, j, :])  # Phantom after decay at x-y plane (on x-axis)

            for ph_rowtr in range(row):  # each pixel in phantom
                for ph_coltr in range(col):
                    phantom[ph_rowtr, ph_coltr, 0] = 0  # zero component at x-axis
                    phantom[ph_rowtr, ph_coltr, 1] = 0  # zero component at y-axis
                    # recovery on z-axis
                    # phantom[ph_rowtr, ph_coltr, 2] = ((phantom[ph_rowtr, ph_coltr, 2]) * np.exp(
                    #    -self.tr / self.t11_array[i, j])) + (1 - np.exp(-self.tr / self.t11_array[ph_rowtr, ph_coltr]))
                    phantom[ph_rowtr, ph_coltr, 2] = (1 - np.exp(-self.tr / self.t1_array[ph_rowtr, ph_coltr]))


        for r in range(row):  # k-space row
            for i in range(row):
                for j in range(col):
                    dec = np.exp(-self.te / self.t2_array[i][j])
#                    dec = np.array([[np.exp(-self.te / self.t2_array[i][j]), 0, 0], [0, np.exp(-self.te / self.t2_array[i][j]), 0],
#                                    [0, 0, (np.exp(-self.tr / self.t1_array[i][j]))]])  # Decay equation

                    phantom[i, j, :] = np.dot(RF, phantom[i, j, :])  # Phantom after rotation around y-axis
                    phantom[i, j, :] = np.dot(dec, phantom[i, j, :])  # Phantom after decay at x-y plane (on x-axis)

            for c in range(col):
                Gx_step = ((2 * math.pi) / row) * r  # Frequency encodind
                Gy_step = ((2 * math.pi) / col) * c  # Phase encodind
                for ph_row in range(row):
                    for ph_col in range(col):
                        Toltal_theta = (Gx_step * ph_row) + (Gy_step * ph_col)

                        Mag = math.sqrt(((phantom[ph_row, ph_col, 0]) * (phantom[ph_row, ph_col, 0])) + (
                                    (phantom[ph_row, ph_col, 1]) * (phantom[ph_row, ph_col, 1])))

                        KSpace[r, c] = KSpace[r, c] + (Mag * np.exp(-1j * Toltal_theta))
                    QApplication.processEvents()
                    time.sleep(.001)
                QApplication.processEvents()
                time.sleep(.001)

            for ph_rowtr in range(row):  # each pixel in phantom
                for ph_coltr in range(col):
                    phantom[ph_rowtr, ph_coltr, 0] = 0  # zero component at x-axis
                    phantom[ph_rowtr, ph_coltr, 1] = 0  # zero component at y-axis
                    # recovery on z-axis
                    phantom[ph_rowtr, ph_coltr, 2] = (1 - np.exp(-self.tr / self.t1_array[ph_rowtr, ph_coltr]))
                QApplication.processEvents()
                time.sleep(.001)
            QApplication.processEvents()
            time.sleep(.001)

        output = np.absolute(np.fft.ifft2(KSpace))  # simple ifft2 to bring back the image.
        #print(output)
        maxout = np.max(output)
        #print(maxout)
        minout = np.min(output)
        #print(minout)
        map = (255/(maxout-minout)) * (output-minout)

        trans = qimage2ndarray.array2qimage(map)
        res = QPixmap(trans)
        self.ui.phantom5.setPixmap(res)

        fshift = np.fft.fftshift(KSpace)
        kspaceoutput = 20 * np.log(np.abs(fshift))
        print(kspaceoutput)
        minks = np.min(kspaceoutput)
        maxks = np.max(kspaceoutput)
        kspacemap = [255/(maxks - minks)] * (kspaceoutput - minks)
        trans = qimage2ndarray.array2qimage(kspacemap)
        res = QPixmap(trans)
        self.ui.phantom6.setPixmap(res)

    def SSFP(self):
        row, col = self.arr.shape
        theta = np.radians(self.fa)
        Kspace_ssfp = np.zeros((row, col), dtype=np.complex)
        phantom = self.Phantom(row, col)
        #phantom = np.zeros((row, col, 3))

        # startup cycle with 0.5 theta
        phantom = self.startup_cycle(theta / 2, 15, phantom)
        # decay
        phantom = self.rotate_decay(theta, self.te, self.t2_array, phantom)
        # startup cycle with theta
        phantom = self.startup_cycle(theta, 15, phantom)
        for r in range(row):  # rows
            phantom = self.rotate_decay(theta, self.te, self.t2_array, phantom)
            for c in range(col):
                Gx_step = ((2 * math.pi) / row) * r  # Frequency encodind
                Gy_step = ((2 * math.pi) / col) * c  # Phase encodind
                for ph_row in range(row):
                    for ph_col in range(col):
                        Toltal_theta = (Gx_step * ph_row) + (Gy_step * ph_col)
                        Mag = math.sqrt(((phantom[ph_row, ph_col, 0]) * (phantom[ph_row, ph_col, 0])) +
                                        ((phantom[ph_row, ph_col, 1]) * (phantom[ph_row, ph_col, 1])))

                        Kspace_ssfp[r, c] = Kspace_ssfp[r, c] + (Mag * np.exp(-1j * Toltal_theta))
                        QApplication.processEvents()

                QApplication.processEvents()
            theta = -theta
            #print(theta)
            for ph_rowtr in range(row):
                for ph_coltr in range(col):
                    phantom[ph_rowtr, ph_coltr, 2] = ((phantom[ph_rowtr, ph_coltr, 2]) *
                                                      np.exp(-self.tr / self.t11_array[ph_rowtr, ph_coltr])) + (1 - np.exp(-self.tr / self.t11_array[ph_rowtr, ph_coltr]))

            QApplication.processEvents()
        iff = np.fft.ifft2(Kspace_ssfp)

        #print(iff)
        inverse_array = np.abs(iff)
        inverse_array = (inverse_array - np.amin(inverse_array)) * 255 / (np.amax(inverse_array) - np.amin(inverse_array))
        print(inverse_array)
        inverse_img = qimage2ndarray.array2qimage(inverse_array)
        imgreconstruction = QPixmap(inverse_img)  # piexel of image
        self.ui.phantom5.setPixmap(imgreconstruction)
        self.ui.phantom6.setPixmap(imgreconstruction)


    def RF_rotate(self, theta, phantom, row, col):
        for i in range(row):
            for j in range(col):
                phantom[i, j, :] = self.rotate(theta, phantom[i, j, :])

        return phantom

    def rotate(self, theta, phantom):
        RF = ([[np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [-np.sin(theta), 0, np.cos(theta)]])
        phantom = np.dot(RF, phantom)
        return phantom

    def decay(self, phantom, TE, T2):
        dec = np.exp(-TE / T2)
        phantom = np.dot(dec, phantom)
        return phantom

    def rotate_decay(self, theta, TE, T2, phantom):
        row, col = self.arr.shape
        #phantom = np.zeros((row, col, 3))
        for i in range(row):
            for j in range(col):
                phantom[i, j, :] = self.rotate(theta, phantom[i, j, :])
                phantom[i, j, :] = self.decay(phantom[i, j, :], TE, T2[i, j])
        return phantom

    def recovery(self, TR, T1, phantom):
        row, col = self.arr.shape
        for ph_rowtr in range(row):
            for ph_coltr in range(col):
                phantom[ph_rowtr, ph_coltr, 0] = 0
                phantom[ph_rowtr, ph_coltr, 1] = 0
                phantom[ph_rowtr, ph_coltr, 2] = ((phantom[ph_rowtr, ph_coltr, 2]) * np.exp(
                    -TR / T1[ph_rowtr, ph_coltr])) + (1 - np.exp(-TR / T1[ph_rowtr, ph_coltr]))
        return phantom

    def startup_cycle(self, theta, n, phantom):
        for r in range(n):
            phantom = self.rotate_decay(theta, self.te, self.t2_array, phantom)
            phantom = self.recovery(self.tr, self.t11_array, phantom)
        return phantom

    def Phantom(self, row, col):
        phantom = np.zeros((row, col, 3))
        for i in range(row):
            for j in range(col):
                phantom[i, j, 2] = 1
        return phantom


def main():
    app = QApplication(sys.argv)
    application = Program()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()