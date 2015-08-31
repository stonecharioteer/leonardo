from __future__ import division
import os, glob, random
from PyQt4 import QtGui, QtCore
from FSNTextEdit import FSNTextEdit
from IconButton import IconButton
#from FileLocationWidget import FileLocationWidget
from PrimaryButton import PrimaryButton
from QColorButton import QColorButton

class LayoutDesigner(QtGui.QWidget):
    def __init__(self):
        super(LayoutDesigner,self).__init__()
        self.createUI()
        self.mapEvents()
        self.primary_attr_icon_size_spin_box.setValue(7)

    def createUI(self):
        #Modularized.
        self.preview_group_box = self.createPreviewWidget()
        self.settings_group_box = self.createSettingsWidget()
        self.validate_button  = IconButton(os.path.join("essentials","validate.png"))
        self.validate_button.setToolTip("Validate and Proceed")
        final_ui_layout = QtGui.QGridLayout()
        final_ui_layout.addWidget(self.settings_group_box,0,0,10,4)
        final_ui_layout.addWidget(self.preview_group_box,0,4,10,4, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        final_ui_layout.addWidget(self.validate_button,10,9,1,1, QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
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
        self.preview_widget.setFixedSize(90*size_modifier, 160*size_modifier)
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

        #Create the settings panels. Use a QToolBox
        self.settings_group_box = QtGui.QGroupBox("Settings")

        self.settings_tool_box = QtGui.QToolBox()
        self.layout_panel = self.getLayoutPanel()
        self.font_panel = self.getFontPanel()
        self.advanced_panel = self.getAdvancedPanel()
        self.settings_tool_box.addItem(self.layout_panel, "Layout and Icon Positions")
        self.settings_tool_box.addItem(self.font_panel, "Icon Text Font Settings")
        self.settings_tool_box.addItem(self.advanced_panel, "Advanced Settings")
        settings_layout = QtGui.QHBoxLayout()
        settings_layout.addWidget(self.settings_tool_box)
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
        self.parent_image_position_position_radiobuttons[1][0].setChecked(True) #Default position
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
        self.icon_arrangement_circular.setChecked(True)
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
        self.italics_button = QtGui.QPushButton("I")
        self.underline_button = QtGui.QPushButton("U")
        self.font_size_label = QtGui.QLabel("Font Size:")
        self.font_size_spinbox = QtGui.QSpinBox()
        self.font_size_spinbox.setRange(30,72)
        self.font_color_label = QtGui.QLabel("Font Color:")
        self.font_color_combobox = QtGui.QComboBox()
        self.font_color_combobox.addItems(["Black","White","FK Blue","FK Yellow","Auto Select","Choose Manually"])
        self.font_color_picker = QColorButton()

        font_panel_layout = QtGui.QGridLayout()
        font_panel_layout.addWidget(self.bold_button, 0, 0)
        font_panel_layout.addWidget(self.italics_button, 0, 1)
        font_panel_layout.addWidget(self.underline_button, 0, 2)
        font_panel_layout.addWidget(self.font_size_label,1,0)
        font_panel_layout.addWidget(self.font_size_spinbox,1,1)
        font_panel_layout.addWidget(self.font_color_label,2,0)
        font_panel_layout.addWidget(self.font_color_combobox,2,1)
        font_panel_layout.addWidget(self.font_color_picker,2,2)
        font_panel = QtGui.QWidget()
        font_panel.setLayout(font_panel_layout)
        return font_panel

    def getAdvancedPanel(self):
        #Widget for controlling parent image scaling factor.
        self.product_image_scale_label = QtGui.QLabel("Parent Image Scale:")
        self.product_image_scale_spinbox = QtGui.QDoubleSpinBox()
        self.product_image_scale_spinbox.setToolTip("Choose a scaling factor for the parent image.\nIdeally, 42% is the right answer.")
        self.product_image_scale_spinbox.setValue(42)
        self.product_image_scale_spinbox.setRange(25,50)
        self.product_image_scale_spinbox.setSuffix("%")
        #Widget for controlling icon color.
        self.palette_selection_label = QtGui.QLabel("Icon Palette:")
        self.palette_selection_combobox = QtGui.QComboBox()
        self.palette_selection_combobox.setToolTip("Choose one colour and the program picks a palette that will suit that color.\nHowever, manual QC is required for the generated images, as the program\ndoesn't yet look at the parent or background image color,\nso if the same color is picked, the image will look messy.")
        palettes_list = ["Black","Based on Input Color","From Input File"]
        self.palette_selection_combobox.addItems(palettes_list)
        self.palette_selection_button = QColorButton()
        #Widget for controlling primary and secondary attribute icon sizes.
        self.primary_attr_icon_size_label = QtGui.QLabel("Set Primary Attribute Icon\nRelative Size:")
        self.primary_attr_icon_size_spin_box = QtGui.QSpinBox()
        self.primary_attr_icon_size_spin_box.setSuffix("%")
        self.primary_attr_icon_size_spin_box.setToolTip("This sets the size of the primary attribute icons, at a percentage relative to the background image.")
        self.primary_attr_icon_size_spin_box.setRange(5,8)
        self.secondary_attr_icon_size_label = QtGui.QLabel("Set Secondary Attribute Icon\nRelative Size:")
        self.secondary_attr_icon_size_spin_box = QtGui.QSpinBox()
        self.secondary_attr_icon_size_spin_box  .setSuffix("%")
        self.secondary_attr_icon_size_spin_box.setToolTip("This sets the size of the secondary attribute icons, at a percentage relative to the background image.")
        self.secondary_attr_icon_size_spin_box.setRange(5,8)
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
        self.background_color_threshold_spinbox.setValue(20)
        self.background_color_threshold_spinbox.setToolTip("Choose a threshold for the background color elimination algorithm.\n Note that setting a very high threshold will remove most of the colours from the image.\nExercise with caution.\nA value around 10-30 is recommended. 20 has been found to be optimum.")
        #To allow icons to overlap the parent image.
        self.allow_overlap_checkbox = QtGui.QCheckBox("Allow Icons to Overlap the Parent Image")
        self.allow_overlap_checkbox.setToolTip("This allows the icons to be placed over the parent image.\nIcons themselves will never overlap.\nUse with caution, as icon placement becomes messy when enabled.\nThis is best used for small batches.")
        #Widget to control the overall margin.
        self.image_margin_label = QtGui.QLabel("Margin:")
        self.image_margin_spinbox = QtGui.QDoubleSpinBox()
        self.image_margin_spinbox.setRange(0.0, 10.0)
        self.image_margin_spinbox.setValue(5.0)
        self.image_margin_spinbox.setSuffix("px")
        self.image_margin_spinbox.setToolTip("Select a margin, in pixels, for the background image.\nAll items, except the Flipkart Logo, will be placed taking the margin into account.")
        
        advanced_panel_layout = QtGui.QGridLayout()
        advanced_panel_layout.addWidget(self.image_margin_label,0,0)
        advanced_panel_layout.addWidget(self.image_margin_spinbox,0,1)
        advanced_panel_layout.addWidget(self.product_image_scale_label,1,0)
        advanced_panel_layout.addWidget(self.product_image_scale_spinbox,1,1)
        advanced_panel_layout.addWidget(self.primary_attr_icon_size_label,2,0)
        advanced_panel_layout.addWidget(self.primary_attr_icon_size_spin_box,2,1)
        advanced_panel_layout.addWidget(self.secondary_attr_icon_size_label,3,0)
        advanced_panel_layout.addWidget(self.secondary_attr_icon_size_spin_box,3,1)
        advanced_panel_layout.addWidget(self.use_simple_color_replacement,4,0,1,2)
        advanced_panel_layout.addWidget(self.background_color_threshold_label,5,0)
        advanced_panel_layout.addWidget(self.background_color_threshold_spinbox,5,1)
        advanced_panel_layout.addWidget(self.palette_selection_label,6,0)
        advanced_panel_layout.addWidget(self.palette_selection_combobox,6,1)
        advanced_panel_layout.addWidget(self.palette_selection_button,6,2)
        advanced_panel_layout.addWidget(self.icon_bounding_box_label,7,0)
        advanced_panel_layout.addWidget(self.icon_bounding_box_combobox,7,1)
        advanced_panel_layout.addWidget(self.allow_overlap_checkbox,8,0,1,2)
        advanced_panel = QtGui.QWidget()
        advanced_panel.setLayout(advanced_panel_layout)
        return advanced_panel

    def mapEvents(self):
        self.background_selection_combobox.currentIndexChanged.connect(self.changeBackground)
        self.use_random_parent_image_position.stateChanged.connect(self.toggleRandomParentPosition)
        self.primary_attr_icon_size_spin_box.valueChanged.connect(self.limitSecondaryIconSize)

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
        return "Black" #Fix this later.
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

            