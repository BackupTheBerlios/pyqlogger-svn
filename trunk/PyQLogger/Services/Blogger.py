#! /usr/bin/python
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

from GenericAtom import GenericAtomService

class BloggerService (GenericAtomService):
    """ Wrapper for Blogger.com """
    endpoints = ("/atom", "/atom/%s", "/atom/%s/%s")
    def __init__(self, username, password):
        GenericAtomService.__init__(self, "www.blogger.com", username, password,
                                                *self.endpoints)
        self.hp_re = re.compile(r'<homePageLink>(.*)</homePageLink>', re.MULTILINE)        
        
    name = "Blogger.com"
    
    def getHomepage(self, blogid):
        """ Returns the homepage of the blog """
        req_url = "http://www.blogger.com/rsd.pyra?blogID=%s" % blogid
        try:
            req = urllib2.urlopen(req_url)
            lines = req.read()
            req.close()
            match = self.hp_re.search(lines)
            if match: 
                return match.group(1)
        except Exception , e:
            print "Exception while getting the homepage: " + str(e)
            return None
