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
from qt import QPixmap, QFileDialog, QMessageBox,SIGNAL,QString
from qtnetwork import QHttp,QHttpRequestHeader
from imageform import ImageForm
import urllib2, re, os
from Notifier import Notifier

import mimetypes
import mimetools

def encode_multipart_formdata(fields, files, BOUNDARY = '-----'+mimetools.choose_boundary()+'-----'):
    CRLF = '\r\n'
    L = []
    if isinstance(fields, dict):  fields = fields.items()
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        filetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % filetype)
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body


class ImageForm_Impl(ImageForm):
    alignList = {}
    def __init__(self, parent = None, name = None, modal = 0, fl = 0):
        ImageForm.__init__(self, parent, name, modal, fl)
        self.comboAlign.insertItem('None')
        self.notifier = Notifier(parent, 1,args=[self.progressBar])
        self.alignList['Left'] = 'left'
        self.alignList['Right'] = 'right'
        self.alignList['Center'] = 'center'
        self.btnUpload.setEnabled(False)
        self.buttonOk.setEnabled(False)
        self.http = QHttp()
        self.connect(self.http, SIGNAL( "done(bool)" ), self.httpDone )
        self.connect(self.http, SIGNAL( "dataSendProgress (int, int)"),self.httpProgress)
        self.http2 = QHttp()
        self.connect(self.http2, SIGNAL( "done(bool)" ), self.http2Done )
        self.connect(self.http2, SIGNAL( "dataSendProgress (int, int)"),self.httpProgress)

        for key in self.alignList.keys():
            self.comboAlign.insertItem(key)

    def ImageArkPostData(sel,filename):
        return ([("MAX_FILE_SIZE","512000")],
                    [
                     ("userfile",
                       os.path.basename(filename),
                       open(filename,"rb").read()
                      )
                    ],
                    "www.imageark.net",
                    "/upload.php",
                    "http://www.imageark.net"
                    )
    
    def ImageShackPostData(self,filename):
        return ([],
                    [
                       ( "fileupload",
                         os.path.basename(filename),
                         open(filename,"rb").read()
                       )
                    ],
                    "imageshack.us",
                    "/index2.php",
                    "http://imageshack.us/index2.php",
                    )

    def BeginImageUpload(self, filename, GetPostData ,http):
        (fields,files, host, path, referer) = GetPostData(filename)
        content_type, body = encode_multipart_formdata(fields, files)
        Req = QHttpRequestHeader("POST",path)
        Req.setContentType ( content_type )
        Req.setValue("Host",host)
        Req.setValue("Content-Length", str(len(body)))
        Req.setValue("Referer", referer)
        http.setHost(host)
        http.request(Req,body)
    

    def httpProgress(self,done,total):
        self.notifier.progress(done,total)

    def http2Done(self,error):
        qs = QString(self.http2.readAll())
        match = self.imgre.search(unicode(qs))
        if error:
            QMessageBox.warning(self, "Warning", "Cannot upload! Error:"+self.http2.error())
        else:
            if match:          
                self.editUrl.setText(self.image)
                self.editThumb.setText(match.group(1))
                QMessageBox.information(self, "Info", "Image successfully uploaded!")
            else:
                QMessageBox.warning(self, "Warning", "Cannot upload the thumbnail image file!")
        self.http2.closeConnection()

    def httpDone(self,error):
        qs = QString(self.http.readAll())
        match = self.imgre.search(unicode(qs))
        if error:
            QMessageBox.warning(self, "Warning", "Cannot upload! Error:"+self.http.error())
        else:
            if match:
                self.image = match.group(1)
                if self.thumbfile: # do second upload
                    if self.chkShack.isChecked():
                        self.BeginImageUpload(self.thumbfile,self.ImageShackPostData,self.http2)
                    elif self.chkArk.isChecked():
                        self.BeginImageUpload(self.thumbfile,self.ImageArkPostData,self.http2)
                else: # no need to upload second
                    QMessageBox.information(self, "Info", "Image successfully uploaded!")
                    self.editUrl.setText(self.image)
            else:
                if self.thumbfile:
                    os.unlink(thumbfile)
                QMessageBox.warning(self, "Warning", "Cannot upload the image file!")
        self.http.closeConnection()


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
    

    def __generateThumb(self, filename):
        if not self.chkThumb.isChecked(): 
            return None
        try:            
            p = self.previewImage
            import tempfile
            fn = tempfile.mkstemp('%s' % os.path.basename(filename))[1]
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
        self.image = None
        self.thumbfile = self.__generateThumb(str(self.editFile.text()))
        if self.chkShack.isChecked():
            self.BeginImageUpload(str(self.editFile.text()),self.ImageShackPostData,self.http)
        elif self.chkArk.isChecked():
            self.BeginImageUpload(str(self.editFile.text()),self.ImageArkPostData,self.http)


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
        
