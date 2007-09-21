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
"""The high-level interface to the database.
It in turn uses the module 'dbWrap' to hide the lower level,
implementation and engine specific details.
"""

# Database structure version. The database files must match this.
DBVERSION = u"2"

FixedSpace = u"\u00b7"      # The centre-dot character.

IndentStep = 2.0    # mm

#NOTE: It is assumed that the column width (width of text area)
#     is constant throughout the report.


import os.path
import time
import re

from dbWrap import DB as DBs
from guiDialogs import getFile
from guiBase import Font


class DB(DBs):
    """An object representing a report database.
    It inherits from the simple database wrapper, so that that object's
    methods are also available here.
    """
    def __init__(self, path):
        # path is the full path to the sqlite database.
        DBs.__init__(self, path)
        if not self.db: return
        try:
            if (self.readValue(u"config", u"dbversion") == DBVERSION):

                # Parse 'base' data
                self.baseDict = self.getData(u"base")
                return

        except:
            pass
        self.db = None
        warning(_("File '%1' is not a 'Zeugs' database, version '%2'"),
                (path, DBVERSION))

    def init(self):
        """Further initializations for those applications which
        need more detailed access.
        """
        self.owner = self.getConfig(u"me")
        # The time of creation of this database is needed to ensure
        # that changes get a later timestamp
        try:
            self.createtime = self.getConfig(u"createtime")
        except:
            # '*.zgb' files don't have this field, read the backup time
            self.createtime = self.getConfig(u"backuptime")

        # Get a list of configuration data 'files'
        self.dataFiles = self.listIds(u"data")

        # Set up self.classes to be an ordered list of Class objects
        # and self.classDict to be a dictionary of Class objects with
        # the class tag as key.
        classes = self.dataFilter(u"^classes/[^/]+/info$")
        classes.sort()
        self.classes = []
        self.classDict = {}
        for ipath in classes:
            ctag = ipath.split(u"/")[1]
            c = Class(ctag, self.getData(ipath))
            self.classes.append(c)
            self.classDict[ctag] = c

        # Dictionary of Layout object, key is layout name
        self.layoutDict = {}    # initially empty

        # Read in the teacher information
        self.teachers = {}
        for tfile in self.dataFilter(u"^teachers/[^/]+$"):
            self.teachers[tfile.split(u"/")[1]] = self.getData(tfile)

        # The database object has a 'current' class, which is
        # initially unset.
        self.classObject = None

    def getData(self, path):
        """Return a dictionary containing the parsed data (value-field)
        from the given path (id-field) in the 'data' table.
        """
        return sini2dict(self.getFile(path))

    def listAllFiles(self, path):
        """Return a list of all 'data' files (including those in sub-folders)
        whose path starts with path, but not including path itself.
        The entries are full (data) paths, including the path-prefix.
        """
        return [f for f in self.listIds(u"data") if f.startswith(path)
                and (f != path)]

    def dataFilter(self, pattern):
        """Return the entries in self.dataFiles which match the pattern.
        """
        rp = re.compile(pattern)
        return [p for p in self.dataFiles if rp.search(p)]

    def getReportData(self):
        """Get lists of pupils for each of the subjects for each of
        the classes - a nested dictionary structure.
        """
        cdict = {}
        # This information can be got from the id-field of the reports.
        for rep in self.listIds(u"reports"):
            cls, pup, subj = cpsUnkey(rep)
            sdict = cdict.get(cls)
            if not sdict:
                sdict = {}
                cdict[cls] = sdict
            plist = sdict.get(subj)
            if not plist:
                plist = []
                sdict[subj] = plist
            plist.append(pup)
        return cdict

    def setClass(self, classObject, complete=False):
        """Set the current class.
        If the 'Class' object hasn't been fully initialized, this
        must be done. Once loaded, the layout and pupil information
        is remembered across class changes.
        'complete' determines whether also the 'subjects'
        information for the class should be parsed (needed by the
        printer to determine the teacher for a report).
        """
        if not classObject.layoutInfo:
            # No existing Layout object found.
            layout = classObject.layout
            # See if it has already been parsed
            l = self.layoutDict.get(layout)
            if not l:
                # Get it from the database.
                # Get a list of 'file'-paths for the layout
#NOTE:
# The editor only needs 'document', 'fonts', 'frames', 'subject_frames',
# so it would be possible to restrict ourselves to these in that case.
# The printer needs all files.
                layoutDict = {}

                for ld in self.dataFilter(u"layouts/%s/" % layout):
                    readData(layoutDict, self.getData(ld),
                            ld.split(u"/", 2)[2])

                l = LayoutInfo(layoutDict)
                # This information is cached, so that it doesn't need to be
                # parsed again when this layout is reselected.
                self.layoutDict[layout] = l

            classObject.layoutInfo = l

            # The pupil information for this class must also be fetched.
            pupils = {}
            for pfile in self.dataFilter(u"^classes/%s/pupils/[^/]+$" %
                    classObject.classTag):
                pupils[pfile.rsplit(u"/", 1)[1]] = self.getData(pfile)
            classObject.setPupils(pupils)

            if complete:
                # The subject information for this class must also be fetched.
                subjects = {}
                for sfile in self.dataFilter(u"^classes/%s/subjects/[^/]+$" %
                        classObject.classTag):
                    subjects[sfile.rsplit(u"/", 1)[1]] = self.getData(sfile)
                classObject.setSubjects(subjects)

        self.classObject = classObject
        self.layoutInfo = classObject.layoutInfo

    def getSubjectName(self, subjectTag):
        """Get the name from the given subject tag using the current
        class's layout.
        """
        sfdict = self.layoutInfo.layoutDict[u"subject_frames"]
        return sfdict.get(subjectTag)[u"display-name"]

    def getFrames(self, subjectTag):
        """Return a list of frame names for the given subject. Uses
        the currently set class!
        """
        sfdict = self.layoutInfo.layoutDict[u"subject_frames"]
        return sfdict.get(subjectTag)[u"frames"].split()

    def getTeacherName(self, tag):
        return self.teachers[tag][u"Name"]

    def getReport(self, pupilId, subject):
        """Get the report for the given pupil and subject.
        If the pupil didn't take the subject return 'None'.
        """
        id = self.psKey(pupilId, subject)
        try:
            return self.readValue(u"reports", id)
        except:
            return None

    def psKey(self, pupilId, subject):
        return cpsKey(self.classObject.classTag, pupilId, subject)

    def getReportTeacher(self, pupilId, subject):
        """Used by the printer app to determine the teacher for a
        particular report.
        Return the teacher's tag.
        """
        return self.classObject.subjectsDict[subject][u"Teacher"]

    def saveReport(self, pupilId, subject, reportText, version):
        """Save a report to the database.
        Return the value of the new report.
        """
        report = makeReportValue(reportText, version)
        id = self.psKey(pupilId, subject)
        self.send(u"UPDATE reports SET value = ? WHERE id = ?",
                (report, id))
        return report

    def getConfig(self, item):
        return self.readValue(u"config", item)

    def setConfig(self, item, value):
        self.send(u"""UPDATE config SET value = ?
                WHERE id = ?""", (value, item))

    def getTime(self):
        """Get the current date and time, formatted as a string:
          yyyymmdd_hhmmss.
        The result is constrained to be later than the time of
        creation of this database
        """
        t = u"%4d%02d%02d_%2d%2d%2d" % time.localtime()[:6]
                # (year, month, day, hours, mins, secs, ...)
        if (t <= self.createtime):
            t = self.createtime + u"1"
        return t

    def getPupilName(self, id):
        """Given the pupil id, return the name. Uses the currently set
        class!
        """
        return self.classObject.pupilinfo[id][u"Name"]


class Class:
    """Encapsulates information about a class. Initially this class is
    only partially initialized, to get the class name and the report
    layout name. When a class is actually accessed, the information for
    that class will be loaded.
    """
    def __init__(self, classTag, classInfo):
        self.className = classInfo[u"Name"]
        self.classTag = classTag
        self.layout = classInfo[u"Layout"]
        # layout information cache, initially empty
        self.layoutInfo = None
        # dictionary of pupil info for the class, key=id, initially undefined
        self.pupilinfo = None
        # list of (name, id) pairs for the pupils of this class,
        # ordered by name, initially undefined
        self.orderedPupilList = None

    def setPupils(self, pupilsDict):
        """Set up pupil info for this class.
        'pupilsDict' is the parsed contents of the class's 'pupils' file.
        """
        # Build a list of tuples for sorting the data
        opl = []
        for id, pdict in pupilsDict.items():
            fn = pdict[u"FirstNames"]
            ln = pdict[u"LastName"]
            # Add a 'Name' entry
            n = (u"%s %s" % (fn, ln)).strip()
            pdict[u"Name"] = n
            opl.append((ln, fn, n, id))

        self.pupilinfo = pupilsDict
        opl.sort()
        self.orderedPupilList = [(p[2], p[3]) for p in opl]

    def setSubjects(self, subjectsDict):
        self.subjectsDict = subjectsDict


class LayoutInfo:
    """Encapsulates the information from a layout description.
    """
    def __init__(self, layoutDict):
        """The formatting information is passed in in dictionary form.

        Save the dictionary as self.layoutDict, and extract
        some of the most important data so it is available as
        attributes.
        """
        self.layoutDict = layoutDict

        document = self.layoutDict[u"document"]
        # Width of writeable area
        self.mainWidth = float(document[u"textAreaWidth"])


        # Paragraph body indentation
        self.indent0 = float(document[u"xText0"])
        # Width of (normal) report text line
        self.lineWidth = self.mainWidth - 2*self.indent0
        # Extra indentation of first line of paragraph
        self.indent1 = float(document[u"xPara1"])
        # Default special text indentation
        self.indent2 = float(document[u"xSpecialDefault"])
        # Whether to disable block justification
        self.nojustify = not getBoolean(document, u"justify")

        # Fonts
        self.normalFont = self.getFont(document[u"normalFont"])
        self.specialFont = self.getFont(document[u"specialFont"])
        self.titleFont = self.getFont(document[u"titleFont"])
        self.signatureFont = self.getFont(document[u"signatureFont"])

        # This frame has an essentially unlimited height and is only
        # used to show the overflowing text in the editor - it will
        # not be printed.
        self.layoutDict[u"frames"][u"overflowFrame"] = {
                u"topMargin" : u"0",
                u"bottomMargin" : u"0",
                u"firstLineIndent" : u"0",
                u"firstLineRelative": u"0",
                u"title" : u"",
                u"titleRight" : u"0",
                u"titleOnEmpty" : u"0",
                u"titlex" : u"0",
                u"titley" : u"0",
                u"signatureHeight" : u"0",
                u"signatureLeft" : u"0",
                u"signaturex" : u"0",
                u"signaturey" : u"0",
                u"teacher" : u"",
                u"teacherLeft" : u"0",
                u"teacherBottom" : u"0",
                u"teacherOnSignature" : u"0",
                u"teacherAllFrames" : u"0",
                u"teacherx" : u"0",
                u"teachery" : u"0",
                u"height" : u"100",
                u"minHeight" : u"0",
                u"strikeOut" : u"0"
            }

    def getFont(self, fontName):
        """Get the font information for the given style and generate a Font
        instance for it, if necessary. Once one has been generated it
        is saved for future use.
        """
        fdict = self.layoutDict[u"fonts"].get(fontName)
        f = fdict.get(u"fontObject")
        if not f:
            f = Font(fdict)
            fdict[u"fontObject"] = f
        return f

def selectDBFile(settings=None, force=True, dbSuffix=u"zga"):
    """Open a db file. Also do extended initialization (call self.init).
    force=True => always put up a selection dialog, else try
    getting the file from the 'settings' facility first.
    If it puts up a dialog the start directory will be that of
    the remembered file, or - if that doesn't exist - the user's
    home directory.
     -> DB object, or 'None' if 'cancel' selected
    """
    dbDir = None
    if settings:
        dbFile = settings.getSetting("dbFile")
    else:
        dbFile = None
    while True:
        if force:
            if dbFile:
                dbd = os.path.dirname(dbFile)
                if os.path.isdir(dbd):
                    dbDir = dbd

            dbFile = getFile(_("Select database file"),
                    startDir=dbDir,
                    defaultSuffix=dbSuffix,
                    filter=(_("Database Files"), (u"*.%s" % dbSuffix,)))

            if not dbFile:
                return None
            if settings:
                settings.setSetting("dbFile", dbFile)

        db = DB(dbFile)
        if db.isOpen():
            db.init()
            return db
        force = True

def makeReportsDict(dataSource):
    """Parse all class configuration data, to determine ownership
    of reports.
    Create a dictionary containing entries for all reports
    (in the updated configuration).
    The keys have the form 'classTag-pupilId_subject', the value
    is the teacher.
    It also checks that there are no duplications of pupil/subject
    pairs.
    """
    classesDict = {}
    for d in dataSource.listAllFiles("classes/"):
        readData(classesDict, sini2dict(dataSource.getFile(d)), d[8:])

    reports = {}
    for c, cdic in classesDict.items():
        # c is a class tag, cdic its dictionary
        for p, pdic in cdic[u"pupils"].items():
            # p is a pupil tag, pdic its dictionary
            # The whole-class group ('0') is only implicit (for every
            # pupil) in the pupils data, so add it here.
            groups = pdic[u"Groups"].split() + ["0"]
            # add the class part to the pupil tag
            for s, sdic in cdic[u"subjects"].items():
                # s is a subject tag, sdic its dictionary
                if (sdic[u"CGroup"] in groups):
                    key = cpsKey(c, p, s)
                    if reports.has_key(key):
                        error(_("Pupil '%1' has more than one entry for subject '%2'"),
                                (u"p%s-%s" % (c, p), s))
                    reports[key] = sdic[u"Teacher"]
    return reports

def cpsKey(c, p, s):
    """Make a report-table key from class, pupil and subject tags.
    """
    return u"%s$%s#%s" % (c, p, s)

def cpsUnkey(key):
    """Get class, pupil and subject tags from a key to the reports
    dictionary (inverse of 'cpsKey').
    """
    cp, s = key.split(u"#")
    return cp.split(u"$") + [s,]


def getReportText(data):
    """Returns the text part of a report's 'value'.
    """
    return data.split(u"\n", 1)[1]

def getReportVersion(data):
    """Returns the text part of a report's 'value'.
    """
    return data.split(u"\n", 1)[0]

def makeReportValue(text, version):
    """Returns the 'value' for a report built from its text and version.
    """
    return version + u"\n" + text


def readData(dic, dataDict, path):
    """Given the root dictionary, 'dic', enter the given data
    dictionary, 'dataDict' to the given path, 'path'. Missing levels
    within the path will be created.
    """
    lpath = path.split("/")
    for f in lpath[:-1]:
        if not f in dic:
            dic[f] = {}
        dic = dic[f]
    dic[lpath[-1]] = dataDict


# Regular expressions
rx1 = re.compile(ur'([^ =]+) *= *(.*)$') # field definition line
rx2 = re.compile(ur'"(.*)"$')            # Quote-mark stripping

def sini2dict(utext, withComments=False):
    """Create a dictionary from the unicoded contents of a 'sini'
    file, assuming it is structurally valid (which should have
    been checked before entering it into the system).
    Return a field dictionary.
    """
    d = {}          # to contain data
    comment = u""   # to collect the comments

    ln = 0          # line counter
    if isinstance(utext, str):
        utext = utext.decode('utf8')
    for line in utext.splitlines():
        ln += 1
        line = line.strip()
        if (not line):
            continue
        if (line[0] == u'#'):
            if (comment != None):
                comment += line[1:] + u"\n"
            continue

        if withComments:
            d[u"comment"] = comment
        comment = None

        # A field definition (item = value)
        r = rx1.match(line)
        if not r:
            continue
        item, value = r.groups()
        # Remove quotes
        r = rx2.match(value)
        if r:
            value = r.group(1)

        d[item] = value

    return d

def getBoolean(dict, key):
    """"For reading boolean values from a configuration/layout
    description. It accepts key not defined, '' and '0' as false,
    anything else is true.
    """
    val = dict.get(key)
    if (not val) or (val == u"0"): return False
    return True
