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

import Status, qt , sys

class Notifier:
    def __init__(self, parent, mode, args = None):
        self.parent = parent
        if mode == 0 :
            try:
                import OSD
                self.display = OSD.OSD()
            except Exception, inst:
                print "Exception while loading OSD: " + str(inst)
                qt.QMessageBox.warning(None,
                self.parent.trUtf8("Warning"),
                self.parent.trUtf8("""Seems like you don't have PyOSD installed!\nReverting to status bar notifications"""))
                self.display  = Status.StatusNotifier(parent,args)
        elif mode == 1:
            self.display  = Status.StatusNotifier(parent,args)
        else:
            print "What the hell?"
            sys.exit()
        for method in [mname for mname in dir(self.display) if len(mname)>2 and mname[:2] != '__' ]:
            setattr(self, method, getattr(self.display, method))
