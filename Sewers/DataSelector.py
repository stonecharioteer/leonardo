import os, csv, datetime
from PyQt4 import QtGui, QtCore
from FSNTextEdit import FSNTextEdit
from IconButton import IconButton
from FileLocationWidget import FileLocationWidget
from PrimaryButton import PrimaryButton
from QColorButton import QColorButton
from FKRetriever import FKRetriever
from IconListBox import IconListBox
from Katana import getETA, checkIcon, getCategoryFolderNames
from ProgressBar import ProgressBar

class DataSelector(QtGui.QWidget):
    def __init__(self):
        super(DataSelector,self).__init__()
        self.data_from_fk = None
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
        self.export_scraped_data_button = QtGui.QPushButton("Export Data")
        self.fsn_text_edit = FSNTextEdit()
        self.fsn_text_edit.setFixedSize(450,400)
        self.category_label = QtGui.QLabel("Category:")
        self.category_combo_box = QtGui.QComboBox()
        self.category_combo_box.addItems(getCategoryFolderNames()) #Later, add this data from OINK's server.        
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
        self.fetching_progress = ProgressBar()
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
        fsn_mode_layout.addWidget(self.fetch_images_attributes_button,0,1,1,2,  QtCore.Qt.AlignBottom)
        fsn_mode_layout.addWidget(self.fetching_progress,0,3,1,5, QtCore.Qt.AlignBottom)
        fsn_mode_layout.addWidget(self.fetching_activity,1,3,1,5, QtCore.Qt.AlignTop)
        fsn_mode_layout.addWidget(self.export_scraped_data_button,1,1,1,2,  QtCore.Qt.AlignTop)
        fsn_mode_layout.addWidget(self.fsn_mode_data_options,2,1,5,7, QtCore.Qt.AlignTop)
        self.fsn_mode_widget.setLayout(fsn_mode_layout)

        #CSV Mode Widget
        self.csv_mode_widget = QtGui.QWidget()
        self.input_data_set_button = IconButton(os.path.join("essentials","csv_file.png"))
        self.input_data_set_button.setToolTip("Click to select a data file if you want manual control.")
        self.check_icons_button = QtGui.QPushButton("Check Icon Availability\nand Export Report")
        csv_mode_layout = QtGui.QHBoxLayout()
        csv_mode_layout.addStretch(1)
        csv_mode_layout.addWidget(self.input_data_set_button,0)
        csv_mode_layout.addWidget(self.check_icons_button,0)
        csv_mode_layout.addStretch(1)

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
        self.category_combo_box.currentIndexChanged.connect(self.changeCategory)
        self.export_scraped_data_button.clicked.connect(self.exportData)
        self.check_icons_button.clicked.connect(self.checkIconsAvailability)

    def checkIconsAvailability(self):
        import pandas as pd
        import xlsxwriter
        import Katana
        data = self.getData()
        icons = {}
        repo_path = str(QtGui.QFileDialog.getExistingDirectory(self, "Select the repository folder.", os.getcwd(), 
                                                    QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks))
        if not repo_path:
            repo_path = os.path.join(os.getcwd(), "Images","Repository")
        for fsn_row in self.getData():
            category = fsn_row["Category"]
            for key in fsn_row.keys():
                if "Attribute" in key:
                    attribute = fsn_row[key].strip()
                    if attribute.strip() != "":
                        icon_status, folders = Katana.checkIcon(attribute, category, repository_path=repo_path)
                        if attribute not in icons.keys():
                            icons[attribute] = {
                                        "Category": category,
                                        "Icon in Folder(s)": folders
                            }
                        else:
                            if category not in icons[attribute]["Category"]:
                                icons[attribute]["Category"] = icons[attribute]["Category"] + ", "  +category
                            icons[attribute]["Icon in Folder(s)"] = [folder for folder in list(set(icons[attribute]["Icon in Folder(s)"] + folders)) if len(folder)>0]
        icons_data_frame = pd.DataFrame.from_dict(icons)
        file_path = os.path.join(os.getcwd(),"temp.csv")
        #file_handler = pd.ExcelWriter(file_path,engine="xlsxwriter")
        icons_data_frame.T.to_csv(file_path)
        os.startfile(file_path,"open")


        #icons_data_frame.to_excel(file_handler, "Sheet1")
        #file_handler.save()
        print "Saved file to %s!"%file_path

    def exportData(self):
        import pandas as pd
        import xlsxwriter
        #Get the output location.
        output_path = str(QtGui.QFileDialog.getExistingDirectory(self, "Select the output folder.", os.getcwd(), 
                                                    QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks))
        #Calculate the different types of FSNs based on prefix.
        if output_path:
            file_path = os.path.join(output_path,"flipkart_data_%s.xlsx"%datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
            file_handler = pd.ExcelWriter(file_path,engine="xlsxwriter")
            fsns_list = self.data_from_fk.keys()
            prefixes = list(set([fsn[:3] for fsn in fsns_list]))
            prefixes.sort()
            seggregated_data_set = {}
            #Split data based on FSN prefix.
            for prefix in prefixes:
                valid_fsns = [fsn for fsn in fsns_list if prefix==fsn[:3]]
                seggregated_data_set[prefix] = {}
                for fsn in valid_fsns:
                    seggregated_data_set[prefix][fsn] = self.data_from_fk[fsn]
                #Create dataframes for each data set.
                prefix_data_set = pd.DataFrame.from_dict(seggregated_data_set[prefix])
                #Save the dataframe in an excel file with the entire dataset in one sheet, 
                #and individual sheets containing prefix-wise data, stored in the output folder.
                prefix_data_set.T.to_excel(file_handler, prefix)
            file_handler.save()
        pd.DataFrame.from_dict(self.data_from_fk).T.to_csv(os.path.join(output_path,"flipkart_data_%s.csv"%datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))
        os.startfile(file_path,"open")
        self.sendAlert("Success","Success exported data for %d possible verticals into %s."%(len(prefixes),os.path.basename(file_path)))

        #    data_frame = pd.DataFrame.from_dict(self.data_from_fk).transpose()
        #    data_frame.to_csv("something.csv")
            #get save file name
            #dump data into said file.

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
        self.makeDataFile()

    def makeDataFile(self):
        """Creates a list of dictionaries for the FSNs, using the retrieved data."""
        #Extract the primary and secondary attributes.
        primary_attributes = [str(self.primary_attributes_list_box.item(list_index).text()) for list_index in range(self.primary_attributes_list_box.count())]
        secondary_attributes = [str(self.secondary_attributes_list_box.item(list_index).text()) for list_index in range(self.secondary_attributes_list_box.count())]
        #algorithm
        #Build a list of dictionaries with the following structure:
        output_data_format = [
                    {
                        "FSN": None,
                        "Category": None,
                        "Primary USP-1 Attribute": None,
                        "Primary USP-1 Description Text":None,
                        "Primary USP-2 Attribute": None,
                        "Primary USP-2 Description Text":None,
                        "Secondary USP-1 Attribute": None,
                        "Secondary USP-1 Description Text":None,
                        "Secondary USP-2 Attribute": None,
                        "Secondary USP-2 Description Text":None,
                    }
                ]
        #In doing this, check if FSNs have far too many attributes selected, or if they have none at all.
        #To check, see if the attribute is in the fsn_data_set that FKRetriever passes.
        #End algorithm
        output_data = []
        category = str(self.category_combo_box.currentText())
        if self.data_from_fk is None:
            self.sendAlert("Cowabunga!","Something seems to be wrong. This situation shouldn't ever happen. If there are attributes populated in the list widgets, then this shouldn't ever happen. This indicates that Leonardo failed to retrieve information from the Flipkart website or API. But if the attributes list widgets are populated, then this is ridiculously impossible.")
        else:
            never = False
            if (len(primary_attributes)>0) and (len(secondary_attributes)>0):
                #loop through each fsn key.
                invalid_fsns = []
                total_fsns = len(self.data_from_fk.keys())

                for fsn in self.data_from_fk:
                    fsn_data = self.data_from_fk[fsn]
                    fsn_attributes_mapping = {
                        "FSN": fsn,
                        "Category": category
                    }
                    primary_attribute_counter = 0
                    for primary_attribute in primary_attributes:
                        if primary_attribute in fsn_data.keys():
                            primary_attribute_counter += 1
                            attr_key = "Primary USP-%d Attribute"%primary_attribute_counter
                            descr_key = "Primary USP-%d Description Text"%primary_attribute_counter
                            #Check if the icon exists. If it doesn't compile a list of icons required.
                            #icon_available = checkIcon(attr_key,descr_key)
                            fsn_attributes_mapping.update({attr_key:primary_attribute,descr_key: fsn_data[primary_attribute]})
                    secondary_attribute_counter = 0
                    for secondary_attribute in secondary_attributes:
                        if secondary_attribute in fsn_data.keys():
                            secondary_attribute_counter += 1
                            attr_key = "Secondary USP-%d Attribute"%secondary_attribute_counter
                            descr_key = "Secondary USP-%d Description Text"%secondary_attribute_counter
                            #Check if the icon exists. If it doesn't compile a list of icons required.
                            #icon_available = checkIcon(attr_key,descr_key)
                            fsn_attributes_mapping.update({attr_key:secondary_attribute,descr_key: fsn_data[secondary_attribute]})
                    if (primary_attribute_counter == 0) or (secondary_attribute_counter == 0):
                        invalid_fsns.append(fsn)
                    output_data.append(fsn_attributes_mapping)
                if len(invalid_fsns)>0:
                    message = "There are %d fsns without enough primary or secondary attributes. Trying this process for FSNs of mixed category\sub-category isn't recommended." %len(invalid_fsns)
                    self.sendAlert("Uh-oh!",message)
                    self.validate_button.setStyleSheet("background-color: #B22222")
                    self.validate_button.setEnabled(False)
                else:
                    self.data = output_data
                    self.validate_button.setEnabled(True)
                    self.validate_button.setStyleSheet("QPushButton{background-color: #458B00} QPushButton:hover{background-color: #78AB46};")
            elif never:
                #(len(primary_attributes) == 0) or (len(secondary_attributes) == 0):
                #This could be a problem in runtime. Disabling for now.
                self.sendAlert("Cowabunga!","Please promote some attributes to primary and secondary positions. If you don't want to use secondary attributes, just add one anyway, and select equal relative icon sizes later.")

    def changeCategory(self):
        self.makeDataFile()

    def sendAlert(self, title, message):
        QtGui.QMessageBox.about(self, title, message)

    def downloadFromFK(self):
        """Triggers FKRetriever."""
        fsns = self.fsn_text_edit.getFSNs()
        if len(fsns) >=1:
            self.fetching_activity.setText("Preparing to download images and specifications off the Flipkart website!")
            self.fk_retriever.fsn_list = fsns
            self.fk_retriever.allow_run = True
        else:
            print "No FSNS?"

    def prepareDataRetrievedFromFK(self, status, data_set, progress_value, completion_status, eta):
        """Gets data from FK from the thread's signal and prepares it."""
        self.fetching_progress.setValue(progress_value)
        self.putAttributes(data_set)
        self.data_from_fk = data_set
        if completion_status:
            self.fetching_activity.setText("Fee, fie, fo, fum!")
            self.fsn_mode_data_options.setEnabled(True)
            self.sendAlert("Cowabunga!","Completed fetching data and images for the given list.")
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
                FSN, Brand, Category, Primary USP[1-5] Attribute; Primary USP[1-5] Description; Secondary USP[1-5] Attribute; Secondary USP[1-5] Description;
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
                        "FSN","Brand","Category",
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
                    self.sendAlert("Wrong Data set.", "%s column is required!"%header)
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
            else:
                self.validate_button.setStyleSheet("background-color: #B22222")
                self.validate_button.setEnabled(False)
            data_file_handler.close()

