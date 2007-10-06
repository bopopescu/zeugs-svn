#!/usr/bin/env python
# -*- coding: utf-8 -*-

#2007-08-26
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
"""A simple dialog to fetch the connection parameters for the
master (by default PostgreSQL) database.
"""
# pyuic4 command:
#      pyuic4 -o ui_dlg_connect.py dlg_connect.ui

# To convert the i18n stuff to gettext form, use gettextify, e.g.
#      gettextify ui_dlg_connect.py

# The name of the control database
CONTROLDB = u"zeugscontrol2"

from PyQt4 import QtCore, QtGui

import ui_dlg_connect as ui_dlg
from dbWrapMaster import ADMIN
from gui0 import Application

def getConnectInfo(settings, user):
    return GuiConnectInfo("connectInfo", user).run()


class GuiConnectInfo:
    def __init__(self, appString, user):
        self.app = Application(appString)
        self.settings = self.app.settings

        self.gui = GuiWidget(self.settings)
        #slot("%s-closeMainWindow" % appString, self.slot_tidy)

        self.app.init(self.gui)
        self.gui.init(user)

    def run(self):
        if not self.gui.exec_():
            return None

        return { u"host" : self.gui.host, u"user" : self.gui.dbuser,
                u"pw" : self.gui.pw, u"db" : CONTROLDB }


class GuiWidget(QtGui.QDialog):
    def __init__(self, settings):
        QtGui.QDialog.__init__(self)
        # Don't use this if you want to access the widget afterwards:
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.settings = settings

        self.ui = ui_dlg.Ui_Dialog()

    def init(self, user):
        host = self.settings.getSetting("host")
        if not host:
            host = "localhost"
        self.ui.lineEdit_host.setText(host)

        self.ui.lineEdit_user.setText(user)

        self.ui.lineEdit_pw.setFocus()

    @QtCore.pyqtSignature("")
    def on_pushButton_connect_clicked(self):
        self.host = unicode(self.ui.lineEdit_host.text())
        self.dbuser = unicode(self.ui.lineEdit_user.text())
        self.settings.setSetting("host", self.host)
        self.pw = unicode(self.ui.lineEdit_pw.text())

        signal("%s-closeMainWindow" % self.settings.appString)

        self.accept()
