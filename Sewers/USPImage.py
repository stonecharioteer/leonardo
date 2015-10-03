from PIL import Image, ImageFilter, ImageQt
import PIL
from PyQt4.QtGui import QImage

class USPImage:
    def __init__(self, fsn, product_image_path, icon_data, background_image_path, brand_name, output_path, **kwargs):
        """
        Initializes the USPImage object. It also runs a preliminary preparation algorithm.
        """
        self.fsn = fsn
        self.product_image_path = product_image_path
        self.icon_data = icon_data
        self.background_image_path = background_image_path
        self.brand_name = brand_name
        self.output_path = output_path
        aspect_ratio = [9,14]
        image_width = 1800
        resize_reference = 0
        resize_factor = 0.5
        color_strip_algorithm = 0        
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

        self.prepareCanvas(aspect_ratio, image_width)
        self.loadBackgroundImage()
        self.prepareProductImage(resize_reference, resize_factor, color_strip_algorithm)
        self.prepareIcons()
        self.calculatePositions()
        if not self.detectOverlaps(): self.applyLayout()

    def prepareCanvas(self, aspect_ratio, image_width):
        """Prepares a canvas for plotting the image. 
        This canvas's size is the limiting factor for the entire image."""
        pass
    
    def loadBackgroundImage(self):
        """Opens the background image and resizes it to suit the size of the canvas."""
        pass

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



