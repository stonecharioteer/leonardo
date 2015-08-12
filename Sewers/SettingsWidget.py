import os
from PyQt4 import QtGui
from FSNTextEdit import FSNTextEdit
from IconButton import IconButton
from FileLocationWidget import FileLocationWidget
from PrimaryButton import PrimaryButton
from QColorButton import QColorButton

class SettingsWidget(QtGui.QWidget):
    def __init__(self):
        super(SettingsWidget,self).__init__()
        self.createUI()
        self.mapEvents()
        
    def createUI(self):
        pass
    def mapEvents(self):
        pass