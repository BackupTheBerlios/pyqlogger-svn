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
from qt import QMessageBox
from setupwizardform import SetupWizardForm
from AtomBlog import makeNonce,BloggerClient,MovableTypeClient
import httplib, sha,feedparser,time,base64,re

class SetupWizardForm_Impl(SetupWizardForm):

    def __init__(self, parent = None, name = None, modal = 0, fl = 0):
        SetupWizardForm.__init__(self, parent, name, modal, fl)
        self.frameGeneric.hide()

    def initValues(self, settings):
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
                        
    def editLogin_textChanged(self, widgetName):
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
        if login and password and url and numberblogs and host and endpoint and feedpath and postpath: 
            nextButtonEnable = True
        if login and password and host and endpoint and feedpath and postpath: 
            fetchBlogsEnable = True
        if login and password and host and numberblogs and endpoint and feedpath and postpath: 
            fetchUrl = True
        self.nextButton().setEnabled( nextButtonEnable )
        self.btnFetchBlogs.setEnabled( fetchBlogsEnable )
        if self.comboProviders.currentItem() == 1:
            self.btnFetchUrl.setEnabled( fetchUrl )
        
    def comboBlogs_activated(self, widgetName):
        self.editLogin_textChanged(None)

    def comboProviders_activated(self, widgetName):
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
        bc = BloggerClient(str(self.editHost.text()), str(self.editLogin.text()), str(self.editPassword.text()))
        try:
            url = bc.getHomepage(self.blogs[unicode(self.comboBlogs.currentText())]['id'])
            if url:
                self.editURL.setText(url)
        except Exception, inst:
            print "btnFetchUrl_clicked: %s" % inst
            QMessageBox.critical(self, "Error", "Couldn't fetch blog's URL!")
            
    def _makeCommonHeaders(self, date=None):
        """ Returns a dict with Nonce, Password Digest and other headers """
        nonce = makeNonce()
        base64EncodedNonce = base64.encodestring(nonce).replace("\n", "")
        if not date:
            created = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        else:
            created = date

        passwordDigest = base64.encodestring(sha.new(nonce + created + self.password).digest()).replace("\n", "")
        authorizationHeader = 'UsernameToken Username="%s", PasswordDigest="%s", Created="%s", Nonce="%s"' % (self.login, passwordDigest, created, base64EncodedNonce)
        headers = {
            "Authorization": 'WSSE profile="UsernameToken"',
            "X-WSSE": authorizationHeader,
            "UserAgent": "Reflog's Blogger"
            }

        return headers

    def getBlogs(self):
        """ Returns dict where key is blog's name, and value is blog's properties dict """
        headers = self._makeCommonHeaders()
        conn = httplib.HTTPConnection(self.host)
        conn.request("GET", self.path, "", headers)
        response = conn.getresponse()
        xml = response.read()
        conn.close()
        ret = {}
        id_re = re.compile(r'(\d+)$')
        for blog in feedparser.parse(xml)['feed']['links']:
            ret [ blog["title"] ] = {
                'id'   : id_re.search(blog['href']).group(1),
                'href' : blog['href'],
                'rel'  : blog['rel'] ,
                'type' : blog['type'],
            }
        return ret



    def btnFetchBlogs_clicked(self):
        self.host = str(self.editHost.text())
        self.login = str(self.editLogin.text())
        self.password = str(self.editPassword.text())
        self.path = str(self.editEP.text())
        try:
            self.blogs = self.getBlogs()
            self.comboBlogs.clear()
            for blog in self.blogs.keys():
                self.comboBlogs.insertItem(blog)
            self.editLogin_textChanged(None)
        except Exception, inst:
            print "btnFetchBlogs_clicked: %s" % inst
            QMessageBox.critical(self, "Error", "Couldn't fetch list of blogs!")


    def SetupWizardForm_selected(self, widgetName):
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
                self.settings.set("main", "ep", str(self.editEP.text()))
            self.finishButton().setEnabled(True)
