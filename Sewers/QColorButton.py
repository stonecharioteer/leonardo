import os
from PyQt4.QtGui import QWidget, QHBoxLayout, QPushButton, QColorDialog, QIcon, QPixmap, QColor
from PyQt4.QtCore import pyqtSignal, Qt, QSize
import PIL

class QColorButton(QWidget):
    '''
    Custom Qt Widget to show a chosen color.

    Left-clicking the button shows the color-chooser, while
    right-clicking resets the color to None (no-color). 

    Original:
        #http://martinfitzpatrick.name/article/qcolorbutton-a-color-selector-tool-for-pyqt/
    Modified by adding Pillow based methods plus some UI improvements.
    '''
    colorChanged = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(QColorButton, self).__init__(*args, **kwargs)

        self.color_button = QPushButton()
        
        self._color = None
        self.color_as_rgba = [255,255,255]
        
        #self.setMaximumWidth(32)
        icon_path = os.path.join("essentials","eyedropper.png")
        icon_pixmap = QPixmap(icon_path)
        icon = QIcon(icon_pixmap)
        
        icon_size = icon_pixmap.rect().size()
        button_size = QSize(icon_size.width()*1.2,icon_size.height()*1.2)
        self.color_button.setFixedSize(button_size)
        self.color_button.setIcon(icon)
        self.color_button.pressed.connect(self.onColorPicker)
        layout = QHBoxLayout()
        layout.addWidget(self.color_button, 0)
        self.setMaximumHeight(button_size.height()*1.5)
        self.setLayout(layout)

    def setColor(self, color):
        if color != self._color:
            self._color = color
            self.colorChanged.emit()

        if self._color:
            self.color_button.setStyleSheet("background-color: %s;" % self._color)
        else:
            self.color_button.setStyleSheet("")

        self.color_as_rgba = PIL.ImageColor.getrgb(str(color))

    def color(self):
        return self._color

    def getColor(self):
        return self.color_as_rgba

    def onColorPicker(self):
        '''
        Show color-picker dialog to select color.

        Qt will use the native dialog by default.

        '''
        dlg = QColorDialog(self)
        if self._color:
            dlg.setCurrentColor(QColor(self._color))

        if dlg.exec_():
            self.setColor(dlg.currentColor().name())

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton:
            self.resetColor()
        return super(QColorButton, self).mousePressEvent(e)

    def resetColor(self):
        self.setColor(None)    
        self.color_as_rgba = [255,255,255]