from __future__ import division
import math
from PyQt4 import QtGui, QtCore

class PositionWidget(QtGui.QWidget):
    def __init__(self):
        super(PositionWidget, self).__init__()
        self.x_y_widgets = {}
        self.createUI()
        self.changedCoords = False

    def createUI(self):
        self.position_table = QtGui.QTableWidget()
        self.position_table.setRowCount(11)
        self.position_table.setColumnCount(3)
        label = "Parent"
        self.position_table.setItem(0, 0, QtGui.QTableWidgetItem(str(label)))
        x_parent = QtGui.QSpinBox()
        y_parent = QtGui.QSpinBox()
        self.x_y_widgets[label] = [x_parent, y_parent]
        self.position_table.setCellWidget(0, 1, x_parent)
        self.position_table.setCellWidget(0, 2, y_parent)
        
        for row in range(11)[1:]:
            label = "USP-%d"%row
            x = QtGui.QSpinBox()
            y = QtGui.QSpinBox()
            self.position_table.setItem(row, 0, QtGui.QTableWidgetItem(str(label)))
            self.position_table.setCellWidget(row, 1, x)
            self.position_table.setCellWidget(row, 2, y)
            self.x_y_widgets[label] = [x,y]

        self.position_table.setHorizontalHeaderLabels(["Feature","X","Y"])
        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.position_table)
        for label in self.x_y_widgets.keys():
            limit  = 100000
            self.x_y_widgets[label][0].setRange(-1*limit, limit)
            self.x_y_widgets[label][0].valueChanged.connect(self.changeCoords)
            self.x_y_widgets[label][1].setRange(-1*limit, limit)
            self.x_y_widgets[label][1].valueChanged.connect(self.changeCoords)
        self.setLayout(self.layout)

    def setCoords(self, coords):
        for label in coords.keys():
            self.x_y_widgets[label][0].setValue(coords[label][0])
            self.x_y_widgets[label][1].setValue(coords[label][1])

    def getCoords(self):
        if self.changed_coords:
            coords = {}
            for label in self.x_y_widgets.keys():
                coords[label] = [self.x_y_widgets[label][0].value, self.x_y_widgets[label][1].value]
            return coords
        else:
            return False
            
    def changeCoords(self):
        self.changed_coords = True