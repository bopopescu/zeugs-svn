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
"""Interface to the pyuic4 generated 'form', ui_zgsync.py
pyuic4 command:
      pyuic4 -o ui_zgsync.py zgsync.ui

To convert the i18n stuff to gettext form, use gettextify, e.g.
      gettextify ui_zgsync.py
"""

from PyQt4 import QtCore, QtGui

import ui_zgsync as ui_form

from gui0 import Application
from guiDialogs import getFile
from synchronize import SyncPanel

import os.path


class GuiSync():
    """There may be only one instance of this class, because of the
    slot declarations.
    """
    def __init__(self, appString, filepath=None):
        self.app = Application(appString)
        self.settings = self.app.settings
        slot("%s-closeMainWindow" % appString, self.slot_tidy)
        self.sp = SyncPanel(self.settings)
        self.init(filepath)

    def init(self, filepath=None):
        self.gui = GuiWidget(self.settings)

        self.app.init(self.gui)

        self.sp.init(self.gui, filepath)

    def run(self):
        if self.sp and self.sp.filepath:
            #self.app.run()
            self.gui.exec_()

    def slot_tidy(self, arg):
        """Stuff to do when the program quits
        """
        if self.sp:
            self.sp.disconnect()
            self.sp.closeFile()


class GuiWidget(QtGui.QDialog):
    def __init__(self, settings):
        QtGui.QDialog.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        #self.setModal(True)

        self.settings = settings

        self.ui = ui_form.Ui_Form()

    def closeEvent(self, event):
        """Called when the window is closed. Do tidying up actions.
        """
        signal("%s-closeMainWindow" % self.settings.appString)
        event.accept()

    def setTitle(self, title):
        self.setWindowTitle(title)

    def setDBinfo(self, dbhost, dbname, dbuser, filepath):
        self.ui.lineEdit_host.setText(dbhost)
        self.ui.lineEdit_name.setText(dbname)
        self.ui.lineEdit_user.setText(dbuser)
        self.ui.lineEdit_dbs.setText(filepath)

    def getDBhost(self):
        return unicode(self.ui.lineEdit_host.text())

# 'Autoslots' (connections set up automatically)
# The quit button is connected using 'designer'.
#    @QtCore.pyqtSignature("")   # filters out the desired signal signature
#    def on_pushButton_Quit_clicked(self):
#        self.close()

    @QtCore.pyqtSignature("")
    def on_pushButton_browse_clicked(self):
        signal("sp_browse")

    @QtCore.pyqtSignature("")
    def on_pushButton_pw_clicked(self):
        signal("sp_newpw")

    @QtCore.pyqtSignature("")
    def on_pushButton_sync_clicked(self):
        self.ui.pushButton_pw.setEnabled(False)
        self.ui.pushButton_sync.setEnabled(False)
        self.ui.pushButton_quit.setEnabled(False)

        signal("sp_sync")

        self.ui.pushButton_pw.setEnabled(True)
        self.ui.pushButton_sync.setEnabled(True)
        self.ui.pushButton_quit.setEnabled(True)


