## This file is part of PyQLogger.
## 
## Copyright (c) 2005 Eli Yukelzon a.k.a Reflog &
##                    Xander Soldaat a.k.a. Mightor       
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
import sys
from EaseXML import  XMLObject, ListNode, IntegerAttribute, StringAttribute
from Qt import QDialog

class ConfigOption(XMLObject):
    name = StringAttribute(optional=False)
    label = StringAttribute(optional=False)
    type = StringAttribute(optional=False)
    value = StringAttribute(optional=True)
    items = ListNode('ListItem', optional=True)

class ListItem(XMLObject):
    value = StringAttribute(optional=False)

class ConfigList(XMLObject):
    _entities = [ ('&xml;','eXtensible Markup Language')]
    options = ListNode('ConfigOption')

class OptionForm(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

class OptionStorage:
    def __init__(self):
        __configlist__ = ConfigList()

    def __getitem__(self, value):
        pass

    def __setitem__(self, value):
        pass

    def load(self, file):
        pass

    def save(self):
        pass

    def createFrame(self):
        pass

    def update(self):
        pass

    def __str__(self):
        return __configlist__.toXml()
