#!/usr/bin/env python
# -*- coding: utf-8 -*-

#2007-09-11
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
"""Interface to the pyuic4 generated 'form', ui_dlg_appSelect.py
pyuic4 command:
      pyuic4 -o ui_dlg_appSelect.py dlg_appSelect.ui

To convert the i18n stuff to gettext form, use gettextify, e.g.
      gettextify ui_dlg_appSelect.py
"""

from PyQt4 import QtCore, QtGui

import ui_dlg_appSelect as ui_form
from gui0 import Application


class GuiGetApplication:
    def __init__(self, appString):
        self.app = Application(appString)

        self.settings = self.app.settings
        self.gui = GuiWidget(self.settings)

        self.app.init(self.gui)

    def run(self):
        self.app.run()

class GuiWidget(QtGui.QWidget):
    def __init__(self, settings):
        QtGui.QWidget.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.settings = settings
        self.selected = None

        self.ui = ui_form.Ui_Form()

    def closeEvent(self, event):
        """Called when the window is closed. Do tidying up actions.
        """
        signal("%s-closeMainWindow" % self.settings.appString)
        signal("selectApp", self.selected)
        event.accept()

    @QtCore.pyqtSignature("")
    def on_pushButton_bigger_clicked(self):
        signal("incFontSize", 1)

    @QtCore.pyqtSignature("")
    def on_pushButton_smaller_clicked(self):
        signal("incFontSize", -1)

    @QtCore.pyqtSignature("")
    def on_pushButton_edit_clicked(self):
        self.selected = "edit"
        self.close()

    @QtCore.pyqtSignature("")
    def on_pushButton_sync_clicked(self):
        self.selected = "sync"
        self.close()

    @QtCore.pyqtSignature("")
    def on_pushButton_print_clicked(self):
        self.selected = "print"
        self.close()

    @QtCore.pyqtSignature("")
    def on_pushButton_cp_clicked(self):
        self.selected = "control"
        self.close()

    @QtCore.pyqtSignature("")
    def on_pushButton_setup_clicked(self):
        self.selected = "setup"
        self.close()

    @QtCore.pyqtSignature("")
    def on_pushButton_configEd_clicked(self):
        self.selected = "cfged"
        self.close()
