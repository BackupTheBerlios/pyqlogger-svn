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

__revision__ = "$Id: MainForm_Impl.py 102 2005-01-11 13:37:12Z reflog $"

from qt import  QHBoxLayout, QPopupMenu, QMessageBox, QFileDialog, \
                          QApplication, QListBoxText, QLineEdit, QInputDialog, \
                          Qt, qApp, SIGNAL, QProgressBar,QDialog
import os, pickle, webbrowser
from PyQLogger.Settings import Settings
from datetime import date
#from AtomBlog import MovableTypeClient, BloggerClient, GenericAtomClient,LiveJournalClient
from PyQLogger.ToolBar import initToolbar
from PyQLogger.Notifier import Notifier
from PyQLogger.Post import Post
from PyQLogger.ToolBarManager import PluginFactory
from PyQLogger import BG, KdeQt

class MainDialog(QDialog):
    def getPage(self, title):
        if not title: 
            return self.toolbarTab.page(0)
        for i in range(0, self.toolbarTab.count()):
            if title == str(self.toolbarTab.label(i)):
                return self.toolbarTab.page(i)
        return None

    def editorTab_currentChanged(self, widget):
        if widget == self.Preview:
            KdeQt.setPreview(self, self.sourceEditor.text())

    def pubPopup(self, action):
        if(action == 1):
            res = QMessageBox.question(self, "Question", "Are you sure you want to delete this post?", QMessageBox.Yes, QMessageBox.No)
            if res == QMessageBox.Yes:
                aBlog = self.__getAtomBlog()
                BG.PostEraser(aBlog, self.notifier, self)()
        elif(action == 2):
            filename = QFileDialog.getSaveFileName(os.path.expanduser("~"),
                                        "All files (*.*)",self,           
                                        "Export post dialog",
                                        "Choose a filename to save under")
            if str(filename):
                try:
                    post = self.PublishedItems[ self.listPublishedPosts.selectedItem () ]
                    open(unicode(filename),"w").write(post['content'])
                except Exception, e:
                    print "Exception while saving to file: " + str(e)
                    QMessageBox.warning(self, "Warning", "Cannot write post to file %s" % filename)

    def savePopup(self, action):
        if(action == 1):
            res = QMessageBox.question(self, "Question", "Are you sure you want to delete this post?", QMessageBox.Yes, QMessageBox.No)
            if res == QMessageBox.Yes:
                post = self.SavedItems [ self.listSavedPosts.selectedItem () ]
                del self.SavedItems [ self.listSavedPosts.selectedItem () ]
                blogid = self.settings.get("main", "selectedblog")
                self.SavedPosts[blogid].remove(post)
                self.listSavedPosts.removeItem(self.listSavedPosts.currentItem())
        elif(action == 2):
            filename = QFileDialog.getSaveFileName(os.path.expanduser("~"),
                                        "All files (*.*)",self,           
                                        "Export post dialog",
                                        "Choose a filename to save under")
            if str(filename):
                try:
                    post = self.SavedItems [ self.listSavedPosts.selectedItem () ]
                    open(unicode(filename),"w").write(post['content'])
                except Exception, e:
                    print "Exception while saving to file: " + str(e)
                    QMessageBox.warning(self, "Warning", "Cannot write post to file %s!" % filename)
                
    def listPublishedPosts_contextMenuRequested(self, a0, a1):
        self.aMenu.setItemEnabled(1, a0 != None)
        self.aMenu.setItemEnabled(2, a0 != None)
        self.aMenu.popup(a1)
    
    def listSavedPosts_contextMenuRequested(self, a0, a1):
        self.bMenu.setItemEnabled(1, a0 != None)
        self.bMenu.setItemEnabled(2, a0 != None)
        self.bMenu.popup(a1)

    
    def btnNewPost_clicked(self):
        if self.current_post:
            res = QMessageBox.question(self, "Question", 
                                   "Current post is unsaved. Are you sure you want to erase it?",
                                   QMessageBox.Yes, QMessageBox.No)
            if res == QMessageBox.No:
                return
        self.editPostTitle.setText("")
        self.sourceEditor.setText("")
        self.current_post = None
        
    def accept(self):
        self.reload = True
        QDialog.accept(self)
        
    def reject(self):
        if self.current_post:
            res = QMessageBox.question(self, "Question", 
                                   "Current post is unsaved. Are you sure you want to exit?",
                                   QMessageBox.Yes, QMessageBox.No)
            if res == QMessageBox.No:
                return
        self.SaveAll()
        QDialog.reject(self)

    
    def btnPublish_clicked(self):       
        title = unicode(self.editPostTitle.text())
        content = unicode(self.sourceEditor.text())
        if content:
            if title:
                aBlog = self.__getAtomBlog()
                if self.current_post and self.current_post.has_key('id'):
                    bgWorker = BG.PostEditor(aBlog, self.notifier, self )
                else:
                    bgWorker = BG.PostCreator(aBlog, self.notifier, self )
                bgWorker()
            else:
                QMessageBox.warning(self, "Warning", "You forgot the post's title!")
        else:
            QMessageBox.warning(self, "Warning", "You cannot post an empty item!")
    
    def btnSavePost_clicked(self):
        title = unicode(self.editPostTitle.text())
        if title:
            listitem = QListBoxText(self.listSavedPosts, title)
            item = Post(Created=date.today(), Title=title,Content=unicode(self.sourceEditor.text()))                
            self.account.Blogs[self.account.SelectedBlog].Drafts += [ item ]
            self.SavedItems [ listitem ] = item
        else:
            QMessageBox.warning(self, "Warning", "You forgot the post's title!")

    
    def btnRefreshBlogs_clicked(self):      
        aBlog = self.__getAtomBlog()
        if aBlog:
            bg = BG.BlogFetcher(aBlog, self.notifier, self, self.sender())
            bg()
    
    def btnSettings_clicked(self):
        wnd = self.forms["Settings"]
        wnd["Impl"].init(self.settings)
        if wnd["Class"].exec_loop() == QDialog.Accepted:
            try:
                self.settings.save()
            except Exception, inst: 
                print "btnSettings_clicked: %s" % inst
                QMessageBox.critical(self, "Error", "Cannot write configuration!")
                QApplication.exit()
    
    def btnPreview_clicked(self):
        url = self.account.Blogs[self.account.SelectedBlog].Url
        if url:
            webbrowser.open_new(url)
        else:
            QMessageBox.warning(self, "Warning", "You don't have homepage configured!\nYou can do that in the Setup dialog.")
    
    def btnReloadFeed_clicked(self):
        aBlog = self.__getAtomBlog()
        if aBlog:
            bg = BG.PostFetcher(aBlog, self.notifier, self, self.sender())
            bg()
    
    def comboBlogs_activated(self, blogname):
        if blogname:
            self.account.SelectedBlog =  self.account.blogById(self.account.blogByName(blogname).ID)
            self.populateLists()
    
    def listPublishedPosts_doubleClicked(self, postitem):
        if self.PublishedItems.has_key(postitem):
            post = self.PublishedItems[postitem]
            self.current_post = post
            self.editPostTitle.setText(post.Ttitle)
            self.sourceEditor.setText(post.Content)
            self.editorTab.setCurrentPage(0)            
            self.sender().setFocus()
        else:
            QMessageBox.critical(self, "Error", "Something is not right!")
    
    def listSavedPosts_doubleClicked(self, item):
        if self.SavedItems.has_key(item):
            currentItem = self.SavedItems[item]
            self.editPostTitle.setText(currentItem.Title)
            self.sourceEditor.setText(currentItem.Content)
            self.editorTab.setCurrentPage(0)
            self.sender().setFocus()
        else:
            QMessageBox.critical(self, "Error", "Something is not right!")

    def sourceEditor_textChanged(self):
        """ this even should be connected to plugins """
        pass

    def SaveAll(self):
        try:
            self.settings.save()
        except Exception, inst:
            print "SaveAll: %s" % inst
            QMessageBox.critical(self, "Error", "Cannot write configuration!")
            
    def init_ui(self, settings):
        KdeQt.setPreviewWidget(self)
        KdeQt.setEditWidget(self)
        self.current_post = None
        self.cached_password = None
        self.cached_atomblog = None
        self.plugins = PluginFactory(self)
        tabLayout = QHBoxLayout(self.toolbarTab.page(0), 11, 6, "tabLayout")
        tabLayout.setAutoAdd( True )
        tabLayout2 = QHBoxLayout(self.toolbarTab.page(1), 11, 6, "tabLayout2")
        tabLayout2.setAutoAdd( True )
        initToolbar(self, self.plugins)
        self.notifier = Notifier(self, settings.UI_Settings.Notification)
        if self.notifier.mode != 1:
            self.statusFrame.hide()
        self.aMenu = QPopupMenu()
        self.aMenu.insertItem("Delete post", 1)
        self.aMenu.insertItem("Export post", 2)
        self.bMenu = QPopupMenu()
        self.bMenu.insertItem("Delete post", 1)
        self.bMenu.insertItem("Export post", 2)
        self.connect(self.aMenu, SIGNAL("activated(int)"), self.pubPopup)
        self.connect(self.bMenu, SIGNAL("activated(int)"), self.savePopup)
        self.frameCat.hide()
        
    def init(self, settings, account, password):
        print settings
        self.reload = False
        self.account = account
        self.password = password
        self.settings = settings        
        self.comboBlogs.clear()
        for blog in self.account.Blogs:
            self.comboBlogs.insertItem(blog.Name)
            
        selectedblog = self.account.Blogs [ self.account.SelectedBlog ]

        for counter in range(0, self.comboBlogs.count()):
            if self.comboBlogs.text(counter) == selectedblog.Name:
                self.comboBlogs.setCurrentItem( counter )
                break
        
##        if self.settings.getint("main", "hosttype") == 2:
##            self.frameCat.show()
        self.populateLists()
        return True

    def populateLists(self):
        self.PublishedItems = {}
        self.SavedItems = {}
        self.listPublishedPosts.clear()
        self.listSavedPosts.clear()
        selectedblog = self.account.Blogs [ self.account.SelectedBlog ]
        
        for post in selectedblog.Drafts:
            self.SavedItems [ QListBoxText(self.listSavedPosts, post.Title) ] = post

        for post in selectedblog.Posts:
            self.PublishedItems [ QListBoxText(self.listSavedPosts, post.Title) ] = post

