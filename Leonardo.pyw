import os, sys, math
from PyQt4 import QtGui, QtCore
from LeonardoModules import LeonardoMethods
from LeonardoModules.Splinter import Splinter
from LeonardoModules.LeonardoToolbox import LeonardoToolbox
from LeonardoModules.LeonardoImagePreview import LeonardoImagePreview
from LeonardoModules.ShellShocked import showSplashScreen, setWindowTheme

class Leonardo(QtGui.QMainWindow):
    def __init__(self):
        super(Leonardo, self).__init__()
        self.createUI()
        self.mapEvents()

    def createUI(self):
        self.tool_box = LeonardoToolbox()
        self.image_viewer = LeonardoImagePreview()
        self.progress_bar = 
        final_layout = QtGui.QGridLayout()
        final_layout.addWidget(self.tool_box,0,0,1,7)
        final_layout.addWidget(self.image_viewer,0,2,7,5)
        final_layout.addWidget(self.progress_bar,7,0,5,1)
        main_widget = QtGui.QWidget()
        main_widget.setLayout(final_layout)
        self.setCentralWidget(main_widget)
        self.setWindowTitle("Leonardo: The Valorous Informational Creator of Images")
        self.setWindowIcon(QtGui.QIcon(os.path.join("essentials","oink.png")))
        

    def mapEvents(self):
        pass


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    setWindowTheme()
    splash = showSplashScreen()
    leo = Leonardo()
    QtGui.QApplication.processEvents()
    splash.finish(leo)
    sys.exit(app.exec_())