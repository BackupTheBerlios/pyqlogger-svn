#! /usr/bin/python
## $Id$
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
import  PyQLogger.KdeQt 
from PyQLogger import *
import sys
import os

try:
	from qt import *
except:
	print """Could not locate the PyQt module.  Please make sure that
you have installed PyQt for the version of Python that you are running."""
	sys.exit(1)


VERSION = '1.3.2'

def main():
	a =  PyQLogger.KdeQt.KQApplication(sys.argv,None)
	QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
	w = MainForm_Impl.MainForm_Impl()
	if w.init():
		a.setMainWidget(w)
		PyQLogger.KdeQt.setupKDE(a,w)
		w.show()
		res = a.exec_loop()
		sys.exit(res)


if __name__ == '__main__':
	main()

