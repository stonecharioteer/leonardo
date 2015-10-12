from __future__ import division
import os
from PyQt4 import QtGui, QtCore


class ImageLabel(QtGui.QLabel):
    def __init__(self, image_path, height=None, width=None):
        super(ImageLabel, self).__init__()
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
        self.setPixmap(image_pixmap)
        self.setFixedSize(image_pixmap.rect().size())