# -*- coding: UTF-8 -*-

#2007-09-17
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

"""This module deals with the editor view GUI.
Only the reports for the teacher set in the db config table ('me')
are editable. Only these reports should be stored in the '.zga'
databse file.

The report selection is event driven. Initially, when a database is
loaded, the list of classes taught by the given teacher is determined.
These are then made available in the class combobox.

The first link in the event chain is the choice of class - either
programmatically (e.g. when a database is loaded it remembers which class
was last being edited and this is then restored) or else manually
(clicking with the mouse), by selecting a class from the list in the
class combobox. The fallback is to select the first class in the list.

Once a class has been selected, an event is generated indicating this.
This event triggers the slot_classChanged method which then determines
which subjects are available (for this class and the given teacher) in
the subject combobox.

If there was a previously selected subject, the attempt will be made
to return to this, otherwise the first in the list will be selected.
An event is then generated to signal a change of subject. This can also
be triggered by selecting a subject from the combobox using the mouse.

The subject-changed signal triggers the slot_subjectChanged method, which
determines which pupils are entered in the pupil combobox. Again, if
there was a previously selected pupil the attempt will be made to return
to this, otherwise the first in the list will be selected. An event is
generated to signal a change of pupil. This can also be triggered by
selecting a pupil from the combobox using the mouse. In addition,
next and previous buttons are provided for simple stepping between pupils
who are adjacent in the list.

The pupil-changed signal triggers the slot_pupilChanged method, which
first ensures that any previously open report is saved. Then the editor
display is cleared and set up according to the parameters for the new
report. The latest report text for this pupil/subect combination is then
loaded into the editor.
"""

# Should the validity of the reports be checked? (e.g. that they
# really do belong to the 'me' teacher).


from edit import Editor
from rsubjectx import RSubjectX as RSubject
from layoutUnits import LayoutUnits
from guiDialogs import getFile
from guiPdialog import printDialog
from database import selectDBFile, IndentStep, getReportVersion
from guiSync import GuiSync
import spellCheck

import __builtin__
import re
# For extracting the subject tag from the combined name/tag
reS = re.compile(u"\((.*)\)")

class EditorView:
    """There may be only one instance of this class, because of the
    slot declarations. At present there is no possibility of closing
    an editor and reopening it in the same process - also guiEditor.py
    and edit.py would need modifying.
    """
    def __init__(self, gui):
        """Connect up signals to slots and initialize the editor.
        """
        self.db = None          # indicates 'not initialized'
        self.gui = gui
        self.syncHandler = None # holds a GuiSync object, if used
        slot("classChanged", self.slot_classChanged)
        slot("subjectChanged", self.slot_subjectChanged)
        slot("pupilChanged", self.slot_pupilChanged)
        slot("previous", self.slot_previous)
        slot("next", self.slot_next)
        slot("copy", self.slot_copy)
        slot("cut", self.slot_cut)
        slot("paste", self.slot_paste)
        slot("style", self.slot_style)
        slot("indent", self.slot_indent)
        slot("openDB", self.slot_open)
        slot("sync", self.slot_sync)
        slot("undo", self.slot_undo)
        slot("redo", self.slot_redo)
        slot("textChanged", self.slot_clearRedo)
        slot("requestCheck", self.slot_requestCheck)
        slot("print", self.slot_printSubject)
        slot("checkSpelling", self.slot_checkSpelling)
        slot("endCheckSpelling", self.slot_endCheckSpelling)
        slot("nextUnfinished", self.slot_nextUnfinished)
        slot("currentStyle", self.gui.setStyleButton)
        self.canvas = gui.getGView()
        self.editor = Editor(self.canvas)
        spellCheck.spellInit()
        if (self.gui.settings.getSetting("autospellcheck") != "0"):
            self.gui.setAutoSpellCheck()
            __builtin__.autoSpellCheck = True
        slot("autospellcheck", self.slot_autospellcheck)

    def slot_sync(self, arg):
        """Synchronize the present database file with the main
        database.
        """
        if not self.db:
            warning(_("No database file open"))
            return

        self.slot_pupilChanged(-1)      # save current report
        filename = self.db.descriptor
        self.db.close()

        if self.syncHandler:
            self.syncHandler.init(filename)
        else:
            self.syncHandler = GuiSync("sync", filename)
        # The sync dialog needs to be modal!
        self.syncHandler.run()

        #When finished:
        self.slot_open(False)

    def slot_open(self, force):
        """Open a database file. If 'force' is not True try to get the
        last used one from the settings mechanism.
        Return True if successful.
        """
        if self.db:
            self.slot_pupilChanged(-1)      # save current report

        while True:
            db = selectDBFile(self.gui.settings, force)
            if db:
                # Clear revisions dictionary (for undo/redo)
                self.revisionDict = {}
                self.db = db
                try:
                    if self.initialize():
                        self.gui.showDbFile(self.db.descriptor)
                        # Show teacher's name
                        self.gui.showTeacher(self.db.getTeacherName(
                                self.db.owner))
                        return True
                except:
                    warning(_("Database file '%s' contains invalid data")
                            % self.db.descriptor)
                    force = True
                    self.db = None
                    continue
            break
        if self.db:
            return False
        signal("quit")

    def initialize(self):
        """Return True if successfully initialized.
        """
        # Initially there is no RSubject object (current report text)
        self.rsubject = None

        if not self.db.owner:
            warning(_("This is a main database - editing is not permitted"))
            return False

        # Adjust characters for spell-checking etc.
        extraChars = self.db.baseDict[u"extraChars"]
        if not (u"." in extraChars):
            extraChars = u"."
        extraLetters = extraChars.split(u"·")[0]
        checkSpelling.setReP(self.db.baseDict[u"dictionary"], extraLetters)
        self.gui.setExtraChars(extraChars.split(u".")[1])

        # Get lists of pupils for each of the subjects for each of
        # the classes - a nested dictionary structure
        self.reportData = self.db.getReportData()

        # Get a list of class object relevant to the 'owner'
        # First get a list of the class tags
        tclasses =  self.reportData.keys()
        # But that may be in the wrong order, so use self.db.classes
        # to sort them:
        self.classes = [c for c in self.db.classes if c.classTag in tclasses]

        # Set the entries in the class combo box
        # A list of class names is needed
        classNames = [c.className for c in self.classes]

        lastClass = self.db.getConfig(u"class")
        try:
            x = classNames.index(lastClass)
        except:
            x = 0
        self.disable = True
        self.gui.setClasses(classNames)
        # That should cause a classChanged signal to be emitted (0 index),
        # which will be ignored (self.disable)

        self.disable = False
        self.gui.setClass(x)
        # That should cause a classChanged signal to be emitted (index x)
        return True

    def slot_classChanged(self, i):
        """Act upon change of class.

        It renews the list of subjects in the subject comboBox,
        which causes a subjectChanged signal to be emitted.
        The config variable currentClass is set to the new name.

        If there was already a subject selected, try to return to
        the same one, otherwise the first in the list.
        """
        if self.disable or (i < 0): return
        self.slot_pupilChanged(-1)      # save current report

        # Set the current class
        self.currentClassObj = self.classes[i]
        self.db.setClass(self.currentClassObj)

        # Get subjects available for current class
        self.subjectsDict = self.reportData[self.currentClassObj.classTag]

        # Make an ordered list of subjects
        self.subjects = [u"%s (%s)" % (self.db.getSubjectName(s), s)
                for s in self.subjectsDict.keys()]
        self.subjects.sort()

        # Set the entries in the subject combo box
        try:
            x = self.subjects.index(self.db.getConfig(u"subject"))
        except:
            x = 0
        self.disable = True
        self.gui.setSubjects(self.subjects)
        # That should cause a subjectChanged signal to be emitted (0 index),
        # which will be ignored (self.disable)

        self.disable = False
        self.gui.setSubject(x)
        # That should cause a subjectChanged signal to be emitted (index x)

    def slot_subjectChanged(self, i):
        """Act upon change of subject.

        It renews the list of pupils in the comboBox_pupil, which causes
        a pupilChanged signal to be emitted.
        The config variable currentSubject is set to the new name.

        If there was already a pupil selected, try to return to the same one,
        otherwise the first in the list.
        """
        if self.disable or (i < 0): return
        self.slot_pupilChanged(-1)      # save current report

        self.currentSubjectNameId = self.subjects[i]

        # Extract the subject name and tag from self.currentSubjectNameId
        sName, sTag = self.currentSubjectNameId.rsplit(None, 1)
        self.subject = sTag.strip(u"()")

        # Get a list of pupils who take this subject
        pupiltags = self.subjectsDict[self.subject]

        # Order the list and get the names of the pupils for the display
        self.pupils = []        # a list of pupil tags
        self.pupilList = []     # a list of pupil names, for the gui
        for pname, ptag in self.currentClassObj.orderedPupilList:
            if ptag in pupiltags:
                self.pupils.append(ptag)
                self.pupilList.append(pname)

        # See if previously selected pupil is in list
        try:
            x = self.pupils.index(self.db.getConfig(u"pupilId"))
        except:
            x = 0

        # set pupil combobox list:
        self.disable = True
        self.gui.setPupils(self.pupilList)
        # That should cause a pupilChanged signal to be emitted (0 index),
        # which will be ignored (self.disable)

        self.disable = False
        self.gui.setPupil(x)
        # That should cause a pupilChanged signal to be emitted (index ix)

    def slot_pupilChanged(self, i):
        """Act upon change of pupil.

        If the edit-text has been modified, that is saved.
        The edit window is then cleared and the text for the new pupil
        is added.
        The config variable currentPupilId is set to the new id.
        """

        # Save old report text, if it has been modified!
        if self.rsubject:
            self.save()
            self.rsubject = None

        if (i < 0) or self.disable: return

        # Remember the index of the current pupil in the combobox for
        # the previous/next buttons
        self.pupilIx = i

        self.currentPupilId = self.pupils[i]
        self.db.setConfig(u"class", self.currentClassObj.className)
        self.db.setConfig(u"subject", self.currentSubjectNameId)
        self.db.setConfig(u"pupilId", self.currentPupilId)

        # Get an RSubject object for this report
        self.rsubject = RSubject(self.currentPupilId, self.subject,
                self.db, self.revisionDict)

        # Set up the editor
        self.editor.init(self.rsubject)

        # set the 'finished' state
        self.setFinishedButton(self.rsubject.isFinished())

        # initialize the undo/redo facility
        self.initUndo()

        # Give 'focus' to the editor, so that it receives keyboard input.
        self.gui.focusEditor()

    def save(self):
        """If the report has been changed, save the new version to
        the database.
        """
        self.editor.saveText()

    def slot_previous(self, arg):
        """Handler for 'previous pupil' button
        """
        if (self.pupilIx == 0):
            # Give 'focus' back to the editor.
            self.gui.focusEditor()
            return
        self.gui.setPupil(self.pupilIx - 1)
        # That should cause a pupilChanged signal to be emitted

    def slot_next(self, arg):
        """Handler for 'next pupil' button
        """
        ix = self.pupilIx + 1
        if (ix >= len(self.pupils)):
            # Give 'focus' back to the editor.
            self.gui.focusEditor()
            return
        self.gui.setPupil(ix)

    def slot_copy(self, arg):
        """Handler for 'copy' action
        """
        text = self.editor.getMarked()
        ###print "COPY $%s$" % text
        self.gui.setClipboard(text)

    def slot_cut(self, arg):
        """Handler for 'cut' action
        """
        self.slot_copy(None)
        self.editor.delete()

    def slot_paste(self, arg):
        """Handler for 'paste' action
        """
        # Get text and insert as block
        self.editor.insertBlock(self.gui.getClipboard())

    def slot_style(self, style):
        """Handler for 'style' action - change style:
        u"n"/normal, u"l"/special, u"r"/special/right-aligned
        """
        selection = self.editor.selection
        if selection.isSelection():
            sm1, sm2 = selection.order()
            tl = sm1[0].tline   # first selected line
            self.rsubject.restyle(tl, sm2[0].tline.para, style)
            selection.markSelection()
        else:
            word, cx = self.editor.edCursor.getPos()
            tl =  word.tline
            self.rsubject.restyle(tl, tl.para, style)
            self.editor.edCursor.setPos(word, cx)

    def slot_indent(self, arg):
        """Handler for 'indent' action - only valid in special style.
        Change the indentation of a 'special' line.
        If there is a selection and the first line is 'special, all
        selected lines with the same alignement will get the same
        indentation as the first.
        If the first line is not special, the command will be ignored.
        """
        if arg:
            step = IndentStep
        else:
            step = -IndentStep

        mainWidth = self.rsubject.db.layoutInfo.mainWidth
        selection = self.editor.selection
        if selection.isSelection():
            sm1, sm2 = selection.order()
            # First selected paragraph
            tl = sm1[0].tline
            p = tl.para
            if (p.align == u"n"): return
            if (step > 0) and (p.indent >= mainWidth/3): return
            p.indent += step
            if (p.indent < 0.0): p.indent = 0.0

            # Repeat for all selected lines
            while (tl != sm2[0].tline):
                tl = self.rsubject.nextLine(tl)
                tl.y = None         # to ensure re-rendering
                if (tl.para.align == p.align):
                    tl.para.indent = p.indent
            self.rsubject.linify(sm1[0].tline)
            selection.markSelection()
        else:
            word, cx = self.editor.edCursor.getPos()
            p = word.tline.para
            if (p.align == u"n"): return
            if (step > 0) and (p.indent >= mainWidth/3): return
            p.indent += step
            if (p.indent < 0.0): p.indent = 0.0
            self.rsubject.linify(word.tline)
            self.editor.edCursor.setPos(word, cx)

    def slot_undo(self, arg):
        if (self.undoLevel == 0):
            # Save the current text
            self.save()
        self.undoLevel += 1
        self.setFinishedButton(self.rsubject.undo(self.undoLevel))
        self.editor.initCurSel()
        if (self.rsubject.nVersions() <= (self.undoLevel+1)):
            self.gui.enableUndo(False)
        self.gui.enableRedo(True)

    def slot_redo(self, arg):
        self.undoLevel -= 1
        if (self.undoLevel == 0):
            self.gui.enableRedo(False)
        self.setFinishedButton(self.rsubject.undo(self.undoLevel))
        self.editor.initCurSel()
        self.gui.enableUndo(True)

    def initUndo(self):
        """Initialize the undo/redo mechanism.
        """
        self.undoLevel = 0
        self.gui.enableRedo(False)
        self.gui.enableUndo(self.rsubject.nVersions() > 1)
        # Counter for delete operations:
        self.editor.deleteCount = 0

    def slot_clearRedo(self, arg):
        """Called when the text has been altered, thus making a 'redo'
        impossible.
        """
        if (self.undoLevel != 0):
            self.undoLevel = 0
            self.gui.enableRedo(False)
        self.gui.enableUndo(True)

    def setFinishedButton(self, down):
        # A flag (self.finishedButtonDisable) is kept to stop a vicious circle!
        self.finishedButtonDisable = True
        self.gui.activateFinished(down)
        self.finishedButtonDisable = False
        if down:
            self.checkFlag = "on"
        else:
            self.checkFlag = "off"
        self.gui.setFinished(self.checkFlag)

    def slot_requestCheck(self, down):
        if self.finishedButtonDisable: return

        self.setFinishedButton(down)
        self.rsubject.setFinished(down, self.editor.edCursor.getPos())

    def slot_printSubject(self, arg):
        """Use class LayoutUnits to format the reports for all pupils
        in the present class taking this subject, then present a
        print dialog.
        """
        # Save current report
        self.slot_pupilChanged(-1)
        # Restore current report
        self.slot_pupilChanged(self.pupilIx)

        asc = autoSpellCheck
        if asc:
            __builtin__.autoSpellCheck = False

        if arg:
            plist = [self.currentPupilId]
        else:
            plist = self.pupils

        lu = LayoutUnits(self.db, self.subject, plist)

        if asc:
            __builtin__.autoSpellCheck = True

        npages = len(lu.pages)
        if not npages:
            warning(_("No pages to print"))
            return
        dlg = printDialog(npages)
        if not dlg: return

        start = dlg.start()
        end = dlg.end()
        if (start > end): return

        even = dlg.even()
        odd = dlg.odd()

        pages = []
        for i in range(start, end+1):
            if (i % 2):
                if odd:
                    pages.append(i)
            elif even:
                pages.append(i)

        if dlg.reverse():
            pages.reverse()

        if dlg.toPdf():
            pdfFile = getFile(_("Print to pdf-file"),
                    startFile=u"print.pdf",
                    defaultSuffix=u"pdf",
                    filter=(_("pdf Files"), (u"*.pdf",)),
                    create=True)
            if pdfFile:
                lu.printout(pdfFile, pages)
        else:
            lu.printout(None, pages)

    def slot_autospellcheck(self, on):
        __builtin__.autoSpellCheck = on
        if on:
            val = "1"
        else:
            val = "0"
        self.gui.settings.setSetting("autospellcheck", val)
        # spellcheck all words
        if self.rsubject.tlines:
            for tl in self.rsubject.tlines:
                for w in tl.twords:
                    if on:
                        w.spellCheck()
                    else:
                        w.spellUncheck()

    def slot_checkSpelling(self, arg):
        checkSpell.start(self.rsubject.tlines)

    def slot_endCheckSpelling(self, arg):
        if checkSpell.altered:
            self.rsubject.setText(checkSpell.text)
            self.rsubject.cursor = (0, 0, 0)
            self.editor.initCurSel()
            signal("textChanged")

    def slot_nextUnfinished(self, arg):
        ix = self.pupilIx
        while True:
            ix += 1
            if (ix >= len(self.pupils)):
                ix = 0
            if (ix == self.pupilIx):
                # None found
                return

            pupilId = self.pupils[ix]
            key = u"%s+%s" % (pupilId, self.subject)
            revisions = self.revisionDict.get(key)

            if revisions:
                report, cursor = revisions[-1]
            else:
                report = self.db.getReport(pupilId, self.subject)
                cursor = (0,0,0)
                revisions = [(report, cursor)]
                self.revisionDict[key] = revisions

            if not getReportVersion(report).endswith(u"$"):
                break

        self.gui.setPupil(ix)
