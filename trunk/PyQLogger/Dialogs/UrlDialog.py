## This file is part of PyQLogger.
##
## Copyright (c) 2004 Eli Yukelzon a.k.a Reflog &
##                    Xander Soldaat a.k.a. Mightor
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
__revision__ = "$Id: UrlDialog_Impl.py 80 2004-12-20 13:34:44Z reflog $"

from qt import QDialog
from PyQLogger.Settings import DialogSettings

class UrlDialog(QDialog):
    targetList = {}

    def init(self, settings):
        # Hide these two until we've figured out how
        # to deal with them
        self.comboClass.hide()
        self.labelClass.hide()
        self.settings = settings
        self.editUrl.setFocus()
        self.targetList['in new window'] = '_blank'
        self.targetList['in same window'] = '_top'
        self.targetList['in same frame'] = '_self'
        for key in self.targetList.keys():
            self.comboOpen.insertItem(key)
        set = self.settings
        if set.Dialogs and set.Dialogs.UrlDialogTarget:
            target = set.Dialogs.UrlDialogTarget
            self.checkOpen.setChecked(True)
            for counter in range(0, self.comboOpen.count()):
                if self.comboOpen.text(counter) == target:
                    self.comboOpen.setCurrentItem( counter )
                    break

    def initValues(self, text):
        if text:
            self.editName.setText(text)

    def urltag(self):
        urltag = '<a href='
        url = unicode(self.editUrl.text())
        alt = unicode(self.editTitle.text())
        name = unicode(self.editName.text())
    
        if not url or not name:
            return None
        else:
            urltag += '\'%s\'' % url
    
        if alt:
            urltag += ' alt=\'%s\'' % alt
    
        if self.checkOpen.isChecked():
            if self.targetList.has_key(unicode(self.comboOpen.currentText())):
                target = self.targetList[unicode(self.comboOpen.currentText())]
                urltag += ' target=\'%s\'' % target
    
        urltag += '>%s</a>' % name
        return urltag
        
    def accept(self):
        if not self.settings.Dialogs:
            self.settings.Dialogs = DialogSettings()
        if self.checkOpen.isChecked():
            self.settings.Dialogs.UrlDialogTarget = unicode(self.comboOpen.currentText())    
        else:
            self.settings.Dialogs.UrlDialogTarget = ''
            
        QDialog.accept(self)
