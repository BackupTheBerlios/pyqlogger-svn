from PyQLogger.Settings import Settings
from AccountSettingsDialog import AccountSettingsDialog
from qt import QListBoxPixmap,QPixmap,QListBoxText,QDialog

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
            self.btnAddAccount.setEnabled(False)
            self.btnDelAccount.setEnabled(False)
        
    def init(self,settings,forms):
        self.settings = settings
        self.forms = forms
        #add accounts
        self.fillList()
        # set gui settings
        self.chkKDE.setChecked(settings.UI_Settings.EnableKde)
        self.chkScintilla.setChecked(settings.UI_Settings.EnableQScintilla)
        if settings.UI_Settings.Notification == 0:
            self.rbOSD.setChecked(True)
        else:
            self.rbStatus.setChecked(True)

    def btnEditAccount_clicked(self):
        wnd = forms["AccountSettingsDialog"]
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
        QDialog.accept(self)
