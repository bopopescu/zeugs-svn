# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zgprint.ui'
#
# Created: Fri Oct 12 21:55:51 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(QtCore.QSize(QtCore.QRect(0,0,549,433).size()).expandedTo(Form.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(Form)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName("hboxlayout")

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.widget = QtGui.QWidget(Form)
        self.widget.setObjectName("widget")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.widget)
        self.vboxlayout2.setSpacing(3)
        self.vboxlayout2.setMargin(3)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.pushButton_open = QtGui.QPushButton(self.widget)
        self.pushButton_open.setObjectName("pushButton_open")
        self.vboxlayout2.addWidget(self.pushButton_open)

        self.groupBox = QtGui.QGroupBox(self.widget)
        self.groupBox.setObjectName("groupBox")

        self.vboxlayout3 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout3.setSpacing(3)
        self.vboxlayout3.setMargin(3)
        self.vboxlayout3.setObjectName("vboxlayout3")

        self.comboBox_class = QtGui.QComboBox(self.groupBox)
        self.comboBox_class.setObjectName("comboBox_class")
        self.vboxlayout3.addWidget(self.comboBox_class)
        self.vboxlayout2.addWidget(self.groupBox)

        self.pushButton_selectAllPupils = QtGui.QPushButton(self.widget)
        self.pushButton_selectAllPupils.setObjectName("pushButton_selectAllPupils")
        self.vboxlayout2.addWidget(self.pushButton_selectAllPupils)

        self.pushButton_unselectAllPupils = QtGui.QPushButton(self.widget)
        self.pushButton_unselectAllPupils.setObjectName("pushButton_unselectAllPupils")
        self.vboxlayout2.addWidget(self.pushButton_unselectAllPupils)

        spacerItem = QtGui.QSpacerItem(20,71,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout2.addItem(spacerItem)
        self.vboxlayout1.addWidget(self.widget)

        self.checkBox_shrink = QtGui.QCheckBox(Form)
        self.checkBox_shrink.setAcceptDrops(True)
        self.checkBox_shrink.setObjectName("checkBox_shrink")
        self.vboxlayout1.addWidget(self.checkBox_shrink)

        self.checkBox_landscape = QtGui.QCheckBox(Form)
        self.checkBox_landscape.setObjectName("checkBox_landscape")
        self.vboxlayout1.addWidget(self.checkBox_landscape)

        self.checkBox_reverse = QtGui.QCheckBox(Form)
        self.checkBox_reverse.setObjectName("checkBox_reverse")
        self.vboxlayout1.addWidget(self.checkBox_reverse)

        self.checkBox_pdf = QtGui.QCheckBox(Form)
        self.checkBox_pdf.setChecked(True)
        self.checkBox_pdf.setObjectName("checkBox_pdf")
        self.vboxlayout1.addWidget(self.checkBox_pdf)
        self.hboxlayout.addLayout(self.vboxlayout1)

        self.groupBox_2 = QtGui.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")

        self.vboxlayout4 = QtGui.QVBoxLayout(self.groupBox_2)
        self.vboxlayout4.setSpacing(3)
        self.vboxlayout4.setMargin(3)
        self.vboxlayout4.setObjectName("vboxlayout4")

        self.listWidget_pupils = QtGui.QListWidget(self.groupBox_2)
        self.listWidget_pupils.setMinimumSize(QtCore.QSize(200,0))
        self.listWidget_pupils.setObjectName("listWidget_pupils")
        self.vboxlayout4.addWidget(self.listWidget_pupils)
        self.hboxlayout.addWidget(self.groupBox_2)

        self.groupBox_3 = QtGui.QGroupBox(Form)
        self.groupBox_3.setObjectName("groupBox_3")

        self.vboxlayout5 = QtGui.QVBoxLayout(self.groupBox_3)
        self.vboxlayout5.setSpacing(3)
        self.vboxlayout5.setMargin(3)
        self.vboxlayout5.setObjectName("vboxlayout5")

        self.radioButton_pagesM = QtGui.QRadioButton(self.groupBox_3)
        self.radioButton_pagesM.setObjectName("radioButton_pagesM")
        self.vboxlayout5.addWidget(self.radioButton_pagesM)

        self.radioButton_pagesS = QtGui.QRadioButton(self.groupBox_3)
        self.radioButton_pagesS.setObjectName("radioButton_pagesS")
        self.vboxlayout5.addWidget(self.radioButton_pagesS)

        self.radioButton_pagesI = QtGui.QRadioButton(self.groupBox_3)
        self.radioButton_pagesI.setCheckable(True)
        self.radioButton_pagesI.setChecked(False)
        self.radioButton_pagesI.setObjectName("radioButton_pagesI")
        self.vboxlayout5.addWidget(self.radioButton_pagesI)

        self.listWidget_pages = QtGui.QListWidget(self.groupBox_3)
        self.listWidget_pages.setObjectName("listWidget_pages")
        self.vboxlayout5.addWidget(self.listWidget_pages)

        self.pushButton_allPages = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_allPages.setObjectName("pushButton_allPages")
        self.vboxlayout5.addWidget(self.pushButton_allPages)
        self.hboxlayout.addWidget(self.groupBox_3)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.groupBox_4 = QtGui.QGroupBox(Form)
        self.groupBox_4.setAlignment(QtCore.Qt.AlignRight)
        self.groupBox_4.setObjectName("groupBox_4")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.groupBox_4)
        self.hboxlayout1.setSpacing(3)
        self.hboxlayout1.setMargin(3)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.textEdit = QtGui.QTextEdit(self.groupBox_4)
        self.textEdit.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.textEdit.setObjectName("textEdit")
        self.hboxlayout1.addWidget(self.textEdit)
        self.vboxlayout.addWidget(self.groupBox_4)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.pushButton_preview = QtGui.QPushButton(Form)
        self.pushButton_preview.setObjectName("pushButton_preview")
        self.hboxlayout2.addWidget(self.pushButton_preview)

        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem1)

        self.pushButton_print = QtGui.QPushButton(Form)
        self.pushButton_print.setObjectName("pushButton_print")
        self.hboxlayout2.addWidget(self.pushButton_print)

        self.pushButton_cancel = QtGui.QPushButton(Form)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.hboxlayout2.addWidget(self.pushButton_cancel)
        self.vboxlayout.addLayout(self.hboxlayout2)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.pushButton_cancel,QtCore.SIGNAL("clicked()"),Form.close)
        QtCore.QObject.connect(self.radioButton_pagesM,QtCore.SIGNAL("toggled(bool)"),self.checkBox_shrink.setEnabled)
        QtCore.QObject.connect(self.radioButton_pagesM,QtCore.SIGNAL("toggled(bool)"),self.checkBox_landscape.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_("Form"))
        self.pushButton_open.setText(_("Open report file"))
        self.groupBox.setTitle(_("Class"))
        self.pushButton_selectAllPupils.setText(_("Select all pupils"))
        self.pushButton_unselectAllPupils.setText(_("Unselect all pupils"))
        self.checkBox_shrink.setText(_("Shrink to A4"))
        self.checkBox_landscape.setText(_("Landscape orientation"))
        self.checkBox_reverse.setText(_("Last page first"))
        self.checkBox_pdf.setText(_("Print to file (pdf)"))
        self.groupBox_2.setTitle(_("Pupils"))
        self.groupBox_3.setTitle(_("Sheet selection"))
        self.radioButton_pagesM.setText(_("A3 sheets"))
        self.radioButton_pagesS.setText(_("A4 sheets"))
        self.radioButton_pagesI.setText(_("Individual pages"))
        self.pushButton_allPages.setText(_("Select all"))
        self.groupBox_4.setTitle(_("Messages"))
        self.pushButton_preview.setText(_("Preview"))
        self.pushButton_print.setText(_("Print"))
        self.pushButton_cancel.setText(_("Cancel"))

