import os, math, random, glob, csv
import pandas as pd
import numpy as np
from PIL import Image
if __name__ == """__main__""":
	image_array = Image.new("RGBA",(20,20),color=(255,0,0,255))
	print np.array(image_array)
	image_data_frame = pd.DataFrame.from_records(np.array(image_array))
	print image_data_frame