import os
from PyQt4 import QtGui
from FSNTextEdit import FSNTextEdit
from FileBrowserButton import FileBrowserButton
from FileLocationWidget import FileLocationWidget
from PrimaryButton import PrimaryButton
from QColorButton import QColorButton
class LeonardoToolbox(QtGui.QWidget):
    def __init__(self):
        super(LeonardoToolbox,self).__init__()
        self.createUI()

    def createUI(self):
        self.fsn_text_edit = FSNTextEdit()
        self.input_data_set_button = FileBrowserButton()
        self.output_images_location_widget = FileLocationWidget("Output:")
        self.template_selection_label = QtGui.QLabel("Template:")
        self.template_selection_combobox = QtGui.QComboBox()
        self.template_list = ["Parent to One Side","Parent-Centric","Feature-Heavy","Random"]
        self.template_selection_combobox.addItems(self.template_list)
        self.icon_positioning_label = QtGui.QLabel("Icon Positioning:")
        self.icon_positioning_combobox = QtGui.QComboBox()
        self.icon_positions = ["Rectangular","Planetary"]
        self.icon_positioning_combobox.addItems(self.icon_positions)
        self.palette_selection_label = QtGui.QLabel("Icon Palette:")
        self.palette_selection_combobox = QtGui.QComboBox()
        self.palettes_list = ["Black","Based on Input Color","From Input File"]
        self.palette_selection_combobox.addItems(self.palettes_list)
        self.palette_selection_button = QColorButton()
        self.run_button = PrimaryButton("Run")

        tool_layout = QtGui.QGridLayout()
        tool_layout.addWidget(self.fsn_text_edit,0,0,3,3)
        tool_layout.addWidget(self.input_data_set_button,3,1,1,1)
        tool_layout.addWidget(self.template_selection_label,4,0,1,1)
        tool_layout.addWidget(self.template_selection_combobox,4,1,1,2)
        tool_layout.addWidget(self.icon_positioning_label,5,0,1,1)
        tool_layout.addWidget(self.icon_positioning_combobox,5,1,1,2)
        tool_layout.addWidget(self.palette_selection_label,6,0,1,1)
        tool_layout.addWidget(self.palette_selection_combobox,6,1,1,1)
        tool_layout.addWidget(self.palette_selection_button,6,2,1,1)
        tool_layout.addWidget(self.output_images_location_widget,7,0,1,3)

        tool_layout.addWidget(self.run_button,8,2,1,1)
        toolbox = QtGui.QGroupBox("Katana")
        toolbox.setLayout(tool_layout)
        final_layout = QtGui.QHBoxLayout()
        final_layout.addWidget(toolbox)
        self.setLayout(final_layout)