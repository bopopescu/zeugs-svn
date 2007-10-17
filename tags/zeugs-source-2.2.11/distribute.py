#!/usr/bin/env python
# -*- coding: utf-8 -*-

#2007-09-19
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
"""Reorganize modules for distribution.

To produce a PyInstaller executable (Windows), do something like:
  Change to distribution directory, then run
      PyI_zeugs.bat

To produce a py2exe executable (Windows), do something like:
  Change to distribution directory, then run
      c:\python25\python setup.py py2exe
(Doesn't work fully - problems with finding QtSvg - use pyInstaller
instead)
"""

import os, tarfile
from shutil import rmtree, copy2, copytree

def start():
    thisdir = os.path.dirname(os.path.realpath(__file__))
    updir = os.path.dirname(thisdir)
    # Get name of distribution directory
    os.chdir(thisdir)
    vf = open("VERSION")
    version = vf.read().strip()
    vf.close()

    sourcename = "zeugs-source-" + version
    source = os.path.join(updir, sourcename)
    print "Copying source folder to '%s'" % source
    # Create base directory (deleting old one?)
    if os.path.exists(source):
        rmtree(source)
    copytree(thisdir, source)
    # Remove files ending with '~' and '.pyc'
    for dirpath, dirnames, filenames in os.walk(source):
        for f in filenames:
            if f.endswith('~') or f.endswith('.pyc'):
                os.remove(os.path.join(dirpath, f))

    distname = "zeugs-" + version
    dist = os.path.join(updir, distname)
    print "Building distribution in '%s'" % dist
    # Create base directory (deleting old one?)
    if os.path.exists(dist):
        rmtree(dist)
    os.mkdir(dist)

    os.chdir(source)
    # Copy all .py files to base directory
    for dir in ("gui", "zgcommon", "zgcp", "zgedit", "zgprint", "zgsync"):
        for f in os.listdir(dir):
            if f.endswith(".py"):
                copy2(os.path.join(dir, f), dist)
    copy2("zeugs.py", dist)
    copy2("getApplication.py", dist)
    copy2("VERSION", dist)

    # For PyInstaller, NSIS on Windows
    copy2(os.path.join("windows", "zeugs.spec"), dist)
    copy2(os.path.join("windows", "zeugs_PyI.bat"), dist)
    copy2(os.path.join("windows", "zeugs.nsi0"), dist)
    copy2(os.path.join("windows", "zeugs-nsi.py"), dist)
    copy2(os.path.join("windows", "HOWTO_Windows_Installer"), dist)

    # For PyInstaller on Linux
    copy2(os.path.join("linux", "zeugs-linux.spec"), dist)
    copy2(os.path.join("linux", "build.sh"), dist)
    copy2(os.path.join("linux", "zeugs.sh"), dist)
    copy2(os.path.join("linux", "HOWTO_Linux_Installer"), dist)

    # For py2exe on Windows (but it doesn't work - problems with QtSvg)
#    copy2("setup.py", dist)

    # icons
    copytree(os.path.join("gui", "icons"), os.path.join(dist, "icons"))

    # example layouts and databases
    #copytree("examples", os.path.join(dist, "examples"))

    # i18n
    copytree("i18n", os.path.join(dist, "i18n"))

    # documentation
    copytree("doc", os.path.join(dist, "doc"))

    # Pack the directories up for easy maintenance
    print "Compressing folders to tar.gz"
    os.chdir(updir)
    stgz = tarfile.open(sourcename + ".tar.gz", "w:gz")
    stgz.add(sourcename)
    stgz.close()
    print "   ...", source + ".tar.gz"

    dtgz = tarfile.open(distname + ".tar.gz", "w:gz")
    dtgz.add(distname)
    dtgz.close()
    print "   ", dist + ".tar.gz"

    print "Removing created folders:\n   %s\n   %s" % (source, dist)
    rmtree(source)
    rmtree(dist)


if __name__ == "__main__":
    start()
