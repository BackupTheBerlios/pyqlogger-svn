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


from EaseXML import XMLObject,ItemNode,TextNode,RawNode,ChoiceNode

class Option(XMLObject):
  Type = ChoiceNode(['Integer','String','List'])
  Name = TextNode()
  Value = TextNode(default='',optional=True)

class OptionStorage:
  """  Class for getting/setting/loading/saving and displaying plugin's settings  """

  def __init__(self):
    pass

  def __getitem__(self, param):
    """    return specific item    """
    pass

  def __setitem__(self, param, value):
    """    set specific item    """
    pass

  def load(self, xml):
    """    load options from xml string    """
    pass

  def save(self):
    """    save options to xml    """
    pass

  def createFrame(self):
    """    Creates a QFrame with all fields and controls for options    """
    pass

  def update(self):
    """    Syncronize the content from the Frame to local settings storage    """
    pass



