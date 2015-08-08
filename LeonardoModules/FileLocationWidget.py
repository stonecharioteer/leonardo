import os
from PyQt4.QtGui import QPushButton, QLabel, QLineEdit, QWidget, QHBoxLayout, QPixmap, QIcon
from PyQt4.QtCore import QSize, Qt

class FileLocationWidget(QWidget):
    def __init__(self,name):
        super(FileLocationWidget,self).__init__()
        self.label = QLabel(name)
        self.line_edit = QLineEdit()
        self.line_edit.setText(os.getcwd())
        self.line_edit.setReadOnly(True)
        self.browse_button = QPushButton()
        browse_icon_path = os.path.join("essentials","folder.png")
        browse_icon_pixmap = QPixmap(browse_icon_path)
        browse_icon = QIcon(browse_icon_pixmap)
        self.browse_button.setIcon(browse_icon)
        icon_size = browse_icon_pixmap.rect().size()
        button_size = QSize(icon_size.width(),icon_size.height())
        self.browse_button.setIconSize(icon_size)
        self.browse_button.setFixedSize(button_size)
        self.browse_button.setToolTip("Click this to change the location")

        layout = QGridLayout()
        layout.addWidget(self.label,0,0,1,1,Qt.AlignLeft)
        layout.addWidget(self.line_edit,0,1,2,1,Qt.AlignLeft)
        layout.addWidget(self.browse_button,0,3,1,1,Qt.AlignHCenter)

        self.setLayout(layout)