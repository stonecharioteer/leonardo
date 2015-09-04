import os, math, random, glob, csv
import pandas as pd
import numpy as np
from PIL import Image
if __name__ == """__main__""":
	#image_array = Image.new("RGBA",(20,20),color=(255,0,0,255))
	#print np.array(image_array)
	#image_data_frame = pd.DataFrame.from_records(np.array(image_array))
	#print image_data_frame
	data = [
			[(255,255,255,255),(255,255,255,255),(200,255,255,255),(200,255,255,255)],
			[(255,255,255,255),(200,255,255,255),(200,255,255,255),(255,200,255,255)],
			[(200,255,255,255),(200,255,255,255),(200,200,255,255),(255,255,200,255)],
			[(199,255,255,255),(200,255,255,255),(255,200,255,255),(255,200,255,255)],
			[(198,255,255,255),(200,255,255,255),(255,255,255,255),(255,255,255,255)],
			[(255,255,255,255),(255,255,255,255),(255,255,255,255),(255,255,255,255)],
			[(255,255,255,255),(255,255,255,255),(255,255,255,255),(255,255,255,255)],
		]
	data_frame = pd.DataFrame.from_records(np.array(data))
	print data_frame
	r_limit, g_limit, b_limit = 200, 200, 200
	condition = [True if ((cell[0] <= r_limit) or (cell[1] <= g_limit) or (cell[2] <= b_limit)) else False for cell in data_frame[0]]
	print condition

	indices =  list(data_frame[0].ix[condition].index)
	print indices
	#data_frame[0].set_value(indices[0],0,(200,255,255,0))
	#data_frame[0].set_value(indices[0],0,(200,255,255,0))
	#data_frame[0].set_value(indices[-1],0,(200,255,255,0))
	data_frame[0].loc[indices[-1]] = (200,255,255,0)


	print np.array(data_frame)