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

class UrlDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("UrlDialog")

        self.setSizeGripEnabled(1)


        LayoutWidget = QWidget(self,"Layout1")
        LayoutWidget.setGeometry(QRect(10,180,450,33))
        Layout1 = QHBoxLayout(LayoutWidget,0,6,"Layout1")
        Horizontal_Spacing2 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        Layout1.addItem(Horizontal_Spacing2)

        self.buttonOk = QPushButton(LayoutWidget,"buttonOk")
        self.buttonOk.setAutoDefault(1)
        self.buttonOk.setDefault(1)
        Layout1.addWidget(self.buttonOk)

        self.buttonCancel = QPushButton(LayoutWidget,"buttonCancel")
        self.buttonCancel.setAutoDefault(1)
        Layout1.addWidget(self.buttonCancel)

        self.editUrl = QLineEdit(self,"editUrl")
        self.editUrl.setGeometry(QRect(60,20,400,26))

        self.editTitle = QLineEdit(self,"editTitle")
        self.editTitle.setGeometry(QRect(60,60,400,26))

        self.editName = QLineEdit(self,"editName")
        self.editName.setGeometry(QRect(60,100,400,26))

        self.comboOpen = QComboBox(0,self,"comboOpen")
        self.comboOpen.setGeometry(QRect(320,140,140,26))

        self.comboClass = QComboBox(0,self,"comboClass")
        self.comboClass.setGeometry(QRect(60,140,120,26))

        self.labelUrl = QLabel(self,"labelUrl")
        self.labelUrl.setGeometry(QRect(10,20,40,26))

        self.labelTitle = QLabel(self,"labelTitle")
        self.labelTitle.setGeometry(QRect(10,60,40,26))

        self.labelName = QLabel(self,"labelName")
        self.labelName.setGeometry(QRect(10,100,40,26))

        self.labelClass = QLabel(self,"labelClass")
        self.labelClass.setGeometry(QRect(10,140,40,26))

        self.checkOpen = QCheckBox(self,"checkOpen")
        self.checkOpen.setGeometry(QRect(240,140,70,26))

        self.languageChange()

        self.resize(QSize(471,228).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.buttonOk,SIGNAL("clicked()"),self,SLOT("accept()"))
        self.connect(self.buttonCancel,SIGNAL("clicked()"),self,SLOT("reject()"))


    def languageChange(self):
        self.setCaption(self.__tr("Add URL"))
        self.buttonOk.setText(self.__tr("&OK"))
        self.buttonOk.setAccel(QString.null)
        self.buttonCancel.setText(self.__tr("&Cancel"))
        self.buttonCancel.setAccel(QString.null)
        self.editUrl.setText(self.__tr("http://"))
        self.labelUrl.setText(self.__tr("URL:"))
        self.labelTitle.setText(self.__tr("Title:"))
        self.labelName.setText(self.__tr("Name:"))
        self.labelClass.setText(self.__tr("Class:"))
        self.checkOpen.setText(self.__tr("Open in:"))


    def __tr(self,s,c = None):
        return qApp.translate("UrlDialog",s,c)
