#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The zeugs synchronization utility.
For transferring edited reports (and comments) from a user's database
to the main and updated configuration information from the main
to the client (well, actually the client database file is replaced).
"""

# Add module directories to search path
import sys, os.path
thisDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(thisDir, "zgsync"))
sys.path.append(os.path.join(thisDir, "zgcommon"))
sys.path.append(os.path.join(thisDir, "gui"))

from guiSync import GuiSync

import gettext
gettext.install('zeugs', 'i18n', unicode=1)

import sys

import framework


def start():
    # See if a client database file has been passed on the command line
    filepath = None
    if (len(sys.argv) > 1):
        f = sys.argv[1]
        if f.endswith(".zgn"):
            filepath = f

    # Initialize graphical interface
    gui = GuiSync("sync", filepath)

    # enter event loop
    gui.run()

if __name__ == "__main__":
    start()
