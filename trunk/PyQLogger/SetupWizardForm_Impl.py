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
from AtomBlog import AtomBlog

class SetupWizardForm_Impl(SetupWizardForm):

	def __init__(self,parent = None,name = None,modal = 0,fl = 0):
		SetupWizardForm.__init__(self,parent,name,modal,fl)
		
	def initValues(self,params):
		if params.has_key("login"):	self.editLogin.setText(params["login"])
		if params.has_key("url"):
			self.editURL.setText(params["url"])
		if params.has_key("password"):
			self.editPassword.setText(params["password"])
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
		u = str(self.editURL.text())
		i = self.comboBlogs.count() > 0
		b = False
		b2 = False
		if l and p and u and i: b = True
		if l and p : b2 = True
		self.nextButton().setEnabled( b )
		self.btnFetchBlogs.setEnabled( b2 )
		
	def comboBlogs_activated(self,a0):
		self.editLogin_textChanged(None)
		
	def btnFetchBlogs_clicked(self):
		at = AtomBlog(str(self.editLogin.text()), str(self.editPassword.text()))
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
				"blogs":self.blogs,
				"selectedblog":str(self.comboBlogs.currentText()),
			}
			if self.checkSave.isChecked():
				self.settings["password"] = str(self.editPassword.text())
			self.finishButton().setEnabled(True)

