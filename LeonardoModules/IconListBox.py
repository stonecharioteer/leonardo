import os
from PyQt4 import QtGui, QtCore
class IconListBox(QtGui.QListWidget):
    def __init__(self,icon_size=None,element_data_list=None):
        super(IconListBox,self).__init__()
        if icon_size is None:
            icon_size = (96,84)
        self.setViewMode(QtGui.QListView.IconMode)
        self.setIconSize(QtCore.QSize(icon_size[0],icon_size[1]))
        self.setMovement(QtGui.QListView.Static)
        self.setSpacing(12)
        self.setMaximumWidth(128)
        if element_data_list is not None:
            self.addElements(element_data_list)
        
    def addElements(self, element_data_list):
        for element in element_data_list:
            element_button = QtGui.QListWidgetItem()
            element_button.setIcon(QtGui.QIcon(element["Icon"]))
            element_button.setText(element["Name"])
            element_button.setTextAlignment(QtCore.Qt.AlignHCenter)
            element_button.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled) #WOOOFRIGGINGYEAH!
            super(IconListBox,self).addItem(element_button)
