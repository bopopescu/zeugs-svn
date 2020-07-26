#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#2007-09-21
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
"""Synchronize a Zeugs database file (*.zga) with its main database.
Transfer any updated reports to the main.
"""

# Clients should first read 'updatetime' and then 'unstable' before
# starting a synchronization process. If 'unstable', don't start,
# otherwise carry out process and check at end that 'updatetime'
# hasn't changed.
from traceback import print_exc

from newPassword import getPassword
from getPw import getPw
from backup import Dump
from guiDialogs import getDirectory, getFile, confirmationDialog
from guiOutput import Output
from database import DB as DBs
from dbWrapMain import DB as DBm, teacher2user

from time import sleep
from subprocess import Popen, PIPE
import os, re

class SyncPanel:
    """There may be only one instance of this class, because of the
    slot declarations.
    """
    def __init__(self, settings):
        self.settings = settings
        # connect slots
        slot("sp_newpw", self.slot_newpw)
        slot("sp_sync", self.slot_sync)
        slot("sp_browse", self.slot_fileBrowser)

    def init(self, gui, filepath, forceDialog=False):
        self.gui = gui
        self.filepath = filepath

        # Get the path to the user database file
        self.dbs = None
        dbDir = None
        dbPath = self.settings.getSetting("dbFile")
        while True:
            if not self.filepath:
                if dbPath:
                    dbd = os.path.dirname(dbPath)
                    if os.path.isdir(dbd):
                        dbDir = dbd
                    if os.path.isfile(dbPath):
                        self.filepath = dbPath
                    dbPath = None

                if forceDialog or not self.filepath:
                    self.filepath = getFile(_("User Database File"),
                            startDir=dbDir,
                            defaultSuffix=u".zga",
                            filter=(_("Database Files"), (u"*.zga",)))
                    if not self.filepath: return

            self.dbs = DBs(self.filepath)
            if self.dbs.isOpen():
                break
            dbDir = os.path.dirname(self.filepath)
            self.filepath = None

        self.settings.setSetting("dbFile", self.filepath)

        # Set window title
        self.gui.setTitle(_("Synchronize %s") % self.filepath)

        self.dbm = None
        # Get the default host name from the 'base' data
        self.dbhost = self.dbs.baseDict[u"mainHost"]

        # Get information from the 'config' table
        self.dbname = self.dbs.getConfig(u"dbname")
        teacher = self.dbs.getConfig(u"me")
        if not teacher:
            error(_("'%s' is not a teacher's database file") % self.filepath)
        self.dbuser = teacher2user(teacher)

        # Close user database file
        self.closeFile()

        # set gui lineEdits
        self.gui.setDBinfo(self.dbhost, self.dbname, self.dbuser,
                self.filepath)

    def slot_fileBrowser(self, arg):
        self.init(self.gui, None, True)

    def slot_newpw(self, arg):
        if not self.connect():
            return
        pw = getPassword()
        if pw:
            try:
                self.dbm.setPassword(self.dbuser, pw)
                message(_("Password changed"))
            except:
                message(_("Couldn't change password"))
        self.disconnect()

    def slot_sync(self, arg):
        if self.connect():
            if (self.dbm.readValue(u"config", u"finalized") == u""):
                self.dlg = Output()
                synchronize(self.dbm, self.filepath, self.dlg)
                self.dlg.done()
            else:
                warning(_("This database is finalized, you can't access it"))
            # Disconnect from main database
            self.disconnect()

    def closeFile(self):
        """Close the user database in self.dbs
        """
        if self.dbs:
            self.dbs.close()
            self.dbs = None

    def connect(self):
        """Connect to main db.
        """
        host = self.gui.getDBhost()
        pw = getPw(host, self.dbname, self.dbuser)
        if (pw == None):
            return False
        cData = {   u"host" : host,
                    u"db"   : self.dbname,
                    u"user" : self.dbuser,
                    u"pw"   : pw
                }

        db = DBm(cData)
        if not db.isOpen():
            warning(_("Couldn't open main database"))
            return False
        self.dbm = db
        return True

    def disconnect(self):
        """Disconnect from main db.
        """
        if self.dbm:
            self.dbm.close()
            self.dbm = None


def synchronize(dbm, filepath, gui):
    """Synchronize the given file with the given (open) main database.
    """
    # Current main time
    mtime = dbm.getTime()
    # Move the user database file to backup location
    dir = os.path.dirname(filepath)
    bfile = re.sub(".zga$", "_%s.zga" % mtime, filepath)
    if (os.name == 'posix'):
        try:
            if Popen(["lsof", filepath],
                    stdout=PIPE).communicate()[0]:
                warning(_("The database file (%1) is being used"
                        " by another application"), (filepath,))
                return
        except:
            warning(_("You should install 'lsof' so that usage"
                    " of the file can be tested"))
    try:
        os.rename(filepath, bfile)
    except:
        # This trap only works on Windows. Linux will happily
        # allow you to delete a file while another program is
        # working on it! 'lsof filename' (see above) should be
        # a way to avoid that.
        warning(_("Couldn't rename the database file (%1).\n"
                "Is it being used by another application?"),
                (filepath,))
        return

    gui.report(_("Database file renamed to %s") % bfile)

    dbs = DBs(bfile)
    if not dbs.isOpen():
        os.rename(bfile, filepath)
        return

    # Teacher's report table
    teacher = dbs.getConfig(u"me")
    mtb = teacher2user(teacher)
    if mtb not in dbm.getTeacherTables():
        warning(_("%1: Owning teacher (%2) not known to main database"),
                (filepath, teacher))
        return

    gui.report(_("Copying reports from user database to main"))
    # Counter for transferred reports
    rcount = 0
    # Creation time of subordinate db, i.e. last sync time
    ctime = dbs.getConfig(u"createtime")
    # Get all updated reports
    for id, data in dbs.read(u"SELECT * FROM reports"):
        # Split off the version data
        dver, drep = data.split(u"\n", 1)
        # Get the main version data
        try:
            mver = dbm.readValue(mtb, id).split(u"\n", 1)[0]
        except:
            gui.report(_("Invalid report, not updated : %s") % id)

        if (mver > ctime):
            if confirmationDialog(_("Report update problem"),
                    _("Main version of report has been updated"
                    " since this client was last synchronized.\n"
                    "   Replace that version of '%s'?") % id, False):
                gui.report(_("Revised main version of report '%s'"
                        " will be overwritten") % id)
            else:
                gui.report(_("Revised main version of report '%s'"
                        " not overwritten") % id)
                continue

        elif (dver <= mver):
            # Only do anything if the local version is newer than the
            # the main version
            continue

        if (dver > mtime):
            # The new version has a time stamp later than the
            # current time on the main, adjust it
            if dver.endswith(u"$"):
                dver = mtime + u"$"
            else:
                dver = mtime

        try:
            sqlupd = u"UPDATE %s SET value = ? WHERE id = ?" % mtb
            dbm.send(sqlupd, (dver + u"\n" + drep, id))
            rcount += 1
        except:
            gui.report(_("Couldn't update report '%s'") % id)

    gui.report(_("Transferred %d reports") % rcount)

    # Close the user database
    dbs.close()

    # Remember the latest sync time
    if rcount:
        dbm.send(u"""UPDATE interface SET value = ?
                    WHERE id = 'lastsynctime'""", (mtime,))

    # Recreate the user database
    gui.report(_("Recreating the user database"))
    recreate(dbm, filepath, teacher, gui)

def recreate(dbm, filepath, user, gui):
    """Recreate the user database, taking main update lock
    into consideration. NOTE that this 'lock' is not 100%
    effective, but it is a simple method which I hope will be
    adequate for the envisaged application.
    """
    dir = os.path.dirname(filepath)
    while True:
        udt = getudtime(dbm)
        if not mUnstable(dbm):
            break
        gui.report(_("Main database is in unstable state.\n  Waiting ..."))
        sleep(10)

    # Dump the main database to the selected file
    while True:
        dump = Dump(dbm, dir, user)
        if dump.filepath:
            break
        warning(_("Couldn't create database file in folder %1,"
                " select new folder"), (dir,))
        dir = getDirectory(dir)
        if not dir:
            if confirmationDialog(_("Abandon?"),
                    _("User database not regenerated,"
                    " do you really want to abandon this operation?"), False):
                break

    if dump.filepath:
        dump.run(gui)

    fp = dump.filepath
    dump = None
    if fp:
        # Check main database hasn't been updated
        if (udt == getudtime(dbm)):
            gui.report(_("\nSUCCESS! - User database regenerated"))
        else:
            gui.report(_("Main has been updated,"
                    " need to repeat...\n"))
            recreate(dbm, filepath, user, gui)
    else:
        gui.report(_("\nFAILED! Couldn't regenerate user database.\n"
                " --- Please contact administrator!"))

def getudtime(dbm):
    """Fetch the last update time of the main database.
    """
    return dbm.readValue(u"config", u"updatetime")

def mUnstable(dbm):
    """Return True if the main database is unstable (itself
    being updated)
    """
    return (dbm.readValue(u"config", u"unstable") != u"")
