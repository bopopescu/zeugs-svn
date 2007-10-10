#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#2007-09-11
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
# Print handling. This version can also output pdf.

from PyQt4 import QtGui, QtCore
from guiBase import RESOLUTION, mm2pts

class Page:
    """Deals with rendering a single page.
    """
    def __init__(self, x0, y0, width, height, mainWidth):
        """x0 is the left-margin, y0 the top margin.
        mainWidth is the width of the main printing area.
        """
        # Get the size and margins
        self.x0 = x0 * mm2pts
        self.y0 = y0 * mm2pts
        self.width = width * mm2pts
        self.height = height * mm2pts
        self.mainWidth = mainWidth * mm2pts

        # Create a 'drawing area'
        # For compatibility with the GView widget used by the editor
        # it has to be called 'gScene'
        self.gScene = QtGui.QGraphicsScene(-self.x0, -self.y0,
                self.width, self.height)

        # This sort of canvas doesn't need spellchecking
        self.checkSpelling = None

# At present (v4.2) Qt4 cannot handle custom paper sizes
pageSizes = (QtGui.QPrinter.A4, QtGui.QPrinter.A3)

class Printer(QtGui.QPrinter):
    """Represents the printing device. It can output to the printer
    (default) or a pdf file.
    """
    def __init__(self, n=1, shrink=True, landscape=False, filename=None):
        """By default print in portrait mode, one document page to
        one sheet of paper. n is the number of pages to fit on one
        side of a sheet.
        """
        QtGui.QPrinter.__init__(self)
        self.setPageSize(pageSizes[0])
        self.setOrientation(QtGui.QPrinter.Portrait)
        self.scale = 1
        if (n > 1):
            if landscape:
                self.setOrientation(QtGui.QPrinter.Landscape)
            if shrink:
                self.scale = n
            else:
                self.setPageSize(pageSizes[1])

        self.setResolution(RESOLUTION)
        self.setFullPage (True)
        if filename:
            self.setOutputFileName (filename)    # ends .pdf for pdf output

        self.painter = QtGui.QPainter(self)

        # Is rotation necessary?
        if (n > 1) and not landscape:
            w = self.paperRect().width()
            m = QtGui.QMatrix()
            m.rotate(90)
            m.translate(0, -w)
            self.painter.setWorldMatrix(m)


    def render(self, scene, pos=0):
        """Render a QGraphicsScene to the printer.
        'pos' is the position (left-to-right) of the scene within
        the page, starting at 0.
        It uses the number of pages (self.scale) and the dimensions
        of the document page to determine the actual scale factor, so
        that the sum of the page widths is equal to the page height
        (rendered in landscape mode).
        """
        w = scene.width()
        h = scene.height()
        x = 0.0
        if (self.scale > 1):
            scale = (w * self.scale) / h
            w = w / scale
            h = h / scale
        x += w * pos
        scene.render(self.painter, QtCore.QRectF(x, 0, w, h))

    def end(self):
        """All pages done, end print job.
        """
        self.painter.end()



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)

    from database import DB
    from layoutReport import LayoutReport
    layout = LayoutReport(DB("db1.zgn"), u"3", u"23")

    printer = Printer("testPrint1.pdf", 0)

    first = True
    for p in layout.pages:
        if first:
            first = False
        else:
            printer.newPage()
        printer.render(p.gScene, 0)

    printer.end()
