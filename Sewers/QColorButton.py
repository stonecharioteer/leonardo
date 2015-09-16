import os
from PyQt4.QtGui import QWidget, QHBoxLayout, QPushButton, QColorDialog, QIcon, QPixmap, QColor
from PyQt4.QtCore import pyqtSignal, Qt, QSize
import PIL

class QColorButton(QWidget):
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
        self.black_button = QPushButton()
        self.current_black = (0,0,0)
        self.current_grey_1 = (55,55,55)
        self.current_grey_2 = (123,123,123)
        self.current_white = (255,255,255)
        self.black_button.pressed.connect(self.onColorPicker)
        icon_path = os.path.join("essentials","eyedropper.png")
        icon_pixmap = QPixmap(icon_path)
        icon = QIcon(icon_pixmap)
        self.black_button.setIcon(icon)
        icon_size = icon_pixmap.rect().size()
        button_size = QSize(icon_size.width()*1.2,icon_size.height()*1.2)
        
        self.black_button.setIconSize(icon_size)
        self.grey_1_button = QPushButton()
        self.grey_2_button = QPushButton()
        self.white_button = QPushButton()
        layout = QHBoxLayout()
        self.buttons_list = [self.black_button,self.grey_1_button, self.grey_2_button, self.white_button]
        self.color_list = [self.current_black, self.current_grey_1, self.current_grey_2, self.current_white]
        counter = 0
        for button in self.buttons_list:
            button.setFixedSize(button_size)
            layout.addWidget(button,0)
            button.setStyleSheet("QPushButton{background-color: rgb(%d,%d,%d);}" % (self.color_list[counter][0], self.color_list[counter][1], self.color_list[counter][2]))
            counter += 1

        #self.setFixedSize(button_size)
        self.black_button.setToolTip("Left click to select the base black color.")
        self.setMaximumHeight(button_size.height()*1.5)
        self.setLayout(layout)

    def setColor(self, color):
        import PIL
        if color != self._color:
            self._color = color
            self.colorChanged.emit()
        self.current_black = PIL.ImageColor.getrgb(str(color))
        self.current_grey_1 = [int(0.6*(255-color)) for color in self.current_black]
        self.current_grey_2 = [int(0.8*(255-color)) for color in self.current_black]
        self.current_white = [int(1*(255-color)) for color in self.current_black]
        self.color_list = [self.current_black, self.current_grey_1, self.current_grey_2, self.current_white]

        print "Changed colors:"
        for color in self.color_list:
            print color
        counter = 0
        for button in self.buttons_list:
            button.setStyleSheet("QPushButton{background-color: rgb(%d,%d,%d);}" % (self.color_list[counter][0],self.color_list[counter][1],self.color_list[counter][2]))
            counter+=1
        

        if self._color:
            self.black_button.setStyleSheet("QPushButton{background-color: %s;}" % self._color)
        else:
            self.black_button.setStyleSheet("")

    def color(self):
        return self._color

    def onColorPicker(self):
        '''
        Show color-picker dialog to select color.

        Qt will use the native dialog by default.

        '''
        dlg = QColorDialog(self)
        if self._color:
            color_as_qcolor = QColor(self._color)
            dlg.setCurrentColor(color_as_qcolor)
        if dlg.exec_():
            self.setColor(dlg.currentColor().name())


    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton:
            self.setColor(None)

        return super(QColorButton, self).mousePressEvent(e)