import sys
import os
from PyQt4 import QtGui, QtCore
from PIL import Image, ImageFilter
import numpy as np

from ProgressBar import ProgressBar

class MonaLisa(QtGui.QPushButton):
    gotStart = QtCore.pyqtSignal(list)
    gotEnd = QtCore.pyqtSignal(list)
    def __init__(self, *args, **kwargs):
        super(MonaLisa, self).__init__(*args, **kwargs)
        self.start_point = QtCore.QPoint(0,0)
        self.end_point = QtCore.QPoint(0,0)
        self.createUI()

    def mousePressEvent(self, QMouseEvent):
        #print "Captured!"
        self.start_point = QMouseEvent.pos()
        self.gotStart.emit([self.start_point.x(), self.start_point.y()])

    def mouseReleaseEvent(self, QMouseEvent):
        #print "Captured!"
        cursor = QtGui.QCursor()
        self.end_point = QMouseEvent.pos()
        self.gotEnd.emit([self.end_point.x(), self.end_point.y()])

    def createUI(self):               
        self.base_size = 350
        self.setFixedSize(self.base_size, self.base_size)
        self.setWindowTitle('MonaLisa')
#        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        #self.clicked.connect(self.test)
        self.show()
        self.setStyleSheet("QPushButton{border: 2px solid black; color: red;}")

    def getCoords(self):
      return [self.start_point.x(), self.start_point.y()], [self.end_point.x(),self.end_point.y()]
    
    def setImage(self, image_path):
        type = os.path.splitext(os.path.basename(str(image_path)))[1].upper()
        image_pixmap = QtGui.QPixmap(image_path, type)
        icon = QtGui.QIcon(image_pixmap)
        self.setIcon(icon)
        #print image_pixmap.rect().size()
        pixmap_size = image_pixmap.rect().size()
        self.setIconSize(pixmap_size)
        icon_size = QtCore.QSize(100, 100) if ((pixmap_size.width() < 100) or (pixmap_size.height() < 100)) else image_pixmap.rect().size()

        self.setFixedSize(icon_size)

    def zoomInOut(self, zoom_level):
        self.zoom_factor = zoom_level

class Donatello(QtGui.QWidget):
    def __init__(self):
        super(Donatello, self).__init__()
        self.current_file = None
        self.createUI()

    def createUI(self):
        self.load_button = QtGui.QPushButton("Load")
        self.revert_button = QtGui.QPushButton("Revert")
        self.clean_button = QtGui.QPushButton("Clean")
        self.save_button = QtGui.QPushButton("Save")
        self.clean_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.revert_button.setEnabled(False)    
        
        self.file_name_label = QtGui.QLabel("File:")
        self.file_name_line_edit = QtGui.QLineEdit()
        self.file_name_line_edit.setReadOnly(True)

        
        self.start_label = QtGui.QLabel("Starting Coordinates:")
        self.start_x = QtGui.QSpinBox()
        self.start_y = QtGui.QSpinBox()

        self.end_label = QtGui.QLabel("Ending Coordinates:")
        self.end_x = QtGui.QSpinBox()
        self.end_y = QtGui.QSpinBox()

        self.strip_type_label = QtGui.QLabel("Algorithm:")
        self.strip_type_combo_box = QtGui.QComboBox()
        self.strip_type_combo_box.addItems(["Simple","Row and Column Movement","Canny's Edge Detection"])
        self.strip_threshold_label = QtGui.QLabel("Threshold")
        self.strip_threshold_spinbox = QtGui.QSpinBox()
        self.strip_threshold_spinbox.setPrefix(u"\u00B1")
        self.strip_threshold_spinbox.setRange(0, 255)
        self.slider_label = QtGui.QLabel("Zoom:")
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(0,250)
        self.slider.setSingleStep(1)
        self.slider.setValue(100)
        self.slider_value_label = QtGui.QLabel("%d%%"%self.slider.value())
        self.slider.valueChanged.connect(self.zoomInOut)
        self.slider.setTickInterval(10)
        self.slider.setTickPosition(2)


        self.clearance_label = QtGui.QLabel("Pixel Clearance:")
        self.clearance = QtGui.QSpinBox()
        self.clearance.setRange(0,10000)

        settings = QtGui.QHBoxLayout()
        settings.addWidget(self.strip_type_label,0)
        settings.addWidget(self.strip_type_combo_box,0)
        settings.addWidget(self.strip_threshold_label,0)
        settings.addWidget(self.strip_threshold_spinbox,0)
        settings.addWidget(self.clearance_label,0)
        settings.addWidget(self.clearance,0)
        
        settings.addWidget(self.slider_label, 0)
        settings.addWidget(self.slider, 5)
        settings.addWidget(self.slider_value_label, 0)

        limit = 100000

        self.start_x.setRange(-limit, limit)
        self.start_y.setRange(-limit, limit)
        
        self.end_x.setRange(-limit, limit)
        self.end_y.setRange(-limit, limit)

        self.mona = MonaLisa()
        scrollable_widget = QtGui.QScrollArea()
        scrollable_widget.setWidget(self.mona)
        scrollable_widget.setWidgetResizable(True)
        scrollable_widget.setMinimumHeight(400)
        scrollable_widget.setMinimumWidth(400)
        #scrollable_widget.setFixedWidth(800)

        self.progress_bar = ProgressBar()
        self.status = QtGui.QLabel("Cowabunga!")
        self.chosen_color = QtGui.QPushButton()
        self.chosen_color.setEnabled(False)
        self.chosen_color.setFixedSize(15,15)
        self.chosen_color.setToolTip("Color at the chosen pixel")

        status_bar = QtGui.QHBoxLayout()
        status_bar.addWidget(self.status,10)
        status_bar.addWidget(self.chosen_color)

        buttons = QtGui.QHBoxLayout()
        buttons.addWidget(self.load_button)
        buttons.addWidget(self.revert_button)
        buttons.addWidget(self.clean_button)
        buttons.addWidget(self.save_button)
        
        file_name = QtGui.QHBoxLayout()
        file_name.addWidget(self.file_name_label,0)
        file_name.addWidget(self.file_name_line_edit,1)
        
        coords = QtGui.QHBoxLayout()
        coords.addWidget(self.start_label)
        coords.addWidget(self.start_x)
        coords.addWidget(self.start_y)
        coords.addWidget(self.end_label)
        coords.addWidget(self.end_x)
        coords.addWidget(self.end_y)
        
        layout = QtGui.QVBoxLayout()
        layout.addLayout(buttons,0)
        layout.addLayout(file_name,0)
        layout.addLayout(coords,0)
        layout.addLayout(settings, 0)
        layout.addWidget(scrollable_widget,2)
        layout.addWidget(self.progress_bar,0)
        layout.addLayout(status_bar,0)

        self.setLayout(layout)

        self.revert_button.clicked.connect(self.revertImage)
        self.load_button.clicked.connect(self.loadImage)
        self.clean_button.clicked.connect(self.cleanImage)

        self.mona.gotStart.connect(self.captureStart)
        self.mona.gotEnd.connect(self.captureEnd)
        
        self.setWindowTitle("Donatello")
        self.move(500,70)
        self.show()
    
    def captureStart(self, coords):
        self.start_x.setValue(coords[0])
        self.start_y.setValue(coords[1])

    def captureEnd(self, coords):
        self.end_x.setValue(coords[0])
        self.end_y.setValue(coords[1])

    def revertImage(self):
        print "Reverting to original."

    def loadImage(self):
        open_path = os.getcwd() if self.current_file is None else os.path.dirname(self.current_file)
        open_file_name = QtGui.QFileDialog.getOpenFileName(self, "Load an Image",
                                                        open_path, ("Image files (*.jpeg *.jpg *.png)")
                                                        )
        if open_file_name is not None:
            self.file_name_line_edit.setText(os.path.splitext(os.path.basename(str(open_file_name)))[0])
            self.mona.setImage(open_file_name)
            self.current_file = str(open_file_name)
            self.clean_button.setEnabled(True)
        else:
            self.clean_button.setEnabled(False)
            self.save_button.setEnabled(False)

    def zoomInOut(self):

        self.slider_value_label.setText("%d%%"%int(self.slider.value()))
        self.mona.zoomInOut(int(self.slider.value()))

    def cleanImage(self):
        start, end = self.mona.getCoords()
        image_path = self.current_file
        threshold = self.strip_threshold_spinbox.value()
        clearance_pixels = self.clearance.value()
        self.cleanImageRectangle(image_path, start, end, threshold, clearance_pixels)

    def cleanImageRectangle(self, image_path, start, end, threshold, clearance_pixels):
        image_object = Image.open(image_path).convert("RGBA")
        start_x, start_y = start
        end_x, end_y = end
        image_array = np.array(image_object)
        #print image_object.size, image_array.shape
        
        #Remember: x is columns, y is rows in an array.
        chosen_color = image_array[start_y][start_x]

        #print "Received a request for cleaning %s in an image between "%chosen_color, start, end
        r, g, b, a = chosen_color
        min_r = r-threshold
        max_r = r+threshold

        min_g = g-threshold
        max_g = g+threshold
        
        min_b = b-threshold
        max_b = b+threshold

        self.chosen_color.setStyleSheet("background-color: rgb(%d,%d,%d);"%(r,g,b))
        #print chosen_color
        clean_down = True
        #Along one row, proceed forward in the column
        min_row = min(start_y,end_y)
        min_col = min(start_x, end_x)
        max_row = max(start_y, end_y)
        max_col = max(start_x, end_x)
        rows, columns, rgba = image_array.shape
        if max_row >= rows:
            max_row = rows-1
        if max_col >= columns:
            max_col = columns-1 
        current_row = min_row 
        while current_row <= (max_row+clearance_pixels):
            current_col = min_col
            while current_col <= (max_col+clearance_pixels):
                current_r, current_g, current_b, current_a = image_array[current_row][current_col]
                if min_r <= current_r <= max_r:
                    if min_g <= current_g <= max_g:
                        if min_b <= current_b <= max_b:
                            image_array[current_row][current_col] = [0,0,0,0]
                current_col +=1
            current_row += 1
        print "*"*10
        print start, end

        print max_row, max_col
        print current_row, current_col
        print "*"*10
        new_image = Image.fromarray(image_array, mode="RGBA")
        new_image.save("test.png")
        os.startfile("test.png","open")

        #while clean_down:



def main():
    app = QtGui.QApplication([])
    test = Donatello()
    sys.exit(app.exec_())
    print "What?"


if __name__ == '__main__':
    main()