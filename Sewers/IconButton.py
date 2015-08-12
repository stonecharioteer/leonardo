import os
from PyQt4.QtGui import QPushButton, QPixmap, QIcon
from PyQt4.QtCore import QSize

class IconButton(QPushButton):
    def __init__(self,icon_path=None,*args,**kwargs):
        super(IconButton,self).__init__(*args,**kwargs)
        icon_pixmap = QPixmap(icon_path)
        icon = QIcon(icon_pixmap)
        self.setIcon(icon)
        icon_size = icon_pixmap.rect().size()
        button_size = QSize(icon_size.width()*1.2,icon_size.height()*1.2)

        self.setIconSize(icon_size)
        self.setFixedSize(button_size)
        