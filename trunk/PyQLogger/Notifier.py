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
""" Wrapper module for displaying notifications """

import OSD,Status

class Notifier:
    def __init__(self,parent,mode):
        self.parent = parent
        if mode == 0 :
            self.display = OSD.OSD()
        elif mode == 1:
            self.display  = Status.StatusNotifier(parent)
        else:
            print "What the hell?"
            sys.exit()
        for m in filter(lambda x: len(x)>2 and x[:2] != '__' , dir(self.display)):
            setattr(self,m,getattr(self.display,m))
