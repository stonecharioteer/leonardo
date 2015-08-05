from PyQt4 import QtCore
import LeonardoMethods

class Splinter(QtCore.QThread):
    def __init__(self):
        super(Splinter,self).__init__()