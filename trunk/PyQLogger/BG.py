## This file is part of PyQLogger.
## 
## Copyright (c) 2004 Eli Yukelzon a.k.a Reflog &
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

__revision__ = "$Id$"

""" Background workers """
from qt import QTimer, SIGNAL, QListBoxText, QThread, \
               QObject, QString
from datetime import date
from distutils.version import LooseVersion
import sys, urllib2

###########  Fetch Blogs ###################

def doneFetchingBlogs(self, res):
    if not res:
        self.comboBlogs.clear()
        for blog in self.account.Blogs:            
            self.comboBlogs.insertItem(blog.Name)
        self.comboBlogs.setCurrentItem( self.account.SelectedBlog )
        self.notifier.info("%d Blogs fetched!" % len(self.account))        
    else:
        self.notifier.error(res)
    self.btnRefreshBlogs.setEnabled(True)
    
def startFetchingBlogs(self):
    self.btnRefreshBlogs.setEnabled(False)
    try:
        self.account.fetchBlogs()
    except Exception, e:
        return str(e)


###########  Fetch Posts ###################
            
def startFetchingPosts(self):
    self.btnFetchPosts.setEnabled(False)
    try:
        self.account.Blogs[self.account.SelectedBlog].reloadPosts()
    except Exception, e:
        return str(e)

def doneFetchingPosts(self, res):
    if not res:
        self.populateLists()
        blogs = self.account.Blogs[self.account.SelectedBlog]
        self.notifier.info("%d posts fetched!" % len( blogs ))
        self.SaveAll()
    else:
        self.notifier.error(res)
    self.btnFetchPosts.setEnabled(True)


###########  Publish Post ###################

def donePublishPost(self, res):
    if not res:
        blog = self.account.Blogs [ self.account.SelectedBlog ]
        post = blog.Posts.Data [ len(blog) - 1 ] # get last added one
        i = QListBoxText(post.Title)
        self.listPublishedPosts.insertItem(i,0)
        self.PublishedItems [ i ] = post
        self.current_post = None
        self.editPostTitle.setText("")
        self.sourceEditor.setText("")
        self.notifier.info("Publishing success!")
    else:
        self.notifier.error(res)
    self.btnPublish.setEnabled(True)
    
def startPublishPost(self):        
    self.btnPublish.setEnabled(False)
    try:
        title = unicode(self.editPostTitle.text())
        content = unicode(self.sourceEditor.text())
        self.account.Blogs[self.account.SelectedBlog].createPost(title, content)
    except Exception, e:
        import traceback
        traceback.print_exc()
        return str(e)
        
###########  Edit Post ###################

def startEditPost(self):
    self.btnPublish.setEnabled(False)
    try:
        self.current_post.Title = unicode(self.editPostTitle.text())
        self.current_post.Content = unicode(self.sourceEditor.text())
        self.account.Blogs[self.account.SelectedBlog].editPost(self.current_post)
    except Exception, e:
        return str(e)

def doneEditPost(self, res):
    if not res:
        self.editPostTitle.setText("")
        self.sourceEditor.setText("")
        for (item, post) in self.PublishedItems.items():
            if post == self.current_post:
                item.setText(post.Title)
                self.listPublishedPosts.triggerUpdate(False)
        self.notifier.info("Publishing success!")
        self.current_post = None
    else:
        self.notifier.error(res)
    self.btnPublish.setEnabled(True)
