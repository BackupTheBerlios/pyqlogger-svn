'''
Module for workig with plugins. To recap:
1. plugins should be stored in .py files inside ~/.pyqlogger/plugins/ dir
2. internal plugins are made using static function called SimpleButton
3. each plugin MUST have:
	* on_click  - method
	* title - string attribute
4. it CAN have:
	* image - QPixmap attribute
	* page - string attribute (on what tab page to put the button)
5. all plugins are loaded once and not reloaded. I may redo that later.
'''
import os
from glob import glob
from qt import *

class ToolbarPlugin:
	''' All plugins should inherit from this class '''
	def on_click(self):
		abstract		
	def SimpleButton(parent,title,handler,page=None,image=None):
		button = ToolbarPlugin(parent)
		button.image = image
		button.page = page
		button.title = title
		button.on_click = handler
		return button

	def __init__(self,parent):
		self.parent = parent

	def parent(self):
		return parent
		
	SimpleButton = staticmethod(SimpleButton)

class PluginFactory:
	plugins = [] # to store plugin classes
	buttons = {} # to store generated buttons per tabwidget

	def __init__(self,dir,parent):
		self.dir = dir
		self.parent = parent
		self.scan()
	
	def plugIsOk(self,plug):
		return bool( hasattr(plug,'__bases__') and	ToolbarPlugin in plug.__bases__ \
				and hasattr(plug,'image') and hasattr(plug,'page')\
				and hasattr(plug,'parent') and hasattr(plug,'title') )
		
	def scan(self):
		path = os.path.join(self.dir, '*.p')		
		for filename in glob(path):
			if os.path.isfile(filename):
				lines = open(filename).readlines()
				g = globals()
				l = {} # locals
				try:
					exec "\n".join(lines) in g,l
					for k,v in l.items():
						# check if provided class can be applied
						if self.plugIsOk(v):
							self.plugins += [ v(self.parent) ]
				except:
					pass

	def manualAdd(self,plugin):
		self.plugins += [ plugin ]
			
	def fillToolbar(self, tabWidget):
	
		def getPage(title, tabWidget):
			if not title: return tabWidget.page(0)
			for i in range(0,tabWidget.count()):
				if title == str(tabWidget.label(i)):
					return tabWidget.page(i)

		for pi in self.plugins:
			tabpage = getPage(pi.page, tabWidget)
			button = QPushButton(tabpage)
			if pi.image : 
				bi = QPixmap()
				bi.loadFromData(pi.image,"PNG")
				button.setIconSet(QIconSet(bi))
				button.setMaximumSize(QSize(bi.width()+3,bi.height()+3))
			else:
				button.setText(pi.title)
			button.show()
			if not self.buttons.has_key(tabpage): 
				self.buttons[tabpage] = []
			self.buttons[tabpage] += [ button ]
			self.parent.connect(button,SIGNAL("clicked()"),pi.on_click)
