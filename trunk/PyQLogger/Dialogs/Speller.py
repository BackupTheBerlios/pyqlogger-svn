## $Id: SpellForm_Impl.py 65 2004-12-15 20:36:03Z mightor $
## This file is part of PyQLogger.
## 
## Copyright (c) 2004 Eli Yukelzon a.k.a Reflog
##                    Xander Soldaat a.k.a. Mightor
##
## PyQLogger is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
## 
## PyQLogger is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with PyQLogger; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# -*- coding: utf-8 -*-
"""
Simple Spell Checker using ASpell
"""
from qt import *
import re,sys

class Speller:
    _digitRegex = re.compile(r"^\d")
    _htmlRegex = re.compile(r"</[c-g\d]+>|</[i-o\d]+>|</[a\d]+>|</[q-z\d]+>|<[cg]+[^>]*>|<[i-o]+[^>]*>|<[q-z]+[^>]*>|<[a]+[^>]*>|<(\[^\]*\|'[^']*'|[^'\>])*>", re.IGNORECASE|re.MULTILINE)
    _htmlTags = None
    _letterRegex = re.compile(r"\D")
    _upperRegex = re.compile(r"[^A-Z]")
    _wordEx = re.compile(r"\b\w+\b", re.MULTILINE|re.UNICODE|re.LOCALE)

    def __init__(self,parent):
        self.parent = parent
        self.notcapable = False
        try:
            import aspell
        except:
            QMessageBox.warning(None,
                self.trUtf8("Error"),
                self.trUtf8("""Seems like you don't have ASpell bindings installed!\nYou can get it from http://prdownloads.sourceforge.net/uncpythontools/aspell-1.0.zip?download"""))
            self.notcapable = True
            return
        try:
            self.speller = aspell.spell_checker(prefix='/usr')
        except:
            QMessageBox.warning(None,
                self.trUtf8("Error"),
                self.trUtf8("""ASpell module couldn't be initialized!"""))
            self.notcapable = True

    def CalculateWords(self):
        """Calculates the words from the Text property"""
        #splits the text into words
        self._words = []
        for m in self._wordEx.finditer(self.text):
            self._words.append(m) 
        self.MarkHtml()

    def CheckString(self,word,characters):
        """Determines if the string should be spell checked
        @param characters The Characters to check
        Returns true if the string should be spell checked
        """     
        if not self._upperRegex.match(characters):  return False
        if self._digitRegex.match(characters):  return False
        if not self._letterRegex.match(characters): return False
        startIndex = word.start()
        for item in self._htmlTags:
            if (startIndex >= item.start() and startIndex <= item.end() - 1):
                return False
        return True;

    def MarkHtml(self):
        """Calculates the position of html tags in the Text property"""
        # splits the text into words
        self._htmlTags = []
        for m in self._htmlRegex.finditer(self.text):
            self._htmlTags.append(m)

    def ReplaceWord(self, replacedIndex, _replacementWord):
        """ Replaces the instances of the CurrentWord in the Text Property """
        if not self._words or not len (self._words):
            return
        replacedWord = self._words[replacedIndex].group(0)
        index = self._words[replacedIndex].start()
        length = self._words[replacedIndex].end()
        # if first letter upper case, match case for replacement word
        if replacedWord.istitle():          
            _replacementWord = _replacementWord.title()
        tmps = self.text[index: length].replace(replacedWord,_replacementWord)
        self.text = self.text[:index] + tmps + self.text[length:]
        self.CalculateWords()

    def load(self,text):
        self.text = unicode(text)
        self.CalculateWords()
        self.cur_word = 0
        ret = {}
        self.keepChecking(ret)
        return ret

    def keepChecking(self, ret):        
        if self.cur_word < len(self._words):
            w = self._words[ self.cur_word ]
            word = w.group(0)
            if self.CheckString(w,word) and not self.speller.check(word):  # should we even check it?
                    sug = self.speller.suggest(word)
                    ret[word] =  { "word":w, "sug": sug, "idx":self.cur_word } 
            self.cur_word += 1
            self.keepChecking(ret)



    def btnAdd_clicked(self):
        self.speller.add_to_personal(self._words [ self.cur_word ].group(0))
        self.cur_word += 1
        self.viewText.setText(self.text)
        self.keepChecking()

    def btnReplace_clicked(self):
        if unicode(self.editReplace.text()):
            self.ReplaceWord(unicode(self.editReplace.text()))
            self.cur_word += 1
            self.viewText.setText(self.text)
            self.keepChecking()

    def btnReplaceAll_clicked(self):
        if unicode(self.editReplace.text()):
            d = self._words [ self.cur_word ].group(0)
            self.btnReplace_clicked()
            # check if the user made he's own replacement
            if not self.listVariants.findItem(self.editReplace.text(),Qt.ExactMatch):
                self.speller.store_replacement(d,unicode(self.editReplace.text()))
            self.cur_word += 1
            self.viewText.setText(self.text)
            self.keepChecking()


    def btnCancel_clicked(self):
        self.reject()

    def listVariants_doubleClicked(self,a0):
        self.editReplace.setText(a0.text())

