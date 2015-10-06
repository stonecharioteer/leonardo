from __future__ import division
import os, glob, random
import json
from PyQt4 import QtGui, QtCore
from FSNTextEdit import FSNTextEdit
from IconButton import IconButton
#from FileLocationWidget import FileLocationWidget
from PrimaryButton import PrimaryButton
from QColorButton import QColorButton
from QColorPanel import QColorPanel
from ProgressBar import ProgressBar
from Splinter import Splinter
from ParentImageSelectorWidget import ParentImageSelectorWidget
from PositionWidget import PositionWidget

class LayoutDesigner(QtGui.QWidget):
    def __init__(self, repo_path):
        super(LayoutDesigner,self).__init__()
        self.repo_path = repo_path
        self.current_image = None
        self.splinter_thread = Splinter(0, self.repo_path)
        self.createUI()
        self.mapEvents()
        #Load values from the default file.
        self.resetValues()
        #Start a splinter thread.


    def resetValues(self):
        default_file = os.path.join("cache","defaults.json")
        if os.path.isfile(default_file):
            self.setValues(default_file)

    def setValues(self, file_path):
        """
        Sets the defaults for the settings, loading from a JSON file.
        """
        with open(file_path) as json_file_handler:
            settings_from_json = json.load(json_file_handler)

        #Set the primary and secondary icon sizes.
        primary_attr_icon_size_value = settings_from_json["Primary Attribute Relative Size"]
        self.primary_attr_icon_size_spin_box.setValue(primary_attr_icon_size_value)
        
        secondary_attr_icon_size_value = settings_from_json["Secondary Attribute Relative Size"]
        self.secondary_attr_icon_size_spin_box.setValue(secondary_attr_icon_size_value)
        #Set the Parent Image position y and x.
        parent_image_position_value = settings_from_json["Parent Image Position"]
        if type(parent_image_position_value) == list:
            x, y = parent_image_position_value
            self.parent_image_position_position_radiobuttons[int(2*y)][int(2*x)].setChecked(True)
        else:
            self.parent_image_position_position_radiobuttons[1][1].setChecked(True)
            self.use_random_parent_image_position.setChecked(True)

        #Set the primary image resize reference.
        parent_image_resize_reference_value = settings_from_json["Parent Image Resize Reference"]
        resize_reference_combo_index = self.parent_image_resize_reference.findText(parent_image_resize_reference_value)
        self.parent_image_resize_reference.setCurrentIndex(resize_reference_combo_index)
        
        #Set the primary or product image resize percentage value.
        parent_image_resize_factor_value = 100*settings_from_json["Parent Image Resize Factor"]
        self.product_image_scale_spinbox.setValue(parent_image_resize_factor_value)
        
        #Set the color replacement algorithm
        use_simple_color_replacement_value = settings_from_json["Use Simple Color Replacement"]
        self.use_simple_color_replacement.setChecked(use_simple_color_replacement_value)
        
        #Set the Color stripping threshold
        background_color_threshold_value = settings_from_json["Background Color Threshold Value"]
        self.background_color_threshold_spinbox.setValue(background_color_threshold_value)
        
        #Set the Palette selection method.
        icon_colors_value = settings_from_json["Icon Palette"]
        try:
            if len(icon_colors_value) == len(self.palette_selection_buttons):
                counter = 0
                for button in self.palette_selection_buttons:
                    button.setColors(icon_colors_value[counter])
                    counter += 1
            else:
                for button in self.palette_selection_buttons:
                    button.setColors(icon_colors_value[0])
        except:
            pass
        #Set the Image margin percentage.
        margin_value = 100*settings_from_json["Margin"]
        self.image_margin_spinbox.setValue(margin_value)
        
        #Set the Aspect ratio
        image_aspect_ratio_value = settings_from_json["Image Aspect Ratio"]
        aspect_x, aspect_y = image_aspect_ratio_value
        self.final_image_aspect_ratio_input_box_1.setValue(aspect_x)
        self.final_image_aspect_ratio_input_box_2.setValue(aspect_y)
        
        #Set the Icon arrangement method.
        icon_arrangement_value = str(settings_from_json["Icon Arrangement"])
        if icon_arrangement_value == "Circular":
            self.icon_arrangement_circular.setChecked(True)
        else:
            self.icon_arrangement_rectangular.setChecked(True)
        
        #Set the overlap boolean
        allow_overlap_value = settings_from_json["Allow Icons Overlap"]
        if type(allow_overlap_value) != bool:
            allow_overlap_value = False
        self.allow_overlap_checkbox.setChecked(allow_overlap_value)

        #Set the boolean to allow icons without text.
        allow_textless_icons = settings_from_json["Allow Icons Without Text"]
        if type(allow_textless_icons) != bool:
            allow_textless_icons = False
        self.allow_textless_icons_checkbox.setChecked(allow_textless_icons)

        #Set Icon Font Bold
        icon_font_bold = settings_from_json["Icon Font Bold"]
        if type(icon_font_bold) != bool:
            icon_font_bold = False
        self.bold_button.setChecked(icon_font_bold)
        
        #Set Icon Font Underlined
        icon_font_underline = settings_from_json["Icon Font Underline"]
        if type(icon_font_underline) != bool:
            icon_font_underline = False
        self.underline_button.setChecked(icon_font_underline)
        
        #Set Icon Font Italics
        icon_font_italics = settings_from_json["Icon Font Italics"]
        if type(icon_font_italics) != bool:
            icon_font_italics = False
        self.italics_button.setChecked(icon_font_italics)

        #Set Icon font size
        icon_font_size = settings_from_json["Icon Font Size"]

        #Set the background-appropriate icon color loading behaviour.
        load_icon_color_from_background = settings_from_json["Load Icon Colors From Background"]
        if type(load_icon_color_from_background) != bool:
            load_icon_color_from_background = False

        #Set the bounding box.
        icon_bounding_box = settings_from_json["Icon Bounding Box"]
        self.icon_bounding_box_combobox.setCurrentIndex(self.icon_bounding_box_combobox.findText(icon_bounding_box))

        #Set the fix icon case checkbox.
        fix_icon_text_case = settings_from_json["Fix Icon Text Case"]
        self.fix_icon_text_case.setChecked(fix_icon_text_case)
        
        #Set the preserve icon colors checkbox.
        preserve_icon_colors = settings_from_json["Preserve Icon Colors"]
        self.preserve_icon_colors.setChecked(preserve_icon_colors)

        use_category_specific_backgrounds = settings_from_json["Use Category Specific Backgrounds"]
        self.use_category_specific_backgrounds.setChecked(use_category_specific_backgrounds)

        background_image = settings_from_json["Background Image"]
        self.background_selection_combobox.setCurrentIndex(self.background_selection_combobox.findText(background_image))

        #Set the icon font color
        #Set the bool to use the icon color for font color.
        font_color = settings_from_json["Icon Font Color"]
        self.font_color_picker.setColorFromRGB(font_color)

        use_icon_color_for_font_color = settings_from_json["Use Icon Color For Font Color"]
        if type(use_icon_color_for_font_color) == bool:
            self.use_icon_color_for_font_color.setChecked(use_icon_color_for_font_color)
        else:
            print "The JSON has a non boolean value for the use_icon_color_for_font_color variable."

        icon_font_size = settings_from_json["Icon Font Size"]
        self.font_size_spinbox.setValue(icon_font_size)
        if "Bypass Parent Image Cleanup" in settings_from_json.keys():
            bypass_parent_image_cleanup = settings_from_json["Bypass Parent Image Cleanup"]
            self.bypass_parent_image_cleanup.setChecked(bypass_parent_image_cleanup)

    def createUI(self):        
        self.preview_group_box = self.createPreviewWidget()
        self.settings_group_box = self.createSettingsWidget()
        self.validate_button  = IconButton(os.path.join("essentials","validate.png"))
        self.validate_button.setToolTip("Validate and Proceed")
        self.fsn_list_box = QtGui.QListWidget()
        self.fsn_list_box.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.fsn_list_box.setFixedWidth(250)

        final_ui_layout = QtGui.QGridLayout()
        final_ui_layout.addWidget(self.fsn_list_box,0,0,10,1)
        final_ui_layout.addWidget(self.settings_group_box,0, 1, 10, 6)
        final_ui_layout.addWidget(self.preview_group_box,0, 7, 10, 4, 
                                QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        final_ui_layout.addWidget(self.validate_button,10, 10, 1, 1, 
                                QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        
        self.over_all_group_box = QtGui.QGroupBox("Design")
        self.over_all_group_box.setLayout(final_ui_layout)
        over_all_layout_wrapper = QtGui.QHBoxLayout()
        over_all_layout_wrapper.addWidget(self.over_all_group_box)
        self.setLayout(over_all_layout_wrapper)

    def createPreviewWidget(self):
        #Creates the preview pane.
        self.update_preview_button = QtGui.QPushButton("Update")
        self.update_preview_button.setToolTip("Click to build the USP image for the selected image with the chosen settings.")
        self.stop_button = QtGui.QPushButton("Stop")
        self.stop_button.setToolTip("Click to stop after building the on-going image.")
        self.open_destination_folder = QtGui.QPushButton("Locate File")
        self.open_destination_folder.setToolTip("Click to open the destination folder in Explorer.")
        self.stop_button.setEnabled(False)

        buttons_layout = QtGui.QHBoxLayout()
        buttons_layout.addWidget(self.update_preview_button,0)
        buttons_layout.addWidget(self.stop_button,0)
        buttons_layout.addWidget(self.open_destination_folder,0)
        self.file_name_label = QtGui.QLabel("Current File:")
        self.file_name_line_edit = QtGui.QLineEdit()

        self.file_name_line_edit.setReadOnly(True)


        line_layout = QtGui.QHBoxLayout()
        line_layout.addWidget(self.file_name_label)
        line_layout.addWidget(self.file_name_line_edit)


        self.preview_widget = QtGui.QPushButton()
        self.preview_widget.setToolTip("USP Image Preview. Click to open externally.")
        size_modifier = 2.7
        self.preview_widget.setFixedSize(90*size_modifier, 140*size_modifier)
        self.left_button = QtGui.QPushButton("&<")
        self.left_button.setEnabled(False)
        self.left_button.setFixedSize(15, 140*size_modifier)
        self.left_button.setToolTip("Click to show the previous image.")
        
        self.right_button = QtGui.QPushButton("&>")
        self.right_button.setEnabled(False)
        self.right_button.setFixedSize(15, 140*size_modifier)
        self.right_button.setToolTip("Click to show the next image.")

        preview_widget_style_sheet = """
                                QLabel {
                                    background-color: grey;
                                    border: 2px solid black;
                                };
                                """
        self.preview_widget.setStyleSheet(preview_widget_style_sheet)
        self.progress_bar = ProgressBar()
        self.progress_status = QtGui.QLabel("Humpty Dumpty sat on a wall.")
        self.progress_status.setWordWrap(True)
        self.progress_status.setFixedHeight(50)

        preview_buttons_image_layout = QtGui.QHBoxLayout()
        preview_buttons_image_layout.addWidget(self.left_button,0, QtCore.Qt.AlignLeft)
        preview_buttons_image_layout.addWidget(self.preview_widget,2, QtCore.Qt.AlignHCenter)
        preview_buttons_image_layout.addWidget(self.right_button,0, QtCore.Qt.AlignRight)

        preview_layout = QtGui.QVBoxLayout()
        preview_layout.addLayout(buttons_layout, 0)
        preview_layout.addLayout(line_layout, 0)
        preview_layout.addLayout(preview_buttons_image_layout, 3)
        preview_layout.addWidget(self.progress_bar, 0, QtCore.Qt.AlignTop)
        preview_layout.addWidget(self.progress_status, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        preview_group_box = QtGui.QGroupBox("Preview")
        preview_group_box.setLayout(preview_layout)
        return preview_group_box

    def openImage(self):
        if self.current_image is not None:
            os.startfile(self.current_image,"open")

    def displayProgress(self,status, progress_value, eta, completion_status, images_list, thread_index):
        self.progress_bar.setValue(progress_value)
        self.progress_status.setText(status)
        self.setImage(images_list)
        if completion_status:
            self.update_preview_button.setEnabled(True)
            self.stop_button.setEnabled(False)

    def setImage(self, images_list):
        self.images_list = images_list
        self.current_index = len(self.images_list)-1
        self.changeIndex(self.current_index)
    
    def changeIndex(self, image_index):
        if (0 <= image_index <= (len(self.images_list)-1)):
            self.current_image = self.images_list[image_index]
            self.file_name_line_edit.setText(os.path.splitext(os.path.basename(self.current_image))[0])
            image_pixmap = QtGui.QPixmap(self.current_image)
            image_pixmap = image_pixmap.scaled(
                                            self.preview_widget.size(),
                                            QtCore.Qt.IgnoreAspectRatio, 
                                            QtCore.Qt.SmoothTransformation)
            icon = QtGui.QIcon(image_pixmap)
            self.preview_widget.setIcon(icon)
            self.preview_widget.setIconSize(image_pixmap.rect().size())
            self.preview_widget.setStyleSheet("QPushButton {background-color: grey; border: 1px solid black;}")
            if image_index == 0:
                self.left_button.setEnabled(False)
            else:
                self.left_button.setEnabled(True)
            
            if image_index == (len(self.images_list)-1):
                self.right_button.setEnabled(False)
            else:
                if len(self.images_list)>1:
                    self.right_button.setEnabled(True)

    def showNextImage(self):
        self.current_index += 1
        self.changeIndex(self.current_index)

    def showPreviousImage(self):
        self.current_index -= 1
        self.changeIndex(self.current_index)



    def displayActivity(self, status, eta, thread_index):
        self.progress_status.setText(status)
    
    def stopRunning(self):
        self.splinter_thread.allow_run = False
        self.update_preview_button.setEnabled(True)

    def alertMessage(self, title, message):
        QtGui.QMessageBox.about(self, title, message)
    
    def runSplinter(self):
        required_fsns = [str(str(fsn_item.text())[(str(fsn_item.text()).rfind(" ")+1):]) for fsn_item in self.fsn_list_box.selectedItems()]

        if len(required_fsns) <= 0:
            self.alertMessage("Select at least 1 FSN.","If you're trying to run Leo FSN-by-FSN, you'll need to select at least one FSN in the list to the left.")
        else:
            self.progress_bar.setValue(0)
            self.update_preview_button.setEnabled(False)
            self.stop_button.setEnabled(True)

            requested_data = []
            for fsn in required_fsns:
                for fsn_row in self.fsn_data:
                    if fsn_row["FSN"] == fsn:
                        requested_data.append(fsn_row)

            if len(requested_data) == 0:
                self.alertMessage("Zero FSNs Selected!", "Although you've selected some FSNs, there doesn't seem to be a match with the loaded data. This is a scenario which shouldn't happen. The code is at fault.")
                print required_fsns
            else:
                self.splinter_thread.data = requested_data
                self.splinter_thread.parent_image_position = self.getParentImageCoords()
                self.splinter_thread.icon_positioning = self.getIconPosition()
                self.splinter_thread.icon_palette = self.getIconPalette() #Enable this later.
                self.splinter_thread.allow_overlap = self.getOverlap()
                self.splinter_thread.background_image_path = self.getBackgroundImage()
                self.splinter_thread.primary_attribute_relative_size = self.getPrimaryAttrRelativeSize()
                self.splinter_thread.secondary_attribute_relative_size = self.getSecondaryAttrRelativeSize()
                self.splinter_thread.bounding_box = self.getIconBoundingBox()
                self.splinter_thread.use_simple_bg_color_strip = self.useSimpleColorStripAlgorithm()
                self.splinter_thread.bg_color_strip_threshold = self.getColorStripThreshold()
                self.splinter_thread.parent_image_resize_reference = self.getParentImageResizeReference()
                self.splinter_thread.parent_image_resize_factor = self.getParentImageResizeFactor()
                self.splinter_thread.allow_textless_icons = self.allowTextlessIcons()
                self.splinter_thread.margin = self.getMargin()
                self.splinter_thread.use_category_specific_backgrounds = self.useCategorySpecificBackgrounds()
                self.splinter_thread.output_location = self.repo_path
                self.splinter_thread.colors_list = self.getIconPalette()
                self.splinter_thread.preserve_icon_colors = self.preserveIconColors()
                self.splinter_thread.fix_icon_text_case = self.fixIconTextCase()
                self.splinter_thread.font = self.getFont()
                self.splinter_thread.font_color = self.getIconFontColor()
                self.splinter_thread.use_icon_color_for_font_color = self.useIconColorForFontColor()
                self.splinter_thread.icon_font_size = self.getIconFontSize()
                self.splinter_thread.bypass_parent_image_cleanup = self.bypassParentImageCleanup()
                self.splinter_thread.parent_image_paths = self.getParentImagePaths()
                self.splinter_thread.use_enforced_coords = self.useEnforcedCoordinates()
                self.splinter_thread.enforced_coords = self.getCoords()
                self.splinter_thread.show_position_markers = self.showPositionMarkers()
                self.splinter_thread.allow_run = True

    def setFSNs(self, fsn_data):
        self.fsn_data = fsn_data
        self.update_preview_button.setEnabled(True)
        fsns = []
        for fsn_row in fsn_data:
            fsn = fsn_row["FSN"]
            category = fsn_row["Category"]
            usp_count = 0
            fsn_row.keys()
            for key in fsn_row.keys():
                if "Attribute" in key:
                    if len(fsn_row[key].strip()) > 0:
                        usp_count +=1
            fsn_label = "%s - %d USPs - %s"%(category, usp_count, fsn)
            if fsn_label not in fsns:
                fsns.append(fsn_label)
        fsns.sort()
        self.fsn_list_box.clear()
        self.fsn_list_box.addItems(fsns)
        self.parent_image_selector.setFSNs(fsns)

    def createSettingsWidget(self):
        #Create the settings panels.

        self.settings_group_box = QtGui.QGroupBox("Settings")
        self.settings_tool_box = QtGui.QTabWidget()
        self.layout_panel = self.getLayoutPanel()
        self.font_panel = self.getFontPanel()
        self.advanced_panel = self.getAdvancedPanel()
        self.position_widget = PositionWidget()
        self.parent_image_selector = self.getParentImageSelector()

        self.settings_tool_box.addTab(self.layout_panel, "Layout")
        self.settings_tool_box.addTab(self.position_widget, "Positions")
        self.settings_tool_box.addTab(self.parent_image_selector, "Parent Images")
        self.settings_tool_box.addTab(self.font_panel, "Icon and Font")
        self.settings_tool_box.addTab(self.advanced_panel, "Advanced")

        
        self.save_settings_button = QtGui.QPushButton("Save Current\nSettings")
        self.save_settings_button.setToolTip("Click to save all the current settings to a JSON file.")
        self.load_settings_from_file_button = QtGui.QPushButton("Load Settings\nFrom File")
        self.load_settings_from_file_button.setToolTip("Click to load settings from a JSON file.")
        self.reset_settings_button = QtGui.QPushButton("Reset\nSettings")
        self.reset_settings_button.setToolTip("Click to reset all settings to their default values.")
        settings_buttons_layout = QtGui.QHBoxLayout()
        settings_buttons_layout.addWidget(self.save_settings_button,0,QtCore.Qt.AlignRight)
        settings_buttons_layout.addWidget(self.load_settings_from_file_button,0,QtCore.Qt.AlignHCenter)
        settings_buttons_layout.addWidget(self.reset_settings_button,0,QtCore.Qt.AlignLeft)
        settings_layout = QtGui.QVBoxLayout()
        settings_layout.addWidget(self.settings_tool_box,10)
        settings_layout.addLayout(settings_buttons_layout,0)

        self.settings_group_box.setLayout(settings_layout)
        return self.settings_group_box

    def getLayoutPanel(self):
        #Create the layout selector.
        #Instantiate the radiobuttons.
        self.parent_image_position_position_radiobuttons = []
        for i in range(3):
            self.parent_image_position_position_radiobuttons.append([QtGui.QRadioButton() for j in range(3)])
        #Add all radiobuttons to a QButtonGroup.
        self.parent_image_position_selector_radiobuttons_group = QtGui.QButtonGroup()
        #Create dictionaries that can translate the position index to a meaningful string for the tooltip.
        vpos = {0: "Top", 1:"Middle", 2:"Bottom"}
        hpos = {0: "Left", 1:"Center", 2:"Right"}
        for i in range(3):
            for j in range(3):
                self.parent_image_position_selector_radiobuttons_group.addButton(self.parent_image_position_position_radiobuttons[i][j])
                self.parent_image_position_position_radiobuttons[i][j].setToolTip("This sets the position of the parent image to the %s %s of the image.\nPlease note that the representation isn't exact and\nthe final image layout may vary as constraints dictate." %(vpos[i], hpos[j]))
        self.parent_image_position_selector_radiobuttons_group.setExclusive(True)
        #Map the layout_selector to a layout.
        self.parent_image_position_selector_layout = QtGui.QGridLayout()
        #Create a checkbox that allows randomly choosing a position.
        self.use_random_parent_image_position = QtGui.QCheckBox("Randomize")
        self.use_random_parent_image_position.setToolTip("This makes the program pick a random position for the product image.\nThis provides true variation in icon positions as well.")
        self.parent_image_position_selector_layout.addWidget(self.use_random_parent_image_position,0,0,1,3,QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        self.background_preview_space = QtGui.QLabel()
        self.background_preview_space.setFixedSize(170, 280)        
        self.background_preview_space.setStyleSheet("QLabel {background-color: grey; border: 1px solid black;}")
        self.background_preview_space.setToolTip("Preview of the selected background image.")
        self.parent_image_position_selector_layout.addWidget(self.background_preview_space,1,0,3,3,QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        halignment = [QtCore.Qt.AlignLeft, QtCore.Qt.AlignHCenter, QtCore.Qt.AlignRight]
        valignment = [QtCore.Qt.AlignTop, QtCore.Qt.AlignVCenter, QtCore.Qt.AlignBottom]
        for i in range(3):
            for j in range(3):
                self.parent_image_position_selector_layout.addWidget(self.parent_image_position_position_radiobuttons[i][j],i+1,j,1,1,halignment[j]|valignment[i])
        self.parent_image_position_selector = QtGui.QGroupBox("Parent Image Position:")
        self.parent_image_position_selector.setLayout(self.parent_image_position_selector_layout)
        self.parent_image_position_selector.setFixedSize(192,335)
        
        #Create label and dropdown for background
        self.background_selection_label = QtGui.QLabel("Background Image:")
        self.background_selection_combobox = QtGui.QComboBox()
        self.background_selection_combobox.setToolTip("Choose a background to use for all the FSNs.\nIf you need to add more backgrounds to this list, just add them to the Images\\Backgrounds folder.\nEnsure that the first word of the image is Background, with an uppercase B.\nFormat doesn't matter. Please use images of 9:16 aspect ratio.\nYes, portrait mode only.")
        self.background_selection_combobox.setMaximumWidth(200)
        self.backgrounds = ["Random"] + [os.path.basename(file_path) for file_path in glob.glob(os.path.join(self.repo_path,"Backgrounds","*.*"))]
        self.background_selection_combobox.addItems(self.backgrounds)

        #Create icon positions toggle buttons. Set default to circular.
        self.icon_arrangement_label = QtGui.QLabel("Icon Arrangement:")
        self.icon_arrangement_circular = IconButton(os.path.join("essentials","circular_layout.png"))
        self.icon_arrangement_circular.setSize(48,48)
        self.icon_arrangement_circular.setCheckable(True)
        self.icon_arrangement_circular.setToolTip("This layout arranges the icons around the product image in arcs.")
        self.icon_arrangement_rectangular = IconButton(os.path.join("essentials","rectangular_layout.png"))
        self.icon_arrangement_rectangular.setSize(48,48)
        self.icon_arrangement_rectangular.setCheckable(True)
        self.icon_arrangement_rectangular.setToolTip("This layout arranges the icons around the product image in linear stacks.")
        self.icon_arrangement_group = QtGui.QButtonGroup()
        self.icon_arrangement_group.addButton(self.icon_arrangement_circular)
        self.icon_arrangement_group.addButton(self.icon_arrangement_rectangular)
        self.icon_arrangement_group.setExclusive(True)
        #Widget for controlling icon bounding box.
        self.icon_bounding_box_label = QtGui.QLabel("Icon Bounding Box Shape:")
        self.icon_bounding_box_combobox = QtGui.QComboBox()
        self.icon_bounding_box_combobox.addItem("None")
        icon_shape_paths = glob.glob(os.path.join(self.repo_path,"Shapes","*.png"))
        icon_names = [os.path.splitext(os.path.basename(icon_path))[0] for icon_path in icon_shape_paths]
        for counter in range(len(icon_shape_paths)):
            self.icon_bounding_box_combobox.addItem(QtGui.QIcon(icon_shape_paths[counter]),icon_names[counter])
        self.icon_bounding_box_combobox.setIconSize(QtCore.QSize(35,35))
        #Create layout and return the overall widget.
        layout_panel_layout = QtGui.QGridLayout()
        layout_panel_layout.addWidget(self.background_selection_label,0, 0)
        layout_panel_layout.addWidget(self.background_selection_combobox,1, 0, 1, 2)
        layout_panel_layout.addWidget(self.parent_image_position_selector,0, 3, 10, 2, QtCore.Qt.AlignTop)
        layout_panel_layout.addWidget(self.icon_arrangement_label, 2, 0, 1, 1)
        layout_panel_layout.addWidget(self.icon_arrangement_circular, 3, 0, 1, 1, QtCore.Qt.AlignRight)
        layout_panel_layout.addWidget(self.icon_arrangement_rectangular, 3, 1, 1, 1, QtCore.Qt.AlignLeft)
        layout_panel_layout.addWidget(self.icon_bounding_box_label, 4, 0, 1, 1, QtCore.Qt.AlignRight)
        layout_panel_layout.addWidget(self.icon_bounding_box_combobox, 4, 1, 1, 1, QtCore.Qt.AlignLeft)
        layout_panel = QtGui.QWidget()
        layout_panel.setLayout(layout_panel_layout)
        self.changeBackground()
        return layout_panel

    def getFontPanel(self):
        self.bold_button = QtGui.QPushButton("B")
        self.bold_button.setMaximumWidth(25)
        self.bold_button.setCheckable(True)
        self.bold_button.setStyleSheet("QPushButton {font-weight: bold;}")
        self.italics_button = QtGui.QPushButton("I")
        self.italics_button.setMaximumWidth(25)
        self.italics_button.setCheckable(True)
        self.italics_button.setStyleSheet("QPushButton {font-style: italic;}")
        self.underline_button = QtGui.QPushButton("U")
        self.underline_button.setMaximumWidth(25)
        self.underline_button.setCheckable(True)
        self.underline_button.setStyleSheet("QPushButton {text-decoration: underline;}")
        self.font_size_label = QtGui.QLabel("Font Size:")
        self.font_size_spinbox = QtGui.QSpinBox()
        self.font_size_spinbox.setRange(10,120)
        self.font_color_label = QtGui.QLabel("Font Color:")
        self.font_color_picker = QColorButton()
        self.font_color_picker.setStyleSheet("Click to select a font color. You can override this color in the advanced panel,\nusing the primary icon color as the font color.")
        #Widget for controlling icon color.
        self.palette_selection_label = QtGui.QLabel("Icon Palette:")
        self.palette_selection_buttons = [QColorPanel() for i in range(10)]
        self.palette_reset_button = QtGui.QPushButton("Copy First Row's\ncolors to all rows.")



        font_panel_layout = QtGui.QGridLayout()
        font_panel_layout.addWidget(self.bold_button, 0, 0, 1, 1,
                                    QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        font_panel_layout.addWidget(self.italics_button, 0, 1, 1, 1, 
                                    QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        font_panel_layout.addWidget(self.underline_button, 0, 2, 1, 1, 
                                    QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        font_panel_layout.addWidget(self.font_size_label, 1, 0, 1, 1, 
                                    QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        font_panel_layout.addWidget(self.font_size_spinbox,1, 1, 1, 1, 
                                    QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        font_panel_layout.addWidget(self.font_color_label, 1, 2, 1, 1, 
                                    QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        font_panel_layout.addWidget(self.font_color_picker, 1, 3, 1, 1, 
                                    QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        font_panel_layout.addWidget(self.palette_selection_label, 2, 0, 1, 1,
                                    QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        row = 2
        font_panel_layout.addWidget(self.palette_reset_button, row, 4, 1, 1,
                                    QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        for button in self.palette_selection_buttons:
            font_panel_layout.addWidget(button, row, 1, 2, 1)
            row+=1
        font_panel_layout.addWidget(QtGui.QWidget(), row, 0, 1, 1)



        font_panel_layout.setColumnStretch(0,0)
        font_panel_layout.setColumnStretch(1,0)
        font_panel_layout.setColumnStretch(2,0)
        font_panel_layout.setColumnStretch(3,0)
        font_panel_layout.setColumnStretch(4,0)
        font_panel_layout.setColumnStretch(5,0)
        font_panel_layout.setColumnStretch(6,10)
        font_panel_layout.setColumnStretch(0,0)
        font_panel_layout.setColumnStretch(0,0)
        for i in range(2):
            font_panel_layout.setRowStretch(i,0)
        for i in range(row+2)[2:]:
            font_panel_layout.setRowStretch(i,2)
        font_panel_layout.setRowStretch(row+2,10)
        

        font_panel = QtGui.QWidget()
        font_panel.setLayout(font_panel_layout)
        return font_panel

    def getParentImageSelector(self):
        parent_image_selector = ParentImageSelectorWidget(self.repo_path)
        return parent_image_selector

    def getAdvancedPanel(self):
        #Widget for controlling parent image scaling factor.
        self.product_image_scale_label = QtGui.QLabel("Parent Image Scale:")
        self.product_image_scale_spinbox = QtGui.QDoubleSpinBox()
        self.product_image_scale_spinbox.setToolTip("Choose a scaling factor for the parent image.\nIdeally, 42% is the right answer.")
        self.product_image_scale_spinbox.setRange(10,100)
        self.product_image_scale_spinbox.setSuffix("%")

        #Widget for controlling primary and secondary attribute icon sizes.
        self.primary_attr_icon_size_label = QtGui.QLabel("Set Primary Attribute Icon\nRelative Size:")
        self.primary_attr_icon_size_spin_box = QtGui.QSpinBox()
        self.primary_attr_icon_size_spin_box.setSuffix("%")
        self.primary_attr_icon_size_spin_box.setToolTip("This sets the size of the primary attribute icons, at a percentage relative to the background image.")
        self.primary_attr_icon_size_spin_box.setRange(5,20)
        self.secondary_attr_icon_size_label = QtGui.QLabel("Set Secondary Attribute Icon\nRelative Size:")
        self.secondary_attr_icon_size_spin_box = QtGui.QSpinBox()
        self.secondary_attr_icon_size_spin_box.setSuffix("%")
        self.secondary_attr_icon_size_spin_box.setToolTip("This sets the size of the secondary attribute icons, at a percentage relative to the background image.")
        self.secondary_attr_icon_size_spin_box.setRange(5,20)
        #For changing color replacement algorithm.
        self.use_simple_color_replacement = QtGui.QCheckBox("Use a Simple Colour Extraction Method to remove Parent Image Background.")
        self.use_simple_color_replacement.setToolTip("If selected, the code just finds the likely background color and removes it from the entire message.\nThis method saves a large amount of runtime.\nThis is a risky method if the product image has similar colors, or if the image quality is dodgy.\nExercise with caution.")
        #For changing background color replacement algorithm's threshold.
        self.background_color_threshold_label = QtGui.QLabel("Threshold for Background Color Extraction:")
        self.background_color_threshold_spinbox = QtGui.QSpinBox()
        self.background_color_threshold_spinbox.setPrefix(u"\u00B1")
        self.background_color_threshold_spinbox.setRange(0,255)
        self.background_color_threshold_spinbox.setToolTip("Choose a threshold for the background color elimination algorithm.\n Note that setting a very high threshold will remove most of the colours from the image.\nExercise with caution.\nA value around 10-30 is recommended. 20 has been found to be optimum.")
        #To allow icons to overlap the parent image.
        self.allow_overlap_checkbox = QtGui.QCheckBox("Allow Icons to Overlap the Parent Image")
        self.allow_overlap_checkbox.setToolTip("This allows the icons to be placed over the parent image.\nIcons themselves will never overlap.\nUse with caution, as icon placement becomes messy when enabled.\nThis is best used for small batches.")
        #Widget to control the overall margin.
        self.image_margin_label = QtGui.QLabel("Margin:")
        self.image_margin_spinbox = QtGui.QDoubleSpinBox()
        self.image_margin_spinbox.setRange(0.0, 10.0)
        self.image_margin_spinbox.setSingleStep(0.05)
        self.image_margin_spinbox.setSuffix("%")
        self.image_margin_spinbox.setToolTip("Select a margin, as a percentage of the background, for the background image.")
        #Parent Image resize factor and reference controls.
        self.parent_image_resize_reference_instruction = QtGui.QLabel("Resize Parent Image By:")
        self.parent_image_resize_reference = QtGui.QComboBox()
        self.parent_image_resize_reference.addItems(["Height","Width","Smart Fit"])
        self.parent_image_resize_reference.setToolTip("Choose whether to resize the product image with respect to the height or the width of the base image.")
        #Aspect Ratio controls.
        self.final_image_aspect_ratio_instruction = QtGui.QLabel("Aspect Ratio:")
        self.final_image_aspect_ratio_input_box_1 = QtGui.QSpinBox()
        self.final_image_aspect_ratio_colon = QtGui.QLabel(":")
        self.final_image_aspect_ratio_input_box_2 = QtGui.QSpinBox()
        self.final_image_aspect_ratio_input_box_1.setRange(1,100)
        self.final_image_aspect_ratio_input_box_2.setRange(1,100)
        self.final_image_aspect_ratio_input_box_1.setToolTip("Select the width aspect ratio factor.")
        self.final_image_aspect_ratio_input_box_2.setToolTip("Select the height aspect ratio factor.")
        self.aspect_ratio_widget_layout = QtGui.QHBoxLayout()
        self.aspect_ratio_widget_layout.addWidget(self.final_image_aspect_ratio_input_box_1, 0,
                                            QtCore.Qt.AlignRight)
        self.aspect_ratio_widget_layout.addWidget(self.final_image_aspect_ratio_colon,0)
        self.aspect_ratio_widget_layout.addWidget(self.final_image_aspect_ratio_input_box_2, 0,
                                            QtCore.Qt.AlignLeft)
        self.aspect_ratio_widget_layout.addStretch(10)
        #Checkbox to allow icons without text.
        self.allow_textless_icons_checkbox = QtGui.QCheckBox("Allow Icons Without Text")
        #Preserve icon colors
        self.preserve_icon_colors = QtGui.QCheckBox("Preserve Icon Colors")
        #Fix the icon text case.
        self.fix_icon_text_case = QtGui.QCheckBox("Convert USP Description Text to Title Case")
        self.fix_icon_text_case.setToolTip("Force the first character of the USP description text to capitals. This could result in possible problems.")
        #
        self.use_category_specific_backgrounds = QtGui.QCheckBox("Use Category-Specific Background Images.")
        #
        self.use_icon_color_for_font_color = QtGui.QCheckBox("Use the first color from Icon palette as font color.")

        self.bypass_parent_image_cleanup = QtGui.QCheckBox("Bypass Parent Image Background Cleanup.")
        self.bypass_parent_image_cleanup.setToolTip("This method is useful when running trials.\nIt won't attempt to clean the parent image, and it will paste it as-is.\nBe careful when using this.")
        #Layout
        left_center_alignment = QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        left_top_alignment = QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop
        advanced_panel_layout = QtGui.QGridLayout()
        row, column = 0, 0
        advanced_panel_layout.addWidget(self.image_margin_label, row, column, 
                                    left_center_alignment)
        column += 1
        advanced_panel_layout.addWidget(self.image_margin_spinbox, row, column, 
                                    left_center_alignment)
        row += 1
        column = 0
        advanced_panel_layout.addWidget(self.product_image_scale_label, row, column, 
                                    left_center_alignment)
        column += 1
        advanced_panel_layout.addWidget(self.product_image_scale_spinbox, row, column, 
                                    left_center_alignment)
        row += 1
        column = 0
        advanced_panel_layout.addWidget(self.parent_image_resize_reference_instruction, row, column,
                                    left_center_alignment)
        column += 1
        advanced_panel_layout.addWidget(self.parent_image_resize_reference, row, column,
                                    left_center_alignment)
        row += 1
        column = 0
        advanced_panel_layout.addWidget(self.final_image_aspect_ratio_instruction, row, column, 
                                    left_center_alignment)
        column += 1
        advanced_panel_layout.addLayout(self.aspect_ratio_widget_layout, row, column, 
                                    left_center_alignment)
        row += 1
        column = 0
        advanced_panel_layout.addWidget(self.primary_attr_icon_size_label, row, column, 
                                    left_center_alignment)
        column += 1 
        advanced_panel_layout.addWidget(self.primary_attr_icon_size_spin_box, row, column, 
                                    left_center_alignment)
        row += 1
        column = 0
        advanced_panel_layout.addWidget(self.secondary_attr_icon_size_label, row, column, 
                                    left_center_alignment)
        column += 1
        advanced_panel_layout.addWidget(self.secondary_attr_icon_size_spin_box, row, column, 
                                    left_center_alignment)
        row += 1
        column = 0
        advanced_panel_layout.addWidget(self.background_color_threshold_label, row, column, 
                                    left_center_alignment)
        column += 1
        advanced_panel_layout.addWidget(self.background_color_threshold_spinbox, row, column, 
                                    left_center_alignment)
        row += 1
        column = 0
        advanced_panel_layout.addWidget(self.use_simple_color_replacement, row, column,1,2, 
                                    left_center_alignment)
        
        row += 1
        column = 0
        advanced_panel_layout.addWidget(self.bypass_parent_image_cleanup, row, column,1,2, 
                                    left_center_alignment)
        row += 1
        column = 0
        advanced_panel_layout.addWidget(self.preserve_icon_colors, row, column, 1, 2, 
                                    left_top_alignment)
        row += 1
        column = 0
        advanced_panel_layout.addWidget(self.allow_overlap_checkbox, row, column, 1, 2, 
                                    left_center_alignment)
        row += 1
        column = 0
        advanced_panel_layout.addWidget(self.fix_icon_text_case, row, column, 1, 2, 
                                    left_center_alignment)
        
        row += 1
        column = 0
        advanced_panel_layout.addWidget(self.use_category_specific_backgrounds, row, column, 1, 2, 
                                    left_center_alignment)

        row += 1
        column = 0
        advanced_panel_layout.addWidget(self.use_icon_color_for_font_color, row, column, 1, 2, 
                                    left_center_alignment)
        
        row += 1
        column = 0
        advanced_panel_layout.addWidget(self.allow_textless_icons_checkbox, row, column, 1, 2, 
                                    left_top_alignment)
        advanced_panel_layout.setColumnStretch(0, 0)
        advanced_panel_layout.setColumnStretch(1, 0)
        advanced_panel_layout.setColumnStretch(2, 10)
        for row_number in range(row):
            advanced_panel_layout.setRowStretch(row_number,0)
        advanced_panel_layout.setRowStretch(row, 10)
        advanced_panel = QtGui.QWidget()
        advanced_panel.setLayout(advanced_panel_layout)
        scrollable_widget = QtGui.QScrollArea()
        scrollable_widget.setWidget(advanced_panel)
        scrollable_widget.setWidgetResizable(True)
        scrollable_widget.setFixedHeight(350)

        return scrollable_widget

    def mapEvents(self):
        self.background_selection_combobox.currentIndexChanged.connect(self.changeBackground)
        self.use_random_parent_image_position.stateChanged.connect(self.toggleRandomParentPosition)
        self.primary_attr_icon_size_spin_box.valueChanged.connect(self.limitSecondaryIconSize)
        self.reset_settings_button.clicked.connect(self.resetValues)
        self.save_settings_button.clicked.connect(self.saveSettingsToJSON)
        self.load_settings_from_file_button.clicked.connect(self.loadSettingsFromJSON)
        self.splinter_thread.progress.connect(self.displayProgress)
        self.splinter_thread.sendMessage.connect(self.displayActivity)
        self.splinter_thread.sendCoords.connect(self.position_widget.setCoords)
        self.update_preview_button.clicked.connect(self.runSplinter)
        self.stop_button.clicked.connect(self.stopRunning)
        self.preview_widget.clicked.connect(self.openImage)
        self.palette_reset_button.clicked.connect(self.resetPalette)
        self.left_button.clicked.connect(self.showPreviousImage)
        self.right_button.clicked.connect(self.showNextImage)
        self.open_destination_folder.clicked.connect(self.openDestinationFolder)

    def openDestinationFolder(self):
        import subprocess
        if self.current_image is not None:
            subprocess.call('explorer /select,"%s"'%self.current_image, shell=True)

    def resetPalette(self):
        palette = self.getIconPalette()[0]
        for button in self.palette_selection_buttons:
            button.setColors(palette)

    def loadSettingsFromJSON(self):
        open_file_name = QtGui.QFileDialog.getOpenFileName(self, "Load Settings from a JSON",
                                                        os.getcwd(), ("JSON files (*.json)")
                                                        )
        if open_file_name:
            if os.path.isfile(open_file_name):
                self.setValues(open_file_name)

    def saveSettingsToJSON(self):
        save_file_name = QtGui.QFileDialog.getSaveFileName(self, "Save Settings To a JSON",
                                                        os.getcwd(), ("JSON files (*.json)")
                                                        )
        if save_file_name:
            settings = self.getCurrentSettings()
            with open(save_file_name,"w") as json_file_handler:
                json.dump(settings,json_file_handler,indent=4,sort_keys=True)


    def limitSecondaryIconSize(self,maximum_primary_value):
        self.secondary_attr_icon_size_spin_box.setMaximum(maximum_primary_value)
   
    def toggleRandomParentPosition(self):
        state = not(self.use_random_parent_image_position.isChecked())
        for radiobuttons_row in self.parent_image_position_position_radiobuttons:
            for radiobutton in radiobuttons_row:
                radiobutton.setEnabled(state)

    def changeBackground(self):
        self.current_background = str(self.background_selection_combobox.currentText())
        if self.current_background != "Random":
            self.current_background_path = os.path.join(self.repo_path,"Backgrounds",self.current_background)
            self.background_image_pixmap = QtGui.QPixmap(self.current_background_path)
            self.background_image_pixmap = self.background_image_pixmap.scaled(self.background_preview_space.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation)
            self.background_preview_space.setPixmap(self.background_image_pixmap)
        else:
            random_image_path = os.path.join("essentials","random_background.png")
            self.background_image_pixmap = QtGui.QPixmap(random_image_path)
            self.background_image_pixmap = self.background_image_pixmap.scaled(self.background_preview_space.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation)
            self.background_preview_space.setPixmap(self.background_image_pixmap)

    def getParentImageCoords(self):
        if self.use_random_parent_image_position.isChecked():
            return "Random"
        else:
            number_of_rows_or_columns = 2
            for i in range(number_of_rows_or_columns+1):
                for j in range(number_of_rows_or_columns+1):
                    if self.parent_image_position_position_radiobuttons[i][j].isChecked():
                        return (j/number_of_rows_or_columns,i/number_of_rows_or_columns)

    def getIconPosition(self):
        if self.icon_arrangement_circular.isChecked():
            position = "Circular"
        else:
            position = "Rectangular"
        return position

    def getIconPalette(self):
        return [palette_selection_button.getColors() for palette_selection_button in self.palette_selection_buttons]
    
    def getCoords(self):
        return self.position_widget.getCoords()
    
    def getOverlap(self):
        return self.allow_overlap_checkbox.isChecked()

    def getBackgroundImage(self):
        self.changeBackground()
        return (self.current_background if self.current_background == "Random" else self.current_background_path)

    def getIconBoundingBox(self):
        return str(self.icon_bounding_box_combobox.currentText())

    def getPrimaryAttrRelativeSize(self):
        return (self.primary_attr_icon_size_spin_box.value()/100)

    def getSecondaryAttrRelativeSize(self):
        return (self.secondary_attr_icon_size_spin_box.value()/100)

    def useSimpleColorStripAlgorithm(self):
        return self.use_simple_color_replacement.isChecked()

    def getColorStripThreshold(self):
        return self.background_color_threshold_spinbox.value()

    def getParentImageResizeReference(self):
        return str(self.parent_image_resize_reference.currentText())

    def getParentImageResizeFactor(self):
        resize = int(self.product_image_scale_spinbox.value())/100
        return resize

    def getAspectRatio(self):
        width = int(self.final_image_aspect_ratio_input_box_1.value())
        height = int(self.final_image_aspect_ratio_input_box_2.value())
        return width, height #is this order fine?

    def allowTextlessIcons(self):
        return self.allow_textless_icons_checkbox.isChecked()

    def getMargin(self):
         return (self.image_margin_spinbox.value()/100)

    def loadIconColorsFromBackground(self):
        return False #Add handles for this later.

    def getIconFontColor(self):
        return self.font_color_picker.getColor()

    def useIconColorForFontColor(self):
        return self.use_icon_color_for_font_color.isChecked()

    def getIconFontSize(self):
        return self.font_size_spinbox.value()

    def allowOverlap(self):
        return False #Add functionality for this later.

    def useCategorySpecificBackgrounds(self):
        return self.use_category_specific_backgrounds.isChecked() #Add a handle for this later.

    def preserveIconColors(self):
        return self.preserve_icon_colors.isChecked()

    def fixIconTextCase(self):
        return self.fix_icon_text_case.isChecked()

    def showPositionMarkers(self):
        return self.position_widget.showPositionMarkers()

    def getFont(self):
        import os
        is_bold = self.bold_button.isChecked()
        is_italics = self.italics_button.isChecked()
        if is_bold and is_italics:
            font = os.path.join("essentials", "RionaSans-BoldItalic.ttf")
        elif is_bold and (not is_italics):
            font = os.path.join("essentials", "RionaSans-Bold.ttf")
        elif (not is_bold) and is_italics:
            font = os.path.join("essentials", "RionaSans-MediumItalic.ttf")
        else:
            font = os.path.join("essentials", "RionaSans-Medium.ttf")
        return font

    def bypassParentImageCleanup(self):
        return self.bypass_parent_image_cleanup.isChecked()

    def getParentImagePaths(self):
        return self.parent_image_selector.getParentImagesData()
    
    def useEnforcedCoordinates(self):
        return self.position_widget.useEnforcedCoordinates()
    
    def getCurrentSettings(self):
        """Returns a dictionary that summarizes all the current settings."""
        parent_image_resize_factor = self.getParentImageResizeFactor()
        icon_font_italics = self.italics_button.isChecked()
        icon_arrangement_value = self.getIconPosition()
        image_aspect_ratio = self.getAspectRatio()
        use_simple_color_replacement = self.useSimpleColorStripAlgorithm()
        icon_font_underline = self.underline_button.isChecked()
        allow_overlap = self.allowOverlap()
        allow_textless_icons = self.allowTextlessIcons()
        parent_image_resize_reference = self.getParentImageResizeReference()
        icon_palette = self.getIconPalette()
        background_color_threshold = self.getColorStripThreshold()
        load_icon_color_from_background = self.loadIconColorsFromBackground()
        primary_attr_icon_size_value = self.primary_attr_icon_size_spin_box.value()
        secondary_attr_icon_size_value = self.secondary_attr_icon_size_spin_box.value()
        icon_font_color = self.getIconFontColor()
        use_icon_color_for_font_color = self.useIconColorForFontColor()
        parent_image_position = self.getParentImageCoords()
        icon_font_size = self.getIconFontSize()
        margin = self.getMargin()
        icon_font_bold = self.bold_button.isChecked()
        preserve_icon_colors = self.preserveIconColors()
        fix_icon_text_case = self.fixIconTextCase()
        icon_bounding_box = self.getIconBoundingBox()
        use_category_specific_backgrounds = self.useCategorySpecificBackgrounds()
        background_image = self.current_background
        icon_font_size = self.getIconFontSize()
        bypass_parent_image_cleanup = self.bypassParentImageCleanup()


        settings = {
                    "Parent Image Resize Factor": parent_image_resize_factor, 
                    "Icon Palette": icon_palette, 
                    "Icon Font Italics": icon_font_italics, 
                    "Icon Font Bold": icon_font_bold,
                    "Icon Font Underline": icon_font_underline, 
                    "Image Aspect Ratio": image_aspect_ratio, 
                    "Icon Arrangement": icon_arrangement_value, 
                    "Use Simple Color Replacement": use_simple_color_replacement, 
                    "Allow Icons Overlap": allow_overlap, 
                    "Allow Icons Without Text": allow_textless_icons, 
                    "Parent Image Resize Reference": parent_image_resize_reference, 
                    "Background Color Threshold Value": background_color_threshold, 
                    "Load Icon Colors From Background": load_icon_color_from_background, 
                    "Primary Attribute Relative Size": primary_attr_icon_size_value, 
                    "Secondary Attribute Relative Size": secondary_attr_icon_size_value, 
                    "Icon Font Color": icon_font_color, 
                    "Use Icon Color For Font Color": use_icon_color_for_font_color, 
                    "Parent Image Position": parent_image_position, 
                    "Icon Font Size": icon_font_size, 
                    "Margin": margin, 
                    "Icon Bounding Box": icon_bounding_box,
                    "Fix Icon Text Case": fix_icon_text_case,
                    "Preserve Icon Colors": preserve_icon_colors,
                    "Use Category Specific Backgrounds": use_category_specific_backgrounds,
                    "Background Image": background_image,
                    "Icon Font Size": icon_font_size,
                    "Bypass Parent Image Cleanup": bypass_parent_image_cleanup
                }
        return settings
