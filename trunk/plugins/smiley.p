import ToolBarManager
class Smiley_Plugin(ToolBarManager.ToolbarPlugin):
    def on_click(self):
        if self.frame.isHidden(): 
	    pos = self.parent.sender().cursor().pos()-self.parent.pos()
	    self.frame.move(pos)
	    self.frame.show()
	else: 
	    self.frame.hide()

    def on_smile_click(self):
        self.frame.hide()
        for sm in self.smiles:
	    if sm["button"] != self.parent.sender(): continue
            self = qApp.mainWidget()
	    line, index = self.sourceEditor.getCursorPosition()
	    ku = """<img src="%s" alt="%s" width="%d" height="%d" >"""%(sm["url"],sm["variants"][0],sm["pixmap"].width(),sm["pixmap"].height())
	    self.sourceEditor.insertAt(ku, line, index)
	    self.sourceEditor.setCursorPosition(line,index+len(ku))
	    self.sourceEditor.setFocus()
	    return
	
    def getWidget(self):
        page = self.parent.getPage("Plugins")
        button = QPushButton("smile!",page)
        import os,pickle
        self.smiles = pickle.load(open(os.path.expanduser("~/.pyqlogger/plugins/")+"smiley.theme"))
	self.frame = QFrame(self.parent)
	self.frame.setFrameShape(QFrame.StyledPanel)
	self.frame.setFrameShadow(QFrame.Raised)
	self.frame.hide()
	self.framelayout = QGridLayout(self.frame)
	r = c = 0
        for sm in self.smiles:
	    if c > 5:
	        c = 0
		r += 1
            bi = QPixmap()
            bi.loadFromData(pickle.loads(sm["image"]),"PNG")
            b = QPushButton(self.frame)
	    self.framelayout.addWidget(b,r,c)
	    b.setPixmap(bi)
	    QToolTip.add(b,sm["variants"][0])
	    self.parent.connect(b,SIGNAL("clicked()"),self.on_smile_click)
	    sm["button"] = b
	    sm["pixmap"] = bi
	    c += 1

	if len(self.smiles)>0:
            qs = QSize(self.smiles[0]["pixmap"].width()*8,self.smiles[0]["pixmap"].height()*(r+3))
	    self.frame.resize(self.frame.minimumSizeHint())
            button.setPixmap(self.smiles[0]["pixmap"])	    
	QToolTip.add(button,"Show list of available smileys")
	w = 32
	h = 32
	button.setMaximumSize(QSize(w,h))
        self.parent.connect(button,SIGNAL("clicked()"),self.on_click)
        button.show()