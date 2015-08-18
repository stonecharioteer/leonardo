import os, csv, datetime
from PyQt4 import QtGui, QtCore
from FSNTextEdit import FSNTextEdit
from IconButton import IconButton
from FileLocationWidget import FileLocationWidget
from PrimaryButton import PrimaryButton
from QColorButton import QColorButton
from FKRetriever import FKRetriever
from IconListBox import IconListBox
from Katana import getETA

class DataSelector(QtGui.QWidget):
    def __init__(self):
        super(DataSelector,self).__init__()
        self.createUI()
        self.fk_retriever = FKRetriever()
        self.mapEvents()
        self.data_is_ready = False
        self.data = None
        self.validate_button.setEnabled(False)

    def createUI(self):
        self.group_box = QtGui.QGroupBox("Data Selector")
        self.page_selector = IconListBox()
        page_control_list = [
                    {
                    "Name": "From Flipkart Using FSNs",
                    "Icon": os.path.join("essentials","download.png")
                    },
                    {
                    "Name": "From CSV Data File",
                    "Icon": os.path.join("essentials","csv_file.png")
                    }
                ]
        self.page_selector.addElements(page_control_list)
        self.page_selector.setFixedSize(302,110)
        #FSN Mode Widget
        self.fsn_mode_widget = QtGui.QGroupBox("Data By FSN")
        self.fsn_text_edit = FSNTextEdit()
        self.fsn_text_edit.setFixedSize(450,400)
        self.category_label = QtGui.QLabel("Category:")
        self.category_combo_box = QtGui.QComboBox()
        self.category_combo_box.addItems(["Cameras","Mobiles","Tablets"]) #Later, add this data from OINK's server.        
        self.category_combo_box.setToolTip("Select the default category for the given FSNs.\nNote that mixing various types of FSNs isn't recommended.\nThe icons won't load.")
        self.attributes_list_box = QtGui.QListWidget()
        self.attributes_list_box.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.attributes_list_box.setToolTip("Displays all product attributes, obtained from the FK server.")
        self.primary_attributes_list_box = QtGui.QListWidget()
        self.primary_attributes_list_box.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.primary_attributes_list_box.setToolTip("Displays primary product attributes that you have selected.")
        self.secondary_attributes_list_box = QtGui.QListWidget()
        self.secondary_attributes_list_box.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.secondary_attributes_list_box.setToolTip("Displays secondary product attributes that you have selected.")
        self.push_to_primary_button = QtGui.QPushButton("Add to\nPrimary List")
        self.push_to_primary_button.setToolTip("Click to move the chosen attribute into the list of primary attributes.")
        self.remove_from_primary_button = QtGui.QPushButton("Remove from\nPrimary List")
        self.remove_from_primary_button.setToolTip("Click to move the chosen attribute out of the list of primary attributes.")
        self.push_to_secondary_button = QtGui.QPushButton("Add to\nSecondary List")
        self.push_to_secondary_button.setToolTip("Click to move the chosen attribute into the list of secondary attributes.")
        self.remove_from_secondary_button = QtGui.QPushButton("Remove from\nSecondary List")
        self.remove_from_secondary_button.setToolTip("Click to move the chosen attribute out of the list of secondary attributes.")
        self.fetch_images_attributes_button = QtGui.QPushButton("Download Images\nand Specs.")
        self.fetch_images_attributes_button.setToolTip("This will check if parent images are available for all the FSNs and download them if necessary from the FK site. It will also load the spec table.")
        self.fetching_progress = QtGui.QProgressBar()
        self.fetching_progress.setRange(0,100)
        self.fetching_progress.setValue(0)
        self.fetching_activity = QtGui.QLabel("All that is gold does not glitter!")
        self.fetching_activity.setToolTip("This indicates the current downloader's activity, or some random quote that Vinay thinks is funny.")
        self.fsn_mode_data_options = QtGui.QGroupBox("Data Options")
        fsn_mode_data_options_layout = QtGui.QGridLayout()
        fsn_mode_data_options_layout.addWidget(self.category_label,0,0,1,2,QtCore.Qt.AlignVCenter)
        fsn_mode_data_options_layout.addWidget(self.category_combo_box,0,2,1,2,QtCore.Qt.AlignVCenter)
        fsn_mode_data_options_layout.addWidget(self.attributes_list_box,1,0,4,4, QtCore.Qt.AlignHCenter)
        fsn_mode_data_options_layout.addWidget(self.primary_attributes_list_box,1,5,2,2, QtCore.Qt.AlignHCenter)
        fsn_mode_data_options_layout.addWidget(self.push_to_primary_button,1,4,1,1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        fsn_mode_data_options_layout.addWidget(self.remove_from_primary_button,2,4,1,1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        fsn_mode_data_options_layout.addWidget(self.secondary_attributes_list_box,3,5,2,2, QtCore.Qt.AlignHCenter)
        fsn_mode_data_options_layout.addWidget(self.push_to_secondary_button,3,4,1,1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        fsn_mode_data_options_layout.addWidget(self.remove_from_secondary_button,4,4,1,1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.fsn_mode_data_options.setLayout(fsn_mode_data_options_layout)
        self.fsn_mode_data_options.setEnabled(False)
        fsn_mode_layout = QtGui.QGridLayout()
        fsn_mode_layout.addWidget(self.fsn_text_edit,0,0,7,1)
        fsn_mode_layout.addWidget(self.fetch_images_attributes_button,0,1,2,2, QtCore.Qt.AlignVCenter)
        fsn_mode_layout.addWidget(self.fetching_progress,0,3,1,5, QtCore.Qt.AlignBottom)
        fsn_mode_layout.addWidget(self.fetching_activity,1,3,1,5, QtCore.Qt.AlignTop)
        fsn_mode_layout.addWidget(self.fsn_mode_data_options,2,1,4,7, QtCore.Qt.AlignTop)
        self.fsn_mode_widget.setLayout(fsn_mode_layout)

        #CSV Mode Widget
        self.csv_mode_widget = QtGui.QWidget()
        self.input_data_set_button = IconButton(os.path.join("essentials","csv_file.png"))
        self.input_data_set_button.setToolTip("Click to select a data file if you want manual control.")
        csv_mode_layout = QtGui.QGridLayout()
        csv_mode_layout.addWidget(self.input_data_set_button,0,0)
        self.csv_mode_widget.setLayout(csv_mode_layout)

        self.fsn_or_csv_stacked_widget = QtGui.QStackedWidget()
        self.fsn_or_csv_stacked_widget.addWidget(self.fsn_mode_widget)
        self.fsn_or_csv_stacked_widget.addWidget(self.csv_mode_widget)

        self.validate_button  = IconButton(os.path.join("essentials","validate.png"))
        layout = QtGui.QGridLayout()
        layout.addWidget(self.page_selector,0,0,1,2, QtCore.Qt.AlignHCenter)
        layout.addWidget(self.fsn_or_csv_stacked_widget,1,0,1,2)
        layout.addWidget(self.validate_button,3,1)
        self.group_box.setLayout(layout)
        final_layout = QtGui.QHBoxLayout()
        final_layout.addWidget(self.group_box)
        self.setLayout(final_layout)

    def mapEvents(self):
        self.page_selector.currentItemChanged.connect(self.changePage)
        self.input_data_set_button.clicked.connect(self.loadDataFromFile)
        self.fetch_images_attributes_button.clicked.connect(self.downloadFromFK)
        self.fk_retriever.sendData.connect(self.prepareDataRetrievedFromFK)
        self.fk_retriever.sendException.connect(self.postException)
        self.push_to_primary_button.clicked.connect(self.pushAttrToPrimary)
        self.remove_from_primary_button.clicked.connect(self.removeFromPrimary)
        self.push_to_secondary_button.clicked.connect(self.pushAttrToSecondary)
        self.remove_from_secondary_button.clicked.connect(self.removeFromSecondary)

    def postException(self, error_msg):
        self.fetching_activity.setText("%s @%s"%(error_msg,datetime.datetime.now().strftime("%H:%M:%S")))

    def pushAttrToPrimary(self):
        self.pushFromTo(self.attributes_list_box,self.primary_attributes_list_box)

    def removeFromPrimary(self):
        self.pushFromTo(self.primary_attributes_list_box,self.attributes_list_box)

    def pushAttrToSecondary(self):
        self.pushFromTo(self.attributes_list_box,self.secondary_attributes_list_box)

    def removeFromSecondary(self):
        self.pushFromTo(self.secondary_attributes_list_box,self.attributes_list_box)
    
    def pushFromTo(self,source_list_widget, destination_list_widget):
        #identify the selected attributes
        selected_attribute_items = source_list_widget.selectedItems()
        #Store them in a list.
        selected_attributes = [str(selected_attribute_item.text()) for selected_attribute_item in selected_attribute_items]
        #Send them to the destination list.
        destination_list_widget.setSortingEnabled(False)
        destination_list_widget.addItems(selected_attributes)
        destination_list_widget.setSortingEnabled(True)
        destination_list_widget.sortItems()
        #Remove them from the source list
        for selected_item in selected_attribute_items:
            source_list_widget.takeItem(source_list_widget.row(selected_item))

    def downloadFromFK(self):
        """Triggers FKRetriever."""
        fsns = self.fsn_text_edit.getFSNs()
        if len(fsns) >=1:
            self.fetching_activity.setText("Preparing to download images and specifications off the Flipkart website!")
            self.fk_retriever.fsn_list = fsns
            self.fk_retriever.allow_run = True

    def prepareDataRetrievedFromFK(self, status, data_set, progress_value, completion_status, eta):
        """Gets data from FK from the thread's signal and prepares it."""
        self.fetching_progress.setValue(progress_value)
        self.putAttributes(data_set)
        if completion_status:
            self.fetching_activity.setText("Fee, fie, fo, fum!")
            self.fsn_mode_data_options.setEnabled(True)
            #Map to say cowabunga?
        else:
            self.fetching_activity.setText("%s ETA: %s"%(status,eta.strftime("%a (%d-%b), %H:%M:%S")))
            self.fsn_mode_data_options.setEnabled(False)
            
    def putAttributes(self, data_set):
        attributes = []
        for fsn in data_set:
            attributes+=data_set[fsn].keys()
        attributes = list(set(attributes))
        self.attributes_list_box.setSortingEnabled(False)
        self.attributes_list_box.clear()
        self.primary_attributes_list_box.clear()
        self.secondary_attributes_list_box.clear()
        self.attributes_list_box.addItems(attributes)
        self.attributes_list_box.setSortingEnabled(True)
        self.attributes_list_box.sortItems()
    
    def getData(self):
        return self.data

    def changePage(self, current, previous):
        if not current:
            current = previous
        self.fsn_or_csv_stacked_widget.setCurrentIndex(self.page_selector.row(current))

    def loadDataFromFile(self):
        """This method asks for a csv data file. Upon loading, it'll read the file, 
            check it and declare whether it's valid or not.
            It does it based on:
            1. File headers: 
                FSN, Category, Primary USP[1-5] Attribute; Primary USP[1-5] Description; Secondary USP[1-5] Attribute; Secondary USP[1-5] Description;
            2. At least 1 row of data.
        """
        #Get the file name.
        data_file_name = str(QtGui.QFileDialog.getOpenFileName(self,"Open Data File",os.getcwd(),("Comma Separated Values Files (*.csv)")))
        if data_file_name:
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
                next(data_file_handler) #0 has the header, so go to row 1.
                self.data = []
                for row in data_file_as_csv:
                    self.data.append(row)
                self.data_is_ready = True
                #print self.data
            else:
                self.validate_button.setStyleSheet("background-color: #B22222")
                self.validate_button.setEnabled(False)
                #print file_headers, required_file_headers
            data_file_handler.close()

