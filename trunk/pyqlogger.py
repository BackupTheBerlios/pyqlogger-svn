#! /usr/bin/python
## This file is part of PyQLogger.
##
## Copyright (c) 2004 Eli Yukelzon a.k.a Reflog
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
from PyQLogger import UI,qt_ui_loader
from PyQLogger.UI import MyQextScintilla
from PyQLogger import Settings
from PyQLogger.Plugins.Manager import Manager

import sys,os

try:
    import psyco
    psyco.profile()
except:
    print 'Psyco not found, ignoring it (though it''s highly recommended to install it!)'

try:
    from qt import QObject, SIGNAL, SLOT,QSplashScreen, \
                   QPixmap, qApp, Qt, QDialog, QMessageBox
except ImportError, e:
    print """Could not locate the PyQt module.  Please make sure that
you have installed PyQt for the version of Python that you are running."""
    sys.exit(1)

VERSION = '2.0'
__revision__ = "$Id$"

__FORMS__ = {}

alignflag = Qt.AlignBottom

def load_forms(splash, app, settings):
    splash.message( "Loading form: Main",alignflag )
    qApp.processEvents()
    from PyQLogger.Dialogs import MainDialog
    wnd = MainDialog.MainDialog()
    wnd_c = qt_ui_loader.create( 'UI/maindialog.ui', wnd,None,True )
    wnd_c.closeEvent = wnd.closeEvent
    __FORMS__["Main"] = { "Class": wnd_c , "Impl": wnd }
    wnd.init_ui(settings, __FORMS__)
    UI.API.setupTray(app, __FORMS__["Main"])
    UI.API.setupDCOP(app, __FORMS__["Main"])
    splash.message( "Loading form: Login" ,alignflag)
    qApp.processEvents()
    from PyQLogger.Dialogs import LoginDialog
    wnd = LoginDialog.LoginDialog()
    wnd_c = qt_ui_loader.create( 'UI/logindialog.ui', wnd,None,True )
    __FORMS__["Login"] = { "Class": wnd_c , "Impl": wnd }
    splash.message( "Loading form: Settings",alignflag )
    qApp.processEvents()
    from PyQLogger.Dialogs import SettingsDialog
    wnd = SettingsDialog.SettingsDialog()
    wnd_c = qt_ui_loader.create( 'UI/settingsdialog.ui', wnd,None,True )
    __FORMS__["Settings"] = { "Class": wnd_c , "Impl": wnd }
    splash.message( "Loading form: Account Settings",alignflag )
    qApp.processEvents()
    from PyQLogger.Dialogs import AccountSettingsDialog
    wnd = AccountSettingsDialog.AccountSettingsDialog()
    wnd_c = qt_ui_loader.create( 'UI/accountsettingsdialog.ui', wnd,None,True )
    wnd.init_ui()
    __FORMS__["AccountSettings"] = { "Class": wnd_c , "Impl": wnd }
    splash.message( "Loading form: Image Insert",alignflag )
    qApp.processEvents()
    from PyQLogger.Dialogs import ImageDialog
    wnd = ImageDialog.ImageDialog()
    wnd_c = qt_ui_loader.create( 'UI/imagedialog.ui', wnd,None,True )
    __FORMS__["Image"] = { "Class": wnd_c , "Impl": wnd }
    splash.message( "Loading form: Url Insert",alignflag )
    qApp.processEvents()
    from PyQLogger.Dialogs import UrlDialog
    wnd = UrlDialog.UrlDialog()
    wnd_c = qt_ui_loader.create( 'UI/urldialog.ui', wnd,None,True )
    __FORMS__["Url"] = { "Class": wnd_c , "Impl": wnd }
    splash.message( "Loading form: Plugin settings",alignflag )
    qApp.processEvents();
    from PyQLogger.Dialogs import PluginSettingsDialog
    wnd = PluginSettingsDialog.PluginSettingsDialog()
    wnd_c = qt_ui_loader.create( 'UI/pluginsettingsdialog.ui', wnd,None,True )
    __FORMS__["PluginSettings"] = { "Class": wnd_c , "Impl": wnd }
    splash.message( "Loading form: Template settings",alignflag )
    qApp.processEvents()
    wnd = QDialog()
    wnd_c = qt_ui_loader.create( 'UI/templatesettingsdialog.ui', wnd, None,True )
    __FORMS__["TemplateSettings"] = { "Class": wnd_c , "Impl": wnd }

def main():
    if not os.path.exists(os.path.expanduser("~/.pyqlogger")):
        os.mkdir(os.path.expanduser("~/.pyqlogger"))    
    settings = Settings.Settings.load()
    UI.prepareModule(settings)
    app =  UI.API.KQApplication(sys.argv, None)
    stat = UI.API.prepareCommandLine()    
    pixmap = QPixmap( "splash.png" )
    splash = QSplashScreen( pixmap )
    splash.show()
    splash.message( "Loading forms...",alignflag )
    qApp.processEvents()
    load_forms(splash,app,settings)
    splash.message( "Loading plugins...",alignflag )
    qApp.processEvents()
    manager = Manager.load(__FORMS__["Main"]["Impl"])
    del splash
    acc = None
    pwd = None
    if settings.AutoLogin: # check if we have auto login info
        acc = settings.accountByName(settings.AutoLogin)
        pwd = acc.Password

    while True:
        if not acc:
            wnd = __FORMS__["Login"]
            if wnd["Impl"].init(settings,__FORMS__,manager):
                if wnd["Class"].exec_loop() == QDialog.Accepted:
                    acc = wnd["Impl"].acc
                    pwd = str(wnd["Impl"].edtPassword.text())
        if not acc or not pwd:
            break
        else:
            (acc.Password,oldpwd) = (pwd,acc.Password)            
            acc.init()
            logres = acc.login()
            acc.Password = oldpwd
            if not logres:
                QMessageBox.warning(None,"Failed!","""Cannot login!""")
                acc = None
            else:
                wnd = __FORMS__["Main"]
                acc.init()
                wnd["Impl"].init(settings,__FORMS__, acc, pwd,\
                                 manager)
                app.setMainWidget(wnd["Class"])
                wnd["Class"].show()
                #splash.finish(wnd["Class"])
                app.exec_loop()
                if wnd["Impl"].reload:
                    acc = None
                else:
                    break



if __name__ == '__main__':
    main()

