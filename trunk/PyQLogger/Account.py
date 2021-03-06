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

#from BloggerService import *
from EaseXML import XMLObject, TextNode, IntegerAttribute, ListNode,\
                    StringAttribute
from Blog import Blog
from Services import *
from Services import BlogServices
__revision__ = "$Id$"

class Account(XMLObject):
    """
    Base class for blog account providers
    """        
    Name = StringAttribute() # Display name    
    Username = TextNode() #  Login name
    Password = TextNode(optional=True) # Top Secret!
    Host = TextNode() # Account's host
    SelectedBlog = IntegerAttribute(default=0) # id of currently selected blog
    Service = StringAttribute() #What Blogging API Is used
    Blogs = ListNode('Blog')
    
    def serviceByName(self, name):
        assert  name , "Name cannot be empty"
        for b in BlogServices:            
            (s_module, s_class) = b.split('.')
            if name == s_class:
                return getattr(globals()[s_module], s_class)
        raise Exception("Invalid Blog Service name : "+name)
        
    def blogByName(self, name):
        """ searches the list of accouns, and returns one by it's .Name """
        assert  name , "Name cannot be empty"
        for a in self.Blogs:
            if a.Name == name:
                return a
        raise Exception("Invalid Blog name: "+name)

  
    def blogById(self, blogId):
        assert  blogId , "Id cannot be empty"
        cnt = 0
        for blog in self.Blogs:
            if blog.ID == blogId:
                return cnt
            cnt += 1
        raise Exception("Invalid blog number %s !"%blogId)

    def init(self):
        if not hasattr(self,"inited"):
            svc = self.serviceByName(self.Service)
            self.BlogService = svc(self.Host, self.Username, self.Password)
            for blog in self.Blogs: 
                blog.Service = self.BlogService
        self.inited = True

    def login(self):
        """
        Perform login to server (if needed)
        """
        if hasattr(self.BlogService,'login'):
            return self.BlogService.login()
        return True
    
    
    def fetchBlogs(self):
        """
        get the list of blogs for this account
        """
        blogs = self.BlogService.getBlogs() # fetch blogs from server        
        for blog in blogs:
            here = [ bb for bb in self.Blogs if bb.Name == blog.Name ]
            if not here :
                self.Blogs += [ blog ]
    
    def __len__(self):
        """
        Return number of blogs in account
        """
        return len(self.Blogs)
    
    def __getitem__(self, blogId):
        """
        Get a blog in account by it's id
        """
        return self.Blogs [ self.blogById(blogId) ]
