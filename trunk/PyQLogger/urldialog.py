# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'urldialog.ui'
#
# Created: Sun Dec 26 14:20:10 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.12
#
# WARNING! All changes made in this file will be lost!


from qt import *

image0_data = \
    "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
    "\x49\x48\x44\x52\x00\x00\x00\x10\x00\x00\x00\x10" \
    "\x08\x06\x00\x00\x00\x1f\xf3\xff\x61\x00\x00\x01" \
    "\xb6\x49\x44\x41\x54\x38\x8d\x95\xd3\x3f\x48\x95" \
    "\x51\x18\xc7\xf1\xcf\x79\xef\xeb\x9f\x50\x44\x29" \
    "\x22\x22\xc9\xa8\xd6\x90\x08\x1a\x02\xb7\xf6\x68" \
    "\x68\x68\x68\xb8\x5c\xa2\xc1\x96\x96\x06\x21\x68" \
    "\x8d\x5a\x82\xb0\x28\x1a\x1a\x0a\x0a\x89\x36\x09" \
    "\xa4\x70\x6c\x34\x8a\x22\x0d\x6a\x28\x43\x6f\xbd" \
    "\x75\x49\xed\x7a\x7d\x4f\xc3\xab\x5e\x4d\xc9\xfa" \
    "\xc1\xc3\x39\xcf\x39\x3c\xdf\xe7\xfc\x79\x9e\x10" \
    "\x63\x04\xce\x86\x4c\xee\xdf\x14\x70\x3b\x76\x43" \
    "\x88\x31\x52\x0e\x51\x0b\xb1\xbd\x8b\xa4\xf4\xf7" \
    "\xe0\x98\x0b\x0b\x35\xea\x39\x77\x63\x48\x95\x43" \
    "\x66\xef\x21\x4e\x5d\xa3\xb7\x9f\xa4\x65\x0b\x40" \
    "\x83\xcf\x6f\x78\x72\x89\x72\xc8\xc4\x4a\x92\xc5" \
    "\x57\xa3\xf1\xbf\x35\x33\x15\xe3\x60\x47\x96\xea" \
    "\xea\x66\xdf\xd1\x66\x86\xaf\x1f\xc5\x5a\xb5\xb8" \
    "\xe7\xba\xcc\x84\xae\x1d\xf4\xf4\x16\xfe\xf6\x3e" \
    "\x76\x1d\x94\xda\xd6\x43\xda\x5e\x2c\x8e\xdf\xe4" \
    "\xe1\x90\xd0\x12\x36\x05\x88\x29\x83\x23\x1c\x38" \
    "\x46\x48\xe8\xdc\x29\x15\x92\xc2\x81\xb1\xeb\xec" \
    "\x3f\x2c\x56\xee\x6f\x04\x20\x3c\x1e\x62\x72\xbc" \
    "\x00\x40\xda\x2a\x6d\xe2\xd1\x77\x84\x97\x63\xc2" \
    "\xc8\x45\x92\x4d\x08\xaf\x9f\x73\xfc\x7c\xd3\xcf" \
    "\x73\x45\xea\xb8\x5c\x00\xa7\x87\x39\x71\x59\x94" \
    "\x88\x8b\x75\xb1\xb1\xc6\x16\xeb\x2c\xcd\xf1\xe2" \
    "\x01\x2b\xb5\x33\xff\x63\xe5\x04\xcb\x6a\xeb\x60" \
    "\xa0\x22\x0c\x54\x36\x66\x87\x7b\x15\x7a\x76\x13" \
    "\x02\xf5\x9f\xcc\x4e\xfe\x01\xd8\x4a\x67\xee\x14" \
    "\xe3\x42\x8d\xa7\x57\xa8\x4e\x4b\x85\xd0\x7c\xc4" \
    "\xcd\x34\x33\xc5\xe8\x55\xb1\xfa\x81\x04\x79\x43" \
    "\x98\x7d\xcf\xf4\x14\x25\x52\xf3\xdf\x69\xfc\x22" \
    "\x6d\xdb\x18\x3c\x97\x31\x7c\x92\xb7\x13\xc2\x4a" \
    "\x81\x06\x05\xa8\x54\xcc\x13\xd5\x2f\x3c\xbb\xc1" \
    "\x52\x9d\xbc\xd1\xb4\x85\x1a\x8f\x2e\x30\x39\x41" \
    "\x27\xda\x96\xad\x15\xa9\xd5\x6f\x2e\x9a\xe9\x5c" \
    "\x12\xed\xe9\xa7\xb4\xa6\x0f\xe6\xbe\xf1\xe9\x9d" \
    "\xbf\xbe\xd2\xad\x18\xc2\x6a\x3b\x97\x43\xb6\x6e" \
    "\x33\xd8\x2a\xb8\x1b\x7e\x03\x55\x32\xd0\x4e\xb6" \
    "\x8a\x95\xb5\x00\x00\x00\x00\x49\x45\x4e\x44\xae" \
    "\x42\x60\x82"

class UrlDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        self.image0 = QPixmap()
        self.image0.loadFromData(image0_data,"PNG")
        if not name:
            self.setName("UrlDialog")

        self.setIcon(self.image0)
        self.setSizeGripEnabled(1)

        UrlDialogLayout = QVBoxLayout(self,11,6,"UrlDialogLayout")

        layout9 = QVBoxLayout(None,0,6,"layout9")

        layout3 = QHBoxLayout(None,0,6,"layout3")

        self.labelUrl = QLabel(self,"labelUrl")
        self.labelUrl.setMinimumSize(QSize(40,0))
        layout3.addWidget(self.labelUrl)

        self.editUrl = QLineEdit(self,"editUrl")
        layout3.addWidget(self.editUrl)
        layout9.addLayout(layout3)

        layout4 = QHBoxLayout(None,0,6,"layout4")

        self.labelName = QLabel(self,"labelName")
        self.labelName.setMinimumSize(QSize(40,0))
        layout4.addWidget(self.labelName)

        self.editName = QLineEdit(self,"editName")
        layout4.addWidget(self.editName)
        layout9.addLayout(layout4)

        layout5 = QHBoxLayout(None,0,6,"layout5")

        self.labelTitle = QLabel(self,"labelTitle")
        self.labelTitle.setMinimumSize(QSize(40,0))
        layout5.addWidget(self.labelTitle)

        self.editTitle = QLineEdit(self,"editTitle")
        layout5.addWidget(self.editTitle)
        layout9.addLayout(layout5)

        layout8 = QHBoxLayout(None,0,6,"layout8")

        layout6 = QHBoxLayout(None,0,6,"layout6")

        self.labelClass = QLabel(self,"labelClass")
        layout6.addWidget(self.labelClass)

        self.comboClass = QComboBox(0,self,"comboClass")
        layout6.addWidget(self.comboClass)
        layout8.addLayout(layout6)

        layout7 = QHBoxLayout(None,0,6,"layout7")

        self.checkOpen = QCheckBox(self,"checkOpen")
        layout7.addWidget(self.checkOpen)

        self.comboOpen = QComboBox(0,self,"comboOpen")
        layout7.addWidget(self.comboOpen)
        layout8.addLayout(layout7)
        layout9.addLayout(layout8)
        UrlDialogLayout.addLayout(layout9)

        Layout1 = QHBoxLayout(None,0,6,"Layout1")
        Horizontal_Spacing2 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        Layout1.addItem(Horizontal_Spacing2)

        self.buttonOk = QPushButton(self,"buttonOk")
        self.buttonOk.setAutoDefault(1)
        self.buttonOk.setDefault(1)
        Layout1.addWidget(self.buttonOk)

        self.buttonCancel = QPushButton(self,"buttonCancel")
        self.buttonCancel.setAutoDefault(1)
        Layout1.addWidget(self.buttonCancel)
        UrlDialogLayout.addLayout(Layout1)

        self.languageChange()

        self.resize(QSize(453,187).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.buttonOk,SIGNAL("clicked()"),self,SLOT("accept()"))
        self.connect(self.buttonCancel,SIGNAL("clicked()"),self,SLOT("reject()"))


    def languageChange(self):
        self.setCaption(self.__tr("Add URL"))
        self.labelUrl.setText(self.__tr("URL:"))
        self.editUrl.setText(self.__tr("http://"))
        self.labelName.setText(self.__tr("Text:"))
        self.labelTitle.setText(self.__tr("Alt:"))
        self.labelClass.setText(self.__tr("Class:"))
        self.checkOpen.setText(self.__tr("Open in:"))
        self.buttonOk.setText(self.__tr("&OK"))
        self.buttonOk.setAccel(QString.null)
        self.buttonCancel.setText(self.__tr("&Cancel"))
        self.buttonCancel.setAccel(QString.null)


    def __tr(self,s,c = None):
        return qApp.translate("UrlDialog",s,c)
