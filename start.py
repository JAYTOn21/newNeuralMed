import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from ui import Ui_MainWindow
import main


# try:
#     from PyQt5.QtWinExtras import QtWin
#     myappid = 'mycompany.myproduct.subproduct.version'
#     QtWin.setCurrentProcessExplicitAppUserModelID(myappid)
# except ImportError:
#     pass


class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)
        self.ui.lineEdit_4.textChanged.connect(self.ui.loadData)
        # self.ui.but.clicked.connect(self.ui.loadDataHand)

    def graphSet(self):
        self.ui.graphSet()

    def show(self):
        self.main_win.show()

    def train(self):
        self.ui.trainTime(main.train())



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # app.setWindowIcon(QtGui.QIcon('MR.png'))
    main_win = MainWindow()
    main_win.train()
    # main_win.show()
    main_win.graphSet()
    main_win.ui.loadData()
    main.testRun()
    sys.exit()

