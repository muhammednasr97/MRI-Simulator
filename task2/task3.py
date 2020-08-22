from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QPixmap, QPainter, QPen, QBrush, QColor
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
        self.res, self.result, self.t11_array,self.value, self.t1prep_phantom, self.tagging_phantom, self.t2prep_phantom,\
        self.size, self.draw, self.text, self.flag\
            = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, True, '', True]
        self.prep_end_pos = 1
        self.x_range = np.arange(0, self.prep_end_pos, .001)  # x -axis
  #      self.preperation_pulse("IR", self.x_range, 70)
        self.x2_range = None
#        self.acquisition_pulse("GRE", self.x2_range, 80, 100, 90)

        self.viewer = PhotoViewer(self)  # object for the basic phantom
        # self.port1 = PhotoViewer(self)  # object for the first view port
        self.zoomControl('separated')  # set zooming setting to linked zooming at the start of the program
        self.ui.cbZoom.currentTextChanged.connect(self.zoomControl)  # combo box to control zooming settings

        self.ui.gridLayout_2.addWidget(self.viewer, 1, 1)  # add the 'viewer' graphicsview object to a layout
        # self.viewer.setPhoto(pixmap)
        # self.ui.gridLayout_7.addWidget(self.port1, 2, 1)  # add the 'port1' graphicsview object to a layout
        self.ui.ernst_btttn.clicked.connect(self.ernset)
        self.ui.pushButton.clicked.connect(self.browse)
        self.ui.pushButton_2.clicked.connect(self.run)
        self.ui.pushButton_2.setEnabled(False)
        self.ui.spinBox_TE.valueChanged.connect(self.time_eco)
        self.ui.spinBox.valueChanged.connect(self.T_ir)
        self.ui.spinBox_TR.valueChanged.connect(self.time_repeat)
        self.ui.spinBox_stcy.valueChanged.connect(self.st_cycle)
        self.ui.spinBox_FA.valueChanged.connect(self.flib_angle)
        self.ui.comboBox_sp.activated[str].connect(self.current_text)
        self.ui.comboBox_aqu.activated[str].connect(self.aquicition)
        self.ui.comboBox_prep.activated[str].connect(self.preparation)
        self.ui.brightness.valueChanged.connect(self.slider_brightness)
        self.ui.contrast.valueChanged.connect(self.slider_contrast)
        self.ui.phantom1.mousePressEvent = self.position

########################################################################################################################

    def T_ir(self):
        self.ti = self.ui.spinBox.value()

    def st_cycle(self):  #changing the value of startup cycle
        self.stcy = self.ui.spinBox_stcy.value()

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
                    self.pd_array[v][b] = 150
                elif (self.arr[v][b] > 29) & (self.arr[v][b] <= 107):
                    self.t11_array[v][b] = 900
                    self.t2_array[v][b] = 130
                    self.pd_array[v][b] = 20
                elif self.arr[v][b] >= 107:
                    self.t11_array[v][b] = 1100
                    self.t2_array[v][b] = 230
                    self.pd_array[v][b] = 250
        self.current_text()
        #print(self.t1_array)
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

########################################################################################################################
    def ernset(self):  # ??????? ????? T1 array
        T1 = 800
        FA = np.arange(0, 95, 2)
        Intensity = np.zeros((len(FA)))
        spinz = 1
        signal = 0
        for idx, theta in enumerate(FA):
            # signal = signal* np.sin(theta*np.pi/180)
            for i in range(20):
                signal = spinz * np.sin(theta * np.pi / 180)
                spinz = spinz * np.cos(theta * np.pi / 180) + (1 - spinz * np.cos(theta * np.pi / 180)) * (
                            1 - np.exp(-self.tr / T1))
            Intensity[idx] = signal
            spinz = 1

        self.ui.ernst_graph.plot(FA, Intensity, pen='w')

    def gre_prep(self, t1_array, TR, FA,PreparedPhantom):
        theta = np.radians(FA)
        row, col = self.arr.shape
     #   phantom = self.Phantom(row, col)  # Creating phantom as a 3D array, each pixel has a vector
        phantom = np.zeros([row, col, 3])
        phantom[:, :, 2] = PreparedPhantom
        phantom = self.RF_rotate(theta, phantom)
        phantom = self.rotate_decay(theta, self.te, self.t2_array, phantom)
        Phantom = phantom[:, :, 0]
        return Phantom

    def k_space(self, phantom):
        row, col = phantom.shape
        kspace = np.zeros((row, col), dtype=np.complex)

        for r in range(row):  # rows
            for c in range(col):
                Gx_step = ((2 * math.pi) / row) * r  # Frequency encodind
                Gy_step = ((2 * math.pi) / col) * c  # Phase encodind
                for ph_row in range(row):
                    for ph_col in range(col):
                        Toltal_theta = (Gx_step * ph_row) + (Gy_step * ph_col)
                        Mag = np.absolute(phantom[ph_row, ph_col])
                        kspace[r, c] = kspace[r, c] + (Mag * np.exp(-1j * Toltal_theta))
                        QApplication.processEvents()
                QApplication.processEvents()
        return kspace

    def ssfp(self, t1_array, TR, FA, PreparedPhantom):
        row, col = self.arr.shape
        theta = np.radians(FA)
        kspace_ssfp = np.zeros((row, col), dtype=np.complex)
        #phantom = self.Phantom(row, col)
        phantom = np.zeros([row, col, 3])
        phantom[:, :, 2] = PreparedPhantom
        # startup cycle with 0.5 theta
        phantom = self.startup_cycle(theta / 2, self.stcy, phantom)
        # rotate and decay
        phantom = self.rotate_decay(theta, self.te, self.t2_array, phantom)
        # startup cycle with theta
        phantom = self.startup_cycle(theta, self.stcy, phantom)
        for r in range(row):  # rows
            phantom = self.rotate_decay(theta, self.te, self.t2_array, phantom)
            for c in range(col):
                Gx_step = ((2 * math.pi) / row) * r  # Frequency encodind
                Gy_step = ((2 * math.pi) / col) * c  # Phase encodind
                for i in range(row):
                    for j in range(col):
                        Toltal_theta = (Gx_step * i) + (Gy_step * j)
                        Mag = math.sqrt(((phantom[i, j, 0]) * (phantom[i, j, 0])) +
                                        ((phantom[i, j, 1]) * (phantom[i, j, 1])))

                        kspace_ssfp[r, c] = kspace_ssfp[r, c] + (Mag * np.exp(-1j * Toltal_theta))
                        QApplication.processEvents()

                QApplication.processEvents()
            theta = -theta #for ernst angle
            #print(theta)
            for l in range(row):
                for m in range(col):
                    phantom[l, m, 2] = ((phantom[l, m, 2]) * np.exp(-TR / t1_array[l, m])) + (1 - np.exp(
                                                             -TR / t1_array[l, m]))

            QApplication.processEvents()
        return kspace_ssfp
    """
    def ssfp(self, TE, TR, T1, T2, pd, filpAngle, prep, cycles):
        ## initializie
        pd = np.asarray(pd)
        T1 = np.asarray(T1)
        T2 = np.asarray(T2)
        filpAngle = np.radians(filpAngle)
        row, col = np.shape(pd)
        kspace = np.zeros([row, col], dtype=np.complexfloating)

        # re rotation
        ## modifing to a vector
        x = np.array([[0.0], [0.0], [1.0]])
        spin = pd.tolist()
        yRotMat = np.array([[np.cos(filpAngle / 2), 0, np.sin(filpAngle / 2)], [0, 1, 0],
                            [-np.sin(filpAngle / 2), 0, np.cos(filpAngle / 2)]])
        for i in range(row):
            for j in range(col):
                # spin[i][j]=x*((1-np.exp(-TR/T1[i][j]))**startup)
                spin[i][j] = x * prep[i, j]
        spin = np.array(spin)
        spin = startup(TE, TR, T1, T2, spin, filpAngle, cycles)
        # start kspace
        for kRow in range(row):
            # Rf
            # rotation around y axis
            if (kRow != 0):
                yRotMat = np.array(
                    [[np.cos(filpAngle), 0, np.sin(filpAngle)], [0, 1, 0], [-np.sin(filpAngle), 0, np.cos(filpAngle)]])
            filpAngle *= -1
            for i in range(row):
                for j in range(col):
                    spin[i][j] = np.matmul(yRotMat, spin[i][j])
            #       #decay
            for i in range(row):
                for j in range(col):
                    spin[i][j][0] = spin[i][j][0] * np.exp(-TE / T2[i][j])
                    spin[i][j][1] = spin[i][j][1] * np.exp(-TE / T2[i][j])
            # gradiant and read data
            for kcol in range(col):
                stepi = 2 * np.pi / (row) * (kRow)
                stepj = 2 * np.pi / (row) * (kcol)

                for i in range(row):
                    for j in range(col):
                        theta = stepi * i + stepj * j
                        kspace[kRow][kcol] += (np.sqrt(np.square(spin[i][j][0]) + np.square(spin[i][j][1])) * np.exp(
                            complex(0, -theta)))
            ''' # recovery  
            for i in range(row):
                for j in range  (col):
                    spin[i][j][2]*=(1-np.exp(-TR/T1[i][j]))'''

        return kspace
    """
    def spinEcho(self, TE, TR, T1Arr, T2Arr, PreparedPhantom, StartUpNumber):

        # Create Magnetic Field array
        [rows, columns] = np.shape(T1Arr)
        Phantom = np.zeros([rows, columns, 3])
        mappedPhantom = 0  # for not affecting the main phantom
        Phantom[:, :, 2] = PreparedPhantom

        # Create empty K_space and gradients
        kspace = np.zeros([rows, columns], dtype=complex)
        Gx = 2 * np.pi / columns
        Gy = 2 * np.pi / rows

        # Convert T2* to T2 (ie simulate the elemination of inhomogenity)
        T2Arrnew = T2Arr * 2.5

        # Create rotation matrix with pi/2 degree around x axis
        Rotate90X = np.array(
            [[1, 0, 0], [0, np.cos(np.pi / 2), np.sin(np.pi / 2)], [0, -np.sin(np.pi / 2), np.cos(np.pi / 2)]])

        # Create rotation matrix with pi degree around x axis
        Rotate180X = np.array([[1, 0, 0], [0, np.cos(np.pi), np.sin(np.pi)], [0, -np.sin(np.pi), np.cos(np.pi)]])

        # Start UP sequence
        for x in range(StartUpNumber):
            for i in range(rows):
                for j in range(columns):
                    # Rotate by 90
                    Phantom[i, j, :] = Rotate90X.dot(Phantom[i, j, :])

                    # Decay in XY plane and Recover the difference in z for half TE
                    Decay = np.array(
                        [[np.exp(-(TE / 2) / T2Arrnew[i, j]), 0, 0], [0, np.exp(-(TE / 2) / T2Arrnew[i, j]), 0],
                         [0, 0, 1]])
                    Phantom[i, j, :] = Decay.dot(Phantom[i, j, :]) + [0, 0, (
                                1 - np.exp(-(TE / 2) / T1Arr[i, j]))]  # Recover only the residual part

                    # Rotate by 180
                    Phantom[i, j, :] = Rotate180X.dot(Phantom[i, j, :])

                    # Decay in XY plane and Recover the difference in z for another half TE
                    Decay = np.array(
                        [[np.exp(-(TE / 2) / T2Arrnew[i, j]), 0, 0], [0, np.exp(-(TE / 2) / T2Arrnew[i, j]), 0],
                         [0, 0, 1]])
                    Phantom[i, j, :] = Decay.dot(Phantom[i, j, :]) + [0, 0, (1 - Phantom[i, j, 2]) * (
                                1 - np.exp(-(TE / 2) / T1Arr[i, j]))]  # Recover only the residual part

                    # Decay and Recover for TR
                    Decay = np.array(
                        [[np.exp(-(TR - TE) / T2Arrnew[i, j]), 0, 0], [0, np.exp(-(TR - TE) / T2Arrnew[i, j]), 0],
                         [0, 0, 1]])
                    Phantom[i, j, :] = Decay.dot(Phantom[i, j, :]) + [0, 0, (1 - Phantom[i, j, 2]) * (
                                1 - np.exp(-(TR - TE) / T1Arr[i, j]))]  # Recover only the residual part
                    QApplication.processEvents()
                QApplication.processEvents()
            QApplication.processEvents()

        # Spin Echo sequence
        # For each row in k_space
        for kr in range(rows):
            # Record complete row
            for kc in range(columns):
                result = 0
                for i in range(rows):
                    for j in range(columns):
                        # Rotate by 90
                        Phantom[i, j, :] = Rotate90X.dot(Phantom[i, j, :])

                        # Decay in XY plane and Recover the difference in z for half TE
                        Decay = np.array(
                            [[np.exp(-(TE / 2) / T2Arrnew[i, j]), 0, 0], [0, np.exp(-(TE / 2) / T2Arrnew[i, j]), 0],
                             [0, 0, 1]])
                        Phantom[i, j, :] = Decay.dot(Phantom[i, j, :]) + [0, 0, (1 - Phantom[i, j, 2]) * (
                                    1 - np.exp(-(TE / 2) / T1Arr[i, j]))]

                        # Rotate by 180
                        Phantom[i, j, :] = Rotate180X.dot(Phantom[i, j, :])

                        # Decay in XY plane and Recover the difference in z for another half TE
                        Decay = np.array(
                            [[np.exp(-(TE / 2) / T2Arrnew[i, j]), 0, 0], [0, np.exp(-(TE / 2) / T2Arrnew[i, j]), 0],
                             [0, 0, 1]])
                        Phantom[i, j, :] = Decay.dot(Phantom[i, j, :]) + [0, 0, (1 - Phantom[i, j, 2]) * (
                                    1 - np.exp(-(TE / 2) / T1Arr[i, j]))]  # Recover only the residual part

                        # read in y with gradient and accumulate all cells
                        mappedPhantom = np.copy(Phantom[i, j, 1])
                        mappedPhantom = abs(mappedPhantom)  # eliminate the negative sign
                        mappedPhantom = mappedPhantom * 255  # map to [0,255]
                        result = abs(mappedPhantom) * np.exp(-1j * (Gy * i * kr + Gx * j * kc)) + result
                        # QApplication.processEvents()

                        # Decay and Recover for TR
                        Decay = np.array(
                            [[np.exp(-(TR - TE) / T2Arrnew[i, j]), 0, 0], [0, np.exp(-(TR - TE) / T2Arrnew[i, j]), 0],
                             [0, 0, 1]])
                        Phantom[i, j, :] = Decay.dot(Phantom[i, j, :]) + [0, 0, (1 - Phantom[i, j, 2]) * (
                                    1 - np.exp(-(TR - TE) / T1Arr[i, j]))]  # Recover only the residual part
                        QApplication.processEvents()
                    QApplication.processEvents()
                QApplication.processEvents()

                # Fill one cell in K space
                kspace[kr, kc] = result
                # print('Loading')

        kspace = np.around(kspace)  # because of very small fractions
        # print('Done')
        image = np.fft.ifft2(kspace)
        trans = qimage2ndarray.array2qimage(image)
        pixmap = QPixmap(trans)
        # self.ui.phantom5.setPixmap(pixmap)
        self.viewer.setPhoto(pixmap)
        fshift = np.fft.fftshift(kspace)
        kspaceoutput = 20 * np.log(np.abs(fshift))
        # print(kspaceoutput)
        # print(minks, maxks)
        trans = qimage2ndarray.array2qimage(kspaceoutput)
        res = QPixmap(trans)
        self.ui.phantom6.setPixmap(res)

    def IR(self, startup, T1, tissue):
        print(T1)
        row, col = np.shape(startup)
        prep = np.zeros([row, col])
        tNull = tissue * np.log(2)
        for i in range(row):
            for j in range(col):
                prep[i, j] = startup[i, j] * (1 - 2 * np.exp(-tNull / T1[i, j]))
        print(prep)
        return prep
    """
    def ir(self, t1_array, t2_array, Ti):

        # Create_array_of_magnetic_field_in_z_direction
       # [h, w] = np.shape(t1_array)
       # Phantom = np.zeros([h, w, 3])
       # Phantom[:, :, 2] = 1
        row, col = self.arr.shape
        Phantom = self.Phantom(row, col)
        RF1 = np.array([[math.cos(math.pi), 0, math.sin(math.pi)], [0, 1, 0],
                        [-math.sin(math.pi), 0, math.cos(math.pi)]])  # Rotate around y-axis with angle 180
        #RF = ([[np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [-np.sin(theta), 0, np.cos(theta)]])

        for i in range(row):
            for j in range(col):
                IR = np.array([[np.exp(-Ti / t2_array[i, j]), 0, 0], [0, np.exp(-Ti / t2_array[i, j]), 0],
                               [0, 0, 1 - np.exp(-Ti / t1_array[i, j])]])

                Phantom[i, j, :] = np.dot(RF1, Phantom[i, j, :])  # Phantom after rotation around 180 around x-axis

                Phantom[i, j, :] = np.dot(IR, Phantom[i, j, :]) + np.array(
                    [0, 0, 1 - np.exp(-Ti / t1_array[i, j])])  # Phantom after decay at x-y plane (on y-axis)

        return Phantom[:, :, 0]
    """
    def T2Prep(self, t1_array, t2_array, TE):

        # Create_array_of_magnetic_field_in_z_direction
        row, col = self.arr.shape
        #Phantom = np.zeros([row, col, 3])
        #Phantom[:, :, 2] = 1
        phantom = self.Phantom(row, col)
        RF1 = np.array([[math.cos(math.pi / 2), 0, math.sin(math.pi / 2)], [0, 1, 0],
                        [-math.sin(math.pi / 2), 0, math.cos(math.pi / 2)]])  # Rotate around y-axis with angle 90
        RF2 = np.array([[math.cos(math.pi), 0, math.sin(math.pi)], [0, 1, 0],
                        [-math.sin(math.pi), 0, math.cos(math.pi)]])  # Rotate around y-axis with angle 180

        for i in range(row):
            for j in range(col):
                decayrecovery = np.array([[np.exp(-TE / t2_array[i, j]), 0, 0], [0, np.exp(-TE / t2_array[i, j]), 0],
                                          [0, 0, 1 - np.exp(-TE / t1_array[i, j])]])

                phantom[i, j, :] = np.dot(RF1, phantom[i, j, :])  # Phantom after rotation around 90 around y-axis

                phantom[i, j, :] = np.dot(decayrecovery, phantom[i, j, :]) + np.array(
                    [0, 0, 1 - np.exp(-TE / t1_array[i, j])])  # Phantom after decay at x-y plane (on y-axis)

                phantom[i, j, :] = np.dot(RF2, phantom[i, j, :])  # Phantom after rotation around 90 then 180 around y-axis
        return phantom[:, :, 0]
        print(phantom.shape)

    def tagging_prep(self, array, step):
        row, col =self.arr.shape
        for i in range(row):
            for j in range(1, col, step):
                array[i][j] *= np.sin(np.pi * i / col)
        return array

########################################################################################################################

    def run(self):
        self.preparation()

    def preparation(self):
        value = (self.ui.comboBox_prep.currentText())
        if value == 'Preparation':
            QMessageBox.information(self, 'Message', ' you should select aquisition type ')
        elif value == 'IR':
            row, col = self.arr.shape
            #Phantom = np.zeros([row, col, 3])
            #Phantom[:, :, 2] = 1
            self.value = 1
            self.t1prep_phantom = self.IR(self.arr, self.t1_array, 660)
            self.aquicition()
            #self.preperation_pulse('IR', self.x2_range, 100)
        elif value == 'T2_Prep':
            self.value = 2
            self.t2prep_phantom = self.T2Prep(self.t11_array, self.t2_array, self.te)
            self.aquicition()
            #self.preperation_pulse('T2_Prep', self.x2_range, 130)

        elif value == 'Tagging':
            self.value = 3
            self.tagging_phantom = self.tagging_prep(self.arr, 2)
            self.aquicition()
            #self.preperation_pulse('Tagging', self.x2_range, 100)

    def aquicition(self):
        text = (self.ui.comboBox_aqu.currentText())
        if text == 'Aquisition':
            QMessageBox.information(self, 'Message', ' you should select aquisition type ')
        elif text == 'GRE' and self.value == 1:
            self.ui.graphicsView.clear()
            signal = self.gre_prep(self.t1prep_phantom, self.tr, self.fa, self.t1prep_phantom)
            print(signal.shape)
            maxsig = np.max(signal)
            minsig = np.min(signal)
            mapsig = (255 / (maxsig - minsig)) * (signal - minsig)
            kspace = self.k_space(mapsig)
            self.show_image(kspace)
            self.preperation_pulse('IR', self.x_range, 100)
            self.acquisition_pulse('GRE', self.x2_range, self.te, self.fa)
        elif text == 'GRE' and self.value == 2:
            self.ui.graphicsView.clear()
            signal = self.gre_prep(self.t2prep_phantom, self.tr, self.fa, self.t2prep_phantom)
            print(signal.shape)
            maxsig = np.max(signal)
            minsig = np.min(signal)
            mapsig = (255 / (maxsig - minsig)) * (signal - minsig)
            kspace = self.k_space(mapsig)
            self.show_image(kspace)
            self.preperation_pulse('T2_Prep', self.x_range, 130)
            self.acquisition_pulse('GRE', self.x2_range, self.te, self.fa)
        elif text == 'GRE' and self.value == 3:
            self.ui.graphicsView.clear()
            signal = self.gre_prep(self.tagging_phantom, self.tr, self.fa, self.tagging_phantom)
            print(signal.shape)
            maxsig = np.max(signal)
            minsig = np.min(signal)
            mapsig = (255 / (maxsig - minsig)) * (signal - minsig)
            kspace = self.k_space(mapsig)
            self.show_image(kspace)
            self.preperation_pulse('Tagging', self.x_range, 100)
            self.acquisition_pulse('GRE', self.x2_range, self.te, self.fa)
        elif text == 'SSFP' and self.value == 1:
            self.ui.graphicsView.clear()
            kspace = self.ssfp(self.t1_array, self.tr, self.fa, self.t1prep_phantom)
            self.show_image(kspace)
            self.preperation_pulse('IR', self.x_range, 100)
            self.acquisition_pulse('SSFP', self.x2_range, self.te, self.fa)
        elif text == 'SSFP' and self.value == 2:
            self.ui.graphicsView.clear()
            kspace = self.ssfp(self.t1_array, self.tr, self.fa, self.t2prep_phantom)
            self.show_image(kspace)
            self.preperation_pulse('T2_Prep', self.x_range, 130)
            self.acquisition_pulse('SSFP', self.x2_range, self.te, self.fa)
        elif text == 'SSFP' and self.value == 3:
            self.ui.graphicsView.clear()
            kspace = self.ssfp(self.t1_array, self.tr, self.fa, self.tagging_phantom)
            self.show_image(kspace)
            self.preperation_pulse('Tagging', self.x_range, 100)
            self.acquisition_pulse('SSFP', self.x2_range, self.te, self.fa)
        elif text == 'SE' and self.value == 1:
            self.ui.graphicsView.clear()
            kspace = self.spinEcho(self.te, self.tr, self.t1_array, self.t2_array, self.t1prep_phantom, self.stcy)
            #self.show_image(kspace)
            self.preperation_pulse('IR', self.x_range, 100)
            self.acquisition_pulse('SE', self.x2_range, self.te, self.fa)
        elif text == 'SE' and self.value == 2:
            self.ui.graphicsView.clear()
            kspace = self.spinEcho(self.te, self.tr, self.t1_array, self.t2_array, self.t2prep_phantom, self.stcy)
            #self.show_image(kspace)
            self.preperation_pulse('T2_Prep', self.x_range, 130)
            self.acquisition_pulse('SE', self.x2_range, self.te, self.fa)
        elif text == 'SE' and self.value == 3:
            self.ui.graphicsView.clear()
            kspace = self.spinEcho(self.te, self.tr, self.t1_array, self.t2_array, self.tagging_phantom, self.stcy)
            #self.show_image(kspace)
            self.preperation_pulse('Tagging', self.x_range, 100)
            self.acquisition_pulse('SE', self.x2_range, self.te, self.fa)


        #print(kspace)
        #np.set_printoptions(threshold=np.inf)
        #kspace = self.ssfp(self.t11_array, self.tr, self.fa)
        #print(kspace)

    def show_image(self, kspace):
        #global pixmap
        output = np.absolute(np.fft.ifft2(kspace))  # simple ifft2 to bring back the image.
        maxoutput = np.max(output)
        minoutput = np.min(output)
        mapoutput = (255 / (maxoutput - minoutput)) * (output - minoutput)
        trans = qimage2ndarray.array2qimage(mapoutput)
        pixmap = QPixmap(trans)
        #self.ui.phantom5.setPixmap(pixmap)
        self.viewer.setPhoto(pixmap)
        fshift = np.fft.fftshift(kspace)
        kspaceoutput = 20 * np.log(np.abs(fshift))
        # print(kspaceoutput)
        minks = np.min(kspaceoutput)
        maxks = np.max(kspaceoutput)
        # print(minks, maxks)
        kspacemap = [255 / (maxks - minks)] * (kspaceoutput - minks)
        trans = qimage2ndarray.array2qimage(kspacemap)
        res = QPixmap(trans)
        self.ui.phantom6.setPixmap(res)
        return kspace

########################################################################################################################

    def RF_rotate(self, theta, phantom):
        row, col = self.arr.shape
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
        for i in range(row):
            for j in range(col):
                phantom[i, j, :] = self.rotate(theta, phantom[i, j, :])
                phantom[i, j, :] = self.decay(phantom[i, j, :], TE, T2[i, j])
        return phantom

    def recovery(self, TR, T1, phantom):
        row, col = self.arr.shape
        for i in range(row):
            for j in range(col):
                phantom[i, j, 0] = 0
                phantom[i, j, 1] = 0
                phantom[i, j, 2] = ((phantom[i, j, 2]) * np.exp(
                    -TR / T1[i, j])) + (1 - np.exp(-TR / T1[i, j]))
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

    def spin_Echo(self, t1, t2, tr, te, fa,Prepared_phantom):
        row, col = self.arr.shape
        theta = np.radians(fa)
        Kspace_SE =np.zeros([row, col], dtype=complex)
        #phantom = self.Phantom(row, col)
        phantom = np.zeros([row, col, 3])
        phantom[:, :, 2] = Prepared_phantom
        phantom = self.startup_cycle(theta, self.stcy, phantom)

        for r in range(Kspace_SE.shape[0]):  # rows
            phantom = self.rotate_decay(theta, self.te / 2, self.t2_array, phantom)
            phantom = self.recovery(self.tr, self.t1_array, phantom)
            phantom = self.rotate_decay(2 * theta, self.te / 2, self.t2_array, phantom)
            for c in range(Kspace_SE.shape[1]):

                Gx_step = ((2 * math.pi) / row) * r
                Gy_step = (2* math.pi / col) * c
                for ph_row in range(row):
                    for ph_col in range(col):
                        Toltal_theta = (Gx_step * ph_row) + (Gy_step * ph_col)
                        Mag = math.sqrt(((phantom[ph_row, ph_col, 0])(phantom[ph_row, ph_col, 0])) + (
                            (phantom[ph_row, ph_col, 1])(phantom[ph_row, ph_col, 1])))

                        Kspace_SE[r, c] = Kspace_SE[r, c] + (Mag * np.exp(-1j * Toltal_theta))
                        QApplication.processEvents()

                QApplication.processEvents()

            phantom = self.recovery(self.tr, self.t1_array, phantom)
        return Kspace_SE


########################################################################################################################
    def RectangularGraph(self, tr, y_shift, x_shift, height, width):
        z = []

        for i in range(0, tr):
            if i < int(x_shift - width):
                z.append(y_shift)
            elif i >= int(x_shift - width) and i < int(width + x_shift):
                z.append(y_shift + (height * 1))
            else:
                z.append(y_shift)
        return z

    def draw_rf_pulse(self, x_range, shift_x, shift_y, flip_angle):

        amp = int(flip_angle * 2 / 180)

        sinc = np.sin(amp * (x_range - shift_x)) / (x_range - shift_x) + shift_y

        return sinc

    # def sin(self,x_range , amp , shift_x , shift_y):
    #
    #     return np.sin(amp*(x_range-shift_x))+shift_y

    def tagging(self, x_range):
        start_pos = x_range.min()
        end_pos = 100
        self.prep_end_pos = end_pos
        x_range = np.arange(0, self.prep_end_pos, .001)
        # print(x_range.min())
        self.ui.graphicsView.plot(x_range, self.draw_rf_pulse(x_range, start_pos + 10, 7, 90), pen='y')  # 90
        self.ui.graphicsView.plot(x_range, self.draw_rf_pulse(x_range, start_pos + 50, 7, 90), pen='y')  # 90

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 5, start_pos + 70, 1, 5), pen='y')  # G_spoiler
        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 5, start_pos + 30, 0.5, 5), pen='y')  # G_tag
        self.x2_range = np.arange(self.prep_end_pos, 400, .001)
        print(self.prep_end_pos)

    def inversion_recovery(self, x_range, t1):

        start_pos = x_range.min() + 10
        ti = t1 * np.log(2)
        if ti > 100:
            ti = ti % 100
            if ti % 100 == 0:
                ti = 100
        self.prep_end_pos = ti + 50
        x_range = np.arange(0, self.prep_end_pos, .001)
        self.ui.graphicsView.plot(x_range, self.draw_rf_pulse(x_range, start_pos, 7, 180), pen='y')  # 180
        self.ui.graphicsView.plot(x_range, self.draw_rf_pulse(x_range, start_pos + ti, 7, 90), pen='y')  # 90
        self.x2_range = np.arange(self.prep_end_pos, 400, .001)

    def t2_prep(self, x_range, t2_prep_value):
        start_pos = x_range.min() + 10
        if t2_prep_value > 100:
            t2_prep_value = t2_prep_value % 100
            if t2_prep_value % 100 == 0:
                t2_prep_value = 100
        self.prep_end_pos = t2_prep_value + 50
        x_range = np.arange(0, self.prep_end_pos, .001)
        self.ui.graphicsView.plot(x_range, self.draw_rf_pulse(x_range, start_pos, 7, 90), pen='y')  # 90
        self.ui.graphicsView.plot(x_range, self.draw_rf_pulse(x_range, start_pos + t2_prep_value, 7, -90),
                                  pen='y')  # -90
        self.x2_range = np.arange(self.prep_end_pos, 400, .001)


    def spin_echo_seq(self, x_range, te):

        # RF pulse

        taw = te / 2

        start_pos = x_range.min()
        end_pos = int(x_range.max())

        self.ui.graphicsView.plot(x_range, self.draw_rf_pulse(x_range, start_pos + taw / 4, 7, 90), pen='b')  # 90

        self.ui.graphicsView.plot(x_range, self.draw_rf_pulse(x_range, start_pos + taw, 7, 180), pen='b')  # 180

        # gradients

        # Gz
        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 5, start_pos + taw / 4, 0.5, taw / 10), pen='g')

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 5, start_pos + taw, 0.5, taw / 10), pen='g')

        # Gy

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 3, start_pos + te - 2 * te / 10, 0.4, te / 10),
                                  pen='r')

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 3, start_pos + te - 2 * te / 10, 0.2, te / 10),
                                  pen='r')

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 3, start_pos + te - 2 * te / 10, -0.2, te / 10),
                                  pen='r')

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 3, start_pos + te - 2 * te / 10, -0.4, te / 10),
                                  pen='r')

        # read out

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 1, start_pos + te, 0.4, te / 10), pen='w')

    def gre(self, x_range, te, flip_angle):

        start_pos = x_range.min()
        end_pos = int(x_range.max())
        print(start_pos)
        self.ui.graphicsView.plot(x_range, self.draw_rf_pulse(x_range, start_pos + te - 2 * 16, 7, flip_angle),
                                  pen='b')  # 90

        # gradients

        # 16 width of gx = 5 + 10 + 1

        # Gz

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 5, start_pos + te - 2 * 16, 0.5, 5), pen='g')

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 5, start_pos + te - 16, -0.5, 10), pen='g')

        # Gy

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 3, start_pos + te - 16, 0.4, 5), pen='r')

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 3, start_pos + te - 16, 0.2, 5), pen='r')

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 3, start_pos + te - 16, -0.2, 5), pen='r')

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 3, start_pos + te - 16, -0.4, 5), pen='r')

        # read out

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 1, start_pos + te - 16, -0.4, 5), pen='w')
        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 1, start_pos + te, 0.4, 10), pen='w')

    def sSFp_seq(self, x_range, te, flip_angle):

        start_pos = x_range.min()

        end_pos = int(x_range.max())

        self.ui.graphicsView.plot(x_range, self.draw_rf_pulse(x_range, start_pos + 10 * te / 20, 7, flip_angle),
                                  pen='b')  # 90

        # Gz

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 5, start_pos + 7 * te / 20 - 1, -0.5, te / 20),
                                  pen='g')

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 5, start_pos + 10 * te / 20, 0.5, te / 10), pen='g')

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 5, start_pos + 13 * te / 20 + 1, -0.5, te / 20),
                                  pen='g')

        # Gy

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 3, start_pos + 15 * te / 20, 0.4, te / 20 - 1),
                                  pen='r')

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 3, start_pos + 15 * te / 20, 0.2, te / 20 - 1),
                                  pen='r')

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 3, start_pos + 15 * te / 20, -0.2, te / 20 - 1),
                                  pen='r')

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 3, start_pos + 15 * te / 20, -0.4, te / 20 - 1),
                                  pen='r')

        # read out

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 1, start_pos + 17 * te / 20 - 1, -0.4, te / 20),
                                  pen='w')
        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 1, start_pos + te, 0.4, te / 10), pen='w')
        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 1, start_pos + 23 * te / 20 + 1, -0.4, te / 20),
                                  pen='w')

        # -Gy

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 3, start_pos + 25 * te / 20, 0.4, te / 20 - 1),
                                  pen='r')

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 3, start_pos + 25 * te / 20, 0.2, te / 20 - 1),
                                  pen='r')

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 3, start_pos + 25 * te / 20, -0.2, te / 20 - 1),
                                  pen='r')

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 3, start_pos + 25 * te / 20, -0.4, te / 20 - 1),
                                  pen='r')

        # -Gz

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 5, start_pos + 27 * te / 20 - 1, -0.5, te / 20),
                                  pen='g')

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 5, start_pos + 30 * te / 20, 0.5, te / 10), pen='g')

        self.ui.graphicsView.plot(self.RectangularGraph(end_pos, 5, start_pos + 33 * te / 20 + 1, -0.5, te / 20),
                                  pen='g')

        # -90

        self.ui.graphicsView.plot(x_range, self.draw_rf_pulse(x_range, start_pos + 30 * te / 20, 7, -flip_angle),
                                  pen='b')

    def preperation_pulse(self, prep_name, x_range, unique_parameter):
        if prep_name == 'IR':
            self.inversion_recovery(x_range, unique_parameter)
        elif prep_name == 'T2Prep':
            self.t2_prep(x_range, unique_parameter)
        elif prep_name == 'Tagging':
            self.tagging(x_range)

    def acquisition_pulse(self, seq_name, x_range, te, flip_angle):
        if seq_name == 'GRE':
            self.gre(x_range, te, flip_angle)

        elif seq_name == 'SSFP':
            self.sSFp_seq(x_range, te, flip_angle)

        elif seq_name == 'SE':
            self.spin_echo_seq(x_range, te)

########################################################################################################

    def zoomControl(self, value):
        def clearZoom(obj):
            if (obj._zoom > 0):
                obj.scale(pow(0.8, obj._zoom), pow(0.8, obj._zoom))
            else:
                obj.scale(pow(1.25, abs(obj._zoom)), pow(1.25, abs(obj._zoom)))
            obj._zoom = 0

        if (value == 'separated'):
            self.viewer.toggleDragMode(1)
            #self.port1.wheelEvent = self.port1.wheel
            self.viewer.wheelEvent = self.viewer.wheel
            #self.port1.mousePressEvent = self.port1.mousePress
            self.viewer.mousePressEvent = self.viewer.mousePress
            #self.port1.mouseMoveEvent = self.port1.mouseMove
            self.viewer.mouseMoveEvent = self.viewer.mouseMove
            #self.port1.mouseReleaseEvent = self.port1.mouseRelease
            self.viewer.mouseReleaseEvent = self.viewer.mouseRelease
        elif (value == 'Linked'):
            clearZoom(self.viewer)
            clearZoom(self.port1)
            self.viewer.toggleDragMode(1)
            #self.port1.wheelEvent = self.zoomLink
            self.viewer.wheelEvent = self.zoomLink
            #self.port1.mousePressEvent = self.mousePressLink
            self.viewer.mousePressEvent = self.mousePressLink
            #self.port1.mouseMoveEvent = self.mouseMoveLink
            self.viewer.mouseMoveEvent = self.mouseMoveLink
            #self.port1.mouseReleaseEvent = self.mouseReleaseLink
            self.viewer.mouseReleaseEvent = self.mouseReleaseLink

    def zoomLink(self, event):
        self.viewer.wheel(event)
        #self.port1.wheel(event)

    def mousePressLink(self, event):
        self.viewer.mousePress(event)
        #self.port1.mousePress(event)

    def mouseMoveLink(self, event):
        self.viewer.mouseMove(event)
        #self.port1.mouseMove(event)

    def mouseReleaseLink(self, event):
        self.viewer.mouseRelease(event)
        #self.port1.mouseRelease(event)

########################################################################################################################

class PhotoViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(int, int)

    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True

        self.wheelEvent = self.wheel
        self.mousePressEvent = self.mousePress
        self.mouseMoveEvent = self.mouseMove
        self.mouseReleaseEvent = self.mouseRelease

        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
        self.setResizeAnchor(QtWidgets.QGraphicsView.NoAnchor)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QBrush(QColor(30, 30, 30)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 0, 0))
                # self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.oiginal = pixmap
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        # self.fitInView()

    def wheel(self, event):
        if self.hasPhoto() and self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            # print(event.pos().x(), 'x', event.pos().y())
            print(self._photo.pixmap().size())
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.scale(factor, factor)
            else:
                self._zoom = 0
            # self.photoZoomed.emit(factor,self._zoom)

    def zoom(self, factor, zoom):
        if self.hasPhoto() and self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            print(zoom)
            self._zoom = zoom
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def toggleDragMode(self, val):
        if (val == 0):
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        elif (val == 1) and (not self._photo.pixmap().isNull()):
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def mousePress(self, event):
        
        super(PhotoViewer, self).mousePressEvent(event)

    def mouseRelease(self, event):
        super(PhotoViewer, self).mouseReleaseEvent(event)

    def mouseMove(self, event):
        super(PhotoViewer, self).mouseMoveEvent(event)

########################################################################################################################




def main():
    app = QApplication(sys.argv)
    application = Program()
    application.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()