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

__revision__ = "$Id: Status.py 132 2005-02-06 15:29:06Z reflog $"

from kdeui import KPassivePopup
from kdecore import KIconLoader, KIcon

class KdePopupNotifier:
    def __init__(self, parent):
        self.parent = parent
        self.PassivePopup = KPassivePopup()        
        IconLoader   = KIconLoader()        
        self.icoCancel = IconLoader.loadIcon('cancel', KIcon.Small)
        self.icoInfo = IconLoader.loadIcon('info', KIcon.Small)
        self.st = parent.systray

    def error(self, msg, hold=False):
        self.PassivePopup.setTimeout( (30,-1)[hold] )
        self.PassivePopup.message("PyQLogger Status:", msg, self.icoCancel, self.st)

    def info(self, msg, hold=False):
        self.PassivePopup.setTimeout( (30,-1)[hold] )
        self.PassivePopup.message("PyQLogger Status:", msg, self.icoInfo, self.st)

    def warn(self, msg, hold=False):
        self.PassivePopup.setTimeout( (30,-1)[hold] )
        self.PassivePopup.message("PyQLogger Status:", msg, self.icoCancel, self.st)

    def status(self, msg, hold=False):
        self.PassivePopup.setTimeout( (30,-1)[hold] )
        self.PassivePopup.message("PyQLogger Status:", msg, self.icoInfo, self.st)

