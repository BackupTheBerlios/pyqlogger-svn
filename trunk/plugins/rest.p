class reSTPlugin(ToolbarPlugin):
    Name  = "reST"
    def on_click(self):
        text = str(self.parent.sourceEditor.selectedText())
        self.parent.sourceEditor.removeSelectedText()
        line, index = self.parent.sourceEditor.getCursorPosition()
        from docutils.core import publish_parts
        res = publish_parts(text,writer_name="html4css1")
        if res:
            self.parent.sourceEditor.insertAt(res["body"], line, index)	

    def getWidget(self, parent):
        self.parent = parent
        page = parent.getPage("Plugins")
        button = QPushButton(page)
        button.setText("reST")
        QToolTip.add(button,"Convert the text through reST.")
        w = 52
        h = 32
        button.setMaximumSize(QSize(w,h))
        parent.connect(button,SIGNAL("clicked()"),self.on_click)
        button.hide()
        return button
