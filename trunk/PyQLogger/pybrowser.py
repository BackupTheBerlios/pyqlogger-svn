## $Id$
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
from qt import *
import urlparse
import traceback
from urllib import urlopen
import time


class MimeFactory(QMimeSourceFactory):

	current=None

	def __init__(self,browser):
		QMimeSourceFactory.__init__(self)
		self.browser=browser
		
	def data(self,name,context=None):
		if context:
			return self.data(self.makeAbsolute(name,context))
		res=None
		(local,type,subtype)=self.fetchURL(str(name))
		if type=="image":
			i=QImage()
			#If image loading fails, return empty image
			if not i.loadFromData(local,None):
				i.create(10,10,8)
			res=QImageDrag(i)
		else: #Assume it's text
			res=QTextDrag(local)
			if subtype=="html":
				res.setSubtype("html")
			else:
				res.setSubtype("plain")
		self.current=res
		return self.current
		
	def makeAbsolute(self,name,context):
		return urlparse.urljoin(str(context),str(name))

	def fetchURL(self,url):
		local=""
		type="text"
		subtype="plain"
		try:
			remote=urlopen(url)
			info=remote.info()
			(type,subtype)=info.gettype().split("/")
			local=remote.read()
			l=info.getheader('content-length')
			if not l:
				l=0
			else:
				l=int(l)
			print 'size',l
				
			p=0
			c=0
			bsize=1024
			while True:
				self.browser.emit(PYSIGNAL('status'),("Downloading: "+url+"(%sKB)"%str(p/1024),))
				self.browser.emit(PYSIGNAL('size'),(p,))
				if l:
					self.browser.emit(PYSIGNAL('percent'),((p*100)/l,))
				qApp.processEvents()	
				#Lame attempt at making this report about once a second
				stamp=time.time()
				c=c+1
				buf=remote.read(int(bsize))
				delta=time.time()-stamp
				if delta <.5: #Data coming quickly, get more on each loop
					bsize=min(bsize*1.25,10000)
				elif delta >.75: #Data coming slowly, get less on each loop
					bsize=max(bsize*.75,100)
					
				#End of file
				if buf=='':
					self.browser.emit(PYSIGNAL('percent'),(100,))
					break
					
				p=p+len(buf)
				local=local+buf
		
		except:
			traceback.print_exc()
		return (local,type,subtype)
        

class QBrowser(QTextBrowser):
	def __init__(self,parent=None,title=''):
		QTextBrowser.__init__(self,parent)
		self.mf=MimeFactory(self)
		self.setMimeSourceFactory(self.mf)

def printit(arg):
	print str(arg)
		
if __name__=="__main__":
	from sys import argv
	app=QApplication(argv)
	w=QBrowser()
	
	w.connect(w,PYSIGNAL('percent'),printit)
	w.connect(w,PYSIGNAL('size'),printit)
	w.connect(w,PYSIGNAL('status'),printit)
	
	w.show()
	w.setSource(argv[1])
	app.connect(app, SIGNAL("lastWindowClosed()")
				, app, SLOT("quit()"))
	app.exec_loop()
