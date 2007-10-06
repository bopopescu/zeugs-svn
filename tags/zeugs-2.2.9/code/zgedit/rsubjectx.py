# -*- coding: UTF-8 -*-

#2007-08-23
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
UNDOMAX = 10

from rsubject import RSubject
from database import getReportText, getReportVersion

class RSubjectX(RSubject):
    """An extension of RSubject for the editor.
    """
    def __init__(self, pupilId, subject, db, revisions=None):
        """pupilId: id field of the pupil's database record
        subject: subject tag
        db: database.DB object
        revisions: dictionary of revision lists (editor only)

        Note that concurrent editing of a database file will probably
        make a mess of it - the revisions mechanism ignores any changes
        made externally.
        """
        # self.revisions will be the list of revisions for this report
        self.key = u"%s+%s+%s" % (db.classObject.classTag, pupilId, subject)
        if (revisions == None):
            # For printing from the editor
            self.report = db.getReport(pupilId, subject)

        else:
            self.revisions = revisions.get(self.key)

            if self.revisions:
                self.report, self.cursor = self.revisions[-1]
            else:
                self.report = db.getReport(pupilId, subject)
                self.cursor = (0,0,0)
                self.revisions = [(self.report, self.cursor)]
                revisions[self.key] = self.revisions

        RSubject.__init__(self, pupilId, subject, db)

    def getReportInfo(self):
        """This version replaces the printer version.
        """
        self.printMode = False
        # The editor only handles a single teacher at a time
        # The teacher's tag
        self.teacher = self.db.owner

    def undo(self, level):
        """Set the text to a different historical version, from the
        self.revisions list, level being the index (the most recent is
        level 0).
        The 'textChanged' signal is suppressed so that the button
        enabling can work properly.
         => True if report marked as 'finished'
        """
        version = self.revisions[-1 - level]
        self.report, self.cursor = version
        self.setText(getReportText(self.report))
        return getReportVersion(self.report).endswith(u"$")

    def nVersions(self):
        """How many versions of this report are available?
        """
        return len(self.revisions)

    def setFinished(self, on, cursor):
        """Set the 'finished' state for this report.
        If that means a change, the report must be saved.
        """
        if (on == self.isFinished()):
            return
        self.saveOnChanged(cursor, on)
        signal("textChanged")

    def saveOnChanged(self, cursor, finishedFlag=None):
        """If the text has changed since the last recorded revision,
        save the new version and add it to the revisions list. If
        'finishedFlag' != None, force a save.
        finishedFlag = None, keep as at present
                     = False, set to off
                     = True, set to on
         => True if saved
        """
        lastSaved = self.revisions[-1][0]   # don't need the old cursor
        utext, ci = self.getText(cursor)

        if (finishedFlag == None):
            finishedFlag = self.isFinished()
            if (utext == getReportText(lastSaved)):
                return False

        revN = self.db.getTime()
        if finishedFlag:
            # If the report is flagged as 'finished'
            revN += u"$"

        self.report = self.db.saveReport(self.pupilId, self.subject,
                utext, revN)

        # Save to revisions list
        self.revisions.append((self.report, ci))
        while (len(self.revisions) > UNDOMAX):
            # Delete the second oldest in the list, thus always
            # keeping the initially loaded version.
            del(self.revisions[1])

        return True

    def getText(self, cursor=(None, 0)):
        """Convert the RSubject object into text form, for saving in
        the database. Generate format prefixes as necessary. It also
        returns the cursor position as a triple:
            (paragraph index, word index, character index)
        cursor is a pair: the TWord object for the word containing the
        cursor and character index of the cursor within that word.
         => (text, index-cursor)
        """
        # First convert the lines into paragraphs. Then output each line
        # as text.
        para = None
        paras = []              # list of paragraphs
        for tl in self.tlines:

            if (tl.para != para):
                if para:
                    paras.append(pwords)

                para = tl.para
                pwords = list(tl.twords)
            else:
                pwords += list(tl.twords)

        paras.append(pwords)

        ipara = -1              # paragraph index, for cursor location
        cword, cx = cursor
        cp, cw = 0, 0           # paragraph and word indexes for cursor
        text = u""
        for pwords in paras:
            ipara += 1

            text += pwords[0].tline.para.getFormat()
            # Add the words from this paragraph
            ch = u""
            iword = 0   # word index, for cursor location
            for w in pwords:
                # Seek cursor
                if (w == cword):
                    cp = ipara
                    cw = iword
                    # Hack for temporary empty words
                    if (not w.string) and (cw != 0) and (pwords[-1] == w):
                        cw -= 1
                        cx = len(pwords[-2].string)

                # Ignore empty words
                if w.string:
                    iword += 1
                    text += ch + w.string
                    ch = u" "
            text += u"\n"

        return (text, (cp, cw, cx))

    def previousLine(self, tline):
        """Get previous line.
        """
        lx = self.tlines.index(tline)
        if (lx == 0): return None
        return self.tlines[lx - 1]

    def nextLine(self, tline):
        """Get next line.
        """
        lx = self.tlines.index(tline) + 1
        if (len(self.tlines) <= lx): return None
        return self.tlines[lx]

    def deleteTLine(self, tline):
        """Delete the given line, including any words it contains.
        """
        for w in tline.twords:
            w.delete()
        self.tlines.remove(tline)

    def renderShortened(self, word):
        """Rearrange the layout from the given word, which has become
        shorter, so if it is the first word of a line, which is not
        the first of a paragraph, the linification must start from
        the previous line.
        """
        tline = word.tline
        if (tline.twords.index(word) == 0):
            pl = self.previousLine(tline)
            if pl:
                tline.y = None      # mark for reformatting
                tline = pl

        # Render the text from this line:
        self.linify(tline)

    def restyle(self, tline, endPara, style):
        """Change the style of one or more paragraphs.
        tline: a line (not necessarily the first) of the first paragraph
        endPara: the last paragraph
        style: u"n", u"l" or u"r"
        """
        p0 = tline.para
        # Must start from beginning of paragraph
        if (p0.align == u"n"):
            # Only 'normal' paragraphs can have multiple lines
            while True:
                tlp = self.previousLine(tline)
                if (not tlp) or (tlp.para != p0): break
                tline = tlp

        # Remember the first word, as start point for re-rendering
        w0 = tline.twords[0]

        # The frame and y-offset of the first line are needed for re-rendering
        #NOTE: If a text line at a frame boundary is restyled, it is possible
        #  for it to end up in the wrong frame (if the new style takes less
        #  height than the old, and the starting point is determined from
        #  the old line). By taking frame and y from the previous line
        #  (if any) this is avoided.
        pl = self.previousLine(tline)
        if pl:
            frame = pl.frame
            y = pl.y + pl.height
        else:
            frame = tline.frame
            y = tline.y

        # Now go through rebuilding the lines in the selected paragraphs
        while True:     #loop over paragraphs
            newTL = Paragraph().textlineFromAlign(self, style)
            self.tlines.insert(self.tlines.index(tline), newTL)

            while True:     # loop over TLines
                for w in tline.twords:
                    newTL.insert(w)
                tln = self.nextLine(tline)
                self.tlines.remove(tline)
                tline = tln
                if (not tln) or (tln.para != p0):
                    break

            if (p0 == endPara):
                break
            p0 = tln.para

        tl = w0.tline
        tl.frame = frame
        tl.y = y
        self.linify(tl)
