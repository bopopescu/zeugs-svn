# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'printPreview.ui'
#
# Created: Fri Oct 12 21:55:53 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,749,575).size()).expandedTo(Dialog.minimumSizeHint()))

        self.hboxlayout = QtGui.QHBoxLayout(Dialog)
        self.hboxlayout.setObjectName("hboxlayout")

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setObjectName("vboxlayout")

        self.groupBox_pupil = QtGui.QGroupBox(Dialog)
        self.groupBox_pupil.setObjectName("groupBox_pupil")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.groupBox_pupil)
        self.hboxlayout1.setSpacing(3)
        self.hboxlayout1.setMargin(3)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.comboBox_pupil = QtGui.QComboBox(self.groupBox_pupil)
        self.comboBox_pupil.setWindowModality(QtCore.Qt.WindowModal)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_pupil.sizePolicy().hasHeightForWidth())
        self.comboBox_pupil.setSizePolicy(sizePolicy)
        self.comboBox_pupil.setMinimumSize(QtCore.QSize(250,0))
        self.comboBox_pupil.setObjectName("comboBox_pupil")
        self.hboxlayout1.addWidget(self.comboBox_pupil)
        self.vboxlayout.addWidget(self.groupBox_pupil)

        self.groupBox_page = QtGui.QGroupBox(Dialog)
        self.groupBox_page.setObjectName("groupBox_page")

        self.hboxlayout2 = QtGui.QHBoxLayout(self.groupBox_page)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.comboBox_page = QtGui.QComboBox(self.groupBox_page)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_page.sizePolicy().hasHeightForWidth())
        self.comboBox_page.setSizePolicy(sizePolicy)
        self.comboBox_page.setMinimumSize(QtCore.QSize(150,0))
        self.comboBox_page.setObjectName("comboBox_page")
        self.hboxlayout2.addWidget(self.comboBox_page)

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.radioButton_l = QtGui.QRadioButton(self.groupBox_page)
        self.radioButton_l.setEnabled(False)
        self.radioButton_l.setObjectName("radioButton_l")
        self.vboxlayout1.addWidget(self.radioButton_l)

        self.radioButton_r = QtGui.QRadioButton(self.groupBox_page)
        self.radioButton_r.setEnabled(False)
        self.radioButton_r.setObjectName("radioButton_r")
        self.vboxlayout1.addWidget(self.radioButton_r)
        self.hboxlayout2.addLayout(self.vboxlayout1)
        self.vboxlayout.addWidget(self.groupBox_page)

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setObjectName("vboxlayout2")

        spacerItem1 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout2.addItem(spacerItem1)

        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setIcon(QtGui.QIcon("icons/quit.png"))
        self.pushButton.setObjectName("pushButton")
        self.vboxlayout2.addWidget(self.pushButton)
        self.hboxlayout3.addLayout(self.vboxlayout2)

        spacerItem2 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout3.addItem(spacerItem2)

        self.groupBox_size = QtGui.QGroupBox(Dialog)
        self.groupBox_size.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.groupBox_size.setObjectName("groupBox_size")

        self.hboxlayout4 = QtGui.QHBoxLayout(self.groupBox_size)
        self.hboxlayout4.setObjectName("hboxlayout4")

        self.sizeSlider = QtGui.QSlider(self.groupBox_size)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizeSlider.sizePolicy().hasHeightForWidth())
        self.sizeSlider.setSizePolicy(sizePolicy)
        self.sizeSlider.setMaximum(20)
        self.sizeSlider.setPageStep(1)
        self.sizeSlider.setSliderPosition(10)
        self.sizeSlider.setOrientation(QtCore.Qt.Vertical)
        self.sizeSlider.setObjectName("sizeSlider")
        self.hboxlayout4.addWidget(self.sizeSlider)
        self.hboxlayout3.addWidget(self.groupBox_size)
        self.vboxlayout.addLayout(self.hboxlayout3)
        self.hboxlayout.addLayout(self.vboxlayout)

        self.graphicsView = QtGui.QGraphicsView(Dialog)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setObjectName("graphicsView")
        self.hboxlayout.addWidget(self.graphicsView)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_("Print preview"))
        self.groupBox_pupil.setTitle(_("Pupil"))
        self.groupBox_page.setTitle(_("Page"))
        self.radioButton_l.setText(_("left"))
        self.radioButton_r.setText(_("right"))
        self.pushButton.setText(_("Done"))
        self.groupBox_size.setTitle(_("size"))

