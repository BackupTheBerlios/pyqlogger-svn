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

import httplib,sha,sha,base64
import time, random
from xml.sax.saxutils import escape , unescape
import feedparser, re

class AtomBlog:
	""" Implementation of Atom API for posting to Blogger
		Written by Reflog, based on code from http://www.daikini.com """
		
	def __init__(self,username,password):
		self.id_re = re.compile(r'(\d+)$')
		self.host = "www.blogger.com"
		self.path = "/atom"
		self.username = username
		self.password = password
		
	def _getNonce(self):
		""" Generate a random string 'Nonce' marked with timestamp """
		private = base64.encodestring(str(random.random()))
		timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
		return "%s %s" % (timestamp, sha.new("%s:%s" % (timestamp, private)).hexdigest())

	def _makeCommonHeaders(self,date=None):
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
		
		return (created,headers)
		
	def getBlogs(self):
		""" Returns dict where key is blog's name, and value is blog's properties dict """
		(created,headers) = self._makeCommonHeaders()
		conn = httplib.HTTPConnection(self.host)
		conn.request("GET", self.path, "", headers)
		response = conn.getresponse()
		xml = response.read()
		conn.close()
		ret = {}
		for b in feedparser.parse(xml)['feed']['links']:
			ret [ b["title"] ] = {
				'id'   : self.id_re.search(b['href']).group(1),
				'href' : b['href'],
				'rel'  : b['rel'] ,
				'type' : b['type'],
			} 
		return ret

	def getPosts(self,blogId):
		""" Returns posts Atom Feed """
		(created,headers) = self._makeCommonHeaders()
		conn = httplib.HTTPConnection(self.host)
		path = "%s/%s" % (self.path , blogId)
		conn.request("GET", path, "", headers)
		response = conn.getresponse()
		xml = response.read()
		conn.close()
		res = []
		for en in feedparser.parse(xml)['entries']:
			s = en['content'][0]['value']
			if en['content'][0]['mode'] == 'escaped':
				unescape(s)
			res += [ {
				'title':en['title'],
				'date':en['modified'],
				'id':self.id_re.search( en['id'] ).group(1),
				'content':s
				}]
		return res

	def getPost(self,blogId,postId):
		""" Returns a post """
		(created,headers) = self._makeCommonHeaders()
		conn = httplib.HTTPConnection(self.host)
		path = "%s/%s/%s" % (self.path , blogId, postId)
		conn.request("GET", path, "", headers)
		response = conn.getresponse()
		xml = response.read()
		conn.close()
		res = []
		for en in feedparser.parse(xml)['entries']:
			s = en['content'][0]['value']
			if en['content'][0]['mode'] == 'escaped':
				unescape(s)
			res += [ {
				'title':en['title'],
				'date':en['modified'],
				'id':self.id_re.search( en['id'] ).group(1),
				'content':s
				}]
		if res:
			return res[0]
			
	def _makeBody(self,title,content,created):
		""" generate body of post entry based on parameters """
		return """<?xml version="1.0" encoding="UTF-8" ?>
		<entry xmlns="http://purl.org/atom/ns#">
		<generator url="http://www.reflog.info/">Reflog's Blogger</generator>
		<title mode="escaped" type="text/html">%s</title>
		<issued>%s</issued>
		<content mode="escaped" type="text/html">%s</content>
		</entry>""" % (escape(title),created,escape(content))
		
	def newPost(self,blogId,title,content,date=None):
		""" Make a new post to Blogger, returning it's ID """
		
		(created,headers) = self._makeCommonHeaders(date)	
		headers["Content-type"] = "application/atom+xml"
		path = "%s/%s" % (self.path,blogId)
		body = self._makeBody(title,content,created)
		conn = httplib.HTTPConnection(self.host)
		conn.request("POST", path, body, headers)
		response = conn.getresponse()
		resp = response.read()
		conn.close()
		m = self.id_re.search(feedparser.parse(resp)['entries'][0]['id'])
		if m:
			return m.group(1)
	
	
	def editPost (self,blogId,entryId,title,content,date=None):
		""" Edits existing post on Blogger, returns new ID """		
		path = "%s/%s/%s" % (self.path , blogId, entryId)
		(created,headers) = self._makeCommonHeaders(date)	
		headers["Content-type"] = "application/atom+xml"
		body = self._makeBody(title,content,created)
		conn = httplib.HTTPConnection(self.host)
		conn.request("PUT", path, body, headers)
		response = conn.getresponse()
		resp = response.read()
		conn.close()


	def deletePost(self,blogId,entryId):
		""" Deletes a post from specified Blog """
		path = "%s/%s/%s" % (self.path , blogId, entryId)
		path = "%s/%s/%s" % (self.path , blogId, entryId)
		(created,headers) = self._makeCommonHeaders()	
		conn = httplib.HTTPConnection(self.host)
		conn.request("DELETE", path, "", headers)
		response = conn.getresponse()
		return bool(response.status == 410 or response.status == 200)


