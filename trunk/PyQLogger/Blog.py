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

from Post import Post
from EaseXML import  XMLObject,TextNode,ListNode,StringAttribute

class Blog(XMLObject):
    """
    Base class for Blogs.
    """

    Url = TextNode(optional=True) #Url used for preview
    Name = StringAttribute() #Visible blog's name
    ID = StringAttribute() #Internal blog id
    Posts = ListNode('Post') #List of posts in the blog
    Drafts = ListNode('Post') #List of posts in the blog
    def __postById(self,postNr):
        for post in Posts:
            if post.ID == postNr:
                return post
        raise Exception("Invalid post number %s !"%postNr)
    

    def delete(self, postNr):
        """  remove post  """
        pass
    
    def updatePost(self, postNr, title, content, **other):
        """   change post's content     """
        pass
    
    def createPost(self, title, content, **other):
        """  create new post    """
        pass
    
    def reloadPosts(self):
        """   fetch the list of posts in a blog   """
        self.Posts = self.Service.getPosts(self.ID)
    
    def __len__(self):
        """   return the amount of posts in a blog     """
        return len(self.Posts)
    
    def __getitem__(self, postNr):
        """    return a post by it's id     """
        return self.__postById(postNr)
    
    
    
