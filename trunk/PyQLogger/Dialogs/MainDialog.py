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

from qt import *
import os, pickle, webbrowser
from PyQLogger.Settings import Settings
from datetime import date
from PyQLogger.ToolBar import initToolbar
from PyQLogger.Notifier import Notifier
from PyQLogger.Post import Post
from PyQLogger import BG, UI
from PyQLogger.Network import Network, netOp, OpCompleteEvent
from Speller import Speller
from PyQLogger.Plugins.EventPlugin import EventType
from Logging import LoggerWidget
from logging import Logger
import thread
class MainDialog(QMainWindow):
    
    def spellTimer(self):
        if not self.spellthread.running():
            self.spellthread.start()
    
    def getPage(self, title):
        if not title: 
            return self.toolbarTab.page(0)
        for i in range(0, self.toolbarTab.count()):
            if title == str(self.toolbarTab.label(i)):
                return self.toolbarTab.page(i)
        return None

    def editorTab_currentChanged(self, widget):
        if widget == self.Preview:
            UI.API.setPreview(self, self.sourceEditor.text())

    def pubPopup(self, action):
        if(action == 1):
            res = QMessageBox.question(self, "Question", "Are you sure you want to delete this post?", QMessageBox.Yes, QMessageBox.No)
            if res == QMessageBox.Yes:
                self.network.enqueue(netOp("Deleting post...",BG.startDeletePost,BG.doneDeletePost))
        elif(action == 2):
            filename = QFileDialog.getSaveFileName(os.path.expanduser("~"),
                                        "All files (*.*)",self,           
                                        "Export post dialog",
                                        "Choose a filename to save under")
            if str(filename):
                try:
                    self.postsmutex.lock()
                    post = self.PublishedItems[ self.listPublishedPosts.selectedItem () ]
                    open(unicode(filename),"w").write(post.Content)
                    self.postsmutex.unlock()
                except Exception, e:
                    self.log.error("Exception while saving to file",exc_info=1)
                    QMessageBox.warning(self, "Warning", "Cannot write post to file %s" % filename)

    def savePopup(self, action):
        self.draftsmutex.lock()
        if(action == 1):
            res = QMessageBox.question(self, "Question", "Are you sure you want to delete this post?", QMessageBox.Yes, QMessageBox.No)
            if res == QMessageBox.Yes:
                post = self.SavedItems [ self.listSavedPosts.selectedItem () ]
                del self.SavedItems [ self.listSavedPosts.selectedItem () ]
                self.account.Blogs[self.account.SelectedBlog].Drafts.Data.remove(post)
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
                    open(unicode(filename),"w").write(post.Content)
                except Exception, e:
                    self.log.error("Exception while saving to file",exc_info=1)
                    QMessageBox.warning(self, "Warning", "Cannot write post to file %s!" % filename)
        elif(action == 3):
            files = QFileDialog.getOpenFileNames("All files (*.*)",
                                                 os.path.expanduser("~"),self,           
                                                 "Import posts",
                                                 "Choose a files with posts")
            if files.count():
                for fname in files:
                    try:
                        title = os.path.basename(str(fname))
                        item = Post(Created=date.today(), 
                                    Title=title,
                                    Content=open(str(fname)).read() )
                        self.account.Blogs[self.account.SelectedBlog].Drafts.Data += [ item ]
                        listitem = QListBoxText(self.listSavedPosts, title)
                        self.SavedItems [ listitem ] = item
                    except:
                        self.log.error("Exception while importing file",exc_info=1)
                        QMessageBox.warning(self, "Warning", "Cannot import post file!")
        self.draftsmutex.lock()
        
    def listPublishedPosts_contextMenuRequested(self, a0, a1):
        self.aMenu.setItemEnabled(1, a0 != None)
        self.aMenu.setItemEnabled(2, a0 != None)
        self.aMenu.popup(a1)

    def listSavedPosts_contextMenuRequested(self, a0, a1):
        self.bMenu.setItemEnabled(1, a0 != None)
        self.bMenu.setItemEnabled(2, a0 != None)
        self.bMenu.popup(a1)

    def proposeSavePost(self, action):
        if self.current_post:
            changed = self.current_post.Title != unicode(self.editPostTitle.text())
            changed = changed or self.current_post.Content != unicode(self.sourceEditor.text())
        else:
            changed = unicode(self.editPostTitle.text()) != ""
            changed = changed or unicode(self.sourceEditor.text()) != ""
        if changed:
            res = QMessageBox.question(self, "Question", 
                                   "Current post is unsaved. Are you sure you want to %s?"%action,
                                   QMessageBox.Yes, QMessageBox.No)
            if res == QMessageBox.No:
                return True
        return False    
    
    def NewPostAction_activated(self):
        if self.proposeSavePost("erase it"):
            return
        self.editPostTitle.setText("")
        self.sourceEditor.setText("")
        self.current_post = None

    def close_Event(self, event):
        print "in close_even"
        if self.proposeSavePost("exit"):
            return False
        self.SaveAll()
        return True

    def btnPublish_clicked(self):
        title = unicode(self.editPostTitle.text())
        content = unicode(self.sourceEditor.text())
        if content:
            if title:
                if self.current_post and self.current_post.ID:
                    self.btnPublish.setEnabled(False)
                    self.network.enqueue(netOp("Editing post...",BG.startEditPost,BG.doneEditPost))
                else:
                    self.manager.handleEvent(EventType.BEFOREPUBLISH, None)
                    if self.getCrossBlogList():
                        self.btnPublish.setEnabled(False)
                        self.network.enqueue(netOp("Publishing post...",BG.startPublishPost,BG.donePublishPost))
                    else:
                        QMessageBox.warning(self, "Warning", "You have to select at least one blog to post to!")
            else:
                QMessageBox.warning(self, "Warning", "You forgot the post's title!")
        else:
            QMessageBox.warning(self, "Warning", "You cannot post an empty item!")

    def btnSavePost_clicked(self):
        self.draftsmutex.lock()
        title = unicode(self.editPostTitle.text())
        if title:
            listitem = QListBoxText(self.listSavedPosts, title)
            item = Post(Created=str(date.today()), Title=title,Content=unicode(self.sourceEditor.text()))
            self.account.Blogs[self.account.SelectedBlog].Drafts.Data += [ item ]
            self.SavedItems [ listitem ] = item
        else:
            QMessageBox.warning(self, "Warning", "You forgot the post's title!")
        self.draftsmutex.unlock()

    def FetchBlogsAction_activated(self):
        self.FetchBlogsAction.setEnabled(False)
        self.network.enqueue(netOp("Fetching blogs...",BG.startFetchingBlogs,BG.doneFetchingBlogs))

    def SettingsAction_activated(self):
        wnd = self.forms["Settings"]
        wnd["Impl"].init(self.settings, self.forms, self.manager)
        if wnd["Class"].exec_loop() == QDialog.Accepted:
            try:
                self.settings.save()
            except Exception, inst: 
                import traceback
                traceback.print_exc()
                QMessageBox.critical(self, "Error", "Cannot write configuration!")
                QApplication.exit()
    
    def PreviewAction_activated(self):
        url = self.account.Blogs[self.account.SelectedBlog].Url
        if url:
            webbrowser.open_new(url)
        else:
            QMessageBox.warning(self, "Warning", "You don't have homepage configured!\nYou can do that in the Setup dialog.")


    def FetchPostsAction_activated(self):
        self.FetchPostsAction.setEnabled(False)
        self.network.enqueue(netOp("Fetching posts...",BG.startFetchingPosts,BG.doneFetchingPosts))
    
    def comboBlogs_activated(self, blogname):
        self.account.SelectedBlog =  self.account.blogById(self.account.blogByName(blogname).ID)
        self.populateLists()
    
    def listPublishedPosts_doubleClicked(self, postitem):
        if self.proposeSavePost("overwrite it"):       
            return
        if self.PublishedItems.has_key(postitem):
            post = self.PublishedItems[postitem]
            self.current_post = post
            self.editPostTitle.setText(post.Title)
            self.sourceEditor.setText(post.Content)
            self.editorTab.setCurrentPage(0)            
            self.sender().setFocus()
        else:
            QMessageBox.critical(self, "Error", "Something is not right!")
    
    def listSavedPosts_doubleClicked(self, item):
        if self.proposeSavePost("overwrite it"):       
            return
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
            self.log.critical("Cannot write configuration!", exc_info=1)
            QMessageBox.critical(self, "Error", "Cannot write configuration!")
                    
    def getCrossBlogList(self):
        res = []
        for (account, bloghash) in self.crossPost.items():
            for (blog, control) in bloghash.items():
                if control.isChecked():
                    if not hasattr(account, "inited"):
                        account.init()
                    res += [ blog ] 
        return res
    
    def prepareCrossBlog(self):
        for control in self.crossPostControls:
            control.hide()
        self.crossPostControls = []
        self.crossPost = {}
        for a in self.settings.Accounts:
            self.crossPost[a]={}
            lbl = QLabel(self.grpCross)
            lbl.setText("Account: %s Blogs: "%a.Name )
            self.crossPostControls += [ lbl ]
            bidx = 0
            for b in a.Blogs:
                ctrl = QCheckBox(self.grpCross)
                ctrl.setText(b.Name)
                self.crossPost[a][b] = ctrl
                self.crossPostControls += [ ctrl ]
                if bidx == a.SelectedBlog and a.Name == self.account.Name:
                    ctrl.setChecked(True)
                bidx += 1

    def close(self):
        print "in close from:"+str(self.sender())
        self.reload = self.sender() == self.btnRelogin or self.sender() == self.ReloginAction
        self.forms["Main"]["Class"].close() 

    def event(self, e):
        if hasattr(e, "data") and isinstance(e.data(),OpCompleteEvent):
            d = e.data()
            d.method(d.parent, d.data)
            return True
        return False
    
    def eventFilter(self, object, event):
        """ this is a dirty-ass hack to intercept the closeEvent fully """
        if event and event.type() == QEvent.Close and object != self:
            print "in eventfilter from"+str(object)+" sender "+str(self.sender())
            if not self.close_Event(event):
                return True
            else:
                self.forms["Main"]["Class"].removeEventFilter(self)
        return False

    def init_ui(self, settings, forms):
        self.forms = forms
        forms["Main"]["Class"].installEventFilter(self)
        UI.API.setPreviewWidget(self)
        self.sourceEditor = UI.MyQextScintilla(self.Source, self)
        self.Source.layout().addWidget(self.sourceEditor)
        logLayout = QHBoxLayout(None,0,6,"logLayout")
        self.log = Logger("Default", settings.DebugLevel)
        self.logFrame.hide()
        self.btnLogger = LoggerWidget(self.leftFrame, self.log, self)
        logLayout.addWidget(self.btnLogger)
        self.leftFrame.layout().addLayout(logLayout)
        self.log.info("info test")
        self.log.critical("critical test")
        self.current_post = None
        self.cached_password = None
        self.cached_atomblog = None
        grpLayout = QVBoxLayout(self.grpCross)
        grpLayout.setAutoAdd( True )
        tabLayout = QHBoxLayout(self.toolbarTab.page(0), 11, 6, "tabLayout")
        tabLayout.setAutoAdd( True )
        tabLayout2 = QHBoxLayout(self.toolbarTab.page(1), 11, 6, "tabLayout2")
        tabLayout2.setAutoAdd( True )
        forms["Main"]["Class"].setUsesTextLabel( settings.UI.EnableText )
        for button in [self.btnPublish,self.btnSavePost,self.btnExit,self.btnRelogin]:
            if settings.UI.EnableText:
                button.setMaximumSize(QSize(65,65))
                button.setMinimumSize(QSize(65,65))
            else:
                button.setMaximumSize(QSize(45,45))
                button.setMinimumSize(QSize(45,45))
            button.setUsesTextLabel( settings.UI.EnableText )
        self.statusBar=forms["Main"]["Class"].statusBar()
        self.aMenu = QPopupMenu()
        self.aMenu.insertItem("Delete post", 1)
        self.aMenu.insertItem("Export post", 2)
        self.bMenu = QPopupMenu()
        self.bMenu.insertItem("Delete post", 1)
        self.bMenu.insertItem("Export post", 2)
        self.bMenu.insertItem("Import posts", 3)
        self.connect(self.CutAction,SIGNAL("activated()"),self.sourceEditor.cut)
        self.connect(self.CopyAction,SIGNAL("activated()"),self.sourceEditor.copy)
        self.connect(self.PasteAction,SIGNAL("activated()"),self.sourceEditor.paste)
        self.connect(self.UndoAction,SIGNAL("activated()"),self.sourceEditor.undo)
        self.connect(self.RedoAction,SIGNAL("activated()"),self.sourceEditor.redo)
        self.connect(self.aMenu, SIGNAL("activated(int)"), self.pubPopup)
        self.connect(self.bMenu, SIGNAL("activated(int)"), self.savePopup)
        self.connect(self.sourceEditor, PYSIGNAL("aboutToShowMenu"), self.showMenu)
        self.connect(self.sourceEditor, SIGNAL("textChanged()"), self.sourceEditor_textChanged)
        self.network = Network(self)
        self.network.start()


    def handleContextMenu(self):
        if hasattr(self,"editMenu"):
            self.sourceEditor.updateDefaultMenu(self.editMenu)

    def handleSpellMenu(self, idx):
        if idx == 99:
            self.speller.speller.add_to_personal(self.curword)
        else:
            for rez in self.speller_result.keys():
                if rez.group(0) == self.curword:
                    res = self.speller_result[rez]
            newword = res["sug"][idx]
            self.speller.ReplaceWord(res["idx"],newword)
            self.sourceEditor.setText(self.speller.text)
        
    def fillSpellerMenu(self, start, end , parent):
        self.curword = unicode(self.sourceEditor.text())[start:end]
        res = None
        if hasattr(self,"speller_result"):
            for rez in self.speller_result.keys():
                if rez.group(0) == self.curword:
                    res = self.speller_result[rez]
            
        if res:
            idx = 0
            Menu = QPopupMenu(parent)
            for s in res["sug"][:15]:
                Menu.insertItem(s, idx)
                idx += 1
            Menu.insertSeparator()
            Menu.insertItem("Add",99)
            self.connect(Menu, SIGNAL('activated(int)'), self.handleSpellMenu)
            parent.insertSeparator()
            parent.insertItem("Corrections",Menu)
            
    def showMenu(self, evt):
        sci = self.sourceEditor
        gpos = evt.globalPos()
        pos = evt.pos()
        position = sci.SendScintilla(sci.SCI_POSITIONFROMPOINTCLOSE,pos.x(),pos.y())
        self.editMenu = QPopupMenu(self.sourceEditor)
        self.connect(self.editMenu, SIGNAL('aboutToShow()'), self.handleContextMenu)
        sci.fillDefaultMenu(self.editMenu)
        if position > -1 :
            end = sci.SendScintilla( sci.SCI_WORDENDPOSITION , position, True)
            start = sci.SendScintilla( sci.SCI_WORDSTARTPOSITION , position, True)
            self.fillSpellerMenu(start,end,self.editMenu)
        self.editMenu.insertSeparator()
        self.manager.fillMenu(self.editMenu)
        self.editMenu.popup(gpos)
        
    
    def init(self, settings, forms, account, password, manager):
        self.manager = manager
        self.reload = False
        self.account = account
        self.password = password
        self.settings = settings        
        self.forms = forms
        self.postsmutex = QMutex()
        self.blogsmutex = QMutex()
        self.draftsmutex = QMutex()
        self.spellthread = BG.SpellThread(self)
        if not hasattr(self,"crossPostControls"):
            self.crossPostControls = []
        self.crossPost = {}
        self.prepareCrossBlog()
        self.notifier = Notifier(self, settings.UI.Notification)
        
        if self.notifier.mode != 1:
            self.statusBar.hide()
        self.sourceEditor.manager = manager
        manager.fillToolbar()
        self.edtStylesheet.setText(self.settings.StyleSheet)
        self.edtStylesheet_textChanged('')
        if settings.Speller.Enabled:
            try:
                import aspell
                self.speller = Speller(settings)
                timer = QTimer( self )
                self.connect( timer, SIGNAL("timeout()"), self.spellTimer )
                timer.start( 5000 )        
            except Exception , e:
                self.log.warn("Asked to use ASpell when it's not installed! Disabling...")
                settings.Speller.Enabled = 0                
        self.comboBlogs.clear()
        for blog in self.account.Blogs:
            self.comboBlogs.insertItem(blog.Name)
            
        self.comboBlogs.setCurrentItem( self.account.SelectedBlog )
        
        self.populateLists()
        return True

    def populateLists(self):
        self.PublishedItems = {}
        self.SavedItems = {}
        self.listPublishedPosts.clear()
        self.listSavedPosts.clear()
        selectedblog = self.account.Blogs [ self.account.SelectedBlog ]
        for post in selectedblog.Drafts.Data:
            self.SavedItems [ QListBoxText(self.listSavedPosts, post.Title) ] = post

        for post in selectedblog.Posts.Data:
            self.PublishedItems [ QListBoxText(self.listPublishedPosts, post.Title) ] = post


    def edtStylesheet_textChanged( self, text ):
        fname = str(self.edtStylesheet.text())
        havefile = bool(fname and os.path.exists(fname))
        canapply = bool(self.settings.UI.EnableKde) and havefile
        self.btnApplyCSS.setEnabled(havefile)
    
    def btnLoadCSS_clicked(self):
        filename = QFileDialog.getOpenFileName(os.path.expanduser("~"),
                                    "All files (*.*)",self,           
                                    "CSS Sheet",
                                    "Choose a filename to open")
        if str(filename):
            self.edtStylesheet.setText(filename)
            self.edtStylesheet_textChanged(filename)
                
    def btnApplyCSS_clicked(self):
        self.settings.StyleSheet = str(self.edtStylesheet.text())
        self.vp.setUserStyleSheet(open(self.settings.StyleSheet).read())
        
