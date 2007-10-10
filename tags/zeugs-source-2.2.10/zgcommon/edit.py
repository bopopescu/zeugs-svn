# -*- coding: UTF-8 -*-

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
"""A simple specialized WYSIWIG text editor for Waldorf school reports.
It is also possible to use this editor in read-only mode for reviewing
reports.

The text is divided into word chunks which are then organized into
display lines, which are constrained to fit in frames  - so that the
text can be rendered to particular areas of a (printed) page.
Certain size parameters are defined in layout files incorporated into
the report database.
This module handles the general control logic. The lower level display
stuff is handled by a separate class (GView) and the actualhandling of
report texts is also separated out (in RSubject).
The cursor uses a (word, character-offset) pair to reference
a position in the text.
The text may be fetched from and stored to a very simple mark-up
format. A newline separates paragraphs and there are no multiple
spaces.
The only styling available is an alternative paragraph layout,
including a font and an indentation. This is signalled in the
mark-up format by a special paragraph prefix.
"""

# For undo: after how many character deletions the text will be saved
DELETECOUNT = 30

import types

from rsubject import TWord, TextLine, Paragraph
from curSel import Selection, EdCursor
from guiCanvas import BGRect, HLine, SHIFT
from guiBase import TextItem
from database import FixedSpace


class Editor:
    """There may be only one instance of this class, because of the
    slot declarations.

    Given a canvas widget to draw on, implement a report text editor.
    It can also be restricted to use in a view-only mode by passing
    'False' to the 'editable' argument.

    Much of the low level stuff is done in the 'graphics view' widget,
    which is a GUI class. I decided not to make this class inherit from
    that widget, in order to leave maximum flexibility in how it is
    created and implemented itself (I hope that makes sense).

    According to the settings in the layout description the area
    available for the report can comprise more than one 'frame'.
    The text can be split over a number of separate boxes - specifically
    here for the case of longer, principally class teacher, reports,
    which need more than one page). The editor needs the vertical sizes
    (in mm) of these boxes, so that the display area can be divided
    into several blocks which will appear sequentially, and also margin
    information.

    To deal with text that is too long for a report box, an additional
    large 'dummy' box is added after the 'official' box(es). This gets
    a coloured background, to indicate the overflow.

    The text being edited is primarily managed by the RSubject object,
    which stores it as a list of TextLine objects, each containing a
    list of TWord objects.
    """
    def __init__(self, canvas, editable=True):
        self.canvas = canvas        # the canvas widget
        self.editable = editable

        slot = canvas.slot
        slot("edPress", self.edPress)
        slot("edMove", self.edMove)
        slot("edRelease", self.edRelease)
        slot("keyPress", self.edKey)
        slot("renderedToEnd", self.renewOvfl)
        self.edCursor = None
        self.selection = None
        self.cursorX = None

    def init(self, rsubject):
        """Set up the editor for a new report.
        rsubject: A RSubject object for the current report.
        """
        self.rsubject = rsubject

        if self.edCursor:
            self.edCursor.stop()

        # Set the viewing area (x-margin, y-margin, width)
        self.mainWidth = self.rsubject.db.layoutInfo.mainWidth
        self.canvas.initArea(20, 10, self.mainWidth)

        # Special background for overflow text
        self.ovflRect = BGRect(self.canvas, "ovflbg", under=True)

        # Render the frames
        frames = self.rsubject.frames
        y = 0.0
        for f in frames[:-1]:
            # Separator line
            HLine(self.canvas, y, self.mainWidth)
            f.render(self.canvas, self.rsubject, y)
            y += f.maxHeight

        # The overflow frame:
        HLine(self.canvas, y, self.mainWidth)
        f = frames[-1]
        yo = 0.0
        ol = self.rsubject.getFrameLines(f)
        if ol:
            lastline = ol[-1]
            # vertical space needed by the frame text:
            yo = lastline.y + lastline.height
        f.getHeight(yo)
        f.render(self.canvas, self.rsubject, y)

        self.setSize(y, f.height)

        self.edCursor = EdCursor(self)

        self.selection = Selection(self)
        self.initCurSel()

    def initCurSel(self):
        # Convert cursor from index to word format
        cp, cw, cx = self.rsubject.cursor
        para = None
        ipara = -1
        for tl in self.rsubject.tlines:
            if (tl.para != para):
                ipara += 1
                para = tl.para
            if (ipara == cp):
                nw = len(tl.twords)
                if (cw < nw):
                    w = tl.twords[cw]
                    break
                cw -= nw
        self.edCursor.setPos(w, cx)

#        else:
#            self.edCursor.setPos(self.rsubject.tlines[0].twords[0], 0)

        self.selection.clearSelection()

    def setSize(self, y, h):
        """Set the size of the background rectangle behind the
        text overflow area and also the displayed canvas area.
        y: y-coordinate of overflow start
        h: height of overflow area
        """
        if (h <= 0.0):
            self.ovflRect.hide()
            self.canvas.setHeight(y)
        else:
            self.ovflRect.setRect(0, y, self.mainWidth, h)
            self.ovflRect.show()
            self.canvas.setHeight(y + h)

    def renewOvfl(self, arg):
        # This is a 'slot', called when a report has been rendered to
        # the end.
        f = self.rsubject.frames[-1]
        # How much space is used in the overflow area?
        lastLine = self.rsubject.tlines[-1]
        if (lastLine.frame != f):
            y = 0.0
        else:
            y = lastLine.y + lastLine.height
        self.setSize(f.yF, f.getHeight(y))

    def edKey(self, key):
        """This handles key presses.
        """
        # Any key press except cursor keys (?) causes the selection to be deleted!
        if isinstance(key, types.IntType):
            rawkey = (key & (SHIFT-1))
            if (rawkey in (1,2,3,4)):
                # First check for shift+cursor-key, because these alter the selection
                if (key & SHIFT):  # SHIFT + cursor key
                    # if there is not already a selection, set the first marker before
                    # moving the cursor
                    if not self.selection.selectionMark2:
                        w, cx = self.edCursor.getPos()
                        # Hack to handle empty words which are about to be deleted
                        if (w.string == u"") and (len(w.tline.twords) > 1):
                            # Don't start selection, just move cursor
                            self.cursorKey(rawkey)
                            return
                        self.selection.selectionMark = (w, cx)
                    self.cursorKey(rawkey)
                    self.selection.setMark2(self.edCursor.getPos())

                else:           # cursor key without SHIFT
                    # clear selection and move cursor.
                    self.selection.clearSelection()
                    self.cursorKey(rawkey)
                return

            # All other keys are ignored if this widget is read-only
            if not self.editable: return

            self.cursorX = None
            # If there is a selection this must be deleted
            if self.delete() and (rawkey in (8,9)): return

            # Get cursor position
            word, cx = self.edCursor.getPos()
            tline = word.tline

            if (rawkey == 10):      # space
                if (key & SHIFT):
                    self.insertChar(FixedSpace)
                    return
                s1 = word.string[:cx]
                s2 = word.string[cx:]
                word.setString(s1)
                # Create a new TWord with the second half of the split:
                nw = TWord(s2)
                wx = tline.twords.index(word)
                tline.insert(nw, wx+1)
                nw.setCanvas(self.canvas)

                # Re-render from this word, noting that it became shorter:
                self.rsubject.renderShortened(word)
                self.edCursor.setPos(nw, 0)
                return

            if (rawkey == 7):       # line break
                s1 = word.string[:cx]
                s2 = word.string[cx:]
                word.setString(s1)
                # Create a new TWord with the second half of the split:
                nw = TWord(s2)
                # And a new Paragraph, copying the properties of the old one:
                para = Paragraph(tline.para)
                # And a new TextLine:
                ntl = TextLine(para, [nw])
                lx = self.rsubject.tlines.index(tline) + 1
                self.rsubject.tlines.insert(lx, ntl)
                nw.setCanvas(self.canvas)
                # Move words following the split:
                wx = tline.twords.index(word)
                for w in tline.twords[wx+1:]:
                    ntl.insert(w)
                del(tline.twords[wx+1:])
                # Now move subsequent lines to new paragraph
                while True:
                    lx += 1
                    if (len(self.rsubject.tlines) <= lx) or \
                            (self.rsubject.tlines[lx].para != tline.para):
                        break
                    self.rsubject.tlines[lx].para = para

                # Re-render from this word, noting that it became shorter:
                self.rsubject.renderShortened(word)
                # Set cursor to start of new word.
                self.edCursor.setPos(nw, 0)
                return

            if (rawkey == 8) or (rawkey == 9):       # delete / backspace
                if (rawkey == 9):
                    # backspace: take one step back and then do as delete.
                    if (cx == 0): # at start of word
                        para0 = tline.para
                        # if stepping back works ...
                        if not self.edCursor.step(False): return
                        # Get new cursor position
                        word, cx = self.edCursor.getPos()
                        tline = word.tline
                        para = tline.para   # needed for deletion test below
                    else:
                        cx -= 1
                s = word.string
                if (len(s) == cx): # at end of word
                    # Join words
                    wx = tline.twords.index(word) + 1
                    if (wx >= len(tline.twords)): # at end of line
                        # If we arrived at the end of a paragraph with
                        # backspace, and the step backwards didn't skip
                        # to the previous paragraph, do nothing!
                        # That is necessary because of the
                        # automatic deletion of words which become empty
                        # when the cursor leaves them.
                        if (rawkey == 9) and (para == para0): return
                        # If at end of paragraph, join paragraphs
                        nl = self.rsubject.nextLine(tline)
                        if nl:
                            para0 = tline.para
                            para = nl.para
                            if (para != para0):
                                nl2 = nl
                                while True:
                                    nl2.setPara(para0)
                                    nl2 = self.rsubject.nextLine(nl2)
                                    if (not nl2) or (nl2.para != para): break
                            # Next line is (now) in same paragraph.
                            # Move first word of next line to current line:
                            tline.insert(nl.twords[0])
                            del(nl.twords[0])
                            if not nl.twords:
                                # Line now empty, delete it
                                self.rsubject.deleteTLine(nl)
                            else:
                                nl.y = None     # to ensure re-rendering
                        else:
                            # Nothing to delete
                            return

                    nw = tline.twords[wx]
                    del(tline.twords[wx])
                    word.setString(s + nw.string)
                    # The removed word must be 'freed'
                    nw.delete()
                    # Re-render from tline:
                    self.rsubject.linify(tline)
                else:
                    # Not at end of word, the word will be shortened.
                    s = s[:cx] + s[cx+1:]
                    word.setString(s)
                    # Re-render from this word, noting that it became shorter:
                    self.rsubject.renderShortened(word)
                # Reset cursor to start of new word/paragraph.
                self.edCursor.setPos(word, cx)

                self.deleteCount +=1
                if (self.deleteCount >= DELETECOUNT):
                    self.saveText()
                return

            # Anything else is ignored
            return

        # All other keys are ignored if this widget is read-only
        if not self.editable: return

        # character key
        self.cursorX = None
        # If there is a selection this must be deleted
        # This must also reset the cursor appropriately
        self.delete()
        self.insertChar(key)

    def insertChar(self, ch):
        """Insert the given character into the current word.
        """
        word, cx = self.edCursor.getPos()
        string = word.string[:cx] + ch + word.string[cx:]
        word.setString(string)
        # Re-render from tline:
        self.rsubject.linify(word.tline)
        self.edCursor.setPos(word, cx+1)

    def insertBlock(self, utext):
        """Insert the given (unicode) text at the current cursor position.
        Special style formatting will also be recognized but only after
        a newline.
        """
        self.saveText()

        self.selection.clearSelection()
        word, cx = self.edCursor.getPos()
        # Get cursor offset from end of word (for new cursor placement)
        cxn = len(word.string) - cx
        # Insert the new text at the cursor position ...
        string = word.string[:cx] + utext + word.string[cx:]
        textLines = self.rsubject.textToLines(string)
        tline = word.tline
        nline0 = textLines[0]
        word1 = nline0.twords[0]    # position to start rendering
        wx = tline.twords.index(word)   # insertion index
        # delete the word which was under the cursor
        word.delete()
        # and set its string to non-empty so that the cursor
        # repositioning works (!)
        word.string = u"DUMMY"
        # and add the rest of the original line to the end of the insertion
        oline2 = tline.twords[wx+1:]
        del(tline.twords[wx:])
        nlineL = textLines[-1]
        word = nlineL.twords[-1]        # get new word under cursor
        for w in oline2:
            nlineL.insert(w)
        # Append the first inserted line to tline
        for w in nline0.twords:
            tline.insert(w)

        # Insert the remaining lines into the subjects line list
        tlx = self.rsubject.tlines.index(tline) + 1
        self.rsubject.tlines[tlx:tlx] = textLines[1:]

        self.rsubject.renderShortened(word1)

        cx = len(word.string) - cxn
        self.edCursor.setPos(word, cx)

    def delete(self):
        """Delete the text between the two selection marks, if they are set,
        and place the cursor appropriately afterwards.
        Return True if something was deleted.
        """
        if not self.selection.isSelection(): return False

        # Save the current text
        self.saveText()

        sm1, sm2 = self.selection.order(self.selection.selectionMark,
                self.selection.selectionMark2)
        w1 = sm1[0]
        w2 = sm2[0]
        cx = sm1[1]
        self.edCursor.setPos(w1, cx)
        # Join words before and after selection
        w1.setString(w1.string[:cx] + w2.string[sm2[1]:])
        # Delete all intervening words, and w2
        tl1 = w1.tline
        wx1 = tl1.twords.index(w1)
        tl2 = w2.tline
        wx2 = tl2.twords.index(w2)
        if (tl1 == tl2):    # only delete from 1 line
            # delete words from wx1+1 to wx2 (incl.)
            for w in tl1.twords[wx1+1:wx2+1]:
                w.delete()
            del(tl1.twords[wx1+1:wx2+1])

        else:               # deletion block covers >1 line
            # delete words from wx1+1 to end of paragraph
            for w in tl1.twords[wx1+1:]:
                w.delete()
            del(tl1.twords[wx1+1:])
            # delete all the intervening lines
            while True:
                tl = self.rsubject.nextLine(tl1)
                if (tl == tl2): break
                self.rsubject.deleteTLine(tl)

            # Move remaining words after w2 in tl2 to end of tl1
            for w in tl2.twords[wx2+1:]:
                tl1.insert(w)
            del(tl2.twords[wx2+1:])
            # Delete tl2
            self.rsubject.deleteTLine(tl2)

        self.selection.clearSelection()

        self.rsubject.renderShortened(w1)

        self.edCursor.setPos(w1, cx)
        return True

    def getMarked(self):
        """Get the text between the two selection marks.
        This shares much of the same logic as the block delete function,
        but for the sake of clarity I decided to keep them separate.
        """
        if not self.selection.isSelection():
            return u""
        sm1, sm2 = self.selection.order(self.selection.selectionMark,
                self.selection.selectionMark2)
        w1 = sm1[0]
        w2 = sm2[0]
        cx1 = sm1[1]
        cx2 = sm2[1]
        if (w1 == w2):
            return w1.string[cx1:cx2]
        # Get the word fragments at the beginning and end of the selection
        snip1 = w1.string[cx1:]
        snip2 = w2.string[:cx2]
        tl1 = w1.tline
        wx1 = tl1.twords.index(w1)
        tl2 = w2.tline
        wx2 = tl2.twords.index(w2)
        # Start the text string with the format of the first line
        text = tl1.para.getFormat() + snip1
        # then get all intervening words
        if (tl1 == tl2):    # only 1 line is involved
            # get words from wx1+1 to wx2-1 (incl.)
            for w in tl1.twords[wx1+1:wx2]:
                text += u" " + w.string
            ch = u" "

        else:               # deletion block covers >1 line
            # get words from wx1+1 to end of paragraph
            for w in tl1.twords[wx1+1:]:
                text += u" " + w.string
            # get all the intervening lines
            while True:
                para = tl1.para
                tl1 = self.rsubject.nextLine(tl1)
                if (tl1.para == para):
                    text += u" "
                else:
                    text += u"\n" + tl1.para.getFormat()
                if (tl1 == tl2): break
                text += tl1.getText()

            ch = u""
            # Add the remaining words in tl2 up to w2-1
            for w in tl2.twords[:wx2]:
                text += ch + w.string
                ch = u" "

        # Add the fragment of the last marked word
        return text + ch + snip2

    def cursorKey(self, key):
        if (key in (1,2)):
            self.cursorX = None
            if (key == 1):  # left
                self.edCursor.step(False)
            else:           # right
                self.edCursor.step(True)
        else:
            if (self.cursorX == None):
                w, x = self.edCursor.getPos()
                self.cursorX = w.getXYH(x)[0]
            if (key == 3):  # up
                self.edCursor.lineStep(self.cursorX, True)
            else:           # down
                self.edCursor.lineStep(self.cursorX, False)


    # These event handlers are passed mm coordinates!
    def edPress(self, xy):
        # This also sets the cursor
        self.selection.setMark1(self.getPos(*xy))

    def edMove(self, xy):
        # This also sets the cursor
        self.selection.setMark2(self.getPos(*xy))

    def edRelease(self, xy):
        # Not so significant at the moment.
        # For cursor key up/down only:
        self.cursorX = None

    def getPos(self, x, y):
        """Get the nearest text position to the given (mm) coordinates.
        Return a (word, charIx) tuple.
        """
        # First find the TextLine
        tline = self.rsubject.tlines[0]
        for tl in self.rsubject.tlines:
            if (y < (tl.y + tl.frame.yF)): break
            tline = tl
        return self.getXPos(tline, x)

    def getXPos(self, tline, x):
        """Get the nearest text position to the given (mm) x-coordinate
        within the line 'tline'.
        Return a (word, charIx) tuple.
        """
        # Find the TWord object
        words = tline.twords
        j = 0   # word index
        imax = len(words) - 1
        for w in words:
            # Find out if the point is in this word -
            # need to include half the space width after the word, if there
            # is a following word.
            x0 = w.getX()
            x1 = x0 + w.getWidth()
            if (j == imax): break
            x2 = words[j+1].getX()
            spw = (x2 - x1)/2
            if (x < x1 + spw): break
            j += 1

        word = words[j]

        # Then the character
        xvec = word.getOffsets()

        k = 0
        if xvec:
            xo = x - x0     # xo is x relative to word start
            p0 = 0.0
            for p in xvec:
                p1 = xvec[k]
                if (xo < (p0 + p1)/2): break
                k += 1
                p0 = p1

        return (word, k)

    def saveText(self):
        """Called by various operations to keep backup versions of the
        text which can be reverted to using 'undo'.
        It is a rather primitive mechanism, but it should suffice for
        the foreseen purpose.
        """
        self.rsubject.saveOnChanged(self.edCursor.getPos())

        # Allows saving after a certain number of delete operations:
        self.deleteCount = 0

