from PyQLogger.Account import Account
from PyQLogger.Blog import Blog
from qt import QListBoxPixmap,QPixmap,QListBoxText,QDialog
from PyQLogger.Services import *
from PyQLogger.Services import BlogServices

class AccountSettingsDialog(QDialog):
    def setFromAccount(self):
        self.edtName.setText(self.acc.Name)
        self.edtUsername.setText(self.acc.Username)
        self.edtPassword.setText(self.acc.Password)
        self.edtHost.setText(self.acc.Host)
        for b in self.acc.Blogs:
            self.comboBlogs.insertItem(b.Name)
        if len(self.acc.Blogs) and self.acc.SelectedBlog<len(self.acc.Blogs):
            self.comboBlogs.setCurrentItem(self.acc.SelectedBlog)
        for tn in range(0,self.comboProviders.count()):
            if self.comboProviders.text(tn) == self.acc.BlogService.name:
                self.comboProviders.setCurrentItem(tn)
                break        

    def putToAccount(self):
        # save strings
        self.acc.Name = unicode(self.edtName.text())
        self.acc.Username = unicode(self.edtUsername.text())
        self.acc.Password = unicode(self.edtPassword.text())
        self.acc.Host = unicode(self.edtHost.text())
        # add new blogs (if any)
        for tn in range(0,self.comboBlogs.count()):
            flag = False
            cbname = unicode(self.comboBlogs.text(tn))
            for b  in self.acc.Blogs:
                if b.Name == cbname:
                    flag = True
                    break
            if not flag:
                self.acc.Blogs += [ self.getBlog(cbname) ]
        self.acc.SelectedBlog = int(self.comboBlogs.currentItem())
        # set account type        
        for s in BlogServices:            
            (m,c) = s.split(".")
            cla = getattr(globals()[m],c)
            if self.comboProviders.text(self.comboProviders.currentItem()) == cla.name:
                self.acc.Service = c
                return
        
    def getBlog(self,name):
        # return just fetched blog...
        return Blog()

    def init_ui(self):
        for s in BlogServices:            
            (smodule,sclass) = s.split(".")
            cla = getattr(globals()[smodule],sclass)
            image = cla.getEmpty().getPixmap()
            if image:
                self.comboProviders.insertItem(image,cla.name)
            else:
                self.comboProviders.insertItem(cla.name)
        

    def init(self,acc=None):            
        if not acc:
            self.acc = Account(SelectedBlog = 0,Service='MovableTypeService')
            self.acc.Blogs += [ Blog(Name="test",ID="123") ]
            self.acc.init()
        else:
            self.acc = acc
            
        self.setFromAccount()

    def accept(self):
        self.putToAccount()
        QDialog.accept(self)
