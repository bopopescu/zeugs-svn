#!/usr/bin/env python
# -*- coding: utf-8 -*-

#2007-09-17
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
"""The structure of the configuration data is defined here.
This information is structured hierarchically using folders. The
individual items of data are mostly stored in files using a simplified
'ini' structure.

Field definitions are of the form:

    field-name = value

The information in the data structure below is used for verifying
a set of data, in addition to documenting the structure.
The valid items are presented as a nested list. There are also
validity checks for individual data (field) items, and brief
descriptions of each item, which may be translated.

The field tuples are of the form:
    (<field-name>, <verifier>, <description>),

The file/folder tuples are of the form:
    (<file-name>, <file-type>, <description>, <contents>, ...)

If <file-name> is empty, an indefinite number of user-defined
names may be used.
<file-type>: '/' - Folder
             '=' - 'sini' (data) file
             'i' - image file

The available verifiers are:
    "int|default|min|max" : integer
    "flt|default|min|max" : floating point
    ""                    : anything
    "!<function>"         : 'custom' check
    "bool|default"        : boolean, '0' for false or '1' for true
    "table|<table-name>   : check against other table, <table-name> is
        the ('/'-separated) path relative to the folder containing
        the current dictionary ('^' signifies parent folder),
        unless it is preceded by '@', in which case it is relative to
        the data root
    "table?|<table-name>  : as 'table' but may also be '0'
    "colour|default"      : a colour in #rrggbb form, e.g. '#a3528f'
    "choice|default|list" : one of the given (' '-separated) list

The ordering of the files in the list determines the order in which
they will be parsed and checked by the verifier, which could be
important in the case of cross-references.
"""

def dataDefinition():
    return (

    ("imagefiles", "/", _("Folder containing image (picture) files used in the reports"),
        ("teachers", "/", _("Folder containing teachers signatures as images"),
            ("", "i", _("An image file (svg-format)")),
        ),

        ("", "i", _("An image file (svg-format)")),
    ),

    ("layouts", "/", _("Folder containing layout definitions"),
        ("", "/", _("Folder containing a single layout definition"),

            ("fonts", "/", _("Font definitions"),
                ("", "=", _("A single font definition"),
                    ("family", "!fontFamily",
                            _("The name of the font family, e.g. 'DejaVu Sans'")),
                    ("points", "flt|11|5|100",
                            _("Font size in points")),
                    ("weight", "int|40|0|100",
                            _("Font weight (0-100)")),
                    ("stretch", "flt|1|0.5|2",
                            _("Stretch factor, unstretched is 1.0")),
                    ("style", "bool|0",
                            _("Use italic/sloped style (boolean)")),
                    ("underline", "bool|0",
                            _("Underlined font (boolean)")),
                    ("lineSpacing", "flt|1|0.5|2",
                            _("Line spacing factor, normal is 1.0")),
                    ("colour", "colour|#505050",
                            _("The colour of the font, in #rrggbb format, hex values")),
                ),
            ),

            ("text", "/", _("Text object definitions"),
                ("", "=", _("A single text object definition"),
                    ("font", "table|^^fonts",
                            _("The font for this text")),
                    ("text", "",
                            _("The text to display")),
                ),
            ),

            ("lines", "/", _("Line object definitions"),
                ("", "=", _("A single line object definition"),
                    ("width", "flt|0.3|0.02|5",
                            _("The thickness of the line")),
                    ("colour", "colour|#505050",
                            _("The colour of the line, in #rrggbb format, hex values")),
                    ("x0", "flt|0|-20|300",
                            _("Starting x-coordinate")),
                    ("x1", "flt|170|-20|300",
                            _("Ending x-coordinate")),
                    ("y0", "flt|0|-20|300",
                            _("Starting y-coordinate")),
                    ("y1", "flt|0|-20|300",
                            _("Ending y-coordinate")),
                ),
            ),

            ("images", "/", _("Image object definitions"),
                ("", "=", _("A single image object definition"),
                    ("file", "table|@imagefiles",
                            _("The file (in the 'imagefiles' folder) containing this image")),
                    ("vsize", "flt|5|1|300",
                            _("The vertical size of this image")),
                ),
            ),

            ("frames", "/", _("Frame configuration information"),
                ("", "=", _("A single frame definition"),
                    ("topMargin", "flt|8|0|20",
                            _("Space above report text")),
                    ("bottomMargin", "flt|0|0|20",
                            _("Space below report text")),
                    ("firstLineIndent", "flt|0|0|20",
                            _("Indentation of first text line")),
                    ("firstLineRelative", "bool|0",
                            _("Indentation relative to title (boolean)")),
                    ("title", "",
                            _("Format string for title")),
                    ("titleRight", "bool|0",
                            _("The title is placed at the right of the frame (boolean)")),
                    ("titleOnEmpty", "bool|0",
                            _("The title is shown even in empty frames (boolean)")),
                    ("titlex", "flt|0|-10|20",
                            _("x-offset of title (relative to chosen margin)")),
                    ("titley", "flt|8|0|20",
                            _("y-offset of title")),
                    ("signatureHeight", "flt|0|0|20",
                            _("Height of signature image, '0' implies don't use image")),
                    ("signatureLeft", "bool|0",
                            _("The image is placed at the left of the frame (boolean)")),
                    ("signaturex", "flt|0|0|300",
                            _("x-offset for image")),
                    ("signaturey", "flt|10|0|20",
                            _("y-offset for image")),
                    ("teacher", "",
                            _("Format string for teacher's name")),
                    ("teacherLeft", "bool|0",
                            _("The name is placed at the left of the frame (boolean)")),
                    ("teacherBottom", "bool|0",
                            _("The name is placed at the bottom of the frame (boolean)")),
                    ("teacherOnSignature", "bool|0",
                            _("Teacher's name is displayed regardless of image (boolean)")),
                    ("teacherAllFrames", "bool|0",
                            _("Teacher's name is displayed in all frames, else at most one (boolean)")),
                    ("teacherx", "flt|0|-10|20",
                            _("x-offset of name (relative to chosen margin)")),
                    ("teachery", "flt|8|0|20",
                            _("y-offset of name (relative to chosen margin)")),
                    ("height", "flt|50|20|300",
                            _("Height of frame")),
                    ("minHeight", "flt|50|0|300",
                            _("Minimum height of frame")),
                    ("strikeOut", "table?|^^lines",
                            _("Select behaviour when no report for a subject is available: Skip, Title, Empty, StrikeOut")),
                ),
            ),

            ("subject_frames", "/", _("Display information for subjects"),
                ("", "=", _("Information for a single subject"),
                    ("display-name", "",
                            _("The name which is displayed for this subject")),
                    ("frames", "!frameList",
                            _("These frames contain the given subject")),
                ),
            ),

            ("blocks", "/", _("Subject-block object definitions"),
                ("", "=", _("Information for a single subject-block"),
                    ("separator", "table?|^^lines",
                            _("The line to separate reports, '0' => none")),
                    ("height", "flt|50|20|300",
                            _("Vertical space for block")),
                    ("subject-list", "!subjectList",
                            _("List of subjects to put in this block, if they fit")),
                ),
            ),

            ("sheets", "/", _("Folder containing sheet definitions"),
                ("", "=", _("Single sheet definition"),
                    ("size", "choice|A3|A3 A4", _("The paper size")),
                ),
            ),

            ("pages", "/", _("Folder containing page definitions"),
                ("", "/", _("Single page definition"),
                    ("_info_", "=", _("General information about the page"),
                        ("sheet", "table|^^^sheets",
                                _("Which sheet of the complete report")),
                        ("back", "bool|0",
                                _("Which side of the sheet (boolean)")),
                        ("leftSpace", "flt|20|0|50",
                                _("Horizontal offset of page area")),
                        ("position", "choice|0|0 1",
                                _("Which page position on sheet (A3 only)")),
                    ),

                    ("", "=", _("Individual object placement on the page"),
                        ("object", "table|^^^",
                                _("Type of object and its identifier: <type>/<id>")),
                        ("x","flt|0|-20|300",
                                _("x-coordinate of item")),
                        ("y","flt|0|-20|300",
                                _("y-coordinate of item")),
                    ),
                ),
            ),

            ("document", "=", _("Data concerning the whole document"),
                ("pages", "!pageList",
                        _("Individual pages in rendering order")),
                ("pageWidth", "flt|210|140|330",
                        _("The width of the layout page")),
                ("pageHeight", "flt|297|140|330",
                        _("The height of the layout page")),
                ("topSpace", "flt|20|0|40",
                        _("Top margin, y-axis offset")),
                ("textAreaWidth", "flt|170|100|300",
                        _("Width of content area")),
                ("textAreaHeight", "flt|257|100|300",
                        _("Height of content area")),
                ("normalFont", "table|^fonts",
                        _("Font for report texts")),
                ("xText0", "flt|0|-10|30",
                        _("Text indentation (whole paragraph)")),
                ("xPara1", "flt|0|-10|30",
                        _("Additional indentation for first line of paragraph")),
                ("specialFont", "table|^fonts",
                        _("Font for 'special' text")),
                ("xSpecialDefault", "flt|0|-10|100",
                        _("Default indentation of special text")),
                ("titleFont", "table|^fonts",
                        _("Font for title")),
                ("signatureFont", "table|^fonts",
                        _("Font for teacher's name")),
                ("justify", "bool|1",
                        _("Full justification (boolean)")),
            ),

        ),
    ),

    ("base", "=", _("Data concerning the whole system"),
        ("schoolYear", "",
                _("School-year, as it should appear in the reports")),
        ("mainHost", "",
                _("Network-address of the main database")),
        ("dictionary", "",
                _("The name of the dictionary for spell-checking, e.g. 'de_DE' for German")),
        ("extraChars", "",
                _("Special, non-ASCII, characters (language-dependent)")),
    ),

    ("teachers", "/", _("Information about the teachers"),
        ("", "=", _("Individual teacher information"),
            ("Name", "",
                    _("The teacher's (real) name")),
        ),
    ),

    ("classes", "/", _("Folder containing class information"),
        ("", "/", _("Folder containing information for a single class"),
            ("info", "=", _("General information about the class"),
                ("Name", "",
                        _("The actual (displayed) name for the class")),
                ("Layout", "table|@layouts",
                        _("The layout definition to be used for this class")),
                ("lastId", "int|1|0|999",
                        _("Last automatically allocated pupil id."
                        " In general, don't touch it!")),
            ),

            ("subjects", "/", _("Information about the courses taught"),
                ("", "=", _("Information about a single course"),
                    ("Teacher", "table|@teachers",
                            _("Teacher's 'tag' (short identifier)")),
                    ("CGroup", "",
                            _("The teaching group (class subset)")),
                ),
            ),

            ("pupils", "/", _("Information about the pupils"),
                ("", "=", _("Information about a single pupil"),
                    ("LastName", "",
                            _("Pupil's surname")),
                    ("FirstNames", "",
                            _("Pupil's forenames")),
                    ("DateOfBirth", "",
                            _("Pupil's date of birth")),
                    ("PlaceOfBirth", "",
                            _("Pupil's place of birth")),
                    ("Groups", "",
                            _("The teaching groups (class subsets), space-separated")),
                ),
            ),

        ),
    ),

)


def getSpec(path):
    """Return the specification for the given path.
    Empty file-names are denoted by '*' instead of '', just to make
    it more visible and not look like a mistake.
    """
    s = getLevel(dataDefinition(), path)
    if s:
        return s
    bug(_("No specification for path '%s'") % path)

def getLevel(spec, path):
    """Used only be getSpec.
    """
    ci = path.split('/', 1)
    if (len(ci) == 1):
        child = None
        item = path
    else:
        item, child = ci
    if (item == '*'):
        item = ''

    for i in spec:
        if (item == i[0]):
            if (child == None):
                return i
            return getLevel(i[3:], child)

    return None
