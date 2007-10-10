#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#2007-09-07
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
"""This module provides error handling (error, warning and bug)
and a simple signals mechanism.
It installs these in the 'builtin' namespace, for easy access.
"""

MESSAGEMAXLINES = 10

from traceback import format_exc

from guiDialogs import warnDialog, messageDialog
from gui0 import Settings

import __builtin__

class Signals:
    """A very simple signal/slot mechanism.
    It pays no attention to where the signal comes from or where the
    slot is, the connection is established purely on the basis of the
    signal name.
    A signal argument is passed (default is 'None').
    """
    def __init__(self):
        # The connections are organized using this dictionary. The
        # keys are the signal names. The slots are held as values in
        # a list.
        self.signals = {}

    def signal(self, name, arg=None):
        """Send the named signal with the given argument.
        There need not be a corresponding slot.
        """
        try:
            slots = self.signals.get(name)
            if slots:
                for s in slots:
                    s(arg)
        except:
            error(_("Program Error - please report\n\n%1"),
                    (unicode(format_exc(), "utf8"),))

    def slot(self, name, func):
        """Notify the signals mechanism that the given function is
        to be called when the named signal is emitted.
        """
        slots = self.signals.get(name)
        if slots:
            slots.append(func)
        else:
            self.signals[name] = [func]


#**************** ERROR HANDLING *******************

def argSub(string, args):
    """Substitute '%n' in the string, where n is an integer, starting
    with 1, by the values in args, sequentially.
    """
    for i in range(len(args)):
        string = string.replace(u"%" + unicode(i + 1), args[i])
    return string

def warning(message, args=[], title=None):
    if not title:
        title = _("Warning")
    lines = argSub(message, args).splitlines()
    text = lines[0] + u"\n"
    if (len(lines) > MESSAGEMAXLINES):
        lines = [u" ..."] + lines[-MESSAGEMAXLINES:]
    else:
        lines = lines[1:]
    for l in lines:
        text += l + u"\n"
    warnDialog(title, text)
    return text

def error(message, args=[]):
    remember("lastError", warning(message, args, _("Error")))
    signal("quit")

def bug(message, args=[]):
    remember("lastBug", warning(message, args, u"Bug"))
    signal("quit")

def message(text, args=[]):
    messageDialog(_("Information"), argSub(text, args))

def remember(key, text):
    """Save the last message using the "settings" mechanism.
    """
    Settings("").setVal(key, text)


# Install the functions in the 'builtin' namespace
if "signal" not in dir(__builtin__):
    signals = Signals()
    __builtin__.signal = signals.signal
    __builtin__.slot = signals.slot
    __builtin__.argSub = argSub
    __builtin__.message = message
    __builtin__.error = error
    __builtin__.warning = warning
    __builtin__.bug = bug
