import os
from PyQt4.QtGui import QPushButton, QPixmap, QIcon
from PyQt4.QtCore import QSize

class FileBrowserButton(QPushButton):
    def __init__(self,*args,**kwargs):
        super(FileBrowserButton,self).__init__(*args,**kwargs)
        file_browser_icon_path = os.path.join("essentials","csv_file.png")
        file_browser_icon_pixmap = QPixmap(file_browser_icon_path)
        file_browser_icon = QIcon(file_browser_icon_pixmap)
        self.setIcon(file_browser_icon)
        icon_size = file_browser_icon_pixmap.rect().size()
        button_size = QSize(icon_size.width()*1.2,icon_size.height()*1.2)

        self.setIconSize(file_browser_icon_pixmap.rect().size())
        self.setFixedSize(button_size)
        self.setToolTip("Select Input CSV Data Set.")
        