#!/usr/bin/env python
# -*- coding: utf-8 -*-

#2007-09-16
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
"""Interface to the pyuic4 generated 'form', ui_configEd.py

pyuic4 command:
      pyuic4 -o ui_configEd.py configEd.ui

To convert the i18n stuff to gettext form, use gettextify, e.g.
      gettextify ui_configEd.py
"""

from PyQt4 import QtCore, QtGui

import ui_configEd as ui_form

from gui0 import Application
from configEd import ConfigEd

BASEITEMFLAGS = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled |
        QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsEnabled)

class GuiConfigEd:
    """There may be only one instance of this class, because of the
    slot declarations.
    """
    def __init__(self, appString):
        self.app = Application(appString)
        self.settings = self.app.settings
        slot("%s-closeMainWindow" % appString, self.slot_tidy)
        self.cfed = ConfigEd(self.settings)

        self.init()

    def init(self):
        self.gui = GuiWidget(self.settings)
        self.gui.show()
        self.app.init(self.gui)
        self.gui.setup()
        self.cfed.init(self.gui)

    def run(self):
        self.app.run()

    def slot_tidy(self, arg):
        """Stuff to do when the program quits
        """
        self.cfed.save()
        signal("ced_done")

    def getSourcePath(self):
        return self.cfed.sourcePath

    def getErrorCount(self):
        return self.cfed.errorCount


class MyTreeWidgetItem(QtGui.QTreeWidgetItem):
    def __init__(self, parent, text, path, itype, itip):
        QtGui.QTreeWidgetItem.__init__(self, parent,
                [QtCore.QString.fromUtf8(text)])
        self.xpath = path
        self.setToolTip(0, itip)
# Should the type be shown somehow?


class MyItemDelegate(QtGui.QItemDelegate):
    """A simple modification of the QItemDelegate class so that only
    column 1 (the second column!) is editable.
    """
    def __init__(self, parent = None):
        QtGui.QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        if index.column() != 1:
            return None
        return QtGui.QItemDelegate.createEditor(self, parent, option, index)


class GuiWidget(QtGui.QWidget):
    def __init__(self, settings):
        QtGui.QWidget.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.settings = settings

        self.ui = ui_form.Ui_Form()

    def setup(self):
        self.ui.tableWidget.setItemDelegate(MyItemDelegate(self.ui.tableWidget))
        self.ui.treeWidget.headerItem().setHidden(True)
        self.ui.tableWidget.setColumnWidth(0,150)

    def closeEvent(self, event):
        """Called when the window is closed. Do tidying up actions.
        """
        signal("%s-closeMainWindow" % self.settings.appString)
        event.accept()

    def addnode(self, parent, iname, path, itype, itip):
        """Add a node to the 'directory' tree.
        """
        if not parent:
            parent = self.ui.treeWidget
        return MyTreeWidgetItem(parent, iname, path, itype, itip)

    def clearTable(self):
        self.ui.tableWidget.clear()

    def clearTree(self):
        self.ui.treeWidget.clear()

    def setTitle(self, title):
        self.setWindowTitle(title)

    def setLabel(self, text):
        self.ui.label.setText(text)

    def setComment(self, text):
        self.enableText = False
        self.commentText = QtCore.QString.fromUtf8(text)
        self.ui.textEdit.setText(self.commentText)
        self.ui.textEdit.setEnabled(True)
        self.enableText = True

    def clearComment(self):
        self.enableText = False
        self.commentText = u''
        self.ui.textEdit.setEnabled(False)
        self.ui.textEdit.clear()

    def setValid(self, row, error):
        item = self.ui.tableWidget.topLevelItem(row)
        item.setToolTip(1, error)
        if error:
            item.setTextColor(1, QtCore.Qt.red)
        else:
            item.setTextColor(1, QtCore.Qt.black)

    def addBoolField(self, field, value, tip):
        # tip will be unicode, other args utf-8
        qf = QtCore.QString.fromUtf8(field)
        item = QtGui.QTreeWidgetItem([qf])
        item.setFlags(BASEITEMFLAGS | QtCore.Qt.ItemIsUserCheckable)
        self.ui.tableWidget.addTopLevelItem(item)
        if value and (value != "0"):
            item.setCheckState (1, QtCore.Qt.Checked)
        else:
            item.setCheckState (1, QtCore.Qt.Unchecked)
        item.setToolTip(0, tip)

    def addField(self, field, value, tip):
        # tip will be unicode, other args utf-8
        qf = QtCore.QString.fromUtf8(field)
        qv = QtCore.QString.fromUtf8(value)
        item = QtGui.QTreeWidgetItem([qf, qv])
        item.setFlags(BASEITEMFLAGS | QtCore.Qt.ItemIsEditable)
        self.ui.tableWidget.addTopLevelItem(item)
        item.setToolTip(0, tip)

    def setTreeNodeColours(self, tagDict):
        self.tagDict = tagDict
        self.colourNodes(self.ui.treeWidget.invisibleRootItem())

    def colourNodes(self, twi):
        for i in range(twi.childCount()):
            twic = twi.child(i)
            tag = self.tagDict[twic.xpath]
            if (tag == 0):
                twic.setTextColor(0, QtCore.Qt.black)
            elif (tag == 1):
                twic.setTextColor(0, QtCore.Qt.red)
            else:
                twic.setTextColor(0, QtCore.Qt.gray)
            self.colourNodes(twic)

    def deleteItem(self, item):
        """Delete the given item, and its children, recursively.
        """
        p = self.parent(item)
        p.removeChild(item)

    def currentItem(self):
        return self.ui.treeWidget.currentItem()

    def setCurrentItem(self, item):
        self.ui.treeWidget.setCurrentItem(item)

    def parent(self, item):
        cp = item.parent()
        if cp:
            return cp
        else:
            return self.ui.treeWidget.invisibleRootItem()

    def sort(self, item):
        """Used to reorder a level after a clone operation.
        """
        if not item:
            item = self.ui.treeWidget.invisibleRootItem()
        item.sortChildren(0, QtCore.Qt.AscendingOrder)


# 'Autoslots' (connections set up automatically)
# The quit button is connected using 'designer'.
#    @QtCore.pyqtSignature("")   # filters out the desired signal signature
#    def on_pushButton_Quit_clicked(self):
#        self.close()

    @QtCore.pyqtSignature("")
    def on_pushButton_switch_clicked(self):
        signal("ced_open", True)

    @QtCore.pyqtSignature("QTreeWidgetItem*, QTreeWidgetItem*")
    def on_treeWidget_currentItemChanged(self, newItem, oldItem):
        if newItem:
            signal("ced_newItem", newItem.xpath)

    @QtCore.pyqtSignature("QTreeWidgetItem*, QTreeWidgetItem*")
    def on_tableWidget_currentItemChanged(self, newItem, oldItem):
        index = self.ui.tableWidget.indexFromItem(newItem, 1)
        self.ui.tableWidget.setCurrentIndex(index)

    @QtCore.pyqtSignature("QTreeWidgetItem*, int")
    def on_tableWidget_itemChanged(self, item, column):
# This is maybe not the best way of distinguishing boolean values!
        if (item.flags() & QtCore.Qt.ItemIsUserCheckable):
            if (item.checkState(1) == QtCore.Qt.Checked):
                value = "1"
            else:
                value = "0"
        else:
            value = str(item.text(1).toUtf8())
        row = self.ui.tableWidget.indexOfTopLevelItem(item)
        signal("ced_edit", (row, value))

    @QtCore.pyqtSignature("")
    def on_pushButton_clone_clicked(self):
        signal("ced_clone")

    @QtCore.pyqtSignature("")
    def on_pushButton_delete_clicked(self):
        signal("ced_delete")

    @QtCore.pyqtSignature("")
    def on_textEdit_textChanged(self):
        if self.enableText:
            self.commentText = self.ui.textEdit.toPlainText()
            signal("ced_comment", str(self.commentText.toUtf8()))

    @QtCore.pyqtSignature("")
    def on_pushButton_pupils_clicked(self):
        signal("ced_pupils")

    @QtCore.pyqtSignature("")
    def on_pushButton_pix_clicked(self):
        signal("ced_pix")

    @QtCore.pyqtSignature("")
    def on_pushButton_save_clicked(self):
        signal("ced_tempsave")
