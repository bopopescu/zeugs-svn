# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'checkSpell.ui'
#
# Created: Mon Sep 17 21:21:49 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.ApplicationModal)
        Form.resize(QtCore.QSize(QtCore.QRect(0,0,391,288).size()).expandedTo(Form.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(Form)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")

        self.hboxlayout = QtGui.QHBoxLayout(self.groupBox)
        self.hboxlayout.setMargin(9)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.textEdit = QtGui.QTextEdit(self.groupBox)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.hboxlayout.addWidget(self.textEdit)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.pushButton_ignore = QtGui.QPushButton(self.groupBox)
        self.pushButton_ignore.setObjectName("pushButton_ignore")
        self.vboxlayout1.addWidget(self.pushButton_ignore)

        self.pushButton_ignoreAll = QtGui.QPushButton(self.groupBox)
        self.pushButton_ignoreAll.setObjectName("pushButton_ignoreAll")
        self.vboxlayout1.addWidget(self.pushButton_ignoreAll)

        self.pushButton_add = QtGui.QPushButton(self.groupBox)
        self.pushButton_add.setObjectName("pushButton_add")
        self.vboxlayout1.addWidget(self.pushButton_add)
        self.hboxlayout.addLayout(self.vboxlayout1)
        self.vboxlayout.addWidget(self.groupBox)

        self.groupBox_2 = QtGui.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.groupBox_2)
        self.hboxlayout1.setMargin(9)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setMargin(0)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.comboBox = QtGui.QComboBox(self.groupBox_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(3),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setMinimumSize(QtCore.QSize(250,0))
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName("comboBox")
        self.vboxlayout2.addWidget(self.comboBox)

        spacerItem = QtGui.QSpacerItem(20,21,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout2.addItem(spacerItem)
        self.hboxlayout1.addLayout(self.vboxlayout2)

        self.vboxlayout3 = QtGui.QVBoxLayout()
        self.vboxlayout3.setMargin(0)
        self.vboxlayout3.setSpacing(6)
        self.vboxlayout3.setObjectName("vboxlayout3")

        self.pushButton_change = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_change.setObjectName("pushButton_change")
        self.vboxlayout3.addWidget(self.pushButton_change)

        self.pushButton_changeAll = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_changeAll.setObjectName("pushButton_changeAll")
        self.vboxlayout3.addWidget(self.pushButton_changeAll)
        self.hboxlayout1.addLayout(self.vboxlayout3)
        self.vboxlayout.addWidget(self.groupBox_2)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem1)

        self.pushButton_close = QtGui.QPushButton(Form)
        self.pushButton_close.setObjectName("pushButton_close")
        self.hboxlayout2.addWidget(self.pushButton_close)
        self.vboxlayout.addLayout(self.hboxlayout2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_("Check Spelling"))
        self.groupBox.setTitle(_("Not in dictionary"))
        self.pushButton_ignore.setText(_("&Ignore"))
        self.pushButton_ignoreAll.setText(_("Ignore &All"))
        self.pushButton_add.setText(_("A&dd"))
        self.groupBox_2.setTitle(_("Suggestions"))
        self.pushButton_change.setText(_("&Change"))
        self.pushButton_changeAll.setText(_("Change A&ll"))
        self.pushButton_close.setText(_("Clo&se"))

