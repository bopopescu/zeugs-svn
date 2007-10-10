#!/usr/bin/env python
# -*- coding: utf-8 -*-

#2007-09-16
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
import traceback
"""
The various types of node are:
1) Directory containing named or unspecified-named files and/or directories
2) =-file ('sini' format configuration data)
3) i-file, (image)
"""

import os

from verify import Validate
from guiDialogs import getFile, confirmationDialog, getFileName, \
        messageDialog, getDirectory
from dataDefinition import dataDefinition, getSpec
from guiCsvConfig import getCsvConfig
from csv2sini import Csv2Sini, CsvData
from guiReport import guiReport
from fileHandler import dirList, CfgZip, getsini

FDEFAULT = '001'    # 'default' file name (if a file must be created)

def joinPath(a, b):
    """Join two path components.
    """
    if a:
        return "%s/%s" % (a, b)
    else:
        return b

class ConfigEd:
    def __init__(self, settings):
        self.settings = settings
        slot("ced_open", self.slot_openConfig)
        slot("ced_edit", self.slot_valueChange)
        slot("ced_newItem", self.slot_switchNode)
        slot("ced_clone", self.slot_clone)
        slot("ced_delete", self.slot_delete)
        slot("ced_comment", self.slot_commentChanged)
        slot("ced_pupils", self.slot_getPupils)
        slot("ced_pix", self.slot_replacePix)
        slot("ced_tempsave", self.slot_tempsave)

    def init(self, gui):
        self.sourcePath = None  # For the control panel only
        self.gui = gui
        self.baseFolder = None  # For the folder containing the active file
        self.validationObject = Validate()
        if not self.slot_openConfig(False):
            self.gui.close()

    def slot_openConfig(self, force):
        """
        """
        zpath = self.settings.getSetting("configFile")
        if force or (not os.path.isfile(zpath)):
            dir = os.path.dirname(str(zpath))
            if not os.path.isdir(dir):
                dir = None
            zpath = getFile(_("Choose Configuration File"),
                    startDir=dir, defaultSuffix="zip",
                    filter=(_("zip Files"), ("*.zip",)),
                    create=True)
            if not zpath:
                return False
        if isinstance(zpath, unicode):
            zpath = zpath.encode('utf8')

        self.save()     # If a folder is open, save it and close it

        self.source = CfgZip(zpath)
        if not self.source.isOpen():
            warning(_("The supplied configuration file (%s) could"
                    " not be opened. A completely empty configuration"
                    " will be created.") % zpath)

        self.baseFolder = os.path.dirname(zpath)

        self.gui.setTitle(_("Config Editor: %s") % zpath)
        self.gui.setLabel(_("For database: %s") % self.source.cfgName)

        self.settings.setSetting("configFile", zpath)
        self.buildTree()
        return True

    def buildTree(self):
        self.currentSpec = None
        self.fileDict = {}
        self.nodeDict = {}
        self.validationObject.init(self.fileDict)
        self.gui.clearTable()
        self.gui.clearTree()
        self.readLevel(dataDefinition(), "")
        self.checkAll()

    def pathExists(self, path):
        return (self.fileDict.get(path) != None)

    def checkAll(self):
        errorTags = self.validationObject.validateAll()
        self.gui.setTreeNodeColours(errorTags)

    def readLevel(self, itemlist, path):
        for item in itemlist:
            iname = item[0]
            itype = item[1]
            # If it's a directory, make directory sub-nodes
            if (itype == "/"):
                if iname:
                    self.addDir(iname, item, path)
                else:
                    # If the name is empty, all existing directories count
                    dirs = self.source.listDirs(path)
                    if not dirs:
                        # Create a 'default' directory ...
                        self.addDir("default", item, path)

                    else:
                        dirs.sort()
                        for iname in dirs:
                            self.addDir(iname, item, path)
            # Files
            elif (itype == "i"):
                # Image files - just make nodes for them.
                # Only 'empty' file-names (in the spec) are covered
                # at present!
                files = self.source.listFiles(path)
                files.sort()
                for f in files:
                    self.addnode(f, joinPath(path, f), item)

            elif not iname:
                # The file-name can be 'empty', in which case all
                # existing files count, except any starting with '_'
                files = [f for f in self.source.listFiles(path)
                        if not f.startswith('_')]

                if not files:
                    # Create a 'default' file ...
                    self.addFile(path, FDEFAULT, item)

                else:
                    files.sort()
                    for f in files:
                        self.addFile(path, f, item)
                    continue

            else:
                self.addFile(path, iname, item)

    def addDir(self, iname, item, path):
        """Add a directory node to the tree structure.
        """
        newpath = joinPath(path, iname)
        self.addnode(iname, newpath + '/', item)
        self.readLevel(item[3:], newpath)

    def addFile(self, path, iname, item, text=None):
        """Add a file to the tree structure.
        If no text is supplied, get it from the file.
        """
        newpath = joinPath(path.rstrip('/'), iname)
        if (text == None):
            text = self.source.getFile(newpath)

        dic = getsini(text)
        sec = self.buildSection(item[3:], dic)
        comment = dic["comment"]
        self.addnode(iname, newpath, list(item[:3]) + [comment, sec])

    def addnode(self, iname, path, ispec):
        """Add a node to the 'directory' tree.
        """
        # There is the specification record for that path
        self.fileDict[path] = ispec

        # And there is the graphical node, which just records the path.
        # Get the parent (gui) node
        ps = path.rstrip('/').rsplit('/', 1)
        if (len(ps) == 1):
            parent = None
        else:
            parent = self.nodeDict[ps[0] + '/']
        node = self.gui.addnode(parent, iname, path, ispec[1], ispec[2])
        self.nodeDict[path] = node

    def buildSection(self, spec, vdict):
        """Build a list representing a section containing field
        definitions. It will take on the values from the given
        dictionary, leaving out those not in the specification list
        and adding default values for those not in the dictionary.
        """
        slist = []
        for field, ftype, tip in spec:
            ft = ftype.split("|")
            val = vdict.get(field)
            if (val == None):
                # Get the default value
                if (len(ft) > 1):
                    val = ft[1]
                else:
                    val = ""
            if (ft[0]== "bool"):
                if (val == ""):
                    val = "0"
                elif (val != "0"):
                    val = "1"
            slist.append([field, val, ft, tip])
        return slist

    def writeSection(self, path, flist, comment):
        """Build a sini-file from the given data.
        Return the text of the file.
        """
        text = ''
        clines = comment.splitlines()
        if clines:
            for cl in clines:
                text += '#%s\n' % cl
        for fspec in flist:
            text += '%s = %s\n' % (fspec[0], fspec[1])
        return text

    def saveData(self, filePath, imageX=None):
        """Save all the data to a zip file.
        If imageX is a directory path, get the images from there
        instead of from the source file
        """
        dest = CfgZip(filePath, write=True)
        for f, spec in self.fileDict.items():
            if f.endswith('/'):
                continue
            if (spec[1] == 'i'):
                if not imageX:
                    # Image file, copy it from the source
                    dest.addFile(f, self.source.getFile(f))
            else:
                # Information file, write it in 'sini'-format
                dest.addFile(f, self.writeSection(f, spec[4], spec[3]))

        if imageX:
            # Copy in all files ending .svg and .jpg from the given folder
            try:
                tlist = ["teachers/" + i
                        for i in os.listdir(imageX + "/teachers")]
            except:
                tlist = []
            try:
                ilist = os.listdir(imageX)
            except:
                ilist = []
            imlist = ilist + tlist
            for i in imlist:
                if i.endswith(".svg") or i.endswith(".jpg"):
                    fpath = [imageX] + i.split('/')
                    dest.addFromFile(os.path.join(*fpath), "imagefiles/" + i)
        dest.close()

    def slot_tempsave(self, arg):
        self.save(True)

    def save(self, onlytemp=False, force=False, imageX=None):
        """Save the data to a temporary file, close it and then ask if
        the original file should be replaced by it.
        If onlytemp is True, stop after saving the data to the
        temporary file, leaving the source file open, and fail if that
        didn't work first time. Otherwise the possibility of entering
        an alternative save path will be given.
        If force is True, don't ask, just do everything.
        If imageX is a directory path, get the images from there
        instead of from the source file
        """
        if not self.baseFolder:
            return
        cfgFile = os.path.join(self.baseFolder, self.source.cfgName + '.zip')
        tmpsave = cfgFile + '_'
        backup = cfgFile + '~'

        while True:
            try:
                if os.path.exists(tmpsave):
                    os.remove(tmpsave)
                self.saveData(tmpsave, imageX)
                if onlytemp:
                    messageDialog(_("Information"),
                            _("Saved as '%s'") % tmpsave)
                    return
                self.source.close()
                break

            except:
                traceback.print_exc()
                warning(_("Could not save data to '%s'") % tmpsave)
                if onlytemp:
                    return
                tmpsave = getFile(_("Save file to"),
                        startDir=os.path.dirname(tmpsave),
                        defaultSuffix="zip",
                        filter=(_("zip Files"), ("*.zip",)),
                        create=True)
                if isinstance(tmpsave, unicode):
                    tmpsave = tmpsave.encode('utf8')
            if not tmpsave:
                return


        if (not force) and (not confirmationDialog(_("Replace existing file?"),
                _("The changes have been saved to '%s'.\n"
                "Should this now replace the previous data?") % tmpsave)):
            return

        try:
            if os.path.exists(backup):
                os.remove(backup)
            if os.path.exists(cfgFile):
                os.rename(cfgFile, backup)
            os.rename(tmpsave, cfgFile)
            if imageX:
                self.baseFolder = None
                self.slot_openConfig(False)
            else:
                # For the control panel, to indicate that the file has
                # been saved:
                self.sourcePath = cfgFile
                self.validationObject.validateAll()
                self.errorCount = self.validationObject.errorCount
        except:
            traceback.print_exc()
            warning(_("Couldn't update configuration file '%s'") % cfgFile)

# self.currentSection is a list of field-item lists, in display order.
# These consist of [field-name, value, field-type-list, tip].
# The field-type list is the field specifier split at '|'.

    def slot_valueChange(self, rv):
        if self.disableChange:
            return

        row, value = rv
        entry = self.currentSection[row]
        entry[1] = value

        # This is to allow checking of changes to the error state of
        # the file
        newERC = self.errorRowCount
        if self.rowErrors[row]:
            newERC -= 1

        # Set the error state for the particular field
        vError = self.validate(value, entry[2])
        self.gui.setValid(row, vError)

        # Continue with checking the file error state
        self.rowErrors[row] = vError
        if vError:
            newERC += 1
        if ((newERC != self.errorRowCount) and (newERC == 0) or
                (self.errorRowCount == 0)):
            self.checkAll()

    def slot_switchNode(self, path):
        self.currentPath = path
        self.currentSpec = self.fileDict[path]

        # Block attempts to update the data
        self.disableChange = True

        self.gui.clearTable()
        self.rowErrors = []
        self.errorRowCount = 0
        if (self.currentSpec[1] == "="):
            self.currentSection = self.currentSpec[4]
            row = 0
            for sec in self.currentSection:
                ftype = sec[2][0]
                field = sec[0]
                value = sec[1]
                if (ftype == "bool"):
                    self.gui.addBoolField(sec[0], sec[1], sec[3])
                    vError = ''
                else:
                    self.gui.addField(sec[0], sec[1], sec[3])
                    vError = self.validate(sec[1], sec[2])
                    self.gui.setValid(row, vError)
                self.rowErrors.append(vError)
                if vError:
                    self.errorRowCount += 1

                row += 1

        else:
            self.currentSection = None

        if (self.currentSpec[1] == "="):
            self.gui.setComment(self.currentSpec[3])
        else:
            self.gui.clearComment()

        # Unblock attempts to update the data
        self.disableChange = False

    def slot_commentChanged(self, text):
        if self.disableChange:
            return
        self.currentSpec[3] = text

    def validate(self, value, spec):
        """Check the value against the field specification.
        If valid, return '', otherwise return an error message.
        """
        return self.validationObject.checkValue(value, spec, self.currentPath)

    def slot_clone(self, arg):
        """Make an exact copy of this node. Only 'non-fixed' nodes
        may be cloned.
        """
        spec = self.currentSpec
        if not spec:
            return
        if (spec[0] != '') or (spec[1] not in ('/', '=')):
            warning(_("Can't clone this node"))
            return

        fpath = self.currentPath.rstrip('/')
        spl = fpath.rsplit("/", 1)
        if (len(spl) == 1):
            basePath = ''
            oldName = fpath
        else:
            basePath, oldName = spl

        while True:
            filename = None
            if basePath.endswith('/pupils'):
                ipath = basePath[:-6] + 'info'
                try:
                    id = int(self.getField(ipath, 'lastId'))
                    if (id > 0):
                        id += 1
                        self.changeField(ipath, 'lastId', str(id))
                        filename = "%03d" % id
                except:
                    pass

            if not filename:
                filename = getFileName(oldName)
                if not filename:
                    return
            path = joinPath(basePath, filename)
            if (spec[1] == '/'):
                path += '/'
            if self.fileDict.has_key(path):
                warning(_("Node '%s' already exists") % filename)
            else:
                 break

        # Handle '='-files and folders separately
        if (spec[1] == '/'):
            # Folder
            self.cloneDir(self.currentPath, path, filename)

        elif (spec[1] == '='):
            # Information file
            self.cloneFile(path, filename, spec)

        else:
            return

        self.gui.sort(self.nodeDict[basePath + '/'])
        self.gui.setCurrentItem(self.nodeDict[path])
        self.checkAll()

    def cloneFile(self, newpath, name, spec):
        """Copy a file node to the new name, using the details
        in spec. path is the path of the new node.
        """
        # The specification list needs to be duplicated
        spec2 = list(spec)
        # But that's not enough, also the field lists
        spec2[4] = [list(l) for l in spec[4]]
        self.addnode(name, newpath, spec2)

    def cloneDir(self, oldpath, newpath, name):
        """Copy a folder node recursively. Note that oldpath
        and newpath are the paths including the folder to be
        copied.
        """
        spec = self.fileDict[oldpath]
        self.addnode(name, newpath, spec)

        dirs, files = dirList(self.fileDict.keys(), oldpath)

        files.sort()
        for f in files:
            spec = self.fileDict[oldpath + f]
            self.cloneFile(newpath + f, f, spec)

        dirs.sort()
        for d in dirs:
            self.cloneDir(oldpath + d + '/', newpath + d + '/', d)

    def slot_delete(self, arg):
        """The graphical items must be deleted but also the entries in
        self.fileDict.
        Only 'non-fixed' nodes may be deleted and then only when they
        are not the only one at that level.
        """
        spec = self.currentSpec
        if (spec[0] != ''):
            warning(_("Can't delete this node"))
            return

        spl = self.currentPath.rstrip('/').rsplit("/", 1)
        if (len(spl) == 1):
            basePath = ''
        else:
            basePath = spl[0] + '/'

        # Check for siblings
        baselen = len(basePath)
        for p in self.fileDict.keys():
            if p.startswith(basePath):
                if (p == self.currentPath):
                    continue
                rest = p[baselen:].rstrip('/')
                if (len(rest.split('/')) != 1):
                    continue
                specf = self.fileDict[p]
                if (specf[0] != '') or (specf[1] != spec[1]):
                    continue

                self.delete(self.currentPath)

                self.checkAll()
                return

        warning(_("This is the last node of its type, not deleting"))

    def delete(self, path):
        """This deletes a node and all its children.
        """
        # Get the graphical item
        item = self.nodeDict[path]
        # Delete the memory structures
        if path.endswith('/'):
            # Folder
            for p in self.fileDict.keys():
                if p.startswith(path):
                    del self.fileDict[p]
                    del self.nodeDict[p]
        else:
            del self.fileDict[path]
            del self.nodeDict[path]

        # Delete the gui items
        self.gui.deleteItem(item)

    def slot_getPupils(self, arg):
        """Import pupil data from csv files, one file per class.
        """
        columns = [f[0] for f in getSpec("classes/*/pupils/*")[3:]]
        csv = CsvData(self.settings.getSetting("csvData"))
        if not getCsvConfig(["id"] + columns, csv):
            return
        self.settings.setSetting("csvData", csv.setting)

        csvHandler = Csv2Sini(self, csv.separator, csv.columns)

        lastDir = self.settings.getSetting("csvDir")
        csvdir = csvHandler.init(lastDir)
        if not csvdir:
            return
        self.settings.setSetting("csvDir", csvdir)

        guiReport(_("Importing pupil data"), csvHandler, '')

        self.checkAll()
        self.gui.setCurrentItem(self.nodeDict["classes/"])

    def slot_replacePix(self, arg):
        """Replace the all images by the contents of a supplied folder.
        """
        sdir = getDirectory(_("Image Folder"))
        if not sdir:
            return
        # Perform a save operation, but instead of getting the images
        # from the (old) source file, get them from sdir.
        if isinstance(sdir, unicode):
            sdir = sdir.encode('utf8')
        self.save(imageX=sdir)

    def emptyDir(self, path):
        """Empty the directory node at the given path.
        """
        dirs, files = dirList(self.fileDict.keys(), path.rstrip('/') + '/')
        for f in (dirs + files):
            self.delete(joinPath(path, f))

    def addPupil(self, pupilPath, id, sinitext):
        """Used by the csv import utility to add a pupil.
        """
        for s in self.fileDict[pupilPath.rstrip('/') + '/'][3:]:
            if (s[0] == '') and (s[1] == '='):
                spec = s
                break
        self.addFile(pupilPath, id, spec, sinitext)

    def endPupils(self, classPath, idauto):
        """After all pupils have been entered for a class (using the
        csv import utility), make sure there is at least one pupil (!)
        and set the 'lastId' field in 'info'.
        """
        if (idauto == 0):
            self.addPupil(classPath + "/pupils", FDEFAULT, '')
            idauto = 1
        elif (idauto < 0):
            idauto = 0
        self.changeField(classPath + "/info", "lastId", str(idauto))

    def changeField(self, path, field, value):
        """Change one field of a file.
        """
        # First in the memory structure
        spec = self.fileDict[path]
        flist = spec[4]
        for sec in flist:
            if (sec[0] == field):
                sec[1] = value

    def getField(self, path, field):
        """Get the value of the given field in the given file.
        """
        spec = self.fileDict[path]
        flist = spec[4]
        for sec in flist:
            if (sec[0] == field):
                return sec[1]
        return None

