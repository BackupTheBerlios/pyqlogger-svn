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
# -*- coding: utf-8 -*-

from qt import *
from setupwizardform import SetupWizardForm
from AtomBlog import *

class SetupWizardForm_Impl(SetupWizardForm):

	def __init__(self,parent = None,name = None,modal = 0,fl = 0):
		SetupWizardForm.__init__(self,parent,name,modal,fl)
		self.frameGeneric.hide()
		
	def initValues(self,params):
		if params.has_key("login")	:self.editLogin.setText(params["login"])
		if params.has_key("url")		:self.editURL.setText(params["url"])
		if params.has_key("password"):self.editPassword.setText(params["password"])
		if params.has_key("host")	:self.editHost.setText(params["host"])
		if params.has_key("hosttype"):
			self.comboProviders.setCurrentItem(params["hosttype"])
			self.comboProviders_activated(self.comboProviders.text(params["hosttype"]))
		else:
			self.comboProviders.setCurrentItem(1)
			self.comboProviders_activated(self.comboProviders.text(1))
		if params.has_key("ep")		:self.editEP.setText(params["ep"])
		if params.has_key("pp")		:self.editPP.setText(params["pp"])
		if params.has_key("fp")		:self.editFP.setText(params["fp"])
		self.checkSave.setChecked(params.has_key("password"))
		if params.has_key("blogs"):
			for b in params["blogs"]:
				self.comboBlogs.insertItem(b)
		if params.has_key("selectedblog"):
			idx = [i for i in range(0,self.comboBlogs.count()) if self.comboBlogs.text(i) == params["selectedblog"]]
			self.comboBlogs.setCurrentItem( idx [0] )

	
	def editLogin_textChanged(self,a0):
		l = str(self.editLogin.text())
		p = str(self.editPassword.text())
		h = str(self.editHost.text())
		u = str(self.editURL.text())
		p1 = str(self.editEP.text())
		p2 = str(self.editFP.text())
		p3 = str(self.editPP.text())
		i = self.comboBlogs.count() > 0
		b = False # control next button
		b2 = False #control fetch blogs button
		b3 = False #control fetch url button
		if l and p and u and i and h and p1 and p2 and p3: b = True
		if l and p and h and p1 and p2 and p3: b2 = True
		if l and p and h and i and p1 and p2 and p3: b3 = True
		self.nextButton().setEnabled( b )
		self.btnFetchBlogs.setEnabled( b2 )
		if self.comboProviders.currentItem() == 1:
			self.btnFetchUrl.setEnabled( b3 )
		
	def comboBlogs_activated(self,a0):
		self.editLogin_textChanged(None)

	def comboProviders_activated(self,a0):
		""" generic/blogger/movable """
		if self.comboProviders.text(0) == a0:
			self.frameGeneric.show()
			host = ep = fp = pp = ""
		elif self.comboProviders.text(1) == a0:
			self.frameGeneric.hide()
			host = "www.blogger.com"
			(ep,fp,pp)	= BloggerClient.endpoints
		elif self.comboProviders.text(2) == a0:
			self.frameGeneric.hide()
			host = ""
			(ep,fp,pp)	= MovableTypeClient.endpoints
			
		self.editHost.setText(host)
		self.editEP.setText(ep)
		self.editFP.setText(fp)
		self.editPP.setText(pp)
	
	def btnFetchUrl_clicked(self):
		bc = BloggerClient(str(self.editHost.text()),str(self.editLogin.text()), str(self.editPassword.text()))
		try:
			url = bc.getHomepage(self.blogs[unicode(self.comboBlogs.currentText())]['id'])
			if url:
				self.editURL.setText(url)
		except:
			QMessageBox.critical(self,"Error","Couldn't fetch blog's URL!")
			pass
	
	def btnFetchBlogs_clicked(self):	
		(h,l,p) = (str(self.editHost.text()),str(self.editLogin.text()), str(self.editPassword.text()))
		(ep,fp,pp) = (str(self.editEP.text()),str(self.editFP.text()),str(self.editPP.text()))
		if self.comboProviders.currentItem() == 0:
			at = GenericAtomClient(h,l,p,ep,fp,pp)
		elif self.comboProviders.currentItem() == 1:
			at = BloggerClient(h,l,p)
		elif self.comboProviders.currentItem() == 2:
			at = MovableTypeClient(h,l,p)
		try:
			self.blogs = at.getBlogs()
			self.comboBlogs.clear()
			for blog in self.blogs.keys():
				self.comboBlogs.insertItem(blog)
			self.editLogin_textChanged(None)
		except:
			QMessageBox.critical(self,"Error","Couldn't fetch list of blogs!")


	def SetupWizardForm_selected(self,a0):
		
		if a0 == "Login Details":
			self.editLogin_textChanged(None)
		if a0 == "Final":
			self.settings = {
				"login":str(self.editLogin.text()),
				"url":str(self.editURL.text()),
				"host":str(self.editHost.text()),
				"hosttype":self.comboProviders.currentItem(),
				"blogs":self.blogs,
				"selectedblog":str(self.comboBlogs.currentText()),
			}
			if self.checkSave.isChecked():
				self.settings["password"] = str(self.editPassword.text())
			if self.comboProviders.currentItem() == 0:
				self.settings["pp"] = str(self.editPP.text())
				self.settings["fp"] = str(self.editFP.text())
				self.settings["ep"] = str(self.editEP.text())
			self.finishButton().setEnabled(True)

