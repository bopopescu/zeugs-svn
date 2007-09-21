# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dlg_pw.ui'
#
# Created: Mon Sep 17 21:21:47 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,176,150).size()).expandedTo(Dialog.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(Dialog)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.lineEdit_1 = QtGui.QLineEdit(Dialog)
        self.lineEdit_1.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.vboxlayout.addWidget(self.lineEdit_1)

        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.vboxlayout.addWidget(self.label_2)

        self.lineEdit_2 = QtGui.QLineEdit(Dialog)
        self.lineEdit_2.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.vboxlayout.addWidget(self.lineEdit_2)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.pushButton_accept = QtGui.QPushButton(Dialog)
        self.pushButton_accept.setDefault(True)
        self.pushButton_accept.setObjectName("pushButton_accept")
        self.hboxlayout.addWidget(self.pushButton_accept)

        self.pushButton_cancel = QtGui.QPushButton(Dialog)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.hboxlayout.addWidget(self.pushButton_cancel)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_("New Password"))
        self.label.setText(_("Enter password:"))
        self.label_2.setText(_("Repeat password:"))
        self.pushButton_accept.setText(_("Accept"))
        self.pushButton_cancel.setText(_("Cancel"))

