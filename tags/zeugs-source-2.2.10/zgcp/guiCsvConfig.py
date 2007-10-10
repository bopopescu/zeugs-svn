#!/usr/bin/env python
# -*- coding: utf-8 -*-

#2007-09-08
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
"""Interface to the pyuic4 generated 'form', ui_dlg_csv.py
pyuic4 command:
      pyuic4 -o ui_dlg_csv.py dlg_csv.ui

To convert the i18n stuff to gettext form, use gettextify, e.g.
      gettextify ui_dlg_csv.py
"""

from PyQt4 import QtCore, QtGui

import ui_dlg_csv as ui_form


class GuiCsvConfig(QtGui.QDialog):
    """A dialogue to set the configuration for the csv-file converter
    for pupil files.
    """
    def __init__(self, colspec, csvData):
        """colspec is a list of fields, csvData is a CsvData
        object, which should contain the results on returning.
        """
        QtGui.QDialog.__init__(self)
        self.fields = colspec
        self.csvData = csvData
        self.ui = ui_form.Ui_Dialog()
        self.ui.setupUi(self)

        sepix = self.ui.comboBox.findText(self.csvData.separator)
        if (sepix >= 0):
            self.ui.comboBox.setCurrentIndex(sepix)

        text = _("Enter the column numbers for the data in your"
                " csv files. If a field is not present in the csv"
                " file, set the column to 0.")
        self.ui.textEdit.setPlainText(text)

        gridLayout = QtGui.QGridLayout(self.ui.frame)
        row = 0
        self.ledits = []
        for col in self.fields:
            l = QtGui.QLabel(col)
            gridLayout.addWidget(l, row, 0)

            value = self.csvData.columns.get(col)
            if value:
                value = str(value)
            else:
                value = "0"
            le = QtGui.QLineEdit(value)
            le.setValidator(QtGui.QIntValidator(0, 9, le))
            gridLayout.addWidget(le, row, 1)
            self.ledits.append(le)
            row += 1

    def accept(self):
        sep = str(self.ui.comboBox.currentText().toUtf8())
        i = 0
        cols = {}
        for f in self.fields:
            v = int(self.ledits[i].text())
            cols[f] = v
            i += 1
        self.csvData.setData(sep, cols)
        QtGui.QDialog.accept(self)

def getCsvConfig(colspec, csvData):
    dlg = GuiCsvConfig(colspec, csvData)
    return dlg.exec_()
