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

class GenericAtomService (BlogService):
    """ Implementation of Atom API
        This is an abstract class. Clients should introduce the following:
        self.host = blog host
        self.path = blog atom endpoint
        self.feedpath = format for getting the feed
        self.postpath = format for getting the post    
    """
    endpoints = ("", "", "")        
    name = "Generic Atom API Provider"
    def __init__(self, host, username, password, path, feedpath, postpath):
        self.id_re = re.compile(r'(\d+)$')
        BlogService.__init__(self,host, username, password)
        self.path = path
        self.feedpath = feedpath
        self.postpath = postpath
        
    def getOptions(self):
        return { "Atom Endpoint":self.path , "Blog Atom Feed Path":self.feedpath, "Post Atom Url Path ":self.psotpath }
            
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

    def getHomepage(self, blogid):
        """ Returns the homepage of the blog """
        return None

    def deletePost(self,  blogId, entryId):
        """ Deletes a post from specified Blog """
        Req = QHttpRequestHeader("DELETE",self.postpath % (blogId, entryId))
        created = self._makeCommonHeaders(Req)
        return Req
