#!/usr/bin/env python
# -*- coding: utf-8 -*-

#2007-09-08
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
"""A utility to convert pupil list files in csv format to my 'sini'
(configuration file) format. Called from the configuration editor.
"""

import os
import re

from guiDialogs import getDirectory, confirmationDialog

quoteStrip = re.compile(r'"(.*)"$')


class Csv2Sini:
    def __init__(self, configEd, separator, columns):
        self.configEd = configEd
        self.colSep = separator
        self.columns = columns
        self.idcol = self.columns["id"]

    def init(self, lastDir):
        # Get the directory containing the files
        self.idir = getDirectory(_("Folder: csv-files"), lastDir)
        if isinstance(self.idir, unicode):
            self.idir = self.idir.encode('utf8')
        return self.idir

    def report(self, message):
        self.ui.report(message)

    def done(self):
        self.ui.done()

    def run(self, ui):
        minCols = 0
        for v in self.columns.values():
            if (v > minCols):
                minCols = v
        self.ui = ui
        for f in os.listdir(self.idir):
            if not f.endswith('.csv'):
                self.report(_("Ignoring '%s'") % f)
                continue

            classTag = f[:-4]   # cut off the ending
            classPath = "classes/" + classTag
            if not self.configEd.pathExists(classPath + '/'):
                self.report(_("ERROR: There is no class with tag '%s'")
                        % classTag)
                continue


            lastId = self.configEd.getField(classPath + "/info", "lastId")
            if (lastId > 0):
                if not confirmationDialog(_("Warning"),
                        _("Reloading pupil information can lead to loss"
                        " or mixing up of reports. Continue?"),
                        False):
                    continue

            self.report(_("Removing all pupils from class '%s'") % classTag)
            pupilPath = classPath + "/pupils"
            self.configEd.emptyDir(pupilPath)

            # Open the input file
            fi = os.path.join(self.idir, f)
            fih = open(fi, "rb")
            self.report(_("Fetching pupils from file '%s'") % fi)

            ln = 0
            id = 0      # counter for automatic id
            for line in fih:
                ln += 1
                line = line.strip()
                if (not line) or (line[0] == '#'):
                    continue

                # 'Strip' the individual columns
                cols = []
                for cv in [c.strip() for c in line.split(self.colSep)]:
                    r = quoteStrip.match(cv)
                    if r:
                        cv = r.group(1)
                    cols.append(cv)

                if (len(cols) < minCols):
                    self.report(_("ERROR: Insufficient columns at line %d")
                            % ln)
                    continue

                # Write out the file for this pupil
                if (self.idcol == 0 ):
                    id += 1
                    pfile = "%03d" % id
                else:
                    id -= 1
                    pfile = cols[self.idcol]
                opstring = ''
                for field, ix in self.columns.items():
                    if ix:
                        value = cols[ix - 1]
                    else:
                        value = ''
                    if (field != "id"):
                        opstring += "%s = %s\n" % (field, value)

                self.configEd.addPupil(pupilPath, pfile, opstring)

            self.report(_("Imported %d pupils\n") % abs(id))
            self.configEd.endPupils(classPath, id)

class CsvData:
    def __init__(self, setting=''):
        self.columns = {}
        self.separator = ';'
        self.setting = ';:'

        try:
            sep, fields = setting.split(":")
            self.separator = sep
            fc = {}
            for item in fields.split("|"):
                f, c = item.split("/")
                fc[f] = c
            self.setting = setting
            self.columns = fc
        except:
            pass

    def setData(self, sep, cols):
        self.columns = cols
        self.separator = sep
        cs = ""
        for f, v in cols.items():
            cs += "|%s/%d" % (f, v)
        self.setting = "%s:%s" % (self.separator, cs[1:])
