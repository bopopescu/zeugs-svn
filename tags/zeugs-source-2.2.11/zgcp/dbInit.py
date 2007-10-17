# -*- coding: utf-8 -*-

#2007-09-01
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

from traceback import print_exc, format_exc
from dbWrapMaster import DB, ADMIN, USERROLE
from getConnectInfo import getConnectInfo
from gui0 import Application
from newPassword import getPassword
from guiDialogs import confirmationDialog
from guiDbInit import GuiDbInit


intro = _("Welcome to the Zeugs initialization utility.\n"
"This will set up a control database on your PostgreSQL server."
"You should only need to run this once to prepare the database"
" server for use with Zeugs.")

def setup():
    # Initialize graphical interface, note that the same settings
    # group as the control panel is used.
    global app, gui
    app = Application("cp")

    gui = GuiDbInit(intro, go)
    app.run()

def go():
    gui.report("  ------------------------------------\n")
    # Connect to control database
    connectData = getConnectInfo(app.settings, "postgres")
    if not connectData:
        return False

    gui.report(_("Connecting to postgres@%s") % connectData[u"host"])

    dbzc = connectData[u"db"]
    connectData[u"db"] = u"postgres"
    dbp = DB(connectData)
    if not dbp.isOpen():
        error(_("Couldn't open 'postgres' database"))
        return False

    gui.report(_("Checking existing databases"))

    if dbp.read1(u"SELECT datname FROM pg_database WHERE datname = ?",
            (dbzc,)):
        if not confirmationDialog(_("Remove Control Database?"),
                _("The control database (%s) already exists."
                  " Should it be removed, with everything it contains?")
                        % dbzc, False):
            dbp.close()
            return False

        connectData[u"db"] = dbzc
        userset = set()
        try:
            # Remove all databases and users
            db = DB(connectData)
            try:
                info = db.read(u"SELECT * FROM databases")
            except:
                info = None
            db.close()
            if info:
                for id, name, finalized, users in info:
                    gui.report(_("Removing database '%s'") % name)
                    dbp.send(u"DROP DATABASE IF EXISTS %s" % name)
                    userset |= set(users.split())

            gui.report(_("Removing database '%s'") % dbzc)
            dbp.send(u"DROP DATABASE %s" % dbzc)

        except:
            #print_exc()

            error(_("Couldn't remove old data -"
                    " summon a PostgreSQL expert:\n%s") % format_exc())

        gui.report(_("Trying to remove users ..."))
        try:
            dbp.send(u"DROP ROLE IF EXISTS %s" % USERROLE)
        except:
            gui.report(_("  ... couldn't remove user '%s'") % USERROLE)
        try:
            dbp.send(u"DROP ROLE IF EXISTS %s" % ADMIN)
        except:
            gui.report(_("  ... couldn't remove user '%s'") % ADMIN)
        for u in userset:
            try:
                dbp.send(u"DROP ROLE IF EXISTS %s" % u)
            except:
                gui.report(_("  ... couldn't remove user '%s'") % u)

    gui.report(_("\nCreating control database"))
    dbp.send(u"CREATE DATABASE %s ENCODING 'UTF8'" % dbzc)
    dbp.close()
    dbp = None

    connectData[u"db"] = dbzc
    db = DB(connectData)
    if not db.isOpen():
        error(_("Couldn't open control database"))
        return False

    try:
        setupCDB(db)
    except:
        db.close()
        error(_("Couldn't set up the '%s' database."
                " Please try again:\n%s") % (dbzc, format_exc()))
        return False
    gui.report(_("\nSuccess! The control database is ready."))
    gui.report(_("  Now use the control panel (zgcp) to set up"
            " report databases."))

    db.close()
    return True

def setupCDB(db):
    """Initialization of the database tables for the control panel.
    This need only be run once.
    """
    # Create the main administrator account (owner of the Zeugs
    # databases)
    message(_("The administrative user '%s' will now be created."
              " Please enter a difficult-to-guess password") % ADMIN)
    pw = getPassword()
    if not pw: raise NameError
    db.createMainAdmin(pw)

    # Create the table of databases
    t = u"databases"
    db.send(u"DROP TABLE IF EXISTS %s" % t)
    assert db.createTable(t, (u"id", u"name", u"finalized", u"users"))
    # Grant privileges
    db.send(u"""GRANT ALL PRIVILEGES ON TABLE %s
            TO %s WITH GRANT OPTION""" % (t, ADMIN))

    # Create 'role model' for normal users
    db.createGroupRole(USERROLE)

# To get user names
#    SELECT rolname FROM pg_roles;
