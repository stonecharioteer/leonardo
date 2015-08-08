import os, csv
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
        self.data_is_ready = False
        self.data = None
        self.setMode()
        self.validate_button.setEnabled(False)

    def setMode(self):
        self.mode = "FSNs" if self.use_fsns_and_fk_information_checkbox.isChecked() else "CSV"

    def createUI(self):
        self.group_box = QtGui.QGroupBox("Data Selection")
        self.use_fsns_and_fk_information_checkbox = QtGui.QCheckBox("Get Attribute Data from Flipkart")
        self.use_fsns_and_fk_information_checkbox.setToolTip("If checked, this enables building images for a list of FSNs by getting attribute data from the website.")
        self.use_csv_file_checkbox = QtGui.QCheckBox("Load Data from CSV")
        self.use_csv_file_checkbox.setToolTip("Get the parent image data, the attributes list and image locations from a csv file. Use this when you want to get data for more than one category at the same time.")
        #Button groups need to be defined at the class level. Hence, self.
        self.check_button_group = QtGui.QButtonGroup()
        self.check_button_group.setExclusive(True)
        self.check_button_group.addButton(self.use_fsns_and_fk_information_checkbox)
        self.check_button_group.addButton(self.use_csv_file_checkbox)
        self.use_fsns_and_fk_information_checkbox.setChecked(True)
        

        self.fsn_text_edit = FSNTextEdit()
        self.category_label = QtGui.QLabel("Category:")
        self.category_combo_box = QtGui.QComboBox()
        self.category_combo_box.addItems(["Cameras","Mobiles","Tablets"]) #Later, add this data from OINK's server.        
        self.attributes_list_box = QtGui.QListWidget()
        self.primary_attributes_list_box = QtGui.QListWidget()
        self.secondary_attributes_list_box = QtGui.QListWidget()
        self.push_to_primary_button = QtGui.QPushButton("Add to\nPrimary List")
        self.remove_from_primary_button = QtGui.QPushButton("Remove from\nPrimary List")
        self.push_to_secondary_button = QtGui.QPushButton("Add to\nSecondary List")
        self.remove_from_secondary_button = QtGui.QPushButton("Remove from\nSecondary List")
        self.fetch_images_attributes_button = QtGui.QPushButton("Download Images\nand Specs.")
        self.fetch_images_attributes_button.setToolTip("This will check if parent images are available for all the FSNs and download them if necessary from the FK site. It will also load the spec table.")
        self.fetching_progress = QtGui.QProgressBar()

        fsn_mode_layout = QtGui.QGridLayout()
        fsn_mode_layout.addWidget(self.fsn_text_edit,0,0,2,3)
        fsn_mode_layout.addWidget(self.fetch_images_attributes_button,2,0,1,1)
        fsn_mode_layout.addWidget(self.fetching_progress,2,1,1,2)
        fsn_mode_layout.addWidget(self.category_label,3,0,1,1)
        fsn_mode_layout.addWidget(self.category_combo_box,3,1,1,1)
        fsn_mode_layout.addWidget(self.attributes_list_box,4,0,4,1)
        fsn_mode_layout.addWidget(self.push_to_primary_button,4,1,1,1)
        fsn_mode_layout.addWidget(self.remove_from_primary_button,5,1,1,1)
        fsn_mode_layout.addWidget(self.primary_attributes_list_box,4,2,2,1)
        fsn_mode_layout.addWidget(self.push_to_secondary_button,6,1,1,1)
        fsn_mode_layout.addWidget(self.secondary_attributes_list_box,6,2,2,1)
        fsn_mode_layout.addWidget(self.remove_from_secondary_button,7,1,1,1)

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
        self.input_data_set_button.clicked.connect(self.loadDataFromFile)

    def changePage(self):
        button_number = 0 if self.use_fsns_and_fk_information_checkbox.isChecked() else 1
        self.fsn_or_csv_stacked_widget.setCurrentIndex(button_number)
        self.setMode()

    def loadDataFromFile(self):
        """This method asks for a csv data file. Upon loading, it'll read the file, 
            check it and declare whether it's valid or not.
            It does it based on:
            1. File headers: 
                FSN, Category, Primary USP[1-5] Attribute; Primary USP[1-5] Description; Secondary USP[1-5] Attribute; Secondary USP[1-5] Description;
            2. At least 1 row of data.
        """
        #Get the file name.
        data_file_name = QtGui.QFileDialog.getOpenFileName(self,"Open Data File",os.getcwd(),("Comma Separated Values Files (*.csv)"))
        #Load the file.
        data_file_handler = open(data_file_name,"r")
        data_file_as_csv = csv.DictReader(data_file_handler)
        file_headers = []
        for row in data_file_as_csv:
            file_headers = row.keys()
        file_headers.sort()
        required_file_headers = [
                    "FSN","Category",
                    "Primary USP-1 Attribute","Primary USP-1 Description Text",
                    "Primary USP-2 Attribute","Primary USP-2 Description Text",
                    "Primary USP-3 Attribute","Primary USP-3 Description Text",
                    "Primary USP-4 Attribute","Primary USP-4 Description Text",
                    "Primary USP-5 Attribute","Primary USP-5 Description Text",
                    "Secondary USP-1 Attribute","Secondary USP-1 Description Text",
                    "Secondary USP-2 Attribute","Secondary USP-2 Description Text",
                    "Secondary USP-3 Attribute","Secondary USP-3 Description Text",
                    "Secondary USP-4 Attribute","Secondary USP-4 Description Text",
                    "Secondary USP-5 Attribute","Secondary USP-5 Description Text"
                    ]
        required_file_headers.sort()
        data_is_valid = True
        for header in required_file_headers:
            if header not in file_headers:
                data_is_valid = False
                break
        if data_is_valid:
            self.validate_button.setEnabled(True)
            self.validate_button.setStyleSheet("QPushButton{background-color: #458B00} QPushButton:hover{background-color: #78AB46};")
            data_file_handler.seek(0)
            self.data = []
            for row in data_file_as_csv:
                self.data.append(row)
            self.data_is_ready
            #print self.data
        else:
            self.validate_button.setStyleSheet("background-color: #B22222")
            self.validate_button.setEnabled(False)
            #print file_headers, required_file_headers
        data_file_handler.close()

