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
## Changes:
## 15/10/2004 - added new function getPost for single post fetching
##            - added optional date passing for newPost and editPost
__revision__ = "$Id$"

import httplib, sha, base64, urllib2, time, random
from xml.sax.saxutils import escape , unescape
import feedparser, re

class AtomBlog:
    """ Implementation of Atom API for posting to Blogger
        Written by Reflog, based on code from http://www.daikini.com 
        This is an abstract class. Clients should introduct the following:
        self.host = blog host
        self.path = blog atom endpoint
        self.feedpath = format for getting the feed
        self.postpath = format for getting the post    
    """
        
    def __init__(self, host, username, password):
        self.id_re = re.compile(r'(\d+)$')
        self.username = username
        self.password = password
        self.host = host
        self.path = ""
        self.feedpath = ""
        self.postpath = ""

        
    def _getNonce(self):
        """ Generate a random string 'Nonce' marked with timestamp """
        private = base64.encodestring(str(random.random()))
        timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        return "%s %s" % (timestamp, sha.new("%s:%s" % (timestamp, private)).hexdigest())

    def _makeCommonHeaders(self, date=None):
        """ Returns a dict with Nonce, Password Digest and other headers """
        nonce = self._getNonce()
        base64EncodedNonce = base64.encodestring(nonce).replace("\n", "")
        if not date:
            created = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        else:
            created = date
    
        passwordDigest = base64.encodestring(sha.new(nonce + created + self.password).digest()).replace("\n", "")
        authorizationHeader = 'UsernameToken Username="%s", PasswordDigest="%s", Created="%s", Nonce="%s"' % (self.username, passwordDigest, created, base64EncodedNonce)
        headers = {
            "Authorization": 'WSSE profile="UsernameToken"', 
            "X-WSSE": authorizationHeader, 
            "UserAgent": "Reflog's Blogger"
            }
        
        return (created, headers)
        
    def getBlogs(self):
        """ Returns dict where key is blog's name, and value is blog's properties dict """
        (created, headers) = self._makeCommonHeaders()
        conn = httplib.HTTPConnection(self.host)
        conn.request("GET", self.path, "", headers)
        response = conn.getresponse()
        xml = response.read()
        conn.close()
        ret = {}
        for blog in feedparser.parse(xml)['feed']['links']:
            ret [ blog["title"] ] = {
                'id'   : self.id_re.search(blog['href']).group(1),
                'href' : blog['href'],
                'rel'  : blog['rel'] ,
                'type' : blog['type'],
            } 
        return ret

    def getPosts(self, blogId):
        """ Returns posts Atom Feed """
        (created, headers) = self._makeCommonHeaders()
        conn = httplib.HTTPConnection(self.host)
        path = self.feedpath % (blogId)
        conn.request("GET", path, "", headers)
        response = conn.getresponse()
        xml = response.read()
        conn.close()
        res = []
        for post in feedparser.parse(xml)['entries']:
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

    def getPost(self, blogId, postId):
        """ Returns a post """
        (created, headers) = self._makeCommonHeaders()
        conn = httplib.HTTPConnection(self.host)
        path = self.postpath % (blogId, postId)
        conn.request("GET", path, "", headers)
        response = conn.getresponse()
        xml = response.read()
        conn.close()
        res = []
        for post in feedparser.parse(xml)['entries']:
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
        
    def newPost(self, blogId, title, content, date=None):
        """ Make a new post to Blogger, returning it's ID """
        
        (created, headers) = self._makeCommonHeaders(date)    
        headers["Content-type"] = "application/atom+xml"
        path = self.feedpath % (blogId)
        body = self._makeBody(title, content, created)
        conn = httplib.HTTPConnection(self.host)
        conn.request("POST", path, body, headers)
        response = conn.getresponse()
        resp = response.read()
        conn.close()
        amatch = self.id_re.search(feedparser.parse(resp)['entries'][0]['id'])
        if amatch:
            return amatch.group(1)
        return None
    
    def editPost (self, blogId, entryId, title, content, date=None):
        """ Edits existing post on Blogger, returns new ID """        
        path = self.postpath % (blogId, entryId)
        (created, headers) = self._makeCommonHeaders(date)    
        headers["Content-type"] = "application/atom+xml"
        body = self._makeBody(title, content, created)
        conn = httplib.HTTPConnection(self.host)
        conn.request("PUT", path, body, headers)
        response = conn.getresponse()
        response.read() # error checking should be added here
        conn.close()

    def getCategories(self, blogId):
        """ Fetches the list of blog's categories """
        return None

    def getHomepage(self, blogid):
        """ Returns the homepage of the blog """
        return None

    def deletePost(self, blogId, entryId):
        """ Deletes a post from specified Blog """
        path = self.postpath % (blogId, entryId)
        (created, headers) = self._makeCommonHeaders()    
        conn = httplib.HTTPConnection(self.host)
        conn.request("DELETE", path, "", headers)
        response = conn.getresponse()
        return bool(response.status == 410 or response.status == 200)

class GenericAtomClient(AtomBlog):
    """ Generic class for AtomAPI Handling """
    endpoints = ("", "", "")
    def __init__(self, host, username, password, path, feedpath, postpath):
        AtomBlog.__init__(self, host, username, password)
        self.path = path
        self.feedpath = feedpath
        self.postpath = postpath


class BloggerClient(GenericAtomClient):
    """ Wrapper for Blogger.com """
    endpoints = ("/atom", "/atom/%s", "/atom/%s/%s")
    def __init__(self, host, username, password):
        GenericAtomClient.__init__(self, host, username, password, "/atom", "/atom/%s", "/atom/%s/%s")
        self.hp_re = re.compile(r'<homePageLink>(.*)</homePageLink>', re.MULTILINE)        

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


class MovableTypeClient(GenericAtomClient):
    """ Wrapper for MovableType servers """
    def __init__(self, host, username, password):
        GenericAtomClient.__init__(self, host, username, password,
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

