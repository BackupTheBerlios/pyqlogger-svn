# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/reflog/Personal/pyqlogger/trunk/PyQLogger/urldialog.ui'
#
# Created: Thu Dec 2 17:58:57 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class UrlDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("UrlDialog")

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

        self.connect(self.buttonOk,SIGNAL("clicked()"),self.accept)
        self.connect(self.buttonCancel,SIGNAL("clicked()"),self.reject)


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

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = UrlDialog()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
