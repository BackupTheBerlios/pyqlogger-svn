## $Id$
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

""" Background workers """
from qt import *
from threading import *
from datetime import date
from time import sleep
from distutils.version import LooseVersion
import sys,urllib2,re
import sys

class BackGround:
    """ class that provides a timer that checks on background processes,
    and method for adding new background workers. all workers should provide following methods:
    ui(),bg() """
    def __init__(self):
        self.workers = {}
        self.checkTimer = QTimer()
        self.checkTimer.connect(self.checkTimer, SIGNAL("timeout()"), self.check)
        self.checkTimer.start(500)
    
    def check(self):
        for worker in self.workers.keys():
            if not self.workers[worker].THREAD.isAlive():
                self.workers[worker].ui()
                if self.workers[worker].SENDER: 
                    self.workers[worker].SENDER.setEnabled(True)
                del self.workers[worker]
            else:
                self.workers[worker].status()

    def add(self,worker,sender=None):
        if self.workers.has_key(str(worker)): # only add unique workers!
            return False
        worker.THREAD = Thread(args=[worker],target=worker.bg)
        worker.THREAD.start()
        if sender:
            sender.setEnabled(False)            
        worker.SENDER = sender
        self.workers[str(worker)] = worker
        return True
    

class bgWorker:
    def __init__(self,atomBlog,notifier,parent,statusmsg=None):
        self.notifier = notifier
        self.parent = parent
        self.atomBlog = atomBlog
        self.result = None
        self.statusmsg = statusmsg

    def status(self):
        if self.statusmsg:
            self.notifier.status(self.statusmsg)

class blogFetchWorker(bgWorker):
    """ class for fetching list of blogs in background """

    def bg(self,*args):
        p = self.parent
        blogs = None
        try:
            blogs = self.atomBlog.getBlogs()
            self.result = len(blogs)
            p.settings.addblogs(blogs)
        except Exception, inst:
            self.result = None
        
    def ui(self):
        p = self.parent
        if self.result:
            p.comboBlogs.clear()
            for blogid in p.settings.get("main", "blogs").split(';'):
                blogname = p.settings.getblogName(blogid)
                p.comboBlogs.insertItem(unicode(blogname))
            selectedblogid = p.settings.get("main", "selectedblog")
            selectedblogname = p.settings.getblogName(selectedblogid)
            for counter in range(0, p.comboBlogs.count()):
                if p.comboBlogs.text(counter) == selectedblogname:
                    p.comboBlogs.setCurrentItem( counter )
                    break
            self.notifier.info("%d Blogs fetched!"%(self.result))
        else:
            self.notifier.error("Couldn't fetch blogs!")



class postFetchWorker(bgWorker):
    """ class for fetching list of posts in background """
    def bg(self,*args):
        p = self.parent
        try:
            blogid = p.settings.get("main", "selectedblog")
            #blogid = self.parent.settings["blogs"][self.parent.settings["selectedblog"]]['id']
            self.PublishedPosts = self.atomBlog.getPosts(blogid)
        except:
            self.result = 666

    def ui(self):
        p = self.parent
        if not self.result:
            p.PublishedItems = {}
            p.PublishedPosts[p.settings.get("main", "selectedblog")] = self.PublishedPosts
            p.populateLists()
            self.notifier.info("%d posts fetched!"%(len(self.PublishedPosts)))
            self.parent.SaveAll()
        else:
            self.notifier.error("Couldn't fetch posts from blog!")


class postDeleteWorker(bgWorker):
    """ class for deleting current post in background """
    def bg(self,*args):
        p = self.parent
        try:
            post = p.PublishedItems [ p.listPublishedPosts.selectedItem () ]
            del p.PublishedItems [ p.listPublishedPosts.selectedItem () ]
            blogid = p.settings.get("main", "selectedblog")
            self.atomBlog.deletePost(blogid, post["id"])
            p.PublishedPosts[p.settings.get("main", "selectedblog")].remove(post)
        except:
            self.result = sys.exc_info()[0].__doc__

        
    def ui(self):
        p = self.parent
        if not self.result:
            i = p.listPublishedPosts.currentItem()
            p.listPublishedPosts.removeItem(i)
            self.notifier.info("Post deleted!")
        else:
            self.notifier.error("Couldn't fetch posts from blog! Error:"+self.result)

class newPostWorker(bgWorker):
    """ class for posting new blog item (or reposting) in background """
    def bg(self,*args):
        p = self.parent
        self.item_to_update = None
        self.result = False
        blogId = p.settings.get("main", "selectedblog")
        title = unicode(p.editPostTitle.text())
        content = unicode(p.sourceEditor.text())
        # are we editing?
        if p.current_post and p.current_post.has_key('id'): #yes!
            #yes, edit it
            try:
                self.atomBlog.editPost(blogId,p.current_post['id'], title,content)
                self.result = True
                idx = p.PublishedPosts[p.settings.get("main", "selectedblog")].index(p.current_post)
                p.PublishedPosts[p.settings.get("main", "selectedblog")][idx]['date'] = date.today()
                p.PublishedPosts[p.settings.get("main", "selectedblog")][idx]["title"] = title
                p.PublishedPosts[p.settings.get("main", "selectedblog")][idx]["content"] = content
                self.item_to_update = p.PublishedPosts[p.settings.get("main", "selectedblog")][idx] 
            except:
                self.result = False
                    
        else: #no, we are creating
            try:
                idx = self.atomBlog.newPost(int(blogId),title,content)
                if idx:
                    self.result = True
                    item = {
                        "id":idx,
                        "date":date.today(),
                        "title":title,
                        "content":content,
                        }
                    i = QListBoxText(p.listPublishedPosts,title)
                    p.PublishedPosts[p.settings.get("main", "selectedblog")] += [ item ]
                    p.PublishedItems [ i ] = item
            except Exception, inst:
                self.result = False

    def ui(self):
        if self.result:
            self.parent.current_post = None
            self.parent.editPostTitle.setText("")
            self.parent.sourceEditor.setText("")
            if self.item_to_update:
                for (k,v) in self.parent.PublishedItems.items():
                    if v == self.item_to_update:
                        k.setText(v['title'])
                        self.parent.listPublishedPosts.updateItem(k)
            self.notifier.info("Publishing success!")
        else:
            self.notifier.error("Couldn't post to blog!")

class updateCheckWorker:
    """ class that provides new version checking in background """
    def __init__(self,notifier):
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
