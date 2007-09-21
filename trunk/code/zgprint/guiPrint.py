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
"""Interface to the pyuic4 generated 'form', ui_zgprint.py
pyuic4 command:
      pyuic4 -o ui_zgprint.py zgprint.ui

To convert the i18n stuff to gettext form, use gettextify, e.g.
      gettextify ui_zgprint.py
"""

from PyQt4 import QtCore, QtGui

import ui_zgprint as ui_form

from gui0 import Application
from printView import PrintView

class GuiPrint():
    """There may be only one instance of this class, because of the
    slot declarations.
    """
    def __init__(self, appString, file=None):
        self.app = Application(appString)
        self.settings = self.app.settings

        slot("%s-closeMainWindow" % appString, self.slot_tidy)

        # Prepare the print handler
        self.pView = PrintView()

        self.init(file)

    def init(self, file):
        """Subsequent invocations of the print application start by
        reinitializing the print handler here.
        """
        self.gui = GuiWidget(self.settings)
        self.app.init(self.gui)

        # Set up the print gui
        self.pView.init(self.gui, file)

    def run(self):
        self.app.run()

    def slot_tidy(self, arg):
        """Stuff to do when the program quits
        """
        if self.pView.printer:
            self.pView.printer.abort()


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

    def showDbFile(self, path):
        self.setWindowTitle(
                argSub(_("zgprint - Waldorf report printer   (%1)"), (path,)))

    def setClasses(self, classList):
        self.ui.comboBox_class.clear()
        self.ui.comboBox_class.addItems(classList)
        # causes a classChanged signal to be emitted (0 index)

    def setPupils(self, pupilList):
        """Set the content of the pupilList widget, all entries
        initially unchecked.
        """
        self.ui.listWidget_pupils.clear()
        for p in pupilList:
            lwi = QtGui.QListWidgetItem(p, self.ui.listWidget_pupils)
            lwi.setCheckState(QtCore.Qt.Unchecked)

    def initPagesList(self):
        """Initiate the setting up of the page selection list.
        Thus causes an 'individualPages' signal to be emitted.
        Toggling the 'multi' button first ensures the sending of the
        signal and also the correct disabling of the irrelevant
        print options.
        """
        self.ui.radioButton_pagesM.setChecked(True)
        self.ui.radioButton_pagesI.setChecked(True)

    def setPages(self, pageList):
        """Set the content of the pageList widget, all entries
        initially unchecked.
        """
        self.ui.listWidget_pages.clear()
        for p in pageList:
            lwi = QtGui.QListWidgetItem(p, self.ui.listWidget_pages)
            lwi.setCheckState(QtCore.Qt.Unchecked)

    def isPupilChecked(self, i):
        """Return checked state of the pupil at position i of the list.
        """
        return (self.ui.listWidget_pupils.item(i).checkState() ==
                QtCore.Qt.Checked)

    def getPages(self):
        """Return a list of (page name, checked state) pairs for the
        pages in the page list widget.
        """
        count = self.ui.listWidget_pages.count()
        items = []
        for i in range(count):
            item = self.ui.listWidget_pages.item(i)
            items.append((unicode(item.text()), (item.checkState() ==
                QtCore.Qt.Checked)))
        return items

    def pageType(self):
        """Return whether printing single, individual or multi- pages.
        """
        if self.ui.radioButton_pagesS.isChecked():
            return "single"
        elif self.ui.radioButton_pagesM.isChecked():
            return "multi"
        else:
            return "all"


    def isShrink(self):
        """Return whether shrinking multiple pages.
        """
        return (self.ui.checkBox_shrink.checkState() ==
                QtCore.Qt.Checked)

    def isLandscape(self):
        """Return whether printing multiple pages in landscape orientation.
        """
        return (self.ui.checkBox_landscape.checkState() ==
                QtCore.Qt.Checked)

    def isReverse(self):
        """Return whether reversing the printing order.
        """
        return (self.ui.checkBox_reverse.checkState() ==
                QtCore.Qt.Checked)

    def isPdf(self):
        """Return whether outputting to pdf.
        """
        return (self.ui.checkBox_pdf.checkState() ==
                QtCore.Qt.Checked)

    def report(self, text):
        self.ui.textEdit.append(text)
        QtGui.QApplication.sendPostedEvents()
        QtGui.QApplication.processEvents()

# 'Autoslots' (connections set up automatically)
# The cancel button is connected using 'designer'.
#    @QtCore.pyqtSignature("")   # filters out the desired signal signature
#    def on_pushButton_cancel_clicked(self):
#        self.close()

    @QtCore.pyqtSignature("int")
    def on_comboBox_class_currentIndexChanged(self, index):
        signal("classChanged", index)

    @QtCore.pyqtSignature("")
    def on_pushButton_open_clicked(self):
        signal("openDB", True)

    @QtCore.pyqtSignature("")
    def on_pushButton_selectAllPupils_clicked(self, enable=QtCore.Qt.Checked):
        """Set selection flag for all pupils in list according to
        'enable' value.
        """
        plist = self.ui.listWidget_pupils
        for i in range(plist.count()):
            plist.item(i).setCheckState(enable)

    @QtCore.pyqtSignature("")
    def on_pushButton_unselectAllPupils_clicked(self):
        self.on_pushButton_selectAllPupils_clicked(QtCore.Qt.Unchecked)

    @QtCore.pyqtSignature("bool")
    def on_radioButton_pagesI_toggled(self, on):
        if on:
            signal("individualPages")

    @QtCore.pyqtSignature("bool")
    def on_radioButton_pagesS_toggled(self, on):
        if on:
            signal("singlePages")

    @QtCore.pyqtSignature("bool")
    def on_radioButton_pagesM_toggled(self, on):
        if on:
            signal("multiPages")

    @QtCore.pyqtSignature("")
    def on_pushButton_allPages_clicked(self, enable=QtCore.Qt.Checked):
        """Set selection flag for all pages in list according to
        'enable' value.
        """
        plist = self.ui.listWidget_pages
        for i in range(plist.count()):
            plist.item(i).setCheckState(enable)

    @QtCore.pyqtSignature("")
    def on_pushButton_preview_clicked(self):
        signal("preview")

    @QtCore.pyqtSignature("")
    def on_pushButton_print_clicked(self):
        signal("print")
