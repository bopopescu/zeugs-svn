#!/usr/bin/env python
# -*- coding: UTF-8 -*-

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
"""A LayoutUnits object lays a set of text units (individual reports)
out for print formatting. It is for use in the editor.
"""

XTITLE = 0.0            # indentation for page header
YTITLE = 0.0            # y-shift for page header
UNDERLINEWIDTH = 0.2
TITLEGAP = 0.5          # extra space below page header and pupil names
GAP = 3.0               # gap between reports
XSHIFT = 0.0            # offset of printing area on page, direction
                        # depends on even/odd page


from guiBase import LineH, TextItem, getColour
from print_backend import Page, Printer
from rsubjectx import RSubjectX as RSubject

class LayoutUnits:
    """Handles the laying out in pages of a set of report entries for
    one subject tag and a list of pupils.
    Each page is constructed on a 'canvas'. These can then be printed,
    or saved as a pdf.
    """

    def __init__(self, db, subject, pupils):
        layoutInfo = db.layoutInfo

        self.subjectName = db.getSubjectName(subject)
        self.className = db.classObject.className
        self.titleFont = layoutInfo.titleFont
        self.titleSpace = self.titleFont.lineSpacing + TITLEGAP

        docinfo = layoutInfo.layoutDict[u"document"]
        width = float(docinfo[u"pageWidth"])
        height = float(docinfo[u"pageHeight"])
        y0 = float(docinfo[u"topSpace"])
        x0 = (width - layoutInfo.mainWidth) / 2
        lineWidth = layoutInfo.lineWidth
        textSpace = float(docinfo[u"textAreaHeight"])

        page = None         # current page
        self.pages = []     # list of pages

        for p in pupils:
            rs = RSubject(p, subject, db)
            pupilName = db.getPupilName(p)

            # Take the existing frames and re-render these in the
            # available area, one frame at a time
            lix = 0     # line index
            nlines = len(rs.tlines)
            frameNo = 0         # frame number

            for frame in rs.frames:
                frameNo += 1

                # Get all the lines from this frame
                lines = []
                while  (lix < nlines):
                    line = rs.tlines[lix]
                    if (line.frame != frame):
                        break
                    lines.append(line)
                    lix += 1

                if not lines:
                    # Don't show empty frames
                    break

                # will they fit on the current page?
                if (not page) or self.noFit(textSpace - yoff - self.titleSpace,
                        lines):
                    # if not, end the page and get a new one
                    if (len(self.pages) % 2):
                        xoff = -XSHIFT
                    else:
                        xoff = XSHIFT
                    page = Page(x0 + xoff, y0, width, height, lineWidth)
                    self.pages.append(page)

                    # set yoff
                    yoff = GAP

                # Render the collected lines

                #  - pupil name + frame number
                text = pupilName
                if (frameNo > 1):
                    if (frameNo < len(rs.frames)):
                        text += u" (%d)" % frameNo
                    else:
                        # overflow frame
                        text = u"     (%s [X])" % text
                ti = TextItem(page, text)
                ti.setFont(self.titleFont)
                ti.setPos(0.0, yoff)

                yoff += self.titleSpace - lines[0].y

                for l in lines:
                    l.render0(page, yoff)

                # reset yoff to after last line
                ##yoff += lines[-1].getYafter() - lines[0].y
                yoff += lines[-1].getYafter()

                # gap at end
                yoff += GAP


    def noFit(self, h, lines):
        """Is too much space required by the lines?
        """
        return (lines[-1].getYafter() - lines[0].y) > h

    def printout(self, filepath=None, pages=None):
        """Print the selected pages ('None' => all pages !).
        If filepath is given the output will be to a file, otherwise
        the default printer.
#Or should I use the print dialog?
        """
        printer = Printer(filename=filepath)
        first = True    # to control 'newPage'

        npages = len(self.pages)    # total number of pages
        if (pages == None):
            pages = range(1, npages+1)

        for pn in pages:
            p = self.pages[pn-1]

            # add header/footer (class, subject, ...)
            text = u"%s - %s  (%s)" % (
                    argSub(_("Class %1"), (self.className,)),
                    self.subjectName,
                    argSub(_("page %1 of %2"), (unicode(pn), unicode(npages))))
            ti = TextItem(p, text)
            ti.setFont(self.titleFont)
            ti.setPos(XTITLE, YTITLE - self.titleSpace)

            LineH(p, XTITLE, 0.0,
                    self.titleFont.getWidth(text),
                    UNDERLINEWIDTH,
                    getColour(u"#606060"))

            if not first:
                printer.newPage()

            printer.render(p.gScene)

            first = False

        printer.end()
