"""
Leonardo is a tool that'll help Flipkart Content Artists in batch processing.
When complete, it'll be able to help them make the secondary iconic image for the App.
It's part of the artists' and SMEs' toolset.
"""
import os, sys, math, datetime

from PyQt4 import QtGui, QtCore
#Sewers is the folder containing all the modules.
from Sewers.Turtle import Turtle
from Sewers.Splinter import Splinter #Thread for Leo to use. 
from Sewers.IconListBox import IconListBox
from Sewers.DataSelector import DataSelector
from Sewers.LayoutDesigner import LayoutDesigner
from Sewers.PreviewRunWidget import PreviewRunWidget
from Sewers.ShellShocked import showSplashScreen, setWindowTheme
#from Sewers.April import April
 
class Leonardo(Turtle):
    def __init__(self):
        super(Leonardo, self).__init__()
        self.createUI()
        self.hamato_yoshi = Splinter()
        self.mapEvents()

    def createUI(self):
        self.page_changer = IconListBox()
        page_control_list = [
                    {
                    "Name": "Data Set",
                    "Icon": os.path.join("essentials","data.png")
                    },
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
        self.page_changer.setFixedSize(120, 400)
        self.page_changer.item(1).setFlags(QtCore.Qt.NoItemFlags)
        self.page_changer.item(2).setFlags(QtCore.Qt.NoItemFlags)

        #Initialize the individual widget pages
        self.data_selector_widget = DataSelector()
        self.layout_designer_widget = LayoutDesigner()
        self.preview_and_run_widget = PreviewRunWidget("Preview and Run")

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
        self.hamato_yoshi.progress.connect(self.preview_and_run_widget.displayProgress)
        self.hamato_yoshi.sendMessage.connect(self.displayActivity)

    def displayActivity(self,message):
        full_message = message + " @" + datetime.datetime.now().strftime("[%a (%d-%m)] %H:%M:%S") 
        self.preview_and_run_widget.status_message.setText(full_message)

    def showPreviewScreen(self):
        #self.page_changer.item(0).setFlags(QtCore.Qt.NoItemFlags)
        #self.page_changer.item(1).setFlags(QtCore.Qt.NoItemFlags)
        self.page_changer.item(2).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.page_changer.setCurrentRow(2)

    
    def allowDesign(self):
        self.page_changer.item(1).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.page_changer.setCurrentRow(1)
    
    def runSplinter(self):
        self.hamato_yoshi.data = self.data_selector_widget.data
        self.hamato_yoshi.parent_image_position = self.layout_designer_widget.getParentImageCoords()
        self.hamato_yoshi.icon_positioning = self.layout_designer_widget.getIconPosition()
        self.hamato_yoshi.icon_palette = self.layout_designer_widget.getIconPalette() #Enable this later.
        self.hamato_yoshi.allow_overlap = self.layout_designer_widget.getOverlap()
        self.hamato_yoshi.background_image_path = self.layout_designer_widget.getBackgroundImage()
        self.hamato_yoshi.primary_attribute_relative_size = self.layout_designer_widget.getPrimaryAttrRelativeSize()
        self.hamato_yoshi.secondary_attribute_relative_size = self.layout_designer_widget.getSecondaryAttrRelativeSize()
        self.hamato_yoshi.bounding_box = self.layout_designer_widget.getIconBoundingBox()
        self.hamato_yoshi.use_simple_bg_color_strip = self.layout_designer_widget.useSimpleColorStripAlgorithm()
        self.hamato_yoshi.bg_color_strip_threshold = self.layout_designer_widget.getColorStripThreshold()
        self.hamato_yoshi.parent_image_resize_reference = self.layout_designer_widget.getParentImageResizeReference()
        self.hamato_yoshi.parent_image_resize_factor = self.layout_designer_widget.getParentImageResizeFactor()
        self.hamato_yoshi.allow_textless_icons = self.layout_designer_widget.allowTextlessIcons()
        self.hamato_yoshi.output_location = os.getcwd()
        self.hamato_yoshi.allow_run = True
    
    def sayCowabunga(self, message):
        print "Cowabunga! ", message

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    setWindowTheme()
    splash = showSplashScreen()
    leo = Leonardo()
    QtGui.QApplication.processEvents()
    splash.finish(leo)
    sys.exit(app.exec_())