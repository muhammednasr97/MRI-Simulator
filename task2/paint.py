from PyQt5 import QtWidgets, QtGui, QtCore

image = np.copy(self.res)
        image = np.dstack([image, image, image])
        cv2.rectangle(image, (self.x - 1, self.y - 1, 1, 1), (0, 255, 0), 1)
        image = qimage2ndarray.array2qimage(image)
        res = QPixmap(image)
        self.ui.phantom1.setPixmap(res)


painter = QPainter(self.res)
        painter.begin(self)
        pen = QPen(QtCore.Qt.red)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRect(self.x, self.y, 1, 1)
        self.ui.phantom1.setPixmap(self.res)
        painter.end()
        QApplication.processEvents()