from PyQLogger.Settings import Settings
from AccountSettingsDialog import AccountSettingsDialog
from qt import QListBoxPixmap,QPixmap,QListBoxText,QDialog,QMessageBox

class SettingsDialog(QDialog):
    def getAccItem(self,acc):
        image = acc.BlogService.getPixmap()
        if image:        
            i = QListBoxPixmap (  image, acc.Name )
        else:
            i = QListBoxText ( acc.Name )
        return i
        
    def fillList(self):
        self.lbAccounts.clear()
        for f in self.settings.Accounts:
            f.init()
            self.lbAccounts.insertItem(self.getAccItem(f))
        #select firt
        if len(self.settings.Accounts):
            self.lbAccounts.setCurrentItem(0)
        else: #if empty, disable controls
            self.btnEditAccount.setEnabled(False)
            self.btnDelAccount.setEnabled(False)
        
    def init(self,settings,forms):
        self.settings = settings
        self.forms = forms
        #add accounts
        self.fillList()
        # set gui settings
        self.chkKDE.setChecked(bool(settings.UI_Settings.EnableKde))
        self.chkScintilla.setChecked(bool(settings.UI_Settings.EnableQScintilla))
        if settings.UI_Settings.Notification == 0:
            self.rbOSD.setChecked(True)
        else:
            self.rbStatus.setChecked(True)

    def btnAddAccount_clicked(self):
        wnd = self.forms["AccountSettings"]
        wnd["Impl"].init()
        if wnd["Class"].exec_loop() == QDialog.Accepted:
            self.settings.Accounts += [ wnd["Impl"].acc ]
            self.settings.save()
            self.fillList()        

    def btnDelAccount_clicked(self):
        res = QMessageBox.warning(None,
            self.trUtf8("Confirmation"),
            self.trUtf8("""Are you absolutely sure that you want to erase <b>all</b> data inside this account (i.e. all the blogs and posts)?"""),
            self.trUtf8("&Yes"),
            self.trUtf8("&No"),
            None,
            0, -1)
        if res == 0:
                acc = self.settings.accountByName(str(self.lbAccounts.currentText()))
                del self.settings.Accounts[self.settings.Accounts.index(acc)]
                self.settings.save()
                self.fillList()  



    def btnEditAccount_clicked(self):
        wnd = self.forms["AccountSettings"]
        wnd["Impl"].init(self.settings.accountByName(str(self.lbAccounts.currentText())))
        if wnd["Class"].exec_loop() == QDialog.Accepted: #if something changed, reload the title
            self.fillList()        

    def accept(self):
        #update gui changes
        self.settings.UI_Settings.EnableKde = int(self.chkKDE.isChecked())
        self.settings.UI_Settings.EnableQScintilla = int(self.chkScintilla.isChecked())
        if self.rbOSD.isChecked():
            self.settings.UI_Settings.Notification = 0
        else:
            self.settings.UI_Settings.Notification = 1
        #update plugin changes
        self.settings.save()
        QDialog.accept(self)
