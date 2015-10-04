from __future__ import division
from multiprocessing import Manager, Process, Pool, Queue, Lock
import datetime
import os
import getpass
import glob
import time
import math
import random

from PIL import Image
import PIL
from PyQt4 import QtCore
import Katana

class Splinter(QtCore.QThread):
    progress = QtCore.pyqtSignal(str, int, datetime.datetime, bool, list, int)
    sendMessage = QtCore.pyqtSignal(str, datetime.datetime, int)

    def __init__(self, thread_index=None, repo_path=None):
        super(Splinter, self).__init__()
        if thread_index is None:
            self.thread_index = 0
        else:
            self.thread_index = thread_index
        self.repo_path = repo_path 

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
        self.preserve_icon_colors = False
        self.colors_list = [
                                (0,0,0),
                                (55,55,55),
                                (127,127,127),
                                (255,255,255)
                            ]
        self.fix_icon_text_case = False
        self.use_category_specific_backgrounds = True
        self.font = os.path.join("essentials", "RionaSans-Regular.ttf")
        self.font_color = [0,0,0]
        self.icon_font_size = 38
        self.use_icon_color_for_font_color = True
        self.bypass_parent_image_cleanup = False

        if not self.isRunning():
            self.start(QtCore.QThread.LowPriority)

    def run(self):
        while True:
            if self.allow_run:
                total = len(self.data)
                self.last_eta = datetime.datetime.now()
                self.sendMessage.emit("Started processing %d FSNs."%total, self.last_eta, self.thread_index)
                counter = 0
                start_time = datetime.datetime.now()
                images_list = []
                for row in self.data:
                    if not self.allow_run:
                        self.sendMessage.emit("Stopped...", datetime.datetime.now(), self.thread_index)
                    else:
                        fsn_start_time = datetime.datetime.now()
                        counter+=1
                        self.sendMessage.emit("Starting to process %d of %d FSNs."%(counter,total), self.last_eta, self.thread_index)
                        fsn = row["FSN"]
                        if "Brand" in row.keys():
                            brand = row["Brand"]
                        else:
                            #print "No brand for %s (%s)."%(fsn,category)
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
                        self.sendMessage.emit("Seggregated primary and secondary attributes for %d of %d FSNs."%(counter,total), self.last_eta, self.thread_index)

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
                        self.sendMessage.emit("Preparing app image for %d of %d FSNs."%(counter,total), self.last_eta, self.thread_index)

                        image_name = self.prepareAppImage(
                                                    fsn, brand, category, 
                                                    primary_attribute_data, secondary_attribute_data, 
                                                    self.parent_image_position, self.icon_positioning, 
                                                    self.icon_palette, self.allow_overlap, 
                                                    self.background_image_path, 
                                                    self.primary_attribute_relative_size, 
                                                    self.secondary_attribute_relative_size, 
                                                    self.bounding_box, self.use_simple_bg_color_strip, 
                                                    self.bg_color_strip_threshold, self.colors_list,
                                                    self.fix_icon_text_case, self.preserve_icon_colors, 
                                                    self.font, self.font_color, self.use_icon_color_for_font_color,
                                                    self.icon_font_size,
                                                    self.output_location
                                                )

                        self.eta = Katana.getETA(start_time, counter, total)
                        images_list.append(image_name)
                        if counter < total:
                            message = "Processing %d of %d FSNs. Spent %ss for the last FSN." %(counter, total, (datetime.datetime.now()-fsn_start_time))
                            progress = int(counter/total*100)
                            completion_status = False
                        else:
                            message = "Completed."
                            progress = 100
                            completion_status = True
                        self.progress.emit(message, progress, self.eta, completion_status, images_list, self.thread_index)
                        self.last_eta = self.eta
                        self.sendMessage.emit("Completed %d in %ss." %(counter, datetime.datetime.now() - start_time), self.last_eta, self.thread_index)
                self.allow_run = False

    def prepareAppImage(
                    self, 
                    fsn, 
                    brand, 
                    category, 
                    primary_attribute_data, 
                    secondary_attribute_data, 
                    parent_image_positioning, 
                    icon_positioning, 
                    icon_palette, 
                    allow_overlap, 
                    background_image_path, 
                    primary_attribute_relative_size, 
                    secondary_attribute_relative_size, 
                    bounding_box, 
                    use_simple_bg_color_strip, 
                    bg_color_strip_threshold, 
                    colors_list, 
                    fix_icon_text_case, 
                    preserve_icon_colors, 
                    font, 
                    font_color, 
                    use_icon_color_for_font_color, 
                    icon_font_size, 
                    output_location):
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
        #Multiprocessing.
        #manager = Manager()
        #return_dict = manager.dict()
        #Get the base empty canvas.
        base_image = Katana.getBaseImage()
        #Get the primary image path
        message = "Getting parent image for %s."%fsn
        self.sendMessage.emit(message, self.last_eta, self.thread_index)
        parent_image_path = Katana.getParentImage(fsn, self.repo_path)
        #Ready the parent image.
        message = "Resizing parent image for %s."%fsn
        self.sendMessage.emit(message, self.last_eta, self.thread_index)
        original_parent_image = Image.open(parent_image_path).convert("RGBA")
        #Check the resize reference for the smartfit option. Create use a local parent_image_resize_reference value to control this.
        if self.parent_image_resize_reference == "Smart Fit":
            parent_image_resize_reference = "Height" if original_parent_image.size[1]>original_parent_image.size[0] else "Width"
            message = "Resizing parent image by %s since Smart Fit was selected. (%s)"%(parent_image_resize_reference, fsn)
            self.sendMessage.emit(message, self.last_eta, self.thread_index)
            if (parent_image_resize_reference == "Width"):
                parent_image_resize_factor = (1.5*self.parent_image_resize_factor)
                if parent_image_resize_factor > 0.55:
                    parent_image_resize_factor = 0.55
            else:
                parent_image_resize_factor = self.parent_image_resize_factor
        else:
            parent_image_resize_reference = self.parent_image_resize_reference
            parent_image_resize_factor = self.parent_image_resize_factor
        message = "Resizing parent image to %f%% along the %s. (%s)"%(parent_image_resize_factor*100, parent_image_resize_reference, fsn)
        self.sendMessage.emit(message, self.last_eta, self.thread_index)
        resized_parent_image = Katana.getResizedImage(
                                                original_parent_image, 
                                                parent_image_resize_factor, 
                                                parent_image_resize_reference, 
                                                base_image.size)
        parent_image_size = resized_parent_image.size
        #Use the selected background colour strip algorithm 
        #to strip the parent image of its colour.
        if self.bypass_parent_image_cleanup:
            parent_image = resized_parent_image
        else:
            if use_simple_bg_color_strip:
                #Simple background strip just searches for white and removes it.
                #Later, this should be extended to remove any background color.
                message = "Stripping parent image background using simple strip algorithm for %s."%fsn
                self.sendMessage.emit(message, self.last_eta, self.thread_index)
                #Added for multiprocessing
                #parent_image_strip_process = Process(target=Katana.replaceColorInImage, args=(resized_parent_image, (255,255,255,255), (0,0,0,0), bg_color_strip_threshold, True, "Parent Image", return_dict))
                parent_image = Katana.replaceColorInImage(
                                                    resized_parent_image, 
                                                    (255,255,255,255), 
                                                    (0,0,0,0), 
                                                    bg_color_strip_threshold)
            else:
                #The complex movement algorithm takes thing by strokes.
                #First, it identifies the background colour, reading the
                #four corner pixels and taking the median of that list.
                #Then, it swipes up, down, left and right, turning the alpha
                #channel to zero, quitting whenever it encounters an RGB value
                #that is below or above the threshold.
                message = "Stripping parent image background using movement algorithm for %s."%fsn
                self.sendMessage.emit(message, self.last_eta, self.thread_index)
                parent_image = Katana.getStrippedImage(resized_parent_image, bg_color_strip_threshold)
                #parent_image_strip_process = Process(target=Katana.getStrippedImage, args=(resized_parent_image, bg_color_strip_threshold, True, "Parent Image", return_dict))
        #parent_image_strip_process.start()

        #Get the background image.
        message = "Getting background image for %s."%fsn
        self.sendMessage.emit(message, self.last_eta, self.thread_index)
        background_image = Katana.getBackgroundImage(background_image_path,
                                            self.use_category_specific_backgrounds, category, fsn, self.repo_path)
        #Get the primary and secondary attribute icons.
        
        #primary_attributes_process = Process(target=Katana.getIcons, args=(primary_attribute_data, category, primary_attribute_relative_size, base_image.size, colors_list, bounding_box, fix_icon_text_case, preserve_icon_colors, font, font_color, use_icon_color_for_font_color, icon_font_size, True, "Primary", return_dict))
        #primary_attributes_process.start()
        message = "Getting primary attribute data image for %s."%fsn
        self.sendMessage.emit(message, self.last_eta, self.thread_index)


        primary_attributes_and_icons_data = Katana.getIcons(
                                                    primary_attribute_data, 
                                                    category, 
                                                    primary_attribute_relative_size, 
                                                    base_image.size, 
                                                    colors_list, 
                                                    bounding_box, 
                                                    fix_icon_text_case, 
                                                    self.repo_path,
                                                    preserve_icon_colors, 
                                                    font, 
                                                    font_color, 
                                                    use_icon_color_for_font_color, 
                                                    icon_font_size)

        #secondary_attributes_process = Process(target=Katana.getIcons, args=(secondary_attribute_data,category,secondary_attribute_relative_size, base_image.size, colors_list, bounding_box, fix_icon_text_case, preserve_icon_colors, font, font_color, use_icon_color_for_font_color, icon_font_size, True, "Secondary", return_dict))
        #secondary_attributes_process.start()
        message = "Getting secondary attribute data image for %s."%fsn
        self.sendMessage.emit(message, self.last_eta, self.thread_index)
        secondary_attributes_and_icons_data = Katana.getIcons(
                                                    secondary_attribute_data,
                                                    category,
                                                    secondary_attribute_relative_size, 
                                                    base_image.size, 
                                                    colors_list, 
                                                    bounding_box, 
                                                    fix_icon_text_case,
                                                    self.repo_path,
                                                    preserve_icon_colors, 
                                                    font, 
                                                    font_color, 
                                                    use_icon_color_for_font_color, 
                                                    icon_font_size)
        #Based on the input control parameters, get the coordinates for the parent image.
        message = "Getting parent image coordinates corresponding to %s for %s."%(parent_image_positioning, fsn)
        self.sendMessage.emit(message, self.last_eta, self.thread_index)
        if parent_image_positioning == "Random":
            parent_image_positioning = Katana.getRandomParentImagePlacementPoints()
        parent_image_coords = Katana.getParentImageCoords(base_image.size,parent_image_size, parent_image_positioning)

        counter = 0
        #Added for multiprocessing
        #message = "Waiting for the primary icons process to complete for %s."%(fsn)
        #self.sendMessage.emit(message, self.last_eta, self.thread_index)
        #primary_attributes_process.join()
        #primary_attributes_and_icons_data = return_dict["Primary"] 
        #message = "Waiting for the secondary icons process to complete for %s."%(fsn)
        #self.sendMessage.emit(message, self.last_eta, self.thread_index)
        #secondary_attributes_process.join()
        #secondary_attributes_and_icons_data = return_dict["Secondary"]
        #message = "Getting USP icon coordinates for %s."%(fsn)
        #self.sendMessage.emit(message, self.last_eta, self.thread_index)
        icons_and_coordinates = Katana.getIconsAndCoordinates(
                                            base_image, 
                                            parent_image_size, 
                                            parent_image_coords, 
                                            primary_attributes_and_icons_data, 
                                            secondary_attributes_and_icons_data, 
                                            icon_positioning,
                                            "Separate", 
                                            parent_image_positioning
                                            )
        #Paste the FK and Brand Icon
        message = "Getting the merged Flipkart and Brand Logo for %s."%(fsn)
        self.sendMessage.emit(message, self.last_eta, self.thread_index)
        fk_brand_icon = Katana.getMergedFlipkartBrandImage(brand, self.repo_path)
        #message = "Waiting for the parent image strip process to complete for %s."%(fsn)
        #self.sendMessage.emit(message, self.last_eta, self.thread_index)
        #Waiting for the parent image strip process to complete so that we can retrieve the parent image.
        #parent_image_strip_process.join()
        #parent_image = return_dict["Parent Image"]
        message = "Pasting the parent image for %s."%(fsn)
        self.sendMessage.emit(message, self.last_eta, self.thread_index)
        base_image.paste(parent_image, parent_image_coords, parent_image)
        message = "Pasting the USP icons for %s."%(fsn)
        self.sendMessage.emit(message, self.last_eta, self.thread_index)
        for icon in icons_and_coordinates:
            try:
                position = tuple([int(pos) for  pos in  icon["Position"]])
                base_image.paste(icon["Icon"], position, icon["Icon"])
                #message = "Pasted icon on base image at %s for %s." %(icon["Position"],fsn)
                #self.sendMessage.emit(message, self.last_eta, self.thread_index)
            except:
                if icon["Position"] is None:
                    message = "Icon position cannot be None for %s." %(fsn)                    
                else:
                    message = "Encountered a problem while pasting the icon on base image at %s for %s." %(icon["Position"],fsn)
                self.sendMessage.emit(message, self.last_eta, self.thread_index)
                raise
        message = "Final preparations are ongoing for %s."%(fsn)
        self.sendMessage.emit(message, self.last_eta, self.thread_index)
        merged_base_image = Katana.getFinalBaseImage(base_image)
        #Remove this later.
        merged_base_image.paste(
                    fk_brand_icon,
                    (int(fk_brand_icon.size[0]*0.005),0), 
                    fk_brand_icon
                )
        merged_base_image.paste(
                    base_image, 
                    (int(fk_brand_icon.size[0]*0.05), int(fk_brand_icon.size[1]*1.05)), 
                    base_image
                )


        final_image = background_image.copy()
        margin = 1 - self.margin
        resized_dimensions = (
                            int(margin*merged_base_image.size[0]),
                            int(margin*merged_base_image.size[1])
                        )
        message = "Adjusting for the margin for %s."%(fsn)
        self.sendMessage.emit(message, self.last_eta, self.thread_index)
        resized_base_image = merged_base_image.resize(resized_dimensions, resample=PIL.Image.ANTIALIAS)
        base_image_x = (background_image.size[0]-resized_base_image.size[0])/2
        base_image_y = (background_image.size[1]-resized_base_image.size[1])/4
        base_image_coords = (
                        int(base_image_x), 
                        int(base_image_y)
                    )
        message = "Merging the background and USP image for %s."%(fsn)
        self.sendMessage.emit(message, self.last_eta, self.thread_index)
        final_image.paste(resized_base_image,base_image_coords,resized_base_image)
        message = "Converting to RGB for %s."%(fsn)
        self.sendMessage.emit(message, self.last_eta, self.thread_index)
        final_image = final_image.convert("RGB")
        message = "Saving the image for %s."%(fsn)
        self.sendMessage.emit(message, self.last_eta, self.thread_index)
        #Saving to the output folder with username and date subfolders.
        output_path = os.path.join(self.output_location, "Output", getpass.getuser(),datetime.datetime.now().strftime("%y%m%d"),category)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        image_path = os.path.join(output_path,fsn+"_app_image_%s.png"%datetime.datetime.now().strftime("%H%M%S"))
        final_image.save(image_path,dpi=(300,300), quality=100)
        return image_path


    def __del__(self):
        self.mutex.lock()
        self.condition.wakeOne()
        self.mutex.unlock()
        self.wait()