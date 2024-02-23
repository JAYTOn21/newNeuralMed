import plotly.express as px
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
import pandas as pd
import Settings
import main

df = pd.read_excel('newData.xlsx', dtype=float).round(5)
vals = [df['imt'].tolist(), df['choles'].tolist(), df['HDL'].tolist(), df['LDL'].tolist(), df['trigl'].tolist(),
        df['ather'].tolist()]


class Ui_MainWindow(object):

    net = main.NetworkTrained(Settings.NS)
    X, Y, resX = main.reading()

    def trainTime(self, num):
        self.textEdit.setHtml(
            ("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
             "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
             "p, li { white-space: pre-wrap; }\n"
             "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
             f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Время обучения нейронной сети: {num.__round__(3)} сек. </span></p></body></html>"))

    def graphSet(self):
        df = main.result(self.net)
        fig = px.line(df, x="epoch", y="error")
        fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
        self.graphicsView.setHtml(fig.to_html(include_plotlyjs='cdn'))

    # def loadDataHand(self):
    #     df = pd.read_excel('dataneed.xlsx', dtype=float).round(5)
    #     vals = [df['imt'].tolist(), df['choles'].tolist(), df['HDL'].tolist(), df['LDL'].tolist(), df['trigl'].tolist(),
    #             df['ather'].tolist()]
    #     data = []
    #     try:
    #         data = [float(self.lineEdit.text()), float(self.lineEdit_2.text()), float(self.lineEdit_3.text()),
    #                 float(self.lineEdit_5.text()), float(self.lineEdit_6.text()), float(self.lineEdit_7.text()),
    #                 float(self.lineEdit_8.text())]
    #         for i in range(6):
    #             vals[i].append(data[i])
    #         check = True
    #     except ValueError:
    #         print("err")
    #         check = False
    #     if check:
    #         y_arr = []
    #         for i in range(6):
    #             for j in range(len(df['imt'].tolist())):
    #                 y_arr.append((vals[i][j] - min(vals[i])) / (max(vals[i]) - min(vals[i])))
    #             vals[i] = y_arr
    #             y_arr = []
    #         resX = []
    #         temp = []
    #         for i in range(len(df['imt'].tolist())):
    #             for j in range(6):
    #                 temp.append(vals[j][i])
    #             resX.append(temp)
    #             temp = []
    #         if main.runHand(data)[0] == 1:
    #             result = f"Болен {main.runHand(data)[1]}"
    #         else:
    #             result = f"Не болен {main.runHand(data)[1]}"
    #     self.textBrowser_2.setHtml(
    #         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
    #         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
    #         "p, li { white-space: pre-wrap; }\n"
    #         "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
    #         f"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">{result}</span></p></body></html>")

    def loadData(self):
        data = self.resX
        ind = 0
        try:
            ind = int(self.lineEdit_4.text())
            check = True
        except ValueError:
            check = False
        if not check or ind >= len(data):
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit_3.setText('')
            self.lineEdit_5.setText('')
            self.lineEdit_6.setText('')
            self.lineEdit_7.setText('')
            self.lineEdit_8.setText('')
            result = ""
        else:
            self.lineEdit.setText(str(vals[0][ind]))
            self.lineEdit_2.setText(str(vals[1][ind]))
            self.lineEdit_3.setText(str(vals[2][ind]))
            self.lineEdit_5.setText(str(vals[3][ind]))
            self.lineEdit_6.setText(str(vals[4][ind]))
            self.lineEdit_7.setText(str(vals[5][ind]))

            if main.run(ind, self.net, self.resX)[0] == 1:
                result = f"Болен {main.run(ind, self.net, self.resX)[1]}"
            else:
                result = f"Не болен {main.run(ind, self.net, self.resX)[1]}"

        self.textBrowser_2.setHtml(
            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
            f"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">{result}</span></p></body></html>")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1043, 454)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 271, 436))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_4.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_4.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.verticalLayout.addWidget(self.lineEdit_4)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout.addWidget(self.lineEdit_2)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_3.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.verticalLayout.addWidget(self.lineEdit_3)
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_5.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_5.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.verticalLayout.addWidget(self.lineEdit_5)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_6.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_6.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.verticalLayout.addWidget(self.lineEdit_6)
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_7.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_7.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.verticalLayout.addWidget(self.lineEdit_7)
        self.label_8 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.lineEdit_8 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_8.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_8.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.verticalLayout.addWidget(self.lineEdit_8)
        self.but = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.but.setObjectName("but")
        self.but.setText("Пуск")
        self.verticalLayout.addWidget(self.but)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(290, 10, 201, 431))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.verticalLayoutWidget_2)
        self.textBrowser.setMaximumSize(QtCore.QSize(200, 80))
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_2.addWidget(self.textBrowser)
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.verticalLayoutWidget_2)
        self.textBrowser_2.setMaximumSize(QtCore.QSize(200, 16777215))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.verticalLayout_2.addWidget(self.textBrowser_2)
        self.graphicsView = QWebEngineView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(500, 10, 531, 401))
        self.graphicsView.setObjectName("graphicsView")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(500, 410, 531, 31))
        self.textEdit.setObjectName("textEdit")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Нейронная сеть"))
        self.label.setText(_translate("MainWindow", "Введите номер"))
        self.label_2.setText(_translate("MainWindow", "УОС"))
        self.label_3.setText(_translate("MainWindow", "КВ"))
        self.label_4.setText(_translate("MainWindow", "УПСС"))
        self.label_5.setText(_translate("MainWindow", "ИЛГ"))
        self.label_6.setText(_translate("MainWindow", "ИСЛМ"))
        self.label_7.setText(_translate("MainWindow", "ИСНМ"))
        self.label_8.setText(_translate("MainWindow", "ЛИИР"))
        self.textBrowser.setHtml(_translate("MainWindow",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">Результат работы<br />нейронной сети</span></p></body></html>"))
        self.textBrowser_2.setHtml(_translate("MainWindow",
                                              "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                              "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                              "p, li { white-space: pre-wrap; }\n"
                                              "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                              "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\"></span></p></body></html>"))
        self.textEdit.setHtml(_translate("MainWindow",
                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Время обучения нейронной сети: </span></p></body></html>"))
