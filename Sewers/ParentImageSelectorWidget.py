import os, glob, re
import datetime
from PyQt4 import QtGui, QtCore
import Katana

class ParentImageSelectorWidget(QtGui.QWidget):
	def __init__(self, repo_path):
		super(ParentImageSelectorWidget, self).__init__()
		self.repo_path = repo_path
	def setFSNs(self, fsn_list):
		pass
