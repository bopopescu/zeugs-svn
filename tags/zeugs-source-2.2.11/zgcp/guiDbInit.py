#!/usr/bin/env python
# -*- coding: utf-8 -*-

#2007-09-01
# Copyright 2007 Michael Towers

# This file is part of Zeugs.
#
# Zeugs is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# Zeugs is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Zeugs; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
#
"""A very simple 'main window' for zgsetup.
"""
# pyuic4 command:
#      pyuic4 -o ui_zgsetup.py zgsetup.ui

# To convert the i18n stuff to gettext form, use gettextify, e.g.
#      gettextify ui_zgsetup.py

from PyQt4 import QtCore, QtGui

import ui_zgsetup as ui_dlg

class GuiDbInit(QtGui.QWidget):
    def __init__(self, text, runfunc):
        QtGui.QWidget.__init__(self)
        self.ui = ui_dlg.Ui_Form()
        self.ui.setupUi(self)
        self.ui.textEdit.append(text)
        self.runfunc = runfunc
        self.show()

    def report(self, message):
        self.ui.textEdit.append(message)
        self.activateWindow()
        QtCore.QCoreApplication.processEvents()

    @QtCore.pyqtSignature("")
    def on_pushButton_run_clicked(self):
        self.ui.pushButton_run.setEnabled(False)
        self.ui.pushButton_quit.setEnabled(False)
        self.c0 = self.cursor()
        self.setCursor(QtGui.QCursor(QtCore.Qt.BusyCursor))
        if self.runfunc and self.runfunc():
            self.ui.pushButton_run.setEnabled(True)
            self.runfunc = None
            self.setCursor(self.c0)
        else:
            self.close()
