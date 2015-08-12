import os
from PyQt4.QtGui import QPushButton, QColorDialog, QIcon, QPixmap, QColor
from PyQt4.QtCore import pyqtSignal, Qt, QSize

class QColorButton(QPushButton):
    '''
    Custom Qt Widget to show a chosen color.

    Left-clicking the button shows the color-chooser, while
    right-clicking resets the color to None (no-color).    
    '''

    colorChanged = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(QColorButton, self).__init__(*args, **kwargs)
        self._color = None
        #self.setMaximumWidth(32)
        self.pressed.connect(self.onColorPicker)
        icon_path = os.path.join("essentials","eyedropper.png")
        icon_pixmap = QPixmap(icon_path)
        icon = QIcon(icon_pixmap)
        self.setIcon(icon)
        icon_size = icon_pixmap.rect().size()
        button_size = QSize(icon_size.width()*1.2,icon_size.height()*1.2)
        self.setIconSize(icon_size)
        self.setFixedSize(button_size)
        self.setToolTip("Left click to select a color.\nRight click to delete selected color information.")

    def setColor(self, color):
        if color != self._color:
            self._color = color
            self.colorChanged.emit()

        if self._color:
            self.setStyleSheet("QPushButton{background-color: %s;}" % self._color)
        else:
            self.setStyleSheet("")

    def color(self):
        return self._color

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
            self.setColor(None)

        return super(QColorButton, self).mousePressEvent(e)