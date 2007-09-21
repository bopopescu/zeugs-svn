# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zgsetup.ui'
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
        Form.resize(QtCore.QSize(QtCore.QRect(0,0,540,249).size()).expandedTo(Form.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(Form)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setObjectName("vboxlayout")

        self.textEdit = QtGui.QTextEdit(Form)
        self.textEdit.setReadOnly(True)
        self.textEdit.setAcceptRichText(False)
        self.textEdit.setObjectName("textEdit")
        self.vboxlayout.addWidget(self.textEdit)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.pushButton_quit = QtGui.QPushButton(Form)
        self.pushButton_quit.setObjectName("pushButton_quit")
        self.hboxlayout.addWidget(self.pushButton_quit)

        self.pushButton_run = QtGui.QPushButton(Form)
        self.pushButton_run.setObjectName("pushButton_run")
        self.hboxlayout.addWidget(self.pushButton_run)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.pushButton_quit,QtCore.SIGNAL("clicked()"),Form.close)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_("zgsetup - initialize database"))
        self.textEdit.setHtml(QtGui.QApplication.translate("Form", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_quit.setText(_("Cancel"))
        self.pushButton_run.setText(_("OK"))

