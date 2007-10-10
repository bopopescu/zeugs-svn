# -*- coding: UTF-8 -*-
#2007-09-06
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
"""Pop-up dialogs for general use.
"""

from PyQt4 import QtCore, QtGui

import os.path

import ui_dlg_newNode as ui_dialog

def getDirectory(title, startDir=None):
    """Present a dialog to select a directory.
    """
    dialog = QtGui.QFileDialog(None, title)
    dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
    dialog.setLabelText(QtGui.QFileDialog.LookIn, _("Look in:"))
    dialog.setLabelText(QtGui.QFileDialog.FileName, _("Directory name:"))
    dialog.setLabelText(QtGui.QFileDialog.FileType, _("Files of type:"))
    dialog.setLabelText(QtGui.QFileDialog.Accept, _("OK"))
    dialog.setLabelText(QtGui.QFileDialog.Reject, _("Cancel"))
    if startDir:
        dialog.setDirectory(os.path.dirname(startDir))
        dialog.selectFile(os.path.basename(startDir))
    else:
        dialog.setDirectory(os.path.expanduser('~'))
    dialog.setResolveSymlinks(False)
    if dialog.exec_():
        return unicode(dialog.selectedFiles()[0]).rstrip(u"/\\")
    else:
        return None

def getFile(title, startDir=None, startFile=None,
        defaultSuffix=None, filter=None, create=False):
    """Present a dialog to select a file. If 'create' is True
    a not-yet-existing file may be selected.
    filter format example: (_("pdf Files"), (u"*.pdf",))
    """
    dialog = QtGui.QFileDialog(None, title)
    if create:
        dialog.setFileMode(QtGui.QFileDialog.AnyFile)
    else:
        dialog.setFileMode(QtGui.QFileDialog.ExistingFile)
    dialog.setLabelText(QtGui.QFileDialog.LookIn, _("Look in:"))
    dialog.setLabelText(QtGui.QFileDialog.FileName, _("File name:"))
    dialog.setLabelText(QtGui.QFileDialog.FileType, _("Files of type:"))
    dialog.setLabelText(QtGui.QFileDialog.Accept, _("OK"))
    dialog.setLabelText(QtGui.QFileDialog.Reject, _("Cancel"))
    if startDir:
        dialog.setDirectory(startDir)
    else:
        dialog.setDirectory(os.path.expanduser('~'))
    if defaultSuffix:
        dialog.setDefaultSuffix(defaultSuffix)
    if filter:
        # very toolkit-specific!
        f = filter[1][0]
        for fx in filter[1][1:]:
            f += u" " + fx
        dialog.setFilter(u"%s (%s)" % (filter[0], f))
    dialog.setConfirmOverwrite(False)
    dialog.setResolveSymlinks(False)
    if startFile:
        dialog.selectFile(startFile)
    if not dialog.exec_():
        return None
    return unicode(dialog.selectedFiles()[0])

def warnDialog(title, text):
    """Present a warning dialog.
    """
    QtGui.QMessageBox.warning(None, title, text, _("OK"))

def messageDialog(title, text):
    """Present a message dialog.
    """
    QtGui.QMessageBox.information(None, title, text, _("OK"))

def confirmationDialog(title, text, default=True):
    """Present a confirmation dialog. 'default' determines whether 'OK'
    (True) or 'Cancel' (False) is the default.
    """
    if default:
        dbn = 1
    else:
        dbn = 0
    btn = QtGui.QMessageBox.question(None, title, text,
            _("Cancel"), _("OK"), "", dbn)
    return (btn != 0)


class GuiNewNode(QtGui.QDialog):
    """Interface to the pyuic4 generated line edit dialog ui_dlg_newNode.py

    pyuic4 command:
          pyuic4 -o ui_dlg_newNode.py dlg_newNode.ui

    To convert the i18n stuff to gettext form, use gettextify, e.g.
          gettextify ui_dlg_newNode.py
    """
    def __init__(self, qv, start):
        QtGui.QDialog.__init__(self)
        self.ui = ui_dialog.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.lineEdit.setValidator(qv)
        self.ui.lineEdit.setText(QtCore.QString.fromUtf8(start))
        self.string = ''

    def accept(self):
        self.string = str(self.ui.lineEdit.text().toUtf8())
        QtGui.QDialog.accept(self)

def getFileName(start=''):
    """A dialog to fetch a filename which may only contain the
    characters [a-z], [0-9], [_] and [-]
    """
    rx = QtCore.QRegExp(QtCore.QString.fromUtf8('[a-z0-9_\-]+'))
    qv = QtGui.QRegExpValidator(rx, None)
    dlg = GuiNewNode(qv, start)
    if dlg.exec_():
        return dlg.string.strip()
    else:
        return None

