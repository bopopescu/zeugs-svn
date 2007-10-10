#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#2007-09-19
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

defaultLetters = u"a-zA-Z"

import re
import __builtin__
import os

import enchant

from checkSpell import CheckSpell

class SpellCheck:
    def __init__(self):
        self.setReP(None)

    def setReP(self, dictionary, letters=u""):
        """Set the dictionary and accepted set of letters.
        """
        if dictionary:
            try:
                if isinstance(dictionary, unicode):
                    dictionary = str(dictionary)
                self.d = enchant.DictWithPWL(dictionary,
                        os.path.join(os.path.expanduser('~'),
                        "mywords_%s" % dictionary))
            except:
                warning(_("Couldn't find dictionary for language %s.\n"
                        "Spelling checks will be disabled") % dictionary)
                self.d = None
        else:
            self.d = None
        llist = defaultLetters + letters
        self.reP = re.compile(ur"([^%s]*)([%s\-]*)(.*)" % (llist, llist))

    def ignoreWord(self, word):
        """Ignore this word throughout the document.
        """
        if not self.d:
            return
        self.d.add_to_session(self.falseWord)

    def addWord(self, word):
        """Add this word to the personal word list.
        """
        if not self.d:
            return
        self.d.add_to_pwl(self.falseWord)

    def suggest(self):
        """Return a list of suggestions for the given word.
        """
        if not self.d:
            return
        return self.d.suggest(self.falseWord)

    def check(self, string):
        """Check the spelling of (words within) the string.
        Return True if ok.
        """
        # Because of the way TWords are built, only the whole block can
        # be marked as ok or not. A correction dialog could, however,
        # separate out the individual words.
        if not self.d:
            return True
        pre, m, post = self.reP.match(string).groups()
        while m:
            if not self.d.check(m):
                m = m.strip(u".-")
                if not self.d.check(m):
                    self.falseWord = m
                    return False
            pre, m, post = self.reP.match(post).groups()
        return True

def spellInit():
    __builtin__.autoSpellCheck = False
    __builtin__.checkSpelling = SpellCheck()
    __builtin__.checkSpell = CheckSpell()

#>>> d.suggest("Helo")
#['He lo', 'He-lo', 'Hello', 'Helot', 'Help', 'Halo', 'Hell', 'Held',
#'Helm', 'Hero', "He'll"]
#>>>

# The suggestions are returned in a list, ordered from most likely
#replacement to least likely.
# Once a correction is made to a miss-spelled word, it is often useful
#to store this correction in some way for later use. The Dict object
#provides several methods to handle this:

#add_to_pwl: store an unrecognised word in the user's personal
#            dictionary so that it is recognised as correct in the future.
#add_to_session:
#            store an unrecognised word so that it will be recognised
#            as correct while the Dict object is still in use.
#store_replacement:
#            note that one word was used to replace another, meaning
#            that it will appear higher in the list of suggestions in
#            the future.

