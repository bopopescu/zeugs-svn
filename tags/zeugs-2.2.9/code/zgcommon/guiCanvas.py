# -*- coding: UTF-8 -*-
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
"""Interface to PyQt4 toolkit. A customized canvas widget.
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QBasicTimer as Timer
from guiBase import Font, colours, mm2pts, pts2mm

SHIFT = 32

CURSORWIDTH = 0.5       # mm
LINEWIDTH = 0.3         # mm


class GView(QtGui.QGraphicsView):
    """A customized graphics view, which works like a canvas and
    includes the 'scene'
    """
    def __init__(self, parent=None):
        QtGui.QGraphicsView.__init__(self, parent)
        self.id = None      # see method 'setSignalId'
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # Disable mouse move events when no button is pressed
        self.viewport().setMouseTracking(False)
        self.setBackgroundBrush(colours("paper"))
        # This ensures that the background remains 'clean':
        self.setCacheMode(self.CacheBackground)
        self.sceneWidth = 100   # no real need, but avoids an error message

    def setSignalId(self, id):
        """'id' is a string suffix for the ('framework') signals for
        this widget, just in case more than one of these is used in a
        single application (if not it can be left empty, by not calling
        this method).
        """
        self.id = id

    def connectPySignal(self, signal, slot):
        """Connector for Qt signals.
        """
        QtCore.QObject.connect(self, QtCore.SIGNAL(signal), slot)

    def mousePressEvent(self, event):
        if (event.button() == QtCore.Qt.LeftButton):
            point = self.mapToScene(event.pos())
            self.signal("edPress", (point.x() * pts2mm, point.y() * pts2mm))

    def mouseMoveEvent(self, event):
        # Only react when left button is pressed
        if (event.buttons() == QtCore.Qt.LeftButton):
            point = self.mapToScene(event.pos())
            self.signal("edMove", (point.x() * pts2mm, point.y() * pts2mm))

    def mouseReleaseEvent(self, event):
        if (event.button() == QtCore.Qt.LeftButton):
            point = self.mapToScene(event.pos())
            self.signal("edRelease", (point.x() * pts2mm, point.y() * pts2mm))

    def keyPressEvent(self, event):
        op = event.key()
        m = event.modifiers()
        if (m & QtCore.Qt.ShiftModifier):
            k = SHIFT
        else:
            k = 0

        ##print "KEY op: %x" % op
        if (op == QtCore.Qt.Key_Left):          k += 1
        elif (op == QtCore.Qt.Key_Right):       k += 2
        elif (op == QtCore.Qt.Key_Up):          k += 3
        elif (op == QtCore.Qt.Key_Down):        k += 4
        elif (op == QtCore.Qt.Key_PageUp):      k += 5
        elif (op == QtCore.Qt.Key_PageDown):    k += 6
        elif (op == QtCore.Qt.Key_Return):      k += 7
        elif (op == QtCore.Qt.Key_Delete):      k += 8
        elif (op == QtCore.Qt.Key_Backspace):   k += 9
        elif (op == QtCore.Qt.Key_Space):       k += 10
        #elif (op == QtCore.Qt.Key_Tab):         k += 11
        elif (op == QtCore.Qt.Key_Home):        k += 12
        elif (op == QtCore.Qt.Key_End):         k += 13
        elif (op == QtCore.Qt.Key_PageUp):      k += 14
        elif (op == QtCore.Qt.Key_PageDown):    k += 15
        elif (op == QtCore.Qt.Key_acute):       k = u"\u201e"
        elif (op == QtCore.Qt.Key_QuoteLeft):   k = u"\u201c"
        else:
            k = unicode(event.text())
            if (k == u"") or \
                    (not k.isalnum() and \
                    (k not in u"\"'´`^<>~!%&/()[]=-*+?{},.;:°")):
                event.ignore()
                return
        self.signal("keyPress", k)

    def initArea(self, x0, y0, textWidth):
        """Set the scene area which is shown in the view.
        Clear all display items.
        """
        # Here I just create a new scene, so I don't have to tidy up
        # the old one, hoping that PyQt will manage that!
        gScene = QtGui.QGraphicsScene()
        self.x0 = x0 * mm2pts
        self.y0 = y0 * mm2pts
        self.sceneWidth = textWidth*mm2pts + 2*self.x0
        self.setScene(gScene)
        self.gScene = gScene
        #self.resizeEvent()

    def setHeight(self, h):
        sceneRect = QtCore.QRectF(-self.x0, -self.y0,
                self.sceneWidth, h*mm2pts+2*self.y0)
        self.gScene.setSceneRect(sceneRect)

    def resizeEvent(self, event=None):
        """Scale the view so that the scene width fits
        """
        s = float(self.viewport().width()) / self.sceneWidth
        matrix = QtGui.QMatrix()
        # This ensures that the view gets adjusted even when only the
        # vertical size is changed:
        self.setMatrix(matrix)
        matrix.scale(s, s)
        self.setMatrix(matrix)

    def signal(self, sig, arg=None):
        """Signal adapter - adds the widget's suffix.
        """
        if self.id:
            sig += "-" + self.id
        signal(sig, arg)

    def slot(self, sig, fn):
        """Set up a ('framework') connection using a signal adapter -
        adds the widget's suffix.
        """
        if self.id:
            sig += "-" + self.id
        slot(sig, fn)

class BGRect(QtGui.QGraphicsRectItem):
    """A rectangle graphics item which is placed in the background
    'under'=True makes the rectangle appear below the background.
    """
    def __init__(self, view, colour, under=False):
        if not colour: colour = "paper"
        QtGui.QGraphicsRectItem.__init__(self)
        if under:
            z = -20
        else:
            z = -10
        self.setZValue(z)
        self.setBrush(colours(colour))
        self.setPen(QtGui.QPen(QtCore.Qt.NoPen))

        #Other possibilities?
        #self.setPen = QtGui.QPen(QtCore.Qt.transparent)
        #self.setPen = QtGui.QPen(colour)
        #self.hide()
        view.gScene.addItem(self)

    #def hide(self): inherited from parent

    #def show(self): inherited from parent

    def setRect(self, topLeft, topRight, width, height):
        # floating point coordinates - they are scene coordinates,
        # in mm, not view/screen coordinates.
        QtGui.QGraphicsRectItem.setRect(self, topLeft * mm2pts,
                topRight * mm2pts, width * mm2pts, height * mm2pts)

class CursorLine(QtGui.QGraphicsLineItem):
    """A line.
    """
    def __init__(self, view):
        QtGui.QGraphicsLineItem.__init__(self)
        self.setZValue(10)  # to appear above text
        self.pen = QtGui.QPen(colours("cursor"), CURSORWIDTH * mm2pts)
        self.setPen(self.pen)
        view.gScene.addItem(self)

    #def hide(self): inherited from parent

    #def show(self): inherited from parent

    def set(self, x, y, h):
        x *= mm2pts
        y *= mm2pts
        self.setLine(x, y, x, y + h*mm2pts)

class HLine(QtGui.QGraphicsLineItem):
    """A horizontal separator.
    """
    def __init__(self, view, y, width):
        QtGui.QGraphicsLineItem.__init__(self)
        #self.setZValue(10)  # to appear above text
        self.pen = QtGui.QPen(colours("sep"), LINEWIDTH * mm2pts)
        self.setPen(self.pen)
        y *= mm2pts
        self.setLine(0.0, y, width * mm2pts, y)
        view.gScene.addItem(self)

class Timer(QtCore.QObject):
    def __init__(self, callback):
        QtCore.QObject.__init__(self)
        self.timer = QtCore.QBasicTimer()
        self.callback = callback

    def timerEvent(self, event):
        self.callback()

    def count(self, time):
        self.timer.start(time, self)

    def stop(self):
        self.timer.stop()
