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
from imagedialog import ImageDialog


class ImageDialog_Impl(ImageDialog):


	alignList = {}

        def __init__(self,parent = None,name = None,modal = 0,fl = 0):
                ImageDialog.__init__(self,parent,name,modal,fl)

		self.editImage.setFocus()
		self.comboAlign.insertItem('None')
		self.alignList['Left'] = 'left'
		self.alignList['Right'] = 'right'
		self.alignList['Center'] = 'center'
		for key in self.alignList.keys():
			self.comboAlign.insertItem(key)

	def imagetag(self):
		imagetag = '<img src='
		image = self.editImage.text()
		title = self.editTitle.text()

		if not image: 
			return None
		else:
			imagetag += '\'%s\'' % image

		if title:
			imagetag += ' alt=\'%s\'' % title

		if self.alignList.has_key('%s' % self.comboAlign.currentText()):
			align = self.alignList['%s' % self.comboAlign.currentText()]
			imagetag += ' align=\'%s\'' % align

		imagetag += '>' 
		return imagetag
