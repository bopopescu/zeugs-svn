#!/usr/bin/env python
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

"""
1) Generally something like: pygettext.py -p i18n -o zeugs.pot *.py

Here including the various subdirectories:
pygettext.py -p i18n -o zeugs.pot *.py zgcommon/*.py zgprint/*.py \
        zgedit/*.py gui/*.py zgcp/*.py zgsync/*.py


I think poedit can do most of the processing, but the steps are:

2) cd i18n ; msginit -i zeugs.pot -l de

OR:
2a) to update a po file:

cd i18n ; msgmerge -U zeugs.po zeugs.pot

3) edit po file

4) generate binary file:
cd i18n ; msgfmt -c -v -o zeugs.mo zeugs.po

5) move the .mo file to i18n/de/LC_MESSAGES

6) Add to the main program file:

import gettext
gettext.install('zeugs', 'i18n', unicode=1)

5) Run, e.g.:
LANG=de_DE ./zeugs.py

There seems to be no way (at present?) to get qt4 to display Strg+C
instead of Ctrl+C for shortcuts in menu items ...
"""

import sys, os, shutil
from subprocess import call

thisdir = os.path.dirname(os.path.realpath(__file__))
basedir = os.path.dirname(thisdir)
os.chdir(basedir)

if (len(sys.argv) < 2):
    lang = "de"
else:
    lang = sys.argv[1]
print "Generating internationalization for language '%s'\n" % lang
print "    If you wanted a different language run 'i18n.py <language>'"
print "    For example 'i18n.py fr'\n"

dirs = [".", "zgcommon", "zgprint", "zgedit", "gui", "zgcp", "zgsync"]
allpy = [os.path.join(d, "*.py") for d in dirs]
call(["pygettext.py", "-p", thisdir, "-o", "zeugs.pot"] + allpy)

os.chdir(thisdir)
langfile = lang + ".po"
pofile = os.path.join(lang, "LC_MESSAGES", langfile)
if os.path.isfile(pofile):
    shutil.copy(pofile, ".")
    call(["msgmerge", "-U", langfile, "zeugs.pot"])
else:
    call(["msginit", "-i", "zeugs.pot", "-l", lang])

lf = open("lang", "w")
lf.write(lang)
lf.close()

print "Now edit '%s' and then run 'i18n2.py'" % langfile
