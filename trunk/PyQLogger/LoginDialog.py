import sys,os
from qt import *
from Settings import Settings
from SettingsDialog import SettingsDialog
from Account import Account
from Blog import Blog
from Post import Post
from EaseXML import XMLObject
import qt_ui_loader

class LoginDialog(QDialog):
    def init(self):
        self.btnLogin.setEnabled(False)
        self.settings = Settings.load()
        if self.settings.Accounts:
            self.fillList()
        else:
            QMessageBox.information(None,"No Accounts!","""No accounts were found in your configuration! Please add at least one account in <b>Setup</b> dialog.""")

    def fillList(self):
        self.comboUsers.clear()
        for f in self.settings.Accounts:
            f.init()
            image = f.BlogService.getPixmap()
            if image:
                self.comboUsers.insertItem(image,f.Name)
            else:
                self.comboUsers.insertItem(f.Name)                


    def comboUsers_activated(self,itemname):
        acc = self.settings.accountByName(str(itemname))
        self.chkAutoLogin.setChecked(bool(self.settings.AutoLogin == acc.Name))
        self.chkSavePass.setChecked(bool(acc.Password))
        self.edtPassword.setText(acc.Password)         
        self.btnLogin.setEnabled(bool(str(self.edtPassword.text())))
        
    def edtPassword_textChanged(self,text):
        self.btnLogin.setEnabled(bool(str(text)))
        
    def btnLogin_clicked(self):
        pass
        
    def btnSettings_clicked(self):
        sett_impl = SettingsDialog()
        aform = qt_ui_loader.create( 'settingsdialog.ui', sett_impl,None,True )
        sett_impl.init(self.settings)
        if aform.exec_loop() == QDialog.Accepted:
            self.fillList()
            self.settings.save()
        
a = QApplication(sys.argv)
myform_impl = LoginDialog()
myform = qt_ui_loader.create( 'logindialog.ui', myform_impl,None,True )
myform_impl.init()
QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
a.setMainWidget(myform)
myform.show()
a.exec_loop()



