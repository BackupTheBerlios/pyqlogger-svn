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

class StatusNotifier:
    def __init__(self, parent,ctrl):
        self.parent = parent
        self.progressBar = ctrl
        
    def error(self, msg):
        self.parent.statusLabel.setText("<font color='red'>%s</font>"%msg)

    def info(self, msg):
        self.parent.statusLabel.setText(msg)

    def warn(self, msg):
        self.parent.statusLabel.setText(msg)

    def status(self, msg):
        self.parent.statusLabel.setText(msg)

    def progress(self, completed, total):        
        self.progressBar.setProgress(completed, total)
