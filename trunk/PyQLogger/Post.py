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

from EaseXML import  XMLObject, TextNode, RawNode, ItemNode
__revision__ = "$Id:  $"

class PostData(XMLObject):
    Pickle  = RawNode(main=True)
    
class Post(XMLObject):
    """
    Basic class for post in a blog
    """
    
    ID = TextNode(optional=True)#post's id (optional because we use it for drafts aswell)
    Title = TextNode()#post's title
    Content = RawNode()#body of the post
    Created = TextNode()#date of post's publication (or last update)
    Data = ItemNode('PostData', optional=True)
    
    def __str__(self):
        """
        return string representation of the post
        """
        return "ID: %s\nTitle: %s\nDate: %s\nBody:\n%s" % \
               (self.ID, self.Title, self.Created, self.Content)


