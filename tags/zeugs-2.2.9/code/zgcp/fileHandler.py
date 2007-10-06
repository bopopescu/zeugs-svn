#!/usr/bin/env python
# -*- coding: utf-8 -*-

#2007-09-16
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

import os
import re
from zipfile import ZipFile

from database import rx1, rx2

def dirList(allList, dpath):
    dirs = []
    files = []
    lenDpath = len(dpath)
    subtree = [f[lenDpath:] for f in allList if f.startswith(dpath)]
    for fd in subtree:
        if not fd:
            continue    # the directory itself
        dc = fd.split('/', 1)
        if (len(dc) > 1):
            # sub-directory
            d = dc[0]
            if d not in dirs:
                dirs.append(d)
        else:
            # file
            files.append(fd)
    return (dirs, files)

class CfgZip:
    def __init__(self, filepath, write=False):
        if isinstance(filepath, unicode):
            filepath = filepath.encode('utf8')
        # Get the database name from the file-name, convert to
        # lowercase and ' ' to '_', to avoid confusion ...
        self.cfgName = os.path.basename(filepath).rsplit('.',
                1)[0].lower().replace(" ", "_")
        if write:
            rw = "w"
        else:
            rw = "r"
        self.all0 = []
        self.base = self.cfgName + '/'
        try:
            self.zipfile = ZipFile(filepath, rw)
        except:
            traceback.print_exc()
            self.zipfile = None
            return
        if not write:
            self.all0 = self.zipfile.namelist()
            self.base = self.all0[0].split('/', 1)[0] + '/'
        self.baseLen = len(self.base)

    def isOpen(self):
        return (self.zipfile != None)

    def close(self):
        if self.isOpen():
            self.zipfile.close()
            self.zipfile = None

    def allFiles(self):
        """Get a list of all entries in the archive.
        The base prefix is stripped.
        """
        return [f[self.baseLen:] for f in self.all0]

    def listDir(self, path):
        """Return a list of folders and a list of files within the
        given folder.
        Return (folder-list, file-list)
        """
        dpath = "%s%s/" % (self.base, path.rstrip('/'))
        return dirList(self.all0, dpath)

    def listFiles(self, path):
        return self.listDir(path)[1]

    def listDirs(self, path):
        return self.listDir(path)[0]

    def listAllFiles(self, path):
        """Return a list of all files (including those in sub-folders)
        whose path starts with path, but not including path itself.
        The entries are full paths, including the path-prefix.
        """
        dpath = self.base + path
        return [f[self.baseLen:] for f in self.all0
                if f.startswith(dpath) and (f != dpath)]

    def getFile(self, path):
        """If the file doesn't exist return ''.
        """
        try:
            return self.zipfile.read(self.base + path)
        except:
            return ''

    def addFile(self, path, data):
        if isinstance(path, unicode):
            path = path.encode('utf8')
        self.zipfile.writestr(self.base + path, data)

    def addFromFile(self, filepath, path):
        if isinstance(path, unicode):
            path = path.encode('utf8')
        if isinstance(filepath, unicode):
            filepath = filepath.encode('utf8')
        self.zipfile.write(filepath, self.base + path)


def getsini(text):
    """Parse the contents of a 'sini' file, assuming it is
    structurally valid. Return a field dictionary.
    """
    # To contain the data from the file
    d = {"comment": ""}

    comment = ""    # to collect the comments

    ln = 0          # line counter
    for line in text.splitlines():
        ln += 1
        line = line.strip()
        if (not line):
            continue
        if (line[0] == '#'):
            if (comment != None):
                comment += line[1:] + "\n"
                d["comment"] = comment
            continue

        comment = None

        # A field definition (item = value)
        r = rx1.match(line)
        if not r:
            continue
        item, value = r.groups()
        # Remove quotes
        r = rx2.match(value)
        if r:
            value = r.group(1)

        d[item] = value

    return d

