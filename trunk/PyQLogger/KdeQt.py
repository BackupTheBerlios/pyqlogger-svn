## This file is part of PyQLogger.
##
## Copyright (c) 2004 Eli Yukelzon a.k.a Reflog &
##                    Xander Soldaat a.k.a. Mightor
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
##
__revision__ = "$Id: KdeQt.py 75 2004-12-19 14:12:35Z reflog $"

icon = \
    "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
    "\x49\x48\x44\x52\x00\x00\x00\x10\x00\x00\x00\x10" \
    "\x08\x06\x00\x00\x00\x1f\xf3\xff\x61\x00\x00\x01" \
    "\xb6\x49\x44\x41\x54\x38\x8d\x95\xd3\x3f\x48\x95" \
    "\x51\x18\xc7\xf1\xcf\x79\xef\xeb\x9f\x50\x44\x29" \
    "\x22\x22\xc9\xa8\xd6\x90\x08\x1a\x02\xb7\xf6\x68" \
    "\x68\x68\x68\xb8\x5c\xa2\xc1\x96\x96\x06\x21\x68" \
    "\x8d\x5a\x82\xb0\x28\x1a\x1a\x0a\x0a\x89\x36\x09" \
    "\xa4\x70\x6c\x34\x8a\x22\x0d\x6a\x28\x43\x6f\xbd" \
    "\x75\x49\xed\x7a\x7d\x4f\xc3\xab\x5e\x4d\xc9\xfa" \
    "\xc1\xc3\x39\xcf\x39\x3c\xdf\xe7\xfc\x79\x9e\x10" \
    "\x63\x04\xce\x86\x4c\xee\xdf\x14\x70\x3b\x76\x43" \
    "\x88\x31\x52\x0e\x51\x0b\xb1\xbd\x8b\xa4\xf4\xf7" \
    "\xe0\x98\x0b\x0b\x35\xea\x39\x77\x63\x48\x95\x43" \
    "\x66\xef\x21\x4e\x5d\xa3\xb7\x9f\xa4\x65\x0b\x40" \
    "\x83\xcf\x6f\x78\x72\x89\x72\xc8\xc4\x4a\x92\xc5" \
    "\x57\xa3\xf1\xbf\x35\x33\x15\xe3\x60\x47\x96\xea" \
    "\xea\x66\xdf\xd1\x66\x86\xaf\x1f\xc5\x5a\xb5\xb8" \
    "\xe7\xba\xcc\x84\xae\x1d\xf4\xf4\x16\xfe\xf6\x3e" \
    "\x76\x1d\x94\xda\xd6\x43\xda\x5e\x2c\x8e\xdf\xe4" \
    "\xe1\x90\xd0\x12\x36\x05\x88\x29\x83\x23\x1c\x38" \
    "\x46\x48\xe8\xdc\x29\x15\x92\xc2\x81\xb1\xeb\xec" \
    "\x3f\x2c\x56\xee\x6f\x04\x20\x3c\x1e\x62\x72\xbc" \
    "\x00\x40\xda\x2a\x6d\xe2\xd1\x77\x84\x97\x63\xc2" \
    "\xc8\x45\x92\x4d\x08\xaf\x9f\x73\xfc\x7c\xd3\xcf" \
    "\x73\x45\xea\xb8\x5c\x00\xa7\x87\x39\x71\x59\x94" \
    "\x88\x8b\x75\xb1\xb1\xc6\x16\xeb\x2c\xcd\xf1\xe2" \
    "\x01\x2b\xb5\x33\xff\x63\xe5\x04\xcb\x6a\xeb\x60" \
    "\xa0\x22\x0c\x54\x36\x66\x87\x7b\x15\x7a\x76\x13" \
    "\x02\xf5\x9f\xcc\x4e\xfe\x01\xd8\x4a\x67\xee\x14" \
    "\xe3\x42\x8d\xa7\x57\xa8\x4e\x4b\x85\xd0\x7c\xc4" \
    "\xcd\x34\x33\xc5\xe8\x55\xb1\xfa\x81\x04\x79\x43" \
    "\x98\x7d\xcf\xf4\x14\x25\x52\xf3\xdf\x69\xfc\x22" \
    "\x6d\xdb\x18\x3c\x97\x31\x7c\x92\xb7\x13\xc2\x4a" \
    "\x81\x06\x05\xa8\x54\xcc\x13\xd5\x2f\x3c\xbb\xc1" \
    "\x52\x9d\xbc\xd1\xb4\x85\x1a\x8f\x2e\x30\x39\x41" \
    "\x27\xda\x96\xad\x15\xa9\xd5\x6f\x2e\x9a\xe9\x5c" \
    "\x12\xed\xe9\xa7\xb4\xa6\x0f\xe6\xbe\xf1\xe9\x9d" \
    "\xbf\xbe\xd2\xad\x18\xc2\x6a\x3b\x97\x43\xb6\x6e" \
    "\x33\xd8\x2a\xb8\x1b\x7e\x03\x55\x32\xd0\x4e\xb6" \
    "\x8a\x95\xb5\x00\x00\x00\x00\x49\x45\x4e\x44\xae" \
    "\x42\x60\x82"

try:
    from kdecore import KApplication, KCmdLineArgs, KAboutData, KIconLoader,KLocale
    import sys
    from qt import QToolTip,QPixmap
    from kdeui import KSystemTray
    from khtml import KHTMLPart
    from dcopexport import DCOPExObj

    def isKde():
        return 1

    def setPreviewWidget(parent):
        parent.sourcePreview.hide() # hide default
        parent.vp = KHTMLPart (parent.Preview, "HTMLPart", parent.Preview) #create
        parent.sourcePreview = parent.vp.view() # re-route
        parent.Preview.layout().addWidget(parent.sourcePreview) # show new

    def setPreview(parent, text):
        parent.vp.begin()
        parent.vp.write(text)
        parent.vp.end()

    def prepareCommandLine(): 
        args = KCmdLineArgs.parsedArgs()
        return args.isSet ( "statusbar") or args.isSet ( "s")
        
    def setupKDE(app, wnd, settings):
        try:
            icons = KIconLoader ()
            systray = KSystemTray (wnd["Class"])
            p = QPixmap()
            p.loadFromData(icon)
            systray.setPixmap (p)
            QToolTip.add(systray, "PyQLogger - Blogger GUI")
            systray.show ()
        except Exception, inst:
            sys.stderr.write("setupKDE: cannot set tray, exception: %s\n" % inst)
            
        dcop  = app.dcopClient ()
        if dcop:
            dcop.registerAs('pyqlogger')
            PQDCOP(wnd["Impl"])
        else:
            print "setupKDE: dcop is None"

    class PQDCOP (DCOPExObj):
        def __init__ (self, parent, dcopid = 'PyQLogger'):
            DCOPExObj.__init__ (self, dcopid)
            self.parent = parent
            self.addMethod ('void newpost()', self.parent.btnNewPost_clicked)
            self.addMethod ('void preview()', self.parent.btnPreview_clicked)
            self.addMethod ('QString getPostTitle()', self.getPostTitle)
            self.addMethod ('QString getPostText()', self.getPostText)
            self.addMethod ('void setPostTitle(QString)', self.setPostTitle)
            self.addMethod ('void setPostText(QStringList)', self.setPostText)

        def setPostText(self, text):
            self.parent.sourceEditor.setText(text)
        def setPostTitle(self, text):
            self.parent.editPostTitle.setText(text)
        def getPostText(self):
            return self.parent.sourceEditor.text()
        def getPostTitle(self):
            return self.parent.editPostTitle.text()
   
    class KQApplication(KApplication):
        def __init__(self, argv, opts):
            KLocale.setMainCatalogue("kdelibs") 
            if not '--caption' in argv:
                argv += [ '--caption','PyQLogger' ]
                sysargv = argv[:]
                from pyqlogger import VERSION
                aboutData = KAboutData("pyqlogger", "PyQLogger", VERSION,  
                                   "Blogger GUI", KAboutData.License_GPL, 
                       "(C) 2004, Eli Yukelzon", "","http://pyqlogger.berlios.de","")
                aboutData.addAuthor("Eli Yukelzon a.k.a Reflog",  "",
                                "reflog@gmail.com");
                aboutData.addAuthor("Xander Soldaat a.k.a Mightor", "", 
                                "mightor@gmail.com");
                try:
                    options =  [
                       ("s", "Status bar (default = disabled)"),
                       ("statusbar", "Status bar (default = disabled)")
                    ]
                    KCmdLineArgs.init( argv, aboutData)
                    KCmdLineArgs.addCmdLineOptions( options )
                except TypeError:
                    KCmdLineArgs.init(sysargv, sysargv[0], '', '')
                if opts:
                    KCmdLineArgs.addCmdLineOptions(opts)
                KApplication.__init__(self)

except ImportError,e:
    def isKde():
        return 0    
    def setPreviewWidget(parent):
        pass
    def setPreview(parent, text):
        parent.sourcePreview.setText(text)

    def prepareCommandLine():
        import optparse
        parser = optparse.OptionParser(usage="%prog [options]")
        parser.add_option("--statusbar", "-s",
                      action = "store_true",
              help = "Status bar (default = disabled)")
        (opt, arg) = parser.parse_args()
        stat = opt.statusbar
        return stat == True
        
    def setupKDE(app, wnd):
        pass

    from qt import QApplication
    class KQApplication(QApplication):
        def __init__(self, argv, opts):
            QApplication.__init__(self, argv)

try:
    from qt import SIGNAL, QFont
    from qtext import QextScintilla, QextScintillaLexerHTML

    def setMonospaced(editor):
        try:
            rangeLow = range(editor.STYLE_DEFAULT)
        except AttributeError:
            rangeLow = range(32)
        try:
            rangeHigh = range(editor.STYLE_LASTPREDEFINED + 1, editor.STYLE_MAX + 1)
        except AttributeError:
            rangeHigh = range(40, 128)
        try:
            font = QFont('Bitstream Vera Sans,11,-1,5,50,0,0,0,0,0')
        except:
            return # no font. bail.
        for style in rangeLow + rangeHigh:
            editor.SendScintilla(QextScintilla.SCI_STYLESETFONT, style, font.family().latin1())
            editor.SendScintilla(QextScintilla.SCI_STYLESETSIZE, style, font.pointSize())


    def setEditWidget(parent):
        parent.sourceEditor.hide()
        parent.sourceEditor = QextScintilla(parent.Source)
        parent.sourceEditor.setUtf8(1)
        parent.sourceEditor.SendScintilla(QextScintilla.SCI_SETWRAPMODE, QextScintilla.SC_WRAP_WORD)
        parent.sourceEditor.setLexer(QextScintillaLexerHTML(parent))
        setMonospaced(parent.sourceEditor)
        parent.Source.layout().addWidget(parent.sourceEditor)
        parent.connect(parent.sourceEditor, SIGNAL("textChanged()"), parent.sourceEditor_textChanged)

except ImportError, e:
    from qt import Qt
    from SyntaxHighlight import HTMLSyntax    
    def setEditWidget(parent): 
        parent.sh = HTMLSyntax(parent.sourceEditor)
        parent.sourceEditor.setTextFormat(Qt.PlainText)

