import datetime, os, glob
from PyQt4 import QtCore

class FKRetriever(QtCore.QThread):
	sendData = QtCore.pyqtSignal(list)

	def __init__(self,*args,**kwargs):
		super(FKRetriever,self).__init__(*args, **kwargs)

	def run(self):
		pass

	def __del__(self):
		pass