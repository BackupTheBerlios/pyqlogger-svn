# -*- coding: utf-8 -*-

from qt import *
from imageform import ImageForm
import urllib2

class ImageForm_Impl(ImageForm):
    alignList = {}
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        ImageForm.__init__(self,parent,name,modal,fl)
        self.comboAlign.insertItem('None')
        self.alignList['Left'] = 'left'
        self.alignList['Right'] = 'right'
        self.alignList['Center'] = 'center'
        self.btnUpload.setEnabled(False)
	self.chkArk.setEnabled(False)
	self.chkShack.setEnabled(False)
	self.buttonOk.setEnabled(False)
        for key in self.alignList.keys():
            self.comboAlign.insertItem(key)

    def imagetag(self):
        imagetag = ''
        image = str(self.editUrl.text())
        thumb = str(self.editThumb.text())
        title = str(self.editTitle.text())
        if str(self.editWidth.text()): width = int(str(self.editWidth.text())) 
	else: width = None
        if str(self.editBorder.text()): border = int(str(self.editBorder.text())) 
	else: border = None
        if str(self.editHeight.text()): height = int(str(self.editHeight.text()))
	else: height = None
        if not image: return None
        else:  
            if thumb:
                width = 40
                height = 40
                imagetag += "<a href='%s'><img src='%s'" % (image,thumb)
            else:
                imagetag += '<img src=\'%s\'' % image

        if width:  imagetag += ' width=\'%d\'' % width
        if border:  imagetag += ' border=\'%d\'' % border
        if height:  imagetag += ' height=\'%d\'' % height
        if title:  imagetag += ' alt=\'%s\'' % title
        if self.alignList.has_key('%s' % self.comboAlign.currentText()):
            align = self.alignList['%s' % self.comboAlign.currentText()]
            imagetag += ' align=\'%s\'' % align
        imagetag += '>' 
        if thumb: imagetag += '</a>'
        return imagetag


    def btnRefresh_clicked(self):
        if str(self.editUrl.text()):
            try:
                img = urllib2.urlopen(str(self.editUrl.text())).read()
                p = QPixmap()
                p.loadFromData(img)
                if not str(self.editWidth.text()):
                    self.editWidth.setText(str(p.width()))
                if not str(self.editHeight.text()):
                    self.editHeight.setText(str(p.height()))
                self.previewImage.setPixmap(p)
            except:
                QMessageBox.warning(self,"Warning","Cannot open the image url!")                

    # public slot
    def editUrl_textChanged(self,a0):
        self.buttonOk.setEnabled(str(self.editUrl.text())!='')

    def chk_stateChanged(self,a0):
        if self.chkUrl.isChecked():
            self.widgetStack2.raiseWidget(self.pageUrl)
            self.buttonOk.setEnabled(str(self.editUrl.text())!='')
        else:
            self.widgetStack2.raiseWidget(self.pageUpload)
            self.buttonOk.setEnabled(self.btnUpload.isEnabled())

    def chkThumb_toggled(self,a0):
        pass

    def btnUpload_clicked(self):
        pass

    def btnOpen_clicked(self):
        s = str(QFileDialog.getOpenFileName(None , \
            "Images (*.png *.jpg *.gif)", \
            self, \
            "open image file", \
            "Choose a file to open" ))
        self.editFile.setText(s)
        try:
            p = QPixmap()
            p.loadFromData(open(s,"rb").read())
            if not str(self.editWidth.text()):
                self.editWidth.setText(str(p.width()))
            if not str(self.editHeight.text()):
                self.editHeight.setText(str(p.height()))
            self.previewImage.setPixmap(p)
            self.btnUpload.setEnabled(True)
        except:
            QMessageBox.warning(self,"Warning","Cannot open the image file!")
            self.btnUpload.setEnabled(False)
        self.buttonOk.setEnabled(self.btnUpload.isEnabled())
