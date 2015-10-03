from __future__ import division
import math
import os
import datetime
import glob
import random
import numpy as np
import pandas as pd
from PIL import Image, ImageFilter, ImageQt
import PIL
from PyQt4.QtGui import QImage

import Katana


class USPImage:
    def __init__(self, fsn, category, product_image_path, icon_data, background_image_path, brand_name, image_repository_path, output_path, **kwargs):
        """
        Initializes the USPImage object. It also runs a preliminary preparation algorithm.
        1. fsn, is the Flipkart Serial Number.
        2. Category serves two purposes. First, it is indicative of what category we're running.
        Second, it should have a folder within the Icon Repository, containing all the required icons.
        3. product_image_path is the exact product image that needs to be used. This should be contained
        within in the repository folder.
        4. icon_data is a list of dictionaries with this structure.
            [
                {
                    "Attribute": "Attribute name, and the icon basename.",
                    "Icon Image Path": "Path to the icon. If this is None, then the algorithm assumes there 
                                    will be one in the category's icon repository folder.",
                    "Description": "Text one would like to see below the icon. Of course, None will force 
                                    the same text as the attribute itself."
                }
            ]
        5. background_image_path: This can be either the path to the background_image, "Random", or an RGB value.
        If "Random", the algorithm will pick a random background from those available in the repo.
        If an RGB value, the algorithm will create a background palette from the color.
        6. brand_name is the name of the brand. This helps the algorithm pick a brand logo from the repo.
        If there's no available brand logo, the algorithm picks just the FK logo.
        7. image_repository_path is the path to the repository. It should have the following structure:
            repository:
                    \Icons
                    \Parent Images
                    \Brands
                    \Shapes
                    \Background Images
        """
        self.fsn = fsn
        self.category = category
        self.vertical = fsn[:3]
        self.image_repository_path = image_repository_path
        self.product_image_path = product_image_path
        self.icon_data = icon_data
        self.output_path = output_path
        aspect_ratio = [9,14]
        image_width = 1800
        resize_reference = 0
        resize_factor = 0.5
        color_strip_algorithm = 0
        icon_colors = None
        icon_text_color = [0, 0, 0]
        icon_shape = None
        use_category_specific_backgrounds = False
        icon_text_inside_shape = False
        preserve_icon_colors = False

        if kwargs is not none:
            if "aspect_ratio" in kwargs.keys():
                aspect_ratio = kwargs["aspect_ratio"]
            if "image_width" in kwargs.keys():
                image_width = kwargs["image_resolution"]
            if "resize_reference" in kwargs.keys():
                resize_reference = kwargs["resize_reference"]
            if "resize_factor" in kwargs.keys()
                resize_factor = kwargs["resize_factor"]
            if "color_strip_algorithm" in kwargs.keys():
                color_strip_algorithm = kwargs["color_strip_algorithm"]
            if "icon_colors" in kwargs.keys():
                icon_colors = kwargs["icon_colors"]
            if "icon_text_color" in kwargs.keys():
                icon_text_color = kwargs["icon_text_color"]
            if "icon_shape" in kwargs.keys():
                icon_shape = kwargs["icon_shape"]
            if "use_category_specific_backgrounds" in kwargs.keys():
                use_category_specific_backgrounds = kwargs["use_category_specific_backgrounds"]
            if "icon_text_inside_shape" in kwargs.keys():
                icon_text_inside_shape = kwargs["icon_text_inside_shape"]
            if "preserve_icon_colors" in kwargs.keys():
                preserve_icon_colors = kwargs["preserve_icon_colors"]


        self.prepareCanvas(aspect_ratio, image_width)
        self.loadBackgroundImage(background_image_path)
        self.prepareProductImage(resize_reference, resize_factor, color_strip_algorithm)
        self.prepareIcons()
        self.prepareFSNBrandLogo(brand_name)
        self.resizeAllObjects()
        self.calculatePositions()
        if not self.detectOverlaps(): self.applyLayout()
        self.saveImage()

    def prepareCanvas(self, aspect_ratio, image_width):
        """Prepares a canvas for plotting the image. 
        This canvas's size is the limiting factor for the entire image."""
        image_height = math.ceil(image_width*aspect_ratio[1]/aspect_ratio[0])
        canvas_size = (int(image_width), int(image_height))
        self.canvas = Image.new("RGBA", canvas_size, (255,255,255,255))
        
    def loadBackgroundImage(self, background_path, use_category_specific_backgrounds):
        """Opens the background image."""
        if use_category_specific_backgrounds:
            search_string = os.path.join(self.image_repository_path,"Images","Backgrounds","*%s*%s.*"%(category.replace(" ","*"),fsn[:3].replace(" ","*")))
            backgrounds = glob.glob(search_string)
            if len(backgrounds) == 0:
                backgrounds = glob.glob(os.path.join(self.image_repository_path, "Images", "Backgrounds", "*%s.*"%category.replace(" ","*")))
            background_path =  backgrounds[0]
        else:
            if background_path == "Random":
                backgrounds = glob.glob(os.path.join(os.getcwd(), "Images", "Backgrounds", "Background*.*"))
                background_path = random.choice(backgrounds)
        if type(background_path) is not tuple: #IF the path isn't an RGBA
            self.background_image = Image.open(background_path).convert("RGBA")
        else: #If the path is actually an RGB value
            background_color = [color for color in background_path]
            if len(background_color) == 3: background_color.append(255)
            self.background_image = Image.new("RGBA", self.canvas.size, background_color)

    def prepareProductImage(self, resize_reference, resize_factor, color_strip_algorithm, **kwargs):
        """
        * resize_reference can be 0 or 1.
            0. Height
            1. Width
        * resize_factor is a percentage, specified from 0.00 to 1.00. Of course, 1.00 = 100%.
        * color_strip_algorithm can be 0,1,2 or 3. 
            0 leaves the image as is, 
            1 uses the simple strip algorithm. 
            2 uses a primitive edge detection algorithm. 
            3. If I can implement Canny Edge Detection, then 3 will use that.
        * The keyword arguments (kwargs) are necessary when using the primitive edge detection algorithm.
        These include:
            1. threshold
            2. Nothing else for now.
        """
        #self.original_product_image
        #self.color_stripped_product_image
        #self.resized_product_image
        #self.current_product_image
        pass

    def prepareIcons(self):
        pass

    def calculatePositions(self):
        pass
        
    def detectOverlaps(self):
        """
        Checks the occupied area of the canvas. 
        returns True if there's any overlap.
        Returns False if there's none.
        """
        pass

    def applyLayout(self):
        pass

    def tryLayout(self):
        pass

    def saveImage(self):
        pass

    def dumpLayers(self):
        for layer in self.layers:
            layer_name = layer["Name"]
            os.path.makedirs(os.path.join(self.output_path, self.fsn)
            layer_object.save(os.path.join(self.output_path, self.fsn,layer_name+".png"))

    def getPILImage(self):
        """
        Returns the USP Image as a PIL.Image.
        """
        return self.usp_image

    def getQtImage(self):
        """
        Returns the USP Image as a PyQt4.QtGui.QImage.
        """
        return ImageQt.ImageQt(self.getPILImage())
