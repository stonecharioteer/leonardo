import os
from PyQt4 import QtGui
from FSNTextEdit import FSNTextEdit
from IconButton import IconButton
from FileLocationWidget import FileLocationWidget
from PrimaryButton import PrimaryButton
from QColorButton import QColorButton
class LeonardoToolbox(QtGui.QWidget):
    def __init__(self):
        super(LeonardoToolbox,self).__init__()
        self.createUI()

    def createUI(self):
        self.use_fsns_and_fk_information_checkbox = QtGui.QCheckBox("Get Attribute Data from Flipkart")
        self.use_fsns_and_fk_information_checkbox.setToolTip("If checked, this enables building images for a list of FSNs by getting attribute data from the website.")
        self.fsn_text_edit = FSNTextEdit()

        self.input_data_set_button = IconButton(os.path.join("essentials","csv_file.png"))
        self.input_data_set_button.setToolTip("Click to select a data file if you want manual control.")
        self.attributes_dialog_button = IconButton(os.path.join("essentials","wrench.png"))
        self.attributes_dialog_button.setToolTip("Once the attributes are loaded, click this to select the primary and secondary attributes list.")
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
        tool_layout.addWidget(self.use_fsns_and_fk_information_checkbox,0,0,1,3)
        tool_layout.addWidget(self.fsn_text_edit,1,0,3,3)
        tool_layout.addWidget(self.input_data_set_button,4,0,1,1)
        tool_layout.addWidget(self.attributes_dialog_button,4,1,1,1)

        tool_layout.addWidget(self.template_selection_label,5,0,1,1)
        tool_layout.addWidget(self.template_selection_combobox,5,1,1,2)
        tool_layout.addWidget(self.icon_positioning_label,6,0,1,1)
        tool_layout.addWidget(self.icon_positioning_combobox,6,1,1,2)
        tool_layout.addWidget(self.palette_selection_label,7,0,1,1)
        tool_layout.addWidget(self.palette_selection_combobox,7,1,1,1)
        tool_layout.addWidget(self.palette_selection_button,7,2,1,1)
        tool_layout.addWidget(self.output_images_location_widget,8,0,1,3)

        tool_layout.addWidget(self.run_button,9,2,1,1)
        toolbox = QtGui.QGroupBox("Katana")
        toolbox.setLayout(tool_layout)
        final_layout = QtGui.QHBoxLayout()
        final_layout.addWidget(toolbox)
        self.setLayout(final_layout)