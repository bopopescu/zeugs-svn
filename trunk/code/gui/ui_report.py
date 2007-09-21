# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'report.ui'
#
# Created: Mon Sep 17 21:21:48 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,400,300).size()).expandedTo(Dialog.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(Dialog)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setObjectName("vboxlayout")

        self.textEdit = QtGui.QTextEdit(Dialog)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.vboxlayout.addWidget(self.textEdit)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setEnabled(False)
        self.pushButton.setObjectName("pushButton")
        self.hboxlayout.addWidget(self.pushButton)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        self.pushButton.setText(_("OK"))

