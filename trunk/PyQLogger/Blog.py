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
__revision__ = "$Id:  $"

from Post import Post
from EaseXML import XMLObject, ListNode, \
                    StringAttribute, ItemNode

class Drafts(XMLObject):
    Data = ListNode('Post', main=True)
    
class Posts(XMLObject):
    Data = ListNode('Post', main=True)

class Blog(XMLObject):
    """
    Base class for Blogs.
    """

    Url = StringAttribute(optional=True) #Url used for preview
    Name = StringAttribute() #Visible blog's name
    ID = StringAttribute() #Internal blog id
    Posts = ItemNode('Posts') #List of posts in the blog
    Drafts = ItemNode('Drafts') #List of drafts in the blog
    def __postById(self, postNr):
        for post in Posts.Data:
            if post.ID == postNr:
                return post
        raise Exception("Invalid post number %s !"%postNr)
    

    def delete(self, postNr):
        """  remove post  """
        pass
    
    def editPost(self, post ):
        """   change post's content     """
        self.Service.editPost ( self.ID, post )
    
    def createPost(self, title, content, **other):
        """  create new post    """
        post = self.Service.newPost ( self.ID , title, content, None, other)
        self.Posts.Data += [ post ]
    
    def reloadPosts(self):
        """   fetch the list of posts in a blog   """
        posts = self.Service.getPosts(self.ID)
        for post in posts:
            here = [ bb for bb in self.Posts.Data if bb.ID == post.ID ]
            if not here: # it's new! add it
                self.Posts.Data += [ post ]
    
    def __len__(self):
        """   return the amount of posts in a blog     """
        return len(self.Posts.Data)
    
    def __getitem__(self, postNr):
        """    return a post by it's id     """
        return self.__postById(postNr)
    
    
    
