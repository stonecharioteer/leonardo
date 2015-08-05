import os
from PyQt4 import QtGui
from FSNTextEdit import FSNTextEdit
from FileBrowserButton import FileBrowserButton
from FileLocationWidget import FileLocationWidget
from PrimaryButton import PrimaryButton

class LeonardoToolbox(QtGui.QWidget):
    def __init__(self):
        super(LeonardoToolbox,self).__init__()
        self.createUI()

    def createUI(self):
        self.fsn_text_edit = FSNTextEdit()
        self.input_data_set_button = FileBrowserButton()
        self.input_images_location_widget = FileLocationWidget("Input")
        self.output_images_location_widget = FileLocationWidget("Output")
        self.run_button = PrimaryButton("Run")

        tool_layout = QtGui.QGridLayout()
        tool_layout.addWidget(self.fsn_text_edit,0,0,3,3)
        tool_layout.addWidget(self.input_data_set_button,3,0,3,1)
        tool_layout.addWidget(self.input_images_location_widget,4,0,3,1)
        tool_layout.addWidget(self.output_images_location_widget,5,0,3,1)
        tool_layout.addWidget(self.run_button,6,3,1,1)
        toolbox = QtGui.QBoxWidget("Katana")
        toolbox.setLayout(tool_layout)
        final_layout = QtGui.QHBoxLayout()
        final_layout.addWidget(toolbox)
        self.setLayout(final_layout)