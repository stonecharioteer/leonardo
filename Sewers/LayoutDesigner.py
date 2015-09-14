from __future__ import division
import os, glob, random
import json
from PyQt4 import QtGui, QtCore
from FSNTextEdit import FSNTextEdit
from IconButton import IconButton
#from FileLocationWidget import FileLocationWidget
from PrimaryButton import PrimaryButton
from QColorButton import QColorButton

class LayoutDesigner(QtGui.QWidget):
    def __init__(self):
        super(LayoutDesigner,self).__init__()
        defaults = {
                    "Parent Image Resize Factor": 42, 
                    "Icon Font Italics": True, 
                    "Image Aspect Ratio": [9, 14], 
                    "Icon Arrangement": "Circular", 
                    "Use Simple Color Replacement": True, 
                    "Icon Font Underline": False, 
                    "Allow Icons Overlap": False, 
                    "Allow Icons Without Text": False, 
                    "Parent Image Resize Reference": "Width", 
                    "Icon Palette": [0, 0, 0], 
                    "Background Color Threshold Value": 15, 
                    "Secondary Attribute Relative Size": 8, 
                    "Load Icon Colors From Background": False, 
                    "Primary Attribute Relative Size": 8, 
                    "Icon Font Color": [0, 0, 0], 
                    "Use Icon Color For Font Color": True, 
                    "Parent Image Position": [1, 1], 
                    "Icon Font Size": 30, 
                    "Margin": 5.0, 
                    "Icon Font Bold": False
                }
        #with open(os.path.join("cache","defaults.json"),"w") as json_file_handler:
        #    json.dump(defaults,json_file_handler, indent=4, sort_keys=True)
        self.createUI()
        self.mapEvents()
        #Load values from the default file.
        self.resetValues()
        

    def resetValues(self):
        default_file = os.path.join("cache","defaults.json")
        if os.path.isfile(default_file):
            self.setValues(default_file)

    def setValues(self, file_path):
        """Sets the defaults for the settings.
        At a later stage, I need to read from and export to a JSON file. 
        That way, things will be much smoother and I can have saved settings.
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
        if type(parent_image_position_value) != str:
            y, x = parent_image_position_value
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
        icon_color_value = settings_from_json["Icon Palette"]
        self.palette_selection_combobox.setCurrentIndex(1)
        
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

        #Set the icon font color
        #Set the bool to use the icon color for font color.
        use_icon_color_for_font_color = settings_from_json["Use Icon Color For Font Color"]
        if type(use_icon_color_for_font_color) != bool:
            use_icon_color_for_font_color = False
        if use_icon_color_for_font_color:
            icon_font_color = icon_color_value
        else:
            icon_font_color = settings_from_json["Icon Font Color"]
        icon_font_r, icon_font_g, icon_font_b = icon_font_color

        #Set the background-appropriate icon color loading behaviour.
        load_icon_color_from_background = settings_from_json["Load Icon Colors From Background"]
        if type(load_icon_color_from_background) != bool:
            load_icon_color_from_background = False


    def createUI(self):        
        self.preview_group_box = self.createPreviewWidget()
        self.settings_group_box = self.createSettingsWidget()
        self.validate_button  = IconButton(os.path.join("essentials","validate.png"))
        self.validate_button.setToolTip("Validate and Proceed")
        
        final_ui_layout = QtGui.QGridLayout()
        final_ui_layout.addWidget(self.settings_group_box,0, 0, 10, 4)
        final_ui_layout.addWidget(self.preview_group_box,0, 4, 10, 4, 
                                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        final_ui_layout.addWidget(self.validate_button,10, 9, 1, 1, 
                                QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        
        self.over_all_group_box = QtGui.QGroupBox("Design")
        self.over_all_group_box.setLayout(final_ui_layout)
        
        over_all_layout_wrapper = QtGui.QHBoxLayout()
        over_all_layout_wrapper.addWidget(self.over_all_group_box)
        
        self.setLayout(over_all_layout_wrapper)

    def createPreviewWidget(self):
        #Creates the preview pane.
        self.update_preview_button = QtGui.QPushButton("Update")
        self.preview_widget = QtGui.QLabel("Preview goes here.")
        size_modifier = 3
        self.preview_widget.setFixedSize(90*size_modifier, 140*size_modifier)
        preview_widget_style_sheet = """
                                QLabel {
                                    background-color: grey;
                                    border: 2px solid black;
                                };
                                """
        self.preview_widget.setStyleSheet(preview_widget_style_sheet)
        preview_layout = QtGui.QVBoxLayout()
        preview_layout.addWidget(self.update_preview_button,0)
        preview_layout.addWidget(self.preview_widget,3)
        preview_group_box = QtGui.QGroupBox("Preview")
        preview_group_box.setLayout(preview_layout)
        return preview_group_box

    def createSettingsWidget(self):
        #Create the settings panels.
        self.settings_group_box = QtGui.QGroupBox("Settings")

        self.settings_tool_box = QtGui.QToolBox()
        self.layout_panel = self.getLayoutPanel()
        self.font_panel = self.getFontPanel()
        self.advanced_panel = self.getAdvancedPanel()
        self.settings_tool_box.addItem(self.layout_panel, "Layout and Icon Positions")
        self.settings_tool_box.addItem(self.font_panel, "Icon Text Font Settings")
        self.settings_tool_box.addItem(self.advanced_panel, "Advanced Settings")
        
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
        self.backgrounds = ["Random"] + glob.glob(os.path.join(os.path.join(os.path.join(os.getcwd(),"Images"),"Backgrounds"),"Background*.*"))
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

        #Create layout and return the overall widget.
        layout_panel_layout = QtGui.QGridLayout()
        layout_panel_layout.addWidget(self.background_selection_label,0, 0)
        layout_panel_layout.addWidget(self.background_selection_combobox,1,0,1,2)
        layout_panel_layout.addWidget(self.parent_image_position_selector,0,3,10,2, QtCore.Qt.AlignTop)
        layout_panel_layout.addWidget(self.icon_arrangement_label, 2, 0, 1, 1)
        layout_panel_layout.addWidget(self.icon_arrangement_circular, 3, 0, 1, 1, QtCore.Qt.AlignRight)
        layout_panel_layout.addWidget(self.icon_arrangement_rectangular, 3, 1, 1, 1, QtCore.Qt.AlignLeft)
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
        self.font_size_spinbox.setRange(30,72)
        self.font_color_label = QtGui.QLabel("Font Color:")
        self.font_color_combobox = QtGui.QComboBox()
        self.font_color_combobox.addItems(["Black","White","FK Blue","FK Yellow","Auto Select","Choose Manually"])
        self.font_color_picker = QColorButton()

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
        font_panel_layout.addWidget(self.font_color_label, 2, 0, 1, 1, 
                                    QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        font_panel_layout.addWidget(self.font_color_combobox, 2, 1, 1, 1, 
                                    QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        font_panel_layout.addWidget(self.font_color_picker,2, 2, 1, 1, 
                                    QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        font_panel_layout.setColumnStretch(0,0)
        font_panel_layout.setColumnStretch(1,0)
        font_panel_layout.setColumnStretch(2,10)
        font_panel_layout.setColumnStretch(0,0)
        font_panel_layout.setColumnStretch(0,0)
        font_panel_layout.setRowStretch(0,0)
        font_panel_layout.setRowStretch(1,0)
        font_panel_layout.setRowStretch(2,10)

        font_panel = QtGui.QWidget()
        font_panel.setLayout(font_panel_layout)
        return font_panel

    def getAdvancedPanel(self):
        #Widget for controlling parent image scaling factor.
        self.product_image_scale_label = QtGui.QLabel("Parent Image Scale:")
        self.product_image_scale_spinbox = QtGui.QDoubleSpinBox()
        self.product_image_scale_spinbox.setToolTip("Choose a scaling factor for the parent image.\nIdeally, 42% is the right answer.")
        self.product_image_scale_spinbox.setRange(10,100)
        self.product_image_scale_spinbox.setSuffix("%")
        #Widget for controlling icon color.
        self.palette_selection_label = QtGui.QLabel("Icon Palette:")
        self.palette_selection_combobox = QtGui.QComboBox()
        self.palette_selection_combobox.setToolTip("Choose one colour and the program picks a palette that will suit that color.\nHowever, manual QC is required for the generated images, as the program\ndoesn't yet look at the parent or background image color,\nso if the same color is picked, the image will look messy.")
        palettes_list = ["Black","Background Appropriate Color","Based on Input Color"]
        self.palette_selection_combobox.addItems(palettes_list)
        self.palette_selection_button = QColorButton()
        self.palette_selection_combobox.setMinimumHeight(self.palette_selection_button.size().height())
        palette_layout = QtGui.QHBoxLayout()
        palette_layout.addWidget(self.palette_selection_combobox,0,QtCore.Qt.AlignRight)
        palette_layout.addWidget(self.palette_selection_button,0,QtCore.Qt.AlignLeft)
        palette_layout.addStretch(10)
        #Widget for controlling primary and secondary attribute icon sizes.
        self.primary_attr_icon_size_label = QtGui.QLabel("Set Primary Attribute Icon\nRelative Size:")
        self.primary_attr_icon_size_spin_box = QtGui.QSpinBox()
        self.primary_attr_icon_size_spin_box.setSuffix("%")
        self.primary_attr_icon_size_spin_box.setToolTip("This sets the size of the primary attribute icons, at a percentage relative to the background image.")
        self.primary_attr_icon_size_spin_box.setRange(5,10)
        self.secondary_attr_icon_size_label = QtGui.QLabel("Set Secondary Attribute Icon\nRelative Size:")
        self.secondary_attr_icon_size_spin_box = QtGui.QSpinBox()
        self.secondary_attr_icon_size_spin_box  .setSuffix("%")
        self.secondary_attr_icon_size_spin_box.setToolTip("This sets the size of the secondary attribute icons, at a percentage relative to the background image.")
        self.secondary_attr_icon_size_spin_box.setRange(5,10)
        #Widget for controlling icon bounding box.
        self.icon_bounding_box_label = QtGui.QLabel("Icon Bounding Box Shape:")
        self.icon_bounding_box_combobox = QtGui.QComboBox()
        self.icon_bounding_box_combobox.addItems(["None","Circle","Rectangle","Square"])
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
        advanced_panel_layout.addWidget(self.palette_selection_label, row, column, 
                                    left_center_alignment)
        column += 1
        advanced_panel_layout.addLayout(palette_layout, row, column, 
                                    left_center_alignment)
        row += 1
        column = 0
        advanced_panel_layout.addWidget(self.icon_bounding_box_label, row, column, 
                                    left_center_alignment)
        column += 1
        advanced_panel_layout.addWidget(self.icon_bounding_box_combobox, row, column, 
                                    left_center_alignment)
        row += 1
        column = 0
        advanced_panel_layout.addWidget(self.use_simple_color_replacement, row, column,1,2, 
                                    left_center_alignment)
        row += 1
        column = 0
        advanced_panel_layout.addWidget(self.allow_overlap_checkbox, row, column, 1, 2, 
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
        return advanced_panel

    def mapEvents(self):
        self.background_selection_combobox.currentIndexChanged.connect(self.changeBackground)
        self.use_random_parent_image_position.stateChanged.connect(self.toggleRandomParentPosition)
        self.primary_attr_icon_size_spin_box.valueChanged.connect(self.limitSecondaryIconSize)
        self.reset_settings_button.clicked.connect(self.resetValues)
        self.save_settings_button.clicked.connect(self.saveSettingsToJSON)
        self.load_settings_from_file_button.clicked.connect(self.loadSettingsFromJSON)

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
            self.current_background_path = self.current_background
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
        return (0,0,0) #Fix this later.

    def getOverlap(self):
        return self.allow_overlap_checkbox.isChecked()

    def getBackgroundImage(self):
        self.changeBackground()
        return self.current_background

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
        return "False" #Add handles for this later.

    def getIconFontColor(self):
        return (0,0,0)

    def useIconColorForFontColor(self):
        return True

    def getIconFontSize(self):
        return self.font_size_spinbox.value()

    def allowOverlap(self):
        return False #Add functionality for this later.

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
        icon_bounding_box = self.getIconBoundingBox()


        settings = {
                    "Parent Image Resize Factor": parent_image_resize_factor, 
                    "Icon Font Italics": icon_font_italics, 
                    "Image Aspect Ratio": image_aspect_ratio, 
                    "Icon Arrangement": icon_arrangement_value, 
                    "Use Simple Color Replacement": use_simple_color_replacement, 
                    "Icon Font Underline": icon_font_underline, 
                    "Allow Icons Overlap": allow_overlap, 
                    "Allow Icons Without Text": allow_textless_icons, 
                    "Parent Image Resize Reference": parent_image_resize_reference, 
                    "Icon Palette": icon_palette, 
                    "Background Color Threshold Value": background_color_threshold, 
                    "Load Icon Colors From Background": load_icon_color_from_background, 
                    "Primary Attribute Relative Size": primary_attr_icon_size_value, 
                    "Secondary Attribute Relative Size": secondary_attr_icon_size_value, 
                    "Icon Font Color": icon_font_color, 
                    "Use Icon Color For Font Color": use_icon_color_for_font_color, 
                    "Parent Image Position": parent_image_position, 
                    "Icon Font Size": icon_font_size, 
                    "Margin": margin, 
                    "Icon Font Bold": icon_font_bold
                }
        return settings