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

from BlogService import BlogService,makeNonce
import re
class GenericAtomService (BlogService):
    """ Implementation of Atom API
        This is an abstract class. Clients should introduce the following:
        self.host = blog host
        self.path = blog atom endpoint
        self.feedpath = format for getting the feed
        self.postpath = format for getting the post    
    """
    endpoints = ("", "", "")
    icon = [
    "16 16 143 2",
    ".f c #6e8c9b",
    "#O c #6f8c9b",
    "#F c #708e9c",
    "#X c #728f9e",
    "#k c #81a3bf",
    "## c #82a3bf",
    "#. c #83a4c0",
    ".9 c #88a7c1",
    "#P c #90a7b2",
    "#Y c #98aeb9",
    "#x c #9bb5c9",
    ".o c #9cb1bc",
    ".g c #9fb3be",
    "af c #a5b2af",
    ".e c #a5b7bf",
    "#w c #a8bed1",
    ".a c #aabcc5",
    ".Q c #abb4a9",
    "#R c #adbec7",
    "#G c #b2c2cb",
    "#Q c #b6c5cd",
    ".Y c #b8cad9",
    ".G c #b9ba98",
    "#7 c #bec1b0",
    "#E c #becbd2",
    "#l c #bfced8",
    "aa c #c4c7b8",
    ".l c #c5c8b8",
    "ah c #c5c8ba",
    "ag c #c5cbc3",
    "ai c #c7cabc",
    ".3 c #c7cfcc",
    "#p c #c9ccbf",
    ".y c #caccbe",
    "ad c #caccbf",
    "#3 c #cacdc0",
    ".Z c #cad7e0",
    "#f c #cccec1",
    "#V c #ccd7dd",
    ".D c #cdd8de",
    "#t c #cedae2",
    ".T c #cfd0be",
    "#0 c #cfd2c7",
    ".L c #d0dadf",
    ".B c #d0dae0",
    "#j c #d1d9d6",
    "#N c #d1d9d7",
    "#T c #d1dbe1",
    "#c c #d1dce5",
    "#g c #d2d4c9",
    ".w c #d2dbe0",
    "#I c #d2dce4",
    ".P c #d2dde5",
    ".s c #d4d6cb",
    ".A c #d4d7cc",
    ".X c #d4dddf",
    "a. c #d4dde1",
    "#K c #d4dde3",
    ".1 c #d5dfe7",
    "ae c #d6d8cd",
    ".r c #d6d8ce",
    "#W c #d7dedf",
    ".u c #d7dfe4",
    "#J c #d7e1e8",
    ".5 c #d8dad0",
    ".0 c #d8e1e7",
    ".t c #d9dbd1",
    ".p c #d9e1e5",
    ".F c #dadcd3",
    "#1 c #dae1e6",
    ".O c #dae3e9",
    ".h c #dbddd4",
    "#a c #dce4eb",
    "#D c #dde0da",
    ".k c #dedfd7",
    ".n c #dee5e8",
    "#m c #dfdfc1",
    ".d c #dfe0d8",
    "#i c #dfe5e7",
    ".E c #e0e2da",
    "#b c #e0e7ed",
    ".x c #e1e3db",
    ".4 c #e2e3dc",
    "#r c #e2e6e5",
    "#Z c #e2e8eb",
    "#H c #e2e8ed",
    "#C c #e3e8ea",
    ".m c #e4e6df",
    ".b c #e4e9ec",
    "ab c #e5e6df",
    ".z c #e5e6e0",
    "#q c #e6e7e1",
    ".v c #e6ebee",
    "al c #e8e9e3",
    ".# c #e8edef",
    ".q c #e9eae5",
    "#2 c #ebeff2",
    ".U c #ece8c2",
    "#u c #ecf0f3",
    ".I c #edeac8",
    "#A c #eeeac8",
    ".H c #eeebc9",
    ".7 c #eeebcb",
    "#6 c #eeefea",
    "am c #eeefeb",
    "#4 c #eef1f3",
    "#9 c #eef1f4",
    "#S c #eef2f4",
    "#h c #eff1ed",
    "#s c #eff3f5",
    "#M c #f0eed1",
    "#y c #f0f1e9",
    ".S c #f0f1ed",
    ".6 c #f1efd5",
    ".8 c #f1f3ef",
    ".2 c #f2f5f7",
    "#B c #f4f2dc",
    "#L c #f4f2dd",
    "aj c #f4f4f2",
    "#8 c #f4f5f3",
    ".W c #f5f3df",
    "#e c #f6f6f4",
    ".C c #f6f8f9",
    ".J c #f7f6e8",
    "a# c #f7f8f6",
    "#d c #f7f8fa",
    "#U c #f7f9f9",
    ".N c #f7f9fa",
    ".V c #f8f7ea",
    "ac c #f8f9f7",
    "#v c #f8fafb",
    "#o c #f9fafa",
    ".i c #fafaf9",
    "#5 c #fafbfc",
    ".M c #fbfcfc",
    "#z c #fcfbf6",
    "#n c #fcfcf8",
    ".c c #fcfcfb",
    ".R c #fcfcfc",
    "ak c #fdfdfd",
    ".K c #fefefd",
    ".j c #fefefe",
    "Qt c #ffffff",
    "QtQtQtQtQtQt.#.a.bQtQtQtQtQtQtQt",
    "QtQtQtQt.c.d.e.f.g.h.iQtQtQtQtQt",
    "QtQt.j.k.l.m.n.o.p.q.l.r.jQtQtQt",
    "QtQt.s.tQtQt.u.v.wQtQt.x.y.jQtQt",
    "Qt.z.AQtQtQt.B.C.DQtQtQt.E.FQtQt",
    ".j.G.H.I.J.K.L.M.D.j.N.O.P.Q.RQt",
    ".S.T.U.V.W.H.X.Y.Z.0.1.2.P.3.4Qt",
    ".5.q.K.6.7.8.9#.###a#b#c#d#e#fQt",
    "#g#hQt.j#i#j#k#.#.#l#m#nQt#o#pQt",
    "#q#r#s#t#u#v#w###x#y#z#A#B#C#DQt",
    "#E#F#G#H#I#J#K.2.u#L.H#M#N#O#P.j",
    "#Q.f#R#S.jQt#T#U#VQtQt#z#W#X#Y.j",
    ".M#Z#0.jQtQt#1#2.DQtQt.j#3#4#5Qt",
    "QtQt#6#7#8Qt#9a..BQta#aaabQtQtQt",
    "QtQtQtacadaaaeafagahaiajQtQtQtQt",
    "QtQtQtQtQtak.Salam.RQtQtQtQtQtQt"
    ]

    name = "Generic Atom API Provider"
    def __init__(self, host, username, password, path, feedpath, postpath):
        self.id_re = re.compile(r'(\d+)$')
        BlogService.__init__(self,host, username, password)
        self.path = path
        self.feedpath = feedpath
        self.postpath = postpath
        
    def getOptions(self):
        return { "Atom Endpoint":self.path , "Blog Atom Feed Path":self.feedpath, "Post Atom Url Path ":self.postpath }
            
    def setOptions(self,hash):
        self.path = hash["Atom Endpoint"]
        self.feedpath = hash["Blog Atom Feed Path"]
        self.postpath = hash["Post Atom Url Path "]
    
    def _makeCommonHeaders(self, Req, date=None):
        """ Returns a dict with Nonce, Password Digest and other headers """
        nonce = makeNonce()
        base64EncodedNonce = base64.encodestring(nonce).replace("\n", "")
        if not date:
            created = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        else:
            created = date
    
        passwordDigest = base64.encodestring(sha.new(nonce + created + self.password).digest()).replace("\n", "")
        authorizationHeader = 'UsernameToken Username="%s", PasswordDigest="%s", Created="%s", Nonce="%s"' % (self.username, passwordDigest, created, base64EncodedNonce)
        Req.setValue("Authorization", 'WSSE profile="UsernameToken"')
        Req.setValue("X-WSSE", authorizationHeader)
        Req.setValue("UserAgent", "PyQLogger")
        Req.setValue("Host",self.host)
        return created
        
    def startGetBlogs(self):
        """ initialize GET request """
        Req = QHttpRequestHeader("GET",self.path)
        self._makeCommonHeaders(Req)
        return Req

    def endGetBlogs(self,result):    
        """ Returns dict where key is blog's name, and value is blog's properties dict """
        ret = {}
        for blog in feedparser.parse(result)['feed']['links']:
            ret [ blog["title"] ] = {
                'id'   : self.id_re.search(blog['href']).group(1),
                'href' : blog['href'],
                'rel'  : blog['rel'] ,
                'type' : blog['type'],
            } 
        return ret

    def startGetPosts(self, blogId ):
        """ Initialize GET post request """
        Req = QHttpRequestHeader("GET",  self.feedpath % (blogId))
        self._makeCommonHeaders(Req)
        return Req
        
    def endGetPosts(self, result):
        """ Returns posts Atom Feed """
        res = []
        for post in feedparser.parse(result)['entries']:
            content = post['content'][0]['value']
            if post['content'][0]['mode'] == 'escaped':
                unescape(content)
            res += [ {
                'title':post['title'],
                'date':post['modified'],
                'id':self.id_re.search( post['id'] ).group(1),
                'content':content
            }]
        return res

    def startGetPost(self,  blogId, postId):
        Req = QHttpRequestHeader("GET",self.postpath % (blogId, postId))
        self._makeCommonHeaders(Req)
        return Req
        
    def endGetPost(self,result):
        """ Returns a post """
        res = []
        for post in feedparser.parse(result)['entries']:
            content = post['content'][0]['value']
            if post['content'][0]['mode'] == 'escaped':
                unescape(content)
            res += [ {
                'title':post['title'],
                'date':post['modified'],
                'id':self.id_re.search( post['id'] ).group(1),
                'content':content
                }]
        if res:
            return res[0]
        return None

    def _makeBody(self, title, content, created, cat=None):
        """ generate body of post entry based on parameters """
        if cat:
            catstr = "\n<dc:subject>%s</dc:subject>\n" % cat
        else:
            catstr = ""
        return unicode("""<?xml version="1.0" encoding="UTF-8" ?>
        <entry xmlns="http://purl.org/atom/ns#">
        <generator url="http://www.reflog.info/">Reflog's Blogger</generator>
        <title mode="escaped" type="text/html">%s</title>
        <issued>%s</issued>%s        
        <content mode="escaped" type="text/html">%s</content>
        </entry>""" % (escape(title), created, catstr, escape(content))).encode("utf-8")
        
    def startNewPost(self,  blogId, title, content, date=None):
        """ Make a new post to Blogger, returning it's body """
        Req = QHttpRequestHeader("POST",self.feedpath % (blogId))
        created = self._makeCommonHeaders(Req,date)
        Req.setContentType("application/atom+xml")
        return (Req, self._makeBody(title, content, created))
        
    def endNewPost(self, result):
        """ Parse result, and return post's ID """
        try:
            res = feedparser.parse(result)['entries'][0]['id']
            amatch = self.id_re.search(res)
            if amatch:
                return amatch.group(1)
        except:
            return None
    
    def startEditPost (self, blogId, entryId, title, content, date=None):
        """ Edits existing post on Blogger, returns new ID """        
        Req = QHttpRequestHeader("PUT",self.postpath % (blogId, entryId))
        created = self._makeCommonHeaders(Req,date)
        Req.setContentType("application/atom+xml")
        return (Req, self._makeBody(title, content, created))
        
    def getCategories(self, blogId):
        """ Fetches the list of blog's categories """
        return None

    def deletePost(self,  blogId, entryId):
        """ Deletes a post from specified Blog """
        Req = QHttpRequestHeader("DELETE",self.postpath % (blogId, entryId))
        created = self._makeCommonHeaders(Req)
        return Req
        
    def getEmpty():
        return GenericAtomService("","","","","","")
    getEmpty = staticmethod(getEmpty)
        
