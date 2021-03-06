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
from xmlrpclib import Server
from md5 import md5
from PyQLogger.Post import Post,PostData
from PyQLogger.Blog import Blog,Posts,Drafts
import urllib2,feedparser,pickle,time

class LiveJournalService (BlogService):
    icon = \
        "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
        "\x49\x48\x44\x52\x00\x00\x00\x10\x00\x00\x00\x10" \
        "\x08\x06\x00\x00\x00\x1f\xf3\xff\x61\x00\x00\x02" \
        "\x4d\x49\x44\x41\x54\x38\x8d\x8d\xd2\x4b\x48\x94" \
        "\x61\x14\xc6\xf1\xff\xfb\x99\x8e\x77\xb3\x14\x89" \
        "\x66\x1c\x41\xb1\x88\xd4\x2e\x46\x90\xd2\x37\x05" \
        "\xa1\x5d\x1c\x6b\x19\x04\x91\x82\xba\x8a\x30\x24" \
        "\x84\x60\xb4\x45\x85\x64\x54\x3b\xb1\x66\x23\xd2" \
        "\x6d\xa1\xd4\xd4\xa2\xd5\x37\x76\x73\xa1\x86\x16" \
        "\x54\x18\x88\x8a\x97\x11\x1b\x1d\x2f\x23\x31\x97" \
        "\xd3\x62\xd0\xb4\x0c\x7d\xe0\x5d\xbd\xf0\xe3\x39" \
        "\x87\xa3\x44\x04\x00\x55\x58\xdd\x00\x38\x88\xa4" \
        "\x51\x7a\x5a\x1a\xd8\x44\x94\x88\x90\x7c\xf4\x8a" \
        "\xf1\xb0\x68\x87\xfe\xd3\x1f\xc0\x39\xbc\xc0\xd4" \
        "\x52\x80\x91\x89\x59\xb7\x0c\x3c\xb2\x6d\x04\x68" \
        "\xaa\xb0\xba\xa1\x4d\x37\xeb\x4f\xbf\x4d\xf3\xc3" \
        "\x9c\x83\xfb\xc9\x0d\x9e\xdd\xbc\xc8\xd6\xb8\x68" \
        "\x5d\x15\x54\x1a\x1b\x02\x80\xe3\xcb\xd4\x02\x69" \
        "\x7b\xb3\xa9\x29\xdf\xc7\xeb\xb7\xfd\x9c\xbf\xfe" \
        "\x98\xe2\xd2\x52\x32\x2d\x96\x4d\x20\x07\xab\xe4" \
        "\xe0\xb9\x7a\xf9\xd4\xd7\x2b\x77\x5a\x9f\x4b\x4a" \
        "\xd1\x65\xb9\x6b\xcc\x48\x6b\x9f\xc8\x83\xf7\xf3" \
        "\x62\x3d\xe3\x10\xf2\x2f\x19\x22\xc2\x7a\x4f\x03" \
        "\x1a\xb5\x38\x13\xde\xb9\x25\x9a\xda\x3f\x60\x2b" \
        "\x29\xa1\xab\xeb\x1d\x20\x98\x4c\x89\x5c\xad\xaf" \
        "\x23\x2b\xd3\xaa\xab\xfc\x8a\x75\x9b\x28\x11\x41" \
        "\x15\x56\x1b\x19\x09\x31\x7a\x76\x7e\x21\x79\xf9" \
        "\x79\x78\xbd\x5e\x96\xfc\x8b\x94\x9f\xb5\x13\x0e" \
        "\x2b\x02\x01\x3f\xcd\xb7\x9b\x19\x1a\x1a\x72\x4b" \
        "\xbf\x73\xcd\x62\x35\x00\xe9\x69\xb1\x79\x66\xfd" \
        "\xee\xb1\xe1\x61\xc2\xe1\x30\xa9\xa9\xa9\xc4\x27" \
        "\x24\xf2\xf2\x85\x0b\xa5\x84\xe8\xe8\x78\x6a\xaf" \
        "\xd5\x92\x65\xb5\xea\xaa\x60\x6d\x13\xb5\x7c\x07" \
        "\x00\xaa\xa0\xd2\x30\x9b\xcd\xfa\x49\x7b\x19\x4a" \
        "\x29\x7c\x3e\x1f\xfe\xc5\x79\xec\xe5\x91\x26\xc1" \
        "\xa0\x9f\x7b\x4d\xf7\x19\x1c\x1c\x74\xcb\x40\xa4" \
        "\xc9\x1a\x20\x82\x54\x18\x3b\x2d\x16\xfd\x54\xd9" \
        "\x1f\xc4\x33\x31\x4e\x4e\x6e\x2e\x3e\x9f\x8f\x85" \
        "\xd1\xcf\x74\xf7\x7e\xc7\xfb\xb1\x45\xad\x8c\xb0" \
        "\x3a\xd2\xef\xb4\x8d\x8d\x8c\xba\x5d\x1d\x9d\x84" \
        "\x42\x21\x52\x52\x52\x88\x4d\x48\xa6\x58\xde\x70" \
        "\x6b\xff\x57\x5c\x55\x49\x9c\xd8\x9d\xb4\x7c\xb9" \
        "\xff\x02\x00\x32\xe0\xb4\x4d\x4c\x8c\xbb\x5f\x75" \
        "\x74\x12\x0c\x06\x89\x89\x8d\x23\x3d\xc9\x44\xf6" \
        "\xf6\x58\xb4\x80\x60\x3f\x9c\x06\x73\xbf\xf8\x2f" \
        "\xb0\xdc\x64\xd2\x33\xe9\x76\x75\x74\x32\x33\xed" \
        "\x61\x57\x46\xec\xca\xdf\xf1\x3d\xc9\x68\x89\xd1" \
        "\x8e\x75\x77\xf0\x77\x54\x41\xa5\x61\x52\xe8\x17" \
        "\x8a\xd3\x39\x7d\x60\x1b\x47\x72\x13\xa9\x6b\x1f" \
        "\xa5\xad\x7b\x1a\xb5\x25\xea\xd8\x86\xc0\x0a\x14" \
        "\x99\xd9\x46\x38\xac\xa3\x69\x10\x0a\x43\x94\xd6" \
        "\xb8\x69\x60\x75\xb4\x43\x35\x36\x11\xb1\x29\xa5" \
        "\x8c\xdf\x6d\x00\x0e\x2c\xcc\xc2\x02\x94\x00\x00" \
        "\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82"
    name = "LiveJournal"
    def __init__(self,host,username,password):
        BlogService.__init__(self,"www.livejournal.com",username,password)
        self.server = Server("http://www.livejournal.com/interface/xmlrpc")
        
    def prepare_call(self,params={}):
        ch = self.server.LJ.XMLRPC.getchallenge()
        response = md5(ch["challenge"] + md5(self.password).hexdigest()).hexdigest()
        params.update( {
                "username":self.username,
                "auth_method" : 'challenge',
                "auth_challenge":ch["challenge"],
                "auth_response":response
                })
        return params
        
    def login(self):    
        """ this should get the challenge and report if all is good """
        try:          
            params = self.prepare_call()
            log = self.server.LJ.XMLRPC.login(params)
            self.userid = log["userid"]
            return True
        except Exception , e:
            return False

    def getBlogs(self):
        req_url = "http://www.livejournal.com/users/%s/data/atom"%self.username
        try:
            req = urllib2.urlopen(req_url)
            lines = req.read()
            req.close()
            feed = feedparser.parse(lines)
            title = feed['feed']['title']
            url = feed['feed']['link']
            id = self.username
            return [ Blog(ID=id,Name=title,Url=url,Drafts=Drafts(),Posts=Posts()) ]
        except:
            return []

    def getEvent(self,eventprops):
        params = self.prepare_call(eventprops)
        res = self.server.LJ.XMLRPC.getevents(params)
        ret = []
        for event in res['events']:
            created = time.strftime('%Y-%m-%dT%H:%M:%SZ',  time.strptime(event['eventtime'],'%Y-%m-%d %H:%M:%S'))
            ret += [ Post(
                            ID=unicode(event['itemid']),
                            Content=unicode(event["event"]),
                            Created=created,
                            Data=PostData(Pickle=pickle.dumps(event["props"])),
                            Title=unicode(event['subject'])
                        )]
        return ret

    def getPosts(self,id):
        return self.getEvent({"selecttype":"lastn" , "howmany":"15" })

    def getPost(self,blogid,postid):
        ret = self.getEvent({"selecttype":"one" , "itemid":postid })
        if ret:
            return ret[0]

    def newPost(self, blogId, title, content, date=None, other=None):
        t = time.localtime()
        created = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        par = { "event":content,"subject":title,"year":t[0],"day":t[2],"hour":t[3],"mon":t[1],"min":t[4] }
        if other:
            par.update(other) 
        params = self.prepare_call(par)
        res = self.server.LJ.XMLRPC.postevent(par)
        p = Post(ID=res['itemid'],Title=title,Content=content,Created=created)
        if other:
            p.Data = PostData(pickle.dumps(other))
        return p

    def editPost(self, blogId, post):
        t = time.localtime()
        post.Created = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        par = { "itemid":post.ID,"event":post.Content,"subject":post.Title,"year":t[0],"day":t[2],"hour":t[3],"mon":t[1],"min":t[4] }
        if post.Data:
            par.update(pickle.loads(post.Data.Pickle))
        params = self.prepare_call(par)
        self.server.LJ.XMLRPC.editevent(par)
        

    def getEmpty():
        return LiveJournalService("","","")
    getEmpty = staticmethod(getEmpty)

