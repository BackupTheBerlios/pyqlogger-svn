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

class MovableTypeService (GenericAtomService):
    """ Wrapper for MovableType servers """
    def __init__(self, host, username, password):
        GenericAtomService.__init__(self, host, username, password,
            "/mt-atom.cgi/weblog", "/mt-atom.cgi/weblog/blog_id=%s", "/mt-atom.cgi/weblog/blog_id=%s/entry_id=%s")

    endpoints = ("/mt-atom.cgi/weblog", "/mt-atom.cgi/weblog/blog_id=%s", "/mt-atom.cgi/weblog/blog_id=%s/entry_id=%s")

    def getCategories(self, blogId):
        """ Fetches the list of blog's categories """
        path = self.feedpath+"/svc=categories" % blogId
        (created, headers) = self._makeCommonHeaders()
        conn = httplib.HTTPConnection(self.host)
        conn.request("GET", path, "", headers)
        response = conn.getresponse()
        xml = response.read()
        conn.close()
        return feedparser.parse(xml)['categories']
