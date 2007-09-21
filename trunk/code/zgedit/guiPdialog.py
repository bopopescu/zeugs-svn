#!/usr/bin/env python


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
"""A dialog to control printing of a set of reports from one class
and subject, for use in the editor.
"""
# pyuic4 command:
#      pyuic4 -o ui_dlg_editPrint.py dlg_editPrint.ui

# To convert the i18n stuff to gettext form, use gettextify, e.g.
#      gettextify ui_dlg_editPrint.py

from PyQt4 import QtCore, QtGui

import ui_dlg_editPrint as ui_dlg

def printDialog(npages):
    """Put up a print dbialog. If the Cancel button is pressed, return
    'None', otherwise return the PrintDialog object, so that its
    methods can be called to retrieve the data.
    """
    dialog = PrintDialog(npages)
    return dialog.run()

class PrintDialog(ui_dlg.Ui_Dialog):
    def __init__(self, npages):
        self.dlg = QtGui.QDialog()
        self.ui = ui_dlg.Ui_Dialog()
        self.ui.setupUi(self.dlg)

        # set number of pages
        self.ui.spinBox_from.setMaximum(npages)
        self.ui.spinBox_to.setMaximum(npages)
        self.ui.spinBox_to.setValue(npages)

    def run(self):
        if self.dlg.exec_():
            return self
        else:
            return None

    def toPdf(self):
        return (self.ui.checkBox_pdf.checkState() == QtCore.Qt.Checked)

    def reverse(self):
        return (self.ui.checkBox_reverse.checkState() == QtCore.Qt.Checked)

    def odd(self):
        return (self.ui.checkBox_odd.checkState() == QtCore.Qt.Checked)

    def even(self):
        return (self.ui.checkBox_even.checkState() == QtCore.Qt.Checked)

    def start(self):
        return self.ui.spinBox_from.value()

    def end(self):
        return self.ui.spinBox_to.value()
