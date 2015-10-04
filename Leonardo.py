"""
Leonardo is a tool that'll help Flipkart Content Artists in batch processing.
When complete, it'll be able to help them make the secondary iconic image for the App.
It's part of the artists' and SMEs' toolset.
"""
from __future__ import division
import os, sys, math, datetime

from PyQt4 import QtGui, QtCore
#Sewers is the folder containing all the modules.
from Sewers.Turtle import Turtle #Base QMainWindow class.
from Sewers.Splinter import Splinter #Thread for Leo to use. 
from Sewers.IconListBox import IconListBox
from Sewers.DataSelector import DataSelector
from Sewers.LayoutDesigner import LayoutDesigner
from Sewers.PreviewRunWidget import PreviewRunWidget
from Sewers.ShellShocked import showSplashScreen, setWindowTheme
from Sewers import Katana
#from Sewers.April import April
 
class Leonardo(Turtle):
    def __init__(self, repo_path):
        super(Leonardo, self).__init__()
        self.threads = 1
        self.repo_path = repo_path 
        self.createUI()
        self.radical_rats = [Splinter(i, self.repo_path) for i in range(self.threads)]
        self.mapEvents()

    def createUI(self):
        self.page_changer = IconListBox()
        page_control_list = [
                    {
                    "Name": "Data Set",
                    "Icon": os.path.join("essentials","data.png")
                    },
                    #{
                    #"Name": "Fine Tune",
                    #"Icon": os.path.join("essentials","marching.png")
                    #},
                    {
                    "Name": "Layout Design",
                    "Icon": os.path.join("essentials","layout.png")
                    },
                    {
                    "Name": "Preview & Run",
                    "Icon": os.path.join("essentials","run.png")
                    }
                ]
        self.page_changer.addElements(page_control_list)
        self.page_changer.setFixedSize(120, 120*len(page_control_list))

        self.page_changer.item(1).setFlags(QtCore.Qt.NoItemFlags)
        self.page_changer.item(2).setFlags(QtCore.Qt.NoItemFlags)
        #self.page_changer.item(3).setFlags(QtCore.Qt.NoItemFlags)

        #Initialize the individual widget pages
        self.data_selector_widget = DataSelector(self.repo_path)
        self.layout_designer_widget = LayoutDesigner(self.repo_path)
        self.preview_and_run_widget = PreviewRunWidget("Preview and Run",self.threads, self.repo_path)

        self.pages = QtGui.QStackedWidget()
        self.pages.addWidget(self.data_selector_widget)
        self.pages.addWidget(self.layout_designer_widget)
        self.pages.addWidget(self.preview_and_run_widget)
        final_layout = QtGui.QGridLayout()
        final_layout.addWidget(self.page_changer,0,0,5,1)
        final_layout.addWidget(self.pages,0,1,5,1)
        main_widget = QtGui.QWidget()
        main_widget.setLayout(final_layout)
        self.setCentralWidget(main_widget)
        self.setWindowTitle("Leonardo: The Valorous Informational Creator of Images")
        self.setWindowIcon(QtGui.QIcon(os.path.join("essentials","oink.png")))
        self.show()
        self.showMaximized()

    def changePage(self, current, previous):
        if not current:
            current = previous
        self.pages.setCurrentIndex(self.page_changer.row(current))

    def mapEvents(self):
        self.page_changer.currentItemChanged.connect(self.changePage)
        self.data_selector_widget.validate_button.clicked.connect(self.allowDesign)
        self.layout_designer_widget.validate_button.clicked.connect(self.showPreviewScreen)
        self.preview_and_run_widget.start_progress_button.clicked.connect(self.runSplinter)
        for i in range(self.threads):
            self.radical_rats[i].progress.connect(self.preview_and_run_widget.displayProgress)
            self.radical_rats[i].sendMessage.connect(self.preview_and_run_widget.displayActivity)

    def showPreviewScreen(self):
        #self.page_changer.item(0).setFlags(QtCore.Qt.NoItemFlags)
        #self.page_changer.item(1).setFlags(QtCore.Qt.NoItemFlags)
        self.page_changer.item(2).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.page_changer.setCurrentRow(2)

    
    def allowDesign(self):
        self.page_changer.item(1).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.page_changer.setCurrentRow(1)
        self.layout_designer_widget.setFSNs(self.data_selector_widget.data)
    
    def runSplinter(self):
        entry_count = len(self.data_selector_widget.data)
        step_size = int(math.ceil((entry_count/self.threads)))
        previous_step = 0
        for i in range(self.threads):
            current_step = previous_step + step_size
            if i != self.threads-1:
                if current_step < entry_count:
                    data = self.data_selector_widget.data[previous_step:current_step]
                else:
                    data = self.data_selector_widget.data[previous_step:]
            else:
                data = self.data_selector_widget.data[previous_step:]

            previous_step = current_step

            self.radical_rats[i].data = data
            self.radical_rats[i].parent_image_position = self.layout_designer_widget.getParentImageCoords()
            self.radical_rats[i].icon_positioning = self.layout_designer_widget.getIconPosition()
            self.radical_rats[i].icon_palette = self.layout_designer_widget.getIconPalette() #Enable this later.
            self.radical_rats[i].allow_overlap = self.layout_designer_widget.getOverlap()
            self.radical_rats[i].background_image_path = self.layout_designer_widget.getBackgroundImage()
            self.radical_rats[i].primary_attribute_relative_size = self.layout_designer_widget.getPrimaryAttrRelativeSize()
            self.radical_rats[i].secondary_attribute_relative_size = self.layout_designer_widget.getSecondaryAttrRelativeSize()
            self.radical_rats[i].bounding_box = self.layout_designer_widget.getIconBoundingBox()
            self.radical_rats[i].use_simple_bg_color_strip = self.layout_designer_widget.useSimpleColorStripAlgorithm()
            self.radical_rats[i].bg_color_strip_threshold = self.layout_designer_widget.getColorStripThreshold()
            self.radical_rats[i].parent_image_resize_reference = self.layout_designer_widget.getParentImageResizeReference()
            self.radical_rats[i].parent_image_resize_factor = self.layout_designer_widget.getParentImageResizeFactor()
            self.radical_rats[i].allow_textless_icons = self.layout_designer_widget.allowTextlessIcons()
            self.radical_rats[i].margin = self.layout_designer_widget.getMargin()
            self.radical_rats[i].use_category_specific_backgrounds = self.layout_designer_widget.useCategorySpecificBackgrounds()
            self.radical_rats[i].output_location = os.getcwd()
            self.radical_rats[i].colors_list = self.layout_designer_widget.getIconPalette()
            self.radical_rats[i].preserve_icon_colors = self.layout_designer_widget.preserveIconColors()
            self.radical_rats[i].fix_icon_text_case = self.layout_designer_widget.fixIconTextCase()
            self.radical_rats[i].font = self.layout_designer_widget.getFont()
            self.radical_rats[i].font_color = self.layout_designer_widget.getIconFontColor()
            self.radical_rats[i].use_icon_color_for_font_color = self.layout_designer_widget.useIconColorForFontColor()
            self.radical_rats[i].icon_font_size = self.layout_designer_widget.getIconFontSize()
            
            self.radical_rats[i].allow_run = True

    
    def sayCowabunga(self, message):
        print "Cowabunga! ", message

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    setWindowTheme()
    repository_exists = Katana.checkRepository()
    if not repository_exists:
        temp_widget = QtGui.QWidget()
        QtGui.QMessageBox.about(temp_widget, "Leonardo Images Repository Not Found", "Leonardo needs the folder with all the background images, icons, shapes and parent images to function properly. Without those, it won't launch. Please select one now.")
        
    while not repository_exists:
        repo_path = str(QtGui.QFileDialog.getExistingDirectory(
                                                    temp_widget, 
                                                    "Select the Leonardo Repository Folder.", 
                                                    os.getcwd(), 
                                                    QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks)
                                                )
        print repo_path
        if repo_path:
            Katana.recordRepository(repo_path)
            repository_exists = Katana.checkRepository()
            if not repository_exists:
                QtGui.QMessageBox.about(temp_widget, "Invalid Repository", "That repository folder is invalid. Ensure that the folder you select contains sub-folders for Backgrounds, Brands, Icons, Parent Images and Shapes.")
        else:
            print "Invalid?"
            break

    #If the repository exists, run the program.
    #If it doesn't, then ask for a repository.
    #If the user hits cancel, then quit.
    if repository_exists:
        repo_path = Katana.getRepoPath()
        print repo_path
        splash = showSplashScreen()
        leo = Leonardo(repo_path)
        QtGui.QApplication.processEvents()
        splash.finish(leo)
        sys.exit(app.exec_())

