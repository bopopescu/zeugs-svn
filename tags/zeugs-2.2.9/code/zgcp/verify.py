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
"""A class to verification of the data/configuration files.
"""
import traceback

from PyQt4 import QtCore, QtGui

import os
import re


class Validate:
    def __init__(self):
        self.verifyFunctions = {
            # functions for the layout files
                "!pageList" : self.vPageList,
                "!subjectList" : self.vSubjectList,
                "!fontFamily" : self.vFontFamily,
                "!frameList" : self.vFrameList,

            # functions for the school data files
                "!subject" : self.vSubject,
            }

    def init(self, fileDict):
        self.fileDict = fileDict

    def checkValue(self, value, info, path):
        """Verify the value of a field definition.
        Return u'' if the value is acceptable, otherwise an error
        description.
        """
        v = info[0]     # Verification type
        if not v:
            return ''
        self.path = path
        if v.startswith('!'):   # call an indirect verification function
            #print "Indirect Check:"
            r = self.verifyFunctions[v](value)
        elif (v == 'flt'):
            r = self.verifyFlt(value, info)
        elif (v == 'int'):
            r = self.verifyInt(value, info)
        elif (v == 'bool'):
            r = self.verifyBool(value, info)
        elif (v == 'table'):
            r = self.verifyTable(value, info[1])
        elif (v == 'table?'):
            # Also '0' is acceptable
            r = self.verifyTable(value, info[1], '0')
        elif (v == 'colour'):
            r = self.verifyColour(value, info)
        elif (v == 'choice'):
            r = self.verifyChoice(value, info)
        else:
            error(_("BUG - Unknown verification test, '%s'") % v)
        return r

    def verifyInt(self, value, info):
        min = int(info[2])
        max = int(info[3])
        try:
            e = int(value)
            if (e >= min) and (e <= max):
                return ''
        except:
            pass
        return _("Invalid 'integer' value")

    def verifyFlt(self, value, info):
        min = float(info[2])
        max = float(info[3])
        try:
            e = float(value)
            if (e >= min) and (e <= max):
                return ''
        except:
            pass
        return _("Invalid 'real' value")

    def verifyBool(self, value, info):
        if value in ('0', '1'):
            return ''
        return _("Invalid 'boolean' value")

    def verifyColour(self, value, info):
        if re.match("#[0-9a-fA-F]{6}$", value):
            return ''
        return _("Invalid 'colour' value")

    def verifyChoice(self, value, info):
        choices = info[2].split()
        if (value in choices):
            return ''
        return _("Must be one of %s") % repr(choices)

    def verifyTable(self, value, table, null=None):
        if (value != null):
            if (table[0] == "@"):
                path = table[1:]
            else:
                path = self.path
                while table and (table[0] == "^"):
                    table = table[1:]
                    path = path.rsplit("/", 1)[0]

                if table:
                    path += "/" + table

            path += "/" + value

            if (not self.checkFile(path)):
#                print value, table, self.path, path
                return _("Referenced item not defined")
        return ''


    def vPageList(self, value):
        """Check that definitions exist for the listed page names.
        """
        pages = value.split()
        result = ''
        while pages:
            p = pages[0]
            pages = pages[1:]
            if self.verifyTable(p, "^pages"):
                result += _("Page has no definition: '%s'\n") % p
        return result

    def vSubjectList(self, value):
        """Check the subjects in the list (possibly in groups with
        a '|' separator) against the keys in the 'subject_frames'
        table. Also check any frame index suffices.
        """
        result = ''
        for ss in value.split():
            for s in ss.split('|'):
                sf = s.split('.')
                try:
                    if (len(sf) == 1):
                        fx = 1
                    elif (len(sf) == 2):
                        fx = int(sf[1])
                        if (fx < 1):
                            raise
                    else:
                        raise

                    path = (self.path.rsplit('/', 2)[0] +
                            "/subject_frames/" + sf[0])
                    if not self.checkFile(path):
                        return _("Subject not found in 'subject_frames' folder")
                    if (fx > len(self.getValue(path, "frames").split())):
                        result += _("Insufficient frames for subject (%s)\n") % s
                except:
#                    traceback.print_exc()
                    result += _("Invalid subject (%s) in subject block\n") % s
        return result

    def vFontFamily(self, value):
        """Check that the font family is available.
        """
        f = QtGui.QFont(value)
        fi = QtGui.QFontInfo(f)
        if (fi.family() != f.family()):
            return _("Font not available: %s") % value
        return ''

    def vFrameList(self, value):
        """Check the frames in the list against the 'frames' keys.
        """
        for f in value.split():
            val = self.verifyTable(f, "^^frames")
            if val:
                return val
        return ''

    def vSubject(self, value):
        """This is called for the subject (tag) field in the subjects
        table. There must be a corresponding entry in the
        'subject_frames' table of the corresponding layout.
        In the case of subject tags with a '-', if the whole tag
        has no entry, then the part before the '-' will be tried.
        """
        basepath = self.path.rsplit("/", 2)[0]
        layout = self.getValue(basepath + "/info", "Layout")
        sfpath = "@layouts/" + layout + "/subject_frames"
        v1 = self.verifyTable(value, sfpath)
        s0 = value.rsplit("-", 1)[0]
        if (s0 == value) or (v1 == ''):
            return v1
        return self.verifyTable(s0, sfpath)

    def getValue(self, path, field):
        """Get the value of the field in the data structure at node 'path'.
        """
        try:
            file = self.fileDict[path]
            for i in self.fileDict[path][4]:
                if (i[0] == field):
                    return i[1]
        except:
            pass
        return None

    def checkFile(self, path):
        """Check that the given path exists in the data structure.
        It doesn't differentiate between files and folders.
        """
        return self.fileDict.has_key(path) or self.fileDict.has_key(path+'/')

    def validateAll(self):
        """Check all fields of all files, returning a dictionary of
        colouring instructions for all the nodes in the tree.
        The keys are the paths and the values may be:
            0: Normal
            1: Contains error
            -1: Image file (not managed by this editor)
        """
        self.errorCount = 0     # Maintain an error counter
        # Note that the number of errors returned is the number of
        # files containing errors.
        tags = {}
        for fd, fddata in self.fileDict.items():
            if (fddata[1] == "="):
                # Information file
                tags[fd] = 0
                for sec in fddata[4]:
                    if self.checkValue(sec[1], sec[2], fd):
                        self.errorCount += 1
                        tags[fd] = 1
                        # Mark all enclosing folders
                        while True:
                            fd = fd.rsplit('/', 1)[0]
                            fdx = fd + '/'
                            if tags.get(fdx):
                                break
                            tags[fdx] = 1
                        break

            elif (fddata[1] == "/"):
                # Folder
                if not tags.get(fd):
                    tags[fd] = 0

            elif (fddata[1] == "i"):
                # Image file
                tags[fd] = -1

            else:
                bug(_("Unknown node type -'%s'") % fd)

        return tags
