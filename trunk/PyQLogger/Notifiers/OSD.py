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

__revision__ = "$Id: OSD.py 87 2004-12-21 16:25:48Z reflog $"
from __future__ import division
import pyosd

class OSD:
    def __init__(self, font='-adobe-*-*-*-*-*-60-*-*-*-*-*-*-*'):
        self.osd = pyosd.osd(font)
        self.osd2 = pyosd.osd(font)
        self.osd.set_align(pyosd.ALIGN_CENTER)
        self.osd.set_pos(pyosd.POS_MID)
        self.osd2.set_align(pyosd.ALIGN_LEFT)
        self.osd2.set_pos(pyosd.POS_BOT)
        
    def error(self, msg, hold=False):
        self.osd.set_colour('red')
        self.osd.display(msg, pyosd.TYPE_STRING, 1)

    def info(self, msg, hold=False):
        self.osd.set_colour('blue')
        self.osd.display(msg, pyosd.TYPE_STRING, 1)

    def warn(self, msg, hold=False):
        self.osd.set_colour('yellow')
        self.osd.display(msg, pyosd.TYPE_STRING, 1)

    def status(self, msg, hold=False):
        self.osd2.set_colour('black')
        self.osd2.display(msg, pyosd.TYPE_STRING, 1)

    def progress(self,completed,total):
        self.osd.set_colour('blue')
        if total: 
            pct = int(completed/total*100)
        else:
            pct = 100
        self.osd.display(pct, pyosd.TYPE_PERCENT, 1)
