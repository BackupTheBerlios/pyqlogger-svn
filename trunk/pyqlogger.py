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
from PyQLogger import KdeQt,qt_ui_loader
from PyQLogger import Settings
import sys

try:
    from qt import QObject, SIGNAL, SLOT,QSplashScreen, QPixmap, qApp , Qt,QDialog,QMessageBox
except ImportError, e:
    print """Could not locate the PyQt module.  Please make sure that
you have installed PyQt for the version of Python that you are running."""
    sys.exit(1)

VERSION = '2.0'
__revision__ = "$Id$"

__FORMS__ = {}

alignflag = Qt.AlignBottom

def load_forms(splash):
    splash.message( "Loading form: Main",alignflag )
    qApp.processEvents()
    from PyQLogger.Dialogs import MainDialog
    wnd = MainDialog.MainDialog()
    wnd_c = qt_ui_loader.create( 'UI/maindialog.ui', wnd,None,True )
    __FORMS__["Main"] = { "Class": wnd_c , "Impl": wnd }
    splash.message( "Loading form: Login" ,alignflag)
    qApp.processEvents()
    from PyQLogger.Dialogs import LoginDialog
    wnd = LoginDialog.LoginDialog()
    wnd_c = qt_ui_loader.create( 'UI/logindialog.ui', wnd,None,True )
    __FORMS__["Login"] = { "Class": wnd_c , "Impl": wnd }
    splash.message( "Loading form: Settings",alignflag )
    qApp.processEvents();
    from PyQLogger.Dialogs import SettingsDialog
    wnd = SettingsDialog.SettingsDialog()
    wnd_c = qt_ui_loader.create( 'UI/settingsdialog.ui', wnd,None,True )
    __FORMS__["Settings"] = { "Class": wnd_c , "Impl": wnd }
    splash.message( "Loading form: Account Settings",alignflag )
    qApp.processEvents();
    from PyQLogger.Dialogs import AccountSettingsDialog
    wnd = AccountSettingsDialog.AccountSettingsDialog()
    wnd_c = qt_ui_loader.create( 'UI/accountsettingsdialog.ui', wnd,None,True )
    __FORMS__["AccountSettings"] = { "Class": wnd_c , "Impl": wnd }
    splash.message( "Loading form: Image Insert",alignflag )
    qApp.processEvents();
    from PyQLogger.Dialogs import ImageDialog
    wnd = ImageDialog.ImageDialog()
    wnd_c = qt_ui_loader.create( 'UI/imagedialog.ui', wnd,None,True )
    __FORMS__["Image"] = { "Class": wnd_c , "Impl": wnd }
    splash.message( "Loading form: Url Insert",alignflag )
    qApp.processEvents();
    from PyQLogger.Dialogs import UrlDialog
    wnd = UrlDialog.UrlDialog()
    wnd_c = qt_ui_loader.create( 'UI/urldialog.ui', wnd,None,True )
    __FORMS__["Url"] = { "Class": wnd_c , "Impl": wnd }



def main():
    app =  KdeQt.KQApplication(sys.argv, None)
    stat = KdeQt.prepareCommandLine()    
    QObject.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))
    pixmap = QPixmap( "splash.png" )
    splash = QSplashScreen( pixmap )
    splash.show()
    splash.message( "Loading forms...",alignflag )
    qApp.processEvents();
    load_forms(splash)
    splash.message( "Loading settings..." ,alignflag)
    qApp.processEvents();
    settings = Settings.Settings.load()
    acc = None
    if not settings.AutoLogin: # check if we don't have auto login info
        wnd = __FORMS__["Login"]
        wnd["Impl"].init(settings,__FORMS__)
        if wnd["Class"].exec_loop() == QDialog.Accepted:
            acc = wnd["Impl"].acc
    else:
        acc = settings.accountByName(settings.AutoLogin)
        
    if not acc:
        QMessageBox.critical(None,"No Accounts!","""Program cannot work without a selected account!""")
    else:
        wnd = __FORMS__["Main"]
        wnd["Impl"].init()
        app.setMainWidget(wnd["Class"])
        KdeQt.setupKDE(app, wnd, settings)
        wnd["Class"].show()
        splash.finish(wnd["Class"])
        del splash
        res = app.exec_loop()

if __name__ == '__main__':
    main()

