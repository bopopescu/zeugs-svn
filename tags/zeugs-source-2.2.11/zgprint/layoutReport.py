#!/usr/bin/env python
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
"""This module handles the interpretation of document layout data
for print formatting.

A LayoutReport object manages the laying out and printing of a
single report.
A dictionary of RSubject instances is built by inspecting the subjects
table and filtering for the current pupil.
"""

from traceback import print_exc

import re

from guiBase import LineH, TextItem, Image, Line, getColour
from print_backend import Page
from database import getBoolean
from rsubject import RSubject, TextFrame


class LayoutReport:
    """Handles the laying out in pages of a whole report.
    Each page is constructed on a 'canvas'. These can then be printed,
    or saved as a pdf, in the desired form.
    It uses the currently set class (db, classObject).
    """
    def __init__(self, db, pupilId):
        self.db = db
        self.pupilId = pupilId
        self.layoutDict = self.db.layoutInfo.layoutDict
        docinfo = self.layoutDict[u"document"]

        self.width = float(docinfo[u"pageWidth"])
        self.height = float(docinfo[u"pageHeight"])
        self.mainWidth = self.db.layoutInfo.mainWidth
        self.y0 = float(docinfo[u"topSpace"])

        # Make a dictionary of RSubject objects, one entry for each
        # entry in the layout ('subject_frames' keys) for this class.
        # Some of these reports will be empty if the pupil did not
        # take all of these subjects.
        self.rsubjects = {}
        for subject in self.layoutDict[u"subject_frames"].keys():

            r = RSubject(self.pupilId, subject, self.db)
            self.rsubjects[subject] = r

            # Add information for the rendering
            for f in r.frames:
                f.rendered = False

        # In the case of a choice (in a 'block' subject list
        # that is a '|'-separated list of subjects, without spaces),
        # the first non-empty subject will be rendered and the rest
        # ignored - unless they are all empty, in which case the last
        # one will be rendered. If the last entry in such a list is
        # empty, the item will be skipped.

        # Now layout the actual pages, as 'canvases'
        pageTags = docinfo[u"pages"]
        self.pages = []
        for tag in pageTags.split():
            # Generate a page scene
            self.pages.append(self.layoutPage(tag))

    def layoutPage(self, tag):
        """Using the information in self.layoutDict, lay out the page
        indicated by 'tag'.
        All drawing coordinates are relative to the top left corner of
        the text area (x increasing rightwards, y increasing downwards).
         -> a Page object
        """
        pdict = self.layoutDict[u"pages"][tag]
        # Only the x-offset is page-specific
        x0 = float(pdict[u"_info_"][u"leftSpace"])
        # I make 'page' an instance variable so that it is
        # available to other methods during rendering of the page
        # (of course this only works if the rendering is done strictly
        # one page at a time).
        self.page = Page(x0, self.y0, self.width, self.height, self.mainWidth)

        # The contents of a page dictionary determine which items are
        # to be rendered on the page. The basic units are lines, text,
        # images and report blocks.
        for name, item in pdict.items():
            if name.startswith(u"_"):
                continue
            # item is a dictionary for the object to be rendered
            self.renderItem(item, tag)

        return self.page

    def renderItem(self, idict, page=u"-"):
        """Render the item described by the given dictionary to the
        current page.
        """
        x = float(idict[u"x"])
        y = float(idict[u"y"])
        object = idict[u"object"]

        try:
            table, item = object.split(u"/")
            odict = self.layoutDict[table][item]
            if (table == u"lines"):
                self.renderLine(odict, x, y)

            elif (table == u"text"):
                t = self.textSub(odict[u"text"])
                ti = TextItem(self.page, t)
                ti.setFont(self.db.layoutInfo.getFont(odict[u"font"]))
                ti.setPos(x, y)

            elif (table == u"images"):
                file = odict[u"file"]
                data = self.db.getBFile(u"imagefiles/%s" % file)

                image = Image(self.page, data)
                image.setPos(x, y)
                image.setSize(float(odict[u"vsize"]))


            elif (table == u"blocks"):
                self.renderSubjects(odict, x, y)

            else:
                raise

        except:
            print_exc()

            warning(_("Invalid item for print rendering on page %1:\n  %2"),
                    (page, object))

    def textSub(self, utext):
        """Perform simple substitutions on text.
        """
        utext = utext.strip(u'"')
        ntext = u""
        while True:
            i = utext.find(u'\\')
            if (i < 0): break
            ch = utext[i+1]
            jump = 2
            if (ch == u','):
                ch = u';'
            elif (ch == u'/'):
                ch = '|'
            elif (ch == u'-'):
                ch = u'='
            elif (ch == u'_'):
                ch = u'\\'
            elif (ch == u"'"):
                ch = u'"'
            elif (ch == u'y'):
                ch = self.db.baseDict[u"schoolYear"]
            elif (ch == u"{"):
                j = utext.find(u"}", i)
                if (j > 0):
                    jump = j - i + 1
                    f = utext[i+2:j]
                    fill = self.db.classObject.pupilinfo[self.pupilId].get(f)
                    if fill:
                        ch = fill
                    else:
                        ch = u"???"
                else:
                    ch = u"??"
            elif (ch == u'p'):
                ch = self.db.classObject.pupilinfo[self.pupilId]["Name"]
            elif (ch == u'b'):
                ch = self.db.classObject.pupilinfo[self.pupilId]["DateOfBirth"]
            elif (ch == u'o'):
                ch = self.db.classObject.pupilinfo[self.pupilId]["PlaceOfBirth"]
            elif (ch == u'c'):
                ch = self.db.classObject.className
            else:
                ch = u'\\' + ch

            ntext += utext[:i] + ch
            utext = utext[i+jump:]
        return ntext + utext

    def renderLine(self, odict, x, y):
        Line(self.page,
                float(odict[u"x0"]) + x,
                float(odict[u"y0"]) + y,
                float(odict[u"x1"]) + x,
                float(odict[u"y1"]) + y,
                float(odict[u"width"]),
                getColour(odict[u"colour"])
            )

    def renderSubjects(self, odict, x0, y0):
        """Render a subjects block to the current page.
        """
        boxHeight = float(odict[u"height"])     # vertical space for box
        separator = odict[u"separator"]
        if (not separator) or (separator == u"0"):
            separator = None
        else:
            separator = self.layoutDict[u"lines"][separator]
        subjects = odict[u"subject-list"].split()

        # Loop over all the subjects for this block, breaking out
        # before the end if the space is exhausted. Create a list of
        # the frames which are to be rendered into this block.
        frameList = []
        h = 0.0         # The height accumulator for the subject frames
        for s in subjects:
            choice = s.split(u"|")
            if (len(choice) == 1):
                # The normal, single-subject case
                rsub, frame = self.getRSubjectFrame(s)
                if frame and frame.rendered:
                    frame = None

            else:
                for subject in choice:
                    if not subject:
                        # Skip this choice group
                        frame = None
                        break

                    rsub, frame = self.getRSubjectFrame(subject)
                    if not frame:
                        break
                    if frame.rendered:
                        # Skip this choice group
                        frame = None
                        break

                    if rsub.tlines:
                        break
                # If no non-empty subject was found use the last
                # empty one.

            # If an unrendered frame was found, 'frame' is set
            # to it, otherwise to 'None'.
            if not frame:
                # Move on to next subject in list
                continue

            # Render the frame in 'frame'
            tlines = rsub.getFrameLines(frame)
            if tlines:
                lastline = tlines[-1]
                # vertical space needed by the frame text:
                hF = lastline.getYafter()
            else:
                hF = 0.0    # vertical space needed by the frame text

            frameHeight = frame.getHeight(hF)
            # See if it fits into the box
            if ((h + frameHeight) > boxHeight):
                break

            # Add the frame and RSubject object to the rendering list
            frameList.append((frame, rsub))
            frame.rendered = True

            h += frameHeight

        # End of subject for-loop

        # Now lay out the frames in frameList in the box
        if getBoolean(odict, u"spreadFrames") and frameList:
            deltaH = (boxHeight - h) / len(frameList)
        else:
            deltaH = 0.0

        for tframe, rsubject in frameList:
            if separator and (tframe != frameList[0]):
                self.renderLine(separator, x0, y0)

            tframe.render(self.page, rsubject, y0)

            strikeOut = tframe.strikeOut()
            if strikeOut:
                self.renderLine(self.layoutDict[u"lines"][strikeOut], x0, y0)

            y0 += tframe.height + deltaH

    def getRSubjectFrame(self, s):
        """Given a subject as in the subjects list of a block
        (format <subject tag>.<frame number>, where the suffix is
        optional, defaulting to 1),
        return for it the (RSubject object, TextFrame object).
        """
        try:
            sf = s.split(u".")
            if (len(sf) == 1):
                rsub = self.rsubjects[s]
                return (rsub, rsub.frames[0])

            if (len(sf) != 2):
                raise

            rsub = self.rsubjects[sf[0]]
            return (rsub, rsub.frames[int(sf[1]) - 1])

        except:
#            print_exc()

            warning(_("Invalid subject (%s) in blocks subject list") % s)
            return (None, None)
