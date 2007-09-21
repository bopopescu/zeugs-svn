#!/usr/bin/env python
# -*- coding: utf-8 -*-

#2007-06-27
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
"""The dialog for interactive spell-checking.
"""

from guiCheckSpell import NUGui

class CheckSpell:
    def __init__(self):
        self.gui = None

    def start(self, lines):
        """Spellcheck the list of TextLine objects in 'lines'.
        """
        if not self.gui:
            self.gui = NUGui(self)

        self.gui.show()
        self.tlines = lines
        self.para = None
        self.text = u"" # Build up whole text as string
        self.line = u"" # Build up a single display line as string
        self.lx = 0     # line index
        self.wx = 0     # word index
        self.subList = {}   # substitution list
        self.altered = False    # flag to indicate text changed
        self.readText()

    def readText(self, skip=False):
        """Read up to the next spelling mistake, copying completed
        lines to the text buffer.
        When a mistake is encountered, display its line with the word
        in question highlighted somehow.
        If skip is True, don't report mistakes, just read to the end
        of the text, to complete the text buffer.
        """
        while True:     # loop over text lines
            tline = self.tlines[self.lx]
            if (tline.para != self.para):
                # start of paragraph
                if (self.lx != 0):
                    # not first paragraph
                    self.text += u"\n"
                self.ch = u""
                self.para = tline.para
                self.text += tline.para.getFormat()
            else:
                self.ch = u" "

            twords = tline.twords
            while (self.wx < len(twords)):
                tw = twords[self.wx]
                self.word = tw.string
                self.wx += 1

                if checkSpelling.check(self.word) or skip:
                    self.line += self.ch + self.word
                    self.ch = u" "
                    continue

                w2 = self.subList.get(checkSpelling.falseWord)
                if w2:
                    self.line += self.ch + \
                            self.word.replace(checkSpelling.falseWord, w2)
                    self.ch = u" "
                    continue

                # Spelling mistake. Display current line with mistake
                # highlighted, and entered into line edit.
                if self.line:
                    text = u"%s " % self.line
                else:
                    text = u""

                text += self.word.replace(checkSpelling.falseWord, u"%s")

                restOfLine = tline.getText(self.wx)
                if restOfLine:
                    text += u" %s" % restOfLine
                self.gui.setText(text, checkSpelling.falseWord)
                suglist = checkSpelling.suggest()
                self.gui.setSuggestions(suglist)
                return

            # End of line
            self.text += self.line
            self.line = u""
            self.lx += 1
            self.wx = 0
            if (self.lx >= len(self.tlines)):
                break

        signal("endCheckSpelling")
        message(_("Spelling check completed"))
        self.gui.hide()

    def ignore(self, skip=False):
        self.line += self.ch + self.word
        self.ch = u" "
        self.readText(skip)

    def ignoreAll(self):
        self.altered = True
        checkSpelling.ignoreWord(self.word)
        self.ignore()

    def addWord(self):
        self.altered = True
        checkSpelling.addWord(self.word)
        self.ignore()

    def subWord(self, word):
        self.altered = True
        self.word = self.word.replace(checkSpelling.falseWord, word)
        self.ignore()

    def subWordAll(self, word):
        self.subList[self.falseWord] = word
        self.subWord(word)

