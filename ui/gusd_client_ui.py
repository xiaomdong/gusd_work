# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gusd_client.ui',
# licensing of 'gusd_client.ui' applies.
#
# Created: Tue Oct 30 09:57:50 2018
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_clientWindow(object):
    def setupUi(self, clientWindow):
        clientWindow.setObjectName("clientWindow")
        clientWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(clientWindow)
        self.centralwidget.setObjectName("centralwidget")
        clientWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(clientWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 28))
        self.menubar.setObjectName("menubar")
        clientWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(clientWindow)
        self.statusbar.setObjectName("statusbar")
        clientWindow.setStatusBar(self.statusbar)

        self.retranslateUi(clientWindow)
        QtCore.QMetaObject.connectSlotsByName(clientWindow)

    def retranslateUi(self, clientWindow):
        clientWindow.setWindowTitle(QtWidgets.QApplication.translate("clientWindow", "MainWindow", None, -1))

