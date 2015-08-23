import os, time
from PyQt4 import QtGui, QtCore

def showSplashScreen(min_time=None):
    if min_time is None:
        min_time = 3
    image = os.path.join("essentials","half-shell.png")
    splash_pix = QtGui.QPixmap(image)
    splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    time.sleep(min_time)
    return splash

def setWindowTheme():
    #import random
    #style = random.choice(QtGui.QStyleFactory.keys())
    #print "Chosen application style is :%s" %style
    #QtGui.qApp.setStyle(style)
    QtGui.qApp.setStyle(QtCore.QString(u'Plastique'))

