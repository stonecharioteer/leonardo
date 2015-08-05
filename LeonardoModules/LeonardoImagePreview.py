import os
from PyQt4 import QtGui

class LeonardoImagePreview(QtGui.QWidget):
    def __init__(self):
        super(LeonardoImagePreview,self).__init__()
        self.setMinimumSize(500,500)
        
        