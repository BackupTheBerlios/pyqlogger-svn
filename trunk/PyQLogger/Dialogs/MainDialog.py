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
from PyQLogger.Network import Network, netOp
from Speller import Speller

class MainDialog(QMainWindow):
    def spellTimer(self):
        scin = self.sourceEditor
        text = unicode ( scin.text() )
        if text :
            # clear indicators
            scin.SendScintilla(scin.SCI_STARTSTYLING, 0, scin.INDIC2_MASK)
            scin.SendScintilla(scin.SCI_SETSTYLING , len(text), 0)
            # set indicator to squigly
            scin.SendScintilla(scin.SCI_INDICSETSTYLE,2,scin.INDIC_SQUIGGLE)
            scin.SendScintilla(scin.SCI_INDICSETFORE,2,0x00ffff)
            self.speller_result = self.speller.load( unicode ( text ) )
            for result in self.speller_result.values():
                scin.SendScintilla(scin.SCI_STARTSTYLING,result["word"].start(), scin.INDIC2_MASK)
                scin.SendScintilla(scin.SCI_SETSTYLING,result["word"].end()-result["word"].start(), scin.INDIC2_MASK)

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
                    open(unicode(filename),"w").write(post.Content)
                except Exception, e:
                    print "Exception while saving to file: " + str(e)
                    QMessageBox.warning(self, "Warning", "Cannot write post to file %s" % filename)

    def savePopup(self, action):
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
                    print "Exception while saving to file: " + str(e)
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
                        print "Cannot import post!"
                
    def listPublishedPosts_contextMenuRequested(self, a0, a1):
        self.aMenu.setItemEnabled(1, a0 != None)
        self.aMenu.setItemEnabled(2, a0 != None)
        self.aMenu.popup(a1)
    
    def listSavedPosts_contextMenuRequested(self, a0, a1):
        self.bMenu.setItemEnabled(1, a0 != None)
        self.bMenu.setItemEnabled(2, a0 != None)
        self.bMenu.popup(a1)


    def NewPostAction_activated(self):
        if self.current_post:
            res = QMessageBox.question(self, "Question", 
                                   "Current post is unsaved. Are you sure you want to erase it?",
                                   QMessageBox.Yes, QMessageBox.No)
            if res == QMessageBox.No:
                return
        self.editPostTitle.setText("")
        self.sourceEditor.setText("")
        self.current_post = None

    def closeEvent(self, event):
        self.reload = self.sender() == self.btnRelogin or self.sender() == self.ReloginAction
        if self.current_post:
            res = QMessageBox.question(self, "Question", 
                                   "Current post is unsaved. Are you sure you want to exit?",
                                   QMessageBox.Yes, QMessageBox.No)
            if res == QMessageBox.No:
                event.ignore()
                return
        self.SaveAll()
        event.accept()

    def btnPublish_clicked(self):
        title = unicode(self.editPostTitle.text())
        content = unicode(self.sourceEditor.text())
        if content:
            if title:
                if self.current_post and self.current_post.ID:
                    self.network.enqueue(netOp("Editing post...",BG.startEditPost,BG.doneEditPost))
                else:
                    self.network.enqueue(netOp("Publishing post...",BG.startPublishPost,BG.donePublishPost))
            else:
                QMessageBox.warning(self, "Warning", "You forgot the post's title!")
        else:
            QMessageBox.warning(self, "Warning", "You cannot post an empty item!")

    def btnSavePost_clicked(self):
        title = unicode(self.editPostTitle.text())
        if title:
            listitem = QListBoxText(self.listSavedPosts, title)
            item = Post(Created=date.today(), Title=title,Content=unicode(self.sourceEditor.text()))
            self.account.Blogs[self.account.SelectedBlog].Drafts.Data += [ item ]
            self.SavedItems [ listitem ] = item
        else:
            QMessageBox.warning(self, "Warning", "You forgot the post's title!")

    def FetchBlogsAction_activated(self):
        self.network.enqueue(netOp("Fetching blogs...",BG.startFetchingBlogs,BG.doneFetchingBlogs))

    def SettingsAction_activated(self):
        wnd = self.forms["Settings"]
        wnd["Impl"].init(self.settings, self.forms, self.manager)
        if wnd["Class"].exec_loop() == QDialog.Accepted:
            try:
                self.settings.save()
            except Exception, inst: 
                print "btnSettings_clicked: %s" % inst
                QMessageBox.critical(self, "Error", "Cannot write configuration!")
                QApplication.exit()
    
    def PreviewAction_activated(self):
        url = self.account.Blogs[self.account.SelectedBlog].Url
        if url:
            webbrowser.open_new(url)
        else:
            QMessageBox.warning(self, "Warning", "You don't have homepage configured!\nYou can do that in the Setup dialog.")


    def FetchPostsAction_activated(self):
        self.network.enqueue(netOp("Fetching posts...",BG.startFetchingPosts,BG.doneFetchingPosts))
    
    def comboBlogs_activated(self, blogname):
        self.account.SelectedBlog =  self.account.blogById(self.account.blogByName(blogname).ID)
        self.populateLists()
    
    def listPublishedPosts_doubleClicked(self, postitem):
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
            
    class PublishMenuHanlder(QObject):
        def Popup(self, idx):
            chk = self.sender().isItemChecked(idx)            
            #itemParameter
            self.sender().setItemChecked(idx, not chk)
            
        def eventFilter(self, object, event):
            if event.type() == QEvent.MouseButtonRelease:
                if event.state() == (Qt.MidButton | Qt.ControlButton):
                    self.Menu.popup(event.globalPos())
                    return True
            return False

        def getTargets(self):
            ret = {}
            for acc in self.menus:
                bidx = 0
                ret [ acc ] = []
                for b in acc.Blogs:
                    if bool(self.menus[acc].isItemChecked(bidx)):
                        ret [ acc ] += [ b ]
                    bidx += 1
            return ret 
        
        def buildAccountMenu(self, settings, account):
            Menu = QPopupMenu()
            aidx = 0
            self.menus = {}
            for a in settings.Accounts:
                bidx = 0
                subMenu = QPopupMenu(Menu)
                for b in a.Blogs:
                    subMenu.insertItem(b.Name, bidx)
                    subMenu.setItemParameter(bidx, aidx)
                    if bidx == a.SelectedBlog and a.Name == account.Name:
                        subMenu.setItemChecked(bidx, True)
                    bidx += 1            
                self.connect(subMenu, SIGNAL("activated(int)"), self.Popup)
                Menu.insertItem(a.Name, subMenu, aidx)
                self.menus [a] = subMenu
                aidx += 1
            self.Menu = Menu

    def init_ui(self, settings):
        UI.API.setPreviewWidget(self)
        self.sourceEditor = UI.MyQextScintilla(self.Source, self)
        self.Source.layout().addWidget(self.sourceEditor)
        self.current_post = None
        self.cached_password = None
        self.cached_atomblog = None
        tabLayout = QHBoxLayout(self.toolbarTab.page(0), 11, 6, "tabLayout")
        tabLayout.setAutoAdd( True )
        tabLayout2 = QHBoxLayout(self.toolbarTab.page(1), 11, 6, "tabLayout2")
        tabLayout2.setAutoAdd( True )
        self.notifier = Notifier(self, settings.UI.Notification)
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
        #self.frameCat.hide()
        self.network = Network(self)
        self.network.start()
        
       
    def handleContextMenu(self):
        if hasattr(self,"editMenu"):
            self.sourceEditor.updateDefaultMenu(self.editMenu)

    def handleSpellMenu(self, idx):
        if idx == 99:
            self.speller.speller.add_to_personal(self.curword)
        else:
            res = self.speller_result[self.curword]
            newword = res["sug"][idx]
            self.speller.ReplaceWord(res["idx"],newword)
            self.sourceEditor.setText(self.speller.text)
        
    def fillSpellerMenu(self, start, end , parent):
        self.curword = unicode(self.sourceEditor.text())[start:end]        
        if hasattr(self,"speller_result") and \
           self.speller_result.has_key(self.curword):
            idx = 0
            Menu = QPopupMenu(parent)
            for s in self.speller_result[self.curword]["sug"][:15]:
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
        forms["Main"]["Class"].setUsesTextLabel( settings.UI.EnableText )
        self.statusBar=forms["Main"]["Class"].statusBar()

        if self.notifier.mode != 1:
            self.statusBar.hide()
        self.sourceEditor.manager = manager
        a = self.PublishMenuHanlder(self)
        a.buildAccountMenu( settings , account )
        self.btnPublish.installEventFilter(a)
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
                print "Asked to use ASpell when it's not installed! Disabling..."
                settings.Speller.Enabled = 0                
        self.comboBlogs.clear()
        for blog in self.account.Blogs:
            self.comboBlogs.insertItem(blog.Name)
            
        self.comboBlogs.setCurrentItem( self.account.SelectedBlog )
        
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
        