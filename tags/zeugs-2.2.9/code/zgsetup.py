#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Set up the Zeugs control database.

Once the master database server (I assume PostgreSQL) has been
installed and set up, a control database for the Zeugs system must
be created by a superuser. This database is called 'zeugscontrol'.
SQL:
   CREATE DATABASE zeugscontrol ENCODING 'UTF8';

Then this script must be run to initialize this control database.

Remember that the postgres configuration file pg_hba.conf must also
be set up (and postgres restarted), to get the desired authentication.
Change 'trust' to 'md5', and if network access is desired, add this.
"""

# Add module directories to search path
import sys, os.path
thisDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(thisDir, "zgcommon"))
sys.path.append(os.path.join(thisDir, "zgcp"))
sys.path.append(os.path.join(thisDir, "gui"))

import gettext
gettext.install('zeugs', 'i18n', unicode=1)

import framework
from dbInit import setup


if __name__ == "__main__":
    setup()
