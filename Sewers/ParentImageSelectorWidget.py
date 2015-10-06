from __future__ import division
import os, glob, re
import datetime
from PyQt4 import QtGui, QtCore
import Katana
from ImageButton import ImageButton
from ImageButtonLine import ImageButtonLine

class ParentImageSelectorWidget(QtGui.QWidget):
    def __init__(self, repo_path):
        super(ParentImageSelectorWidget, self).__init__()
        self.repo_path = repo_path
        self.createUI()
        #self.mapEvents()
        self.fsn_data_dict = {}

    def createUI(self):
        self.fsn_icon_table = QtGui.QTableWidget()
        self.fsn_icon_table.setColumnCount(2)
        self.fsn_icon_table.setRowCount(0)
        self.fsn_icon_table.setToolTip("Select parent images from this list.")
        self.fsn_icon_table.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.fsn_icon_table.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.fsn_icon_table)
        self.setLayout(layout)


    def setFSNs(self, fsn_list):
        self.fsn_data_dict = {}
        self.fsn_icon_table.setRowCount(0)
        row_counter = 0
        fsn_list.sort()
        self.fsn_icon_table.setRowCount(0)
        for fsn_string in fsn_list:
            #get a list of all possible parent images in the repo\Parent Images\ folder.
            fsn = fsn_string[fsn_string.rfind(" ")+1:].strip()

            parent_images_paths_list = Katana.getParentImagesList(fsn, self.repo_path)
            self.fsn_data_dict[fsn] = {
                            "Paths": parent_images_paths_list,
                            "Buttons": ImageButtonLine(parent_images_paths_list)
                            }
            #Add a row in the QTable. The first cell is the FSN.
            self.fsn_icon_table.insertRow(row_counter)
            fsn_column_index = 0
            self.fsn_icon_table.setItem(row_counter, fsn_column_index, QtGui.QTableWidgetItem(str(fsn_string)))
            buttons_column_index = 1
            #The second cell is a buttons group which contains an image button for each possible image.
            self.fsn_icon_table.setCellWidget(row_counter, buttons_column_index, self.fsn_data_dict[fsn]["Buttons"])
            self.fsn_icon_table.setHorizontalHeaderLabels(["FSN", "Images"])
            self.fsn_icon_table.resizeColumnsToContents()
            self.fsn_icon_table.resizeRowsToContents()

            row_counter+=1
    
    def getParentImagesData(self):
        fsn_parent_image_paths = {}
        for fsn in self.fsn_data_dict.keys():
            fsn_parent_image_paths[fsn] = self.fsn_data_dict[fsn]["Buttons"].getChosenParentImagePath()
        return fsn_parent_image_paths