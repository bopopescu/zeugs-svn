#2007-06-25
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
"""Cursor and Selection handling.
"""

from guiCanvas import BGRect, CursorLine, Timer

# Cursor
cursorOnTime = 500
cursorOffTime = 300
class EdCursor:
    """The cursor marks a particular Word object and a particular
    character position within that word.
    """
    def __init__(self, editor):
        self.editor = editor
        self.cursorItem = CursorLine(editor.canvas)
        self.timer = Timer(self.timerEvent)
        self.shown = True
        self.word = None
        self.charIx = 0
        self.timer.count(cursorOnTime)

    def stop(self):
        """Stop the counter
        """
        self.timer.stop()

    def timerEvent(self):
        if self.shown:
            self.cursorItem.hide()
            self.timer.count(cursorOnTime)
            self.shown = False
        else:
            self.cursorItem.show()
            self.timer.count(cursorOffTime)
            self.shown = True

    def setPos(self, word, cx):
        """Set the cursor to a particular word/character.
        It also forces the cursor to be in 'shown' state.
        """
        # Special case: when leaving an empty word that is not the single
        # word of an empty paragraph, that word should be deleted.
        if (self.word != word) and self.word and \
            (self.word.string == u"") and self.word.tline:
            wList = self.word.tline.twords
            if (len(wList) > 1):
                ix = wList.index(self.word)
                t = self.word.tline
                self.word.delete()
                del(wList[ix])
                self.editor.rsubject.renderShortened(wList[0])
        self.word = word
        self.charIx = cx
        # Get editor view coordinates
        x, y, h = word.getXYH(cx)
        self.cursorItem.set(x, y, h)
        # Force cursor shown
        self.shown = False      # so that the next switch is to 'shown'
        self.cursorItem.show()
        self.editor.canvas.ensureVisible(self.cursorItem, 10)

        # Set gui 'style' buttons according to paragraph style
#NOTE: I hope this is the only place where this must be done!
        self.editor.canvas.signal("currentStyle", self.word.tline.para.align)

    def getPos(self):
        """Return cursor position as (word, charIx) pair.
        """
        return (self.word, self.charIx)

    def step(self, forward):
        """Move the cursor one character position.
        """
        w = self.word
        if forward:
            c = self.charIx + 1
            if (c > len(w.string)):
                # Move to next word
                wList = w.tline.twords
                wx = wList.index(w) + 1
                if (wx >= len(wList)):
                    # Move to next line
                    tl = self.editor.rsubject.nextLine(w.tline)
                    if not tl: return False
                    w = tl.twords[0]
                else:
                    w = wList[wx]
                c = 0
        else:
            # backward
            c = self.charIx - 1
            if (c < 0):
                # Move to previous word
                wList = w.tline.twords
                wx = wList.index(w) - 1
                if (wx < 0):
                    # Move to previous line
                    tl = self.editor.rsubject.previousLine(w.tline)
                    if not tl: return False
                    w = tl.twords[-1]
                else:
                    w = wList[wx]
                c = len(w.string)

        self.setPos(w, c)
        return True

    def lineStep(self, x, up):
        """Move the cursor up or down a line.
        It tries to retain the x-coordinate.
        """
        if up:
            # Go to previous line
            tl = self.editor.rsubject.previousLine(self.word.tline)
            if not tl: return

        else:
            # Go to next line
            tl = self.editor.rsubject.nextLine(self.word.tline)
            if not tl: return

        w, c = self.editor.getXPos(tl, x)
        self.setPos(w, c)


class Selection:
    """This class represents a text selection within an 'editor'.

    There are two markers, selectionMark and selectionMark2, the first being
    set by left-cursor-press, the second by left-cursor-move. Their values are
    index triples (line, word, character), and become invalid when the text is
    edited - so any editing action must clear them.
    """
    def __init__(self, editor):
        # There are 3 rectangles for marking selection, 1st line, middle lines
        # and last line.
        self.editor = editor
        view = self.editor.canvas
        self.selRect1 = BGRect(view, "selbg")
        self.selRect2 = BGRect(view, "selbg")
        self.selRect3 = BGRect(view, "selbg")
        self.mainWidth = self.editor.rsubject.db.layoutInfo.mainWidth

    def clearSelection(self):
        # The defining property of a clear selection is that selectiomMark2
        # is 'None'. selectionMark need not be 'None'
        self.selectionMark2 = None
        self.selRect1.hide()
        self.selRect2.hide()
        self.selRect3.hide()

    def isSelection(self):
        return (self.selectionMark2 != None)

    def setMark1(self, newMark):
        """Called when the left mouse button is pressed.
        """
        self.selectionMark = newMark
        self.clearSelection()
        self.editor.edCursor.setPos(*newMark)

    def setMark2(self, newMark):
        """Called when the mouse is moved with the left button pressed.
        """
        if (self.selectionMark2 == newMark): return
        self.selectionMark2 = newMark
        self.markSelection()

    def markSelection(self):
        """Sets the coloured background for the selection.
        It also resets the (display) cursor position.
        """
        self.editor.edCursor.setPos(*self.selectionMark2)
        if (self.selectionMark2 == self.selectionMark):
            self.selRect1.hide()
            self.selRect2.hide()
            self.selRect3.hide()
            return

        sm1, sm2 = self.order()
        w, cx = sm1
        x1, y1, dy1 = w.getXYH(cx)
        w, cx = sm2
        x2, y2, dy2 = w.getXYH(cx)

        if (y1 == y2):
            # single line, 1 rectangle, sm1 to sm2
            self.selRect1.setRect(x1, y1, x2-x1, dy1)
            self.selRect1.show()
            self.selRect2.hide()
            self.selRect3.hide()
            return

        # selRect1: from sm1 to end of line
        # selRect2: from start of line to sm2
        self.selRect1.setRect(x1, y1, self.mainWidth-x1, dy1)
        self.selRect1.show()
        self.selRect2.setRect(0, y2, x2, dy2)
        self.selRect2.show()

        y0 = y1+dy1
        if (y0 == y2):
            # adjacent lines, 2 rectangles
            self.selRect3.hide()
            return

        # several lines, all 3 rectangles
        # selRect3: all lines in between
        self.selRect3.setRect(0, y0, self.mainWidth, y2-y0)
        self.selRect3.show()

    def order(self, mark1=None, mark2=None):
        """Return the two marks as a tuple so that the first entry
        is guaranteed not to be after the second. The default marks
        are the current selection markers.
        """
        if not mark1: mark1 = self.selectionMark
        if not mark2: mark2 = self.selectionMark2
        w1 = mark1[0]
        w2 = mark2[0]
        if (w1 == w2):
            # compare character positions
            if (mark1[1] > mark2[1]):
                return (mark2, mark1)
            return (mark1, mark2)
        tl1 = w1.tline
        tl2 = w2.tline
        if (tl1 != tl2):
            tls = self.editor.rsubject.tlines
            if (tls.index(tl1) > tls.index(tl2)):
                return (mark2, mark1)
            return (mark1, mark2)
        if (tl1.twords.index(w1) > tl1.twords.index(w2)):
            return (mark2, mark1)
        return (mark1, mark2)
