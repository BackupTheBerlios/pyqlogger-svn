from qt import *
import sys
from Queue import Queue

__revision__ = "$Id$"

def netOp(status, code, callback):
    return { "Status":status, "Code":code, "Callback":callback } 

class OpCompleteEvent(QEvent):
    def __init__(self, method, parent, data):
        QEvent.__init__(self, QEvent.User)
        self.parent = parent
        self.method = method
        self.data = data
        
class Network(QThread):
    def __init__(self,parent):
        self.Operations = Queue(0)
        self.parent = parent
        QThread.__init__(self)
        
    def enqueue(self, netop):
        self.Operations.put(netop)
        
    def run(self):
        while True:
            op = self.Operations.get()
            self.parent.notifier.status(op["Status"],True)
            res = op["Code"](self.parent)
            self.postEvent(self.parent, OpCompleteEvent(op["Callback"],self.parent, res))
