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


class ImageDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("ImageDialog")

        self.setSizeGripEnabled(1)


        LayoutWidget = QWidget(self,"Layout1")
        LayoutWidget.setGeometry(QRect(10,140,450,33))
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

        self.editImage = QLineEdit(self,"editImage")
        self.editImage.setGeometry(QRect(60,20,400,25))

        self.editTitle = QLineEdit(self,"editTitle")
        self.editTitle.setGeometry(QRect(60,60,400,26))

        self.comboAlign = QComboBox(0,self,"comboAlign")
        self.comboAlign.setGeometry(QRect(60,100,100,26))

        self.editHeight = QLineEdit(self,"editHeight")
        self.editHeight.setGeometry(QRect(320,100,40,26))

        self.editBorder = QLineEdit(self,"editBorder")
        self.editBorder.setGeometry(QRect(420,100,40,26))

        self.editWidth = QLineEdit(self,"editWidth")
        self.editWidth.setGeometry(QRect(220,100,40,26))

        self.labelImage = QLabel(self,"labelImage")
        self.labelImage.setGeometry(QRect(10,20,40,25))

        self.labelTitle = QLabel(self,"labelTitle")
        self.labelTitle.setGeometry(QRect(10,60,40,26))

        self.labelAlign = QLabel(self,"labelAlign")
        self.labelAlign.setGeometry(QRect(10,100,40,26))

        self.labelWidth = QLabel(self,"labelWidth")
        self.labelWidth.setGeometry(QRect(180,100,40,26))

        self.labelHeight = QLabel(self,"labelHeight")
        self.labelHeight.setGeometry(QRect(280,100,40,26))

        self.labelBorder = QLabel(self,"labelBorder")
        self.labelBorder.setGeometry(QRect(380,100,40,26))

        self.languageChange()

        self.resize(QSize(471,185).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.buttonOk,SIGNAL("clicked()"),self,SLOT("accept()"))
        self.connect(self.buttonCancel,SIGNAL("clicked()"),self,SLOT("reject()"))

        self.setTabOrder(self.editImage,self.editTitle)
        self.setTabOrder(self.editTitle,self.comboAlign)
        self.setTabOrder(self.comboAlign,self.editWidth)
        self.setTabOrder(self.editWidth,self.editHeight)
        self.setTabOrder(self.editHeight,self.editBorder)
        self.setTabOrder(self.editBorder,self.buttonOk)
        self.setTabOrder(self.buttonOk,self.buttonCancel)


    def languageChange(self):
        self.setCaption(self.__tr("MyDialog"))
        self.buttonOk.setText(self.__tr("&OK"))
        self.buttonOk.setAccel(QString.null)
        self.buttonCancel.setText(self.__tr("&Cancel"))
        self.buttonCancel.setAccel(QString.null)
        self.editImage.setText(self.__tr("http://"))
        self.editWidth.setText(QString.null)
        self.labelImage.setText(self.__tr("Image:"))
        self.labelTitle.setText(self.__tr("Title:"))
        self.labelAlign.setText(self.__tr("Align:"))
        self.labelWidth.setText(self.__tr("Width:"))
        self.labelHeight.setText(self.__tr("Height:"))
        self.labelBorder.setText(self.__tr("Border:"))


    def __tr(self,s,c = None):
        return qApp.translate("ImageDialog",s,c)
