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

'''
Module for workig with plugins. To recap:
1. plugins should be stored in .p files inside ~/.pyqlogger/plugins/ dir or /usr/share/pyqlogger/plugins
2. internal plugins are made using static function called SimpleButton
3. each plugin MUST have one method getWidget()
4. it CAN have:
    * page - string attribute (on what tab page to put the button)
5. all plugins are loaded once and not reloaded. I may redo that later.
'''
__revision__ = "$Id$"
import os, sys
from glob import glob
from qt import QPixmap, QSize, QIconSet, QToolTip, QPushButton, SIGNAL,QPopupMenu, \
               QGridLayout, QPoint  

class ToolbarPlugin:
    ''' All plugins should inherit from this class '''
    def SimpleButton(parent, title, handler, page=None, image=None):
        tabpage = parent.getPage(page)
        button = QPushButton(tabpage)
        if image : 
            bi = QPixmap()
            bi.loadFromData(image, "PNG")
            button.setIconSet(QIconSet(bi))
            w = bi.width()+3
            h = bi.height()+3
            if w < 32:
                w = 32
            if h < 32:
                h = 32
            button.setMaximumSize(QSize(w, h))
        else:
            button.setText(title)
        QToolTip.add(button, title)
        parent.connect(button, SIGNAL("clicked()"), handler)
        button.show()
        p = ToolbarPlugin(parent)
        p.getWidget = lambda: button
    
    def getWidget(self):
        abstract
    
    def __init__(self, parent):
        self.parent = parent
    
    SimpleButton = staticmethod(SimpleButton)

class PluginFactory:
    plugins = [] # to store plugin classes
    buttons = {} # to store generated buttons per tabwidget

    def __init__(self, parent):
        self.dirs = [ '/usr/share/pyqlogger/plugins', os.path.expanduser("~/.pyqlogger/plugins/") ]
        sys.path += self.dirs
        self.parent = parent
        self.scan()
    
    def plugIsOk(self, plug):
        return bool( hasattr(plug, '__bases__') and  ToolbarPlugin in plug.__bases__  and hasattr(plug, 'getWidget') )
        
    def scan(self):
        path = os.path.join(self.dirs[0], '*.p')        
        path2 = os.path.join(self.dirs[1], '*.p')        
        for filename in glob(path) + glob(path2):
            if os.path.isfile(filename):
                lines = open(filename).read()
                g = globals()
                l = {} # locals
                try:
                    exec lines in g, l
                    for k, v in l.items():
                        # check if provided class can be applied
                        if self.plugIsOk(v):
                            # don't load duplicate plugins
                            if not [ aplugin for aplugin in self.plugins if str(v) in str(aplugin)]:
                                pl = v(self.parent)
                                self.plugins += [ pl ]
                                pl.getWidget()
                except Exception,  e:
                    print "Exception on loading plugin: " + str(e)

    def manualAdd(self, plugin):
        self.plugins += [ plugin ]
