
class TemplatePlugin(EventPlugin):
    EventType = EventType.TEXTCHANGED
    Name = "Templates"
    Info = "Press Ctrl-J in the editor to paste the templates"
    def usersel(self, name, idx):
        for (tpl,value) in self.hash.items():
            if tpl == name:
                self.parent.sourceEditor.insert( value )
                break
                
    def defaultOptions(self):
        return [ Option(Type="DoubleList",Name="Templates",Value='') ]
    
    def handle(self, parent, evt):
        self.parent = parent
	import pickle
        self.hash = pickle.loads(str(self.Data.Options[0].Value)) 
        if evt.key() == Qt.Key_J and  (evt.state() & Qt.ControlButton):
            words = [tpl for tpl in self.hash.keys() ]
            if words:
                words.sort()                
                sci = parent.sourceEditor
                parent.connect(sci, SIGNAL("SCN_USERLISTSELECTION(const char *, int)"), self.usersel)
                sci.SendScintilla(sci.SCI_USERLISTSHOW, 1, str(" ".join(words)))           
                return True        
        return False
