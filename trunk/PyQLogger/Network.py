from qt import *
import sys
from Queue import Queue

def netOp(status,code,callback):
    return { "Status":status,"Code":code, "Callback":callback } 

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
            self.parent.notifier.status(op["Status"])
            res = op["Code"](self.parent)
            op["Callback"](self.parent,res)
