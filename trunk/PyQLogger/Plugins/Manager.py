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
from Plugin import Plugin
from EventPlugin import EventPlugin, EventType
from ToolbarPlugin import ToolbarPlugin
from MenuPlugin import MenuPlugin
from ServiceGUIPlugin import ServiceGUIPlugin

def import_plugin_classes():
    globals()["Plugin"] = Plugin
    globals()["EventPlugin"] = EventPlugin
    globals()["MenuPlugin"] = MenuPlugin
    globals()["ToolbarPlugin"] = ToolbarPlugin
    globals()["ServiceGUIPlugin"] = ServiceGUIPlugin
    
import os,sys
from glob import glob


def importClasses(folders):
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
                    for k, v in l.items():
                        # check if provided class can be applied
                        if issubclass(v, Plugin):
                            # don't load duplicate plugins
                            if not [ aplugin for aplugin in PluginClasses if str(v) in str(aplugin)]:
                                PluginClasses += [ v ]
                                g[k] = v
                except Exception,  e:
                    print "Exception on loading plugin: " + str(e)
    return PluginClasses

class Manager(XMLObject):
    """ Plugin manager for keeping the list, loading/unloading and etc """
    Plugins = ListNode('Plugin')
    
    def init(self, parent, PluginClasses):
        """ 
        most of the plugins are already initialized by now,
        so only add the new ones
        """
        import_plugin_classes()
        self.parent = parent
        for plug in PluginClasses:
            exists = [ p for p in self.Plugins if type(p) == plug ]
            if not exists:
                self.Plugins += [ plug() ] # add to the list
            
    def fillToolbar(self, panel):
        """ Fills the provided panel with plugins of ToolbarPlugin type """
        for plug in self.Plugins:
            if issubclass(plug.__class__,ToolbarPlugin) and plug.Enabled == 1 :
                panel.layout().addWidget(plug.getWidget())
    
    def handleEvent(self, eventType):
        """ For supplied event, execute all plugins handling it """
        for plug in self.Plugins:
            if issubclass(plug.__class__, EventPlugin) and plug.Enabled == 1 \
               and plug.EventType == eventType:
                plug.getHandler()
        
    def fillMenu(self):
        """ Fills the editor menu with plugins of MenuPlugin type """
        for plug in self.Plugins:
            if issubclass(plug.__class__,MenuPlugin) and plug.Enabled == 1 :
                plug.getMenu()
        
    def load(parent):
        """ Create a fresh copy of initialized Manager class """
        l = importClasses(["/home/reflog/.pyqlogger/plugins","/usr/share/pyqlogger/plugins"])
        file = os.path.expanduser("~")+"/.pyqlogger/plugins.xml"
        if os.path.exists(file):
            try:
                m = XMLObject.instanceFromXml(open(file).read())
            except Exception, e:
                print "Couldn't read plugin data. Either empty of borken! (%s)"%(str(e))
        else:
            m = Manager(Plugins=[])
        m.init(parent,l)
        return m
            
    load = staticmethod(load)
    
    def save(self):
        """ write plugin data back to xml file """
        try:
            file = os.path.expanduser("~")+"/.pyqlogger/plugins.xml"
            open(file,"w").write(str(self))
        except Exception, e:
            print "Cannot write configuration! (%s)"%(str(e))
    


