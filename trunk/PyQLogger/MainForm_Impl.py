## $Id$
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
# -*- coding: utf-8 -*-

import sys, os, pickle, webbrowser, KdeQt
from qt import *
from mainform import MainForm
from SetupWizardForm_Impl import SetupWizardForm_Impl
from datetime import date
from AtomBlog import *
from ToolBar import *
from Notifier import Notifier
from SyntaxHighlight import HTMLSyntax
from BG import *
from ToolBarManager import *
import PyQLoggerConfig

class MainForm_Impl(MainForm):

    def __init__(self,parent = None,name = None,fl = 0):
        MainForm.__init__(self,parent,name,fl)
        notifymode = 0
        if len(sys.argv) > 1 and sys.argv[1] == '-s':
            notifymode = 1
        self.settings = PyQLoggerConfig.PyQLoggerConfig()
        self.statusFrame.hide()
        self.sh = HTMLSyntax(self.sourceEditor)
        self.sourceEditor.setTextFormat(Qt.PlainText)
        KdeQt.setPreviewWidget(self)
        KdeQt.setEditWidget(self)

        self.current_post = None
        self.cached_password = None
        self.cached_atomblog = None
        self.plugins = PluginFactory(self)
        tabLayout = QHBoxLayout(self.tab,11,6,"tabLayout")
        tabLayout.setAutoAdd( True )
        tabLayout2 = QHBoxLayout(self.tab_2,11,6,"tabLayout2")
        tabLayout2.setAutoAdd( True )
        initToolbar(self,self.plugins)
        self.notifier = Notifier(self,notifymode)
        self.bg = BackGround()
        self.workers = BackGround()
        self.uChecker = updateCheckWorker(self.notifier)
        self.aMenu = QPopupMenu()
        self.aMenu.insertItem("Delete post",1)
        self.aMenu.insertItem("Export post",2)
        self.bMenu = QPopupMenu()
        self.bMenu.insertItem("Delete post",1)
        self.bMenu.insertItem("Export post",2)
        self.connect(self.aMenu,SIGNAL("activated(int)"),self.pubPopup)
        self.connect(self.bMenu,SIGNAL("activated(int)"),self.savePopup)
        self.frameCat.hide()
        
    def getPage(self,title):
        if not title: 
            return self.tabWidget3.page(0)
        for i in range(0,self.tabWidget3.count()):
            if title == str(self.tabWidget3.label(i)):
                return self.tabWidget3.page(i)


    def pubPopup(self,i):
        if(i == 1):
            res = QMessageBox.question(self,"Question","Are you sure you want to delete this post?",QMessageBox.Yes,QMessageBox.No)
            if res == QMessageBox.Yes:
                ab = self._getAtomBlog()
                b = postDeleteWorker(ab,self.notifier,self,"Deleting post...")
                self.workers.add(b) 
        elif(i == 2):
            s = QFileDialog.getSaveFileName(os.path.expanduser("~"),
                                        "All files (*.*)",self,           
                                        "Export post dialog",
                                        "Choose a filename to save under")
            if str(s):
                try:
                    file = open(str(s),"w")
                    post = self.PublishedItems[ self.listPublishedPosts.selectedItem () ]
                    file.write(post['content'])
                    file.close()
                except:
                    QMessageBox.warning(self,"Warning","Cannot write post to file!")

    def savePopup(self,i):
        if(i == 1):
            res = QMessageBox.question(self,"Question","Are you sure you want to delete this post?",QMessageBox.Yes,QMessageBox.No)
            if res == QMessageBox.Yes:
                post = self.SavedItems [ self.listSavedPosts.selectedItem () ]
                del self.SavedItems [ self.listSavedPosts.selectedItem () ]
                blogid = self.settings.get("main", "selectedblog")
                self.SavedPosts[blogid].remove(post)
                self.listSavedPosts.removeItem(self.listSavedPosts.currentItem())
        elif(i == 2):
            s = QFileDialog.getSaveFileName(os.path.expanduser("~"),
                                        "All files (*.*)",self,           
                                        "Export post dialog",
                                        "Choose a filename to save under")
            if str(s):
                try:
                    file = open(str(s),"w")
                    post = self.SavedItems [ self.listSavedPosts.selectedItem () ]
                    file.write(post['content'])
                    file.close()
                except:
                    QMessageBox.warning(self,"Warning","Cannot write post to file!")
                
    def listPublishedPosts_contextMenuRequested(self,a0,a1):
        self.aMenu.setItemEnabled(1,a0 != None)
        self.aMenu.setItemEnabled(2,a0 != None)
        self.aMenu.popup(a1)
    
    def listSavedPosts_contextMenuRequested(self,a0,a1):
        self.bMenu.setItemEnabled(1,a0 != None)
        self.bMenu.setItemEnabled(2,a0 != None)
        self.bMenu.popup(a1)

    def sourceEditor_textChanged(self):
        KdeQt.setPreview(self,self.sourceEditor.text())
    
    def btnNewPost_clicked(self):
        if self.current_post:
            res = QMessageBox.question(self,"Question","Current post is unsaved. Are you sure you want to erase it?",QMessageBox.Yes,QMessageBox.No)
            if res == QMessageBox.No:
                return
        self.editPostTitle.setText("")
        self.sourceEditor.setText("")
        self.current_post = None
        
    def btnExit_clicked(self):
        if self.current_post:
            res = QMessageBox.question(self,"Question","Current post is unsaved. Are you sure you want to exit?",QMessageBox.Yes,QMessageBox.No)
            if res == QMessageBox.No:
                return
        self.SaveAll()
        qApp.closeAllWindows()

    
    def btnPublish_clicked(self):       
        title = unicode(self.editPostTitle.text())
        if title:
            ab = self._getAtomBlog()
            b = newPostWorker(ab,self.notifier,self,"Posting to blog...")
            self.workers.add(b,self.sender())
        else:
            QMessageBox.warning(self,"Warning","You forgot the post's title!")
    
    def btnSavePost_clicked(self):
        title = unicode(self.editPostTitle.text())
        if title:
            i = QListBoxText(self.listSavedPosts,title)
            item = { 
                "date":date.today(),
                "title":title,
                "content":unicode(self.sourceEditor.text()),
                }   
            blogid = self.settings.get("main", "selectedblog")
            self.SavedPosts[blogid] += [ item ]
            self.SavedItems [ i ] = item
        else:
            QMessageBox.warning(self,"Warning","You forgot the post's title!")

    
    def btnRefreshBlogs_clicked(self):      
        at = self._getAtomBlog()
        if at:
            b = blogFetchWorker(at,self.notifier,self,"Fetching list of blogs...")
            self.workers.add(b,self.sender())
    
    def btnSettings_clicked(self):
        wiz = SetupWizardForm_Impl(self)
        wiz.initValues(self.settings)
        res = wiz.exec_loop()
        if res:
            self.settings = wiz.settings
            try:
                fd = open(os.path.expanduser("~/.pyqlogger/settings.ini"), "w")
                self.settings.write(fd)
                fd.close()
                self.init()
            except Exception, inst: 
                print "btnSettings_clicked: %s" % inst
                QMessageBox.critical(self,"Error","Cannot write configuration!")
                QApplication.exit()
    
    def btnPreview_clicked(self):
        url = self.settings.get("main", "url")
        webbrowser.open_new(url)
    
    def btnReloadFeed_clicked(self):
        at = self._getAtomBlog()
        if at:
            b = postFetchWorker(at,self.notifier,self,"Fetching posts...")
            self.workers.add(b,self.sender())
    
    def comboBlogs_activated(self,a0):
        blogid = self.settings.getblogID(a0)
        self.settings.set("main", "selectedblog", blogid)
        self.populateLists()
    
    def listPublishedPosts_doubleClicked(self,a0):
        if self.PublishedItems.has_key(a0):
            d = self.PublishedItems[a0]
            self.current_post = d
            self.editPostTitle.setText(d["title"])
            self.sourceEditor.setText(d["content"])
            self.sender().setFocus()
        else:
            QMessageBox.critical(self,"Error","Something is not right!")
    
    def listSavedPosts_doubleClicked(self,a0):
        if self.SavedItems.has_key(a0):
            d = self.SavedItems[a0]
            self.editPostTitle.setText(d["title"])
            self.sourceEditor.setText(d["content"])
            self.sender().setFocus()
        else:
            QMessageBox.critical(self,"Error","Something is not right!")


    def WriteSettings(self,filename,hash):
        """ pickles the current settings hash to specified file """
        if not os.path.exists(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        if not hash.has_key("newstyle"):
            hash["newstyle"] = 1
        f =  open(filename, 'w')
        pickle.dump(hash, f)
        f.close()
        
    def ReadSettings(self,filename):
        """ unpickles the specified file into a hash """
        h = ()
        try:
            if os.path.exists(filename):
                f = open(filename)
                h = pickle.load(f)
                f.close()
            else:
                return None
        except Exception, inst:
            print "ReadSettings: %s" % inst
            return None
            
        if not h.has_key("newstyle"):
            new_hash = {}
            for blogid in self.settings.get("main", "blogs").split(';'):
                blogname = self.settings.get(blogid, "name")
                if h.has_key(blogname):
                    new_hash[blogid] = h[blogname]
                    h[blogname] = None
            h = new_hash
            h["newstyle"] = 1
            self.WriteSettings(filename, h)
        return h

    def SaveAll(self):
        try:
            fd = open(os.path.expanduser("~/.pyqlogger/settings.ini"), "w")
            self.settings.write(fd)
            fd.close()
            self.WriteSettings(os.path.expanduser("~/.pyqlogger/drafts"),self.SavedPosts)
            self.WriteSettings(os.path.expanduser("~/.pyqlogger/posts"),self.PublishedPosts)
        except Exception, inst:
            print "SaveAll: %s" % inst
            QMessageBox.critical(self,"Error","Cannot write configuration!")

    def MainForm_destroyed(self,a0):
        self.SaveAll()
        
    def _getPassword(self):
        if not self.cached_password:
            if self.settings.has_option("main", "password"):
                self.cached_password = self.settings.get("main", "password")
                return self.cached_password
            else:
                (text,ok) = QInputDialog.getText("PyQLogger", "Enter your password:", QLineEdit.Password)
                if ok and  str(text) != "":
                    self.cached_password = str(text)
                    return str(text)
                else:
                    return None
        else:
            return self.cached_password

    def _getAtomBlog(self):
        if not self.cached_atomblog:
            psw = self._getPassword()
            host = self.settings.get("main", "host")
            login = self.settings.get("main", "login")
            if psw:
                self.cached_atomblog = None
                if self.settings.getint("main", "hosttype") == 0:
                    ep = self.settings.get("main", "ep")
                    fp = self.settings.get("main", "fp")
                    pp = self.settings.get("main", "pp")
                    self.cached_atomblog = GenericAtomClient(host, login, psw, ep, fp, pp)
                elif self.settings.getint("main", "hosttype") == 1:
                    self.cached_atomblog = BloggerClient(host, login, psw)
                elif self.settings.getint("main", "hosttype") == 2:
                    self.cached_atomblog = MovableTypeClient(host, login, psw)
                return self.cached_atomblog
            else:
                QMessageBox.warning(self,"Error","Cannot work online without a password!")

        else:
            return self.cached_atomblog
            
    def init(self):
        self.SavedPosts = ()
        self.PublishedPosts = ()
        
        if not os.path.exists(os.path.expanduser("~/.pyqlogger")):
            os.mkdir(os.path.expanduser("~/.pyqlogger"))

        self.settings.read(os.path.expanduser("~/.pyqlogger/settings.ini"))
        self.SavedPosts = self.ReadSettings(os.path.expanduser("~/.pyqlogger/drafts"))
        self.PublishedPosts = self.ReadSettings(os.path.expanduser("~/.pyqlogger/posts"))
        
        if not self.settings.has_section("main"):
            self.btnSettings_clicked()
            if not self.settings.has_section("main"):
                QMessageBox.critical(self,"Error","Cannot procede without configuration!")
                return False
        
        for blogid in self.settings.get("main", "blogs").split(';'):
            self.comboBlogs.insertItem(self.settings.get(blogid, "name"))
            
        selectedblogid = self.settings.get("main", "selectedblog")
        selectedblogname = self.settings.get(selectedblogid, "name")

        for counter in range(0, self.comboBlogs.count()):
            if self.comboBlogs.text(counter) == selectedblogname:
                self.comboBlogs.setCurrentItem( counter )
                break
        
        if self.settings.getint("main", "hosttype") != 1:
            self.frameCat.show()
        self.populateLists()
        
        self._getPassword()
        return True

    def populateLists(self):
        self.PublishedItems = {}
        self.SavedItems = {}
        self.listPublishedPosts.clear()
        self.listSavedPosts.clear()

        if self.SavedPosts != None and self.SavedPosts.has_key(self.settings.get("main", "selectedblog")):
            for post in self.SavedPosts[self.settings.get("main", "selectedblog")]:
                i = QListBoxText(self.listSavedPosts,post["title"])
                self.SavedItems [ i ] = post
        else:
            if self.SavedPosts == None:
                self.SavedPosts = {}
            self.SavedPosts[self.settings.get("main", "selectedblog")] = []

        if self.PublishedPosts != None and self.PublishedPosts.has_key(self.settings.get("main", "selectedblog")):
            for post in self.PublishedPosts[self.settings.get("main", "selectedblog")]:
                i = QListBoxText(self.listPublishedPosts,post["title"])
                self.PublishedItems [ i ] = post
        else:
            if self.PublishedPosts == None:
                self.PublishedPosts = {}
            self.PublishedPosts[self.settings.get("main", "selectedblog")] = []
