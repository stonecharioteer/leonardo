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
    sendCoords = QtCore.pyqtSignal(dict)

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
        self.parent_image_paths = None
        self.use_enforced_coords = False
        self.show_position_markers = False

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
        """
        #New algorithm:
        1. Prepare the base image.
        2. Open the Parent image:
            1. If the parent image dictionary contains this FSN, then use that image.
            2. If not, then use the Katana method to get the first image with the fsn in the starting portion
                of the filename.
        3. Resize the parent image.
        4. If a bypass isn't requested:
            1. Strip the parent image using either the simple algorithm or the edge detection method.
            2. If the bypass is requested, ignore the stripping and use the resized image. 
                (This saves a lot of time.)
        5. Get the background image.
        6. Get all the icons and attribute text as separate objects.
            1. {Attribute: value, icon: PIL.Image, text_image: PIL.Image}
            2. Don't resize or recolor anything just yet.
        7. Given a definite icon group count do this:
            1. If icons are to be colored by group, do so.
            2. If icons are to be colored individually, do so.
            3. Resize icons based on group size. Do not resize the text.
        8. Prepare a dataframe that has the size of the drawing canvas 
            (the one which contains just the parent and the icons).
            1. Instantiate it with zeroes.
        9. Get the parent image coordinates.
        10. Update the position dataframe to record the positions of the parent image.
            1. Here, each cell represents a pixel. 
            2. Record "Parent" across the pixels where the parent image will be.
        11. Split the icons into groups.
        12. Given the positioning method:
            1. Circular
            2. Rectangular
            Calculate positions such that whenever an icon is placed at a calculated position, 
            the position matrix is checked for any non-zero value.
        """
        #Get the base empty canvas.
        base_image = Katana.getBaseImage()
        #Get the primary image path
        message = "Getting parent image for %s."%fsn
        self.sendMessage.emit(message, self.last_eta, self.thread_index)
        if fsn not in self.parent_image_paths.keys():
            parent_image_path = Katana.getParentImage(fsn, self.repo_path)
        else:
            parent_image_path = self.parent_image_paths[fsn]
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


        #Get the background image.
        message = "Getting background image for %s."%fsn
        self.sendMessage.emit(message, self.last_eta, self.thread_index)
        background_image = Katana.getBackgroundImage(
                                            background_image_path,
                                            self.use_category_specific_backgrounds, 
                                            category, 
                                            self.repo_path)
        #Get the primary and secondary attribute icons.
        message = "Getting primary attribute data image for %s."%fsn
        self.sendMessage.emit(message, self.last_eta, self.thread_index)

        if self.show_position_markers:
            position_markers = [i+1 for i in range(len(primary_attribute_data + secondary_attribute_data))]
            print position_markers 
            primary_position_markers = position_markers[:len(primary_attribute_data)]
            secondary_position_markers = position_markers[len(primary_attribute_data):]
            print primary_position_markers, secondary_position_markers
        else:
            primary_position_markers = None
            secondary_position_markers = None
        primary_attributes_and_icons_data = Katana.getIcons(
                                                    primary_attribute_data, 
                                                    category, 
                                                    primary_attribute_relative_size, 
                                                    base_image.size, 
                                                    colors_list[0:len(primary_attribute_data)], 
                                                    bounding_box, 
                                                    fix_icon_text_case, 
                                                    self.repo_path,
                                                    preserve_icon_colors, 
                                                    font, 
                                                    font_color, 
                                                    use_icon_color_for_font_color, 
                                                    icon_font_size,
                                                    primary_position_markers)

        message = "Getting secondary attribute data image for %s."%fsn
        self.sendMessage.emit(message, self.last_eta, self.thread_index)
        secondary_attributes_and_icons_data = Katana.getIcons(
                                                    secondary_attribute_data,
                                                    category,
                                                    secondary_attribute_relative_size, 
                                                    base_image.size, 
                                                    colors_list[len(primary_attribute_data):], 
                                                    bounding_box, 
                                                    fix_icon_text_case,
                                                    self.repo_path,
                                                    preserve_icon_colors, 
                                                    font, 
                                                    font_color, 
                                                    use_icon_color_for_font_color, 
                                                    icon_font_size,
                                                    secondary_position_markers)
        #Based on the input control parameters, get the coordinates for the parent image.
        if not self.use_enforced_coords:
            message = "Getting parent image coordinates corresponding to %s for %s."%(parent_image_positioning, fsn)
            self.sendMessage.emit(message, self.last_eta, self.thread_index)
            if parent_image_positioning == "Random":
                parent_image_positioning = Katana.getRandomParentImagePlacementPoints()
            parent_image_coords = Katana.getParentImageCoords(base_image.size,parent_image_size, parent_image_positioning)
            counter = 0
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
            coords = {"Parent": parent_image_coords}
            counter = 1
            for icon in icons_and_coordinates:
                label = "USP-%d"%counter
                coords[label] = icon["Position"]
                counter+=1
            if len(icons_and_coordinates)<10:
                for i in range(10-len(icons_and_coordinates)):
                    label = "USP-%d"%(i+1+len(icons_and_coordinates))
                    coords[label] = [0,0]
            self.sendCoords.emit(coords)
        else:
            message =  "Using Enforced coordinates for %s!"%fsn
            self.sendMessage.emit(message, self.last_eta, self.thread_index)
            parent_image_coords = tuple([int(pos) for pos in self.enforced_coords["Parent"]])
            icon_data = primary_attributes_and_icons_data + secondary_attribute_data
            icons_and_coordinates = []
            counter=1
            for icon in icon_data:
                icons_and_coordinates.append({
                                        "Icon": icon["Icon"], 
                                        "Position": tuple([int(coord) for coord in self.enforced_coords["USP-%d"%counter]])
                                            })
                counter+=1
        #Paste the FK and Brand Icon
        message = "Getting the merged Flipkart and Brand Logo for %s."%(fsn)
        self.sendMessage.emit(message, self.last_eta, self.thread_index)
        fk_brand_icon = Katana.getMergedFlipkartBrandImage(brand, self.repo_path)
        message = "Pasting the parent image for %s."%(fsn)
        self.sendMessage.emit(message, self.last_eta, self.thread_index)
        base_image.paste(parent_image, parent_image_coords, parent_image)
        message = "Pasting the USP icons for %s."%(fsn)
        self.sendMessage.emit(message, self.last_eta, self.thread_index)
        for icon in icons_and_coordinates:
            try:
                position = tuple([int(pos) for  pos in  icon["Position"]])
                base_image.paste(icon["Icon"], position, icon["Icon"])
            except:
                if icon["Position"] is None:
                    message = "Icon position cannot be None for %s." %(fsn)                    
                else:
                    print icon["Position"], "is not a valid position!"
                    message = "Encountered a problem while pasting the icon on base image at %s for %s." %(icon["Position"],fsn)
                self.sendMessage.emit(message, self.last_eta, self.thread_index)
                raise
        message = "Final preparations are ongoing for %s."%(fsn)
        self.sendMessage.emit(message, self.last_eta, self.thread_index)
        merged_base_image = Katana.getFinalBaseImage(base_image)
#        merged_base_image.paste(
#                    fk_brand_icon,
#                    (int(fk_brand_icon.size[0]*0.005),0), 
#                    fk_brand_icon
#                )
        #Paste the base image.
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
        message = "Pasting FK brand logo for %s."%(fsn)
        self.sendMessage.emit(message, self.last_eta, self.thread_index)
        final_image.paste(fk_brand_icon,(0,0),fk_brand_icon)
        message = "Converting to RGB for %s."%(fsn)
        self.sendMessage.emit(message, self.last_eta, self.thread_index)
        final_image = final_image.convert("RGB")
        message = "Saving the image for %s."%(fsn)
        self.sendMessage.emit(message, self.last_eta, self.thread_index)
        #Saving to the output folder with username and date subfolders.
        output_path = os.path.join(self.output_location, "Output", getpass.getuser(),datetime.datetime.now().strftime("%y%m%d"),category)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        #image_path = os.path.join(output_path,fsn+"_app_image_%s.png"%datetime.datetime.now().strftime("%H%M%S"))
        image_path = os.path.join(output_path,fsn+"_app_image.png")
        final_image.save(image_path,dpi=(300,300), quality=100)
        return image_path


    def __del__(self):
        self.mutex.lock()
        self.condition.wakeOne()
        self.mutex.unlock()
        self.wait()