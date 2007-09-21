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
"""Interface to the pyuic4 generated 'form', ui_zgcp.py
pyuic4 command:
      pyuic4 -o ui_zgcp.py zgcp.ui

To convert the i18n stuff to gettext form, use gettextify, e.g.
      gettextify ui_zgcp.py
"""

from PyQt4 import QtCore, QtGui

import ui_zgcp as ui_form

from gui0 import Application
from getConnectInfo import getConnectInfo
from dbWrapMaster import DB, ADMIN
from controlPanel import ControlPanel

class GuiCP:
    """There may be only one instance of this class, because of the
    slot declarations.
    """
    def __init__(self, appString):
        self.app = Application(appString)
        self.settings = self.app.settings
        slot("%s-closeMainWindow" % appString, self.slot_tidy)
        self.cp = ControlPanel(self.settings)

        self.init()

    def init(self):
        self.db = None

        self.gui = GuiWidget(self.settings)
        self.gui.show()
        c0 = self.gui.cursor()
        self.gui.setCursor(QtGui.QCursor(QtCore.Qt.BusyCursor))

        # Connect to control database
        connectData = getConnectInfo(self.settings, ADMIN)
        if not connectData:
            return
        db = DB(connectData)
        self.gui.setCursor(c0)
        if not db.isOpen():
            error(_("Couldn't open control database"))
            return # actually error shouldn't return
        self.db = db

        self.app.init(self.gui)

        # set up lists of available databases, admins, users, etc.
        # and initialize the main module
        self.cp.init(self.gui, self.db)

    def run(self):
        if self.db:
            self.app.run()

    def slot_tidy(self, arg):
        """Stuff to do when the program quits
        """
        if self.db:
            self.db.close()

class GuiWidget(QtGui.QWidget):
    def __init__(self, settings):
        QtGui.QWidget.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.settings = settings

        self.ui = ui_form.Ui_Form()

    def closeEvent(self, event):
        """Called when the window is closed. Do tidying up actions.
        """
        signal("%s-closeMainWindow" % self.settings.appString)
        event.accept()

    def setDBlist(self, dbs):
        self.ui.comboBox_db.clear()
        self.ui.comboBox_db.addItems(dbs)

#    def getDBname(self, index):
#        unicode(self.ui.comboBox_db.itemText(index))

    def setDBhost(self, dbhost):
        self.ui.lineEdit_host.setText(dbhost)

    def setUserList(self, users):
        """Set the content of the user list widget, all entries
        initially unchecked.
        """
        self.ui.listWidget_users.clear()
        for u in users:
            lwi = QtGui.QListWidgetItem(u, self.ui.listWidget_users)
            lwi.setCheckState(QtCore.Qt.Unchecked)

    def userListSetChecked(self, i, on):
        """Check or uncheck the indexed item in the users list.
        """
        if on:
            state = QtCore.Qt.Checked
        else:
            state = QtCore.Qt.Unchecked
        self.ui.listWidget_users.item(i).setCheckState(state)

    def setFinalized(self, on):
        self.ui.pushButton_finalize.setChecked(on)
        if on:
            text = u"<font color=#ff0000>%s</font>" % _("Finalized")
        else:
            text = u"<font color=#00ff00>%s</font>" % _("Active")
        self.ui.label_finalized.setText(text)

    def getSelectedUsers(self, users):
        ul = []
        for i in range(len(users)):
            if (self.ui.listWidget_users.item(i).checkState() ==
                    QtCore.Qt.Checked):
                ul.append(users[i])
        return ul

    def signal(self, sig, arg=None):
        c0 = self.cursor()
        self.setCursor(QtGui.QCursor(QtCore.Qt.BusyCursor))
        signal(sig, arg)
        self.setCursor(c0)

# 'Autoslots' (connections set up automatically)
# The quit button is connected using 'designer'.
#    @QtCore.pyqtSignature("")   # filters out the desired signal signature
#    def on_pushButton_Quit_clicked(self):
#        self.close()

    @QtCore.pyqtSignature("int")
    def on_comboBox_db_currentIndexChanged(self, index):
        self.signal("cp_newdbIndex", index)

    @QtCore.pyqtSignature("")
    def on_pushButton_updatedb_clicked(self):
        self.signal("cp_updatedb")

    @QtCore.pyqtSignature("")
    def on_pushButton_dump_clicked(self):
        self.signal("cp_dump")

    @QtCore.pyqtSignature("")
    def on_pushButton_print_clicked(self):
        self.signal("cp_print")

    @QtCore.pyqtSignature("bool")
    def on_pushButton_finalize_toggled(self, on):
        self.signal("cp_finalize", on)

    @QtCore.pyqtSignature("")
    def on_pushButton_newdb_clicked(self):
        self.signal("cp_newdb")

    @QtCore.pyqtSignature("")
    def on_pushButton_sync_clicked(self):
        self.signal("cp_sync")

    @QtCore.pyqtSignature("")
    def on_pushButton_restore_clicked(self):
        self.signal("cp_restore")

    @QtCore.pyqtSignature("")
    def on_pushButton_dumpd_clicked(self):
        self.signal("cp_restoreDataFiles")

    @QtCore.pyqtSignature("")
    def on_pushButton_dbdel_clicked(self):
        self.signal("cp_dbdel")

    @QtCore.pyqtSignature("")
    def on_pushButton_gen_clicked(self):
        self.signal("cp_genTdb")

    @QtCore.pyqtSignature("")
    def on_pushButton_pwd_clicked(self):
        self.signal("cp_pwd")

    @QtCore.pyqtSignature("")
    def on_pushButton_usel_clicked(self):
        self.signal("cp_selTeachers")

    @QtCore.pyqtSignature("")
    def on_pushButton_uunsel_clicked(self):
        for i in range(self.ui.listWidget_users.count()):
            self.ui.listWidget_users.item(i).setCheckState(QtCore.Qt.Unchecked)

    @QtCore.pyqtSignature("")
    def on_pushButton_uinvsel_clicked(self):
        for i in range(self.ui.listWidget_users.count()):
            self.userListSetChecked(i,
                    (self.ui.listWidget_users.item(i).checkState()
                            != QtCore.Qt.Checked))
