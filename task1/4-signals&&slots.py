from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap
from sliders import Ui_MainWindow
import sys


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.button_clicked)

    def button_clicked(self):  # single responsibility principle
        fileName, _filter = QFileDialog.getOpenFileName(self, "Title", "Default File", "Filter -- All Files (*);;Python Files (*.py)")
        if fileName:
            print(fileName)
            print(_filter)
            pixmap = QPixmap(fileName)
            pixmap = pixmap.scaled(int(pixmap.height()), int(pixmap.width()), QtCore.Qt.KeepAspectRatio)
            self.ui.label_4.setPixmap(pixmap)


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
