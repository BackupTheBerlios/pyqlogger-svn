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

from Plugin import Plugin

class ToolbarPlugin (Plugin):
  """  Base class for plugins that provide a control on the toolbar  """

  ToolbarName = "Plugins" # on what toolbar to create the widget
  
  def getWidget(self, parent):
    """    Should return the widget(control) that will be added to the toolbar    """
    pass

  def description(self):
    return "(%s) Toolbar plugin"%(self.ToolbarName)

