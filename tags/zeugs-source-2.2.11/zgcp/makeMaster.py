#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#2007-09-15
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

from database import makeReportsDict, DBVERSION, makeReportValue
#from readData import ReadData, getPath
from dbWrapMaster import teacher2user

# Initialization info for 'config' table.
INITCONFIG = (
# Database format version
        (u"dbversion"   , DBVERSION),
# The teacher who owns this db - the master version has '' here,
        (u"me"          , u""),
# Last configuration update time
        (u"updatetime"  , u""),
# Master database stability flag (for use during updating)
        (u"unstable"    , u"1"),
# Master database finalized flag (no normal user updates)
        (u"finalized"   , u""),
# Time of last backup
        (u"backuptime"  , u""),

# The following items are used by the editor to remember the last
# report edited.
        (u"class"       , u""),
        (u"subject"     , u""),
        (u"pupilId"     , u"")
)

class MakeMaster:
    """This class handles (re)generation of a master database from
    a configuration/layout file.
    """
    def __init__(self, source, db):
        """The config file passed as an open CfgZip object in source,
        db is the master database object (DB).
        """
        self.db = db            # master database (DB) object
        self.source = source    # open CfgZip object

    def run(self, gui=None):
        self.gui = gui

        #**************** Write tables ****************
        # build or update the 'config' table
        create = self.makeConfigTable()
        if create:
            self.report(_("created 'config' table"))
        else:
            self.report(_("updated 'config' table"))

        # Create 'interface' table
        self.db.createInterfaceTable()
        self.report(_("(re)created interface table"))

        # build table for the configuration data
        self.enterData()

        # create/update reports tables
        self.report(_("creating/updating reports tables"))
        self.makeReports()

#********* This was just an idea, but it may never be used.
#        # create comments table
#        if create:
#            self.report(_("creating/updating comments table"))
#            tbname = u"comments"
#            self.db.createIVTable(tbname)

        # Flag database as stable again
        self.db.send(u"UPDATE config SET value = '' WHERE id = 'unstable'")
        self.report(_("DONE!"))

    def enterData(self):
        """Enter the configuration data files into the 'data' table.
        """
        self.db.send(u"DROP TABLE IF EXISTS data")
        self.db.createDataTable()
        # Copy over all the files, skipping directories (which end in '/')
        for f in self.source.allFiles():
            if f.endswith('/'):
                continue
            self.db.putFile(f, self.source.getFile(f))

    def makeReports(self):
        """Update the teachers' report tables, adding and removing
        tables and records where demanded by the configuration changes.
        """
        # Get a list of existing teacher tables
        ttables = self.db.getTeacherTables()
        # Get an updated list of teachers from the config data
        teachers = self.source.listFiles("teachers")

        # Create any new tables needed, and check for reports which
        # must be added or deleted
        allReports = makeReportsDict(self.source)
        for teacher in teachers:
            tbname = teacher2user(teacher)
            if tbname in ttables:
                ttables.remove(tbname)
                for rep in self.db.listIds(tbname):
                    if allReports.has_key(rep):
                        # Mark this report as already existing
                        allReports[rep] = None
                    else:
                        self.report(_("Deleting report %1"), (rep,))
                        sqldel = u"DELETE FROM %s WHERE id = ?" % tbname
                        self.db.send(sqldel, (rep,))
            else:
                self.db.createIVTable(tbname)
                self.report(_("... made %1"), (tbname,))

        self.report(_("Creating initial reports"))
        for key, t in allReports.items():
            if t:
                sqlins = u"INSERT INTO %s VALUES(?, ?)" % teacher2user(t)
                self.db.send(sqlins, (key, makeReportValue(u"", u"")))

        # Remove unneeded tables
        for tbname in ttables:
            self.report(_("... removing %1"), (tbname,))
            self.db.send(u"DROP TABLE %s" % tbname)

    def makeConfigTable(self):
        """Create or update the 'config' table.
        Return True if the table was created, else False.
        """
        tbname = u"config"
        sqlins = u"INSERT INTO %s VALUES(?, ?)" % tbname
        sqldel = u"DELETE FROM %s WHERE id = ?" % tbname
        sqlupd = u"UPDATE %s SET value = ? WHERE id = ?" % tbname
        # The createTable method does nothing if the table already exists
        created = self.db.createIVTable(tbname)
        if created:
            self.db.send(sqlins, ('dbname', self.db.getName()))
            for iv in INITCONFIG:
                self.db.send(sqlins, iv)
        else:
            self.db.send(sqlupd, (u"unstable", u"1"))
        self.db.send(sqlupd, (self.db.getTime(), u"updatetime"))
#NOTE:
# Clients should first read 'updatetime' and then 'unstable' before
# starting a synchronization process. If 'unstable', don't start,
# otherwise carry out process and check at end that 'updatetime'
# hasn't changed.
        return created

    def report(self, message, args=[]):
        # Substitute arguments
        text = argSub(message, args)
        if self.gui:
            self.gui.report(text)
