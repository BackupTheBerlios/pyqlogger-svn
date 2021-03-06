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

from EaseXML import XMLObject,ListNode
from Plugin import Plugin , PluginData, Option, InternalPlugin
from EventPlugin import EventPlugin, EventType
from ToolbarPlugin import ToolbarPlugin
from MenuPlugin import MenuPlugin
from ServiceGUIPlugin import ServiceGUIPlugin
from PyQLogger.ToolBar import initToolbar
from qt import *
__revision__ = "$Id$"
def import_plugin_classes():
    globals()["Plugin"] = Plugin
    globals()["EventPlugin"] = EventPlugin
    globals()["MenuPlugin"] = MenuPlugin
    globals()["ToolbarPlugin"] = ToolbarPlugin
    globals()["ServiceGUIPlugin"] = ServiceGUIPlugin
    
import os,sys
from glob import glob


def importClasses(folders, parent):
    """ 
    Function to traverse each forder in the 'folders' list and
    get all files with .p extension and try to compile them.
    If possible - import into the list of plugin classes
    """
    import_plugin_classes()
    
    PluginClasses = []
    for mask in [ os.path.join(path, '*.p') for path in folders ]:
        for filename in glob(mask):
            if os.path.isfile(filename):
                try:
                    lines = open(filename).read()
                    g = globals()
                    l = {} # locals
                    exec lines in g, l
                    for kName, kClass in l.items():
                        # check if provided class can be applied
                        if issubclass(kClass, Plugin) and len(kName)>7 and kName[-6:] == 'Plugin':
                            # don't load duplicate plugins
                            if not [ aplugin for aplugin in PluginClasses if kName == aplugin.__name__]:
                                PluginClasses += [ kClass ]
                                g[ kName ] = kClass
                        else:
                            parent.log.warning("Cannot load plugin: %s is a bad plugin name or unkown parent class!" % kName,exc_info=1)
                except Exception,  e:
                    parent.log.error("Exception on loading plugin",exc_info=1)
    return PluginClasses

class Manager(XMLObject):
    """ Plugin manager for keeping the list, loading/unloading and etc """
    PluginData = ListNode('PluginData') # data hashes
    Plugins = [] # instances
    Plugin2Data = {} # lookup hash
    
    def init(self, parent, PluginClasses):
        """ 
        most of the plugins are already initialized by now,
        so only add the new ones
        """
        self.parent = parent
        PluginClasses += initToolbar(self)
        changed = False
        for plug in PluginClasses:
            exists = [ p for p in self.PluginData if p.Class == plug.__name__ ]
            inst = plug()
            if not exists: # no data created yet. make one    
                changed = True
                inst.Data = PluginData(Class=plug.__name__,
                                       Options=inst.defaultOptions())
                if issubclass(plug, InternalPlugin):
                    inst.Data.Enabled = 1
                self.PluginData += [ inst.Data ]
            else: # use existing data
                inst.Data = exists[0]
            parent.log.debug("Adding (%s) plugin"%inst.Name,exc_info=1)
            self.Plugins += [ inst ] # add to the list            
            self.Plugin2Data [ inst ] = inst.Data # link for lookup
        if changed:
            self.save()
            
    def fillToolbar(self):
        """ Fills the panel with plugins of ToolbarPlugin type """
        if self.toolbarNeeded:
            for plug in self.Plugins:
                if issubclass(plug.__class__,ToolbarPlugin) and plug.Data.Enabled == 1 :
                    widget = plug.getWidget(self.parent)
                    if widget:
                        widget.show()
                    else:
                        print "Failed to initialize plugin: "+plug.Name
        self.toolbarNeeded = False
    
    def handleEvent(self, eventType, data):
        """ For supplied event, execute all plugins handling it """
        for plug in self.Plugins:
            if issubclass(plug.__class__, EventPlugin) and plug.Data.Enabled == 1 \
               and plug.EventType == eventType:
                if plug.handle(self.parent, data):
                    return True
        return False
        
    def fillMenu(self, parentMenu):
        """ Fills the editor menu with plugins of MenuPlugin type """
        for plug in self.Plugins:
            if issubclass(plug.__class__,MenuPlugin) and plug.Data.Enabled == 1 :
                plug.getMenu(self.parent, parentMenu)
        
    def load(parent):
        """ Create a fresh copy of initialized Manager class """
        paths = ["/home/reflog/.pyqlogger/plugins","/usr/share/pyqlogger/plugins"]
        l = importClasses(paths, parent)
        sys.path += paths
        file = os.path.expanduser("~")+"/.pyqlogger/plugins.xml"
        if os.path.exists(file):
            try:
                m = XMLObject.instanceFromXml(open(file).read())
            except Exception, e:
                parent.log.error("Couldn't read plugin data. Either empty of borken!",exc_info=1)
        else:
            m = Manager(PluginData=[])
        m.init(parent,l)
        m.toolbarNeeded = True
        return m
            
    load = staticmethod(load)
    
    def save(self):
        """ write plugin data back to xml file """
        try:
            file = os.path.expanduser("~")+"/.pyqlogger/plugins.xml"
            open(file,"w").write(str(self))
        except Exception, e:
            self.parent.log.error("Couldn't write plugin data!",exc_info=1)
    


