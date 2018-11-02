# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login_dialog.ui',
# licensing of 'login_dialog.ui' applies.
#
# Created: Tue Oct 30 10:01:43 2018
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_login_Dialog(object):
    def setupUi(self, login_Dialog):
        login_Dialog.setObjectName("login_Dialog")
        login_Dialog.resize(259, 109)
        login_Dialog.setMaximumSize(QtCore.QSize(334, 143))
        self.verticalLayout = QtWidgets.QVBoxLayout(login_Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(login_Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.user = QtWidgets.QLineEdit(login_Dialog)
        self.user.setObjectName("user")
        self.horizontalLayout.addWidget(self.user)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(login_Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.password = QtWidgets.QLineEdit(login_Dialog)
        self.password.setObjectName("password")
        self.horizontalLayout_2.addWidget(self.password)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(login_Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(login_Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), login_Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), login_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(login_Dialog)

    def retranslateUi(self, login_Dialog):
        login_Dialog.setWindowTitle(QtWidgets.QApplication.translate("login_Dialog", "GUSD SYSTEM", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("login_Dialog", "usr              ", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("login_Dialog", "password ", None, -1))

