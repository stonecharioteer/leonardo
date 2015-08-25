import os
import glob
import datetime
from PIL import Image
import Katana

def cleanImagesInPath(path_to_images_folder=None):
    if path_to_images_folder is None:
        print "Cannot operate without an absolute or relative path. I recommend using the interactive python module and passing a path combined via os.path.join."
    else:
        images_in_folder = glob.glob(os.path.join(path_to_images_folder,"*.*"))
        total = len(images_in_folder)
        print "Going to process %d images" %total
        counter = 0
        start_time = datetime.datetime.now()
        for image_name in images_in_folder:
            isImage = (".jpg" in image_name) or (".png" in image_name) or (".jpeg" in image_name)
            if isImage:
                stripped_image = Katana.getStrippedImage(Image.open(image_name).convert("RGBA"),threshold=30)
                new_image_name = os.path.join(image_name[:image_name.find(os.path.basename(image_name))],os.path.splitext(os.path.basename(image_name))[0])+".png"
                stripped_image.save(new_image_name)
                counter+=1
                eta = Katana.getETA(start_time, counter, total)
                print "Processed %d of %d. ETA: %s" %(counter, total, eta.strftime("%a %d-%m, %H:%M:%S"))
            else:
                print "Skipped %s." %image_name
        print "Completed %d images at %s."%(counter,datetime.datetime.now().strftime("%a %d-%m, %H:%M:%S"))

if __name__ == "__main__":
    print "This module isn't designed to be run through Main."