import os
from PyQt4.QtGui import QPushButton, QPixmap, QIcon
from PyQt4.QtCore import QSize

class IconButton(QPushButton):
    def __init__(self,icon_path=None,*args,**kwargs):
        super(IconButton,self).__init__(*args,**kwargs)
        self.icon_path = icon_path
        self.icon_pixmap = QPixmap(icon_path)
        self.icon = QIcon(self.icon_pixmap)
        self.setIcon(self.icon)
        self.icon_size = self.icon_pixmap.rect().size()
        self.button_size = QSize(self.icon_size.width()*1.2,self.icon_size.height()*1.2)

        self.setIconSize(self.icon_size)
        self.setFixedSize(self.button_size)
    def setSize(self,width, height):
        self.setIconSize(QSize(width,height))
        self.setFixedSize(QSize(width*1.2,height*1.2))


        