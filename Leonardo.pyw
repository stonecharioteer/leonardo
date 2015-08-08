import os, sys, math

from PyQt4 import QtGui, QtCore

from LeonardoModules import LeonardoMethods
from LeonardoModules.Splinter import Splinter
from LeonardoModules.IconListBox import IconListBox
from LeonardoModules.DataSelector import DataSelector
from LeonardoModules.TemplateSelector import TemplateSelector
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
        self.template_selector_widget = TemplateSelector()
        self.settings_widget = SettingsWidget()
        self.preview_and_run_widget = PreviewRunWidget()

        self.pages = QtGui.QStackedWidget()
        self.pages.addWidget(self.data_selector_widget)
        self.pages.addWidget(self.template_selector_widget)
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
        self.data_selector_widget.validate_button.clicked.connect(self.getData)
        self.template_selector_widget.validate_button.clicked.connect(self.runSplinter)
    
    def getData(self):
        #print len(self.data_selector_widget.data)
        self.page_changer.item(1).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.page_changer.setCurrentRow(1)
    
    def runSplinter(self):
        self.hamato_yoshi.data = self.data_selector_widget.data
        self.hamato_yoshi.template = str(self.template_selector_widget.template_selection_combobox.currentText())
        self.hamato_yoshi.positioning = str(self.template_selector_widget.icon_positioning_combobox.currentText())
        self.hamato_yoshi.icon_palette = "Black" #Enable this later.
        self.hamato_yoshi.allow_overlap = False #Add a checkbox in the template_selector
        self.hamato_yoshi.background_image_path = str(self.template_selector_widget.background_selection_combobox.currentText())
        self.hamato_yoshi.primary_attribute_relative_size = 0.10
        self.hamato_yoshi.secondary_attribute_relative_size = 0.05
        self.hamato_yoshi.output_location = str(self.template_selector_widget.output_images_location_widget.line_edit.currentText())
        self.hamato_yoshi.allow_run = True


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    setWindowTheme()
    splash = showSplashScreen()
    leo = Leonardo()
    QtGui.QApplication.processEvents()
    splash.finish(leo)
    sys.exit(app.exec_())