from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget, QComboBox
from PyQt5.QtGui import QPixmap
from nt2 import Ui_Form
import cv2
import numpy as np
import sys
import time
import qimage2ndarray
from PIL import Image
from matplotlib import pyplot as plt, image
import math
import pyqtgraph as pg
class Program(QWidget):

    def __init__(self):
        super(Program, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.image, self.t1_array, self.t2_array, self.pd_array, self.arr,\
         self.fa, self.tr, self.te, self.t1_value, self.t2_value, self.st, self.size = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.text = ''
        self.draw = True

        self.ui.pushButton.clicked.connect(self.Browse)

        self.ui.phantom1.mousePressEvent = self.position
        self.ui.phantom2.mousePressEvent = self.position

        self.ui.spinBox_TE.valueChanged.connect(self.time_eco)
        self.ui.spinBox_TR.valueChanged.connect(self.time_repeat)
        self.ui.spinBox_FA.valueChanged.connect(self.flib_angle)

        self.ui.comboBox_sp.activated[str].connect(self.current_text)

    def time_repeat(self):  #changing the value of TR by spinbox
        self.tr = self.ui.spinBox_TR.value()
    def time_eco(self):     #changing the value of TE by spinbox
        self.te = self.ui.spinBox_TE.value()
    def flib_angle(self):   #changing the value of Flib angle by spinbox
        self.fa = self.ui.spinBox_FA.value()

    def position(self, event):
        x = math.floor(event.pos().x() * 128 / self.ui.phantom2.frameGeometry().width())
        y = math.floor(event.pos().y()*128/self.ui.phantom2.frameGeometry().height())

        print(x, y)
        if x > 128:
            real_x = int(128*x/320)
        else:
            real_x = x
        if y > 128:
            real_y = int(128 * y / 280)
        else:
            real_y = y
        if self.st == 1:
            self.t1_value = self.t1_array[real_x, real_y]
            print("t1_value", self.t1_value)
        elif self.st == 2:
            self.t2_value = self.t2_array[real_x, real_y]
            print("t2_value", self.t2_value)


    def phantom(self):
        self.size = 128
        self.t1_array = np.ones((self.size, self.size))
        self.t2_array = np.ones((self.size, self.size))
        self.pd_array = np.ones((self.size, self.size))
        i, j = self.arr.shape
        print(i, j)
        for v in range(i):
            for b in range(j):
                if self.arr[v][b] == 29:
                    self.t1_array[v][b] = self.arr[v][b]
                    self.t1_array[v][b] = int(self.arr[v][b] * (.2))
                    self.t2_array[v][b] = 256 - self.t1_array[v][b]
                    self.pd_array[v][b] = 0
                elif (self.arr[v][b] > 29) and (self.arr[v][b] <= 107):
                    self.t1_array[v][b] = self.arr[v][b]
                    self.t1_array[v][b] = int(self.arr[v][b] * 3)
                    self.t2_array[v][b] = 256 - self.t1_array[v][b]
                    self.pd_array[v][b] = 100
                else:
                    self.t1_array[v][b] = self.arr[v][b]
                    self.t1_array[v][b] = 60 + (self.arr[v][b])
                    self.t2_array[v][b] = 40 + (self.arr[v][b])
                    self.pd_array[v][b] = 200
        self.current_text()

    def current_text(self):
        self.text = (self.ui.comboBox_sp.currentText())
        if self.text == 'O.Array':
            self.transfer(self.arr)
            #self.draw = False
        elif self.text == 'T1':
            self.st = 1
            self.transfer(self.t1_array)
           # self.draw = True
            self.plot()
        elif self.text == 'T2':
            self.st = 2
            self.transfer(self.t2_array)
           # self.draw = True
            self.plot()
        else:
            self.st = 3
            self.transfer(self.pd_array)

    def transfer(self, array):
        t1 = qimage2ndarray.array2qimage(array)
        res1 = QPixmap(t1)#.scaled(320, 280)
        self.ui.phantom2.setPixmap(res1)
        return array

    def Browse(self):
        filename, _filter = QFileDialog.getOpenFileName(self,"Browse", "")
        np.set_printoptions(threshold=np.inf)   #full array
        self.image = Image.open(filename).convert("L")
        self.arr = np.asarray(self.image)
        trans = qimage2ndarray.array2qimage(self.arr)
        res = QPixmap(trans).scaled(320, 280)
        self.ui.phantom1.setPixmap(res)
        # print(self.arr)
        self.phantom()

    def rotate(self,V , theta, axis='x'):
        '''Rotate a vector `V` `theta` degrees around axis `axis`'''
        c = np.cos(theta)
        s = np.sin(theta)
        if axis == 'x':
            return np.dot(np.array([
               [1, 0, 0],
               [0, c, -s],
               [0, s, c]
               ]), V)
        elif axis == 'y':
            return np.dot(np.array([
                [c, 0, s],
                [0, 1, 0],
                [-s, 0, c]
            ]), V)
        elif axis == 'z':
            return np.dot(np.array([
                [c, -s, 0],
                [s, c, 0],
                [0, 0, 1.],
                ]), V)

    def plot(self):
        theta = np.radians(self.fa)
        Mo = ([[0], [0], [1]])
        flip = self.rotate(Mo, theta, 'y')
        I = np.eye(3, dtype=None)

        arr1 = []
        arr2 = []
        t = 0
        self.ui.graphicsView_t1.clear()
        while self.draw:
            for t in range(1000):
                if self.t1_value > 0:
                    exp = np.exp(-t / self.t1_value)
                    ex1 = exp * I
                    ex2 = ([[0], [0], [1 - np.exp(-t / self.t1_value)]])
                    out1 = np.dot(ex1, flip)
                    x, y, z = out1 + ex2
                    arr1.extend(z)
                    t = t+1
                if self.t2_value > 0:
                    exp = np.exp(-t / self.t2_value)
                    ex1 = exp * I
                    ex2 = ([[0], [0], [1 - np.exp(-t / self.t2_value)]])
                    out1 = np.dot(ex1, flip)
                    x, y, z = out1 + ex2
                    arr2.extend(x)
                    t = t+1

            self.ui.graphicsView_t1.plot(arr1, pen='b')
            self.ui.graphicsView_t2.plot(arr2, pen='b')
            QApplication.processEvents()
            if t == 1000:
                break

    def plot2(self):
        # x=[]
        arr1 = []
        t = 0
        self.ui.graphicsView_t2.clear()
        # self.ui.graphicsView_t1_2.showGrid(x=True, y=True, alpha=2)

        while self.draw:
            for counter in range(10000):
                if self.t2_value > 0:
                    equation = (math.exp(- counter/self.t2_value))
                    arr1.append(equation)
                    # x.append(counter)
                    t = t+1

            self.ui.graphicsView_t2.plot(arr1, pen='r')

            QApplication.processEvents()
            if t == 10000:
                break

#       self.image =cv2.imread(filename, 0)
#       image=PIL.Image.open(filename).
#       trans = qimage2ndarray.array2qimage(self.image)
#       res = QPixmap(trans).scaled(320, 280)
#       self.ui.phantom1.setPixmap(res)
#       cv2.imwrite(self.image, np.zeros((10, 10)))
#       print(self.image)




def main():
    app = QApplication(sys.argv)
    application = Program()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()