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

from qt import *
from setupwizardform import SetupWizardForm
from AtomBlog import *
import PyQLoggerConfig

class SetupWizardForm_Impl(SetupWizardForm):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        SetupWizardForm.__init__(self,parent,name,modal,fl)
        self.frameGeneric.hide()

    def initValues(self,settings):
        self.settings = settings
        self.blogs = ()
        if self.settings.has_option("main", "login"):
            self.editLogin.setText(self.settings.get("main", "login"))
        if self.settings.has_option("main", "url"):
            self.editURL.setText(self.settings.get("main", "url"))
        if self.settings.has_option("main", "password"):
            self.editPassword.setText(self.settings.get("main", "password"))
        if self.settings.has_option("main", "host"):
            self.editHost.setText(self.settings.get("main", "host"))
        if self.settings.has_option("main", "hosttype"):
            self.comboProviders.setCurrentItem(self.settings.getint("main", "hosttype"))
            self.comboProviders_activated(self.comboProviders.text(self.settings.getint("main", "hosttype")))
        else:
            self.comboProviders.setCurrentItem(1)
            self.comboProviders_activated(self.comboProviders.text(1))
        if self.settings.has_option("main", "ep"):
            self.editEP.setText(self.settings.get("main", "ep"))
        if self.settings.has_option("main", "pp"):
            self.editPP.setText(self.settings.get("main", "pp"))
        if self.settings.has_option("main", "fp"):
            self.editFP.setText(self.settings.get("main", "fp"))
        self.checkSave.setChecked(self.settings.has_option("main", "password"))
        if self.settings.has_option("main", "blogs"):
            counter = 0
            for blogid in self.settings.get("main", "blogs").split(';'):
                blogname = self.settings.get(blogid, "name")
                self.comboBlogs.insertItem(blogname)
                if self.settings.has_option("main", "selectedblog"):
                    if blogid == self.settings.getint("main", "selectedblog"):
                        self.comboBlogs.setCurrentItem( counter )
                counter += 1
                        
    def editLogin_textChanged(self,widgetName):
        login = str(self.editLogin.text())
        password = str(self.editPassword.text())
        host = str(self.editHost.text())
        url = str(self.editURL.text())
        endpoint = str(self.editEP.text())
        feedpath = str(self.editFP.text())
        postpath = str(self.editPP.text())
        numberblogs = self.comboBlogs.count() > 0
        nextButtonEnable = False # control next button (b)
        fetchBlogsEnable = False #control fetch blogs button (b2)
        fetchUrl = False #control fetch url button (b3)
        if login and password and url and numberblogs and host and endpoint and feedpath and postpath: nextButtonEnable = True
        if login and password and host and endpoint and feedpath and postpath: fetchBlogsEnable = True
        if login and password and host and numberblogs and endpoint and feedpath and postpath: fetchUrl = True
        self.nextButton().setEnabled( nextButtonEnable )
        self.btnFetchBlogs.setEnabled( fetchBlogsEnable )
        if self.comboProviders.currentItem() == 1:
            self.btnFetchUrl.setEnabled( fetchUrl )
        
    def comboBlogs_activated(self,widgetName):
        self.editLogin_textChanged(None)

    def comboProviders_activated(self,widgetName):
        """ generic/blogger/movable """
        if self.comboProviders.text(0) == widgetName:
            self.frameGeneric.show()
            host = endpoint = feedpath = postpath = ""
        elif self.comboProviders.text(1) == widgetName:
            self.frameGeneric.hide()
            host = "www.blogger.com"
            (endpoint, feedpath, postpath)  = BloggerClient.endpoints
        elif self.comboProviders.text(2) == widgetName:
            self.frameGeneric.hide()
            host = ""
            (endpoint, feedpath, postpath)  = MovableTypeClient.endpoints
            
        self.editHost.setText(host)
        self.editEP.setText(endpoint)
        self.editFP.setText(feedpath)
        self.editPP.setText(postpath)
    
    def btnFetchUrl_clicked(self):
        bc = BloggerClient(str(self.editHost.text()),str(self.editLogin.text()), str(self.editPassword.text()))
        try:
            url = bc.getHomepage(self.blogs[unicode(self.comboBlogs.currentText())]['id'])
            if url:
                self.editURL.setText(url)
        except Exception, inst:
            print "btnFetchUrl_clicked: %s" % inst
            QMessageBox.critical(self,"Error","Couldn't fetch blog's URL!")
            pass
    
    def btnFetchBlogs_clicked(self):
        host = str(self.editHost.text())
        login = str(self.editLogin.text())
        password = str(self.editPassword.text())
        endpoint = str(self.editEP.text())
        feedpath = str(self.editFP.text())
        postpath = str(self.editPassword.text())
##        (h,l,p) = (str(self.editHost.text()),str(self.editLogin.text()), str(self.editPassword.text()))
##        (ep,fp,pp) = (str(self.editEP.text()),str(self.editFP.text()),str(self.editPP.text()))
        if self.comboProviders.currentItem() == 0:
            at = GenericAtomClient(host, login, password, endpoint, feedpath, postpath)
        elif self.comboProviders.currentItem() == 1:
            at = BloggerClient(host, login, password)
        elif self.comboProviders.currentItem() == 2:
            at = MovableTypeClient(host, login, password)
        try:
            self.blogs = at.getBlogs()
            self.comboBlogs.clear()
            for blog in self.blogs.keys():
                self.comboBlogs.insertItem(blog)
            self.editLogin_textChanged(None)
        except:
            QMessageBox.critical(self,"Error","Couldn't fetch list of blogs!")


    def SetupWizardForm_selected(self,widgetName):

        if widgetName == "Login Details":
            self.editLogin_textChanged(None)
        if widgetName == "Final":
            self.settings.set("main", "login", str(self.editLogin.text()))
            self.settings.set("main", "url", str(self.editURL.text()))
            self.settings.set("main", "host", str(self.editHost.text()))
            self.settings.set("main", "hosttype", self.comboProviders.currentItem())
            if len(self.blogs) > 0:
                self.settings.addblogs(self.blogs)
                self.settings.set("main", "selectedblog", self.blogs[unicode(self.comboBlogs.currentText())]['id'])

            if self.checkSave.isChecked():
                self.settings.set("main", "password", str(self.editPassword.text()))
            if self.comboProviders.currentItem() == 0:
                self.settings.set("main", "pp", str(self.editPP.text()))
                self.settings.set("main", "fp", str(self.editFP.text()))
                self.settigns.set("main", "ep", str(self.editEP.text()))
            self.finishButton().setEnabled(True)
