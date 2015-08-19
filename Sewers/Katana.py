from __future__ import division
import csv
import os, glob, datetime, random, math
import numpy as np
import pandas
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import PIL


def getBackgroundImage(background_path):
    import random, os
    from PIL import Image
    if background_path == "Random":
        backgrounds = glob.glob(os.path.join(os.path.join(os.path.join(os.getcwd(),"Images"),"Backgrounds"),"Background*.*"))
        background_path = random.choice(backgrounds)
    return Image.open(background_path).convert("RGBA").resize((1800,3200))

def getIconsAndCoordinates(base_image, parent_image, parent_image_coords, primary_attributes_and_icons_data, secondary_attributes_and_icons_data, icon_arrangement,ordering,parent_image_positioning):#allow_overlap
    import random, os, math
    #First, store the parameters in an easily-readable manner.
    #Parent image dimensions
    width_parent, height_parent = parent_image.size
    #Parent image top left corner coordinates.
    x_top_left_parent, y_top_left_parent = parent_image_coords
    #Parent image center coordinates.
    x_center_parent, y_center_parent = (x_top_left_parent + width_parent/2), (y_top_left_parent + height_parent/2)
    #get base image size
    width_base, height_base = base_image.size
    #Seggregate the primary and secondary icons.
    primary_icons = [icon["Icon"] for icon in primary_attributes_and_icons_data]
    secondary_icons = [icon["Icon"] for icon in secondary_attributes_and_icons_data]
    #Split the operation based on whether the ordering is separate or alternate.
    if ordering == "Separate":
        #Primary and secondary icon lines and arrangement is to be kept separate.
        #Determine the kind of parent_image_alignment, based on the original parameter.
        if (parent_image_positioning in [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)]): #Club this with other corner-based positions.
            #parent image is placed at the top-left corner
            if icon_arrangement == "Circular":
                #icons are to be arranged in arcs.
                if parent_image_positioning == (0.0,0.0):
                    primary_radius_multiplier = 0.65
                    secondary_radius_multiplier = 1.0
                    theta_range = ((0),(math.pi*0.5)) #~0deg and ~90deg.
                    primary_theta_range = (theta_range[0]-25*math.pi/180,theta_range[1]+25*math.pi/180)
                    primary_arc_center = (x_top_left_parent, y_center_parent)
                    secondary_theta_range = (theta_range[0]+45*math.pi/180,theta_range[1]+5*math.pi/180)
                elif parent_image_positioning == (1.0,0.0):
                    primary_radius_multiplier = 0.65
                    secondary_radius_multiplier = 1.1
                    theta_range = ((math.pi*0.5),(math.pi)) #~90deg and ~180deg.
                    primary_theta_range = (theta_range[0]+10*math.pi/180,theta_range[1]+45*math.pi/180)
                    primary_arc_center = (x_center_parent, y_center_parent)
                    secondary_theta_range = (theta_range[0]+2*math.pi/180,theta_range[1]-35*math.pi/180)
                elif parent_image_positioning == (0.0,1.0):
                    primary_radius_multiplier = 0.76
                    secondary_radius_multiplier = 1.15
                    theta_range = ((math.pi*1.5),(math.pi*2.0)) #270deg and ~360deg.
                    primary_theta_range = (theta_range[0],theta_range[1]+20*math.pi/180)
                    primary_arc_center = (x_top_left_parent, y_center_parent)
                    secondary_theta_range = (theta_range[0]-2*math.pi/180,theta_range[1]-38*math.pi/180)
                elif parent_image_positioning == (1.0, 1.0):
                    primary_radius_multiplier = 0.95
                    secondary_radius_multiplier = 1.35
                    theta_range = ((math.pi),(math.pi*1.5)) #180deg and ~270deg.
                    primary_theta_range = (theta_range[0]-5*math.pi/180,theta_range[1]+1*math.pi/180)
                    primary_arc_center = (x_top_left_parent+width_parent, y_center_parent)
                    secondary_theta_range = (theta_range[0]+40*math.pi/180,theta_range[1]-5*math.pi/180)
                
                primary_plot_points_required = len(primary_icons)
                parent_extreme_point = (x_top_left_parent+width_parent, y_top_left_parent+height_parent)
                diagonal_length = width_base
                #diagonal_length = getDistanceBetweenPoints(primary_arc_center,parent_extreme_point)
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
            #parent image is placed at the top-middle.
            if icon_arrangement == "Circular":
                #icons are to be arranged in arcs.
                pass
            elif icon_arrangement == "Rectangular":
                #icons are to be laid out in arrays.
                pass
            else:
                print "Invalid icon arrangement passed to Katana. Icon Arrangement asked for is %s"%icon_arrangement
        elif parent_image_positioning == (0.5,0.5):
            #parent image is placed at the top-right.
            if icon_arrangement == "Circular":
                #icons are to be arranged in arcs.
                pass
            elif icon_arrangement == "Rectangular":
                #icons are to be laid out in arrays.
                pass
            else:
                print "Invalid icon arrangement passed to Katana. Icon Arrangement asked for is %s"%icon_arrangement
        else:
            print "Parent image positioning hint isn't valid. %r" %parent_image_positioning
    return coordinates_and_icons


def getValidPoints(points, divisions, base_image_size):
    """Given a list of points and the number of points required, it'll return only those 
    points that're within a bounding box dictated by a (max_x, max_y) 
    value obtained from PIL.Image.Image.size"""
    import random
    max_x, max_y = base_image_size
    counter = 1
    random.shuffle(points)
    valid_points = []
    while len(valid_points) <= divisions:
        for point in points:
            point_x, point_y = point
            if (0 <= point_x <= max_x) and (0 <= point_y <= max_y):
                valid_points.append(point)
    return valid_points
    
def getPointsOnCircle(origin, radius, divisions):
    return getPointsOnArc(origin, radius, divisions, (0,2*math.pi)) #What is a circle, but an arc between 0 and 2*Pi?

def getPointOnCircle(origin, radius, theta):
    return (int(origin[0]+radius*math.cos(theta)),int(origin[1]+radius*math.sin(theta)))

def getPointsOnArc(origin, radius, divisions, theta_range):
    theta_max = max(theta_range)
    theta = min(theta_range)
    theta_step = ((theta_max-theta)/divisions)
    points = []
    while (theta <= theta_max):
        points.append(getPointOnCircle(origin, radius, theta))
        theta += theta_step
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

def replaceColorInImage(image, original_colour, replacement_color, threshold):
    import numpy as np
    image_data = np.array(image)
    #print image.size
    #print image_data.shape
    #raw_input("Waiting!")
    rows, columns,rgba = image_data.shape
    original_r, original_g, original_b, original_a = original_colour
    for row in range(rows):
        for column in range(columns):
            pixel = image_data[row][column]
            pixel_red, pixel_green, pixel_blue, pixel_alpha = pixel
            if ((original_r-threshold)<=pixel_red<=(original_r+threshold)) and ((original_g-threshold)<=pixel_green<=(original_g+threshold)) and ((original_b-threshold)<=pixel_blue<=(original_b+threshold)):
                image_data[row][column] = replacement_color
#    image_data[(image_data == original_colour).all(axis=-1)] = replacement_color
    #image_data[(min_color <=image_data <= max_colour).all(axis=-1)] = replacement_color
    return Image.fromarray(image_data,mode="RGBA")

def getStrippedImage(image, threshold):
    """This method removes the background color of the image."""
    import numpy as np
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
    return stripped_image

def getIconCoords(primary_attributes_and_icons_data, secondary_attributes_and_icons_data, parent_image_positioning, base_image_size, parent_image_size):
    coords_list = []
    current_x = -50
    current_y = int(0.10*base_image_size[1])
    for icon in primary_attributes_and_icons_data:
        coords_list.append((current_x,current_y))
        current_x += int(0.20*base_image_size[0])
    current_x = int(0.18*base_image_size[0])
    current_y = int(base_image_size[1]*0.8)
    for icon in secondary_attributes_and_icons_data:
        coords_list.append((current_x,current_y))
        current_x += int(0.1*base_image_size[0])
    return coords_list

def getResizedImage(image_to_resize,resize_factor,resize_by,base_image_size):
    image_to_resize_original_width, image_to_resize_original_height = image_to_resize.size
    base_image_width, base_image_height = base_image_size
    if resize_by == "Width":
        resized_width = resize_factor*base_image_width
        resized_height = image_to_resize_original_height*resized_width/image_to_resize_original_width
    else:
        resized_height = resize_factor*base_image_height
        resized_width = image_to_resize_original_width*resized_height/image_to_resize_original_height
    resized_dimensions = (int(resized_width),int(resized_height))
    resized_image = image_to_resize.resize(resized_dimensions)
    return resized_image

def getParentImageCoords(base_image_size, parent_image_size, parent_image_positioning):
    base_width, base_height = base_image_size
    parent_width, parent_height = parent_image_size
    if parent_image_positioning != "Random":
        x_pos_factor, y_pos_factor = parent_image_positioning
    else:
        x_pos_factor = rangedom.uniform(0.0,1.0)
        y_pos_factor = random.uniform(0.0,1.0)    
    x_pos = int((base_width-parent_width)*x_pos_factor)
    y_pos = int((base_height-parent_height)*y_pos_factor)
    return (x_pos,y_pos)

def getParentImage(fsn):
    try:
        parent_image_path = glob.glob(os.path.join(os.path.join(os.path.join(os.getcwd(),"Images"),"Parent Images"),"%s*.*"%fsn))[0]
    except:
        parent_image_path = os.path.join("essentials","na_parent_image.png")
    return parent_image_path

def getIcons(attribute_data, category, icon_relative_size, base_image_size):
    #print attribute_data, category
    look_in_path = os.path.join(os.path.join(os.path.join(os.getcwd(),"Images"),"Repository"),category)
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
                if attribute["Attribute"].lower().strip() in icon.lower().strip():
                    icon_with_text = getIconImage(icon, attribute["Description Text"], icon_relative_size, base_image_size)
                    attribute.update({"Icon": icon_with_text})
                    found_icon = True
                    #attribute.update({"Icon": None})
            else:
                #If it has already found an icon, do nothing.
                break
        if not found_icon:
            na_icon_path = os.path.join("essentials","icon_na.png")
            icon_with_text = getIconImage(na_icon_path, attribute["Description Text"], icon_relative_size, base_image_size)
            attribute.update({"Icon": icon_with_text})
            attributes_without_icons.append(attribute["Attribute"])
    if (len(attributes_without_icons) > 0):
        print "The following %s attributes don't have icons. Recommend making them before progressing." %category
        print attributes_without_icons
        print "Looking in the %s folder."%image_search_path
    return attribute_data

def checkIcon(attribute,description):
    return True

def getIconImage(icon_path, description_text, icon_relative_size, base_image_size):
    """This method generates an image object which contains the icon image as well as the description text."""
    import textwrap
    clearance_factor_for_text = 2.0
    font_resize_factor = 0.3
    text_as_paragraphs = textwrap.wrap(description_text,width=10)
    #get an image object using the icon path, and resize it to the required dimensions with respect to the height of the base image.
    #Don't strip for now.
    #icon_image = getStrippedImage(getResizedImage(Image.open(icon_path).convert("RGBA"),icon_relative_size,"height",base_image_size), threshold=30)
    icon_image = getResizedImage(Image.open(icon_path).convert("RGBA"),icon_relative_size,"height",base_image_size)
    #icon_image = replaceColorInImage(resized_icon_image,(255,255,255,255),(0,0,0,255))
    #Create a blank canvas for the text.
    max_w, max_h = 500, 500
    text_canvas = Image.new("RGBA",(max_w, max_h),(0,0,0,0))
    
    draw_text_handle = ImageDraw.Draw(text_canvas)
    #font_size = int(icon_image.size[1]*font_resize_factor)
    font_size = 84 #Set default font size for now.
    font = ImageFont.truetype(os.path.join("essentials","RionaSans-Regular.ttf"), font_size)
    
    current_h, pad = 0, 10
    #Ref: http://stackoverflow.com/questions/1970807/center-middle-align-text-with-pil
    for line in text_as_paragraphs:
        w, h = draw_text_handle.textsize(line, font=font)
        draw_text_handle.text(((int((max_w-w)/2)), current_h), line, (0,0,0), font=font)
        current_h += h + pad
    
    #merge both images now.
    final_canvas_width = text_canvas.size[0] if text_canvas.size[0] >= icon_image.size[0] else icon_image.size[0]
    final_canvas_height = text_canvas.size[1] + icon_image.size[1] + pad

    final_canvas = Image.new("RGBA",(final_canvas_width, final_canvas_height))
    icon_x = int((final_canvas.size[0]-icon_image.size[0])/2)
    icon_y = 0
    icon_position = (icon_x, icon_y)
    text_x = int((final_canvas.size[0]-text_canvas.size[0])/2)
    text_y = int(final_canvas.size[1]-text_canvas.size[1])
    text_canvas_position = (text_x, text_y)
    final_canvas.paste(icon_image, icon_position, icon_image)
    final_canvas.paste(text_canvas, text_canvas_position, text_canvas)

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
    path_to_repo = os.path.join(os.getcwd(),os.path.join("Images","Repository"))
    path_and_folders_list = glob.glob(os.path.join(path_to_repo,"*"))

    return [os.path.basename(path_and_folder_name) for path_and_folder_name in path_and_folders_list]

if __name__ == "__main__":
    print "Don't use the Main Function."