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
"""A wrapper for the database functions. (SQLITE)

Allows relatively easy switching to another DB management/access scheme.
At present the interface uses 'unicode' for text items, 'str' (8-bit)
data for the value field of the 'data' table.
"""

import sys
import os.path

try:
    import sqlite3 as sqlite
except:
    from pysqlite2 import dbapi2 as sqlite


class DB:
    """A simple wrapper for a database.
    """
    def __init__(self, dbpath, new=False):
        self.db = None
        # Save a description of this db for error reporting, etc.
        # Exactly what form this takes depends on the engine.
        # For sqlite just use the path to the file.
        self.descriptor = dbpath
        if new:
            if os.path.exists(dbpath):
                warning(_("Couldn't create database file '%1':\n"
                        "    File exists already"), (dbpath,))
            else:
                try:    # this will throw an exception if it fails:
                    self.db = sqlite.connect(dbpath)
                except:
                    warning(_("Couldn't create database file '%1'"), (dbpath,))
            return

        if os.path.exists(dbpath):
            try:    # this will throw an exception if it fails:
                self.db = sqlite.connect(dbpath)
                return
            except:
                pass

        warning(_("Couldn't open database file '%1'"), (dbpath,))

    def isOpen(self):
        return (self.db != None)

    def read(self, *cmd):
        return self.db.execute(*cmd).fetchall()

    def read1(self, *cmd):
        return self.db.execute(*cmd).fetchone()

    def send(self, *cmd):
        self.db.execute(*cmd)

#    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()
        self.db = None

    def sequence(self, name, min=0):
        """A simple sequence generator using the 'config' table.
        """
        # Must be done with the database locked, in case parallel
        # accesses are taking place.
        self.db.isolation_level = None
        cur = self.db.execute(u"BEGIN EXCLUSIVE")
        cur.execute(u"""SELECT Value FROM config
                WHERE Item = ?""", (name,))
        val = int(cur.fetchone()[0]) + 1
        if (val <= min):
            val = min + 1
        cur.execute(u"""UPDATE config SET Value = ?
                WHERE Item = ?""", (unicode(val), name))
        cur.execute(u"COMMIT")
        self.db.isolation_level = ""
        return val

    def createIVTable(self, name):
        """Create a 2-column table.
        Returns True if it succeeded, else False.
        """
        sqlcom = u"CREATE TABLE %s(id TEXT, value TEXT)" % name
        try:
            self.send(sqlcom)
            return True
        except:
            self.db.commit()
            return False

    def createDataTable(self):
        """Returns True if it succeeded, else False.
        """
        try:
            self.send(u"CREATE TABLE data(id TEXT, value BLOB)")
            return True
        except:
            self.db.commit()
            return False

    def createTable(self, name, columns):
        """Returns True if it succeeded, else False.
        """
        sqlcom = u"CREATE TABLE %s(%s TEXT" % (name, columns[0])
        for c in columns[1:]:
            sqlcom += u", %s TEXT" % c
            sep = u", "
        sqlcom += u")"
        try:
            self.send(sqlcom)
            return True
        except:
            self.db.commit()
            return False

    def readValue(self, table, id):
        """Get the value (assuming only 1 value!) for the given
        'id' field of the given table.
        """
        return self.read1(u"SELECT value FROM %s WHERE id = ?" % table,
                (id,)) [0]

    def putFile(self, id, data):
        """Enter a record into the 'data' table. The data should be
        a (utf8) string or binary.
        """
        self.send(u"INSERT INTO data VALUES(?, ?)", (id, buffer(data)))

    def getFile(self, path):
        """Return the contents of the 'data' file at the given (data)
        path. The file is converted to unicode.
        """
        return str(self.readValue(u"data", path)).decode('utf8')

    def getBFile(self, path):
        """Return the contents of the 'data' file at the given (data)
        path. The file is not converted to unicode.
        """
        return str(self.readValue(u"data", path))

    def listIds(self, table):
        """Return a list of all 'id'-field entries for a table.
        """
        return [i[0] for i in self.read(u"SELECT DISTINCT id FROM %s" % table)]

    def description(self):
        """Get a short description of the database connection.
        """
        return self.descriptor
