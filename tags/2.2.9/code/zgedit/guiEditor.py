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
"""Interface to the pyuic4 generated 'form', ui_zgedit.py
pyuic4 command:
      pyuic4 -o ui_zgedit.py zgedit.ui

To convert the i18n stuff to gettext form, use gettextify, e.g.
      gettextify ui_zgedit.py
"""

from PyQt4 import QtCore, QtGui

import os.path

import ui_zgedit as ui_mainWindow
from guiBase import coloursInit
from gui0 import Application
from editorView import EditorView

class GuiEditor:
    """There may be only one instance of this class, because of the
    slot declarations (in editorView.py and edit.py). At present there
    is no possibility of closing an editor and reopening it in the same
    process - the other files would need modifying.
    """
    def __init__(self, appString):
        self.app = Application(appString)
        self.settings = self.app.settings

        self.gui = GuiWidget(self.settings, self.app.clipboard())

        # Initialize the colour objects used by the editor
        coloursInit()

        self.app.init(self.gui)

        styleGroup = QtGui.QActionGroup(self.gui)
        styleGroup.addAction(self.gui.ui.action_styleN)
        styleGroup.addAction(self.gui.ui.action_styleS)
        styleGroup.addAction(self.gui.ui.action_styleSR)

        # Set up the editor gui
        self.edView = EditorView(self.gui)
        # Open a database and initialize the editor
        self.edView.slot_open(force=False)

    def run(self):
        if self.edView.db:
            self.app.run()


class GuiWidget(QtGui.QMainWindow):
    def __init__(self, settings, clipboard):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.settings = settings
        self.clipboard = clipboard

        self.ui = ui_mainWindow.Ui_MainWindow()

        if os.path.isdir("icons"):
            # This is needed so that the code can be run from the
            # source tree as well as the distribution tree, which has
            # slightly different relative paths.
            iconDir = "icons"
        else:
            iconDir = "gui/icons"

        self.checkIcons = {
                "off"     : QtGui.QIcon(iconDir + "/unfinished.png"),
                "on"      : QtGui.QIcon(iconDir + "/finished.png"),
                }
        self.checkLabels = {
                "off"     : _("incomplete"),
                "on"      : _("complete"),
                }

    def closeEvent(self, event):
        """Called when the window is closed. Do tidying up actions.
        """
        signal("pupilChanged", -1)  # ensure current report is saved
        signal("%s-closeMainWindow" % self.settings.appString)
        event.accept()

    def getGView(self):
        """Get the graphics view widget for the editor.
        """
        return self.ui.graphicsView

    def focusEditor(self):
        """Direct keyboard input to the text editor.
        """
        self.ui.graphicsView.setFocus()

    def setStyleButton(self, style):
        if (style == u"n"):
            self.ui.action_styleN.setChecked(True)
            self.enableIndent(False)
            return
        if (style == u"l"):
            self.ui.action_styleS.setChecked(True)
        else:
            self.ui.action_styleSR.setChecked(True)
        self.enableIndent(True)

    def enableIndent(self, en):
        self.ui.action_indent.setEnabled(en)
        self.ui.action_unindent.setEnabled(en)

    def enableRedo(self, en):
        self.ui.action_Redo.setEnabled(en)

    def enableUndo(self, en):
        self.ui.action_Undo.setEnabled(en)

    def setClasses(self, classList):
        self.ui.comboBox_class.clear()
        self.ui.comboBox_class.addItems(classList)
        # causes a classChanged signal to be emitted (0 index)

    def setClass(self, ix):
        self.ui.comboBox_class.setCurrentIndex(-1)
        self.ui.comboBox_class.setCurrentIndex(ix)
        # causes a classChanged signal to be emitted

    def setSubjects(self, subjectList):
        self.ui.comboBox_subject.clear()
        self.ui.comboBox_subject.addItems(subjectList)
        # causes a subjectChanged signal to be emitted (0 index)

    def setSubject(self, ix):
        self.ui.comboBox_subject.setCurrentIndex(-1)
        self.ui.comboBox_subject.setCurrentIndex(ix)
        # causes a subjectChanged signal to be emitted

    def setPupils(self, pupilList):
        self.ui.comboBox_pupil.clear()
        self.ui.comboBox_pupil.addItems(pupilList)
        # causes a pupilChanged signal to be emitted (0 index)

    def setPupil(self, ix):
        self.ui.comboBox_pupil.setCurrentIndex(-1)
        self.ui.comboBox_pupil.setCurrentIndex(ix)
        # causes a pupilChanged signal to be emitted

    def showDbFile(self, path):
        self.setWindowTitle(
                argSub(_("zgedit - Waldorf report editor   (%1)"), (path,)))

    def showTeacher(self, name):
        self.ui.lineEdit_teacher.setText(name)

    def setFinished(self, state):
        icon = self.checkIcons[state]
        label = self.checkLabels[state]
        self.ui.action_RequestCheck.setIcon(icon)
        self.ui.action_RequestCheck.setToolTip(label)

    def activateFinished(self, down):
        self.ui.action_RequestCheck.setChecked(down)

    def setClipboard(self, utext):
        self.clipboard.setText(utext)

    def getClipboard(self):
        return unicode(self.clipboard.text())

    def setAutoSpellCheck(self):
        self.ui.action_autospellcheck.setChecked(True)

    def setExtraChars(self, chars):
        """Display a widget with buttons for the 'extra' characters.
        """
        # This works by adding a widget dynamically to the existing
        # frame. When a new file is loaded this widget is removed
        # and regenerated.
        layout0 = self.ui.frame_chars.layout()
        if layout0:
            layout0.removeWidget(self.xcWidget)
            self.xcWidget.deleteLater()

        else:
            layout0 = QtGui.QVBoxLayout(self.ui.frame_chars)
            layout0.setMargin(1)
            layout0.setSpacing(0)

        self.xcWidget = QtGui.QWidget()
        layout = QtGui.QHBoxLayout(self.xcWidget)
        layout.setMargin(0)
        layout.setSpacing(1)


        fm = QtGui.QFontMetrics(self.font())
        h = fm.height()
        for ch in chars:
            b = QtGui.QPushButton(ch)
            b.setFixedSize(h, h+4)
            b.setFlat(True)
            layout.addWidget(b)
            QtCore.QObject.connect(b, QtCore.SIGNAL("clicked()"), self.char)

        layout0.addWidget(self.xcWidget)

    def char(self):
        """This is the (qt) slot called when one of the extra character
        buttons is pressed.
        """
        key = unicode(self.sender().text())
        self.focusEditor()          # needed to return focus to editor
        signal("keyPress", key)

# 'Autoslots' (connections set up automatically)
# The quit button is connected using 'designer'.
#    @QtCore.pyqtSignature("")   # filters out the desired signal signature
#    def on_pushButton_Quit_clicked(self):
#        self.close()

    @QtCore.pyqtSignature("int")
    def on_comboBox_class_currentIndexChanged(self, index):
        signal("classChanged", index)

    @QtCore.pyqtSignature("int")
    def on_comboBox_subject_currentIndexChanged(self, index):
        signal("subjectChanged", index)

    @QtCore.pyqtSignature("int")
    def on_comboBox_pupil_currentIndexChanged(self, index):
        signal("pupilChanged", index)

    @QtCore.pyqtSignature("")
    def on_pushButton_previous_clicked(self):
        signal("previous")

    @QtCore.pyqtSignature("")
    def on_pushButton_next_clicked(self):
        signal("next")

    @QtCore.pyqtSignature("")
    def on_action_Copy_triggered(self):
        signal("copy")

    @QtCore.pyqtSignature("")
    def on_action_Cut_triggered(self):
        signal("cut")

    @QtCore.pyqtSignature("")
    def on_action_Paste_triggered(self):
        signal("paste")

    @QtCore.pyqtSignature("")
    def on_action_Undo_triggered(self):
        signal("undo")

    @QtCore.pyqtSignature("")
    def on_action_Redo_triggered(self):
        signal("redo")

    @QtCore.pyqtSignature("")
    def on_action_styleN_triggered(self):
        signal("style", u"n")

    @QtCore.pyqtSignature("")
    def on_action_styleS_triggered(self):
        signal("style", u"l")

    @QtCore.pyqtSignature("")
    def on_action_styleSR_triggered(self):
        signal("style", u"r")

    @QtCore.pyqtSignature("")
    def on_action_indent_triggered(self):
        signal("indent", True)

    @QtCore.pyqtSignature("")
    def on_action_unindent_triggered(self):
        signal("indent", False)

    @QtCore.pyqtSignature("")
    def on_action_Open_triggered(self):
        signal("openDB", True)

    @QtCore.pyqtSignature("")
    def on_action_Synchronize_triggered(self):
        signal("sync")

    @QtCore.pyqtSignature("")
    def on_action_Print_triggered(self):
        signal("print", False)

    @QtCore.pyqtSignature("")
    def on_action_Print1_triggered(self):
        signal("print", True)

    @QtCore.pyqtSignature("")
    def on_action_RequestCheck_triggered(self):
        signal("requestCheck", self.ui.action_RequestCheck.isChecked())

    @QtCore.pyqtSignature("")
    def on_action_autospellcheck_triggered(self):
        signal("autospellcheck", self.ui.action_autospellcheck.isChecked())

    @QtCore.pyqtSignature("")
    def on_action_checkSpelling_triggered(self):
        signal("checkSpelling")

    @QtCore.pyqtSignature("")
    def on_action_nextUnfinished_triggered(self):
        signal("nextUnfinished")
