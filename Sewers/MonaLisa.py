import sys
import os
from ProgressBar import ProgressBar
from PyQt4 import QtGui, QtCore

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
        self.factor = 350
        self.setFixedSize(self.factor, self.factor)
        self.setWindowTitle('MonaLisa')
#        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        #self.clicked.connect(self.test)
        self.show()
        self.setStyleSheet("QPushButton{border: 2px solid black; color: red;}")

    def getPath(self):
      return [self.start_point.x(), self.start_point.y()], [self.end_point.x(),self.end_point.y()]
    
    def setImage(self, image_path):
        type = os.path.splitext(os.path.basename(str(image_path)))[1].upper()
        image_pixmap = QtGui.QPixmap(image_path, type)
        icon = QtGui.QIcon(image_pixmap)
        self.setIcon(icon)
        print image_pixmap.rect().size()
        pixmap_size = image_pixmap.rect().size()
        self.setIconSize(pixmap_size)
        icon_size = QtCore.QSize(100, 100) if ((pixmap_size.width() < 100) or (pixmap_size.height() < 100)) else image_pixmap.rect().size()

        self.setFixedSize(icon_size)

class Donatello(QtGui.QWidget):
    def __init__(self):
        super(Donatello, self).__init__()
        self.current_file = None

        self.load_button = QtGui.QPushButton("Load")
        self.revert_button = QtGui.QPushButton("Revert")
        self.clean_button = QtGui.QPushButton("Clean")
        self.save_button = QtGui.QPushButton("Save")
        
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

        settings = QtGui.QHBoxLayout()
        settings.addWidget(self.strip_type_label)
        settings.addWidget(self.strip_type_combo_box)
        settings.addWidget(self.strip_threshold_label)
        settings.addWidget(self.strip_threshold_spinbox)
        limit = 100000

        self.start_x.setRange(-limit, limit)
        self.start_y.setRange(-limit, limit)
        
        self.end_x.setRange(-limit, limit)
        self.end_y.setRange(-limit, limit)

        self.mona = MonaLisa()
        scrollable_widget = QtGui.QScrollArea()
        scrollable_widget.setWidget(self.mona)
        scrollable_widget.setWidgetResizable(True)
        scrollable_widget.setFixedHeight(400)
        scrollable_widget.setFixedWidth(800)



        self.progress_bar = ProgressBar()
        self.status = QtGui.QLabel("I Do Machines!")

        buttons = QtGui.QHBoxLayout()
        buttons.addWidget(self.load_button)
        buttons.addWidget(self.revert_button)
        buttons.addWidget(self.clean_button)
        buttons.addWidget(self.save_button)
        
        file_name = QtGui.QHBoxLayout()
        file_name.addWidget(self.file_name_label,0)
        file_name.addWidget(self.file_name_line_edit,1)
        start_coords = QtGui.QHBoxLayout()
        start_coords.addWidget(self.start_label)
        start_coords.addWidget(self.start_x)
        start_coords.addWidget(self.start_y)
        end_coords = QtGui.QHBoxLayout()
        end_coords.addWidget(self.end_label)
        end_coords.addWidget(self.end_x)
        end_coords.addWidget(self.end_y)
        
        layout = QtGui.QVBoxLayout()
        layout.addLayout(buttons,0)
        layout.addLayout(file_name,0)
        layout.addLayout(start_coords,1)
        layout.addLayout(end_coords,1)
        layout.addLayout(settings, 1)
        layout.addWidget(scrollable_widget,2, QtCore.Qt.AlignHCenter)
        layout.addWidget(self.progress_bar,0)
        layout.addWidget(self.status,0 )

        self.setLayout(layout)

        self.revert_button.clicked.connect(self.revertImage)
        self.load_button.clicked.connect(self.loadImage)
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
        open_file_name = QtGui.QFileDialog.getOpenFileName(self, "Load Settings from a JSON",
                                                        open_path, ("Image files (*.jpeg *.jpg *.png)")
                                                        )
        if open_file_name is not None:
            self.file_name_line_edit.setText(os.path.splitext(os.path.basename(str(open_file_name)))[0])
            self.mona.setImage(open_file_name)
            self.current_file = str(open_file_name)

def main():

    app = QtGui.QApplication([])
    test = Donatello()
    sys.exit(app.exec_())
    print "What?"


if __name__ == '__main__':
    main()