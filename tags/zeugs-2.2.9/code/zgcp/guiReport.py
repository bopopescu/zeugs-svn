#!/usr/bin/env python
# -*- coding: utf-8 -*-

#2007-06-25
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
"""Interface to the pyuic4 generated 'form', ui_report.py
pyuic4 command:
      pyuic4 -o ui_report.py report.ui

To convert the i18n stuff to gettext form, use gettextify, e.g.
      gettextify ui_report.py
"""

from PyQt4 import QtCore, QtGui

import ui_report as ui_form

class GuiReport(QtGui.QDialog):
    """A simple dialogue allowing reporting during a function run.
    The function to run is the 'run' method of the object 'obj'.
    An introductory text is displayed before starting.
    """
    def __init__(self, title, obj, text):
        QtGui.QDialog.__init__(self)
        self.ui = ui_form.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        self.show()
        self.more(obj, text)

    def more(self, obj, text):
        self.obj = obj
        self.report(text)
        self.obj.run(self)
        self.ui.pushButton.setEnabled(True)

    def report(self, message):
        self.ui.textEdit.append(message)
        QtCore.QCoreApplication.processEvents()


    def accept(self):
        QtGui.QDialog.accept(self)


def guiReport(title, obj, text):
    """obj is an object with a 'run' method, text is the text to show
    before it is 'run'.
    """
    dlg = GuiReport(title, obj, text)
    dlg.exec_()
