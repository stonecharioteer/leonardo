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
        #self.output_images_location_widget = FileLocationWidget("Output")
        self.use_random_parent_image_position = QtGui.QCheckBox("Place Parent Image Randomly for Each FSN.")
        self.use_random_parent_image_position.setToolTip("This makes the program pick a random position for the parent image.\This provides true variation in icon positions as well.")
        self.parent_image_position_position_radiobuttons = []
        vpos = {0: "Top", 1:"Middle", 2:"Bottom"}
        hpos = {0: "Left", 1:"Center", 2:"Right"}
        for i in range(3):
            self.parent_image_position_position_radiobuttons.append([QtGui.QRadioButton() for j in range(3)])
        #print self.parent_image_position_position_radiobuttons

        self.parent_image_position_selector_radiobuttons_group = QtGui.QButtonGroup()
        for i in range(3):
            for j in range(3):
                self.parent_image_position_selector_radiobuttons_group.addButton(self.parent_image_position_position_radiobuttons[i][j])
                self.parent_image_position_position_radiobuttons[i][j].setToolTip("This sets the position of the parent image to the %s %s of the image.\nPlease note that the representation isn't exact and\nthe final image layout may vary as constraints dictate." %(vpos[i], hpos[j]))
        self.parent_image_position_selector_radiobuttons_group.setExclusive(True)
        self.parent_image_position_position_radiobuttons[1][1].setChecked(True)
        self.parent_image_position_selector_layout = QtGui.QGridLayout()
        self.background_preview_space = QtGui.QLabel()
        self.background_preview_space.setFixedSize(170, 300)        
        self.parent_image_position_selector_layout.addWidget(self.background_preview_space,0,0,3,3,QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        halignment = [QtCore.Qt.AlignLeft, QtCore.Qt.AlignHCenter, QtCore.Qt.AlignRight]
        valignment = [QtCore.Qt.AlignTop, QtCore.Qt.AlignVCenter, QtCore.Qt.AlignBottom]
        for i in range(3):
            for j in range(3):
                self.parent_image_position_selector_layout.addWidget(self.parent_image_position_position_radiobuttons[i][j],i,j,1,1,halignment[j]|valignment[i])
        self.parent_image_position_selector = QtGui.QGroupBox("Parent Image Position:")
        self.parent_image_position_selector.setLayout(self.parent_image_position_selector_layout)
        self.parent_image_position_selector.setFixedSize(192,335)

        self.image_margin_label = QtGui.QLabel("Margin:")
        self.image_margin_spinbox = QtGui.QDoubleSpinBox()
        self.image_margin_spinbox.setRange(0.0,10.0)
        self.image_margin_spinbox.setValue(5.0)
        self.image_margin_spinbox.setSuffix("px")
        self.image_margin_spinbox.setToolTip("Select a margin, in pixels, for the background image. All items, except the Flipkart Logo, will be placed taking the margin into account.")
        
        self.font_color_label = QtGui.QLabel("Font Color:")
        self.font_color_picker = QColorButton()
        self.font_color_picker_checkbox = QtGui.QCheckBox("Use Appropriate Color(s)")
        self.font_color_picker_checkbox.setToolTip("Processes an appropriate color based on the background image's most featured color.")

        self.product_image_scale_label = QtGui.QLabel("Parent Image Scale:")
        self.product_image_scale_spinbox = QtGui.QDoubleSpinBox()
        self.product_image_scale_spinbox.setToolTip("Choose a scaling factor for the parent image. Ideally, 42% is the right answer.")
        self.product_image_scale_spinbox.setValue(42)
        self.product_image_scale_spinbox.setRange(25,50)
        self.product_image_scale_spinbox.setSuffix("%")



        self.icon_positioning_label = QtGui.QLabel("Icon Positioning:")
        self.icon_positioning_combobox = QtGui.QComboBox()
        self.icon_positioning_combobox.setToolTip("Choose the way you want the icons positioned around the parent image.")
        self.icon_positions = ["Circular","Rectangular"]
        self.icon_positioning_combobox.addItems(self.icon_positions)
        self.palette_selection_label = QtGui.QLabel("Icon Palette:")
        self.palette_selection_combobox = QtGui.QComboBox()
        self.palette_selection_combobox.setToolTip("Choose one colour and the program picks a palette that will suit that color.\nHowever, manual QC is required for the generated images, as the program\ndoesn't yet look at the parent or background image color,\nso if the same color is picked, the image will look messy.")
        self.palettes_list = ["Black","Based on Input Color","From Input File"]
        self.palette_selection_combobox.addItems(self.palettes_list)
        self.palette_selection_button = QColorButton()
        palette_options = QtGui.QHBoxLayout()
        palette_options.addWidget(self.palette_selection_combobox,1)
        palette_options.addWidget(self.palette_selection_button,0)

        self.background_selection_label = QtGui.QLabel("Background Image:")
        self.background_selection_combobox = QtGui.QComboBox()
        self.background_selection_combobox.setToolTip("Choose a background to use for all the FSNs.\nYou may also pick the random option to provide variety.\nIf you need to add more backgrounds to this list, just add them to the Images\\Backgrounds folder.\nEnsure that the first word of the image is Background, with an uppercase B.\nFormat doesn't matter. Please use images of 9:16 aspect ratio.\nYes, portrait mode only.")
        self.background_selection_combobox.setMaximumWidth(200)
        self.backgrounds = glob.glob(os.path.join(os.path.join(os.path.join(os.getcwd(),"Images"),"Backgrounds"),"Background*.*")) + ["Random"]
        self.background_selection_combobox.addItems(self.backgrounds)
        self.background_preview_space.setStyleSheet("QLabel {background-color: grey; border: 1px solid black;}")
        self.background_preview_space.setToolTip("Preview of the selected background image.")
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
        self.icon_bounding_box_label = QtGui.QLabel("Icon Bounding Box Shape:")
        self.icon_bounding_box_combobox = QtGui.QComboBox()
        self.icon_bounding_box_combobox.addItems(["None","Circle","Rectangle","Square"])
        self.use_simple_color_replacement = QtGui.QCheckBox("Use a Simple Colour Extraction Method to remove Parent Image Background.")
        self.use_simple_color_replacement.setToolTip("If selected, the code just finds the likely background color and removes it from the entire message.\nThis method saves a large amount of runtime.\nThis is a risky method if the product image has similar colors, or if the image quality is dodgy.\nExercise with caution.")
        self.background_color_threshold_label = QtGui.QLabel("Threshold for Background Color Extraction:")
        self.background_color_threshold_spinbox = QtGui.QSpinBox()
        self.background_color_threshold_spinbox.setPrefix(u"\u00B1")
        self.background_color_threshold_spinbox.setRange(0,255)
        self.background_color_threshold_spinbox.setValue(20)
        self.background_color_threshold_spinbox.setToolTip("Choose a threshold for the background color elimination algorithm.\n Note that setting a very high threshold will remove most of the colours from the image.\nExercise with caution.\nA value around 10-30 is recommended. 20 has been found to be optimum.")
        self.validate_button  = IconButton(os.path.join("essentials","validate.png"))

        self.validate_button.setToolTip("Validate and Proceed")
        self.allow_overlap_checkbox = QtGui.QCheckBox("Allow Icons to Overlap the Parent Image")
        self.allow_overlap_checkbox.setToolTip("This allows the icons to be placed over the parent image.\nIcons themselves will never overlap.\nUse with caution, as icon placement becomes messy when enabled.\nThis is best used for small batches.")
        settings_layout = QtGui.QGridLayout()
        settings_layout.addWidget(self.use_random_parent_image_position,0,0,1,2,QtCore.Qt.AlignLeft)
        settings_layout.addWidget(self.use_simple_color_replacement,1,0,1,2,QtCore.Qt.AlignLeft)
        settings_layout.addWidget(self.background_color_threshold_label,2,0,1,1,QtCore.Qt.AlignLeft)
        settings_layout.addWidget(self.background_color_threshold_spinbox,2,1,1,1,QtCore.Qt.AlignLeft)
        settings_layout.addWidget(self.image_margin_label, 3, 0, 1, 1, QtCore.Qt.AlignLeft)
        settings_layout.addWidget(self.image_margin_spinbox, 3, 1, 1, 1, QtCore.Qt.AlignLeft)
        settings_layout.addWidget(self.font_color_label, 4, 0, 1, 1, QtCore.Qt.AlignLeft)
        settings_layout.addWidget(self.font_color_picker, 4, 1, 1, 1, QtCore.Qt.AlignLeft)
        settings_layout.addWidget(self.font_color_picker_checkbox, 4, 2, 1, 1, QtCore.Qt.AlignLeft)
        settings_layout.addWidget(self.product_image_scale_label, 5, 0, 1, 1, QtCore.Qt.AlignLeft)
        settings_layout.addWidget(self.product_image_scale_spinbox, 5, 1, 1, 1, QtCore.Qt.AlignLeft)
        settings_layout.addWidget(self.icon_positioning_label,6,0,1,1,QtCore.Qt.AlignLeft)
        settings_layout.addWidget(self.icon_positioning_combobox,6,1,1,1,QtCore.Qt.AlignLeft)
        settings_layout.addWidget(self.allow_overlap_checkbox,7,0,1,2,QtCore.Qt.AlignLeft)
        settings_layout.addWidget(self.icon_bounding_box_label,8,0,1,1,QtCore.Qt.AlignLeft)
        settings_layout.addWidget(self.icon_bounding_box_combobox,8,1,1,1,QtCore.Qt.AlignLeft)
        settings_layout.addWidget(self.palette_selection_label,9,0,1,1,QtCore.Qt.AlignLeft)
        settings_layout.addLayout(palette_options,9,1,1,1,QtCore.Qt.AlignLeft)
        settings_layout.addWidget(self.background_selection_label,10,0,1,1,QtCore.Qt.AlignLeft)
        settings_layout.addWidget(self.background_selection_combobox,10,1,1,1,QtCore.Qt.AlignLeft)
        settings_layout.addWidget(self.primary_attr_icon_size_label,11,0,1,1,QtCore.Qt.AlignLeft)
        settings_layout.addWidget(self.primary_attr_icon_size_spin_box,11,1,1,1,QtCore.Qt.AlignLeft)
        settings_layout.addWidget(self.secondary_attr_icon_size_label,12,0,1,1,QtCore.Qt.AlignLeft)
        settings_layout.addWidget(self.secondary_attr_icon_size_spin_box,12,1,1,1,QtCore.Qt.AlignLeft)
        self.settings_group_box = QtGui.QGroupBox("Settings")
        self.settings_group_box.setLayout(settings_layout)
        self.preview_widget = QtGui.QWidget()
        self.preview_group_box = QtGui.QGroupBox("Icon Positioning and Preview")
        preview_layout = QtGui.QHBoxLayout()
        preview_layout.addWidget(self.parent_image_position_selector,0)
        preview_layout.addWidget(self.preview_widget,0)
        self.preview_group_box.setLayout(preview_layout)
        group_boxes_layout = QtGui.QGridLayout()
        group_boxes_layout.addWidget(self.settings_group_box, 0, 0, 10, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        group_boxes_layout.addWidget(self.preview_group_box, 0, 1, 10, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        group_boxes_layout.addWidget(self.validate_button, 10, 2, QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        group_boxes_layout.addWidget(self.validate_button, 13, 6, 1, 2, QtCore.Qt.AlignRight)
        self.group_box = QtGui.QGroupBox("Design")
        self.group_box.setLayout(group_boxes_layout)
        final_layout = QtGui.QHBoxLayout()
        final_layout.addWidget(self.group_box)
        self.setLayout(final_layout)
        self.changeBackground()

    def mapEvents(self):
        self.background_selection_combobox.currentIndexChanged.connect(self.changeBackground)
        self.use_random_parent_image_position.stateChanged.connect(self.toggleRandomParentPosition)
        self.primary_attr_icon_size_spin_box.valueChanged.connect(self.limitSecondaryIconSize)

    def limitSecondaryIconSize(self,maximum_primary_value):
        self.secondary_attr_icon_size_spin_box.setMaximum(maximum_primary_value)
   
    def toggleRandomParentPosition(self):
        if self.use_random_parent_image_position.isChecked():
            self.parent_image_position_selector.setEnabled(False)
        else:
            self.parent_image_position_selector.setEnabled(True)

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
        return str(self.icon_positioning_combobox.currentText())
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

            