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
""" HTML tags syntax highlighting """

from qt import *
import re

class HTMLSyntax(QSyntaxHighlighter):
	def __init__(self,parent):
		""" sets up the highliting regex's and their funcs """
		QSyntaxHighlighter.__init__(self,parent)
		# order is important!
		self.modes = [
		{#tag
			'color':QColor("blue"),
			'regex':re.compile(r'(<\s*([A-Z][A-Z0-9]*)[^>]*>)(.*?)(<\s*/\2\s*>)',re.MULTILINE|re.IGNORECASE),
			'func' :self.tagre,
			'complete': 1
		},
		{#string inside tag
			'color':QColor("red"),
			'regex':re.compile(r'<(?:.*?)=\s*"(.*?)"',re.MULTILINE),
			'func' :self.strre,
			'complete': 1
		},
		{#comments
			'color':QColor("gray"),
			'regex':re.compile(r'<!--'),
			'ending':re.compile(r'-->',re.MULTILINE),
			'func' :self.comre,
			'complete': 0,
			'code': 3
		}
		]
	
	def tagre(self,match,color):
		self.setFormat(match.start(1),match.end(1)-match.start(1),color)
		self.setFormat(match.start(4),match.end(4)-match.start(1),color)
	
	def strre(self,match,color):
			self.setFormat(match.start(1),match.end(1)-match.start(1),color)
	
	def comre(self,start,end,color):
			self.setFormat(start,end-start,color)

	def match_ending(self, mode, start, text):
		func = mode['func']
		match = mode['ending'].search(text, start)
		if match:
			end = match.end()
			func(start, end, mode['color'])
			return end, 0
		else:
			end = len(text)
			func(start, end, mode["color"])
			return end, mode["code"]

	def highlightParagraph (self, text, endStateOfLastPara):
		t = unicode(text)
		i = 0
		if endStateOfLastPara > 0 and endStateOfLastPara <= len(self.modes):		
			mode = self.modes[endStateOfLastPara-1]
			i, code = self.match_ending(mode, i, t)
			if code != 0:
				return code
	
		while i < len(t):
			matches = []
			for mode in self.modes:
				match = mode['regex'].search(t, i)
				if match:
					matches.append( (match.start(), match, mode) )
		
			if matches == []:
				return 0
		
			# Find the first match.
			matches.sort()
			start, match, mode = matches[0]
			if mode["complete"]:
				func = mode["func"]
				func(match, mode["color"])
				i = match.end()
			else:
				i, code = self.match_ending(mode, match.start(), t)			
				if code != 0:
					return code

		return 0
