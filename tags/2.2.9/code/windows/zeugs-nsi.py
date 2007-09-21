#!/usr/bin/env python

#2007-08-31
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

"""Windows only.
Run this after running PyInstaller. It generates the .nsi (configuration)
file for the NSIS installer generator.
"""

import os

sourceDir = 'distzeugs'

vf = open("VERSION")
version = vf.read().strip()
vf.close()

ifile = open('zeugs.nsi0', 'rb')
ofile = open('zeugs.nsi', 'wb')

os.chdir(sourceDir)

fdlist = []
ddlist = []

for line in ifile:
    line = line.rstrip('\n\r')
    if not line.startswith('***'):
        ofile.write('%s\r\n' % line)
        continue

    if line.startswith('***S***'):
        ofile.write('%s\r\n' % (line[7:].replace('%', sourceDir)))

    elif line.startswith('***V***'):
        ofile.write('%s\r\n' % (line[7:].replace('%', version)))

    elif line.startswith('***I***'):
        for root, dirs, files in os.walk('.'):
            base = root.lstrip('./').replace("/", "\\")

            if base and files:
                ofile.write('  SetOutPath "$INSTDIR\\%s"\r\n' % base)
                ddlist.append(base)
                bpath = '%s\\' % base
            else:
                bpath = ''

            for f in files:
                path = bpath + f
                ofile.write('  File "${SOURCE_DIR}%s"\r\n' % path)
                fdlist.append(path)

    elif line.startswith('***X***'):
        i = len(fdlist)
        while i > 0:
            i -= 1
            ofile.write('  Delete "$INSTDIR\\%s"\r\n' % fdlist[i])

    elif line.startswith('***D***'):
        i = len(ddlist)
        while i > 0:
            i -= 1
            ofile.write('  RMDir "$INSTDIR\\%s"\r\n' % ddlist[i])

    else:
        print "ERROR:", line

ifile.close()
ofile.close()
