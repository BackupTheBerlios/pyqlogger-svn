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
from BlogService import BlogService

class LiveJournalService (BlogService):


  def __init__(self):

    pass


##class LiveJournalClient(GenericAtomClient):
##    """ Wrapper for LiveJournal.com """
##    endpoints = ("something", "/interface/atomapi/%s/feed/", "/interface/atomapi/reflog/post/%s")
##    def __init__(self, username, password):
##        GenericAtomClient.__init__(self, "www.livejournal.com",  username, password, 
##                                                 *self.endpoints)
##        self.id_re = re.compile(r'urn:lj:livejournal.com:atom\d+:(?:.*?):(\d+)$')
##        
##    def getHomepage(self, blogid):
##        return "http://www.livejournal.com/users/%s/"%self.username
##
##    def startGetBlogs(self):
##        return {self.username: { "id": self.username } }
##
