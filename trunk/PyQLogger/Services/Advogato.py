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
import xmlrpclib, time, pickle
from PyQLogger.Post import Post,PostData
from PyQLogger.Blog import Blog,Posts,Drafts
"""
Authentication

string cookie = authenticate(string user, string pass)
    Returns a cookie which is used as the first argument to all methods requiring authentication.

Diary manipulation

int length = diary.len(string user)
    Return the number of entries in a diary.
string html = diary.get(string user, int index)
    Return a diary entry. The index is zero-based, so if diary.len() returns 2 then valid indices are 0 and 1.
date created, date updated = diary.getDates(string user, int index)
    Return the creation and last updated dates of a diary entry. If the entry has not been updated then the updated date will be the same as the creation date.
diary.set(string cookie, int index, string html)
    Set a diary entry. Use -1 as the index to post a new entry, although the value returned by diary.len() is also acceptable.

Obtaining Certs

int exists = user.exists(string user)
    Returns zero if user does not exist, or one if user does exist.
string level = cert.get(string user)
    Returns the certification level of the requested user.


"""
class AdvogatoService (BlogService):
    icon = [
        "16 16 53 1",
        "L c #020202",
        "r c #060606",
        "b c #0a0a0a",
        "w c #0e0e0e",
        "E c #131212",
        "v c #161616",
        "t c #1b1a19",
        "P c #1e1e1e",
        "e c #232222",
        "C c #262625",
        "i c #2b2a29",
        "a c #31302e",
        "B c #3a3938",
        "R c #41403e",
        "h c #474644",
        "S c #4b4a48",
        "g c #4f4e4c",
        "A c #53524f",
        "Y c #565655",
        "J c #5b5a57",
        "l c #61605e",
        "z c #686663",
        "H c #6c6a67",
        "s c #71716f",
        "F c #797875",
        "u c #7e7e7a",
        "K c #83817e",
        "I c #888682",
        "k c #8c8a86",
        "U c #8f8e8b",
        "O c #94928d",
        "j c #969691",
        "x c #9a9692",
        "D c #9a9a96",
        "T c #9e9a96",
        "m c #9e9e98",
        "X c #a29e9a",
        "Q c #a2a29c",
        "N c #a8a6a1",
        "V c #aaaaa8",
        "n c #aeaaa6",
        "o c #b2aeaa",
        "f c #b4b2ad",
        "M c #b9b6b2",
        "d c #bebab6",
        "p c #c2beba",
        "W c #c6c6c6",
        "y c #c7c2bf",
        "c c #cac6c2",
        "# c #d7d7d7",
        "q c #eaeaea",
        "G c #f6f6f6",
        ". c #fefefe",
        "................",
        "................",
        "........#ab.....",
        ".......#cddefcgh",
        ".......ijklmnopi",
        "......qrsmtuvwxw",
        ".....eioccymbzAB",
        "....CocccccoDsEc",
        "FbpaGkh.HcpmIacc",
        "J.fEwxj.zdnKtccc",
        "mDLyccsCMNOrcccc",
        ".PHcciQgwbKccdyc",
        ".LgIFlwbaLMccRfc",
        ".vebSSeTPUUNfBfy",
        ".....PLmbEekjLTp",
        "VVVW.XLkOYLPrMnm"
        ]


    name = "Advogato.org"
    url = "http://www.advogato.org/XMLRPC"
    def __init__(self,host,username,password):
        BlogService.__init__(self,self.url,username,password)        
        
    def login(self):    
        """ this should get the challenge and report if all is good """
        try:          
            self.server = xmlrpclib.Server(self.url)
            self.cookie = self.server.authenticate(self.username, self.password)
        except:
            return False
        return True
    
    def getBlogs(self):
        url="http://www.advogato.org/person/%s/"%self.username
        name="%s's Diary"%self.username
        id = self.username
        return [ Blog(ID=id,Name=name,Url=url,Drafts=Drafts(),Posts=Posts()) ]
    
    def getPosts(self, id):    
        blen = self.server.diary.len(self.username)
        i = 0
        ret = []
        while i < blen and i < 25 :
            ret += [ self.getPost(id, i) ]
            i+=1
        return ret
    
    def deletePost(self, blogId, entryId):
        """ not supported! """
        return False
    
    def getPost(self, blogid, postid):
        postid = int(postid)
        html = self.server.diary.get(self.username, postid)   
        (created, updated) = self.server.diary.getDates(self.username, postid)
        updated = time.strftime('%Y-%m-%dT%H:%M:%SZ',  time.strptime(str(updated),'%Y%m%dT%H:%M:%S'))
        return Post(
                        ID=str(postid),
                        Content=unicode(html),
                        Created=updated,
                        Data=PostData(Pickle=pickle.dumps(None)),
                        Title=updated
                    )

    def newPost(self, blogId, title, content, date=None, other=None):
        if not hasattr(self,"cookie"): 
            self.login()
        blen = self.server.diary.len(self.username)
        self.server.diary.set(self.cookie, -1, content)
        created = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        return Post(ID=blen, Content=content, Created=created, Title=created)
    
    def editPost(self, blogId, post):
        if not hasattr(self,"cookie"): 
            self.login()
        self.server.diary.set(self.cookie, post.ID, post.Content)
                
    def getEmpty():
        return AdvogatoService("","","")
    getEmpty = staticmethod(getEmpty)
    


