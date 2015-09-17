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

        self.black_color = None
        self.white_color = None
        #self.setMaximumWidth(32)
        self.black_button = QPushButton()
        self.grey_1_button = QPushButton()
        self.grey_2_button = QPushButton()
        self.grey_3_button = QPushButton()
        self.white_button = QPushButton()
        self.current_black = (0,0,0)
        self.current_grey_1 = (55,55,55)
        self.current_grey_2 = (123,123,123)
        self.current_grey_3 = (200,200,200)
        self.current_white = (255,255,255)

        self.black_button.pressed.connect(self.onColorPicker("Black"))
        self.white_button.pressed.connect(self.onColorPicker("White"))

        icon_path = os.path.join("essentials","eyedropper.png")
        icon_pixmap = QPixmap(icon_path)
        icon = QIcon(icon_pixmap)
        
        icon_size = icon_pixmap.rect().size()
        button_size = QSize(icon_size.width()*1.2,icon_size.height()*1.2)
        
        self.black_button.setIcon(icon)
        self.white_button.setIcon(icon)
        self.black_button.setIconSize(icon_size)
        self.white_button.setIconSize(icon_size)

        self.black_button.setToolTip("Left click to select the icon border color.")
        self.white_button.setToolTip("Left click to select the icon background color.")


        layout = QHBoxLayout()
        self.buttons_list = [
                        self.black_button,
                        self.grey_1_button,
                        self.grey_2_button, 
                        self.grey_3_button, 
                        self.white_button
                    ]

        self.color_list = [
                    self.current_black, 
                    self.current_grey_1, 
                    self.current_grey_2, 
                    self.current_grey_3, 
                    self.current_white
                ]
        #Loop and set the colors and add to the layout.
        counter = 0
        for button in self.buttons_list:
            button.setFixedSize(button_size)
            layout.addWidget(button, 0)
            button_style_sheet = """QPushButton {
                                background-color: rgb(%d,%d,%d);
                            }"""%(
                                self.color_list[counter][0], 
                                self.color_list[counter][1], 
                                self.color_list[counter][2]
                                )
            button.setStyleSheet(button_style_sheet)
            counter += 1

        self.setMaximumHeight(button_size.height()*1.5)
        self.setLayout(layout)

    def setBorderColor(self, color):
        """Sets the black"""
        import PIL
        if color != self.black_color:
            self.black_color = color
            self.colorChanged.emit()
        self.current_black = PIL.ImageColor.getrgb(str(color))
        self.current_grey_1 = [int(0.8*(color)) for color in self.current_black]
        self.current_grey_2 = [int(0.5*(255-color)) for color in self.current_black]
        self.current_grey_3 = [int(0.8*(255-color)) for color in self.current_black]
        self.current_white = [int(1*(255-color)) for color in self.current_black]
        self.color_list = [self.current_black, self.current_grey_1, self.current_grey_2, self.current_grey_3, self.current_white]
        counter = 0

        for button in self.buttons_list:
            button.setStyleSheet("QPushButton{background-color: rgb(%d,%d,%d);}" % (self.color_list[counter][0],self.color_list[counter][1],self.color_list[counter][2]))
            counter+=1

    def setBackgroundColor(self, color):
        """Sets the white."""
        import PIL
        if self.white_color:
            self.white_button.setStyleSheet("QPushButton{background-color: %s;}" % self._color)
        else:
            self.white_button.setStyleSheet("")

    def color(self):
        return self._color

    def onColorPicker(self, button_name):
        '''
        Show color-picker dialog to select color.

        Qt will use the native dialog by default.

        '''
        dlg = QColorDialog(self)
        if button_name == "Black":
            if self.black_color:
                color_as_qcolor = QColor(self.black_color)
                dlg.setCurrentColor(color_as_qcolor)
            if dlg.exec_():
                self.setBorderColor(dlg.currentColor().name())
        elif button_name == "White":
            if self.white_color:
                color_as_qcolor = QColor(self.white_color)
                dlg.setCurrentColor(color_as_qcolor)
            if dlg.exec_():
                self.setBackgroundColor(dlg.currentColor().name())


    def mousePressEvent(self, e):
        pass
        #if e.button() == Qt.RightButton:
        #    self.setBackgroundColor(None)
        #return super(QColorButton, self).mousePressEvent(e)
    
    def getColors(self):
        self.color_list = [
                    self.current_black, 
                    self.current_grey_1, 
                    self.current_grey_2, 
                    self.current_grey_3, 
                    self.current_white
                ]
        return self.color_list

    def setColors(self, colors_list):
        counter = 0
        self.current_black = colors_list[0]
        self.current_grey_1 = colors_list[1]
        self.current_grey_2 = colors_list[2]
        self.current_white = colors_list[3]

        self.color_list = [self.current_black, self.current_grey_1, self.current_grey_2, self.current_white]
        counter = 0
        for button in self.buttons_list:
            button.setStyleSheet("QPushButton{background-color: rgb(%d,%d,%d);}" % (self.color_list[counter][0],self.color_list[counter][1],self.color_list[counter][2]))
            counter+=1