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
        if self._photo.isUnderMouse():
            self.photoClicked.emit(QtCore.QPoint(event.pos()))
        super(PhotoViewer, self).mousePressEvent(event)

    def mouseRelease(self, event):
        super(PhotoViewer, self).mouseReleaseEvent(event)

    def mouseMove(self, event):
        super(PhotoViewer, self).mouseMoveEvent(event)


class ApplicationWindow(QtWidgets.QMainWindow):
    resized = pyqtSignal()

    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.viewer = PhotoViewer(self)  # object for the basic phantom
        self.port1 = PhotoViewer(self)  # object for the first view port
        self.zoomControl('Linked zooming')  # set zooming setting to linked zooming at the start of the program
        self.ui.cbZoom.currentTextChanged.connect(self.zoomControl)  # combo box to control zooming settings

        self.ui.gridLayout_5.addWidget(self.viewer, 1, 1)  # add the 'viewer' graphicsview object to a layout
        self.ui.gridLayout_7.addWidget(self.port1, 2, 1)  # add the 'port1' graphicsview object to a layout

    def zoomControl(self, value):
        def clearZoom(obj):
            if (obj._zoom > 0):
                obj.scale(pow(0.8, obj._zoom), pow(0.8, obj._zoom))
            else:
                obj.scale(pow(1.25, abs(obj._zoom)), pow(1.25, abs(obj._zoom)))
            obj._zoom = 0

        if (value == 'Zooming'):
            self.viewer.toggleDragMode(1)
            self.port1.wheelEvent = self.port1.wheel
            self.viewer.wheelEvent = self.viewer.wheel
            self.port1.mousePressEvent = self.port1.mousePress
            self.viewer.mousePressEvent = self.viewer.mousePress
            self.port1.mouseMoveEvent = self.port1.mouseMove
            self.viewer.mouseMoveEvent = self.viewer.mouseMove
            self.port1.mouseReleaseEvent = self.port1.mouseRelease
            self.viewer.mouseReleaseEvent = self.viewer.mouseRelease
        elif (value == 'Linked zooming'):
            clearZoom(self.viewer)
            clearZoom(self.port1)
            self.viewer.toggleDragMode(1)
            self.port1.wheelEvent = self.zoomLink
            self.viewer.wheelEvent = self.zoomLink
            self.port1.mousePressEvent = self.mousePressLink
            self.viewer.mousePressEvent = self.mousePressLink
            self.port1.mouseMoveEvent = self.mouseMoveLink
            self.viewer.mouseMoveEvent = self.mouseMoveLink
            self.port1.mouseReleaseEvent = self.mouseReleaseLink
            self.viewer.mouseReleaseEvent = self.mouseReleaseLink

    def zoomLink(self, event):
        self.viewer.wheel(event)
        self.port1.wheel(event)

    def mousePressLink(self, event):
        self.viewer.mousePress(event)
        self.port1.mousePress(event)

    def mouseMoveLink(self, event):
        self.viewer.mouseMove(event)
        self.port1.mouseMove(event)

    def mouseReleaseLink(self, event):
        self.viewer.mouseRelease(event)
        self.port1.mouseRelease(event)


