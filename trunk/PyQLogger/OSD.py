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
""" Wrapper module for PyOSD """
import sys

try:
	import pyosd
except:
	print """Could not locate the PyOSD module.  Please make sure that
you have installed PyOSD for the version of Python that you are running."""
	sys.exit(1)

class OSD:
	def __init__(self,font='-adobe-*-*-*-*-*-60-*-*-*-*-*-*-*'):
		self.osd = pyosd.osd(font)
		self.osd2 = pyosd.osd(font)
		self.osd.set_align(pyosd.ALIGN_CENTER)
		self.osd.set_pos(pyosd.POS_MID)
		self.osd2.set_align(pyosd.ALIGN_LEFT)
		self.osd2.set_pos(pyosd.POS_BOT)
		
	def error(self,msg):
		self.osd.set_colour('red')
		self.osd.display(msg,pyosd.TYPE_STRING,1)

	def info(self,msg):
		self.osd.set_colour('blue')
		self.osd.display(msg,pyosd.TYPE_STRING,1)

	def warn(self,msg):
		self.osd.set_colour('yellow')
		self.osd.display(msg,pyosd.TYPE_STRING,1)

	def status(self,msg):
		self.osd2.set_colour('black')
		self.osd2.display(msg,pyosd.TYPE_STRING,1)
