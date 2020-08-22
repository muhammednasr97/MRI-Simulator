from PyQt5 import QtWidgets, QtCore


class Window(QtWidgets.QMainWindow):
    signal_start_background_job = QtCore.pyqtSignal()

    def __init__(self):
        super(Window, self).__init__()
        self.button = QtWidgets.QPushButton(self)

        self.worker = WorkerObject()
        self.thread = QtCore.QThread()
        self.worker.moveToThread(self.thread)

        self.signal_start_background_job.connect(self.worker.background_job)

        self.button.clicked.connect(self.start_background_job)

    def start_background_job(self):
        # No harm in calling thread.start() after the thread is already started.
        self.thread.start()
        self.signal_start_background_job.emit()


class WorkerObject(QtCore.QObject):
    @QtCore.pyqtSlot()
    def background_job(self):
        # Do stuff
        pass