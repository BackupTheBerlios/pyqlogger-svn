## This file is part of PyQLogger.
## 
## Copyright (c) 2004 Eli Yukelzon a.k.a Reflog 		
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
""" This module contains all functions to be called from 
the toolbar. The mapping is done thru Button->Func method
"""

def initToolbar(self):
	toobarMap = {}
	toobarMap[self.tbBold] = makeBold
	toobarMap[self.tbItalic] = makeItalic
	toobarMap[self.tbUnder] = makeUnderscore
	toobarMap[self.tbLeft] = alignLeft
	toobarMap[self.tbCenter] = alignCenter
	toobarMap[self.tbRight] = alignRight
	toobarMap[self.tbHr] = insertHR
	toobarMap[self.tbUrl] = insertUrl
	toobarMap[self.tbImg] = insertImage
	toobarMap[self.tbBr] = insertBR
	toobarMap[self.tbFontPlus] = incFont
	toobarMap[self.tbFontMinus] = decFont
	toobarMap[self.tbUl] = makeUnorderedList
	toobarMap[self.tbOl] = makeOrderedList

	return toobarMap

def surroundWith(self,tag,param=''):
	text = str(self.sourceEditor.selectedText())
	self.sourceEditor.removeSelectedText()
	line, index = self.sourceEditor.getCursorPosition()
	if param != '': 
		tagp = "%s %s" % (tag, param)
	else:
		tagp = tag
	self.sourceEditor.insertAt("<%s>%s</%s>"%(tagp,text,tag), line, index)
	

def makeBold(self): surroundWith(self,'b')
	
def makeItalic(self): surroundWith(self,'i')

def makeUnderscore(self): surroundWith(self,'u')
	
def alignLeft(self): surroundWith(self,'div','align="left"')

def alignCenter(self):surroundWith(self,'div','align="center"')

def alignRight(self):surroundWith(self,'div','align="right"')

def insertHR(self):
	line, index = self.sourceEditor.getCursorPosition()
	self.sourceEditor.insertAt("<HR>", line, index)

def insertUrl(self):
	pass

def insertImage(self):
	pass

def insertBR(self):
	line, index = self.sourceEditor.getCursorPosition()
	self.sourceEditor.insertAt("<BR>\n", line, index)
	
def incFont(self):surroundWith(self,'font','size="+1"')

def decFont(self):surroundWith(self,'font','size="-1"')

def makeUnorderedList(self):
	text = str(self.sourceEditor.selectedText())
	self.sourceEditor.removeSelectedText()
	lines = ["<li>%s</li>"%(line) for line in text.split("\n")]
	newtext = "<ul>\n%s\n</ul>" % ( "\n".join(lines) )
	line, index = self.sourceEditor.getCursorPosition()
	self.sourceEditor.insertAt(newtext, line, index)
	

def makeOrderedList(self):
	text = str(self.sourceEditor.selectedText())
	self.sourceEditor.removeSelectedText()
	lines = ["<li>%s</li>"%(line) for line in text.split("\n")]
	newtext = "<ol>\n%s\n</ol>" % ( "\n".join(lines) )
	line, index = self.sourceEditor.getCursorPosition()
	self.sourceEditor.insertAt(newtext, line, index)
