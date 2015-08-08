import datetime
from PyQt4 import QtCore
import LeonardoMethods

class Splinter(QtCore.QThread):
    progress = QtCore.pyqtSignal(str, int, datetime.datetime, bool)
    def __init__(self):
        super(Splinter,self).__init__()
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()
        self.allow_run = False
        self.data = None
        self.template = "Parent to One Side"
        self.positioning = None
        self.icon_palette = "Black"
        self.allow_overlap = False
        self.background_image_path = None
        self.primary_attribute_relative_size = 0.10
        self.secondary_attribute_relative_size = 0.05
        self.output_location = None
        if not self.isRunning():
            self.start(QtCore.QThread.LowPriority)

    def run(self):
        while True:
            if self.allow_run:
                rows = len(self.data)
                for row in self.data:
                    fsn = row["FSN"]
                    category = row["Category"]
                    primary_attribute_data = []
                    primary_attributes = []
                    secondary_attributes = []
                    for key in row.keys():
                        if "Primary USP" in key:
                            primary_attributes.append(key)
                        elif "Secondary USP" in key:
                            secondary_attributes.append(key)
                    primary_attributes_count = len(primary_attributes)/2
                    primary_attribute_data = [] 
                    #print primary_attributes_count
                    for i in range(primary_attributes_count):
                        index = i+1
                        primary_attribute_data.append({"Attribute":row["Primary USP-%d Attribute"%index],"Description Text":row["Primary USP-%d Description Text"%index]})
                    secondary_attributes_count = len(secondary_attributes)/2
                    secondary_attribute_data = [] 
                    #print secondary_attributes_count
                    for i in range(secondary_attributes_count):
                        index = i+1
                        secondary_attribute_data.append({"Attribute":row["Secondary USP-%d Attribute"%index],"Description Text":row["Secondary USP-%d Description Text"%index]})
                    LeonardoMethods.prepareAppImage(fsn, category, primary_attribute_data, secondary_attribute_data, self.template, self.positioning, self.icon_palette, self.allow_overlap, self.background_image_path, self.primary_attribute_relative_size, self.secondary_attribute_relative_size, self.output_location)
                    
                self.allow_run = False
#                self.deploy()
    
    def deploy(self):
        print "Doing shit."


    def __del__(self):
        self.mutex.lock()
        self.condition.wakeOne()
        self.mutex.unlock()
        self.wait()