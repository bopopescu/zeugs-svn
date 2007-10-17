# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zgcp.ui'
#
# Created: Fri Oct 12 21:55:52 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(QtCore.QSize(QtCore.QRect(0,0,419,343).size()).expandedTo(Form.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(Form)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.label = QtGui.QLabel(Form)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.vboxlayout1.addWidget(self.label)

        self.comboBox_db = QtGui.QComboBox(Form)
        self.comboBox_db.setMinimumSize(QtCore.QSize(150,0))
        self.comboBox_db.setObjectName("comboBox_db")
        self.vboxlayout1.addWidget(self.comboBox_db)

        spacerItem = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout1.addItem(spacerItem)
        self.hboxlayout.addLayout(self.vboxlayout1)

        self.line = QtGui.QFrame(Form)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.hboxlayout.addWidget(self.line)

        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setMargin(0)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.hboxlayout1.addWidget(self.label_2)

        self.lineEdit_host = QtGui.QLineEdit(Form)
        self.lineEdit_host.setMinimumSize(QtCore.QSize(120,0))
        self.lineEdit_host.setMouseTracking(False)
        self.lineEdit_host.setFocusPolicy(QtCore.Qt.NoFocus)
        self.lineEdit_host.setAcceptDrops(False)
        self.lineEdit_host.setObjectName("lineEdit_host")
        self.hboxlayout1.addWidget(self.lineEdit_host)
        self.vboxlayout2.addLayout(self.hboxlayout1)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.label_finalized = QtGui.QLabel(Form)
        self.label_finalized.setMinimumSize(QtCore.QSize(100,0))
        self.label_finalized.setObjectName("label_finalized")
        self.hboxlayout2.addWidget(self.label_finalized)

        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem1)

        self.pushButton_Quit = QtGui.QPushButton(Form)
        self.pushButton_Quit.setIcon(QtGui.QIcon("icons/quit.png"))
        self.pushButton_Quit.setIconSize(QtCore.QSize(24,24))
        self.pushButton_Quit.setObjectName("pushButton_Quit")
        self.hboxlayout2.addWidget(self.pushButton_Quit)
        self.vboxlayout2.addLayout(self.hboxlayout2)
        self.hboxlayout.addLayout(self.vboxlayout2)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.line_5 = QtGui.QFrame(Form)
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.vboxlayout.addWidget(self.line_5)

        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")

        self.tab_db = QtGui.QWidget()
        self.tab_db.setObjectName("tab_db")

        self.hboxlayout3 = QtGui.QHBoxLayout(self.tab_db)
        self.hboxlayout3.setMargin(9)
        self.hboxlayout3.setSpacing(6)
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.pushButton_updatedb = QtGui.QPushButton(self.tab_db)
        self.pushButton_updatedb.setObjectName("pushButton_updatedb")
        self.gridlayout.addWidget(self.pushButton_updatedb,0,0,1,1)

        self.pushButton_finalize = QtGui.QPushButton(self.tab_db)
        self.pushButton_finalize.setCheckable(True)
        self.pushButton_finalize.setObjectName("pushButton_finalize")
        self.gridlayout.addWidget(self.pushButton_finalize,1,1,1,1)

        self.pushButton_dump = QtGui.QPushButton(self.tab_db)
        self.pushButton_dump.setObjectName("pushButton_dump")
        self.gridlayout.addWidget(self.pushButton_dump,0,1,1,1)

        self.pushButton_print = QtGui.QPushButton(self.tab_db)
        self.pushButton_print.setObjectName("pushButton_print")
        self.gridlayout.addWidget(self.pushButton_print,1,0,1,1)

        self.pushButton_newdb = QtGui.QPushButton(self.tab_db)
        self.pushButton_newdb.setObjectName("pushButton_newdb")
        self.gridlayout.addWidget(self.pushButton_newdb,2,0,1,1)

        self.pushButton_sync = QtGui.QPushButton(self.tab_db)
        self.pushButton_sync.setObjectName("pushButton_sync")
        self.gridlayout.addWidget(self.pushButton_sync,2,1,1,1)
        self.hboxlayout3.addLayout(self.gridlayout)

        self.line_2 = QtGui.QFrame(self.tab_db)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.hboxlayout3.addWidget(self.line_2)

        self.groupBox_3 = QtGui.QGroupBox(self.tab_db)
        self.groupBox_3.setCheckable(True)
        self.groupBox_3.setChecked(False)
        self.groupBox_3.setObjectName("groupBox_3")

        self.vboxlayout3 = QtGui.QVBoxLayout(self.groupBox_3)
        self.vboxlayout3.setMargin(9)
        self.vboxlayout3.setSpacing(6)
        self.vboxlayout3.setObjectName("vboxlayout3")

        self.pushButton_restore = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_restore.setObjectName("pushButton_restore")
        self.vboxlayout3.addWidget(self.pushButton_restore)

        self.pushButton_dumpd = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_dumpd.setObjectName("pushButton_dumpd")
        self.vboxlayout3.addWidget(self.pushButton_dumpd)

        self.pushButton_dbdel = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_dbdel.setObjectName("pushButton_dbdel")
        self.vboxlayout3.addWidget(self.pushButton_dbdel)
        self.hboxlayout3.addWidget(self.groupBox_3)
        self.tabWidget.addTab(self.tab_db,"")

        self.tab_teachers = QtGui.QWidget()
        self.tab_teachers.setObjectName("tab_teachers")

        self.hboxlayout4 = QtGui.QHBoxLayout(self.tab_teachers)
        self.hboxlayout4.setMargin(9)
        self.hboxlayout4.setSpacing(6)
        self.hboxlayout4.setObjectName("hboxlayout4")

        self.listWidget_users = QtGui.QListWidget(self.tab_teachers)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget_users.sizePolicy().hasHeightForWidth())
        self.listWidget_users.setSizePolicy(sizePolicy)
        self.listWidget_users.setMinimumSize(QtCore.QSize(150,0))
        self.listWidget_users.setObjectName("listWidget_users")
        self.hboxlayout4.addWidget(self.listWidget_users)

        self.vboxlayout4 = QtGui.QVBoxLayout()
        self.vboxlayout4.setMargin(0)
        self.vboxlayout4.setSpacing(6)
        self.vboxlayout4.setObjectName("vboxlayout4")

        self.hboxlayout5 = QtGui.QHBoxLayout()
        self.hboxlayout5.setMargin(0)
        self.hboxlayout5.setSpacing(6)
        self.hboxlayout5.setObjectName("hboxlayout5")

        spacerItem2 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.hboxlayout5.addItem(spacerItem2)

        self.vboxlayout5 = QtGui.QVBoxLayout()
        self.vboxlayout5.setMargin(0)
        self.vboxlayout5.setSpacing(6)
        self.vboxlayout5.setObjectName("vboxlayout5")

        self.pushButton_gen = QtGui.QPushButton(self.tab_teachers)
        self.pushButton_gen.setObjectName("pushButton_gen")
        self.vboxlayout5.addWidget(self.pushButton_gen)

        self.pushButton_pwd = QtGui.QPushButton(self.tab_teachers)
        self.pushButton_pwd.setObjectName("pushButton_pwd")
        self.vboxlayout5.addWidget(self.pushButton_pwd)
        self.hboxlayout5.addLayout(self.vboxlayout5)
        self.vboxlayout4.addLayout(self.hboxlayout5)

        spacerItem3 = QtGui.QSpacerItem(20,0,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout4.addItem(spacerItem3)

        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setMargin(0)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.pushButton_usel = QtGui.QPushButton(self.tab_teachers)
        self.pushButton_usel.setObjectName("pushButton_usel")
        self.gridlayout1.addWidget(self.pushButton_usel,0,0,1,1)

        self.pushButton_uinvsel = QtGui.QPushButton(self.tab_teachers)
        self.pushButton_uinvsel.setObjectName("pushButton_uinvsel")
        self.gridlayout1.addWidget(self.pushButton_uinvsel,1,1,1,1)

        self.pushButton_uunsel = QtGui.QPushButton(self.tab_teachers)
        self.pushButton_uunsel.setObjectName("pushButton_uunsel")
        self.gridlayout1.addWidget(self.pushButton_uunsel,1,0,1,1)

        spacerItem4 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem4,0,1,1,1)
        self.vboxlayout4.addLayout(self.gridlayout1)
        self.hboxlayout4.addLayout(self.vboxlayout4)
        self.tabWidget.addTab(self.tab_teachers,"")
        self.vboxlayout.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.pushButton_Quit,QtCore.SIGNAL("clicked()"),Form.close)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_("Zeugs Control Panel"))
        self.label.setText(_("Current Database"))
        self.label_2.setText(_("Host"))
        self.label_finalized.setText(_("Active"))
        self.pushButton_Quit.setText(_("Quit"))
        self.pushButton_updatedb.setText(_("Update"))
        self.pushButton_finalize.setText(_("Finalized"))
        self.pushButton_dump.setText(_("Backup"))
        self.pushButton_print.setText(_("Print"))
        self.pushButton_newdb.setText(_("New"))
        self.pushButton_sync.setToolTip(_("Synchronize with user file"))
        self.pushButton_sync.setText(_("Synchronize"))
        self.groupBox_3.setTitle(_("Extra"))
        self.pushButton_restore.setText(_("Restore from backup"))
        self.pushButton_dumpd.setText(_("Dump config files"))
        self.pushButton_dbdel.setText(_("Delete"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_db), _("database"))
        self.pushButton_gen.setText(_("Generate user databases"))
        self.pushButton_pwd.setText(_("Reset password"))
        self.pushButton_usel.setText(_("Select all"))
        self.pushButton_uinvsel.setText(_("Invert selection"))
        self.pushButton_uunsel.setText(_("Unselect all"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_teachers), _("teachers"))

