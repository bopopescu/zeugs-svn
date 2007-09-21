# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dlg_getPw.ui'
#
# Created: Mon Sep 17 21:21:52 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,238,204).size()).expandedTo(Dialog.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(Dialog)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.pushButton_connect = QtGui.QPushButton(Dialog)
        self.pushButton_connect.setObjectName("pushButton_connect")
        self.hboxlayout.addWidget(self.pushButton_connect)

        self.pushButton_cancel = QtGui.QPushButton(Dialog)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.hboxlayout.addWidget(self.pushButton_cancel)
        self.gridlayout.addLayout(self.hboxlayout,6,0,1,2)

        self.lineEdit_pw = QtGui.QLineEdit(Dialog)
        self.lineEdit_pw.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_pw.setObjectName("lineEdit_pw")
        self.gridlayout.addWidget(self.lineEdit_pw,5,1,1,1)

        self.label = QtGui.QLabel(Dialog)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,5,0,1,1)

        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout.addWidget(self.line,4,0,1,2)

        self.lineEdit_user = QtGui.QLineEdit(Dialog)
        self.lineEdit_user.setReadOnly(True)
        self.lineEdit_user.setObjectName("lineEdit_user")
        self.gridlayout.addWidget(self.lineEdit_user,3,1,1,1)

        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,3,0,1,1)

        self.lineEdit_name = QtGui.QLineEdit(Dialog)
        self.lineEdit_name.setReadOnly(True)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.gridlayout.addWidget(self.lineEdit_name,2,1,1,1)

        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridlayout.addWidget(self.label_5,2,0,1,1)

        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,1,0,1,1)

        self.lineEdit_host = QtGui.QLineEdit(Dialog)
        self.lineEdit_host.setReadOnly(True)
        self.lineEdit_host.setObjectName("lineEdit_host")
        self.gridlayout.addWidget(self.lineEdit_host,1,1,1,1)

        self.label_4 = QtGui.QLabel(Dialog)

        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(10)
        font.setWeight(75)
        font.setUnderline(False)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_4.setFrameShadow(QtGui.QFrame.Raised)
        self.label_4.setLineWidth(2)
        self.label_4.setScaledContents(False)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,0,0,1,2)
        self.label.setBuddy(self.lineEdit_pw)
        self.label_2.setBuddy(self.lineEdit_user)
        self.label_5.setBuddy(self.lineEdit_name)
        self.label_3.setBuddy(self.lineEdit_host)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton_connect,QtCore.SIGNAL("clicked()"),Dialog.accept)
        QtCore.QObject.connect(self.pushButton_cancel,QtCore.SIGNAL("clicked()"),Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_("Connect to Zeugs"))
        self.pushButton_connect.setText(_("C&onnect"))
        self.pushButton_cancel.setText(_("&Cancel"))
        self.label.setText(_("&Password:"))
        self.label_2.setText(_("&User:"))
        self.label_5.setText(_("Database:"))
        self.label_3.setText(_("&Host:"))
        self.label_4.setText(_("Enter Password"))

