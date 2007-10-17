# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dlg_editPrint.ui'
#
# Created: Fri Oct 12 21:55:54 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,300,200).size()).expandedTo(Dialog.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(Dialog)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.hboxlayout.addWidget(self.label)

        self.spinBox_from = QtGui.QSpinBox(Dialog)
        self.spinBox_from.setMinimum(1)
        self.spinBox_from.setObjectName("spinBox_from")
        self.hboxlayout.addWidget(self.spinBox_from)

        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.hboxlayout.addWidget(self.label_2)

        self.spinBox_to = QtGui.QSpinBox(Dialog)
        self.spinBox_to.setMinimum(1)
        self.spinBox_to.setProperty("value",QtCore.QVariant(1))
        self.spinBox_to.setObjectName("spinBox_to")
        self.hboxlayout.addWidget(self.spinBox_to)

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.checkBox_reverse = QtGui.QCheckBox(Dialog)
        self.checkBox_reverse.setObjectName("checkBox_reverse")
        self.vboxlayout1.addWidget(self.checkBox_reverse)

        self.checkBox_pdf = QtGui.QCheckBox(Dialog)
        self.checkBox_pdf.setWindowModality(QtCore.Qt.WindowModal)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(1),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_pdf.sizePolicy().hasHeightForWidth())
        self.checkBox_pdf.setSizePolicy(sizePolicy)
        self.checkBox_pdf.setObjectName("checkBox_pdf")
        self.vboxlayout1.addWidget(self.checkBox_pdf)
        self.hboxlayout1.addLayout(self.vboxlayout1)

        self.groupBox_oddEven = QtGui.QGroupBox(Dialog)
        self.groupBox_oddEven.setObjectName("groupBox_oddEven")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.groupBox_oddEven)
        self.vboxlayout2.setMargin(9)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.checkBox_odd = QtGui.QCheckBox(self.groupBox_oddEven)
        self.checkBox_odd.setChecked(True)
        self.checkBox_odd.setObjectName("checkBox_odd")
        self.vboxlayout2.addWidget(self.checkBox_odd)

        self.checkBox_even = QtGui.QCheckBox(self.groupBox_oddEven)
        self.checkBox_even.setChecked(True)
        self.checkBox_even.setObjectName("checkBox_even")
        self.vboxlayout2.addWidget(self.checkBox_even)
        self.hboxlayout1.addWidget(self.groupBox_oddEven)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem1)

        self.pushButton_ok = QtGui.QPushButton(Dialog)
        self.pushButton_ok.setDefault(True)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.hboxlayout2.addWidget(self.pushButton_ok)

        self.pushButton_cancel = QtGui.QPushButton(Dialog)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.hboxlayout2.addWidget(self.pushButton_cancel)
        self.vboxlayout.addLayout(self.hboxlayout2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton_ok,QtCore.SIGNAL("clicked()"),Dialog.accept)
        QtCore.QObject.connect(self.pushButton_cancel,QtCore.SIGNAL("clicked()"),Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_("Print Reports"))
        self.label.setText(_("Pages from"))
        self.label_2.setText(_("to"))
        self.checkBox_reverse.setText(_("last page first"))
        self.checkBox_pdf.setText(_("print to file (pdf)"))
        self.checkBox_odd.setText(_("odd pages"))
        self.checkBox_even.setText(_("even pages"))
        self.pushButton_ok.setText(_("OK"))
        self.pushButton_cancel.setText(_("Cancel"))

