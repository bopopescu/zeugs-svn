# -*- coding: utf-8 -*-

#2007-09-05
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
"""GUI for Zeugnis program - this provides an application class and
persistent settings. Each individual application can/should use this.
"""

# initial values
defaultAppFontSize = "12"

import sys, os
from PyQt4 import QtCore, QtGui

from database import DBVERSION

def slot_quit(arg):
    QtGui.QApplication.instance().quit()

class Application:
    """This class manages the GUI, including creation of the main window.
    It also handles user-configuration settings, using the QSettings
    facility.
    """
    def __init__(self, appString):
        self.mainWindow = None
        self.app0 = QtGui.QApplication.instance()
        if self.app0:
            self.app = self.app0
        else:
            self.app = QtGui.QApplication(sys.argv)
            slot("quit", slot_quit)

        slot("incFontSize", self.incAppFontSize)
        slot("%s-closeMainWindow" % appString, self.slot_saveSizePos)

        self.settings = Settings(appString)

        if not self.app0:
            # Set the application font size
            size = self.settings.getVal("fontSize")
            if not size:
                size = defaultAppFontSize
            self.setAppFontSize(int(size))

    def incAppFontSize(self, delta):
        size = int(self.settings.getVal("fontSize"))
        if (size < 8):
            self.setAppFontSize(8)
        elif (size > 20):
            self.setAppFontSize(20)
        else:
            size += delta
            if (size >= 8) and (size <= 20):
                self.setAppFontSize(size)

    def setAppFontSize(self, size):
        font = self.app.font()
        font.setPointSize(size)
        self.app.setFont(font)
        self.settings.setVal("fontSize", size)

    def init(self, form):
        """Create the main window.
        """
        self.mainWindow = form

        d0 = os.getcwd()
        if not os.path.isdir("icons"):
            # Change directory to set up the gui, to cope with the icons
            # This is needed so that the code can be run from the
            # source tree as well as the distribution tree, which has
            # slightly different relative paths.
            os.chdir("gui")
        # Set up the form output by pyuic4
        form.ui.setupUi(form)
        os.chdir(d0)

        mainWindowSize = self.settings.getSetting("mainSize")
        if mainWindowSize:
            mainWindowPos = self.settings.getSetting("mainPos")
            self.setSizePos(mainWindowSize, mainWindowPos)

# Alternative using 'restoreGeometry'
#        oldgeom = self.settings.value(self.settings.appString + "/mainGeom")
#        self.mainWindow.restoreGeometry(oldgeom.toByteArray())


    def run(self):
        """Show window and enter event loop.
        """
        if self.mainWindow:
            self.mainWindow.show()
        if not self.app0:
            # This only needs to be (only should be) called for the
            # first main window.
            self.app.exec_()

    def clipboard(self):
        """Get the clipboard.
        """
        return self.app.clipboard()

    def slot_saveSizePos(self, arg):
        """Using the settings mechanism, save the size and position
        of the main window, so that it can be restored for the next run.
        """
#        size = self.mainWindow.size()
#        self.settings.setSetting("mainSize", u"%d %d" %
#                (size.width(), size.height()))
#        pos = self.mainWindow.pos()
#        self.settings.setSetting("mainPos", u"%d %d" %
#                (pos.x(), pos.y()))

# Alternative using 'geometry' (see setSizePos below)
        size = self.mainWindow.geometry()
        self.settings.setSetting("mainSize", u"%d %d" %
                (size.width(), size.height()))
        self.settings.setSetting("mainPos", u"%d %d" %
                (size.x(), size.y()))

# Alternative using 'saveGeometry'
#        self.settings.setValue(self.settings.appString + "/mainGeom",
#                QtCore.QVariant(self.mainWindow.saveGeometry()))

    def setSizePos(self, wH, xY=None):
        """Resize and place the application's main window.
        wH is a string 'width height'.
        xY is a string 'x y', but can also be None, implying no
        placement.
        """
        size = QtCore.QSize(*map(int, wH.split()))
        size = size.expandedTo(self.mainWindow.minimumSizeHint())
#        self.mainWindow.resize(size)
#
#At least in KDE this doesn't work quite as desired, the window is
# placed slghtly offset - maybe connected with the decoration?
#        if xY:
#            pos = QtCore.QPoint(*map(int, xY.split()))
#            self.mainWindow.move(pos)

# Alternative using 'geometry' (see slot_saveSizePos above)
#        if xY:
#            x, y = [int(i) for i in xY.split()]
#            self.mainWindow.setGeometry(x, y, size.width(), size.height())

#        else:
#            self.mainWindow.resize(size)
#BUT it might be better to let the window manager do the placement!
        self.mainWindow.resize(size)

class Settings(QtCore.QSettings):
    def __init__(self, appString):
        self.appString = appString
        QtCore.QSettings.__init__(self, QtCore.QSettings.IniFormat,
            QtCore.QSettings.UserScope,
            "gradgrind", "Zeugs%s" % DBVERSION)
        self.setFallbacksEnabled(False)

    def getVal(self, item):
        """Use the settings facility get a configuration value.
        """
        return unicode(self.value(item).toString())

    def setVal(self, item, value):
        """Use the settings facility set a configuration value.
        """
        self.setValue(item, QtCore.QVariant(value))

    def getSetting(self, item):
        """Use the settings facility get a configuration value, taking
        the settings group into account.
        """
        string = self.appString + "/" + item
        return unicode(self.value(string).toString())

    def setSetting(self, item, value):
        """Use the settings facility set a configuration value, taking
        the settings group into account.
        """
        string = self.appString + "/" + item
        self.setValue(string, QtCore.QVariant(value))
