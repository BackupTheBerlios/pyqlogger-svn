## This file is part of PyQLogger.
##
## Copyright (c) 2004 Xander Soldaat a.k.a. Mightor
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
from urldialog import UrlDialog


class UrlDialog_Impl(UrlDialog):


	targetList = {}

        def __init__(self,parent = None,name = None,modal = 0,fl = 0):
                UrlDialog.__init__(self,parent,name,modal,fl)
		# Hide these two until we've figured out how
		# to deal with them
		self.comboClass.hide()
		self.labelClass.hide()

		self.editUrl.setFocus()
		self.targetList['in new window'] = '_blank'
		self.targetList['in same window'] = '_top'
		self.targetList['in same frame'] = '_self'
		for key in self.targetList.keys():
			self.comboOpen.insertItem(key)

	def initValues(self, text):
		if text:
			self.editName.setText(text)

	def urltag(self):
		urltag = '<a href='
		url = self.editUrl.text()
		title = self.editTitle.text()
		name = self.editName.text()
		width = self.editWidth.text()
		height = self.editHeight.text()
		border = self.editBorder.text()

		if not url or not name:
			return None
		else:
			urltag += '\'%s\'' % url

		if title:
			urltag += ' title=\'%s\'' % title

		if width:
			urltag += ' width=\'%s\'' % width

		if height:
			urltag += ' height=\'%s\'' % height

		if border: 
			urltag += ' border=\'%s\'' % border

		if self.checkOpen.isChecked():
			if self.targetList.has_key('%s' % self.comboOpen.currentText()):
				target = self.targetList['%s' % self.comboOpen.currentText()]
				urltag += ' target=\'%s\'' % target

		urltag += '>%s</a>' % name
