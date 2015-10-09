from __future__ import division
import os
from PyQt4 import QtGui, QtCore


class ImageButton(QtGui.QPushButton):
    def __init__(self, image_path, height=None, width=None):
        super(ImageButton, self).__init__()
        if height is None:
            height = 75
        if width is None:
            width = 75
        type = os.path.splitext(os.path.basename(str(image_path)))[1]
        image_pixmap = QtGui.QPixmap(image_path, type)
        image_pixmap = image_pixmap.scaled(
                                        QtCore.QSize(width, height),
                                        QtCore.Qt.KeepAspectRatio, 
                                        QtCore.Qt.SmoothTransformation)
        icon = QtGui.QIcon(image_pixmap)
        self.setIcon(icon)
        self.setIconSize(image_pixmap.rect().size())
        self.setFixedSize(image_pixmap.rect().size())
