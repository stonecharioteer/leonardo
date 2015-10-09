import os, glob, re
import datetime
from PyQt4 import QtGui, QtCore
from ImageButton import ImageButton
import Katana

class ImageButtonLine(QtGui.QWidget):
    def __init__(self, images_list):
        super(ImageButtonLine, self).__init__()
        self.images_list = images_list
        self.createUI()
        style = """
        QPushButton:checked{
                border: 1px solid black;
        }
        QPushButton:hoven{
                border: 1px solid red;
        }
        QPushButton{
                border: 0px solid black;
        }"""
        self.setStyleSheet(style)

    def createUI(self):
        if len(self.images_list) != 0:
            self.buttons = [ImageButton(image_path) for image_path in self.images_list]
            images_dimensions = [Katana.getImageDimensions(image_path) for image_path in self.images_list]
            self.labels = [QtGui.QLabel("(%d x %d)\n(%s)"%(width, height, os.path.basename(image_path))) for ((width, height), image_path) in zip(images_dimensions,self.images_list)]
            self.has_image = True
        else:
            self.has_image = False
            na_image = os.path.join("essentials","na_parent_image.png")
            self.buttons = [ImageButton(na_image)]
            width, height = Katana.getImageDimensions(na_image)
            self.labels = [QtGui.QLabel("(%d x %d)"%(width, height))]
        self.layout = QtGui.QHBoxLayout()
        self.logic_group = QtGui.QButtonGroup()
        self.logic_group.setExclusive(True)
        button_label_layouts = []
        for button, label in zip(self.buttons, self.labels):
            button.setCheckable(True)
            button_label_layouts.append(QtGui.QVBoxLayout())
            button_label_layouts[-1].addWidget(button, 1, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            button_label_layouts[-1].addWidget(label,0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
            self.layout.addLayout(button_label_layouts[-1])
            self.logic_group.addButton(button)

        self.layout.addStretch(10)
        self.buttons[0].setChecked(True)
        self.setLayout(self.layout)
    
    def getChosenParentImagePath(self):
        counter = 0
        if self.has_image:
            for button in self.buttons:
                if button.isChecked():
                    index = counter
                counter += 1
            image = self.images_list[index]
        else:
            image = os.path.join("essentials","na_parent_image.png")
        return image
            



