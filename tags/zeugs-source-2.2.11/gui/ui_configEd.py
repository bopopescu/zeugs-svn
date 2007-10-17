# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configEd.ui'
#
# Created: Fri Oct 12 21:55:51 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(QtCore.QSize(QtCore.QRect(0,0,538,435).size()).expandedTo(Form.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(Form)
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.pushButton_switch = QtGui.QPushButton(Form)
        self.pushButton_switch.setObjectName("pushButton_switch")
        self.hboxlayout.addWidget(self.pushButton_switch)

        self.frame = QtGui.QFrame(Form)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.frame)
        self.hboxlayout1.setContentsMargins(-1,1,-1,1)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName("label")
        self.hboxlayout1.addWidget(self.label)
        self.hboxlayout.addWidget(self.frame)

        spacerItem = QtGui.QSpacerItem(211,26,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.pushButton_pix = QtGui.QPushButton(Form)
        self.pushButton_pix.setObjectName("pushButton_pix")
        self.hboxlayout.addWidget(self.pushButton_pix)

        self.pushButton_pupils = QtGui.QPushButton(Form)
        self.pushButton_pupils.setObjectName("pushButton_pupils")
        self.hboxlayout.addWidget(self.pushButton_pupils)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.splitter_2 = QtGui.QSplitter(Form)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setChildrenCollapsible(False)
        self.splitter_2.setObjectName("splitter_2")

        self.splitter = QtGui.QSplitter(self.splitter_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")

        self.treeWidget = QtGui.QTreeWidget(self.splitter)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setIndentation(30)
        self.treeWidget.setUniformRowHeights(True)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0,"")

        self.tableWidget = QtGui.QTreeWidget(self.splitter)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.CurrentChanged)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setUniformRowHeights(True)
        self.tableWidget.setObjectName("tableWidget")

        self.textEdit = QtGui.QTextEdit(self.splitter_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setUndoRedoEnabled(True)
        self.textEdit.setReadOnly(False)
        self.textEdit.setObjectName("textEdit")
        self.vboxlayout.addWidget(self.splitter_2)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.pushButton_clone = QtGui.QPushButton(Form)
        self.pushButton_clone.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.pushButton_clone.setObjectName("pushButton_clone")
        self.hboxlayout2.addWidget(self.pushButton_clone)

        self.pushButton_delete = QtGui.QPushButton(Form)
        self.pushButton_delete.setObjectName("pushButton_delete")
        self.hboxlayout2.addWidget(self.pushButton_delete)

        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem1)

        self.pushButton_save = QtGui.QPushButton(Form)
        self.pushButton_save.setObjectName("pushButton_save")
        self.hboxlayout2.addWidget(self.pushButton_save)

        self.pushButton_quit = QtGui.QPushButton(Form)
        self.pushButton_quit.setObjectName("pushButton_quit")
        self.hboxlayout2.addWidget(self.pushButton_quit)
        self.vboxlayout.addLayout(self.hboxlayout2)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.pushButton_quit,QtCore.SIGNAL("clicked()"),Form.close)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_("Configuration/Layout Editor"))
        self.pushButton_switch.setToolTip(_("Switch to a different configuration file"))
        self.pushButton_switch.setText(_("Open"))
        self.pushButton_pix.setText(_("Replace images"))
        self.pushButton_pupils.setText(_("Import pupils"))
        self.tableWidget.headerItem().setText(0,_("Field Name                 "))
        self.tableWidget.headerItem().setText(1,_("Value"))
        self.pushButton_clone.setToolTip(_("Make a copy of the current node"))
        self.pushButton_clone.setText(_("Clone"))
        self.pushButton_delete.setToolTip(_("Remove the current node"))
        self.pushButton_delete.setText(_("Delete"))
        self.pushButton_save.setToolTip(_("Save to temporary file"))
        self.pushButton_save.setText(_("Save"))
        self.pushButton_quit.setToolTip(_("Save the changes and exit the program"))
        self.pushButton_quit.setText(_("Quit"))

