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

from BlogService import BlogService


import xmlrpclib,re,time
from PyQLogger.Post import Post
from PyQLogger.Blog import Blog,Posts,Drafts

class MetablogService (BlogService):
    APIKEY = ''
    name = "MetaWeblog Provider"
    
    def __init__(self,host,username,password):
        BlogService.__init__(self,host,username,password)        
        self.postre = re.compile('<title>(.*)</title><category>(.*)</category>(.*)',re.S)
        
    def login():
        try:
            server = xmlrpclib.Server(host)
        except:
            return False
        return True
    
    def getEmpty():
        return MetablogService("","","")
    getEmpty = staticmethod(getEmpty)
    
    def getBlogs(self):
        """        
        Returns information on all the blogs a given user is a member of.
        """
        bl=self.server.blogger.getUsersBlogs (APIKEY,self.username,self.password)
        ret = []
        for blog in bl:
            ret += Blog(ID=blog['blogid'],
                        Name=blog['blogName'],
                        Url=blog['url'],
                        Posts=Posts(),
                        Drafts=Drafts()
                        )
        return ret
    
    def getPosts(self, blogId):
        """ Returns a list of the most recent posts in the system. """
        #todo: check for 'authorName'
        try:
            res = self.server.metaWeblog.getRecentPosts(str(blogId),self.username,self.password,15)  
        except: # fallback
            res = self.server.blogger.getRecentPosts(APIKEY,str(blogId),self.username,self.password,15)  
        ret = []
        for post in res:
            content = post['content']
            m = self.postre.match(content)
            if m:
                title = m.group(1)
                cat = m.group(2)
                content = m.group(3)
            else:
                title = ""
            updated = time.strftime('%Y-%m-%dT%H:%M:%SZ',  time.strptime(str(post['dateCreated']),'%Y%m%dT%H:%M:%S'))
            ret += Post(ID=post['postid'], Content=content, Title=title, Created=updated)
        return ret


    def getCategories(self, blogId):
        """ Method: metaWeblog.getCategories
            Method: blogger.getCategories(blogid,username,password)
            Returns a list of the categories that you can use to log against a post.
        """
        return []
    
    def editPost (self, blogId, post ):
        self.server.blogger.editPost(self.APIKEY, post.ID, self.username, self.password,
                                 post.Content, True)
        self.server.metaWeblog.editPost(post.ID, self.username, self.password,
                                 post.Content, True)

    def newPost(self, blogId, title, content, date=None,other=None):       
        self.server.blogger.newPost(self.APIKEY, blogId, self.username,self.password, content, True)
        self.server.metaWeblog.newPost(blogId, self.username,self.password, content, True)

    def deletePost(self, blogId, entryId):
        """Deletes a post."""
        try:
            res = blogger.deletePost(APIKEY,str(entryId),self.username,self.password, True)
            return res == '1'
        except:
            #todo, handle: Fault 807: 'No such post.'
            pass
        return False
