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
endpoints = ("/mt-atom.cgi/weblog", "/mt-atom.cgi/weblog/blog_id=%s", "/mt-atom.cgi/weblog/blog_id=%s/entry_id=%s")

class MovableTypeService (GenericAtomService):
    """ Wrapper for MovableType servers """
    def __init__(self, host, username, password):
        GenericAtomService.__init__(self, host, username, password,*endpoints)

    def getEmpty():
        return MovableTypeService("", "", "")
    getEmpty = staticmethod(getEmpty)

    icon = [
    "16 16 19 1",
    "e c #4a6b84",
    "j c #4a7384",
    ". c #5a7b8c",
    "o c #5a7b94",
    "d c #6b8c9c",
    "q c #7b94a5",
    "g c #8ca5ad",
    "# c #94adb5",
    "n c #9cb5bd",
    "p c #a5b5bd",
    "i c #adbdc6",
    "m c #bdc6ce",
    "h c #c6ced6",
    "c c #cedede",
    "l c #d6dede",
    "a c #dee7e7",
    "f c #e7efef",
    "k c #efeff7",
    "b c #ffffff",
    "................",
    "..#abcd.........",
    ".#bd.#bde.......",
    ".fge..hij.......",
    ".kde.eihe.......",
    ".cheedfk........",
    ".dlhmlbbie..j...",
    "...nhkbbbidee...",
    "...e..#bbbfcio..",
    "......epbbbbbfd.",
    "........fbbahfc.",
    ".......embf.e.a.",
    ".......e#bge..q.",
    "....j....kie..e.",
    ".........dhd....",
    "................"
    ]
  
    name = "MovableType Provider"
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
