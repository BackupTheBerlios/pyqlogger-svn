from PyQLogger.Account import Account
from PyQLogger.Blog import Blog
from qt import QListBoxPixmap,QPixmap,QListBoxText,QDialog,QMessageBox
from PyQLogger.Services import *
from PyQLogger.Services import BlogServices

class AccountSettingsDialog(QDialog):
    def setFromAccount(self):
        self.edtName.setText(self.acc.Name)
        self.edtUsername.setText(self.acc.Username)
        self.edtPassword.setText(self.acc.Password)
        self.edtHost.setText(self.acc.Host)
        self.comboBlogs.clear()
        for b in self.acc.Blogs:
            self.comboBlogs.insertItem(b.Name)
        if len(self.acc.Blogs) and self.acc.SelectedBlog<len(self.acc.Blogs):
            self.comboBlogs.setCurrentItem(self.acc.SelectedBlog)
            self.edtHomepage.setText(self.acc.Blogs [ self.acc.SelectedBlog ].Url)
        for tn in range(0,self.comboProviders.count()):
            if self.comboProviders.text(tn) == self.acc.BlogService.name:
                self.comboProviders.setCurrentItem(tn)
                break        

    def putProps(self):
        # save strings
        self.acc.Name = unicode(self.edtName.text())
        self.acc.Username = unicode(self.edtUsername.text())
        self.acc.Password = unicode(self.edtPassword.text())
        self.acc.Host = unicode(self.edtHost.text())        

    def putToAccount(self):
        self.putProps()
        self.acc.SelectedBlog = int(self.comboBlogs.currentItem())
        # set account type
        pt = str(self.comboProviders.text(self.comboProviders.currentItem()))
        if self.text_prov.has_key(pt):
            self.acc.Service = self.text_prov[pt]
            self.acc.init()
        
    def _textChanged(self, text):
        self.updateButtons()
        
    def btnFetchHome_clicked(self):
        self.putProps()
        pt = str(self.comboProviders.text(self.comboProviders.currentItem()))
        self.comboProviders_activated(pt)
        pt = str(self.comboBlogs.text(self.comboBlogs.currentItem()))
        blog = self.acc.blogByName(pt)
        try:
            url = blog.Service.getHomepage(blog.ID)
            blog.Url = url
            self.edtHomepage.setText(url)
        except Exception, e:
            QMessageBox.warning(None,"Error!",str(e))

    def btnFetchBlogs_clicked(self):
        self.putProps()
        pt = str(self.comboProviders.text(self.comboProviders.currentItem()))
        self.comboProviders_activated(pt)
        try:
            self.acc.fetchBlogs()
            self.setFromAccount()
            self.updateButtons()
        except Exception, e:
            QMessageBox.warning(None,"Error!",str(e))
        
    def init_ui(self):
        self.prov_text = {}
        self.text_prov = {}
        for s in BlogServices:            
            (smodule,sclass) = s.split(".")
            cla = getattr(globals()[smodule],sclass)
            self.prov_text[sclass] = cla.name
            self.text_prov[cla.name] = sclass
            image = cla.getEmpty().getPixmap()
            if image:
                self.comboProviders.insertItem(image,cla.name)
            else:
                self.comboProviders.insertItem(cla.name)

    def edtHomepage_textChanged(self, text):
        index = self.comboBlogs.currentItem()
        self.acc.Blogs [ index ].Url = str(text)

    def comboBlogs_activated(self, index):
        self.edtHomepage.setText(self.acc.Blogs [ index ].Url)

    def comboProviders_activated (self, item):
        if self.text_prov.has_key(str(item)):
            self.acc.Service = self.text_prov [ str(item) ]
            self.acc.init()
            self.updateButtons()

    def init(self,acc=None):
        if not acc:
            self.acc = Account()
        else:
            self.acc = acc
            self.setFromAccount()
        self.updateButtons()

    def updateButtons(self):
        done = False
        canFetchBlogs = False
        canFetchHome = False
        hasService = hasattr(self.acc,"BlogService")
        hasGetHome = hasService and hasattr(self.acc.BlogService,"getHomepage")
        name = unicode(self.edtName.text())
        username = unicode(self.edtUsername.text())
        password = unicode(self.edtPassword.text())
        host = unicode(self.edtHost.text())        
        
        canFetchBlogs = bool(username and password and host)
        canFetchHome = bool(canFetchBlogs and self.comboBlogs.count() and hasGetHome)
        done = bool(canFetchBlogs and self.comboBlogs.count() and name)
        self.btnFetchHome.setEnabled(canFetchHome)
        self.btnFetchBlogs.setEnabled(canFetchBlogs)
        self.buttonOk.setEnabled(done)
        
        if hasService and self.acc.BlogService.host:
            self.edtHost.setText(self.acc.BlogService.host)
        if not name and hasService:
            self.edtName.setText(self.acc.BlogService.name+" Account")

    def accept(self):
        self.putToAccount()
        QDialog.accept(self)
