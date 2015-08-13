from __future__ import division
import csv
import os, glob, datetime, random, math
import numpy as np
import pandas
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import PIL

def prepareAppImage(fsn, category, primary_attribute_data, secondary_attribute_data, parent_image_positioning, icon_positioning, icon_palette, allow_overlap, background_image_path, primary_attribute_relative_size, secondary_attribute_relative_size, bounding_box, use_simple_bg_color_strip, bg_color_strip_threshold, output_location):
    """This method takes one fsn set, and prepares the app-image.
    ALGORITHM:
    1. If the background image is specified, check if Background image exists.
        a. If it doesn't, throw an exception.
    2. Check if the parent image exists.
        a. If it doesn't, throw an exception.
    3. Using the Attribute values for the Primary and Secondary USPs, look in the Images\Repository\Category folder for icons. Check if they're available. If they're not, throw an exception.
    4. Check if the bounding box shape image is available.
        (a) If it's not, throw an exception.
    5. Create an Image instance using the background image. If the background image is set to "Random", then use a random background image from the Images\Backgrounds folder.
    6. Add the parent image to the specified location. Acceptable locations are (i,j) where i,j <= 2. 0, 1, 2 indicate position based on % of the background image. If the parent_image_position value is "Random", then pick one of these randomly.
    7. Calculate the size of the primary and secondary icons based on the relative size factor variables.
    8. Calculate the area of the parent image, and that of the entire image. Using this area, as well as the icon_positioning variable as constraints find locations which can be used for a primary icon.
    9. Place the first primary icon at a random coordinate. Place the bounding box right over the icon and the text below the bounding box. If the palette is non-black, then generate the respective colors and use random colors for the text and icons.
    10. Place subsequent icons at the other locations pulled up by the formula.
    11. Next, calculate the available coordinates at which to place the secondary icons.
    12. After getting the coordinates, place the secondary icons at similar positions as well.
    """
    #    print fsn, category, primary_attribute_data, secondary_attribute_data, parent_image_positioning, icon_positioning, icon_palette, allow_overlap, background_image_path, primary_attribute_relative_size, secondary_attribute_relative_size, bounding_box, output_location
    #Get the primary image path
    parent_image_path = getParentImage(fsn)
    #Get the primary and secondary attribute icons.
    base_image = Image.open(background_image_path).convert("RGB")
    primary_attributes_and_icons_data = getIcons(primary_attribute_data,category,primary_attribute_relative_size, base_image.size)
    secondary_attributes_and_icons_data = getIcons(secondary_attribute_data,category,secondary_attribute_relative_size, base_image.size)
    #Create an image with the background image's proportions.
    #Open the parent image and resize it to 50% of the background_image's height.
    if use_simple_bg_color_strip:
        stripped_parent_image = replaceColorInImage(Image.open(parent_image_path).convert("RGBA"), (255,255,255,255),(0,0,0,0), bg_color_strip_threshold)
    else:
        stripped_parent_image = getStrippedImage(Image.open(parent_image_path).convert("RGBA"), bg_color_strip_threshold)
    parent_image = getResizedImage(stripped_parent_image,0.5,"Height",base_image.size)
    #Based on the input control parameters, get the coordinates for the parent image.
    parent_image_coords = getParentImageCoords(base_image.size,parent_image.size,parent_image_positioning)
    base_image.paste(parent_image,parent_image_coords,parent_image)
    #icon_coords = getIconCoords(primary_attributes_and_icons_data,secondary_attributes_and_icons_data,parent_image_positioning,base_image.size,parent_image.size)
    counter = 0
    icons_and_coordinates = getIconsAndCoordinates(base_image, parent_image, parent_image_coords, primary_attributes_and_icons_data, secondary_attributes_and_icons_data, "Circular","Alternate",allow_overlap)
    for icon in icons_and_coordinates:
        base_image.paste(icon["Icon"],icon["Position"],icon["Icon"])
    #for icon in primary_attributes_and_icons_data:
    #    icon_position = getValidPlacementPoints(base_image.size, parent_image.size, parent_image_coords, None,icon, allow_overlap)
    #    base_image.paste(icon["Icon"],icon_position,icon["Icon"])
    #    #base_image.paste(icon["Icon"],icon_coords[counter],icon["Icon"])
    #    counter +=1
    #counter = 0
    #for icon in secondary_attributes_and_icons_data:
    #    icon_position = getValidPlacementPoints(base_image.size, parent_image.size, parent_image_coords, None,icon, allow_overlap)
    #    base_image.paste(icon["Icon"],icon_position,icon["Icon"])
    #    counter +=1
    #Randomizer method.
    #base_image.paste(primary_attributes_and_icons_data[0]["Icon"],icon_position,primary_attributes_and_icons_data[0]["Icon"])
    image_path = os.path.join("Output",fsn+"_app_image.png")
    base_image.save(image_path)
    return image_path

def getIconsAndCoordinates(base_image, parent_image, parent_image_coords, primary_attributes_and_icons_data, secondary_attributes_and_icons_data, icon_arrangement,ordering,allow_overlap):
    width_parent, height_parent = parent_image.size
    x_top_left_parent, y_top_left_parent = parent_image_coords
    x_center_parent, y_center_parent = (x_top_left_parent + width_parent/2), (y_top_left_parent + height_parent/2)
    primary_icons = [icon["Icon"] for icon in primary_attributes_and_icons_data]
    secondary_icons = [icon["Icon"] for icon in secondary_attributes_and_icons_data]
    if ordering == "Separate":
        icon_list = primary_icons + secondary_icons
    elif ordering == "Alternate":
        least_no_of_attributes = min(len(primary_icons),len(secondary_icons))
        max_no_of_attributes = max(len(primary_icons),len(secondary_icons))
        icons_diff = (max_no_of_attributes - least_no_of_attributes)
        icon_list = []
        for i in range(least_no_of_attributes):
            icon_list.append(primary_icons[i])    
            icon_list.append(secondary_icons[i])
        if icons_diff > 0:
            if len(primary_icons) == max_no_of_attributes:
                icon_list.append(primary_icons[(least_no_of_attributes-1):(max_no_of_attributes-1)])
            elif len(primary_icons) == max_no_of_attributes:
                icon_list.append(secondary_icons[(least_no_of_attributes-1):(max_no_of_attributes-1)])
    coordinates_and_icons = []
    origin = (x_center_parent, y_center_parent)
    radius = 0.6*min(base_image.size)
    if icon_arrangement == "Circular":
        #generate circular coordinates.
        counter = 0
        divisions = len(icon_list)
        points = getPointsOnCircle(origin, radius, divisions)
        for icon in icon_list:
            counter +=1
            coord = {
                "Icon": icon,
                "Position": points[counter]
            }
            print points[counter]
            coordinates_and_icons.append(coord)
    return coordinates_and_icons

def getPointsOnCircle(origin, radius, divisions):
    theta_step = (2*math.pi/divisions)
    theta = 0
    points = []
    while (theta <= 2*math.pi):
        points.append(getPointOnCircle(origin, radius, theta))
        theta += theta_step
        print theta
    return points

def getPointOnCircle(origin, radius, theta):
    return (int(origin[0]+radius*math.cos(theta)),int(origin[1]+radius*math.sin(theta)))

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
        x_pos_factor = random.uniform(0.0,1.0)
        y_pos_factor = random.uniform(0.0,1.0)    
    x_pos = int((base_width-parent_width)*x_pos_factor)
    y_pos = int((base_height-parent_height)*y_pos_factor)
    return (x_pos,y_pos)

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
        for icon in images_in_look_in_path:
            if not found_icon:
                if attribute["Attribute"].lower().strip() in icon.lower().strip():
                    icon_with_text = getIconImage(icon, attribute["Description Text"], icon_relative_size, base_image_size)
                    attribute.update({"Icon": icon_with_text})
                    found_icon = True
                else:
                    attribute.update({"Icon": None})
        if not found_icon:
            attributes_without_icons.append(attribute["Attribute"])
    if len(attributes_without_icons) >0:
        print "The following attributes don't have icons. Recommend making them before progressing."
        print attributes_without_icons
    return attribute_data

def getParentImage(fsn):
    try:
        parent_image_path = glob.glob(os.path.join(os.path.join(os.path.join(os.getcwd(),"Images"),"Parent Images"),"%s*.*"%fsn))[0]
    except:
        parent_image_path = os.path.join("essentials","na_parent_image.png")
    return parent_image_path

def getIconImage(icon_path, description_text, icon_relative_size, base_image_size):
    """This method generates an image object which contains the icon image as well as the description text."""
    import textwrap
    clearance_factor_for_text = 2.0
    font_resize_factor = 0.3
    text_as_paragraphs = textwrap.wrap(description_text,width=15)
    #get an image object using the icon path, and resize it to the required dimensions with respect to the height of the base image.
    icon_image = getStrippedImage(getResizedImage(Image.open(icon_path).convert("RGBA"),icon_relative_size,"height",base_image_size), threshold=30)
    #icon_image = replaceColorInImage(resized_icon_image,(255,255,255,255),(0,0,0,255))
    #Create a blank canvas for the text.
    max_w, max_h = 500, 500
    text_canvas = Image.new("RGBA",(max_w, max_h),(0,0,0,0))
    
    draw_text_handle = ImageDraw.Draw(text_canvas)
    font_size = int(icon_image.size[1]*font_resize_factor)
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
        


def main():
    print "Loading Data..."
    with open("raw_data.csv","r") as data_file:
        print "Data file successfully loaded."
        csv_handler = csv.DictReader(data_file)
        parent_image_path = os.path.join("Images","parent_image.png")
        background_image_path = os.path.join("Images","background.png")
        brand_image_path = os.path.join("Images","brand_image.png")

        for row in csv_handler:
            #print row
            fsn = row["FSN"]
            print "Currently processing FSN: %s"%fsn
            primary_usps = []
            secondary_usps = []
            for control_key in row.keys():
                if "Primary USP" in control_key:
                    primary_usps.append(row[control_key])
                elif "Secondary USP" in control_key:
                    secondary_usps.append(row[control_key])
            print "Primary USPS are: ", ", ".join(primary_usps)
            primary_usp_dict_list = [{"USP":usp,"Image":Image.open(os.path.join("Images",usp+".png"))} for usp in primary_usps]
            print "Secondary USPS are: ", ", ".join(secondary_usps)
            secondary_usp_dict_list = [{"USP":usp,"Image":Image.open(os.path.join("Images",usp+".png"))} for usp in secondary_usps]
            print "Processing Background Image"
            background_image = Image.open(background_image_path)
            parent_image = Image.open(parent_image_path)
            brand_image = Image.open(brand_image_path)
            print "Processing Parent Image"
            background_image_width, background_image_height  = background_image.size
            origin_x, origin_y, max_x, max_y = 0, 0, background_image_width, background_image_height
            parent_image_width, parent_image_height = parent_image.size
            resized_parent_image_width = int(0.9*background_image_width)
            resized_parent_image_height = int(resized_parent_image_width*parent_image_height/background_image_width)
            resized_parent_image_size = (resized_parent_image_width, resized_parent_image_height)
            resized_parent_image = parent_image.resize(resized_parent_image_size)
            background_image.paste(resized_parent_image,(int((max_x-resized_parent_image_width)/2),(max_y-resized_parent_image_height)),resized_parent_image)
            background_image.paste(brand_image,(50,50),brand_image)
            
            primary_usp_icon_height = int(0.15*background_image_height)
            primary_usp_locations = [(200,200),(200,1300),(1100,200),(700,700),(1100,1300)]
            counter = 0
            random.shuffle(primary_usp_locations)
            for usp in primary_usp_dict_list:
                temp = usp["Image"]
                callout = usp["USP"]#.toupper()
                temp_icon_width, temp_icon_height = temp.size
                resized_temp_icon_height = primary_usp_icon_height
                resized_temp_icon_width = int(resized_temp_icon_height*temp_icon_width/temp_icon_height)
                resized_temp_icon_size = (resized_temp_icon_width,resized_temp_icon_height)
                resized_temp = temp.resize(resized_temp_icon_size)
                
                temp_location = primary_usp_locations[counter]
                counter+=1
                draw = ImageDraw.Draw(background_image)
                font = ImageFont.truetype("RionaSans-Regular.ttf", 72)
                temp_text_location = (int(temp_location[0]+temp.size[0]*0.25),int(temp_location[1]+temp.size[1]*1.3))
                draw.text(temp_text_location,callout,(0,0,0),font=font)
                background_image.paste(resized_temp,temp_location,resized_temp)
            background_image.show()

def getETA(start_time, counter, total):
    #from __future__ import division
    now = datetime.datetime.now()
    time_spent = now - start_time
    mean_time = time_spent.total_seconds()/counter
    ETA = start_time + datetime.timedelta(seconds=(mean_time*total))
    return ETA

if __name__ == "__main__":
    print "Don't use the Main Function."