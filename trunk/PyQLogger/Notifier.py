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
__revision__ = "$Id$"
""" Wrapper module for displaying notifications """

import qt , sys
from Notifiers import Status

class Notifier:
    def __init__(self, parent, mode, args = None):
        self.parent = parent
        fallback = False
        self.mode = mode
        if mode == 0 :
            try:
                from Notifiers import OSD
                self.display = OSD.OSD()
            except Exception, inst:
                print "Exception while loading OSD: " + str(inst)
                print """Seems like you don't have PyOSD installed!\nReverting to status bar notifications"""
                fallback = True
        elif mode == 2:
            try:
                from Notifiers import KdePopup
                self.display = KdePopup.KdePopupNotifier(parent)
            except Exception, inst:
                print "Exception while loading Kde Popup: " + str(inst)
                print """Seems like you don't have PyKde installed!\nReverting to status bar notifications"""
                fallback = True
        if mode == 1 or fallback:
            self.mode = 1
            self.display  = Status.StatusNotifier(parent,args)

    def error(self, msg):
        self.display.error(msg)        
        self.parent.log.error(msg)
        
    def info(self, msg):
        self.display.info(msg)
        self.parent.log.info(msg)
        
    def warn(self, msg):
        self.display.warn(msg)
        self.parent.log.warning(msg)
        
    def status(self, msg):
        self.display.status(msg)
        self.parent.log.info(msg)
        
        
