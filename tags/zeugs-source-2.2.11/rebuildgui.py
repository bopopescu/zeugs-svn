#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
"""Rebuild gui interface modules (after changing .ui files).
"""

import os
from subprocess import call
import re

repy = re.compile(r"(.+)\.ui$")

def rebuild(path):
    os.chdir(path)
    for f in os.listdir("."):
        rem = repy.match(f)
        if rem:
            fs = rem.group(1)
        else:
            continue

        if (call(["pyuic4 -o ui_%s.py %s.ui" % (fs, fs)], shell=True) != 0):
            print "FAILED: pyuic4 -o ui_%s.py %s.ui" % (fs, fs)

        # To convert the i18n stuff to gettext form, use gettextify, e.g.
        try:
            gettextify("ui_%s.py" % fs)
        except:
            print "FAILED: converting 'ui_%s.py' to gettext-form" % fs


# Modify a file outputted by pyuic4 to work with gettext rather than
# QLinguist.

regt = re.compile('\\QtGui.QApplication.translate\\([^,]*, "(.*)",.*')

def gettextify(filepath):
    file = open(filepath)
    lines = []
    for line in file:
#        m = regt.search(line)
#        if m:
#            print m.groups()
        lines.append(regt.sub('_("\\1"))', line))
    file.close()
    file = open(filepath, "wb")
    for ln in lines:
        file.write(ln)
    file.close()


if __name__ == "__main__":
    rebuild("gui")
    print "DONE"
