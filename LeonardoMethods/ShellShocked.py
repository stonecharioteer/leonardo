import os
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

def setWindowTheme()
	QtGui.qApp.setStyle(QtCore.QString(u'Plastique'))

