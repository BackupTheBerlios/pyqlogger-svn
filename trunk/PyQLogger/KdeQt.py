__revision__ = "$Id: KdeQt.py 75 2004-12-19 14:12:35Z reflog $"

try:
    from kdecore import KApplication, KCmdLineArgs, KAboutData, KIconLoader
    import sys, os
    from qt import QToolTip
    from kdeui import KMainWindow,  KSystemTray , KHelpMenu, KAboutApplication
    from khtml import KHTMLPart, KHTMLView
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
        
    def setupKDE(app, wnd):
        try:
            icons = KIconLoader ()
            systray = KSystemTray (wnd)
            systray.setPixmap (icons.loadIcon("kedit", 1))
            QToolTip.add(systray, "PyQLogger - Blogger GUI")
            systray.show ()
        except Exception, inst:
            sys.stderr.write("setupKDE: cannot set tray, exception: %s\n" % inst)
            
        dcop  = app.dcopClient ()
        if dcop:
            dcop.registerAs('pyqlogger')
            PQDCOP(wnd)
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
    def isKde(): return 0    
    def setPreviewWidget(parent): pass
    def setPreview(parent,text): parent.sourcePreview.setText(text)
    def prepareCommandLine():
        import optparse
        parser = optparse.OptionParser(usage="%prog [options]")
        parser.add_option("--statusbar","-s",
	                  action="store_true",
			  help="Status bar (default = disabled)")
        (opt,arg) = parser.parse_args()
        stat = opt.statusbar
        return stat == True
        
    def setupKDE(app,wnd): pass
    from qt import QApplication
    class KQApplication(QApplication):
        def __init__(self, argv, opts):
            QApplication.__init__(self, argv)

try:
    from qt import SIGNAL,QFont
    from qtext import QextScintilla,QextScintillaLexerHTML
    def setMonospaced(e):
        try:
            rangeLow = range(e.STYLE_DEFAULT)
        except AttributeError:
            rangeLow = range(32)
        try:
            rangeHigh = range(e.STYLE_LASTPREDEFINED + 1,e.STYLE_MAX + 1)
        except AttributeError:
            rangeHigh = range(40, 128)
        try:
            f = QFont('Bitstream Vera Sans,11,-1,5,50,0,0,0,0,0')
        except:
            return # no font. bail.
        for style in rangeLow + rangeHigh:
            e.SendScintilla(QextScintilla.SCI_STYLESETFONT,style,f.family().latin1())
            e.SendScintilla(QextScintilla.SCI_STYLESETSIZE,style,f.pointSize())


    def setEditWidget(parent):
        parent.sourceEditor.hide()
        parent.sourceEditor = QextScintilla(parent.Source)
        parent.sourceEditor.setUtf8(1)
        parent.sourceEditor.SendScintilla(QextScintilla.SCI_SETWRAPMODE, QextScintilla.SC_WRAP_WORD)
        parent.sourceEditor.setLexer(QextScintillaLexerHTML(parent))
        setMonospaced(parent.sourceEditor)
        parent.Source.layout().addWidget(parent.sourceEditor)
        parent.connect(parent.sourceEditor,SIGNAL("textChanged()"),parent.sourceEditor_textChanged)

except ImportError ,e:
    def setEditWidget(parent): pass    

