import os
from PyQt4 import QtGui, QtCore
from FSNTextEdit import FSNTextEdit
from IconButton import IconButton
from FileLocationWidget import FileLocationWidget
from PrimaryButton import PrimaryButton
from QColorButton import QColorButton
class TemplateSelector(QtGui.QWidget):
    def __init__(self):
        super(TemplateSelector,self).__init__()
        self.createUI()
        self.mapEvents()
    def createUI(self):
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
        palette_options = QtGui.QHBoxLayout()
        palette_options.addWidget(self.palette_selection_combobox,1)
        palette_options.addWidget(self.palette_selection_button,0)
        self.background_selection_label = QtGui.QLabel("Background Image:")
        self.background_selection_combobox = QtGui.QComboBox()
        self.backgrounds = ["Background 1", "Background 2", "Background 3", "Random"]
        self.background_selection_combobox.addItems(self.backgrounds)

        self.primary_attr_icon_size_label = QtGui.QLabel("Set Primary Attribute Icon\nRelative Size:")
        self.primary_attr_icon_size_spin_box = QtGui.QSpinBox()
        self.primary_attr_icon_size_spin_box.setSuffix("%")
        self.primary_attr_icon_size_spin_box.setRange(5,20)
        self.secondary_attr_icon_size_label = QtGui.QLabel("Set Secondary Attribute Icon\nRelative Size:")
        self.secondary_attr_icon_size_spin_box = QtGui.QSpinBox()
        self.secondary_attr_icon_size_spin_box  .setSuffix("%")
        self.secondary_attr_icon_size_spin_box.setRange(1,4)
        self.validate_button  = IconButton(os.path.join("essentials","validate.png"))
        self.validate_button.setToolTip("Validate and Proceed")
        
        layout = QtGui.QGridLayout()
        layout.addWidget(self.template_selection_label,0,0,1,1,QtCore.Qt.AlignLeft)
        layout.addWidget(self.template_selection_combobox,0,1,1,1,QtCore.Qt.AlignRight)
        layout.addWidget(self.icon_positioning_label,1,0,1,1,QtCore.Qt.AlignLeft)
        layout.addWidget(self.icon_positioning_combobox,1,1,1,1,QtCore.Qt.AlignRight)
        layout.addWidget(self.palette_selection_label,2,0,1,1,QtCore.Qt.AlignLeft)
        layout.addLayout(palette_options,2,1,1,1,QtCore.Qt.AlignRight)
        layout.addWidget(self.background_selection_label,3,0,1,1,QtCore.Qt.AlignLeft)
        layout.addWidget(self.background_selection_combobox,3,1,1,1,QtCore.Qt.AlignRight)
        layout.addWidget(self.primary_attr_icon_size_label,4,0,1,1,QtCore.Qt.AlignLeft)
        layout.addWidget(self.primary_attr_icon_size_spin_box,4,1,1,1,QtCore.Qt.AlignRight)
        layout.addWidget(self.secondary_attr_icon_size_label,5,0,1,1,QtCore.Qt.AlignLeft)
        layout.addWidget(self.secondary_attr_icon_size_spin_box,5,1,1,1,QtCore.Qt.AlignRight)
        layout.addWidget(self.output_images_location_widget,6,0,1,2)
        layout.addWidget(self.validate_button,10,1,1,2,QtCore.Qt.AlignRight)
        for row in range(layout.rowCount()):
            layout.setRowStretch(row,0)
            layout.setRowMinimumHeight(row,0)
        layout.setRowStretch(7,10)
        layout.setRowMinimumHeight(7,10)

            
        
        self.group_box = QtGui.QGroupBox("Design")
        self.group_box.setLayout(layout)
        final_layout = QtGui.QHBoxLayout()
        final_layout.addWidget(self.group_box)
        self.setLayout(final_layout)
    def mapEvents(self):
        pass