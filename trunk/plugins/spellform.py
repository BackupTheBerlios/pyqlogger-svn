# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/reflog/py/PyQLogger/spellform.ui'
#
# Created: Tue Oct 19 17:35:27 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *

image0_data = \
    "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
    "\x49\x48\x44\x52\x00\x00\x00\x10\x00\x00\x00\x10" \
    "\x08\x06\x00\x00\x00\x1f\xf3\xff\x61\x00\x00\x00" \
    "\xac\x49\x44\x41\x54\x78\x9c\x63\x60\xa0\x02\x70" \
    "\x62\x60\x60\xf8\x8f\x84\x43\xa0\xe2\xff\xd1\xb0" \
    "\x13\x2e\x03\x60\x0a\x90\xf9\xf8\xc4\x51\x00\x0b" \
    "\x11\x2e\x84\x69\x74\x26\x64\x00\x56\x1b\x18\x18" \
    "\x18\x18\x91\xe4\x19\xd1\x25\x99\xd0\x14\x62\x28" \
    "\x20\x04\x98\x08\x2b\x81\x87\x05\xba\x17\xfe\x33" \
    "\x30\x30\x94\x90\x6a\x21\x5c\x73\xf4\xc4\x48\xf4" \
    "\x40\xc6\xb0\x51\x89\x08\xcd\x52\x58\x15\x74\xed" \
    "\xea\xc0\xa5\x80\xa0\x66\x06\x06\x06\x86\x42\x61" \
    "\x1d\xe1\xff\xe5\xcb\xca\xd0\x5d\x42\x94\x66\xb8" \
    "\x4d\x2b\x4e\x2f\xfb\x9f\x3b\x37\x07\x9e\x12\x91" \
    "\x34\xe3\xf2\x1a\x0a\x08\x62\x60\x60\xf8\xbf\xe3" \
    "\xda\x8e\xff\xd1\x13\x23\x49\xb2\x19\xc5\x15\xf3" \
    "\x8f\xce\xfd\x3f\x79\xdf\x24\x92\x6c\xc6\x70\x05" \
    "\x39\x36\x93\x04\x00\x7f\xbe\x53\x30\x43\xc3\x02" \
    "\xc5\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60" \
    "\x82"

class SpellForm(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        self.image0 = QPixmap()
        self.image0.loadFromData(image0_data,"PNG")
        if not name:
            self.setName("SpellForm")

        self.setIcon(self.image0)
        self.setModal(1)

        SpellFormLayout = QHBoxLayout(self,11,6,"SpellFormLayout")

        layout3 = QVBoxLayout(None,0,6,"layout3")

        self.textLabel1 = QLabel(self,"textLabel1")
        layout3.addWidget(self.textLabel1)

        self.viewText = QTextEdit(self,"viewText")
        self.viewText.setTextFormat(QTextEdit.PlainText)
        self.viewText.setReadOnly(1)
        layout3.addWidget(self.viewText)

        self.textLabel2 = QLabel(self,"textLabel2")
        layout3.addWidget(self.textLabel2)

        self.editReplace = QLineEdit(self,"editReplace")
        layout3.addWidget(self.editReplace)

        self.textLabel3 = QLabel(self,"textLabel3")
        layout3.addWidget(self.textLabel3)

        self.listVariants = QListBox(self,"listVariants")
        layout3.addWidget(self.listVariants)
        SpellFormLayout.addLayout(layout3)

        layout3_2 = QVBoxLayout(None,0,6,"layout3_2")

        self.btnIgnore = QPushButton(self,"btnIgnore")
        layout3_2.addWidget(self.btnIgnore)

        self.btnAdd = QPushButton(self,"btnAdd")
        layout3_2.addWidget(self.btnAdd)

        self.btnReplace = QPushButton(self,"btnReplace")
        layout3_2.addWidget(self.btnReplace)

        self.btnReplaceAll = QPushButton(self,"btnReplaceAll")
        layout3_2.addWidget(self.btnReplaceAll)
        spacer1 = QSpacerItem(20,140,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout3_2.addItem(spacer1)

        self.btnCancel = QPushButton(self,"btnCancel")
        layout3_2.addWidget(self.btnCancel)
        SpellFormLayout.addLayout(layout3_2)

        self.languageChange()

        self.resize(QSize(543,426).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.btnIgnore,SIGNAL("clicked()"),self.btnIgnore_clicked)
        self.connect(self.btnAdd,SIGNAL("clicked()"),self.btnAdd_clicked)
        self.connect(self.btnReplace,SIGNAL("clicked()"),self.btnReplace_clicked)
        self.connect(self.btnReplaceAll,SIGNAL("clicked()"),self.btnReplaceAll_clicked)
        self.connect(self.btnCancel,SIGNAL("clicked()"),self.btnCancel_clicked)
        self.connect(self.listVariants,SIGNAL("doubleClicked(QListBoxItem*)"),self.listVariants_doubleClicked)


    def languageChange(self):
        self.setCaption(self.__tr("Spell Checker"))
        self.textLabel1.setText(self.__tr("Text being checked:"))
        self.textLabel2.setText(self.__tr("Replace with:"))
        self.textLabel3.setText(self.__tr("Suggestions:"))
        self.listVariants.clear()
        self.listVariants.insertItem(self.__tr("New Item"))
        self.btnIgnore.setText(self.__tr("Ignore"))
        QToolTip.add(self.btnIgnore,self.__tr("Tell Aspell to allow word for this session."))
        QWhatsThis.add(self.btnIgnore,self.__tr("Tell <b>Aspell</b> to allow word for this session."))
        self.btnAdd.setText(self.__tr("Add"))
        QToolTip.add(self.btnAdd,self.__tr("Tell Aspell to allow word permanently."))
        QWhatsThis.add(self.btnAdd,self.__tr("Tell <b>Aspell</b> to allow word permanently."))
        self.btnReplace.setText(self.__tr("Replace"))
        QToolTip.add(self.btnReplace,self.__tr("Replace misspelled word"))
        QWhatsThis.add(self.btnReplace,self.__tr("Replace misspelled word"))
        self.btnReplaceAll.setText(self.__tr("Replace All"))
        QToolTip.add(self.btnReplaceAll,self.__tr("Tell Aspell about the correction so it can learn about your mistakes."))
        QWhatsThis.add(self.btnReplaceAll,self.__tr("Tell <b>Aspell</b> about the correction so it can learn about your mistakes."))
        self.btnCancel.setText(self.__tr("Cancel"))
        QToolTip.add(self.btnCancel,self.__tr("Cancel the checking and reject changes"))
        QWhatsThis.add(self.btnCancel,self.__tr("Cancel the checking and reject changes"))


    def btnIgnore_clicked(self):
        print "SpellForm.btnIgnore_clicked(): Not implemented yet"

    def btnIgnoreAll_clicked(self):
        print "SpellForm.btnIgnoreAll_clicked(): Not implemented yet"

    def btnAdd_clicked(self):
        print "SpellForm.btnAdd_clicked(): Not implemented yet"

    def btnReplace_clicked(self):
        print "SpellForm.btnReplace_clicked(): Not implemented yet"

    def btnReplaceAll_clicked(self):
        print "SpellForm.btnReplaceAll_clicked(): Not implemented yet"

    def btnOptions_clicked(self):
        print "SpellForm.btnOptions_clicked(): Not implemented yet"

    def btnCancel_clicked(self):
        print "SpellForm.btnCancel_clicked(): Not implemented yet"

    def listVariants_doubleClicked(self,a0):
        print "SpellForm.listVariants_doubleClicked(QListBoxItem*): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("SpellForm",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = SpellForm()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
