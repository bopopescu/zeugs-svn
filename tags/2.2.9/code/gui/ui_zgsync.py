# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zgsync.ui'
#
# Created: Mon Sep 17 21:21:47 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.WindowModal)
        Form.resize(QtCore.QSize(QtCore.QRect(0,0,540,213).size()).expandedTo(Form.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(Form)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName("hboxlayout")

        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.hboxlayout.addWidget(self.label_3)

        self.lineEdit_dbs = QtGui.QLineEdit(Form)
        self.lineEdit_dbs.setReadOnly(True)
        self.lineEdit_dbs.setObjectName("lineEdit_dbs")
        self.hboxlayout.addWidget(self.lineEdit_dbs)

        self.pushButton_browse = QtGui.QPushButton(Form)
        self.pushButton_browse.setObjectName("pushButton_browse")
        self.hboxlayout.addWidget(self.pushButton_browse)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.line = QtGui.QFrame(Form)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.vboxlayout.addWidget(self.line)

        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")

        self.gridlayout = QtGui.QGridLayout(self.groupBox)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.frame_2 = QtGui.QFrame(self.groupBox)
        self.frame_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridlayout.addWidget(self.frame_2,1,2,1,1)

        self.lineEdit_user = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_user.setReadOnly(True)
        self.lineEdit_user.setObjectName("lineEdit_user")
        self.gridlayout.addWidget(self.lineEdit_user,1,1,1,1)

        self.label = QtGui.QLabel(self.groupBox)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.lineEdit_host = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_host.setObjectName("lineEdit_host")
        self.gridlayout.addWidget(self.lineEdit_host,0,1,1,1)

        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,1,0,1,1)

        self.lineEdit_name = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_name.setReadOnly(True)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.gridlayout.addWidget(self.lineEdit_name,0,4,1,1)

        self.pushButton_pw = QtGui.QPushButton(self.groupBox)
        self.pushButton_pw.setObjectName("pushButton_pw")
        self.gridlayout.addWidget(self.pushButton_pw,1,4,1,1)

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,0,3,1,1)

        self.frame = QtGui.QFrame(self.groupBox)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridlayout.addWidget(self.frame,0,2,1,1)
        self.vboxlayout.addWidget(self.groupBox)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setObjectName("hboxlayout1")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem)

        self.pushButton_sync = QtGui.QPushButton(Form)
        self.pushButton_sync.setObjectName("pushButton_sync")
        self.hboxlayout1.addWidget(self.pushButton_sync)

        self.pushButton_quit = QtGui.QPushButton(Form)
        self.pushButton_quit.setObjectName("pushButton_quit")
        self.hboxlayout1.addWidget(self.pushButton_quit)
        self.vboxlayout.addLayout(self.hboxlayout1)
        self.label_3.setBuddy(self.lineEdit_dbs)
        self.label.setBuddy(self.lineEdit_host)
        self.label_4.setBuddy(self.lineEdit_user)
        self.label_2.setBuddy(self.lineEdit_name)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.pushButton_quit,QtCore.SIGNAL("clicked()"),Form.close)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_("Form"))
        self.label_3.setText(_("User Database:"))
        self.pushButton_browse.setText(_("Change file"))
        self.groupBox.setTitle(_("Master Database"))
        self.label.setText(_("Host:"))
        self.label_4.setText(_("User:"))
        self.pushButton_pw.setText(_("Change Password"))
        self.label_2.setText(_("Name:"))
        self.pushButton_sync.setText(_("Synchronize"))
        self.pushButton_quit.setText(_("Quit"))

