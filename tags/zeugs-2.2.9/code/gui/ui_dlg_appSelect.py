# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dlg_appSelect.ui'
#
# Created: Mon Sep 17 21:21:48 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(QtCore.QSize(QtCore.QRect(0,0,259,268).size()).expandedTo(Form.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(Form)
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.pushButton_bigger = QtGui.QPushButton(Form)
        self.pushButton_bigger.setObjectName("pushButton_bigger")
        self.hboxlayout.addWidget(self.pushButton_bigger)

        self.pushButton_smaller = QtGui.QPushButton(Form)
        self.pushButton_smaller.setObjectName("pushButton_smaller")
        self.hboxlayout.addWidget(self.pushButton_smaller)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")

        self.tab_user = QtGui.QWidget()
        self.tab_user.setObjectName("tab_user")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.tab_user)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setMargin(9)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.pushButton_edit = QtGui.QPushButton(self.tab_user)
        self.pushButton_edit.setObjectName("pushButton_edit")
        self.vboxlayout1.addWidget(self.pushButton_edit)

        self.pushButton_sync = QtGui.QPushButton(self.tab_user)
        self.pushButton_sync.setObjectName("pushButton_sync")
        self.vboxlayout1.addWidget(self.pushButton_sync)

        self.pushButton_print = QtGui.QPushButton(self.tab_user)
        self.pushButton_print.setObjectName("pushButton_print")
        self.vboxlayout1.addWidget(self.pushButton_print)
        self.tabWidget.addTab(self.tab_user,"")

        self.tab_admin = QtGui.QWidget()
        self.tab_admin.setObjectName("tab_admin")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.tab_admin)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setMargin(9)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.pushButton_cp = QtGui.QPushButton(self.tab_admin)
        self.pushButton_cp.setObjectName("pushButton_cp")
        self.vboxlayout2.addWidget(self.pushButton_cp)

        self.pushButton_configEd = QtGui.QPushButton(self.tab_admin)
        self.pushButton_configEd.setObjectName("pushButton_configEd")
        self.vboxlayout2.addWidget(self.pushButton_configEd)

        self.groupBox = QtGui.QGroupBox(self.tab_admin)
        self.groupBox.setCheckable(True)
        self.groupBox.setChecked(False)
        self.groupBox.setObjectName("groupBox")

        self.vboxlayout3 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout3.setSpacing(6)
        self.vboxlayout3.setMargin(9)
        self.vboxlayout3.setObjectName("vboxlayout3")

        self.pushButton_setup = QtGui.QPushButton(self.groupBox)
        self.pushButton_setup.setObjectName("pushButton_setup")
        self.vboxlayout3.addWidget(self.pushButton_setup)
        self.vboxlayout2.addWidget(self.groupBox)
        self.tabWidget.addTab(self.tab_admin,"")
        self.vboxlayout.addWidget(self.tabWidget)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setObjectName("hboxlayout1")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem)

        self.pushButton_quit = QtGui.QPushButton(Form)
        self.pushButton_quit.setObjectName("pushButton_quit")
        self.hboxlayout1.addWidget(self.pushButton_quit)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.pushButton_quit,QtCore.SIGNAL("clicked()"),Form.close)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_("Zeugs: select application"))
        self.pushButton_bigger.setText(_("Text bigger"))
        self.pushButton_smaller.setText(_("Text smaller"))
        self.pushButton_edit.setToolTip(_("Enter the report editor"))
        self.pushButton_edit.setText(_("Edit reports"))
        self.pushButton_sync.setToolTip(_("Synchronize a user database with the main"))
        self.pushButton_sync.setText(_("Synchronize database"))
        self.pushButton_print.setToolTip(_("Print whole reports or single pages"))
        self.pushButton_print.setText(_("Print reports"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_user), _("User"))
        self.pushButton_cp.setToolTip(_("Administrative functions for the main database"))
        self.pushButton_cp.setText(_("Control Panel"))
        self.pushButton_configEd.setText(_("Configuration/Layout editor "))
        self.groupBox.setTitle(_("Database setup"))
        self.pushButton_setup.setToolTip(_("Should be run once only, when the Zeugs system is installed"))
        self.pushButton_setup.setText(_("Initialize main database"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_admin), _("Administrator"))
        self.pushButton_quit.setText(_("Quit"))

