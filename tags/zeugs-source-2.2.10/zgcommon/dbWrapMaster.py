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
"""A wrapper for the main database functions. PostgreSQL version.

Allows relatively easy switching to another DB management/access scheme.
Texts should be in unicode.

The connection is run in 'AUTOCOMMIT' mode, for simplicity.
"""

# The main administrative user for Zeugs control panel
ADMIN = u"zgadmin"
# Group (nologin) roles
USERROLE = u"zguser"            # normal user

DEFAULTPASSWORD = u"None"       # for normal users

# Prefixed to teacher tag to creat corresponding report table and
# database user (see teacher2user())
USERPREFIX = u"z_"

def teacher2user(teacherTag):
    """This is the function to get the main database user role
    corresponding to the given teacher. It is the same as the name
    of that teacher's report table.
    """
    return USERPREFIX + teacherTag

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT, \
        register_type, UNICODE
from guiDialogs import confirmationDialog

class DB:
    """A simple wrapper for a database.
    """
    def __init__(self, cData):
        self.dbhost = cData[u"host"]
        self.dbdb = cData[u"db"]
        self.dbuser = cData[u"user"]
        self.dbpasswd = cData[u"pw"]
        # Save a description of this db for error reporting, etc.
        # Exactly what form this takes depends on the engine.
        # For sqlite just use the path to the file.
        self.descriptor = u"Host (%s), Database (%s), User (%s)" % \
                (self.dbhost, self.dbdb, self.dbuser)
        try:    # this will throw an exception if it fails:
            self.db = psycopg2.connect('host=%s dbname=%s user=%s password=%s'\
                    % (self.dbhost, self.dbdb, self.dbuser, self.dbpasswd))
            self.db.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # This should cause psycopg2 to read and write unicode ...
            register_type(psycopg2.extensions.UNICODE)
            self.dbcur = self.db.cursor()
        except:
            self.db = None

    def isOpen(self):
        return self.db

    def getName(self):
        return self.dbdb

    def execute(self, cmd, args):
        self.dbcur.execute(cmd.replace(u"?", u"%s"), args)

    def read(self, cmd, args=None):
        self.execute(cmd, args)
        return self.dbcur.fetchall()

    def read1(self, cmd, args=None):
        self.execute(cmd, args)
        return self.dbcur.fetchone()

    def send(self, cmd, args=None):
        self.execute(cmd, args)
#        self.db.commit()

    def commit(self):
#        self.db.commit()
        pass

    def getTables(self):
        """Get a list of tables defined for this database.
        """
        rows = self.read(u"""SELECT tablename FROM pg_tables
                WHERE schemaname = 'public'""")
        return [r[0] for r in rows]

    def createIVTable(self, name):
        """Create a 2-column table.
        Returns True if it succeeded, else False.
        """
        sqlcom = u"CREATE TABLE %s(id TEXT, value TEXT)" % name
        try:
            self.send(sqlcom)
            return True
        except:
#            self.db.commit()
            #raise
            return False

    def createDataTable(self):
        """Returns True if it succeeded, else False.
        """
        try:
            self.send(u"CREATE TABLE data(id TEXT, value BYTEA)")
            return True
        except:
#            self.db.commit()
            #raise
            return False

    def putFile(self, id, data):
        """Enter a record into the 'data' table. The data should be
        a (utf8) string or binary.
        """
        self.send(u"INSERT INTO data VALUES(?, ?)", (id, buffer(data)))

    def getFile(self, path):
        """Return the contents of the 'data' file at the given (data)
        path. The file is converted to unicode.
        """
        val = self.readValue(u"data", path)
        #print type(val)
        return str(val).decode('utf8')

    def getBFile(self, path):
        """Return the contents of the 'data' file at the given (data)
        path. The file is not converted to unicode.
        """
        return str(self.readValue(u"data", path))

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
#            self.db.commit()
            #raise
            return False

    def readValue(self, table, id):
        """Get the value (assuming only 1 value!) for the given
        'id' field of the given table.
        """
        return self.read1(u"SELECT value FROM %s WHERE id = ?" % table,
                (id,)) [0]

    def listIds(self, table):
        """Return a list of all 'id'-field entries for a table.
        """
        return [i[0] for i in self.read(u"SELECT DISTINCT id FROM %s" % table)]

    def getDataValue(self, id):
        """Fetch the contents of the given data file - as a 'str' (8-bit),
        not unicode.
        """
        return str(self.read1(u"SELECT value FROM data WHERE id = ?") [0])

    def getAllData(self):
        """This returns all files in the 'data' table as (path, data)
        pairs. It returns 8-bit data, not unicode.
        """
        return [(path.decode('utf8'), str(data))
                for path, data in
                self.read(u"SELECT id, value FROM data")]

    def getTeacherTables(self):
        """Get a list of existing teacher tables.
        """
        return [t for t in self.getTables() if t.startswith(USERPREFIX)]

    def newSequence(self, name):
        """A simple sequence generator using the 'SEQUENCE' feature
        of PostgreSQL.
        A sequence is created with the SQL command:
           CREATE SEQUENCE name;
        The first value returned is 1.
        """
        self.send(u"DROP SEQUENCE IF EXISTS %s" % name)
        self.send(u"CREATE SEQUENCE %s" % name)

    def sequence(self, name):
        """Return the next value in the sequence.
        """
        return self.read1(u"SELECT nextval('%s')" % name)[0]

    def seqText(self, name):
        return u"%06d" % self.sequence(name)

    def description(self):
        """Get a short description of the database connection.
        """
        return self.descriptor

    def getUsers(self):
        """Get a list of existing users for the database system.
        """
        rows = self.read(u"SELECT rolname FROM pg_roles")
        return [r[0] for r in rows]

    def userExists(self, user):
        """Return True if given user exists as a role.
        """
        if self.read1(u"""SELECT rolname FROM pg_roles
                WHERE rolname = ?""", (user,)):
            return True
        else:
            return False

    def createMainAdmin(self, pw):
        """This creates an administrator account which can create
        databases and users. pw is the password.
        """
        self.newRole(ADMIN, u"""LOGIN CREATEDB CREATEROLE
                 ENCRYPTED PASSWORD '%s'""" % pw)

    def createGroupRole(self, name):
        """This creates a group role, whose rights are inherited
        by subsidiary users/admins.
        """
        self.newRole(name, u"NOLOGIN")

    def createRole(self, name, rtype=USERROLE, pw=DEFAULTPASSWORD):
        """This creates a user account, which inherits its rights
        from the role 'rtype'.
        """
        # I have put "" around the role name because it wouldn't
        # otherwise accept the role 'in' (single quotes also didn't
        # work)
        self.newRole(name, u"""LOGIN ENCRYPTED PASSWORD '%s'
                IN ROLE %s""" % (pw, rtype))

    def newRole(self, name, properties):
        """Create a new role (user) with the given properties.
        If the user exists already, try to delete it. If that
        doesn't work, ask if its properties should be altered.
        If even that fails (or is rejected) raise an exception.
        """
        try:
            self.send(u"DROP ROLE IF EXISTS %s" % name)
        except:
            pass
        if self.userExists(name) and confirmationDialog(
                _("Problem removing user"),
                _("Couldn't drop user '%s'.\n"
                  "Alter its properties?") % name, True):
            com = u"ALTER"
        else:
            com = u"CREATE"

        self.send(com + u" ROLE " + name + u" WITH " + properties)

    def setPassword(self, name, pw='None'):
        self.send(u"""ALTER ROLE "%s" ENCRYPTED PASSWORD '%s'""" % (name, pw))

    def dropRole(self, name):
        self.send(u"""DROP ROLE "%s" """ % name)

    def getRoles(self):
        """Return a list of all db users (roles).
        """
        rows = self.read(u"SELECT rolname FROM pg_roles")
        return [r[0] for r in rows]

    def getTime(self):
        """Return the server time in the format:
            yyyymmdd_hhmmss
        """
        t = unicode(self.read1(u"SELECT LOCALTIMESTAMP(0)")[0])
        return t.replace(u" ", u"_").replace(u"-", u"").replace(u":", u"")

    def createInterfaceTable(self):
        """A small table which can be updated by all users, at present
        only used as a bodge to allow last synchronization time to be
        recorded.
        """
        tbname = u"interface"
        self.send(u"DROP TABLE IF EXISTS %s" % tbname)
        self.createIVTable(tbname)
        sqlins = u"INSERT INTO %s VALUES(?, ?)" % tbname
        self.send(sqlins, (u"lastsynctime", u""))

    def close(self):
        self.db.close()
        self.db = None



if __name__ == '__main__':
    # A simple example showing how to set this up
    dbd = { u"host" : u"localhost",
            u"db"   : u"zeugscontrol",
            u"user" : u"zgadmin",
            u"pw"   : u"adm"
          }
    db = DB(dbd)
    #print db.read(u"SELECT * FROM one")
    #cur = db.db.cursor()
    #cur.execute(u"CREATE TABLE users (id INT PRIMARY KEY, name TEXT)")
    #cur.execute(u"CREATE TABLE users2 (id INT PRIMARY KEY, name TEXT)")
    #db.db.commit()
    db.send(u"""CREATE TABLE users (id INT PRIMARY KEY,
            name TEXT)""")
