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

class UI(XMLObject):
    EnableKde =  IntegerAttribute()
    EnableQScintilla =  IntegerAttribute()
    Notification = IntegerAttribute()

class Settings(XMLObject):
    UI_Settings = ItemNode('UI',optional=True) # GUI settings
    Accounts = ListNode('Account') # list of accounts
    AutoLogin = TextNode(optional=True) # which account to autologin
    
    def accountByName(self,name):
        for a in self.Accounts:
            if a.Name == name:
                return a
        raise Exception("Inavlid Account name: "+name)

    def load():
        file = os.path.expanduser("~")+"/.pyqlogger/settings.xml"
        if os.path.exists(file):
            try:
                return XMLObject.instanceFromXml(open(file).read())
            except Exception, e:
                print "Couldn't read settings. Either empty of borken! (%s)"%(str(e))
        return Settings()
            
    load = staticmethod(load)
    
    def save(self):
        file = os.path.expanduser("~")+"/.pyqlogger/settings.xml"
        open(file,"w").write(str(self))
        
