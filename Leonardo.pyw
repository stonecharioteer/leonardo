"""
Leonardo is a tool that'll help Flipkart Content Artists in batch processing.
When complete, it'll be able to help them make the secondary iconic image for the App.
It's part of the artists' and SMEs' toolset.
"""
import os, sys, math

from PyQt4 import QtGui, QtCore

from LeonardoModules import LeonardoMethods
from LeonardoModules.Splinter import Splinter
from LeonardoModules.IconListBox import IconListBox
from LeonardoModules.DataSelector import DataSelector
from LeonardoModules.LayoutDesigner import LayoutDesigner
from LeonardoModules.SettingsWidget import SettingsWidget
from LeonardoModules.PreviewRunWidget import PreviewRunWidget
from LeonardoModules.ShellShocked import showSplashScreen, setWindowTheme
from LeonardoModules.ProgressBar import ProgressBar
#from LeonardoModules.April import April

class Leonardo(QtGui.QMainWindow):
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
        #self.page_changer.item(2).setFlags(QtCore.Qt.NoItemFlags)
        #self.page_changer.item(3).setFlags(QtCore.Qt.NoItemFlags)

        #Initialize the individual widget pages
        self.data_selector_widget = DataSelector()
        self.layout_designer_widget = LayoutDesigner()
        self.settings_widget = SettingsWidget()
        self.preview_and_run_widget = PreviewRunWidget()

        self.pages = QtGui.QStackedWidget()
        self.pages.addWidget(self.data_selector_widget)
        self.pages.addWidget(self.layout_designer_widget)
        self.pages.addWidget(self.settings_widget)
        self.pages.addWidget(self.preview_and_run_widget)

        self.progress_bar = ProgressBar()

        final_layout = QtGui.QGridLayout()
        final_layout.addWidget(self.page_changer,0,0,5,1)
        final_layout.addWidget(self.pages,0,1,5,1)
        final_layout.addWidget(self.progress_bar,5,0,1,2)

        main_widget = QtGui.QWidget()
        main_widget.setLayout(final_layout)
        self.setCentralWidget(main_widget)
        self.setWindowTitle("Leonardo: The Valorous Informational Creator of Images")
        self.setWindowIcon(QtGui.QIcon(os.path.join("essentials","oink.png")))
        self.show()
        self.resize(400,600)
        self.move(250,100)

    def changePage(self, current, previous):
        if not current:
            current = previous
        self.pages.setCurrentIndex(self.page_changer.row(current))

    def mapEvents(self):
        self.page_changer.currentItemChanged.connect(self.changePage)
        self.data_selector_widget.validate_button.clicked.connect(self.allowDesign)
        self.layout_designer_widget.validate_button.clicked.connect(self.runSplinter)
    
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
        self.hamato_yoshi.output_location = os.getcwd()
        self.hamato_yoshi.allow_run = True


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    setWindowTheme()
    splash = showSplashScreen()
    leo = Leonardo()
    QtGui.QApplication.processEvents()
    splash.finish(leo)
    sys.exit(app.exec_())