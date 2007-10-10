#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""Utility for printing one or more complete reports, or selected
pages therefrom.
"""

import sys, os.path
# Add module directories to search path
thisDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(thisDir, "zgprint"))
sys.path.append(os.path.join(thisDir, "zgcommon"))
sys.path.append(os.path.join(thisDir, "gui"))

from guiPrint import GuiPrint

import gettext
gettext.install('zeugs', 'i18n', unicode=1)

import framework


def start():
    # Initialize graphical interface
    gui = GuiPrint("print")

    # enter event loop
    gui.run()

if __name__ == "__main__":
    start()
