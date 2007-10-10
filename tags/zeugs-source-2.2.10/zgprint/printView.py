# -*- coding: UTF-8 -*-

#2007-09-15
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
"""This module deals with the report printer GUI.

Initially, when a database is loaded, the list of classes is
determined. These are then made available in the class combobox.

When a class is selected (by clicking with the mouse), an event is
generated indicating this. This event triggers the slot_newPrintClass
method which then determines which pupils are available, setting up
the pupil check-list.

When a database has been freshly loaded, the first class in the list
is selected by default.
"""
# Suffices to indicate which side of a sheet is referred to
FRONTSUFFIX = u"-0"
BACKSUFFIX = u"-1"

from layoutReport import LayoutReport
from print_backend import Printer
from guiDialogs import getDirectory
from database import DB, selectDBFile, getBoolean
import __builtin__

import os.path

class PrintView:
    """There may be only one instance of this class, because of the
    slot declarations.
    """
    def __init__(self):
        """Connect up signals to slots.
        """
        slot("classChanged", self.slot_newPrintClass)
        slot("openDB", self.slot_open)
        slot("individualPages", self.slot_individualPages)
        slot("singlePages", self.slot_singlePages)
        slot("multiPages", self.slot_multiPages)
        slot("preview", self.slot_preview)
        slot("print", self.slot_print)
        __builtin__.autoSpellCheck = False

    def init(self, gui, file):
        self.db = None          # indicates 'not initialized'
        self.gui = gui
        self.printer = None

        # Open a database and initialize the widgets
        if file:
            db = DB(file)
            if db.isOpen():
                db.init()
                self.open(db)
        else:
            self.slot_open(force=False)

    def slot_open(self, force):
        """Open a database file. If 'force' is not True try to get the
        last used one from the settings mechanism.
        """
        self.open(selectDBFile(self.gui.settings, force, dbSuffix=u"zgb"))

    def open(self, db):
        if db:
            self.db = db
            self.initialize()
            self.gui.showDbFile(self.db.descriptor)

    def initialize(self):
        """Set up the GUI from the information in the db.

        A list of available classes, self.classes is built and
        used to set up the class combobox.
        """
        # A list of class names, one for each class
        classes = [c.className for c in self.db.classes]

        # Set the entries in the class combo box
        self.gui.setClasses(classes)
        # That should cause a classChanged signal to be emitted (0 index)

    def slot_newPrintClass(self, i):
        """Act upon change of class.

        It renews the list of pupils in the pupilList.
        """
        if (i < 0): return

        # Set the current class
        classObject = self.db.classes[i]
        self.db.setClass(classObject, complete=True)

        # Get a list of pupil names, for the gui
        pupilList = [p[0] for p in classObject.orderedPupilList]
        # set pupil check-list:
        self.gui.setPupils(pupilList)

        layoutDict = self.db.layoutInfo.layoutDict

        # Get list of pages
        pages = layoutDict[u"document"].get(u"pages")
        if not pages:
            error(_("No 'pages' definition in layout section 'document'"))
        self.pages = pages.split()

        # Make a dictionary of sheet types: key is size name, value is
        # a list of sheet names.
        self.sheets = {}
        for s, sdict in layoutDict[u"sheets"].items():
            size = sdict[u"size"]
            slist = self.sheets.get(size)
            if slist:
                slist.append(s)
            else:
                self.sheets[size] = [s]

        # Make a dictionary associating sheet name and side (key) with
        # a list of (page, position) pairs (value).
        self.sheetSides = {}
        pagesDict = layoutDict[u"pages"]
        for p in self.pages:
            pinfo = pagesDict[p][u"_info_"]
            sheet = pinfo[u"sheet"]
            if getBoolean(pinfo, u"back"):
                sheet += BACKSUFFIX
            else:
                sheet += FRONTSUFFIX
            value = (p, int(pinfo[u"position"]))
            plist = self.sheetSides.get(sheet)
            if plist:
                plist.append(value)
            else:
                self.sheetSides[sheet] = [value]

        # Make lists according to sheet types. Only A4 and A3 are
        # supported at present - also the interface design rather
        # reflects this.
        self.multipages = self.getSides(u"A3")
        self.singlepages = self.getSides(u"A4")

        # cause the pages list to be set up
        self.gui.initPagesList()

    def getSides(self, size):
        sides = []
        ss = self.sheets.get(size)
        if ss:
            for s in self.sheets[size]:
                # Do we want the page names to appear too?
                sides.append(s + FRONTSUFFIX)
                sides.append(s + BACKSUFFIX)
            sides.sort()
        return sides

    def slot_individualPages(self, arg):
        self.gui.setPages(self.pages)

    def slot_singlePages(self, arg):
        self.gui.setPages(self.singlepages)

    def slot_multiPages(self, arg):
        self.gui.setPages(self.multipages)

    def slot_preview(self, arg):
        warning("Not Yet Implemented")

    def slot_print(self, arg):
        pupilList = self.db.classObject.orderedPupilList
        # individual, singlepage or multipage?
        pageType = self.gui.pageType()

        #   -- if multi, shrunk?
        shrink = self.gui.isShrink()

        #   -- if multi, landscape?
        landscape = self.gui.isLandscape()

        #   -- if reverse order printing?
        reverse = self.gui.isReverse()

        # Printer or pdf output?
        pdf = self.gui.isPdf()
        if pdf:
            # pdf needs a folder
            oldDir = self.gui.settings.getSetting("pdfDir")
            dir = getDirectory(_("pdf: folder for class folders"),
                    oldDir)
            if not dir: return
            self.gui.settings.setSetting("pdfDir", dir)
            # Check that the class folder exists
            cdir = os.path.join(dir, self.db.classObject.classTag)
            if not os.path.isdir(cdir):
                os.mkdir(cdir)

        loopCnt = len(pupilList)
        if reverse:             # pupil list index
            i = loopCnt - 1
        else:
            i = 0
        while (loopCnt > 0):
            pupilId = pupilList[i][1]
            if self.gui.isPupilChecked(i):
                self.message(_("Printing report for %1"),
                        (pupilList[i][0],))

                layout = LayoutReport(self.db, pupilId)

                if pdf:
                    # Generate a file name based on pupil id and
                    # page type
                    fileName = os.path.join(cdir, u"%s_%s.pdf" %
                            (pupilId, pageType))
                    self.message(u"  --> %s" % fileName)
                else:
                    fileName = None

                pages = self.gui.getPages()

                if (pageType == "multi"):
                    n = 2       # Only 2*A4 on A3 supported at the moment
                else:
                    n = 1

                printer = Printer(n, shrink, landscape, fileName)

                if reverse:
                    pages.reverse()

                first = True    # to control 'newPage'

                for p in pages: # or sheets

                    if p[1]:
                        page = p[0]

                        if not first:
                            printer.newPage()


                        if (pageType == "all"):
                            self.message(_("  --- page %s") % page)
                            pplist = [(page, 0)]
                        else:
                            self.message(_("  --- sheet %s") % page)
                            pplist = self.sheetSides[page]

                        for pageName, pos in pplist:
                            # find corresponding Page object
                            try:
                                ip = self.pages.index(pageName)
                            except:
                                error(_("No page with name '%1'"),
                                         (pageName,))
                            printer.render(layout.pages[ip].gScene, pos)

                        first = False

                printer.end()

            if reverse:
                i -= 1
            else:
                i += 1

            loopCnt -= 1

        self.message(_(" *** DONE ***"))

    def message(self, mtext, args=[]):
        # Substitute arguments
        text = argSub(mtext, args)
        self.gui.report(text)
