# -*- coding: utf-8 -*-

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
"""The main module of the Zeugs control panel application.
"""

from traceback import print_exc
import os
from shutil import copyfile
import re

from dbWrapMain import DB as DBm, ADMIN, USERROLE, \
        DEFAULTPASSWORD, teacher2user
from guiDialogs import getDirectory, confirmationDialog, getFile
from makeMain import MakeMain
from guiReport import guiReport
from backup import Dump, Restore
from database import DB as DBs, sini2dict
from guiPrint import GuiPrint
from synchronize import synchronize
from guiOutput import Output
from fileHandler import CfgZip
from guiConfigEd import GuiConfigEd

class ControlPanel:
    """There may be only one instance of this class, because of the
    slot declarations.
    """
    def __init__(self, settings):
        self.main = None      # The (reports) main database
        self.settings = settings # Coniguration persistence facility
        # The following item remembers the printer instance
        # started from the control panel, so that it can be started
        # multiple times.
        self.printHandler = None
        self.configEd = None

        slot("cp_newdb", self.slot_newdb)
        slot("cp_updatedb", self.slot_updatedb)
        slot("cp_dbdel", self.slot_deletedb)
        slot("cp_newdbIndex", self.slot_newdbIndex)
        slot("cp_dump", self.slot_dump)
        slot("cp_genTdb", self.slot_genTeacherDb)
        slot("cp_restore", self.slot_restore)
        slot("cp_finalize", self.slot_finalize)
        slot("cp_selTeachers", self.slot_selectTeachers)
        slot("cp_finalize", self.slot_finalize)
        slot("cp_pwd", self.slot_pwReset)
        slot("cp_print", self.slot_print)
        slot("cp_sync", self.slot_sync)
        slot("cp_restoreDataFiles", self.slot_restoreConfigFile)
        slot("ced_done", self.slot_reEnable)

    def init(self, gui, db):
        self.gui = gui
        self.db = db            # The control database
        self.gui.setDBhost(self.db.dbhost)

        self.initDBlist()

    def initDBlist(self):
        rows = self.db.read(u"""SELECT id, name FROM databases
                ORDER BY id DESC""")
        self.dbList = [item[1] for item in rows]

        self.gui.setDBlist(self.dbList)

    def addUser(self, login):
        """Add a new 'normal' user, with limited rights.
        """
        if self.db.userExists(login):

            if confirmationDialog(_("User name problem"),
                    argSub(_("User '%1' already exists. Try to recreate?"),
                    (login,)), True):

                if not self.removeUser(login):
                    raise

        try:
            self.db.createRole(login, USERROLE)
        except:
            #print_exc()
            message(_("Database Problem: Couldn't create user '%1'"),
                    (login,))
            raise

    def connect(self, dbname):

        cData = {}
        cData[u"host"] = self.db.dbhost
        cData[u"db"] = dbname
        cData[u"user"] = self.db.dbuser
        cData[u"pw"] = self.db.dbpasswd

        return DBm(cData)

    def getConfigData(self, newdb):
        """Prepare a configuration data source.
        Initially the configuration editor is started to ensure that
        the selected file is valid. When this is quitted, the
        resulting file can be used, so long as it was error-free.
        newdb is True when a new database is to be created, otherwise
        the current database is to be updated.
        """
        self.newdb = newdb
        if not self.configEd:
            self.configEd = GuiConfigEd("cfged")
        self.configEd.init()
        self.configEd.run()
        # Now wait until the editor has finished.
# Actually, I would need the editor to be modal.
# Maybe an alternative would be to disable the control panel until
# a done signal is received:
        self.gui.setEnabled(False)

    def slot_reEnable(self, arg):
        """Handle updating and creation of database from
        a configuration file.
        Here the configuration editor has finished.
        """
        self.gui.setEnabled(True)
        if not self.configEd.getSourcePath():
            message(_("No data source"))
            return
        errors = self.configEd.getErrorCount()
        if ( errors > 0):
            message(_("%d files containing errors found") % errors)
            return

        source = CfgZip(self.configEd.getSourcePath())
        if not source.isOpen():
            warning(_("The supplied configuration file (%s) could not"
                    " be opened. Actually this shouldn't be possible!")
                            % self.configEd.getSourcePath())
            return
        if self.newdb:
            self.createNewDb(source)
        else:
            self.updateDbConfig(source)
        source.close()

    def slot_newdb(self, arg):
        """Create a new reports database from a layout/config file.
        """
        self.getConfigData(True)

    def createNewDb(self, source):
        """Create a new database using the configuration file supplied
        as a CfgZip object in source.
        """
        dbname = source.cfgName
        state = 0
        try:
            self.db.send(u"""CREATE DATABASE %s
                    OWNER %s ENCODING 'UTF8'""" % (dbname, ADMIN))
            state = 1
            # Add to 'databases' table
            self.db.send(u"INSERT INTO databases VALUES (?, ?, ?, ?)",
                    (self.db.getTime(), dbname, u'', u''))
            state = 2

            newmain = self.connect(dbname)
            state = 3

            guimessage = argSub(_("New database '%1' created, now read in the data"),
                    (dbname,))
            mm = MakeMain(source, newmain)
            guiReport(_("Create New Database"), mm, guimessage)
            #message(_("New database now set up"))

            self.usersPrivileges(newmain)
            # Ensure connection is closed
            mm = None
            newmain.close()
            newmain = None

        except:
#            print_exc()

            message(_("Couldn't create new database (%1)"), (dbname,))
            if (state >= 3):
                newmain.close()
            if (state >= 2):
                self.db.send(u"DELETE FROM databases WHERE name = ?",
                        (dbname,))
            if (state >= 1):
                self.db.send(u"DROP DATABASE %s" % dbname)

        # adjust display, select new db
        self.initDBlist()

    def slot_updatedb(self, arg):
        """Update the current reports database from a layout/config file.
        """
        self.getConfigData(False)

    def updateDbConfig(self, source):
        """Update the current database using the configuration file supplied
        as a CfgZip object in source.
        The selected config file must match the name of the current database.
        Before updating from this file, dump the current database state
        to a folder 'dumps' in the same folder as the config file.
        That is in case something goes wrong and the old state must be
        recovered.
        """
        if (self.dbname != source.cfgName):
            message(_("Database name does not match data folder"))
            return

        # Backup existing database state.
        sPath = self.configEd.getSourcePath()
        budir = os.path.join(os.path.dirname(sPath), 'dumps')
        if not os.path.isdir(budir):
            os.mkdir(budir)
        backup = Dump(self.main, budir)
        filepath = backup.filepath
        if not filepath: return

        guimessage = argSub(_("New backup file '%1' created, now read in the data"),
                (filepath,))
        guiReport(_("Create Backup File"), backup, guimessage)

        backup = None
        if not filepath: return

        try:
            guimessage = argSub(_("Updating database '%1' from %2"),
                    (self.dbname, sPath))
            mm = MakeMain(source, self.main)
            guiReport(_("Updating Main Database"), mm, guimessage)
            mm = None

        except:
            print_exc()
            message(_("Update failed, trying to restore from '%1'"),
                    (filepath,))

            restore = Restore(filepath)
            dbname = restore.getDbName()
            if not dbname:
                message(_("Couldn't open database file '%1'"), (filepath,))
                return

            # Delete all tables
            for t in self.main.getTables():
                self.main.send(u"DROP TABLE %s" % t)

            # Restore old state
            guimessage = argSub(_("Database '%1' cleared, now restore the data"),
                    (dbname,))
            restore.setMain(self.main)
            guiReport(_("Restore Database"), restore, guimessage)

        self.usersPrivileges(self.main)

        # adjust display, select new db
        self.initDBlist()

    def usersPrivileges(self, ndb):
        """Create new users if necessary (all the teachers)
        and grant the necessary privileges on the tables of this
        database. But if the database is finalized, revoke teachers'
        update privileges.
        Also remove users that are no longer active.
        """
        # Get database name from configuration data
        dbname = ndb.readValue(u"config", u"dbname")
        # Get list of users from the report table names
        ulist = ndb.getTeacherTables()

        # SELECT privileges for all on all
        for table in ("config", "data"):
            ndb.send(u"GRANT SELECT ON %s TO %s" % (table, USERROLE))

#        # Comments can also be inserted
#        ndb.send(u"GRANT SELECT, INSERT ON comments TO %s" % USERROLE)

        # Allow access to 'interface' table
        ndb.send(u"GRANT SELECT, UPDATE ON interface TO %s" % USERROLE)

        # Get a set of users before the change.
        set0 = self.activeUsers()

        fin = ndb.readValue(u"config", u"finalized")

        # Update the control database entry
        users = u""
        for u in ulist:
            users += u + u" "
        self.db.send(u"""UPDATE databases
                SET finalized= ?, users = ?
                WHERE name = ?""", (fin, users, dbname))

        # Get a set of users after the change.
        set1 = self.activeUsers()

        for u in (set0-set1):
            # Before removing a user, its privileges must be revoked
            try:
                ndb.send(u'REVOKE UPDATE ON %s FROM "%s"' % (u, u))
            except:
                pass
            self.removeUser(u)

        # new users
        newusers = set1-set0

        # If active:
        #    Grant UPDATE privileges on the report tables to the owning
        # teacher. Everyone else has SELECT only.
        # If finalized:
        #    Revoke update privileges
        for u in ulist:
            if (fin != u""):
                try:
                    ndb.send(u'REVOKE UPDATE ON %s FROM "%s"' % (u, u))
                except:
                    pass
            else:
                if u in newusers:   # Teacher not already in users list
                    self.addUser(u)
                ndb.send(u"GRANT SELECT ON %s TO %s" % (u, USERROLE))
                ndb.send(u'GRANT UPDATE ON %s TO "%s"' % (u, u))

    def activeUsers(self):
        """Return a set of active users, according to the teacher
        lists of non-finalized databases.
        """
        uset = set()
        # Union it with all user lists from non-finalized databases
        for ul in self.db.read(u"""SELECT users FROM databases
                WHERE finalized = ''"""):

            uset = uset.union(ul[0].split())

        return uset

    def slot_deletedb(self, arg):
        """This is a dangerous one! It will completely delete a database.
        """
        if not confirmationDialog(_("Delete Database?"),
                argSub(_("Do you really want to delete database '%1'?"),
                        (self.dbname,)), False):
            return
        if not self.main:
            return
        self.deletedb(self.dbname)

        # adjust display, select new db
        self.initDBlist()

    def deletedb(self, name):
        if self.main:
            self.main.close()
            self.main = None
        try:
            self.db.send(u"DROP DATABASE %s" % name)
        except:
            print_exc()
            message(_("Couldn't delete database '%1'.\n Try again ..."),
                    (name,))
            return

        # Get a set of users before the change.
        set0 = self.activeUsers()

        self.db.send(u"DELETE FROM databases WHERE name = ?", (name,))

        # Get a set of users after the change.
        set1 = self.activeUsers()

        for t in (set0-set1):
            self.removeUser(t)

    def slot_newdbIndex(self, index):
        """The current main database has changed. Disconnect from
        the old one and connect to the new one.
        """
        if (index < 0):
            self.gui.setUserList([])
            return
        self.dbname = self.dbList[index]

        if self.main:
            self.main.close()
        self.main = self.connect(self.dbname)

        # Set 'finalized' state
        fin = self.main.readValue(u"config", u"finalized").strip()
        self.showFinalized(fin != u"")

        # Set 'self.users' to an ordered list of teacher (tag, name)
        # pairs and set the teacher comboBox
        teachers = [path.split(u"/")[1]
                for path in self.main.listIds(u"data")
                if path.startswith(u"teachers/")]
        teachers.sort()

        usrstrings = []
        self.users = []
        for t in teachers:
            n = sini2dict(self.main.getFile(u"teachers/" + t))[u"Name"]
            self.users.append((t, n))
            usrstrings.append(u"%s (%s)" % (t, n))
        self.gui.setUserList(usrstrings)

        self.slot_selectTeachers(None)

    def slot_pwReset(self, arg):
        """Reset all selected users' passwords to their initial state.
        """
        if self.finalized:
            message(_("Invalid operation on finalized database."))
            return
        users = u""
        for u in self.gui.getSelectedUsers(self.getUsers()):
            self.db.setPassword(u)
            users += u + u" "
        message(_("Passwords reset to '%1' for users:\n  %2"),
                (DEFAULTPASSWORD, users))

    def slot_selectTeachers(self, arg):
        """Check all teachers in the comboBox.
        """
        if self.main:
            for i in range(len(self.users)):
                self.gui.userListSetChecked(i, True)

    def slot_dump(self, arg):
        """Generate a backup file (sqlite database).
        """
        # Get destination directory:
        dir0 = self.settings.getSetting("destDir")
        dbpath = getDirectory(_("Destination Folder"), dir0)
        if not dbpath: return
        self.settings.setSetting("destDir", dbpath)

        # Do the dump
        backup = Dump(self.main, dbpath)
        if not backup.filepath: return

        guimessage = argSub(_("New backup file '%1' opened, now write in the data"),
                (backup.filepath,))
        guiReport(_("Create Backup File"), backup, guimessage)

    def getUsers(self):
        """Return a list of users (just the login names).
        """
        return [u[0] for u in self.users]

    def getDbDir(self, settingskey):
        """Get the directory for storing user database files.
        Return None if cancelled.
        """
        dir0 = self.settings.getSetting(settingskey)
        dbpath = getDirectory(_("Database Folder"), dir0)
        if not dbpath: return None
        self.settings.setSetting(settingskey, dbpath)
        return dbpath

    def getBDbPath(self):
        """Select a database backup file.
        Return None if cancelled.
        """
        dir0 = self.settings.getSetting("destDir")
        dbpath = getFile(_("Source File"), dir0,
                filter=(_("Backup Files"), (u"*.zgb",)))
        if dbpath:
            self.settings.setSetting("destDir", os.path.dirname(dbpath))
        return dbpath

    def dump(self, dbpath, user, isList=False):
        if isList and user:
            backup = DumpUsers(user, self.main, dbpath)
            guimessage = _("Creating multiple user database files ...\n")
        else:
            backup = Dump(self.main, dbpath, user)
            if not backup.filepath: return None
            guimessage = argSub(_("Database file '%1' created, now"
                    " read in the data"), (backup.filepath,))
        if user:
            title = _("Create User Database File")
        else:
            title = _("Create Full Database Dump File")
        guiReport(title, backup, guimessage)
        return backup.filepath

    def slot_genTeacherDb(self, arg):
        """Generate a teacher's database file for all selected teachers.
        """
        # Get list of users for whom a database file is to be generated
        users = self.gui.getSelectedUsers(self.getUsers())
        if not users: return

        # Get destination directory:
        dbpath = self.getDbDir("teacherDbDir")
        if not dbpath: return

        # Dump the database files
        self.dump(dbpath, users, True)

    def slot_restore(self, arg):
        """Restore a dumped database.
        It can be either an existing one, or one which has been deleted.
        """
        # Get source file:
        dbpath = self.getBDbPath()
        if not dbpath: return None

        restore = Restore(dbpath)
        dbname = restore.getDbName()
        if not dbname:
            message(_("Couldn't open database file '%1'"), (dbpath,))
            return

        state = 0
        try:

            if dbname in self.dbList:
                if not confirmationDialog(_("Replace Database?"),
                        argSub(_("Are you sure you want to replace database '%1'?"),
                        (dbname,)), False):
                    restore.close()
                    return
                self.deletedb(dbname)

            self.db.send(u"""CREATE DATABASE %s
                    OWNER %s ENCODING 'UTF8'""" % (dbname, ADMIN))
            state = 1
            # Add to 'databases' table
            self.db.send(u"INSERT INTO databases VALUES (?, ?, ?, ?)",
                    (self.db.getTime(), dbname, u'', u''))
            state = 2

            newmain = self.connect(dbname)
            state = 3

            guimessage = argSub(_("New database '%1' created, now read in the data"),
                    (dbname,))
            restore.setMain(newmain)
            guiReport(_("Restore Database"), restore, guimessage)
            #message(_("New database now set up"))

            self.usersPrivileges(newmain)

            # Ensure connection is closed
            restore = None
            newmain.close()
            newmain = None

        except:
            print_exc()

            message(_("Couldn't create new database (%1)"), (dbname,))
            if (state >= 3):
                newmain.close()
            if (state >= 2):
                self.db.send(u"DELETE FROM databases WHERE name = ?",
                        (dbname,))
            if (state >= 1):
                self.db.send(u"DROP DATABASE %s" % dbname)

        # adjust display, select new db
        self.initDBlist()

    def slot_finalize(self, on):
        """'Finalize' the database.
        Set the 'finalized' item in the 'config' table and revoke
        update privelege from teachers.
        """
        if (not self.main) or (on == self.finalized):
            return

        if on:
            if not confirmationDialog(_("Finalize Database?"),
                argSub(_("Finalizing stops teachers' access to the database.\n"
                        "It may also clear their passwords.\n  Continue?"),
                        (self.dbname,)), False):
                return
            val = u"1"
        else:
            val = u""
        self.main.send(u"""UPDATE config SET value= ?
                WHERE id = 'finalized'""", (val,))
        self.showFinalized(on)
        self.usersPrivileges(self.main)

    def showFinalized(self, fin):
        self.finalized = fin
        self.gui.setFinalized(self.finalized)

    def slot_print(self, arg):
        """Pass a database dump file (*.zgb) to the print applicataion.
        """
        dir0 = self.settings.getSetting("destDir")
        filepath = None
        if dir0:
            # See if there is already an adequately new dump file
            rex = re.compile(r"%s_(\d{8}_\d{6}).zgb$" % self.main.getName())
            dumpfiles = [f for f in os.listdir(dir0) if rex.match(f)]
            if dumpfiles:
                dumpfiles.sort()
                latest = dumpfiles[-1]
                dumptime = rex.match(latest).group(1)

                udt = self.main.readValue(u"config", u"updatetime")
                lst = self.main.readValue(u"interface", u"lastsynctime")

                if (dumptime > udt) and (dumptime > lst):
                    filepath = os.path.join(dir0, latest)

        if not filepath:
            dbpath = self.getDbDir("destDir")
            if not dbpath: return

            # Dump a full database
            filepath = self.dump(dbpath, u"")
            if not filepath:
                return

        # Start the printer dialog with this file.
        if self.printHandler:
            self.printHandler.init(filepath)
        else:
            self.printHandler = GuiPrint("print", filepath)
        self.printHandler.run()

    def slot_sync(self, arg):
        """Perform a synchronization with a selected database file
        but as adminstrative user.
        This allows even a finalized database to be updated.
        """
        sfile = self.settings.getSetting("syncFile")
        if sfile:
            sdir = os.path.dirname(sfile)
            sfile = os.path.basename(sfile)
        else:
            sdir = None

        syncfile = getFile(_("User database file"),
                startDir=sdir, startFile=sfile,
                defaultSuffix=".zga",
                filter=(_("Report Files"), (u"*.zga",)))
        if not syncfile:
            return
        self.settings.setSetting("syncFile", syncfile)

        dbs = DBs(syncfile)
        if not dbs.isOpen():
            return

        sdbname = dbs.getConfig(u"dbname")
        dbs.close()

        if (self.dbname != sdbname):
            warning(_("%s: Database name does not match current main name") %
                    syncfile)
            return

        self.dlg = Output()
        synchronize(self.main, syncfile, self.dlg)
        self.dlg.done()

    def removeUser(self, user):
        """Remove a user. Return True if succeeded.
        """
        try:
            self.db.dropRole(user)
        except:
            message(_("Couldn't remove user '%1'"), (user,))
            return False
        return True

    def slot_restoreConfigFile(self, arg):
        if self.main:
            self.restoreConfigFile(self.main)

    def restoreConfigFile(self, db):
        """Get a parent directory for the creation of a data file.
        The file to be created may not exist already.
        Returns the file-name if successful, otherwise 'None'.
        """
        # put up directory dialog, starting one up from dir0
        dir = getDirectory(_("Parent Folder"))
        if not dir: return None
        datapath = os.path.join(dir, self.dbname + '.zip')
        if os.path.exists(datapath):
            message(_("'%1' already exists"), (datapath,))
            return None
        dest = CfgZip(datapath, True)   # open for writing
        if not dest.isOpen():
            message(_("Couldn't open '%s' for writing") % datapath)
            return None

        for path, data in db.getAllData():
            dest.addFile(path, data)
        dest.close()
        message(_("Configuration saved to '%s'") % datapath)
        return datapath

class DumpUsers:
    def __init__(self, userlist, main, dbpath):
        self.userlist = userlist
        self.main = main
        self.dbpath = dbpath
        self.filepath = None    # Needed on return, but unused

    def run(self, gui):
        failList = []
        for user in self.userlist:
            gui.report(u"::: " + user)
            backup = Dump(self.main, self.dbpath, user)
            if not backup.filepath:
                failList.append(user)
                continue
            backup.run(gui)
            if not backup.filepath:
                failList.append(user)
        if failList:
            gui.report(_("***************\n"
                    "Database files could not be created for:\n  %s")
                    % repr(failList))

