'''
Module for workig with plugins. To recap:
1. plugins should be stored in .p files inside ~/.pyqlogger/plugins/ dir or /usr/share/pyqlogger/plugins
2. internal plugins are made using static function called SimpleButton
3. each plugin MUST have one method getWidget()
4. it CAN have:
    * page - string attribute (on what tab page to put the button)
5. all plugins are loaded once and not reloaded. I may redo that later.
'''
import os,sys
from glob import glob
from qt import *


class ToolbarPlugin:
    ''' All plugins should inherit from this class '''
    def SimpleButton(parent,title,handler,page=None,image=None):
        tabpage = parent.getPage(page)
        button = QPushButton(tabpage)
        if image : 
            bi = QPixmap()
            bi.loadFromData(image,"PNG")
            button.setIconSet(QIconSet(bi))
            w = bi.width()+3
            h = bi.height()+3
            if w < 32:
                w = 32
            if h < 32:
                h = 32
            button.setMaximumSize(QSize(w,h))
        else:
            button.setText(title)
    #           button.setMaximumSize(QSize(defw,defh))
        QToolTip.add(button,title)
        parent.connect(button,SIGNAL("clicked()"),handler)
        button.show()
        p = ToolbarPlugin(parent)
        p.getWidget = lambda: button
    
    def getWidget(self):
        abstract
    
    def __init__(self,parent):
        self.parent = parent
    
    SimpleButton = staticmethod(SimpleButton)

class PluginFactory:
    plugins = [] # to store plugin classes
    buttons = {} # to store generated buttons per tabwidget

    def __init__(self,parent):
        self.dirs = [ '/usr/share/pyqlogger/plugins', os.path.expanduser("~/.pyqlogger/plugins/") ]
        sys.path += self.dirs
        self.parent = parent
        self.scan()
    
    def plugIsOk(self,plug):
        return bool( hasattr(plug,'__bases__') and  ToolbarPlugin in plug.__bases__          and hasattr(plug,'getWidget') )
        
    def scan(self):
        path = os.path.join(self.dirs[0], '*.p')        
        path2 = os.path.join(self.dirs[1], '*.p')        
        for filename in glob(path)+glob(path2):
            if os.path.isfile(filename):
                lines = open(filename).read()
                g = globals()
                l = {} # locals
                try:
                    exec lines in g,l
                    for k,v in l.items():
                        # check if provided class can be applied
                        if self.plugIsOk(v):
                            # don't load duplicate plugins
                            if not filter(lambda x: str(v) in str(x) , self.plugins):
                                pl = v(self.parent)
                                self.plugins += [ pl ]
                                pl.getWidget()
                except Exception,  e:
                    print str(e)
                    pass

    def manualAdd(self,plugin):
        self.plugins += [ plugin ]
