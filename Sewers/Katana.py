from __future__ import division
from multiprocessing import Pool, Queue, Lock, Process
import csv
import os, glob, datetime, random, math
import numpy as np
import pandas
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import PIL
from PyQt4 import QtGui, QtCore


def getTitleCase(sentence):
    import re
    while "  " in sentence:
        sentence = sentence.replace("  ", " ")
    exceptions = ["a", "an", "the", "of", "is", "and", "at", "if","but", "to", "upto","mm","l","ml","nm","cm","kPa","m","km","kmph","mph","hr","hrs", "kg", "gm", "gms"]
    word_list = re.split(" ", sentence)
    final = [word_list[0][0].capitalize()+word_list[0][1:]]
    for word in word_list[1:]:
        final.append(word in exceptions and word or (word[0].capitalize()+word[1:]))
    return " ".join(final)

def getRadians(degrees):
    import math
    if (degrees == 0):
        radians = 0.0
    elif degrees > 0:
        radians = degrees*math.pi/180.0
    elif degrees < 0:
        radians = (360-degrees)*math.pi/180
    return radians

def getBaseImage():
    from PIL import Image
    return Image.new("RGBA", (1800, 2800-200), (0,0,0,0))

def getFinalBaseImage(base_image):
    from PIL import Image
    return Image.new("RGBA", (base_image.size[0], base_image.size[1]+200), (0,0,0,0))    

def getBackgroundImage(background_path, use_category_specific_backgrounds, category):
    import random, os
    from PIL import Image
    import PIL
    if use_category_specific_backgrounds:
        backgrounds = glob.glob(os.path.join(os.getcwd(), "Images", "Backgrounds", "*%s*.*"%category.replace(" ","*")))
        background_path =  backgrounds[0]
    else:
        if background_path == "Random":
            backgrounds = glob.glob(os.path.join(os.getcwd(), "Images", "Backgrounds", "Background*.*"))
            background_path = random.choice(backgrounds)
    return Image.open(background_path).convert("RGBA").resize((1800,2800), resample=PIL.Image.ANTIALIAS)

def getFlipkartIconImage():
    import os
    from PIL import Image
    fk_logo_path = os.path.join("essentials","fk_logo.png")
    return Image.open(fk_logo_path).convert("RGBA")

def getBrandImage(fsn):
    from PIL import Image
    brand_image_path = fsn+".png"
    return Image.open(brand_image_path).convert("RGBA")

def getBrandImage_new(brand):
    import os, glob
    image_path = os.path.join("Images","Brands",brand.replace(" ","_")+"*.*")
    brand_image_path = glob.glob(image_path)[0]
    return Image.open(brand_image_path).convert("RGBA")

def getMergedFlipkartBrandImage(brand=None):
    flipkart_image = getFlipkartIconImage()
    padding_factor = 0.05
    final_image = flipkart_image
    if (brand is not None):
        if len(glob.glob(os.path.join("Images","Brands",brand.replace(" ","_")+"*.*"))) >0:
            #Open the brand image.
            original_brand_image = getBrandImage_new(brand)
            #Scale the brand image respective to the flipkart image's height.
            brand_image = getResizedImage(original_brand_image,1,"Height",flipkart_image.size)
            
            #Start a canvas whose length is 1.2x that of fk + brand.
            canvas_width = (flipkart_image.size[0] + brand_image.size[0])*(1+2*padding_factor)
            canvas_height = flipkart_image.size[1]

            canvas_size = (int(canvas_width), int(canvas_height))
            final_image = Image.new("RGBA",canvas_size,(255,255,255,0))
            #Paste the fk logo onto the left.
            flipkart_image_position = (0,0)
            final_image.paste(flipkart_image, flipkart_image_position, flipkart_image)
            #Paste the Brand logo onto the right.
            brand_image_position = (int(flipkart_image.size[0] + 2*padding_factor*(flipkart_image.size[0]+brand_image.size[0])),0)
            final_image.paste(brand_image, brand_image_position, brand_image)
            #At fk_width + 0.1x fk+brandwidth, draw a vertical line.
            final_image_drawing_handle = ImageDraw.Draw(final_image, mode="RGBA")
            line_top_x = flipkart_image.size[0] + padding_factor*(flipkart_image.size[0]+brand_image.size[0])
            line_top_y = 0.5*padding_factor*flipkart_image.size[1]
            line_top = (int(line_top_x), int(line_top_y))
            line_bottom_x = line_top_x
            line_bottom_y = (1-padding_factor*0.5)*flipkart_image.size[1]
            line_bottom = (int(line_bottom_x), int(line_bottom_y))
            line_path = [line_top, line_bottom]
            line_thickness = int(padding_factor/15*(flipkart_image.size[0]+brand_image.size[0]))
            final_image_drawing_handle.line(line_path, (0,0,0,200), line_thickness)        
            final_image.save(os.path.join("cache","FK_"+brand+".png"),dpi=(300,300))
    return final_image

def getIconsAndCoordinates(base_image, parent_image_size, parent_image_coords, primary_attributes_and_icons_data, secondary_attributes_and_icons_data, icon_arrangement, ordering, parent_image_positioning):
    #This is the way I'm getting icon positions now.
    import random, os, math
    #print "Parent Image is at: ", parent_image_positioning
    #First, store the parameters in an easily-readable manner.
    #Parent image dimensions
    width_parent, height_parent = parent_image_size
    #Parent image top left corner coordinates.
    x_top_left_parent, y_top_left_parent = parent_image_coords
    #Parent image center coordinates.
    x_center_parent, y_center_parent = (x_top_left_parent + width_parent/2), (y_top_left_parent + height_parent/2)
    #get base image size
    width_base, height_base = base_image.size
    #Seggregate the primary and secondary icons.
    primary_icons = [icon["Icon"] for icon in primary_attributes_and_icons_data]
    secondary_icons = [icon["Icon"] for icon in secondary_attributes_and_icons_data]
    icons = primary_icons + secondary_icons
    #Get the icon sizes.
    icon_sizes = [icon.size for icon in icons]
    icon_widths = [icon_size[0] for icon_size in icon_sizes]
    icon_heights = [icon_size[1] for icon_size in icon_sizes]
    #Get the maximum Icon width and height.
    max_icon_width = max(icon_widths)
    max_icon_height = max(icon_heights)
    mean_icon_width = sum(icon_widths)/len(icon_widths)
    mean_icon_height = sum(icon_heights)/len(icon_heights)
    working_average_icon_width = (max_icon_width + mean_icon_width)/2
    working_average_icon_height = (max_icon_height + mean_icon_height)/2

    #Split the operation based on whether the ordering is separate or alternate.
    if ordering == "Separate":
        #Primary and secondary icon lines and arrangement is to be kept separate.
        #Determine the kind of parent_image_alignment, based on the original parameter.
        if (parent_image_positioning in [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)]): 
        #Club this with other corner-based positions.
            #parent image is placed at the top-left corner
            if icon_arrangement == "Circular":
                #icons are to be arranged in arcs.
                if parent_image_positioning == (0.0,0.0):
                    #Validated.
                    primary_radius_multiplier = 0.65
                    secondary_radius_multiplier = 1.05
                    primary_theta_range = (getRadians(0),getRadians(90))
                    primary_arc_center = (x_top_left_parent, y_center_parent)
                    secondary_theta_range = (getRadians(0),getRadians(90))
                elif parent_image_positioning == (1.0,0.0):
                    #Validated.
                    primary_radius_multiplier = 0.65
                    secondary_radius_multiplier = 1.0
                    primary_theta_range = (getRadians(90),getRadians(180))
                    primary_arc_center = (x_center_parent, y_center_parent)
                    secondary_theta_range = (getRadians(90),getRadians(180))
                elif parent_image_positioning == (0.0,1.0):
                    #Validated.
                    #BottomLeft
                    primary_radius_multiplier = 0.70
                    secondary_radius_multiplier = 1.03
                    primary_theta_range = (getRadians(270+5),getRadians(360-15))
                    primary_arc_center = (x_top_left_parent, y_center_parent)
                    secondary_theta_range = (getRadians(270-2),getRadians(360-50))
                elif parent_image_positioning == (1.0, 1.0):
                    #Validated.
                    primary_radius_multiplier = 0.95
                    secondary_radius_multiplier = 1.25
                    theta_range = ((math.pi),(math.pi*1.5)) #180deg and ~270deg.
                    primary_theta_range = (getRadians(180+28),getRadians(270-12))
                    primary_arc_center = (x_top_left_parent+width_parent, y_center_parent)
                    secondary_theta_range = (getRadians(180+28),getRadians(270-12))
                
                primary_plot_points_required = len(primary_icons)
                #parent_extreme_point = (x_top_left_parent+width_parent, y_top_left_parent+height_parent)
                #diagonal_length = getDistanceBetweenPoints(primary_arc_center,parent_extreme_point)
                diagonal_length = width_base
                primary_radius = primary_radius_multiplier*diagonal_length
                primary_icon_positions = getPointsOnArc(primary_arc_center, primary_radius, primary_plot_points_required, primary_theta_range)
                secondary_plot_points_required = len(secondary_icons)
                secondary_arc_center = primary_arc_center
                secondary_radius = secondary_radius_multiplier*diagonal_length
                secondary_icon_positions = getPointsOnArc(secondary_arc_center, secondary_radius, secondary_plot_points_required, secondary_theta_range)
                coordinates_and_icons = []
                counter = 0
                for icon in primary_icons:
                    coord = {
                        "Icon": icon,
                        "Position":primary_icon_positions[counter]
                    }
                    coordinates_and_icons.append(coord)
                    counter+=1
                counter = 0
                for icon in secondary_icons:
                    coord = {
                        "Icon": icon,
                        "Position":secondary_icon_positions[counter]
                    }
                    coordinates_and_icons.append(coord)
                    counter+=1
            elif icon_arrangement == "Rectangular":

                #icons are to be laid out in arrays.
                pass
            else:
                print "Invalid icon arrangement passed to Katana. Icon Arrangement asked for is %s"%icon_arrangement
        elif parent_image_positioning in [(0.5,0.0),(0.0,0.5),(1.0,0.5),(0.5,1.0)]:
            if icon_arrangement == "Circular":
                #icons are to be arranged in arcs.
                if parent_image_positioning == (0.5,0.0):
                    #Validated and perfected.
                    #parent image is placed at the top-middle.
                    primary_radius_multiplier = 0.75
                    secondary_radius_multiplier = 2.00
                    theta_range = ((0),(math.pi)) #~0deg and ~180deg.
                    #Arc center positions
                    primary_arc_center = ((width_base*0.35), (height_base*0.4))
                    secondary_arc_center = ((width_base*0.35), (height_base*0.25))
                    #Angles
                    primary_theta_range = (getRadians(0), getRadians(180))
                    secondary_theta_range = (getRadians(0), getRadians(180))
                elif parent_image_positioning == (0.5, 1.0):
                    #Validated and perfected.
                    #Not very happy with this though.
                    #parent image is placed at the bottom middle.
                    primary_radius_multiplier = 0.85
                    secondary_radius_multiplier = 2.08
                    #Arc center positions
                    primary_arc_center = ((width_base*0.35), (height_base*0.6))
                    secondary_arc_center = ((width_base*0.35), (height_base*0.75))
                    #Angles
                    primary_theta_range = (getRadians(180), getRadians(360))
                    secondary_theta_range = (getRadians(180), getRadians(360))
                elif parent_image_positioning == (0.0,0.5):
                    #Validated and perfected.
                    #parent image is placed at the left-middle.
                    primary_radius_multiplier = 1.1
                    secondary_radius_multiplier = 1.6
                    #Arc center positions
                    primary_arc_center = (-x_center_parent, y_center_parent)
                    secondary_arc_center = primary_arc_center
                    #Angles
                    primary_theta_range = (getRadians(270),getRadians(360+90))
                    secondary_theta_range = (getRadians(270+30),getRadians(360-10))
                elif parent_image_positioning == (1.0, 0.5):
                    #Needs tweaking.
                    #parent image is placed at the right-middle
                    primary_radius_multiplier = 1.65
                    secondary_radius_multiplier = 2.10
                    #Arc center positions
                    primary_arc_center = (int(x_top_left_parent+width_parent), int(y_center_parent*0.9))
                    secondary_arc_center = (int(x_top_left_parent+width_parent), int(y_center_parent*0.9))
                    #Angles
                    primary_theta_range = (getRadians(180-35), getRadians(180+35))
                    secondary_theta_range = (getRadians(180-30), getRadians(180+30))
                
                primary_plot_points_required = len(primary_icons)
                #This isn't the diagonal per se. It's the maximum allowable radius.
                diagonal_length = width_base/2 
                #I need to detach this from the individual multipliers and use a better system.
                primary_radius = primary_radius_multiplier*diagonal_length
                
                primary_icon_positions = getPointsOnArc(
                                                primary_arc_center, 
                                                primary_radius, 
                                                primary_plot_points_required, 
                                                primary_theta_range
                                            )

                secondary_plot_points_required = len(secondary_icons)
                secondary_radius = secondary_radius_multiplier*diagonal_length
                secondary_icon_positions = getPointsOnArc(secondary_arc_center, secondary_radius, secondary_plot_points_required, secondary_theta_range)
                coordinates_and_icons = []
                counter = 0
                for icon in primary_icons:
                    coord = {
                        "Icon": icon,
                        "Position":primary_icon_positions[counter]
                    }
                    coordinates_and_icons.append(coord)
                    counter+=1
                counter = 0
                for icon in secondary_icons:
                    coord = {
                        "Icon": icon,
                        "Position":secondary_icon_positions[counter]
                    }
                    coordinates_and_icons.append(coord)
                    counter+=1
            elif icon_arrangement == "Rectangular":
                #icons are to be laid out in arrays.
                pass
            else:
                print "Invalid icon arrangement passed to Katana. Icon Arrangement asked for is %s."%icon_arrangement
        elif parent_image_positioning == (0.5, 0.5):
            #parent image is placed at the center-middle.
            if icon_arrangement == "Circular":
                #print "Center Position!"
                #Steps
                #First, figure out the space between the product image and the canvas edges.
                #If the space is at least 1.2x the maximum width of the icon images,
                #then and then alone should this try to place one icon on either side.
                #If the space isn't at least 1.2x on either side, shift the position 
                #of the arc so that it doesn't place the icon over the image.
                #Angle calculation
                primary_plot_points_required = len(primary_icons)
                secondary_plot_points_required = len(secondary_icons)
                icons_required = (primary_plot_points_required + secondary_plot_points_required)
                half_icons_required = math.ceil(icons_required/2)
                other_half_icons_required = icons_required - half_icons_required

                sweep_angle = 90
                primary_theta_range = (getRadians(270-sweep_angle), getRadians(270+sweep_angle))
                secondary_theta_range = (getRadians(90-sweep_angle), getRadians(90+sweep_angle))
                clearance_on_top = y_top_left_parent
                clearance_on_bottom = height_base - (y_top_left_parent + height_parent)
                clearance_on_left = x_top_left_parent
                clearance_on_right = width_base - (x_top_left_parent + width_parent)
                icon_space_required = max_icon_width*1.05
                
                if (clearance_on_left >= icon_space_required) and (clearance_on_right >= icon_space_required):
                    icon_arc_center_y_top = int(y_center_parent - 0.25*height_parent)
                    icon_arc_center_y_bottom = int(y_top_left_parent + 0.75*height_parent)
                    diagonal_length = (width_base-max_icon_width/2)/2
                else:
                    print "There's no space on either side of the product image, so we'll shift the icons up and down respectively."
                    icon_arc_center_y_top = int(y_top_left_parent-max_icon_height/4)
                    icon_arc_center_y_bottom = int(y_top_left_parent+height_parent-max_icon_height*2/3)
                    diagonal_length = (width_base-max_icon_width)/2

                primary_radius_multiplier = 1.0
                secondary_radius_multiplier = 1.0

                x_clearance = max_icon_width/2

                icon_arc_center_x_bottom = int(x_center_parent-x_clearance)
                icon_arc_center_x_top = int(x_center_parent-x_clearance)

                primary_arc_center = (icon_arc_center_x_top, icon_arc_center_y_top)
                secondary_arc_center = (icon_arc_center_x_bottom, icon_arc_center_y_bottom)
                

                primary_radius = primary_radius_multiplier*diagonal_length

                primary_icon_positions = getPointsOnArc(primary_arc_center, 
                                                primary_radius, 
                                                half_icons_required, 
                                                primary_theta_range
                                            )
                
                if secondary_plot_points_required > 0:
                    secondary_radius = secondary_radius_multiplier*diagonal_length
                    secondary_icon_positions = getPointsOnArc(secondary_arc_center, 
                                                    secondary_radius, 
                                                    other_half_icons_required, 
                                                    secondary_theta_range
                                                )
                else:
                    secondary_icon_positions = []
                coordinates_and_icons = []
                icon_positions = primary_icon_positions + secondary_icon_positions
                icons = primary_icons + secondary_icons
                counter = 0
                for icon in icons:
                    try:
                        coord = {
                            "Icon": icon,
                            "Position":icon_positions[counter]
                        }
                    except: 
                        print counter
                        icon.save("this.png")
                        raise
                    coordinates_and_icons.append(coord)
                    counter+=1
            elif icon_arrangement == "Rectangular":
                #Center position, rectangular placement.  Bottom gets precedence, more icons there than at the top,
                #unless symmetry comes into the picture.
                
                #Need to pass a list of dictionaries with icons and positions.
                primary_plot_points_required = len(primary_icons)
                secondary_plot_points_required = len(secondary_icons)
                icons_required = (primary_plot_points_required + secondary_plot_points_required)
                clearance_factor = 0.05
                
                canvas_x_left = 0.25*max_icon_width
                canvas_x_right = canvas_x_left + width_base - 1.5*max_icon_width
                canvas_y_top = int(clearance_factor*height_base)
                canvas_y_bottom = canvas_y_top + (1-clearance_factor)*height_base - 1.5*max_icon_height
                if canvas_y_bottom <= (y_top_left_parent+height_parent):
                    canvas_y_bottom = y_top_left_parent+height_parent + 0.05*max_icon_height
                canvas_center_x = (canvas_x_left+canvas_x_right)/2
                
                #print "Requested for %d icons."%(icons_required)
                if icons_required == 1:
                    icon_positions = [(canvas_center_x, canvas_y_top)]
                elif icons_required == 2:
                    icon_positions = [
                            (canvas_center_x-max_icon_width/3, canvas_y_top), 
                            (canvas_center_x+max_icon_width/2, canvas_y_top)
                            ]
                elif icons_required == 3:
                    icon_positions = [
                            (canvas_center_x-max_icon_width, canvas_y_top),
                            (canvas_center_x, canvas_y_bottom),
                            (canvas_center_x+max_icon_width, canvas_y_top)
                            ]
                elif icons_required == 4:
                    icon_positions = [
                            (canvas_center_x-max_icon_width, canvas_y_top), 
                            (canvas_center_x+max_icon_width, canvas_y_top),
                            (canvas_center_x-max_icon_width, canvas_y_bottom), 
                            (canvas_center_x+max_icon_width, canvas_y_bottom)
                            ]
                elif icons_required == 5:
                    icon_positions =  [
                            (canvas_center_x+1.5*max_icon_width, canvas_y_top),
                            (canvas_center_x, canvas_y_top),
                            (canvas_center_x-1.5*max_icon_width, canvas_y_top),
                            (canvas_x_left+max_icon_width/2, canvas_y_bottom), 
                            (canvas_x_right-max_icon_width/2, canvas_y_bottom)
                            ]
                elif icons_required == 6:
                    icon_positions = [
                            (canvas_center_x-1.5*mean_icon_width, canvas_y_top),
                            (canvas_center_x+0.05*mean_icon_width, canvas_y_top),
                            (canvas_center_x+1.5*mean_icon_width, canvas_y_top),
                            (canvas_center_x-1.5*mean_icon_width, canvas_y_bottom),
                            (canvas_center_x+0.05*mean_icon_width, canvas_y_bottom),
                            (canvas_center_x+1.5*mean_icon_width, canvas_y_bottom)
                            ]
                elif icons_required == 7:
                    icon_positions = [
                            (canvas_x_left, canvas_y_top),
                            (canvas_center_x-0.5*working_average_icon_width, canvas_y_top),
                            (canvas_center_x+0.5*working_average_icon_width, canvas_y_top),
                            (canvas_x_right, canvas_y_top),
                            (canvas_center_x-1.5*mean_icon_width, canvas_y_bottom),
                            (canvas_center_x, canvas_y_bottom),
                            (canvas_center_x+1.5*mean_icon_width, canvas_y_bottom)
                    ]
                else:
                    raise Exception("I  haven't accounted for %d icons"%icons_required)                
                counter = 0
                coordinates_and_icons = []
                for icon in icons:
                    try:
                        coord = {
                            "Icon": icon,
                            "Position":icon_positions[counter]
                        }
                    except: 
                        print counter
                        icon.save("this.png")
                        raise Exception("Too few USPS!")
                    coordinates_and_icons.append(coord)
                    counter+=1
            else:
                print "Invalid icon arrangement passed to Katana. Icon Arrangement asked for is %s"%icon_arrangement
        else:
            print "Parent image positioning hint isn't valid. %r" %parent_image_positioning
    return coordinates_and_icons

def getIconRectangularPosition(icon_number, total_icons, icon_size, canvas_size, parent_image_size=None, parent_image_coords=None, max_icon_height=None, max_icon_width=None):
    #Currently accounts only for 0.5, 0.5 position
    icon_width, icon_height = icon_size
    icon_width, icon_height = max_icon_width, max_icon_height
    canvas_width, canvas_height = canvas_size
    canvas_left = 0 + canvas_width/2
    canvas_right = canvas_left+canvas_width
    canvas_top = 0
    canvas_bottom = canvas_top + canvas_height
    canvas_x_center = (canvas_left+canvas_right)/2

    if total_icons == 1:
        #*
        #
        pos = (canvas_x_center-icon_width,canvas_top)
    
    elif total_icons == 2:
        #**
        #
        if icon_number == 1:
            pos = (canvas_x_center-3/2*icon_width,canvas_top)
        else:
            pos = (canvas_x_center+3/2*icon_width,canvas_top)

    elif total_icons == 3:
        #**
        #*
        if icon_number == 1:
            pos = (canvas_x_center-3/2*icon_width,canvas_top)
        elif icon_number == 2:
            pos = (canvas_x_center-icon_width,canvas_top)
        else:
            pos = (canvas_x_center-3/2*icon_width,canvas_top)

    elif total_icons == 4:
        #**
        #**
        if icon_number == 1:
            pos = (canvas_x_center-3/2*icon_width,canvas_top)
        elif icon_number == 2:
            pos = (canvas_x_center-3/2*icon_width,canvas_bottom-max_icon_height)
        elif icon_number == 3:
            pos = (canvas_x_center+3/2*icon_width,canvas_top)
        else:
            pos = (canvas_x_center+3/2*icon_width,canvas_bottom-max_icon_height)

    elif total_icons == 5:
        #***
        #**
        if icon_number == 1:
            pos = (canvas_x_center-3/2*icon_width,canvas_top)
        elif icon_number == 2:
            pos = (canvas_x_center-1*icon_width,canvas_top)
        elif icon_number == 3:
            pos = (canvas_x_center+3/2*icon_width,canvas_top)
        elif icon_number == 4:
            pos = (canvas_x_center-3/2*icon_width,canvas_bottom-max_icon_height)
        else:
            pos = (canvas_x_center+3/2*icon_width,canvas_bottom-max_icon_height)

    elif total_icons == 6:
        #***
        #***
        if icon_number == 1:
            pos = (canvas_x_center-3/2*icon_width,canvas_top)
        elif icon_number == 2:
            pos = (canvas_x_center-icon_width,canvas_top)
        elif icon_number == 3:
            pos = (canvas_x_center+3/2*icon_width,canvas_top)
        elif icon_number == 4:
            pos = (canvas_x_center-3/2*icon_width,canvas_bottom-max_icon_height)
        elif icon_number == 5:
            pos = (canvas_x_center-icon_width,canvas_bottom-max_icon_height)
        else:
            pos = (canvas_x_center+3/2*icon_width,canvas_bottom-max_icon_height)

    elif total_icons == 7:
        #****
        #***
        if icon_number == 1:
            pos = (canvas_x_center-icon_width/2-icon_width,canvas_top)
        elif icon_number == 2:
            pos = (canvas_x_center-icon_width/2+icon_width,canvas_top)
        elif icon_number == 3:
            pos = (canvas_x_center-icon_width/2-2*icon_width,canvas_top)
        elif icon_number == 4:
            pos = (canvas_x_center-icon_width/2+2*icon_width,canvas_top)
        elif icon_number == 5:
            pos = (canvas_x_center-icon_width/2-icon_width,canvas_bottom-max_icon_height)
        elif icon_number == 6:
            pos = (canvas_x_center-icon_width/2,canvas_bottom-max_icon_height)
        else:
            pos = (canvas_x_center-icon_width/2+icon_width,canvas_bottom-max_icon_height)
    else:
        raise Exception("Number of USPs is out of the scope of Leonardo.")
    return pos

def getPointsOnCircle(origin, radius, divisions):
    return getPointsOnArc(origin, radius, divisions, (0,2*math.pi)) #What is a circle, but an arc between 0 and 2*Pi?

def getPointOnCircle(origin, radius, theta):
    return (int(origin[0]+radius*math.cos(theta)),int(origin[1]+radius*math.sin(theta)))

def getDegreeFromRadians(theta):
    return theta*180/math.pi

def getPointsOnArc(origin, radius, divisions, theta_range):
    theta_max = max(theta_range)
    theta_min = min(theta_range)
    theta_step = (theta_max-theta_min)/divisions
    theta_diff = theta_max-theta_min
    #print "%d Divisions"%divisions
    #print "Max angle: %f, Min: %f"% (getDegreeFromRadians(theta_max), getDegreeFromRadians(theta_min) )
    if divisions == 0:
        thetas = [(theta_max-theta_min)*0.5]
    elif divisions == 1:
        thetas = [0.5*theta_diff+theta_min]
    elif divisions == 2:
        thetas = [0.25*theta_diff+theta_min, 0.75*theta_diff+theta_min]
    elif divisions == 3:
        thetas = [0.15*theta_diff+theta_min, 0.5*theta_diff+theta_min, 0.85*theta_diff+theta_min]
    elif divisions == 4:
        thetas = [0*theta_diff+theta_min, 0.33*theta_diff+theta_min, 0.66*theta_diff+theta_min, 1.0*theta_diff+theta_min]
    elif divisions == 5:
        thetas = [0*theta_diff+theta_min, 0.25*theta_diff+theta_min, 0.5*theta_diff+theta_min, 0.75*theta_diff+theta_min, 1.0*theta_diff+theta_min]
    else:
        #old method.
        theta = theta_min
        thetas = []
        while (theta <= theta_max):
            thetas.append(theta)
            theta += theta_step
    
    #print [getDegreeFromRadians(theta) for theta in thetas]
    points = [getPointOnCircle(origin, radius, theta) for theta in thetas]
    return points

def getPointOnCircleCartesian(origin_x,origin_y,radius,ref_x=None,ref_y=None):
    if ref_x is None:
        checker=(radius**2-(origin_x-ref_x)**2)
        if checker>=0:
            ref_y = checker**0.5+origin_y
            return ref_y
        else:
            print "No such x-coordinate possible."
            return False
    elif ref_y is None:
        checker=(radius**2-(origin_y-ref_y)**2)
        if checker>=0:
            ref_x = checker**0.5+origin_x
            return ref_x
        else:
            print "No such x-coordinate possible."
            return False
    else:
        print "Don't give both coordinates!"

def getDistanceBetweenPoints(point_1,point_2):
    return ((point_1[0]-point_2[0])**2 + (point_1[1]-point_2[1])**2)**0.5

def replaceColorInImage(image, original_colour, replacement_color, threshold, multiprocess=None, manager_return_handle=None, manager_return_dict=None):
    import numpy as np
    if multiprocess is None:
        multiprocess = False
    if multiprocess:
        if (manager_return_dict is None):
            raise Exception("Provide a multiprocessing.Manager().dict() in order to get a return value.")
        if manager_return_handle is None:
            print "No key was provided for the dictionary. Defaulting to 0."
            manager_return_handle = 0
    image_data = np.array(image)
    #print image.size
    #print image_data.shape
    #raw_input("Waiting!")
    rows, columns, rgba = image_data.shape
    original_r, original_g, original_b, original_a = original_colour
    for row in range(rows):
        for column in range(columns):
            pixel = image_data[row][column]
            pixel_red, pixel_green, pixel_blue, pixel_alpha = pixel
            if ((original_r-threshold)<=pixel_red<=(original_r+threshold)) and ((original_g-threshold)<=pixel_green<=(original_g+threshold)) and ((original_b-threshold)<=pixel_blue<=(original_b+threshold)):
                image_data[row][column] = replacement_color
#    image_data[(image_data == original_colour).all(axis=-1)] = replacement_color
    #image_data[(min_color <=image_data <= max_colour).all(axis=-1)] = replacement_color
    requested_image = Image.fromarray(image_data,mode="RGBA")
    if multiprocess:
        manager_return_dict.update({manager_return_handle: requested_image})
    else:
        return requested_image

def getStrippedImage(image, threshold, multiprocess=None, manager_return_handle=None, manager_return_dict=None):
    """This method removes the background color of the image be recursively going through rows and columns, horizontally and vertically, forward and in reverse."""
    import numpy as np
    if multiprocess is None:
        multiprocess = False
    if multiprocess:
        if (manager_return_dict is None):
            raise Exception("Provide a multiprocessing.Manager().dict() in order to get a return value.")
        if manager_return_handle is None:
            print "No key was provided for the dictionary. Defaulting to 0."
            manager_return_handle = 0
    image_data_columns, image_data_rows = image.size
    image_data = np.array(image)

    row_min, col_min = 0, 0
    row_max, col_max = image_data_rows-1, image_data_columns-1
    rgba_at_borders = [image_data[row_min][col_min],image_data[row_min][col_max],image_data[row_max][col_min],image_data[row_max][col_max]]
    r_border, g_border, b_border, a_border = np.median(np.array(rgba_at_borders),axis=0)
    row_indices = range(row_max+1)
    column_indices = range(col_max+1)
    reversed_row_indices = list(reversed(row_indices))
    reversed_column_indices = list(reversed(column_indices))
    replacement_color = [255,255,255,0]
    #Rows: Top to bottom
    for row_number in row_indices:
        row_of_pixels = image_data[row_number]
        keep_looking_forth = True
        previous_pixel = None
        #Columns: left to right.
        for column_number in column_indices:
            if keep_looking_forth:
                pixel = row_of_pixels[column_number]
                pixel_red, pixel_green, pixel_blue, pixel_alpha = pixel
                if ((r_border-threshold)<=pixel_red<=(r_border+threshold)) and ((g_border-threshold)<=pixel_green<=(g_border+threshold)) and ((b_border-threshold)<=pixel_blue<=(b_border+threshold)):
                    pixel = (pixel_red, pixel_green, pixel_blue,0)
                    image_data[row_number][column_number] = pixel
                else:
                    #On finding a pixel that doesn't lie in this color, quit
                    keep_looking_forth = False
                    break
        #Columns: right to left.
        keep_looking_reverse = True
        for column_number in reversed_column_indices:
            if keep_looking_reverse:
                pixel = row_of_pixels[column_number]
                pixel_red, pixel_green, pixel_blue, pixel_alpha = pixel
                if ((r_border-threshold)<=pixel_red<=(r_border+threshold)) and ((g_border-threshold)<=pixel_green<=(g_border+threshold)) and ((b_border-threshold)<=pixel_blue<=(b_border+threshold)):
                    pixel = (pixel_red, pixel_green, pixel_blue,0)
                    image_data[row_number][column_number] = pixel
                else:
                    #On finding a pixel that doesn't lie in this color, quit
                    keep_looking_reverse = False
                    break

    #Rows: Bottom to top
    for row_number in reversed_row_indices:
        #Columns: left to right.
        row_of_pixels = image_data[row_number]
        keep_looking_forth = True
        for column_number in column_indices:
            if keep_looking_forth:
                pixel = row_of_pixels[column_number]
                pixel_red, pixel_green, pixel_blue, pixel_alpha = pixel
                if ((r_border-threshold)<=pixel_red<=(r_border+threshold)) and ((g_border-threshold)<=pixel_green<=(g_border+threshold)) and ((b_border-threshold)<=pixel_blue<=(b_border+threshold)):
                    pixel = (pixel_red, pixel_green, pixel_blue,0)
                    image_data[row_number][column_number] = pixel
                else:
                    #On finding a pixel that doesn't lie in this color, quit
                    keep_looking_forth = False
                    break
        #Columns: right to left.
        keep_looking_reverse = True
        for column_number in reversed_column_indices:
            if keep_looking_reverse:
                pixel = row_of_pixels[column_number]
                pixel_red, pixel_green, pixel_blue, pixel_alpha = pixel
                if ((r_border-threshold)<=pixel_red<=(r_border+threshold)) and ((g_border-threshold)<=pixel_green<=(g_border+threshold)) and ((b_border-threshold)<=pixel_blue<=(b_border+threshold)):
                    pixel = (pixel_red, pixel_green, pixel_blue,0)
                    image_data[row_number][column_number] = pixel
                else:
                    #On finding a pixel that doesn't lie in this color, quit
                    keep_looking_reverse = False
                    break

    #COLUMNWISE SEARCH FOR BG COLOR
    #Columns: Left to Right
    for column_number in column_indices:
        #Rows: Top to Bottom
        keep_looking_forth = True
        for row_number in row_indices:
            if keep_looking_forth:
                pixel = image_data[row_number][column_number]
                pixel_red, pixel_green, pixel_blue, pixel_alpha = pixel
                if ((r_border-threshold)<=pixel_red<=(r_border+threshold)) and ((g_border-threshold)<=pixel_green<=(g_border+threshold)) and ((b_border-threshold)<=pixel_blue<=(b_border+threshold)):
                    pixel = (pixel_red, pixel_green, pixel_blue,0)
                    image_data[row_number][column_number] = pixel
                else:
                    #On finding a pixel that doesn't lie in this color, quit
                    keep_looking_forth = False
                    break

        #Rows: Bottom to Top 
        keep_looking_reverse = True
        for row_number in reversed_row_indices:
            if keep_looking_reverse:
                pixel = image_data[row_number][column_number]
                pixel_red, pixel_green, pixel_blue, pixel_alpha = pixel
                if ((r_border-threshold)<=pixel_red<=(r_border+threshold)) and ((g_border-threshold)<=pixel_green<=(g_border+threshold)) and ((b_border-threshold)<=pixel_blue<=(b_border+threshold)):
                    pixel = (pixel_red, pixel_green, pixel_blue,0)
                    image_data[row_number][column_number] = pixel
                else:
                    #On finding a pixel that doesn't lie in this color, quit
                    keep_looking_reverse = False
                    break

    #Columns: Right to Left
    for column_number in reversed_column_indices:
        #Rows: Top to Bottom
        keep_looking_forth = True
        for row_number in row_indices:
            if keep_looking_forth:
                pixel = image_data[row_number][column_number]
                pixel_red, pixel_green, pixel_blue, pixel_alpha = pixel
                if ((r_border-threshold)<=pixel_red<=(r_border+threshold)) and ((g_border-threshold)<=pixel_green<=(g_border+threshold)) and ((b_border-threshold)<=pixel_blue<=(b_border+threshold)):
                    pixel = (pixel_red, pixel_green, pixel_blue,0)
                    image_data[row_number][column_number] = pixel
                else:
                    #On finding a pixel that doesn't lie in this color, quit
                    keep_looking_forth = False
                    break

        #Rows: Bottom to Top 
        keep_looking_reverse = True
        for row_number in reversed_row_indices:
            if keep_looking_reverse:
                pixel = image_data[row_number][column_number]
                pixel_red, pixel_green, pixel_blue, pixel_alpha = pixel
                if ((r_border-threshold)<=pixel_red<=(r_border+threshold)) and ((g_border-threshold)<=pixel_green<=(g_border+threshold)) and ((b_border-threshold)<=pixel_blue<=(b_border+threshold)):
                    pixel = (pixel_red, pixel_green, pixel_blue,0)
                    image_data[row_number][column_number] = pixel
                else:
                    #On finding a pixel that doesn't lie in this color, quit
                    keep_looking_reverse = False
                    break

    stripped_image = Image.fromarray(image_data,mode="RGBA")
    if multiprocess:
        manager_return_dict.update({manager_return_handle: stripped_image})
    else:
        return stripped_image


def getResizedImage(image_to_resize,resize_factor,resize_by,base_image_size):
    import PIL
    image_to_resize_original_width, image_to_resize_original_height = image_to_resize.size
    base_image_width, base_image_height = base_image_size
    if resize_by == "Width":
        resized_width = resize_factor*base_image_width
        resized_height = image_to_resize_original_height*resized_width/image_to_resize_original_width
    else:
        resized_height = resize_factor*base_image_height
        resized_width = image_to_resize_original_width*resized_height/image_to_resize_original_height
    resized_dimensions = (int(resized_width),int(resized_height))
    #if (resized_height > image_to_resize_original_height) or (resized_width > image_to_resize_original_width):
    #    print "Requested image is being stretched. Use caution when doing this."
    resized_image = image_to_resize.resize(resized_dimensions, resample=PIL.Image.ANTIALIAS)
    return resized_image

def getParentImageCoords(base_image_size, parent_image_size, parent_image_positioning):
    base_width, base_height = base_image_size
    parent_width, parent_height = parent_image_size
    x_pos_factor, y_pos_factor = parent_image_positioning
    x_pos = int((base_width-parent_width)*x_pos_factor)
    y_pos = int((base_height-parent_height)*y_pos_factor)
    return (x_pos, y_pos)

def getRandomParentImagePlacementPoints():
    import random
    #return (random.choice([0.0,1.0]), random.choice([0.0,1.0]))
    return (random.choice([0.0,0.5,1.0]), random.choice([0.0,0.5,1.0]))

def getParentImage(fsn):
    try:
        parent_image_path = glob.glob(os.path.join(os.getcwd(),"Images","Parent Images","%s*.*"%fsn))[0]
    except:
        parent_image_path = os.path.join("essentials","na_parent_image.png")
    return parent_image_path

def getIcons(attribute_data, category, icon_relative_size, base_image_size, colors_list, bounding_box, fix_icon_text_case, preserve_icon_original_colors=None, font=None, font_color=None, use_icon_color_for_font_color=None, icon_font_size=None, multiprocess=None, manager_return_handle=None, manager_return_dict=None):
    #print attribute_data, category
    if multiprocess is None:
        multiprocess = False
    if multiprocess:
        if manager_return_dict is None:
            raise Exception("Provide a multiprocessing.Manager().dict() in order to get a return value.")
        if manager_return_handle is None:
            print "No key was provided for the dictionary. Defaulting to 0."
            manager_return_handle = 0
    look_in_path = os.path.join(os.getcwd(),"Images","Repository",category)
    image_search_path = os.path.join(look_in_path, "*.*")
    images_in_look_in_path = glob.glob(image_search_path)
    #print look_in_path,"\n",image_search_path
    #print images_in_look_in_path
    attributes_without_icons = []
    for attribute in attribute_data:
        found_icon = False
        #Look for image files in the folder.
        for icon in images_in_look_in_path:
            #If it hasn't yet found an icon, or in first run.
            if not found_icon:
                if attribute["Attribute"].lower().strip() == os.path.basename(icon.lower().strip())[:os.path.basename(icon.lower().strip()).find(".")]:
                    #print attribute["Attribute"].lower().strip(), icon.lower().strip()
                    icon_with_text = getIconImage(icon, 
                                            attribute["Description Text"], icon_relative_size, 
                                            base_image_size, colors_list,bounding_box, fix_icon_text_case, 
                                            preserve_icon_original_colors, font, font_color, 
                                            use_icon_color_for_font_color, icon_font_size
                                            )

                    attribute.update({"Icon": icon_with_text})
                    found_icon = True
                    #attribute.update({"Icon": None})
            else:
                #If it has already found an icon, do nothing.
                break
        if not found_icon:
            na_icon_path = os.path.join("essentials","icon_na.png")
            icon_with_text = getIconImage(na_icon_path, 
                                    attribute["Description Text"], icon_relative_size, base_image_size, 
                                    colors_list, bounding_box, fix_icon_text_case, 
                                    preserve_icon_original_colors, font, font_color, 
                                    use_icon_color_for_font_color, icon_font_size
                                    )

            attribute.update({"Icon": icon_with_text})
            attributes_without_icons.append(attribute["Attribute"])
    #if (len(attributes_without_icons) > 0):
    #    print "The following %s attributes don't have icons. Recommend making them before progressing." %category
    #    print attributes_without_icons
    #    print "Looking in the %s folder."%image_search_path
    if multiprocess:
        manager_return_dict.update({manager_return_handle: attribute_data})
    else:
        return attribute_data

def checkIcon(attribute, category, repository_path=None, description_text=None):
    import glob
    import os
    from PIL import Image
    if not repository_path:
        images_path = os.path.join("Images","Repository")
    else:
        images_path = repository_path
    icon_name = "%s.png"%attribute
    category_folder_path = os.path.join(images_path, category)
    search_string = os.path.join(category_folder_path,icon_name)
    try:
        possible_icons_list = glob.glob(search_string)
    except:
        print search_string
        raise
    folders_with_icons = []
    if len(possible_icons_list)>0:
        icon_found = True
        icon_path = possible_icons_list[0]
        folders_with_icons.append(os.path.basename(category_folder_path))
    else:
        try:
            list_of_folders = glob.glob(os.path.join(images_path,"*",""))
        except:
            print os.path.join(images_path,"*","")
            raise
        for folder in list_of_folders:
            possible_icons_list = glob.glob(os.path.join(folder,icon_name))
            if len(possible_icons_list) >0:
                folders_with_icons.append(os.path.basename(os.path.normpath(folder)))
        if len(folders_with_icons) >0:
            icon_found = True
        else:
            icon_found = False

    return icon_found, folders_with_icons

def getIconImage(icon_path, description_text, icon_relative_size, base_image_size, colors_list, bounding_box, fix_icon_text_case, preserve_icon_original_colors=None, font_path=None, font_color=None, use_icon_color_for_font_color=None, icon_font_size=None):
    """This method generates an image object which contains the icon image 
    as well as the description text."""
    import textwrap
    import numpy as np
    import PIL
    #get an image object using the icon path, and resize it to the required dimensions with respect to the height of the base image.
    #Don't strip for now.
    #icon_image = getStrippedImage(getResizedImage(Image.open(icon_path).convert("RGBA"),icon_relative_size,"height",base_image_size), threshold=30)
    icon_image = getResizedImage(Image.open(icon_path).convert("RGBA"), icon_relative_size,"height",base_image_size)
    if bounding_box != "None":
        shape = bounding_box.replace(" ","_")
        shape_width = int((max(icon_image.size))*1.45)
        shape_path = os.path.join("Images","Shapes","%s.png"%shape)
        shape = Image.open(shape_path).convert("RGBA").resize((shape_width,shape_width), resample=PIL.Image.ANTIALIAS)
        shape_and_icon= shape
        icon_x = int(shape.size[0]/2-icon_image.size[0]/2)
        icon_y = int(shape.size[1]/2-icon_image.size[1]/2)
        icon_position_in_shape = (icon_x, icon_y)
        shape_and_icon.paste(icon_image, icon_position_in_shape, icon_image)
    else:
        shape_and_icon = icon_image
    #icon_image = replaceColorInImage(resized_icon_image,(255,255,255,255),(0,0,0,255))
    #Create a blank canvas for the text.
    #print colors_list
    black = [color for color in colors_list[0]]
    if len(black) == 3:
        black.append(255)
    black = tuple(black)
    
    grey_1 = [color for color in colors_list[1]]
    if len(grey_1) == 3:
        grey_1.append(255)
    grey_1 = tuple(grey_1)

    grey_2 = [color for color in colors_list[2]]
    if len(grey_2) == 3:
        grey_2.append(255)
    grey_2 = tuple(grey_2)

    grey_3 = [color for color in colors_list[3]]
    if len(grey_3) == 3:
        grey_3.append(255)
    grey_3 = tuple(grey_3)

    white = [color for color in colors_list[4]]
    if len(white) == 3:
        white.append(255)
    white = tuple(white)

    icon_image = shape_and_icon #remove to disable circle.
    if preserve_icon_original_colors is None:
        preserve_icon_original_colors = False
    if not preserve_icon_original_colors:
    #if icon_text_color != (0,0,0):
        icon_image_array = np.array(icon_image)
        row_index = 0
        for row in icon_image_array:
            column_index = 0
            for column in row:
                red, blue, green, alpha = column
                if alpha!=0:
                    if (red == 0) and (blue == 0) and (green == 0):
                        icon_image_array[row_index][column_index] = black
                    elif (0<red<100) and (0<blue<100) and (0<green<100):
                        icon_image_array[row_index][column_index] = grey_1
                    elif (100<=red<200) and (100<=blue<200) and (100<=green<200):
                        icon_image_array[row_index][column_index] = grey_2
                    elif (200<=red<255) and (200<=blue<255) and (200<=green<255):
                        icon_image_array[row_index][column_index] = grey_3
                    else:
                        icon_image_array[row_index][column_index] = white
                column_index += 1
            row_index += 1
        icon_image = Image.fromarray(icon_image_array,"RGBA")
    #
    #
    #
    #Put the text now.
    #
    #
    font_size=72
    font_size = icon_font_size #Set default font size for now.
    if fix_icon_text_case:
        description_text = getTitleCase(description_text)
    text_lengths = [len(word) for word in description_text.split(" ")]
    max_text_length = max(text_lengths)
    wrap_width = max_text_length if max_text_length > 10 else 10
    text_as_paragraphs = textwrap.wrap(description_text, width=wrap_width)
    line_lengths = [len(line) for line in text_as_paragraphs]
    max_line_width = max(line_lengths)
    line_count = len(line_lengths)
    #Create an ImageDraw text drawing handle.
    text_measure_handle = ImageDraw.Draw(Image.new("RGBA",(10, 10),(0,0,0,0)))
    canvas_width = shape_and_icon.size[0] #Set maximum width to the width of the canvas at first.
    if font_path is None:
        font = ImageFont.truetype(os.path.join("essentials","RionaSans-Regular.ttf"), font_size)
    else:
        font = ImageFont.truetype(font_path, font_size)
    widths = [text_measure_handle.textsize(line, font=font)[0] for line in text_as_paragraphs]
    heights = [text_measure_handle.textsize(line, font=font)[1] for line in text_as_paragraphs]

    current_h, pad = 0, 15 #this is the padding.
    max_w = int(max(widths) if max(widths) > canvas_width else canvas_width)
    max_h = int(sum(heights) + pad*(len(heights)))
    text_canvas = Image.new("RGBA",(max_w, max_h),(0,0,0,0))
    draw_text_handle = ImageDraw.Draw(text_canvas)
    #Ref: http://stackoverflow.com/questions/1970807/center-middle-align-text-with-pil
    if not use_icon_color_for_font_color:
        icon_text_color = tuple(font_color)
    else:
        icon_text_color = black
    for line in text_as_paragraphs:
        w, h = draw_text_handle.textsize(line, font=font)
        draw_text_handle.text(((int((max_w-w)/2)), current_h), line, icon_text_color, font=font)
        current_h += h + pad
    
    #merge both images now.
    final_canvas_width = text_canvas.size[0] if text_canvas.size[0] >= icon_image.size[0] else icon_image.size[0]
    final_canvas_height = text_canvas.size[1] + icon_image.size[1] + 2*pad

    final_canvas = Image.new("RGBA",(final_canvas_width, final_canvas_height))
    icon_x = int((final_canvas.size[0]-icon_image.size[0])/2)
    icon_y = 0
    icon_position = (icon_x, icon_y)
    text_x = int((final_canvas.size[0]-text_canvas.size[0])/2)
    text_y = int(final_canvas.size[1]-text_canvas.size[1]+pad)
    text_canvas_position = (text_x, text_y)
    final_canvas.paste(icon_image, icon_position, icon_image)
    final_canvas.paste(text_canvas, text_canvas_position, text_canvas)
    #final_canvas.save(os.path.join("cache",os.path.basename(icon_path)))
    return final_canvas

def getValidPlacementPoints(base_image_size, parent_image_size, parent_coordinates, past_icons_data, new_icon_data, allow_overlap):
    """This method calculates valid positions for icons."""
    base_width, base_height = base_image_size
    parent_width, parent_height = parent_image_size
    parent_x, parent_y = parent_coordinates
    icon_width, icon_height = new_icon_data["Icon"].size

    right_gap = (base_width-(parent_x+parent_width))
    bottom_gap = (base_height-(parent_y+parent_height))
    if past_icons_data is None:
        #Figure out if the icon can be placed to the left or the right of the parent image.
        if parent_x > icon_width:
            allow_left = True
        elif parent_x == icon_width:
            allow_left = True
        else: #parent_x < icon_width
            allow_left = False

        if right_gap < icon_width:
            allow_right = False
        else:
            allow_right = True

        left_gap= parent_x-icon_width
        right_gap_limit = base_width-icon_width


        if allow_right and allow_left:
            #Can be between 0 and parent_x-icon_width, OR right_gap and base_width-icon_width
            icon_x = int(random.sample((random.uniform(0,left_gap),random.uniform(right_gap,right_gap_limit)),1)[0]) #random.sample gives a list. So pick the first item.
        elif allow_left and (not allow_right):
            icon_x = int(random.uniform(0,left_gap))
        elif (not allow_left) and allow_right:
            icon_x = int(random.uniform(right_gap,right_gap_limit))
        else:
            #not either!
            print "There's no space along the x axis for the icon."
            print "Icon size is:", icon_width, icon_height
            print "Parent image size is:", parent_width, parent_height
            print "Base image size is:", base_width, base_height
            print "Parent image is at:", parent_x, parent_y
            icon_x = 0
            #raw_input(">")

        if parent_y > icon_height:
            allow_top = True
        elif parent_y == icon_height:
            allow_top = True
        else: #parent_y < icon_height
            allow_top = False

        if bottom_gap < icon_height:
            allow_bottom = False
        else:
            allow_bottom = True

        top_gap= parent_y-icon_height
        bottom_gap_limit = base_height-icon_height

        if allow_top and allow_bottom:
            #Can be between 0 and parent_y-icon_height, OR top_gap and base_height-icon_height
            icon_y = int(random.sample((random.uniform(0,top_gap),random.uniform(top_gap,bottom_gap_limit)),1)[0])
        elif allow_top and (not allow_bottom):
            icon_y = int(random.uniform(0,top_gap))
        elif (not allow_top) and allow_bottom:
            icon_y = int(random.uniform(top_gap,bottom_gap_limit))
        else:
            #not either!
            print "There's no space along the y axis for the icon."
            print "Icon size is:", icon_width, icon_height
            print "Parent image size is:", parent_width, parent_height
            print "Base image size is:", base_width, base_height
            print "Parent image is at:", parent_x, parent_y
            icon_x, icon_y = 0,0

        return (icon_x,icon_y)

def getETA(start_time, counter, total):
    #from __future__ import division
    now = datetime.datetime.now()
    time_spent = now - start_time
    mean_time = time_spent.total_seconds()/counter
    ETA = start_time + datetime.timedelta(seconds=(mean_time*total))
    return ETA

def getCategoryFolderNames():
    import os, glob
    path_to_repo = os.path.join(os.getcwd(),"Images","Repository")
    path_and_folders_list = glob.glob(os.path.join(path_to_repo,"*"))

    return [os.path.basename(path_and_folder_name) for path_and_folder_name in path_and_folders_list]

def getListAsChunks(list_object, chunk_size):
    n = max(1, chunk_size)
    return [list_object[i:i+chunk_size] for i in range(0, len(list_object), chunk_size)]

def stripBGInBatches(image_batch, process_lock, process_id, output_path, threshold=None):
    from multiprocessing import Process, Pool, Queue, Lock
    from PIL import Image
    import os
    import datetime
    if threshold is None:
        threshold=30
    start_time = datetime.datetime.now()
    total = len(image_batch)
    counter = 0
    process_lock.acquire()
    print "Process %d starting now."%process_id
    process_lock.release()
    for image_path in image_batch:
        output_file_name = os.path.join(output_path, os.path.splitext(os.path.basename(image_path))[0]+".png")
        #process_lock.acquire()
        #print "[P%d]: %s. %s"%(process_id, image_path, output_file_name)
        #process_lock.release()
        getStrippedImage(Image.open(image_path).convert("RGBA"), threshold).save(output_file_name)
        counter+=1
        eta_string = getETA(start_time, counter, total).strftime("%H:%M:%S")
        process_lock.acquire()
        print "[P%d]: Completed %d of %d. ETA: %s."%(process_id, counter, total, eta_string)
        process_lock.release()
    process_lock.acquire()
    print "Process %d ended now. Total Time: %ds"%(process_id, (datetime.datetime.now()-start_time).seconds)
    process_lock.release()

def tryMultipleStrips(allowed_processes=None):
    """Test function to try out python's multi-processing module."""
    #from __future__ import division
    from multiprocessing import Process, Pool, Queue, Lock
    import datetime
    import glob
    import os
    import PIL
    import pandas
    path_to_test = os.path.join("Images","Parent Images","Test")
    output_path = os.path.join(path_to_test,"Output")
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    image_path_list = glob.glob(os.path.join(path_to_test,"*.jpeg"))
    start_time = datetime.datetime.now()
    update_time = datetime.datetime.now()
    if allowed_processes is None:
        allowed_processes = 3
    no_of_images = len(image_path_list)
    print "Loaded %d images at %s."%(no_of_images, start_time.strftime("%H:%M:%S"))
    batch_size = int(math.ceil(no_of_images/allowed_processes))

    image_path_batches = getListAsChunks(image_path_list, batch_size)
    process_ids = range(allowed_processes)
    lock = Lock()
    process_list = [Process(target=stripBGInBatches, args=(image_path_batch, lock, process_id, output_path, 30)) for process_id,image_path_batch in zip(process_ids,image_path_batches)]
    lock.acquire()
    print "Processes are going on......"
    lock.release()
    for process_object in process_list:
        process_object.start()
    for process_object in process_list:
        process_object.join()
    print "Processes are done. Time Taken: %ds for %d processes...."%((datetime.datetime.now()-start_time).seconds, allowed_processes)
    print "Average time per image : %fs"%((datetime.datetime.now()-start_time).seconds/no_of_images)


    
if __name__ == "__main__":
    print "Don't use the Main Function."