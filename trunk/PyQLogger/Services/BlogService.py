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
##
__revision__ = "$Id: BlogService.py 93 2004-12-22 15:59:53Z reflog $"

import httplib, sha, base64, urllib2, time, random
from xml.sax.saxutils import escape , unescape
import feedparser, re
from qtnetwork import QHttpRequestHeader
from qt import QPixmap

def makeNonce():
    """ Generate a random string 'Nonce' marked with timestamp """
    private = base64.encodestring(str(random.random()))
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    return "%s %s" % (timestamp, sha.new("%s:%s" % (timestamp, private)).hexdigest())


class BlogService:
    def __init__(self,host,username,password):
        self.host = host
        self.username = username
        self.password = password
        
    def getOptions(self):
        return {}
        
    def setOptions(self,hash):
        pass
        
    def getEmpty(self):
        pass
        
    def getPixmap(self):
        image = None
        if self.icon:                
            if type(self.icon) == str:
                image = QPixmap()
                image.loadFromData(self.icon)
            elif type(self.icon) == list:
                image = QPixmap(self.icon)
        return image
        
    getEmpty = staticmethod(getEmpty)
    name = "(none)"
    icon = None
