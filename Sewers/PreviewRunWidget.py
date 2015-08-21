import os
from PyQt4 import QtGui, QtCore
from ImageViewerWidget import ImageViewerWidget
from ProgressBar import ProgressBar

class PreviewRunWidget(QtGui.QGroupBox):
    def __init__(self,title):
        super(PreviewRunWidget, self).__init__()
        self.setTitle(title)
        self.createUI()
    
    def createUI(self):
        self.process_one_button = QtGui.QPushButton("Process Random FSN\nfrom Queue")
    	self.start_progress_button = QtGui.QPushButton("Start Processing All!")
        self.start_progress_button.setFixedSize(200,50)
        buttons_stylesheet = """QPushButton{background-color: #66CD00; color: white}; QPushButton::hover{background-color:#cccce5; color: black}"""
        self.start_progress_button.setStyleSheet(buttons_stylesheet)

    	self.image_viewer_widget = ImageViewerWidget()
    	self.progress_bar = ProgressBar()
    	self.live_progress = QtGui.QWidget()
        self.status_message = QtGui.QLabel("The Cake is a Lie.")
        buttons_layout = QtGui.QHBoxLayout()
        buttons_layout.addWidget(self.process_one_button,0, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        buttons_layout.addWidget(self.start_progress_button,0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
    	live_progress_layout = QtGui.QVBoxLayout()
    	live_progress_layout.addLayout(buttons_layout, 0)
    	live_progress_layout.addWidget(self.image_viewer_widget,2,QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        live_progress_layout.addSpacing(10)
    	live_progress_layout.addWidget(self.progress_bar,0)
        live_progress_layout.addWidget(self.status_message,0,QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
    	self.live_progress.setLayout(live_progress_layout)
    	self.tabs = QtGui.QTabWidget()
    	self.tabs.addTab(self.live_progress,"Live Progress")
    	
    	self.log = QtGui.QTextEdit()
    	
    	self.tabs.addTab(self.log,"Log")
    	
    	layout = QtGui.QHBoxLayout()
    	layout.addWidget(self.tabs)
    	self.setLayout(layout)

    	self.show()

    def displayProgress(self,status, progress_value, eta, completion_status, images_list):
        """This gets the data from the Splinter Thread."""
        self.image_viewer_widget.setImages(images_list)
        self.image_viewer_widget.moveRight()
        if not completion_status:
            self.progress_bar.setValue(progress_value)
            self.status_message.setText("%s ETA: %s."%(status,eta.strftime("%H:%M:%S")))
        else:
            self.progress_bar.setValue(100)
            self.status_message.setText("Remember, remember, the 5th of November.")





        
        