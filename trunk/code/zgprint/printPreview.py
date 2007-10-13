#!/usr/bin/env python
# -*- coding: utf-8 -*-

#2007-10-12
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
"""The print preview dialog.
"""
# pyuic4 command:
#      pyuic4 -o ui_printPreview.py printPreview.ui

# To convert the i18n stuff to gettext form, use gettextify, e.g.
#      gettextify ui_printPreview.py

from PyQt4 import QtCore, QtGui
import math

from layoutReport import LayoutReport
from guiBase import RESOLUTION

import ui_printPreview as ui_dlg

class PrintPreview(QtGui.QDialog):
    def __init__(self, db, settings, pupilNames, pupilIds, pageType,
            sheetSides, pages, allPages):
        QtGui.QDialog.__init__(self)
        self.ui = ui_dlg.Ui_Dialog()
        self.ui.setupUi(self)
        self.settings = settings
        windowSize = self.settings.getSetting("printPreviewSize")
        if windowSize:
            size = QtCore.QSize(*map(int, windowSize.split()))
            size = size.expandedTo(self.minimumSizeHint())
            self.resize(size)

        self.screenScale = float(self.logicalDpiX()) / RESOLUTION

        s = self.settings.getSetting("printPreviewScale")
        if s:
            s = int(s)
        else:
            s = 10
        self.ui.sizeSlider.setValue(1)
        self.ui.sizeSlider.setValue(s)

        self.db = db
        self.pupilIds = pupilIds
        self.layout = None
        self.page = None
        self.part = 0
        self.pageType = pageType
        if (self.pageType == "multi"):
            self.ui.radioButton_l.setEnabled(True)
            self.ui.radioButton_r.setEnabled(True)
            self.ui.radioButton_l.setChecked(True)
        self.sheetSides = sheetSides
        self.allPages = allPages
        self.ui.comboBox_pupil.addItems(pupilNames)
        self.ui.comboBox_page.addItems(pages)

    @QtCore.pyqtSignature("")
    def on_pushButton_clicked(self):
        """Called when finished with viewing. Save window size and scale.
        """
        size = self.size()
        self.settings.setSetting("printPreviewSize", u"%d %d" %
                (size.width(), size.height()))
        self.settings.setSetting("printPreviewScale", u"%d" % self.scale)
        self.accept()

    @QtCore.pyqtSignature("int")
    def on_comboBox_pupil_currentIndexChanged(self, ix):
        if (ix < 0): return
        pupilId = self.pupilIds[ix]
        c = self.cursor()
        self.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.layout = LayoutReport(self.db, pupilId)
        self.setCursor(c)
        self.newPage()

    @QtCore.pyqtSignature("int")
    def on_comboBox_page_currentIndexChanged(self, ix):
        if (ix < 0): return
        self.page = unicode(self.ui.comboBox_page.itemText(ix))
        self.newPage()

    @QtCore.pyqtSignature("bool")
    def on_radioButton_l_toggled(self, on):
        if on:
            self.part = 0
            self.newPage()

    @QtCore.pyqtSignature("bool")
    def on_radioButton_r_toggled(self, on):
        if on:
            self.part = 1
            self.newPage()

    @QtCore.pyqtSignature("int")
    def on_sizeSlider_valueChanged(self, val):
        self.setSize(val)

    def newPage(self):
        if (self.page == None) or (self.layout == None):
            return

        if (self.pageType == "all"):
            pgname = self.page
        else:
            for pg, pos in self.sheetSides[self.page]:
                if (pos == self.part):
                    pgname = pg
                    break

        ip = self.allPages.index(pgname)

        c = self.cursor()
        self.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.ui.graphicsView.setScene(None)
        self.ui.graphicsView.setScene(self.layout.pages[ip].gScene)
        self.setCursor(c)

    def setSize(self, val):
        self.scale = val
        qm = QtGui.QMatrix()
        s = math.exp(float(val-10)/6) * self.screenScale
        qm.scale(s, s)
        self.ui.graphicsView.setMatrix(qm)

