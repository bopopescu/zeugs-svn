# -*- coding: UTF-8 -*-
#2007-09-21
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
"""Basic gui stuff.
"""

from PyQt4 import QtCore, QtGui, QtSvg

RESOLUTION = 2540
pts2mm = 25.4 / RESOLUTION
mm2pts = RESOLUTION / 25.4

import os.path

# Will be used for a QPicture instance, needed as a sort of bodge to set
# the resolution in a platform independent way.
QP = None

class Font(QtGui.QFont):
    """A slightly customized wrapper for QFont.
    It also supplies space width and line spacing (as well as a general
    getWidth function for the width of a string) in mm.
    """
    def __init__(self, layoutInfo):
        """Set up a QFont object and initialize instance values.
        'layoutInfo' is a dictionary containing the required info
        """
        # Now it's a little complicated because the font needs to have a
        # special platform independent resolution/size. As Qt4 does
        # font metrics based on the display device resolution, we need
        # to know what that is. So a QFont is constructed based on a
        # QPicture, whose resolution can then be read. At first I
        # tried using QPrinter as the device, but this didn't work on
        # a Windows computer without a printer.
        global QP, fontscale
        if not QP:
            QP = QtGui.QPicture()
            # This was the first attempt, and worked well within one
            # platform, but on Linux there seems to be some inaccuracy
            # in the point size(!?)
#            res = QP.logicalDpiX()
#            fontscale = float(RESOLUTION) / res

            # This seems to help the inconsistency of font sizes
            # between Windows and Linux. It's not perfect, but
            # that may be impossible to attain.
            qf = QtGui.QFont()
            qf.setPointSize(1000)
            poi = QtGui.QFontInfo(qf).pointSizeF()
            qf.setPixelSize(1000)
            pix = QtGui.QFontInfo(qf).pointSizeF()

            fontscale = float(RESOLUTION) * pix / poi / 72

        family = layoutInfo[u"family"]
        QtGui.QFont.__init__(self, family)
        self.setPointSizeF(float(layoutInfo[u"points"])*fontscale)
        self.setWeight(int(layoutInfo[u"weight"]))
        self.setStretch(int(float(layoutInfo[u"stretch"])*100))
        self.setItalic(layoutInfo[u"style"] == u"1")
        self.setUnderline(layoutInfo[u"underline"] == u"1")
        self.metric = QtGui.QFontMetricsF(self, QP)

        self.spWidth = self.getWidth(u" ")
        self.lineSpacing = self.metric.lineSpacing() * pts2mm \
                * float(layoutInfo[u"lineSpacing"])
        self.colour = getColour(layoutInfo[u"colour"])

        # Check whether the desired font was chosen
        fi = QtGui.QFontInfo(self)
        if (fi.family() != self.family()):
            warning(_("Font not available: '%s'") % family)

    def getWidth(self, string):
        """Return the width of a string in mm
        """
        return self.metric.width(string) * pts2mm

class TextItem(QtGui.QGraphicsSimpleTextItem):
    def __init__(self, view, string):
        QtGui.QGraphicsSimpleTextItem.__init__(self, string)
        #self.setBrush(colours(colour))
        #self.setFont(font)
        view.gScene.addItem(self)

    def remove(self):
        self.scene().removeItem(self)

    def setFont(self, font):
        QtGui.QGraphicsSimpleTextItem.setFont(self, font)
        self.setBrush(font.colour)

    #def setColour(self, colour):
    #    self.setBrush(colours(colour))

    def setPos(self, x, y):
        QtGui.QGraphicsSimpleTextItem.setPos(self, x * mm2pts, y * mm2pts)

class LineH(QtGui.QGraphicsLineItem):
    """A horizontal line.
    """
    def __init__(self, view, x, y, length, width, colour):
        QtGui.QGraphicsLineItem.__init__(self)
        self.setZValue(-10)  # to appear below text ???
        self.pen = QtGui.QPen(colour, width * mm2pts)
        self.setPen(self.pen)

        view.gScene.addItem(self)
        self.setPos(x, y, length)

    def remove(self):
        self.scene().removeItem(self)

    def setPos(self, x, y, length):
        x *= mm2pts
        y *= mm2pts
        self.setLine(x, y, x + length*mm2pts, y)

class Line(QtGui.QGraphicsLineItem):
    """A line.
    """
    def __init__(self, view, x0, y0, x1, y1, width, colour):
        QtGui.QGraphicsLineItem.__init__(self)
        #self.setZValue(-10)  # to appear below text ???
        self.pen = QtGui.QPen(colour, width * mm2pts)
        self.setPen(self.pen)
        self.setLine(x0*mm2pts, y0*mm2pts, x1*mm2pts, y1*mm2pts)
        view.gScene.addItem(self)

IMAGERESOLUTION = mm2pts / 10
class Image(QtSvg.QGraphicsSvgItem):
    """svg images should be created with sizes in pixels and a
    resolution of 10 pixels per mm. The scaling should then be
    accurate.
    """
    def __init__(self, view, data):
        QtSvg.QGraphicsSvgItem.__init__(self)
        # The renderer must be preserved for the lifetime of the image
        self.renderer = QtSvg.QSvgRenderer(QtCore.QByteArray(data))

        #print "IH", self.renderer.defaultSize().height()

        self.setSharedRenderer(self.renderer)
        view.gScene.addItem(self)
        self.uscale = 1.0

    def setPos(self, x, y):
        QtSvg.QGraphicsSvgItem.setPos(self, x * mm2pts, y * mm2pts)

    def setSize(self, s):
        self.uscale = s / self.getHeight()
        s = self.uscale * IMAGERESOLUTION
        self.scale(s, s)

    def getHeight(self):
        return self.renderer.defaultSize().height() * self.uscale / IMAGERESOLUTION

    def getWidth(self):
        return self.renderer.defaultSize().width() * self.uscale / IMAGERESOLUTION


def coloursInit():
    """Initialize the colourDict dictionary. This sets up colours
    used in the editor window.
    paper: paper colour
    cursor: text cursor colour
    sep: colour of box boundary lines
    selbg: selection background colour
    ovflbg: overflow box background colour
    """
    global colourDict
    colourDict = {}
    colourDict["paper"] = getColour("#ffff80")
    colourDict["sep"] = getColour("#00ff00")
    colourDict["cursor"] = getColour("#ff0000")
    colourDict["selbg"] = getColour("#00ffff")
    colourDict["ovflbg"] = getColour("#ffa0a0")
    colourDict["spell"] = getColour("#ff4040")

def colours(name):
    return colourDict[name]

qcolors = {}
def getColour(colour):
    """Given an rgb colour string (#xxxxxx), return a QColor instance.
    It does caching.
    """
    qc = qcolors.get(colour)
    if not qc:
        qc = QtGui.QColor(colour)
        qcolors[colour] = qc
    return qc
