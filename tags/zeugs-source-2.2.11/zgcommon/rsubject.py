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
SPELLTHICKNESS = 0.5

from database import getBoolean, FixedSpace, getReportText, getReportVersion
from guiBase import TextItem, LineH, colours, Image

import re


class RSubject:
    """Manages / encapsulates a report for a single subject and pupil.
    That includes the laying out in lines and frames.
    """
    def __init__(self, pupilId, subject, db):
        """pupilId: id field of the pupil's database record
        subject: subject tag
        db: database.DB object
        """
        self.db = db
        self.pupilId = pupilId
        self.subject = subject

        self.tlines = None

        self.getReportInfo()

        # Get the frame information as a list of TextFrame objects
        self.frames = []
        i = 0           # The frames are indexed
        for n in self.db.getFrames(self.subject):
            self.frames.append(TextFrame(self.db, n, i, self.subject))
            i += 1
        if not self.printMode:
            self.frames.append(TextFrame(self.db, u"overflowFrame", i,
                    self.subject))

        if self.report:
            self.setText(getReportText(self.report))

    def getReportInfo(self):
        """This version is for the printer only.
        """
        self.printMode = True
        # Get the saved text for this report.
        self.report = self.db.getReport(self.pupilId, self.subject)
        if not self.report:
            # i.e. if the pupil doesn't take this subject
            self.teacher = None
            return

        # The teacher's tag
        self.teacher = self.db.getReportTeacher(self.pupilId, self.subject)

    def setText(self, utext):
        """Read the text into a list of TextLine objects, one for each
        paragraph. If the frames have already been set up with canvases
        (i.e. not on the first run through) the text will also be
        rendered to the canvas(es).
        A 'textChanged' signal is not generated!
        """
        # If an old text is being replaced, delete the TWord objects.
        if self.tlines:
            for tl in self.tlines:
                for w in tl.twords:
                    w.delete()
        self.tlines = self.textToLines(utext)

        # Arrange the lines within the available frames:
        self.linify(suppress=True)

    def linify(self, tline=None, suppress=False):
        """Arrange text lines within the frames for the subject.
        tline is the first line in self.tlines to adjust. If it is
        not supplied the process starts from the first line.
        Stop when a line is found that is already correctly placed.
        The TWord objects are added to TextLine objects up to the
        available line width.
        In the case of justified text (the default), each line gets a
        calculated width for the spaces between words, otherwise the
        default width for the font is taken. The initial
        indentation for each line is also saved for later reference.
        This method only deals with arranging the words in lines - it
        doesn't concern itself with actual placement of these lines
        and words on a canvas.

        If the text has also been rendered to a canvas, a 'textChanged'
        signal will be emitted at the end, unless 'suppress' is True.
        """
        if tline:
            tlineIx = self.tlines.index(tline)
        else:
            tlineIx = 0
            tline = self.tlines[0]

        # Is the line the first in a paragraph?
        para = tline.para
        paraLine1 = True
        if (tlineIx > 0) and (self.tlines[tlineIx - 1].para == para):
            paraLine1 = False

        y = tline.y
        frame = tline.frame
        if not frame:
            if (tlineIx == 0):
                frame = self.frames[0]
                y = 0.0
            else:
                bug("RSubject.linify: line has no frame:\n  %s" %
                        tline.getText())

        # Maximum width available for text body:
        lineWidth = self.db.layoutInfo.lineWidth
        # Extra indentation for first line of (normal) paragraph:
        indent1 = self.db.layoutInfo.indent1
        # Justify unless turned off in layout
        nojustify = self.db.layoutInfo.nojustify

        lx = tlineIx + 1        # index for reading lines from self.tlines
        ntlines = []            # list of newly arranged lines

        wo = tline.twords[0]    # first word in line
        wx = 1                  # index of next word in line
        # To ensure that this first line gets recreated:
        tline.frame = None

        # Loop over new TLine objects:
        while True:
            # If there is space for the next line in the current frame
            # get the y-position, x-start and width-reduction.
            # Otherwise 'None'.
            # Pass in the desired y-position and the line height.
            yl1 = frame.addLine(y, tline.height)
            if yl1:
                y, line1 = yl1

            else:
                # Move on to next frame
                try:
                    frame = self.frames[self.frames.index(frame) + 1]
                except:
                    warning(_("No frames left for text:\n   %1"),
                            (tline.getText(),))
                    break
                y, line1 = frame.addLine(0.0, tline.height)

            # Check whether subsequent lines can be left as they are:
            if (frame == tline.frame) and (y == tline.y) and (wx == 1):
                lx -= 1
                break

            # nW is the accumulated width of the new line as it
            # is built.
            nW = 0.0

            # First get initial indentation
            lx0 = para.indent
            if line1:
                lx0 += frame.line1indent()

            multiline = (para.align == u"n")
            if multiline:
                # extra indentation for first line in paragraph:
                if paraLine1:
                    paraLine1 = False
                    lx0 += indent1
                    nW += indent1

            tl = TextLine(para)     # create new TLine instance
            ntlines.append(tl)      # add to list of new TLines
            tl.x0 = lx0             # save line indentation
            tl.y = y                # and line vertical offset
            tl.frame = frame        # set line's frame
            nW += wo.getWidth()
            sp =  para.font.spWidth # (default) space width

            while True:             # loop over words in (output) line
                tl.insert(wo)       # add word to line

                # Get next word:
                if (wx < len(tline.twords)):
                    wo = tline.twords[wx]   # get next word from current line
                    wx += 1
                elif (lx < len(self.tlines)):
                    tline = self.tlines[lx] # switch to next input line
                    lx += 1
                    wo = tline.twords[0]
                    wx = 1
                    # New paragraph?
                    if (tline.para != para):
                        para = tline.para
                        paraLine1 = True
                        break
                else:                   # no words left in report
                    wo = None
                    break

                newW = nW + sp + wo.getWidth()
                if (newW > lineWidth):
                    # Not all words were used, so a new line is needed
                    if multiline:
                        if not nojustify:
                            # Justify the current line by stretching the spaces
                            spaces = len(tl.twords) - 1
                            if (spaces > 0):
                                sp += (lineWidth - nW) / spaces
                        break
                    else:
#TODO?: Overlong special lines are just passed as is. Is that ok?
                        pass
                nW = newW
            #endwhile - TWords allocated to new TextLine

            tl.spaceWidth = sp      # set spacing for this line
            # If the frame has already been set up with a canvas
            # render the new line:
            if frame.canvas:
                tl.render()

            if not wo:        # end of report, no words left
                break

            y += tl.height      # increment y-coordinate

        #endwhile - all new lines now available

        # Replace rearranged lines
        self.tlines[tlineIx:lx] = ntlines

        if frame.canvas:
            if (not wo):
                # Rendered to end of report, frames might need adjusting
                # For readjusting the view in the editor
                frame.canvas.signal("renderedToEnd")

                lfix = frame.index
                if (frame.lastFrame != lfix):
                    for f in self.frames:
                        # Renew the rendering, passing the current
                        # last frame index and its text extent
                        f.renew(lfix)

                frame.newExtent(tl.getYafter())

            if not suppress:
                frame.canvas.signal("textChanged")

    def textToTWords(self, utext):
        # Split text string into words and make TWord instances from these.
        # An empty string results in a list containing a single TWord with
        # empty string.
        words = utext.split()
        if (words == []): words = [u""]

        # Make a list of TWord instances from the individual word strings
        twords = []
        for w in words:
            if self.printMode:
                twords.append(TWord(w.replace(FixedSpace, u" ")))
            else:
                twords.append(TWord(w))
        return twords

    def textToLines(self, utext):
        """Convert a text into a list of TextLine objects, generating
        Paragraph objects as necessary (one for each paragraph!), and
        taking paragraph tags (< ... >) into account. Each input line
        (ending with 'newline') is made into a paragraph.
        Initially only one TextLine is generated per paragraph, so that
        the layout can be done separately.
        """
        # Bear in mind that ''.splitlines() returns [], so an empty
        # string will lead to an empty line list.
        l = [Paragraph().textlineFromText(self, pText)
                for pText in utext.splitlines()]
        if not l:
            # Ensure that there is always at least one paragraph and
            # line, even if it is empty.
            l = [Paragraph().textlineFromText(self, u"")]
        return l

    def getFrameLines(self, frame):
        """Get the list of TextLine objects allocated to this frame.
        """
        tfl = []
        if self.tlines:
            for tline in self.tlines:
                if (tline.frame == frame):
                    tfl.append(tline)
                elif tfl:
                    break       # ok because the lines are contiguous
        return tfl

    def isFinished(self):
        return getReportVersion(self.report).endswith(u"$")

    def getTeacherName(self):
        return self.db.getTeacherName(self.teacher)


# The formatting info for a paragraph is optional. If present, it is
# contained within a '< ... >' block at the beginning of the paragraph.
# Whitespace before the leading '<' is ignored,
# The information in the format block is in the form of 'item = value'
# statements, separated by ';'
# At present the following items are supported:
#    * = indentation    // 'special' style line, indentation in mm.
#          (a '-' before the indentation indicates right-alignment)


# Regular expression for paragraph format prefix
reP = re.compile(ur"\s*<([^>]*)>(.*)")

class Paragraph:
    """Manages formatting info for a single paragraph of text.
    It does not contain the actual text, which is stored in TextLine
    objects.
    """
    def __init__(self, para=None):
        """Make a paragraph object. If another Paragraph object is
        passed as argument, the settings will be copied from it,
        otherwise, they must be set later, e.g. by calling
        'textlineFromText'.
        """
        if para:
            self.layoutInfo = para.layoutInfo   # a LayoutInfo instance
            self.font = para.font               # a Font instance

            self.align = para.align # 'l'eft, 'r'ight or 'n'ormal (multiline)
            self.indent = para.indent   # paragraph indentation
            self.lineHeight = self.font.lineSpacing

    def textlineFromText(self, rsubject, utext=u""):
        """rsubject is the parent RSubject object.
        utext is an optional unicode string (a raw report text),
        possibly containing a format block.
        -> TextLine instance containing all paragraph text and referring
        to the current Paragraph object (self).
        """
        self.layoutInfo = rsubject.db.layoutInfo
        self.font = self.layoutInfo.normalFont

        self.align = u"n"        # normal style
        self.indent = self.layoutInfo.indent0   # default text indentation
        # Extract formatting information from the supplied (unicode)
        # paragraph string.
        m = reP.match(utext)
        if m:
            # Formatting info present
            fmt, utext = m.groups()
            for i in fmt.split(';'):
                try:
                    item, val = i.split('=', 1)
                    item = item.strip()
                    if (item == u"*"):
                        # Special format, no automatic line breaks
                        self.font = self.layoutInfo.specialFont
                        # A '-' prefix to the indentation is used to
                        # indicate right alignment
                        self.align = u"l"
                        val = val.strip()
                        if (val[0] == u"-"):
                            self.align = u"r"
                            val = val[1:]
                        self.indent = float(val)
                    else:
                        raise ValueError
                except:
                    bug("Format prefix error in line:\n   %s" % (fmt+utext))
        self.lineHeight = self.font.lineSpacing

        return TextLine(self, rsubject.textToTWords(utext))

    def textlineFromAlign(self, rsubject, align):
        self.layoutInfo = rsubject.db.layoutInfo
        self.align = align
        if (align == u"n"):
            self.font = self.layoutInfo.normalFont
            self.indent = self.layoutInfo.indent0
        else:
            self.font = self.layoutInfo.specialFont
            self.indent = self.layoutInfo.indent2
        self.lineHeight = self.font.lineSpacing
        return TextLine(self)

    def getFormat(self, cursor=None):
        """If the paragraph is in special format return a descriptor
        string, otherwise u''.
        cursor: (word index within paragraph, character index within word)
        """
        if (self.align == u"n"): return u""
        fmt = u"%.2f" % self.indent
        if (self.align == u"r"):
            fmt = u"-" + fmt
        return u"<* = " + fmt + u">"

class TextFrame:
    """Manages / encapsulates a single report frame.
    """
    def __init__(self, db, name, index, subject):
        self.canvas = None
        self.yF = None          # y-coordinate of frame start
        self.index = index
        self.layoutInfo = db.layoutInfo
        self.frameDict = self.layoutInfo.layoutDict[u"frames"][name]
        self.title = self.frameDict[u"title"].replace(u"%",
                db.getSubjectName(subject))
        # These margins apply only to the report text:
        self.topMargin = float(self.frameDict[u"topMargin"])
        self.bottomMargin = float(self.frameDict[u"bottomMargin"])
        self.maxHeight = float(self.frameDict[u"height"])
        self.height = self.maxHeight    # used in bottom signature placement

    def addLine(self, y0, h):
        """See if a line with height 'h' can be accommodated in this
        frame, at or below 'y0' (y increases downwards).
        If not return 'None'.
        If so return a pair (y, line1) where y is the actual
        coordinate of the line (within the frame) and line1 is a
        boolean indicating whether it is the first line of the frame.
        """
        line1 = (y0 <= self.topMargin)
        if line1:
            y0 = self.topMargin
        if ((y0 + h) > (self.maxHeight - self.bottomMargin)):
            return None
        return (y0, line1)

# For printing only, the editor always uses the maximum height
    def getHeight(self, y):
        """When a minimum height is specified for the frame, the frame
        can be rendered in less space than the specified height, if
        it is not full. This returns the minimum height for the frame
        taking the text extent, y into account.
        """
        mh = float(self.frameDict[u"minHeight"])
        if (mh < self.maxHeight):
            self.height = y + self.bottomMargin
            if (self.height < mh):
                self.height = mh
        return self.height

    def line1indent(self):
        indent = float(self.frameDict[u"firstLineIndent"])
        if getBoolean(self.frameDict, u"firstLineRelative"):
            indent += self.layoutInfo.titleFont.getWidth(self.title)
        return indent

    def render(self, canvas, rsubject, yF):
        """Display the contents of this frame on the given canvas.
        That includes the title and the signature, and the report text.
        yF is the y-coordinate of the frame.
        """
        # Header/Title (subject name)
        self.canvas = canvas
        self.yF = yF
        x = float(self.frameDict[u"titlex"])
        y = float(self.frameDict[u"titley"])
        alignLeft = not getBoolean(self.frameDict, u"titleRight")
        self.titleItem = self.placeText(self.title, self.layoutInfo.titleFont,
                x, y+yF, alignLeft)
        self.titleOnEmpty = getBoolean(self.frameDict, u"titleOnEmpty")

        # Can get the last frame used by reading the frame of the
        # last tline in rsubject.
        if rsubject.tlines:
            lastUsedFrame = rsubject.frames.index(rsubject.tlines[-1].frame)

            # signature
            sigHeight = float(self.frameDict[u"signatureHeight"])
            if (sigHeight > 0.0):
                im = u"imagefiles/teachers/%s" % rsubject.teacher
                try:
                    self.signatureItem = Image(self.canvas,
                            rsubject.db.getBFile(u"%s.svg" % im))
                except:
                    try:
                        self.signatureItem = ImageR(self.canvas,
                                rsubject.db.getBFile(u"%s.jpg" % im))
                    except:
                        self.signatureItem = None

                if self.signatureItem:
                    self.signatureItem.setSize(sigHeight)
                    x = float(self.frameDict[u"signaturex"])
                    y = float(self.frameDict[u"signaturey"])
                    alignLeft = getBoolean(self.frameDict, u"signatureLeft")
                    yt = yF + self.height - y - sigHeight
                    if not alignLeft:
                        # At right of frame
                        x = self.layoutInfo.mainWidth - x - \
                                self.signatureItem.getWidth()
                    self.signatureItem.setPos(x, yt)

            else:
                self.signatureItem = None

            # teacher
            item = self.frameDict[u"teacher"]
            if item:
                text = item.replace(u"%", rsubject.getTeacherName())
                alignLeft = getBoolean(self.frameDict, u"teacherLeft")
                self.teacherBottom = getBoolean(self.frameDict,
                        u"teacherBottom")
                font = self.layoutInfo.signatureFont
                x = float(self.frameDict[u"teacherx"])
                y = float(self.frameDict[u"teachery"])
                if self.teacherBottom:
                    # At end of box
                    yt = yF + self.height - y - font.lineSpacing
                else:
                    # At top of box
                    yt = y + yF
                self.teacherItem = self.placeText(text, font, x, yt,
                        alignLeft)
                self.teacherOnSignature = getBoolean(self.frameDict,
                        u"teacherOnSignature")
                self.teacherAllFrames = getBoolean(self.frameDict,
                        u"teacherAllFrames")

            else:
                self.teacherItem = None

        else:
            lastUsedFrame = -1
            self.signatureItem = None
            self.teacherItem = None

        # Determine whether the various frame components are shown
        self.renew(lastUsedFrame)

        # Report text
        if rsubject.tlines:
            for tl in rsubject.tlines:
                if (tl.frame == self):
                    tl.render()

    def placeText(self, text, font, x, y, alignLeft):
        """Used for subject headers and teacher names, to place
        them on the canvas.
        """
        ti = TextItem(self.canvas, text)
        ti.setFont(font)
        if not alignLeft:       # Right alignment
            x = self.layoutInfo.mainWidth - x - font.getWidth(text)
        ti.setPos(x, y)
        return ti

    def renew(self, lastFrame):
        """The frame parameters may need adjustment because the index
        of the last occupied frame has changed.
        """
        # Index of the last occupied frame. It is saved so that
        # changes can be detected.
        self.lastFrame = lastFrame

        # A frame can be empty because the subject is invalid. This
        # can't happen in the editor, but if this method is used for
        # drawing the printer frames too, that is relevant. In that
        # case lastFrame will be -1.
        empty = (self.index > lastFrame)

        # title
        if self.titleItem:
            show = (self.titleOnEmpty or not empty)
            self.titleItem.setVisible(show)

        # signature
        if self.signatureItem:
            sig = ((not empty) and (self.index == lastFrame))
            self.signatureItem.setVisible(sig)
        else:
            sig = False

        # teacher
        if self.teacherItem:
            if sig and not self.teacherOnSignature:
                show = False
            else:
                if self.teacherAllFrames:
                    show =True
                elif self.teacherBottom:
                    show = (self.index == lastFrame)
                else:
                    show = (self.index == 0)
                    # If the first page is empty there will be no teacherItem
            self.teacherItem.setVisible(show)

    def newExtent(self, yExtent):
        """Notification that the extent of the text has changed.
        At present unused.
        """
        return

    def strikeOut(self):
        """If the frame is empty and a strike-out line is set,
        return that, else None.
        """
        if (self.index > self.lastFrame):
            strikeOut = self.frameDict[u"strikeOut"]
            if strikeOut and (strikeOut != u"0"):
                return strikeOut
        return None


class TextLine:
    """Manages / encapsulates a single line of report text.
    """
    def __init__(self, para, twords=[]):
        """para: the Paragraph object for the paragraph containing this
        line.
        twords: a list of TWord objects to go in ths line
        """
        self.frame = None       # initially no frame is allocated
        self.para = para
        self.twords = []
        for w in twords:
            self.insert(w)
        self.height = self.para.lineHeight
        self.y = None
        self.x0 = None          # line indentation
        self.spaceWidth = None

    def insert(self, word, ix=None):
        """Add a word to the line, at the given index, ix.
        If no index is given, append the word.
        """
        if (ix == None):
            self.twords.append(word)
        else:
            self.twords.insert(ix, word)
        word.setTLine(self)

    def setPara(self, para):
        """Allocate this line to a new paragraph.
        In particular the items related to the font must be updated.
        """
        if (self.para.font != para.font):
            for w in self.twords:
                w.width = None
                w.offsets = None
                w.textItem.setFont(para.font)
        self.para = para
        self.y = None       # to ensure that the line gets re-rendered.

    def render(self):
        """Place the line on a canvas according to its frame.
        """
        # Get the canvas and the y-offset from the frame
        self.render0(self.frame.canvas, self.frame.yF)

    def render0(self, canvas, dy):
        """Basic rendering function to place this line on a canvas.
        dy is the y-offset, to be added to the offset within the frame
        (which is held as self.y).
        """
        x = self.x0
        if (self.para.align == u"r"):            # Right alignment
            tw = self.twords[0].getWidth()
            for w in self.twords[1:]:
                tw += w.getWidth() + self.spaceWidth
            x = self.para.layoutInfo.mainWidth - x - tw
        self.yReal = self.y + dy
        for w in self.twords:
            if not w.textItem:
                w.setCanvas(canvas)
            w.setPos(x)
            x += w.getWidth() + self.spaceWidth

    def getText(self, ix=0):
        """Return the text of this line as a string.
        Start at word with index ix.
        """
        if (ix >= len(self.twords)):
            return u""
        text = self.twords[ix].string
        for w in self.twords[ix+1:]:
            text += u" " + w.string
        return text

    def getYafter(self):
        """Return the y-coordinate after/underneath this line.
        """
        return self.y + self.height

class TWord:
    """Manages / encapsulates a single text word in a report.
    It must contain the text string, and eventually it will
    contain the graphics object. It provides a method (getWidth) to
    obtain the display/print width of the word.
    After rendering it also contains the x-coordinate relative to the
    beginning of its display line. The units are mm.
    In addition the x-offsets of the characters within the word are
    calculated on demand and cached in the variable 'offsets'.
    """
    def __init__(self, string):
        """string: the text - it should be unicode.
        (the text can be changed later)
        """
        self.x = None
        self.tline = None
        self.textItem = None    # initially there is no graphical item
        self.canvas = None
        self.spellingError = False
        self.spellItem = None
        self.setString(string)

    def setString(self, string):
        """Change the text of the word.
        """
        self.string = string
        self.offsets = None
        self.width = None
        if autoSpellCheck:
            self.spellingError = not checkSpelling.check(string)
            if self.spellItem and (not self.spellingError):
                self.spellItem.remove()
                self.spellItem = None

        if self.textItem:
            self.textItem.setText(self.string)

    def getWidth(self):
        """Get the display/print width of this word.
        """
        if (self.width == None):
            self.width = self.tline.para.font.getWidth(self.string)
        return self.width

    def setPos(self, x):
        """Place the word on the canvas at the given x-coordinate.
        The y-coordinate comes from the Textline.
        """
        self.x = x
        y = self.tline.yReal
        self.textItem.setPos(x, y)

        if self.spellItem:
            self.spellItem.setPos(x, y + self.tline.height, self.getWidth())

        elif self.spellingError:
            self.markSpellingError()

    def markSpellingError(self):
        self.spellItem = LineH(self.canvas, self.x,
                self.tline.yReal + self.tline.height,
                self.getWidth(), SPELLTHICKNESS, colours("spell"))


    def setCanvas(self, canvas):
        """Allocate a graphical item for the word on the given canvas.
        """
        self.canvas = canvas
        self.textItem = TextItem(canvas, self.string)
        self.textItem.setFont(self.tline.para.font)

    def delete(self):
        """The destructor method.
        As TWord objects form circular references with TextLine objects,
        I provide this function to break the cycles, so as not
        to rely on the garbage collector.
        Also the graphical items need removing from the editor view.
        """
        self.tline = None
        self.textItem.remove()
        del(self.textItem)
        del(self.canvas)
        if self.spellItem:
            self.spellItem.remove()
            del(self.spellItem)

    def getX(self, charIx=0):
        """Return the x-coordinate (not offset!) of the character at the
        given index.
        """
        if (charIx == 0):
            x = 0.0
        else:
            x = self.getOffsets()[charIx - 1]
        return self.x + x

    def getOffsets(self):
        """Return a list of character x-offsets, starting at the second
        character (the first character always has offset 0.0).
        """
        if (self.offsets == None):
            dlfont = self.tline.para.font
            self.offsets = []
            k = 1
            while (k <= len(self.string)):
                self.offsets.append(dlfont.getWidth(self.string[:k]))
                k += 1
        return self.offsets

    def setTLine(self, ntline):
        """Tell the TWord object when it is allocated to a new
        TLine instance.
        """
        # Check whether the style of the word has changed
        if (not self.tline) or (self.tline.para.font != ntline.para.font):
            self.offsets = None
            self.width = None
            if self.textItem:
                self.textItem.setFont(ntline.para.font)
        self.tline = ntline

    def getXYH(self, cx):
        """Get editor view coordinates of a given character offset within
        this word.
        Returns a 3-tuple (x, y, lineHeight)
        """
        x = self.getX(cx)
        tl = self.tline
        return (x, tl.y + tl.frame.yF, tl.height)

    def spellUncheck(self):
        """Clears spell-checking data from word.
        """
        self.spellingError = False
        if self.spellItem:
            self.spellItem.remove()
            self.spellItem = None

    def spellCheck(self):
        """Check spelling of the word.
        """
        self.spellingError = not checkSpelling.check(self.string)
        if self.spellingError:
            self.markSpellingError()

