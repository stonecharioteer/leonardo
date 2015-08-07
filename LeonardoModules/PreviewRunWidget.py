import os
from PyQt4 import QtGui

class PreviewRunWidget(QtGui.QWidget):
    def __init__(self):
        super(PreviewRunWidget,self).__init__()
        self.setMinimumSize(500,500)
        
        