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
"""A simple dialog to fetch the password for connecting to the
master (PostgreSQL) database.
"""
# pyuic4 command:
#      pyuic4 -o ui_dlg_getPw.py dlg_getPw.ui

# To convert the i18n stuff to gettext form, use gettextify, e.g.
#      gettextify ui_dlg_getPw.py

from PyQt4 import QtCore, QtGui

import ui_dlg_getPw as ui_dlg

def getPw(host, name, user):
    Dialog = QtGui.QDialog()
    ui = ui_dlg.Ui_Dialog()
    ui.setupUi(Dialog)

    ui.lineEdit_host.setText(host)
    ui.lineEdit_name.setText(name)
    ui.lineEdit_user.setText(user)

    ui.lineEdit_pw.setFocus()
    if not Dialog.exec_():
        return None

    return unicode(ui.lineEdit_pw.text())
