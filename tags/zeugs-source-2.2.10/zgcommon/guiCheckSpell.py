#!/usr/bin/env python
# -*- coding: utf-8 -*-

#2007-06-27
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
"""The dialog for interactive spell-checking.
"""

# pyuic4 command:
#      pyuic4 -o ui_checkSpell.py checkSpell.ui

# To convert the i18n stuff to gettext form, use gettextify, e.g.
#      gettextify ui_checkSpell.py

from PyQt4 import QtCore, QtGui

import ui_checkSpell as ui_form

class NUGui(QtGui.QWidget):
    def __init__(self, main):
        QtGui.QWidget.__init__(self)
        self.ui = ui_form.Ui_Form()
        self.ui.setupUi(self)
        self.main = main        # Main spell checking object

    def setText(self, text, word):
        hword = u"<font color=red>%s</font>" % word
        self.ui.textEdit.setHtml(text % hword)

    def getLine(self):
        return unicode(self.ui.comboBox.currentText())

    def setSuggestions(self, ilist):
        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(ilist)

    @QtCore.pyqtSignature("")
    def on_pushButton_ignore_clicked(self):
        """Ignore just this word, i.e. move on to the next 'error'.
        """
        self.main.ignore()

    @QtCore.pyqtSignature("")
    def on_pushButton_ignoreAll_clicked(self):
        """Ignore this word throughout the document.
        """
        self.main.ignoreAll()

    @QtCore.pyqtSignature("")
    def on_pushButton_add_clicked(self):
        """Add this word to the personal word list.
        """
        self.main.addWord()

    @QtCore.pyqtSignature("")
    def on_pushButton_change_clicked(self):
        """Replace this word by the one in the entry widget.
        """
        self.main.subWord(self.getLine())

    @QtCore.pyqtSignature("")
    def on_pushButton_changeAll_clicked(self):
        """Replace this word by the one in the entry widget, also
        when it is found later during this program run.
        """
        self.main.subWordAll(self.getLine())

    @QtCore.pyqtSignature("")
    def on_pushButton_close_clicked(self):
        """Abort the operation.
        """
        self.main.ignore(True)
