from EaseXML import XMLObject,StringAttribute,TextNode,ListNode
import os

class Template(XMLObject):
    Name = StringAttribute()
    Content = TextNode()
    
class Templates(XMLObject):
    List = ListNode('Template',main=True)
    
    def load():
        """ static method to create new list from xml file """
        file = os.path.expanduser("~")+"/.pyqlogger/templates.xml"
        if os.path.exists(file):
            try:
                return XMLObject.instanceFromXml(open(file).read())
            except Exception, e:
                print "Couldn't read templates. Either empty of borken! (%s)"%(str(e))
        return Templates()
            
    load = staticmethod(load)
    
    def save(self):
        """ write template list back to xml file """
        try:
            file = os.path.expanduser("~")+"/.pyqlogger/templates.xml"
            open(file,"w").write(str(self))
        except Exception, e:
            print "Cannot write (%s)"%(str(e))
            
