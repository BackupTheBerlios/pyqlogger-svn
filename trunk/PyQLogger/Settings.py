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

from Account import Account
from EaseXML import  XMLObject,TextNode,ListNode, IntegerAttribute,ItemNode,ChoiceNode
import os


class Settings(XMLObject):
    """ Class for storing and retrieving ALL information about PyQLogger """
    class UI(XMLObject):
        """ Subclass representing settings related to GUI """
        EnableTray =  IntegerAttribute(default=1,optional=True)
        EnableKde =  IntegerAttribute(default=1,optional=True)
        EnableQScintilla =  IntegerAttribute(default=1,optional=True)
        Notification = IntegerAttribute(default=0)
        
    UI_Settings = ItemNode('UI',optional=True) # GUI settings
    Accounts = ListNode('Account')                  # list of accounts
    AutoLogin = TextNode(optional=True)        # which account to autologin
    
    def accountByName(self,name):
        """ searches the list of accouns, and returns one by it's .Name """
        for a in self.Accounts:
            if a.Name == name:
                return a
        raise Exception("Inavlid Account name: "+name)

    def load():
        """ static method to create new settings class from xml file """
        file = os.path.expanduser("~")+"/.pyqlogger/settings.xml"
        if os.path.exists(file):
            try:
                return XMLObject.instanceFromXml(open(file).read())
            except Exception, e:
                print "Couldn't read settings. Either empty of borken! (%s)"%(str(e))
        return Settings()
            
    load = staticmethod(load)
    
    def save(self):
        """ write settings back to xml file """
        try:
            file = os.path.expanduser("~")+"/.pyqlogger/settings.xml"
            open(file,"w").write(str(self))
        except Exception, e:
            print "Cannot write configuration! (%s)"%(str(e))
            
