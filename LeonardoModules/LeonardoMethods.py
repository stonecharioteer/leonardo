from __future__ import division
import csv
import os
from random import shuffle
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import PIL

def prepareAppImage(fsn, category, primary_attribute_data, secondary_attribute_data, template, positioning, icon_palette, allow_overlap,background_image_path, primary_attribute_relative_size, secondary_attribute_relative_size, output_location):
    """This method takes one fsn set, and prepares the app-image."""

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