from __future__ import division
import datetime
import os
import glob
import time
import math
import random

from PIL import Image
import PIL
from PyQt4 import QtCore
import Katana

class Splinter(QtCore.QThread):
    progress = QtCore.pyqtSignal(str, int, datetime.datetime, bool, list)
    sendMessage = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Splinter,self).__init__()
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()
        self.allow_run = False
        self.data = None
        self.parent_image_position = (0.5,0.5)
        self.icon_positioning = None
        self.icon_palette = "Black"
        self.allow_overlap = False
        self.background_image_path = None
        self.primary_attribute_relative_size = 0.10
        self.secondary_attribute_relative_size = 0.05
        self.use_simple_bg_color_strip = False
        self.bg_color_strip_threshold = 20
        self.parent_image_resize_reference = "Height"
        self.parent_image_resize_factor = 42
        self.allow_textless_icons = False
        self.margin = 0.05
        self.output_location = None

        if not self.isRunning():
            self.start(QtCore.QThread.LowPriority)

    def run(self):
        while True:
            if self.allow_run:
                total = len(self.data)
                self.sendMessage.emit("Started processing %d FSNs."%total)
                counter = 0
                start_time = datetime.datetime.now()
                images_list = []
                for row in self.data:
                    counter+=1
                    self.sendMessage.emit("Starting to process %d of %d FSNs."%(counter,total))
                    fsn = row["FSN"]
                    if "Brand" in row.keys():
                        brand = row["Brand"]
                    else:
                        print "No brand for %s (%s)."%(fsn,category)
                        brand = None
                    category = row["Category"]
                    primary_attribute_data = []
                    primary_attributes = []
                    secondary_attributes = []
                    for key in row.keys():
                        if "Primary USP" in key:
                            primary_attributes.append(key)
                        elif "Secondary USP" in key:
                            secondary_attributes.append(key)
                    self.sendMessage.emit("Seggregated primary and secondary attributes for %d of %d FSNs."%(counter,total))

                    primary_attributes_count = len(primary_attributes)/2
                    primary_attribute_data = [] 
                    #print primary_attributes_count
                    for i in range(int(primary_attributes_count)):
                        index = i+1
                        attribute_name = row["Primary USP-%d Attribute"%index].strip()
                        if len(attribute_name) != 0:
                            description_text = row["Primary USP-%d Description Text"%index].strip()
                            if (len(description_text) == 0):
                                if(not self.allow_textless_icons):
                                    description_text = attribute_name
                                else:
                                    description_text = " "
                            primary_attribute_data.append({"Attribute":attribute_name,"Description Text":description_text})
                    secondary_attributes_count = len(secondary_attributes)/2
                    secondary_attribute_data = [] 
                    #print secondary_attributes_count
                    for i in range(int(secondary_attributes_count)):
                        index = i+1
                        attribute_name = row["Secondary USP-%d Attribute"%index].strip()
                        if len(attribute_name) != 0:
                            description_text = row["Secondary USP-%d Description Text"%index].strip()
                            if (len(description_text) == 0):
                                if(not self.allow_textless_icons):
                                    description_text = attribute_name
                                else:
                                    description_text = " "
                            secondary_attribute_data.append({"Attribute":attribute_name,"Description Text":description_text})
                    self.sendMessage.emit("Preparing app image for %d of %d FSNs."%(counter,total))

                    image_name = self.prepareAppImage(
                                                fsn, brand, category, 
                                                primary_attribute_data, secondary_attribute_data, 
                                                self.parent_image_position, self.icon_positioning, 
                                                self.icon_palette, self.allow_overlap, 
                                                self.background_image_path, 
                                                self.primary_attribute_relative_size, 
                                                self.secondary_attribute_relative_size, 
                                                self.bounding_box, self.use_simple_bg_color_strip, 
                                                self.bg_color_strip_threshold, self.output_location
                                            )

                    eta = Katana.getETA(start_time, counter, total)
                    images_list.append(image_name)
                    if counter < total:
                        message = "Processing %d of %d FSNs." %(counter,total)
                        progress = int(counter/total*100)
                        completion_status = False
                    else:
                        message = "Completed."
                        progress = 100
                        completion_status = True
                    self.progress.emit(message, progress, eta, completion_status, images_list)
                    self.sendMessage.emit("Completed %d in %ss." %(counter, datetime.datetime.now() - start_time))
                self.allow_run = False

    def prepareAppImage(self, fsn, brand, category, primary_attribute_data, secondary_attribute_data, parent_image_positioning, icon_positioning, icon_palette, allow_overlap, background_image_path, primary_attribute_relative_size, secondary_attribute_relative_size, bounding_box, use_simple_bg_color_strip, bg_color_strip_threshold, output_location):
        """This method takes one fsn set, and prepares the app-image.
        ALGORITHM:
        1. If the background image is specified, 
            check if Background image exists.
            a. If it doesn't, throw an exception.
        2. Check if the parent image exists.
            a. If it doesn't, throw an exception.
        3. Using the Attribute values for the Primary and Secondary USPs, 
            look in the Images\Repository\Category folder for icons. 
            Check if they're available. If they're not, throw an exception.
        4. Check if the bounding box shape image is available.
            (a) If it's not, throw an exception.
        5. Create an Image instance using the background image. 
            If the background image is set to "Random", 
            then use a random background image from the 
            Images\Backgrounds folder.
        6. Add the parent image to the specified location. 
            Acceptable locations are (i,j) where i,j <= 2. 
            0, 1, 2 indicate position based on % of the background image. 
            If the parent_image_position value is "Random", 
            then pick one of these randomly.
        7. Calculate the size of the primary and secondary icons based 
            on the relative size factor variables.
        8. Calculate the area of the parent image, 
            and that of the entire image. Using this area, 
            as well as the icon_positioning variable as constraints 
            find locations which can be used for a primary icon.
        9. Place the first primary icon at a random coordinate. 
            Place the bounding box right over the icon and the 
            text below the bounding box. If the palette is non-black, 
            then generate the respective colors and use random 
            colors for the text and icons.
        10. Place subsequent icons at the other locations pulled 
            up by the formula.
        11. Next, calculate the available coordinates at which 
            to place the secondary icons.
        12. After getting the coordinates, place the secondary 
            icons at similar positions as well.
        """
        #Get the primary image path
        message = "Getting parent image for %s."%fsn
        self.sendMessage.emit(message)
        parent_image_path = Katana.getParentImage(fsn)
        #Get the background image.
        message = "Getting background image for %s."%fsn
        self.sendMessage.emit(message)
        background_image = Katana.getBackgroundImage(background_image_path)
        base_image = Katana.getBaseImage()
        #Get the primary and secondary attribute icons.
        message = "Getting primary attribute data image for %s."%fsn
        self.sendMessage.emit(message)
        primary_attributes_and_icons_data = Katana.getIcons(primary_attribute_data,category,primary_attribute_relative_size, base_image.size)
        message = "Getting secondary attribute data image for %s."%fsn
        self.sendMessage.emit(message)
        secondary_attributes_and_icons_data = Katana.getIcons(secondary_attribute_data,category,secondary_attribute_relative_size, base_image.size)
        #First resize the parent image.
        message = "Resizing parent image for %s."%fsn
        self.sendMessage.emit(message)
        original_parent_image = Image.open(parent_image_path).convert("RGBA")
        #resized_parent_image = Katana.getResizedImage(original_parent_image, self.parent_image_resize_factor, self.parent_image_resize_reference, base_image.size)
        #Check the resize reference for the smartfit option. Create use a local parent_image_resize_reference value to control this.
        if self.parent_image_resize_reference == "Smart Fit":
            parent_image_resize_reference = "Height" if original_parent_image.size[1]>original_parent_image.size[0] else "Width"
            if parent_image_resize_reference == "Width":
                parent_image_resize_factor = 1.5*self.parent_image_resize_factor
            else:
                parent_image_resize_factor = self.parent_image_resize_factor
        else:
            parent_image_resize_reference = self.parent_image_resize_reference
            parent_image_resize_factor = self.parent_image_resize_factor
            
        #print "Smart Fit resulted in %s selection."%parent_image_resize_reference
        resized_parent_image = Katana.getResizedImage(original_parent_image, parent_image_resize_factor, parent_image_resize_reference, base_image.size)
        #Use the selected background colour strip algorithm 
        #to strip the parent image of its colour.
        if use_simple_bg_color_strip:
            #Simple background strip just searches for white and removes it.
            #Later, this should be extended to remove any background color.
            message = "Stripping parent image background using simple strip algorithm for %s."%fsn
            self.sendMessage.emit(message)
            parent_image = Katana.replaceColorInImage(resized_parent_image, (255,255,255,255), (0,0,0,0), bg_color_strip_threshold)
        else:
            #The complex movement algorithm takes thing by strokes.
            #First, it identifies the background colour, reading the
            #four corner pixels and taking the median of that list.
            #Then, it swipes up, down, left and right, turning the alpha
            #channel to zero, quitting whenever it encounters an RGB value
            #that is below or above the threshold.
            message = "Stripping parent image background using movement algorithm for %s."%fsn
            self.sendMessage.emit(message)
            parent_image = Katana.getStrippedImage(resized_parent_image, bg_color_strip_threshold)
        #Based on the input control parameters, get the coordinates for the parent image.
        message = "Getting parent image coordinates corresponding to %s for %s."%(parent_image_positioning, fsn)
        self.sendMessage.emit(message)
        if parent_image_positioning == "Random":
            parent_image_positioning = Katana.getRandomParentImagePlacementPoints()
        parent_image_coords = Katana.getParentImageCoords(base_image.size,parent_image.size, parent_image_positioning)
        #print "*"*10
        #print "Parent image Coords: ", parent_image_coords
        #print "*"*10
        message = "Pasting the parent image for %s."%(fsn)
        self.sendMessage.emit(message)
        base_image.paste(parent_image, parent_image_coords, parent_image)
        counter = 0
        message = "Getting icons and coordinates for %s."%(fsn)
        self.sendMessage.emit(message)
        icons_and_coordinates = Katana.getIconsAndCoordinates(base_image, parent_image, parent_image_coords, primary_attributes_and_icons_data, secondary_attributes_and_icons_data, "Circular","Separate",parent_image_positioning)
        for icon in icons_and_coordinates:
            try:
                base_image.paste(icon["Icon"],icon["Position"],icon["Icon"])
                message = "Pasted icon on base image at %s for %s." %(icon["Position"],fsn)
                self.sendMessage.emit(message)
            except:
                if icon["Position"] is None:
                    message = "Icon position cannot be None for %s." %(fsn)                    
                else:
                    message = "Encountered a problem while pasting the icon on base image at %s for %s." %(icon["Position"],fsn)
                self.sendMessage.emit(message)
                raise
        #Paste the FK and Brand Icon
        fk_brand_icon = Katana.getMergedFlipkartBrandImage(brand)
        
        base_image.paste(
                    fk_brand_icon, 
                    (int(fk_brand_icon.size[0]*0.05), 
                    int(fk_brand_icon.size[1]*0.05)), 
                    fk_brand_icon
                )
        
        final_image = background_image.copy()
        margin = 1 - self.margin
        resized_dimensions = (
                            int(margin*base_image.size[0]),
                            int(margin*base_image.size[1])
                        )
        resized_base_image = base_image.resize(resized_dimensions,resample=PIL.Image.ANTIALIAS)
        base_image_x = (background_image.size[0]-resized_base_image.size[0])/2
        base_image_y = (background_image.size[1]-resized_base_image.size[1])/2
        base_image_coords = (
                        int(base_image_x), 
                        int(base_image_y)
                    )
        final_image.paste(resized_base_image,base_image_coords,resized_base_image)
        final_image = final_image.convert("RGB")
        image_path = os.path.join("Output",fsn+"_app_image.png")
        final_image.save(image_path,dpi=(300,300))
        return image_path


    def __del__(self):
        self.mutex.lock()
        self.condition.wakeOne()
        self.mutex.unlock()
        self.wait()