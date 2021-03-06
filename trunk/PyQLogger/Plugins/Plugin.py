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

from EaseXML import XMLObject, ItemNode, TextNode, RawNode, \
                                        ListNode,IntegerAttribute
import pickle

class Option(XMLObject):
    Type = TextNode() # one of : 'Integer','String','Boolean','List', 'DoubleList'
    Name = TextNode()
    Value = RawNode(default='',optional=True)
    def getListOptionValue(self):
        tmp = self.Value.split(';')
        if len(tmp) > 2:
            sel = int(tmp[0])
            return tmp[1:][sel]
        
    def getDoubleListOptionValue(self):
        if self.Value:
            hash = pickle.loads( str(self.Value) )
        else:
            hash = {}
        return hash

class PluginData(XMLObject):
    # Indication of plugin's status (0 - disable, 1 - enable)
    Enabled = IntegerAttribute(default=0)
    Options = ListNode('Option')
    Class = TextNode()

    def optionByName(self, name):
        for o in self.Options:
            if o.Name == name:
                return o
            
        
class Plugin:
    """
    Base class for all plugins
    """
    # Visible name. Will be used as tooltip, as menu caption or as item in config dialog.    
    Name = None
    # Who's responsible for this???
    Author = None
    # Byte array of the icon. (used in menu and toolbar)
    Icon = None
    # Additional information
    Info = None
    # This should be an instance of PluginData type
    Data = None
    
    def description(self):
        return "Unkown plugin type"

    def defaultOptions(self):
        return []
    
    
class InternalPlugin (Plugin):
    """ Subclass to mark the plugin as internal (invisible to settings) """
    def description(self):
        return "Internal plugin"
