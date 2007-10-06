#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
"""The zeugs application despatcher.
The first argument determines which application will be run.
If it isn't given, or it is invalid, a selection dialog will be
presented.

This launcher assumes all modules are in the same directory as it is.
"""

import sys, os

from getApplication import GuiGetApplication

import gettext
lang = os.getenv("LANG")
if lang:
    gettext.install('zeugs', 'i18n', unicode=1)
else:
    tr = gettext.translation('zeugs', 'i18n', languages=['de_DE'])
    tr.install(unicode=1)

import framework

progList = ("sync", "edit", "control", "print", "setup", "cfged")

def start():
    if (len(sys.argv) >= 2):
        prog = sys.argv[1]
    else:
        prog = None

    slot("selectApp", slot_gotProg)
    if prog not in progList:
        # Put up a dialog to select the application
        GuiGetApplication("appGet").run()
    else:
        slot_gotProg(prog)

def slot_gotProg(prog):
    if (prog == "setup"):
        from dbInit import setup
        setup()
        return

    elif (prog == "control"):
        from guiCP import GuiCP
        # Initialize graphical interface
        gui = GuiCP("cp")

    elif (prog == "edit"):
        from guiEditor import GuiEditor
        # Initialize graphical interface
        gui = GuiEditor("editor")

    elif (prog == "sync"):
        from guiSync import GuiSync
        # See if a client database file has been passed on the command line
        filepath = None
        if (len(sys.argv) > 2):
            f = sys.argv[2]
            if f.endswith(".zgn"):
                filepath = f

        # Initialize graphical interface
        gui = GuiSync("sync", filepath)

    elif (prog == "print"):
        from guiPrint import GuiPrint
        # Initialize graphical interface
        gui = GuiPrint("print")

    elif (prog == "cfged"):
        from guiConfigEd import GuiConfigEd
        # Initialize graphical interface
        gui = GuiConfigEd("cfged")

    else:
        return

    # enter event loop
    gui.run()



def we_are_frozen():
    """Returns whether we are frozen via py2exe/pyinstaller.
    This will affect how we find out where we are located.
    """

    return hasattr(sys, "frozen")


def module_path():
    """ This will get us the program's directory,
    even if we are frozen using py2exe etc.
    """
    se = sys.getfilesystemencoding()
    if not se:
        se = 'utf8'
    if we_are_frozen():
        return os.path.dirname(unicode(sys.executable, se))

    return os.path.dirname(unicode(os.path.realpath(__file__), se))




if __name__ == "__main__":
    progdir = module_path()
    os.chdir(progdir)
    start()
