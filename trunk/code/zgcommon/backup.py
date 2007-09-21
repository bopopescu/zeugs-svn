# -*- coding: UTF-8 -*-

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
"""This module deals with dumping and restoring a master database.
The dump is an sqlite database file.
A variation of dumping is also supported where only the files
relevant to a single teacher are dumped, for use in the report editor.
"""
from traceback import print_exc

from dbWrap import DB as DBn
from database import DB, makeReportsDict, readData
from dbWrapMaster import teacher2user
from guiDialogs import confirmationDialog

import os
import re

def checkOverwrite(path, force):
    """If the file exists, ask whether to delete it and return the
    answer. If the answer was affirmative, delete the file.
    If the end result is that there is now no file of that name,
    return True, else False.
    """
    if os.path.exists(path):
        if force or confirmationDialog(_("Overwrite?"),
                _("File '%s' exists already. Delete it?") % path):

            try:
                os.remove(path)
            except:
                warning(_("Couldn't delete file '%s'") % path)
                return False

        else:
            return False
    return True

class Dump:
    """Create a slave (sqlite) database file in the given directory.
    It can be a backup/print file (no teacher), or a teacher's
    database file.
    teacher's file: <dbname>_<teacher>.zga
            an existing one cannot be overwritten.
    backup/print file: <dbname>_<time>.zgb
    The constructor opens the sqlite file, the method 'run' does the backup.

    Note that in dump files all the reports are collected in a single
    table, 'reports', as user authentication is not relevant here.
    """
    def __init__(self, dbm, dir, teacher=u""):
        self.dbm = dbm
        self.dbname = self.dbm.getName()
        self.teacher = teacher
        self.ctime = self.dbm.getTime()

        if teacher:
            # The filename is of the form 'dbname'_'user'.zga
            filename = u"%s_%s.zga" % (self.dbname, teacher)
            force = False
        else:
            # The filename is of the form 'dbname'_'time'.zgb
            filename = u"%s_%s.zgb" % (self.dbname, self.ctime)
            force = True

        self.filepath = os.path.join(dir, filename)
        if not checkOverwrite(self.filepath, force):
            self.filepath = None
            return
        # Create/open database file
        self.dbs = DBn(self.filepath, new=True)

        if not self.dbs.isOpen():
            self.filepath = None
            return

    def run(self, gui):
        """Copy the master database to the slave.
        """
        try:
            # Create tables
            table = u"config"
            gui.report(_("Creating table '%s'") % table)
            self.makeTable(table)
            self.dumpTable(table)

            gui.report(_("Creating table 'data'"))
            self.dbs.createDataTable()
            if self.teacher:
                # Don't dump the image files, just that for the current teacher
                self.dumpDataTable(r"(?!imagefiles/)|imagefiles/teachers/%s\."
                        % self.teacher)
            else:
                self.dumpDataTable()

            # Copy reports
            gui.report(_("Copying reports ..."))
            table = u"reports"
            self.makeTable(table)
            if self.teacher:
                # Database user for self.teacher (also report table name)
                user = teacher2user(self.teacher)

                # Only copy the owner's reports
                self.dumpTable(user, table)

            else:
                for tm in self.dbm.getTeacherTables():
                    self.dumpTable(tm, table)

#********* This was just an idea, but it may never be used.
#            # Copy comments
#            gui.report(_("Copying comments ..."))
#            table = u"comments"
#            self.makeTable(table)
#            if self.teacher:
#                # Only copy comments pertaining to the owner's reports
#                okIds = self.dbm.listIds(user)
#                for c in self.dbm.listIds(table):
#                    if c in okIds:
#                        for v in self.dbm.read(u"""SELECT value FROM comments
#                                WHERE id = ?""", (c,)):
#                            self.dbs.send(u"""INSERT INTO comments
#                                    VALUES(?, ?)""", (c, v[0]))
#
#            else:
#                self.dumpTable(table)

            if self.teacher:
                # Set creation time
                self.dbs.send(u"""INSERT INTO config
                        VALUES('createtime', ?)""", (self.ctime,))

                # Set db-file 'owner'
                self.dbs.send(u"""UPDATE config SET value = ?
                    WHERE id = 'me'""", (self.teacher,))

            else:
                # Set the last backup time
                self.dbs.send(u"""UPDATE config SET value = ?
                        WHERE id = 'backuptime'""", (self.ctime,))
                self.dbm.send(u"""UPDATE config SET value = ?
                    WHERE id = 'backuptime'""", (self.ctime,))

            self.dbs.close()
            self.dbs = None
            gui.report(_("DONE!"))

        except:
            print_exc()

            message(_("Couldn't create database file."
                    " Removing incomplete file (%1)"), (self.filepath,))
            if self.dbs.isOpen():
                self.dbs.close()
            os.remove(self.filepath)
            self.dbs = None
            self.filepath = None

            #raise

    def makeTable(self, name):
        """Create a new database table with the given name and
        standard text fields 'id' and 'value'.
        """
        if not self.dbs.createIVTable(name):
            message(_("Couldn't create table '%1'"), (name,))
            raise

    def dumpTable(self, name, name2=None, filter=".+"):
        """Copy the contents of table name from the master to
        table name2 in the slave. If name2 is not given use name.
        Both tables are assumed to have the 'standard' fields 'id'
        and 'value'.
        Only copy if the 'id' field matches the filter expression.
        """
        rx = re.compile(filter)
        if not name2:
            name2 = name
        sqlsel = u"SELECT * FROM %s" % name
        sqlins = u"INSERT INTO %s VALUES(?, ?)" % name2
        for row in self.dbm.read(sqlsel):
            if rx.match(row[0]):
                self.dbs.send(sqlins, row)

    def dumpDataTable(self, filter=".+"):
        """Copy the files from the table 'data' from master to slave.
        Only copy if the 'id' field matches the filter expression.
        """
        rx = re.compile(filter)
        for id in self.dbm.listIds(u"data"):
            if rx.match(id):
                self.dbs.putFile(id, self.dbm.getBFile(id))

class Restore:
    """Recreate a master database from a backup file (<dbname>_<time>.zgb)
    """
    def __init__(self, dbpath):
        # Open database file
        self.dbs = DB(dbpath)

    def getDbName(self):
        """Return the database name, as stored in the 'config' table.
        If something went wrong with opening the database, None
        will be returned.
        """
        try:
            return self.dbs.getConfig(u"dbname")
        except:
            return None

    def close(self):
        if self.dbs.isOpen():
            self.dbs.close()
        self.dbs = None

    def setMaster(self, dbm):
        """Used by client objects to select the master database.
        """
        self.dbm = dbm

    def run(self, gui):
        """Given a fresh empty master database in self.dbm, fill it from
        the open backup database file (self.dbs).
        """
        try:
            # Create tables
            t = u"config"
            gui.report(_("Creating table '%s'") % t)
            self.makeTable(t)
            self.restoreTable(t)
            gui.report(_("Creating table 'data'"))
            self.dbm.createDataTable()
            self.restoreDataTable()

            self.dbm.createInterfaceTable()
            gui.report(_("Created interface table"))

            # Copy reports
            gui.report(_("Creating teacher report tables ..."))
            t = u"reports"
            # Get list of teachers from configuration data
            for tch in self.dbs.listAllFiles(u"teachers/"):
                self.makeTable(teacher2user(tch[9:]))

            # Parse all class configuration data, to determine
            # ownership of reports
            reports = makeReportsDict(self.dbs)

            for id, value in self.dbs.read(u"SELECT * FROM %s" % t):
                table = teacher2user(reports[id])
                sqlins = u"INSERT INTO %s VALUES(?, ?)" % table
                self.dbm.send(sqlins, (id, value))

#********* This was just an idea, but it may never be used.
#            # Copy comments
#            gui.report(_("Copying comments ..."))
#            t = "comments"
#            self.makeTable(t)
#            self.restoreTable(t)

            gui.report(_("DONE!"))

        except:
            print_exc()
            message(_("Couldn't restore database"))

            self.dbm = None

        self.close()

    def makeTable(self, name):
        """Create a new database table with the given name and
        standard text fields 'id' and 'value'.
        """
        if not self.dbm.createIVTable(name):
            message(_("Couldn't create table '%1'"), (name,))
            raise

    def restoreTable(self, name, name2=None):
        """Copy the contents of table name from the slave to
        table name2 in the master. If name2 is not given use name.
        Both tables are assumed to have the 'standard' fields 'id'
        and 'value'.
        """
        if not name2:
            name2 = name
        sqlsel = u"SELECT * FROM %s" % name
        sqlins = u"INSERT INTO %s VALUES(?, ?)" % name2
        for row in self.dbs.read(sqlsel):
            self.dbm.send(sqlins, row)

    def restoreDataTable(self):
        """Copy the files from the table 'data' from master to slave.
        """
        for id in self.dbs.listIds(u"data"):
            self.dbm.putFile(id, self.dbs.getBFile(id))

