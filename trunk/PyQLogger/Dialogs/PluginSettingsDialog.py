from qt import QDialog, QIntValidator, QComboBox, QGridLayout,\
               QLabel, QLineEdit, Qt, QSize, QCheckBox

class PluginSettingsDialog(QDialog):
    def init(self, manager, plugin):
        self.manager = manager
        self.plugin = plugin
        self.lblName.setText(str(plugin.Name))
        self.lblMoreInfo.setText(["",str(plugin.Info)][bool(plugin.Info)])
        self.lblAuthor.setText(["",str(plugin.Author)][bool(plugin.Author)])
        self.lblType.setText(str(plugin.description()))
        self.grpSettings.hide()
        if self.plugin.Data.Options:
            self.setOptions()
        self.resize(self.minimumSizeHint())
        self.clearWState(Qt.WState_Polished)

     
    def setOptions(self):
        def addOption(parent, layout, option , row):
            ql = QLabel(parent)
            ql.setText(option.Name)
            col = 1
            if option.Type == "String" or option.Type == "Integer":
                qw = QLineEdit(parent)
                qw.setText(option.Value)
                if option.Type == "Integer":
                    qw.setValidator( QIntValidator(parent) )
            elif option.Type == "Boolean":
                ql.hide()
                col = 0
                qw = QCheckBox(parent)
                qw.setText(option.Name)
                qw.setChecked(bool(option.Value))
            elif option.Type == "List":
                qw = QComboBox(parent)
                tmp = option.Value.split(";")
                if len(tmp) > 2:
                    sel = int(tmp[0])
                    for it in tmp[1:]:
                        qw.insertItem(it)
                    qw.setCurrentItem(sel)
                else:
                    return
            if ql:
                layout.addWidget(ql, row, 0)
            layout.addWidget(qw, row, col)
            return qw
                
        self.grpSettings.setColumnLayout(0,Qt.Vertical)
        self.grpSettings.layout().setSpacing(6)
        self.grpSettings.layout().setMargin(11) 
        self.grpSettings.show()
        Layout = QGridLayout(self.grpSettings.layout())
        row = 0
        self.opts = {}
        for opt in self.plugin.Data.Options:
            ctrl = addOption(self.grpSettings, Layout,opt,row)
            if ctrl:
                self.opts [ opt ] = ctrl
                row += 1
            
    def accept(self):
        for opt in self.plugin.Data.Options:
            ctrl = self.opts [ opt ]
            if type(ctrl) == QCheckBox:
                val = ["","True"][bool(ctrl.isChecked())]
            elif type(ctrl) == QLineEdit:
                val = unicode(ctrl.text())
            elif type(ctrl) == QComboBox:
                tmp = opt.Value.split(";")
                tmp[0] = str(int(ctrl.currentItem()))
                val = ";".join(tmp)
            opt.Value = val            
        QDialog.accept(self)
        