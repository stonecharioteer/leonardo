import PIL
from PyQt4 import QtGui, QtCore

class ImageViewerWidget(QtGui.QWidget):
    def __init__(self,*args,**kwargs):
        super(ImageViewerWidget,self).__init__(*args,**kwargs)
        self.current_index = 0
        self.images_list = []
        self.createUI()
        self.mapEvents()

    def createUI(self):
        self.left_button = QtGui.QPushButton("<")
        self.left_button.setFixedSize(50,50)
        self.left_empty = QtGui.QWidget()
        self.left = QtGui.QStackedWidget()
        self.left.addWidget(self.left_empty)
        self.left.addWidget(self.left_button)
        self.right_button = QtGui.QPushButton(">")
        self.right_button.setFixedSize(50,50)
        self.right_empty = QtGui.QWidget()
        self.right = QtGui.QStackedWidget()
        self.right.addWidget(self.right_button)
        self.right.addWidget(self.right_empty)
        self.image_holder = QtGui.QLabel()
        self.image_holder.setFixedSize(90*3,140*3)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.left,
                        0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(self.image_holder,
                        2, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(self.right,
                        0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.setLayout(layout)
    
    def setImages(self, images_list):
        if len(images_list) >= 0:
            self.images_list = images_list
            self.displayImage(self.current_index)

    def mapEvents(self):
        self.left_button.clicked.connect(self.moveLeft)
        self.right_button.clicked.connect(self.moveRight)

    def moveLeft(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.left.setCurrentIndex(1)
        if self.current_index == (len(self.images_list)-1):
            self.right.setCurrentIndex(1)
        elif self.current_index < (len(self.images_list)-1):
            self.right.setCurrentIndex(0)
        self.displayImage(self.current_index)
        if self.current_index == 0:
            self.left.setCurrentIndex(0)

    def moveRight(self):
        if self.current_index < (len(self.images_list)-1):
            self.right.setCurrentIndex(0)
            self.current_index += 1

        if self.current_index == 0:
            self.left.setCurrentIndex(0)
        elif self.current_index > 0:
            self.left.setCurrentIndex(1)
        
        self.displayImage(self.current_index)
        
        if self.current_index == (len(self.images_list)-1):
            self.right.setCurrentIndex(1)

    def displayImage(self, image_index):
        if image_index <= len(self.images_list):
            image_path = self.images_list[image_index]
            image_pixmap = QtGui.QPixmap(image_path)
            image_pixmap = image_pixmap.scaled(self.image_holder.size(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
            self.image_holder.setPixmap(image_pixmap)
            self.image_holder.setStyleSheet("QLabel {background-color: grey; border: 1px solid black;}")




        