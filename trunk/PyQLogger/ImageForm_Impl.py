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

__revision__ = "$Id$"
from qt import QPixmap, QFileDialog, QMessageBox
from imageform import ImageForm
import urllib2, PatchedClientForm, re, os

class ImageForm_Impl(ImageForm):
    alignList = {}
    def __init__(self, parent = None, name = None, modal = 0, fl = 0):
        ImageForm.__init__(self, parent, name, modal, fl)
        self.comboAlign.insertItem('None')
        self.alignList['Left'] = 'left'
        self.alignList['Right'] = 'right'
        self.alignList['Center'] = 'center'
        self.btnUpload.setEnabled(False)
        self.buttonOk.setEnabled(False)
        for key in self.alignList.keys():
            self.comboAlign.insertItem(key)

    def imagetag(self):
        imagetag = ''
        image = str(self.editUrl.text())
        thumb = str(self.editThumb.text())
        title = str(self.editTitle.text())
        if str(self.editWidth.text()): 
            width = int(str(self.editWidth.text())) 
        else: 
            width = None
        if str(self.editBorder.text()): 
            border = int(str(self.editBorder.text())) 
        else: 
            border = None
        if str(self.editHeight.text()): 
            height = int(str(self.editHeight.text()))
        else: 
            height = None
        if not image: 
            return None
        else:  
            if thumb:
                imagetag += "<a href='%s'><img src='%s'" % (image, thumb)
            else:
                imagetag += '<img src=\'%s\'' % image
                if width:
                    imagetag += ' width=\'%d\'' % width
                if height:
                    imagetag += ' height=\'%d\'' % height
        if border:  
            imagetag += ' border=\'%d\'' % border
        if title:
            imagetag += ' alt=\'%s\'' % title
        if self.alignList.has_key('%s' % self.comboAlign.currentText()):
            align = self.alignList['%s' % self.comboAlign.currentText()]
            imagetag += ' align=\'%s\'' % align
        imagetag += '>' 
        if thumb:
            imagetag += '</a>'
        return imagetag


    def btnRefresh_clicked(self):
        if str(self.editUrl.text()):
            try:
                img = urllib2.urlopen(str(self.editUrl.text())).read()
                pic = QPixmap()
                pic.loadFromData(img)
                if not str(self.editWidth.text()):
                    self.editWidth.setText(str(pic.width()))
                if not str(self.editHeight.text()):
                    self.editHeight.setText(str(pic.height()))
                self.previewImage.setPixmap(pic)
            except:
                QMessageBox.warning(self, "Warning", "Cannot open the image url!")                

    def editUrl_textChanged(self, a0):
        self.buttonOk.setEnabled(str(self.editUrl.text())!='')

    def chk_stateChanged(self, a0):
        if self.chkUrl.isChecked():
            self.widgetStack2.raiseWidget(self.pageUrl)
            self.buttonOk.setEnabled(str(self.editUrl.text())!='')
        else:
            self.widgetStack2.raiseWidget(self.pageUpload)
            self.buttonOk.setEnabled(False)

    def chkThumb_toggled(self, a0):
        pass

    imgre = re.compile('\[img\](.*?)\[/img\]', re.IGNORECASE)
    
    def uploadArk(self, afile):
        try:
            cform = PatchedClientForm.ParseResponse(urllib2.urlopen("http://www.imageark.net"))
            cform[0].referer = 'http://www.imageark.net'
            cform[0].find_control("userfile").add_file(open(afile,"rb"), filename = os.path.basename(afile))
            req = cform[0].click()
            content = urllib2.urlopen(req).read()
            match = self.imgre.search(content)
            if match:
                return match.group(1)
        except Exception, e:
            print "Upload exception: " + str(e)
            return None

    def uploadShack(self, afile):
        try:
            cform = PatchedClientForm.ParseResponse(urllib2.urlopen("http://imageshack.us/index2.php"))
            cform[0].referer = 'http://imageshack.us/index2.php'
            cform[0].find_control("fileupload").add_file(open(afile,"rb"), filename = os.path.basename(afile))
            content = urllib2.urlopen(cform[0].click()).read()
            match = self.imgre.search(content)
            if match:
                return match.group(1)
        except Exception, e:
            print "Upload exception: " + str(e)
            return None

    def __generateThumb(self, filename):
        if not self.chkThumb.isChecked(): 
	    return None
        try:            
            p = self.previewImage
            fn = os.tmpnam() + os.path.basename(filename)
            w = p.width()
            h = p.height()
            if w > 120:
                w = 120
            if h > 120:
                h = 120
            # if the image is smaller than the thumb, don't create the thumb
            if h < 120 and w < 120:
                return None
            os.system("convert -geometry %dx%d  %s  %s" % (w, h, filename, fn))
            if os.path.exists(fn):
                return fn
        except:
            return None
            
    def btnUpload_clicked(self):
        res = res2 = None
        thumbfile = self.__generateThumb(str(self.editFile.text()))
        if self.chkShack.isChecked():
            res = self.uploadShack(str(self.editFile.text()))            
            if thumbfile and res : 
                res2 = self.uploadShack(thumbfile)
        elif self.chkArk.isChecked():
            res = self.uploadArk(str(self.editFile.text()))
            if thumbfile and res : 
                res2 = self.uploadArk(thumbfile)

        if thumbfile:
            os.unlink(thumbfile)
        if res:
            self.editUrl.setText(res)
            if res2: 
                self.editThumb.setText(res2)

    def __open(self, txt, btn):
        filename = str(QFileDialog.getOpenFileName(None , \
            "Images (*.png *.jpg *.gif)", \
            self, \
            "open image file", \
            "Choose a file to open" ))
        txt.setText(filename)
        ok = False
        try:
            pic = QPixmap()
            if pic.loadFromData(open(filename,"rb").read()):
                ok = True
                if not str(self.editWidth.text()):
                    self.editWidth.setText(str(pic.width()))
                if not str(self.editHeight.text()):
                    self.editHeight.setText(str(pic.height()))
                self.previewImage.setPixmap(pic)
                btn.setEnabled(True)
        except:            
            ok = False
        if not ok:
            QMessageBox.warning(self, "Warning", "Cannot open the image file!")
            self.previewImage.setPixmap(QPixmap())
            btn.setEnabled(False)
        
    def editFile_textChanged(self, a0):
        self.btnUpload.setEnabled( os.path.exists(str(a0)) )

    def btnOpen_clicked(self):
        self.__open(self.editFile, self.btnUpload)
        
