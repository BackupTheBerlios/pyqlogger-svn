from PyQLogger.Settings import Settings
from AccountSettingsDialog import AccountSettingsDialog
from qt import QListBoxPixmap,QPixmap,QListBoxText,QDialog,\
               QMessageBox,QListView,QListViewItem

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
    
    def statusPixmap(self, plugin):
        if plugin.Data.Enabled and plugin.Data.Enabled == 1:
            return self.btnLoad.iconSet().pixmap()
        return self.btnUnload.iconSet().pixmap()
        
    def fillPlugins(self):
        self.lvPlugins.clear()
        self.li2pl = {}
        First = True
        for plug in self.manager.Plugins:
            li = QListViewItem(self.lvPlugins,str(plug.Name), plug.description())
            li.setPixmap(0,self.statusPixmap(plug))
            self.li2pl[li] = plug
            if First:
                li.setSelected(True)
                self.lvPlugins_selectionChanged(li)
                First = False
                
    def lvPlugins_selectionChanged(self, listItem):
        en = bool(self.li2pl[listItem].Data.Enabled)
        self.btnLoad.setEnabled(not en)
        self.btnUnload.setEnabled(en)
    
    def btnLoad_clicked(self, val = 1):
        li = self.lvPlugins.selectedItem()
        pl = self.li2pl [ li ]
        pl.Data.Enabled = val
        li.setPixmap(0,self.statusPixmap(pl))
        self.lvPlugins_selectionChanged(li)
        
    def btnUnload_clicked(self):
        self.btnLoad_clicked(0)
        
    def init(self,settings,forms,manager):
        self.settings = settings
        self.manager = manager
        self.forms = forms
        # add accounts
        self.fillList()
        # add plugins
        self.fillPlugins()
        # set gui settings
        self.chkKDE.setChecked(bool(settings.UI_Settings.EnableKde))
        self.chkDCOP.setChecked(bool(settings.UI_Settings.EnableDCOP))
        self.chkTray.setChecked(bool(settings.UI_Settings.EnableTray))
        self.chkKDE_stateChanged(0)
        self.chkSpellEnable.setChecked(bool(settings.Speller.Enabled))
        self.edtSpellPrefix.setText(str(settings.Speller.Prefix))
        self.edtSpellLanguage.setText(str(settings.Speller.Language))
        self.chkSpellEnable_stateChanged(0)
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

    def btnConfigPlug_clicked(self):
        wnd = self.forms["PluginSettings"]
        pl = self.li2pl [ self.lvPlugins.selectedItem() ]
        wnd["Impl"].init(self.manager,pl)
        wnd["Class"].exec_loop()
        

    def btnEditAccount_clicked(self):
        wnd = self.forms["AccountSettings"]
        wnd["Impl"].init(self.settings.accountByName(str(self.lbAccounts.currentText())))
        if wnd["Class"].exec_loop() == QDialog.Accepted: #if something changed, reload the title
            self.fillList()        

    def chkKDE_stateChanged(self, ins):
        self.chkTray.setEnabled(self.chkKDE.isChecked())
        self.chkDCOP.setEnabled(self.chkKDE.isChecked())

    def chkSpellEnable_stateChanged(self, ins):
        self.edtSpellPrefix.setEnabled(self.chkSpellEnable.isChecked())
        self.edtSpellLanguage.setEnabled(self.chkSpellEnable.isChecked())
        
    def accept(self):
        #update gui changes
        self.settings.UI_Settings.EnableKde = int(self.chkKDE.isChecked())
        self.settings.Speller.Enables = int(self.chkSpellEnable.isChecked())
        self.settings.Speller.Prefix = self.edtSpellPrefix.text()
        self.settings.Speller.Language = self.edtSpellLanguage.text()
        self.settings.UI_Settings.EnableTray = int(self.chkTray.isChecked())
        self.settings.UI_Settings.EnableDCOP = int(self.chkDCOP.isChecked())
        self.settings.UI_Settings.EnableQScintilla = int(self.chkScintilla.isChecked())
        if self.rbOSD.isChecked():
            self.settings.UI_Settings.Notification = 0
        else:
            self.settings.UI_Settings.Notification = 1
        #update plugin changes
        self.settings.save()
        self.manager.save()
        QDialog.accept(self)
