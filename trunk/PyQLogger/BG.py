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
from qt import QTimer, SIGNAL, QListBoxText,QThread,QObject,QString
from datetime import date
from distutils.version import LooseVersion
import sys, urllib2
from qtnetwork import QHttp

   
class bgOperation(QObject):
    def __init__(self,atomBlog,notifier,parent,sender=None):
        QObject.__init__(self,parent)
        self.notifier = notifier
        self.atomBlog = atomBlog
        self.control = sender
        if sender:
            self.control.setEnabled(False)        
        self.http = QHttp(self)
        self.connect(self.http, SIGNAL( "done(bool)" ), self.httpDone )
        self.connect(self.http, SIGNAL( "dataSendProgress (int, int)"),self.httpProgress)
        self.connect(self.http, SIGNAL( "dataReadProgress (int, int)"),self.httpProgress)
        self.connect(self.http, SIGNAL( "requestFinished (int, bool)"),self.httpRequestFinished)

    def httpRequestFinished ( self, id, error ):
        if error:
            self.notifier.error(self.errormsg)
            print "Error occured: " + self.http.errorString()
    
    def httpDone(self,error):
        result = unicode(QString(self.http.readAll()))
        if error:
            self.notifier.error(self.errormsg)
            print "Error occured: " + self.http.errorString()
        else:
            self.ui(result)
            if self.control:
                self.control.setEnabled(True)
        self.http.closeConnection()
        
    def httpProgress(self,completed,total):
        self.notifier.status(self.statusmsg)

    def begin(self):
        assert (self.req.isValid())
        self.http.setHost(self.atomBlog.host)
        if hasattr(self,"body"):
            self.http.request(self.req,self.body)
        else:
            self.http.request(self.req)
    
class BlogFetcher(bgOperation):
    """ class for fetching list of blogs in background """
    statusmsg =  "Fetching list of blogs..."    
    errormsg =  "Cannot fetch list of blogs!"
    
    def ui(self,result):
        blogs = self.atomBlog.endGetBlogs(result)
        parent = self.parent()
        selectedblog = parent.settings.get("main", "selectedblog")
        parent.settings.addblogs(blogs,selectedblog)
        parent.comboBlogs.clear()
        for blogid in parent.settings.get("main", "blogs").split(';'):
            blogname = parent.settings.getblogName(blogid)
            parent.comboBlogs.insertItem(unicode(blogname))
        selectedblogname = parent.settings.getblogName(selectedblog)
        for i in range(0, parent.comboBlogs.count()):
            if parent.comboBlogs.text(i) == selectedblogname:
                parent.comboBlogs.setCurrentItem( i )
                break
        self.notifier.info("%d Blogs fetched!" % len(blogs))
        
    def __call__(self):
        self.disconnect( self.http , SIGNAL( "dataSendProgress (int, int)") , self.httpProgress)
        self.req = self.atomBlog.startGetBlogs()
        self.begin()

class PostFetcher(bgOperation):
    """ class for fetching list of posts in background """
    errormsg = "Couldn't fetch posts from blog!"
    statusmsg = "Fetching posts..."
    def __call__(self):
            blogid = self.parent().settings.get("main", "selectedblog")
            self.disconnect( self.http , SIGNAL( "dataSendProgress (int, int)") , self.httpProgress)
            self.req = self.atomBlog.startGetPosts(blogid)
            self.begin()
    
    def ui(self,result):
        posts = self.atomBlog.endGetPosts(result)
        p = self.parent()
        p.PublishedItems = {}
        p.PublishedPosts[p.settings.get("main", "selectedblog")] = posts
        p.populateLists()
        self.notifier.info("%d posts fetched!" % len( posts ))
        p.SaveAll()


class PostEraser(bgOperation):
    """ class for deleting current post in background """
    errormsg = "Couldn't fetch posts from blog!"
    statusmsg = "Deleting post..."
    def __call__(self):
        p = self.parent()
        post = p.PublishedItems [ p.listPublishedPosts.selectedItem () ]
        blogid = p.settings.get("main", "selectedblog")
        self.disconnect( self.http , SIGNAL( "dataReadProgress (int, int)") , self.httpProgress)
        self.req = self.atomBlog.deletePost(blogid, post["id"])
        self.begin()
        
    def ui(self,result):
        p = self.parent()
        post = p.PublishedItems [ p.listPublishedPosts.selectedItem () ]
        del p.PublishedItems [ p.listPublishedPosts.selectedItem () ]
        p.PublishedPosts[p.settings.get("main", "selectedblog")].remove(post)
        i = p.listPublishedPosts.currentItem()
        p.listPublishedPosts.removeItem(i)
        self.notifier.info("Post deleted!")

class PostCreator(bgOperation):
    """ class for posting new blog item (or reposting) in background """
    statusmsg = "Posting to blog..."
    errormsg = "Couldn't post to blog..."
    
    def __call__(self):
        p = self.parent()
        blogId = p.settings.get("main", "selectedblog")
        title = unicode(p.editPostTitle.text())
        content = unicode(p.sourceEditor.text())
        (self.req,self.body) = self.atomBlog.startNewPost(int(blogId), title, content)
        self.begin()

    def ui(self,result):
        idx = self.atomBlog.endNewPost(result)
        if idx:
                item = {
                    "id":idx,
                    "date":date.today(),
                    "title":title,
                    "content":content,
                    }
                i = QListBoxText(p.listPublishedPosts, title)
                p.PublishedPosts[p.settings.get("main", "selectedblog")] += [ item ]
                p.PublishedItems [ i ] = item
                p.current_post = None
                p.editPostTitle.setText("")
                p.sourceEditor.setText("")
                self.notifier.info("Publishing success!")
        else:
                self.notifier.error("Couldn't parse server response!")

class PostEditor(bgOperation):
    """ class for posting new blog item (or reposting) in background """
    errormsg = "Couldn't post to blog!"
    statusmsg = "Posting update to blog..."
    def __call__(self):
        p = self.parent()
        blogId = p.settings.get("main", "selectedblog")
        title = unicode(p.editPostTitle.text())
        content = unicode(p.sourceEditor.text())
        self.req = self.atomBlog.editPost(blogId,p.current_post['id'], title,content)
        self.begin()

    def ui(self,result):
        p = self.parent()
        idx = p.PublishedPosts[p.settings.get("main", "selectedblog")].index(p.current_post)
        p.PublishedPosts[p.settings.get("main", "selectedblog")][idx]['date'] = date.today()
        p.PublishedPosts[p.settings.get("main", "selectedblog")][idx]["title"] = title
        p.PublishedPosts[p.settings.get("main", "selectedblog")][idx]["content"] = content
        item_to_update = p.PublishedPosts[p.settings.get("main", "selectedblog")][idx] 
        self.parent.current_post = None
        self.parent.editPostTitle.setText("")
        self.parent.sourceEditor.setText("")
        if item_to_update:
            for (k,v) in self.parent.PublishedItems.items():
                if v == item_to_update:
                    k.setText(v['title'])
                    self.parent.listPublishedPosts.updateItem(k)
            self.notifier.info("Publishing success!")
        else:
            self.notifier.error("Post id changed???")


class updateCheckWorker:
    """ class that provides new version checking in background """
    def __init__(self, notifier):
        from pyqlogger import VERSION
        self.notifier = notifier
        self.notified = LooseVersion(VERSION)
        self.Timer = QTimer()
        self.Timer.connect(self.Timer, SIGNAL("timeout()"), self.work)
        self.Timer.start(60*60*1000)    
        
    def work(self):
        try:
            req = urllib2.urlopen('http://pyqlogger.berlios.de/ver.php')
            line = req.readline()
            newver = LooseVersion( line.strip() )
            if newver > self.notified :
                self.notified = newver
                self.notifier.info("New version %s is available at the site!"%(str(newver)))
        except:
            pass
