#! /usr/bin/python
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
from PyQLogger import MainForm_Impl, KdeQt
import sys

try:
    from qt import QObject, SIGNAL, SLOT
except ImportError, e:
    print """Could not locate the PyQt module.  Please make sure that
you have installed PyQt for the version of Python that you are running."""
    sys.exit(1)

VERSION = '1.3.3.0'
__revision__ = "$Id$"

def main():
    app =  KdeQt.KQApplication(sys.argv, None)
    stat = KdeQt.prepareCommandLine()    
    QObject.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))
    wnd = MainForm_Impl.MainForm_Impl(statusbar=stat)
    if wnd.init():
        app.setMainWidget(wnd)
        KdeQt.setupKDE(app, wnd)
        wnd.show()
        res = app.exec_loop()
        sys.exit(res)


if __name__ == '__main__':
    main()

