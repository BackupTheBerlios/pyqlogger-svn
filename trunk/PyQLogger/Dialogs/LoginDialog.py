import sys,os
from qt import *
from PyQLogger.Settings import Settings
from SettingsDialog import SettingsDialog
from AccountSettingsDialog import AccountSettingsDialog
from PyQLogger.Account import Account
from PyQLogger.Blog import Blog
from PyQLogger.Post import Post
from EaseXML import XMLObject

class LoginDialog(QDialog):
    def init(self, settings, forms, manager):
        self.manager = manager
        self.btnLogin.setEnabled(False)
        self.settings = settings
        self.forms = forms
        if not self.settings.Accounts:
            QMessageBox.information(None,"No Accounts!","""No accounts were found in your configuration! Please add at least one account in <b>Setup</b> dialog.""")
            wnd = forms["AccountSettings"]
            wnd["Impl"].init()
            if wnd["Class"].exec_loop() == QDialog.Rejected: 
                QMessageBox.warning(None,"No Accounts!","""Program cannot work without accounts!""")
                return False
            self.settings.Accounts += [ wnd["Impl"].acc ]
            self.settings.save()
            print self.settings
        self.fillList()
        return True

    def fillList(self):
        self.comboUsers.clear()
        for f in self.settings.Accounts:
            f.init()
            image = f.BlogService.getPixmap()
            if image:
                self.comboUsers.insertItem(image,f.Name)
            else:
                self.comboUsers.insertItem(f.Name)
        if len(self.settings.Accounts):
            tacc = 0
            if self.settings.AutoLogin:
                for i in range(0,self.comboUsers.count()):
                    if self.settings.AutoLogin == str(self.comboUsers.text(i)):
                        tacc = i
                        break
            self.comboUsers.setCurrentItem( tacc )
            self.comboUsers_activated( self.settings.Accounts [ tacc ].Name )
    

    def comboUsers_activated(self,itemname):
        acc = self.settings.accountByName(str(itemname))
        self.chkAutoLogin.setChecked(bool(self.settings.AutoLogin == acc.Name))
        self.chkSavePass.setChecked(bool(acc.Password))
        self.edtPassword.setText(acc.Password)         
        self.btnLogin.setEnabled(bool(str(self.edtPassword.text())))
        
    def edtPassword_textChanged(self,text):
        self.btnLogin.setEnabled(bool(str(text)))
        
    def accept(self):
        acc = self.settings.accountByName(str(self.comboUsers.text(self.comboUsers.currentItem())))
        #check if we need to save changes
        psw = str(self.edtPassword.text())
        shouldsave = False
        if self.chkAutoLogin.isChecked()  and self.settings.AutoLogin != acc.Name:
            self.settings.AutoLogin = acc.Name
            shouldsave = True
        if bool(self.chkSavePass.isChecked()) and acc.Password!=psw:
            acc.Password=psw
            shouldsave = True
        if  shouldsave:                
            self.settings.save()
        QDialog.accept(self)
        self.acc = acc
    
    def btnSettings_clicked(self):
        wnd = self.forms["Settings"]
        wnd["Impl"].init(self.settings,self.forms,self.manager)
        if wnd["Class"].exec_loop() == QDialog.Accepted:
            self.fillList()
            self.settings.save()
        
