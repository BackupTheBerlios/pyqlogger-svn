from PyQLogger.Account import Account
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
        # set account type        
        for s in BlogServices:            
            (m,c) = s.split(".")
            for tn in range(0,self.comboProviders.count()):
                cla = getattr(globals()[m],c)
                if self.comboProviders.text(tn) == cla.name:
                    self.acc.Service = c
                    break
        
    def init(self,acc=None):
        for s in BlogServices:            
            (smodule,sclass) = s.split(".")
            cla = getattr(globals()[smodule],sclass)
            image = cla.getEmpty().getPixmap()
            if image:
                self.comboProviders.insertItem(image,cla.name)
            else:
                self.comboProviders.insertItem(cla.name)
            
        if not acc:
            self.acc = Account()
        else:
            self.acc = acc
            self.setFromAccount()

    def accept(self):
        self.putToAccount()
        QDialog.accept(self)
