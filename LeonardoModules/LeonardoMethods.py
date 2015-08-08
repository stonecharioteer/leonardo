from __future__ import division
import csv
import os
from random import shuffle
import numpy as np
import pandas
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import PIL

def prepareAppImage(fsn, category, primary_attribute_data, secondary_attribute_data, parent_image_positioning, icon_positioning, icon_palette, allow_overlap, background_image_path, primary_attribute_relative_size, secondary_attribute_relative_size, bounding_box, output_location):
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

    

def getValidPlacementPoints(image_base_size, parent_image_size, past_icons_data, new_icon_data, allow_overlap):
    """This method calculates valid positions for icons."""

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
            shuffle(primary_usp_locations)
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

if __name__ == "__main__":
    main()