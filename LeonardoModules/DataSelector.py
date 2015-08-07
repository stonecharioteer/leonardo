import os
from PyQt4 import QtGui
from FSNTextEdit import FSNTextEdit
from IconButton import IconButton
from FileLocationWidget import FileLocationWidget
from PrimaryButton import PrimaryButton
from QColorButton import QColorButton

class DataSelector(QtGui.QWidget):
    def __init__(self):
        super(DataSelector,self).__init__()
        self.createUI()
        self.mapEvents()

    def createUI(self):
        self.group_box = QtGui.QGroupBox("Data Selection")
        self.use_fsns_and_fk_information_checkbox = QtGui.QCheckBox("Get Attribute Data from Flipkart")
        self.use_fsns_and_fk_information_checkbox.setToolTip("If checked, this enables building images for a list of FSNs by getting attribute data from the website.")
        self.use_csv_file_checkbox = QtGui.QCheckBox("Load Data from CSV")
        self.use_csv_file_checkbox.setToolTip("Get the parent image data, the attributes list and image locations from a csv file.")
        #Button groups need to be defined at the class level. Hence, self.
        self.check_button_group = QtGui.QButtonGroup()
        self.check_button_group.setExclusive(True)
        self.check_button_group.addButton(self.use_fsns_and_fk_information_checkbox)
        self.check_button_group.addButton(self.use_csv_file_checkbox)
        self.use_fsns_and_fk_information_checkbox.setChecked(True)
        

        self.fsn_text_edit = FSNTextEdit()
        self.attributes_list_box = QtGui.QListWidget()
        self.primary_attributes_list_box = QtGui.QListWidget()
        self.secondary_attributes_list_box = QtGui.QListWidget()
        self.push_to_primary_button = QtGui.QPushButton("Add to\nPrimary List")
        self.remove_from_primary_button = QtGui.QPushButton("Remove from\nPrimary List")
        self.push_to_secondary_button = QtGui.QPushButton("Add to\nSecondary List")
        self.remove_from_secondary_button = QtGui.QPushButton("Remove from\nSecondary List")
        self.fetch_images_attributes_button = QtGui.QPushButton("Download Images\nand Specs.")
        self.fetching_progress = QtGui.QProgressBar()

        fsn_mode_layout = QtGui.QGridLayout()
        fsn_mode_layout.addWidget(self.fsn_text_edit,0,0,2,3)
        fsn_mode_layout.addWidget(self.fetch_images_attributes_button,2,0,1,1)
        fsn_mode_layout.addWidget(self.fetching_progress,2,1,1,2)
        fsn_mode_layout.addWidget(self.attributes_list_box,3,0,4,1)
        fsn_mode_layout.addWidget(self.push_to_primary_button,3,1,1,1)
        fsn_mode_layout.addWidget(self.remove_from_primary_button,4,1,1,1)
        fsn_mode_layout.addWidget(self.primary_attributes_list_box,3,2,2,1)
        fsn_mode_layout.addWidget(self.push_to_secondary_button,5,1,1,1)
        fsn_mode_layout.addWidget(self.secondary_attributes_list_box,5,2,2,1)
        fsn_mode_layout.addWidget(self.remove_from_secondary_button,6,1,1,1)

        self.fsn_mode_widget = QtGui.QWidget()
        self.fsn_mode_widget.setLayout(fsn_mode_layout)

        self.input_data_set_button = IconButton(os.path.join("essentials","csv_file.png"))
        self.input_data_set_button.setToolTip("Click to select a data file if you want manual control.")
        csv_mode_layout = QtGui.QGridLayout()
        csv_mode_layout.addWidget(self.input_data_set_button,0,0)
        self.csv_mode_widget = QtGui.QWidget()
        self.csv_mode_widget.setLayout(csv_mode_layout)

        self.fsn_or_csv_stacked_widget = QtGui.QStackedWidget()
        self.fsn_or_csv_stacked_widget.addWidget(self.fsn_mode_widget)
        self.fsn_or_csv_stacked_widget.addWidget(self.csv_mode_widget)

        self.validate_button  = IconButton(os.path.join("essentials","validate.png"))
        layout = QtGui.QGridLayout()
        layout.addWidget(self.use_fsns_and_fk_information_checkbox,0,0,1,1)
        layout.addWidget(self.use_csv_file_checkbox,0,1,1,1)
        layout.addWidget(self.fsn_or_csv_stacked_widget,1,0,1,2)
        layout.addWidget(self.validate_button,3,1)
        self.group_box.setLayout(layout)
        final_layout = QtGui.QHBoxLayout()
        final_layout.addWidget(self.group_box)
        self.setLayout(final_layout)

    def mapEvents(self):
        self.check_button_group.buttonClicked.connect(self.changePage)
    def changePage(self):
        if self.use_fsns_and_fk_information_checkbox.isChecked():
            button_number = 0
        else:
            button_number = 1
        self.fsn_or_csv_stacked_widget.setCurrentIndex(button_number)
