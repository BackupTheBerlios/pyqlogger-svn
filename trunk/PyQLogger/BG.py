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
               QObject, QString, QMutex
from datetime import date
from distutils.version import LooseVersion
import sys, urllib2
from PyQLogger.Plugins.EventPlugin import EventType
from PyQLogger.Network import OpCompleteEvent

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
    self.FetchBlogsAction.setEnabled(True)
    self.blogsmutex.unlock()
    
def startFetchingBlogs(self):
    self.blogsmutex.lock()
    try:
        self.account.fetchBlogs()
    except Exception, e:
        return str(e)


###########  Fetch Posts ###################
            
def startFetchingPosts(self):    
    self.postsmutex.lock()
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
    self.FetchPostsAction.setEnabled(True)
    self.postsmutex.unlock()


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
        self.prepareCrossBlog()
        self.manager.handleEvent(EventType.AFTERPUBLISH, None)        
    else:
        self.notifier.error(res)
    self.btnPublish.setEnabled(True)
    self.postsmutex.unlock()
    
def startPublishPost(self):            
    self.postsmutex.lock()
    try:
        title = unicode(self.editPostTitle.text())
        content = unicode(self.sourceEditor.text())
        for blog in self.getCrossBlogList():
            blog.createPost(title, content)
    except Exception, e:
        import traceback
        traceback.print_exc()
        return str(e)
        
###########  Edit Post ###################

def startEditPost(self):    
    self.postsmutex.lock()
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
    self.postsmutex.unlock()

###########  Speller ###################
class SpellThread(QThread):
    def __init__(self,parent):
        self.parent = parent
        self.mutex = QMutex()
        QThread.__init__(self)
                
    def run(self):
        self.mutex.lock()
        scin = self.parent.sourceEditor
        text = unicode ( scin.text() )
        if text :
            self.parent.speller_result = self.parent.speller.load( unicode ( text ) )
        else:
            self.parent.speller_result = {}
        self.postEvent(self.parent, OpCompleteEvent(doneSpell,self.parent))
        self.mutex.unlock()
    
def doneSpell(self, data=None):
    scin = self.sourceEditor
    text = unicode ( scin.text() )
    # clear indicators
    scin.SendScintilla(scin.SCI_STARTSTYLING, 0, scin.INDIC2_MASK)
    scin.SendScintilla(scin.SCI_SETSTYLING , len(text), 0)
    # set indicator to squigly
    scin.SendScintilla(scin.SCI_INDICSETSTYLE,2,scin.INDIC_SQUIGGLE)
    scin.SendScintilla(scin.SCI_INDICSETFORE,2,0x00ffff)
    
    for result in self.speller_result.keys():
        scin.SendScintilla(scin.SCI_STARTSTYLING,result.start(), scin.INDIC2_MASK)
        scin.SendScintilla(scin.SCI_SETSTYLING,result.end()-result.start(), scin.INDIC2_MASK)

