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

from EaseXML import XMLObject,ItemNode,TextNode,RawNode,ListNode,IntegerAttribute
from OptionStorage import OptionStorage,Option
from qt import QPixmap

class Plugin(XMLObject):
  """
  Base class for all plugins
  """
  # Visible name. Will be used as tooltip, as menu caption or as item in config dialog.    
  Name = None
  # Who's responsible for this???
  Author = None
  # Option storage class instance    
  Options = ListNode('Option') 
  # Byte array of the icon. (used in menu and toolbar)
  Icon = None
  # Indication of plugin's status (0 - disable, 1 - enable)
  Enabled = IntegerAttribute(default=0)
  
  def description(self):
    return "Unkown plugin type"
  