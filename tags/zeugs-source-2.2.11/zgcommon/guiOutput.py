#!/usr/bin/env python
# -*- coding: utf-8 -*-

#2007-08-29
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
"""A simple dialog to show messages while processing, non-modal.
"""
# pyuic4 command:
#      pyuic4 -o ui_output.py output.ui

# To convert the i18n stuff to gettext form, use gettextify, e.g.
#      gettextify ui_output.py

from PyQt4 import QtCore, QtGui

import ui_output as ui_dlg

class Output(QtGui.QWidget):
    def __init__(self, title=None):
        QtGui.QWidget.__init__(self)
        self.ui = ui_dlg.Ui_Form()
        self.ui.setupUi(self)
        if title:
            self.setWindowTitle(title)
        self.show()

    def report(self, message):
        self.ui.textEdit.append(message)
        QtCore.QCoreApplication.processEvents()

    def done(self):
        self.ui.pushButton.setEnabled(True)
