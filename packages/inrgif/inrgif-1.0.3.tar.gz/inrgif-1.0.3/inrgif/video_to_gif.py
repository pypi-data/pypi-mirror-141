import cv2
from sklearn.metrics import mean_squared_error
from math import sqrt
import numpy as np
import traceback as tb

from PIL import Image
from io import BytesIO


def frame_gif(frames,duration = 400, loop = 0):
	#print(frames)
	new_width  = 1000
	new_height = 1000
	frames = [img.resize((new_width, new_height), Image.ANTIALIAS) for img in frames]
	print(frames)
	frame_one = frames[0]
	fobj = BytesIO()
	frame_one.save(fobj, format="GIF", append_images=frames,
               save_all=True, duration=duration, loop=loop)
	return fobj
def save(obj,path = 'pil_image.gif' ):
	with open(path, "wb") as f:
		f.write(obj.getbuffer())


def make_gif(video_path ):
	cap = cv2.VideoCapture(video_path)
	# Check if camera opened successfully
	if (cap.isOpened()== False): 
	  print("Error opening video  file")
	farmes_list = list()
	while(cap.isOpened()):
		ret, frame = cap.read()
		ret, frame = cap.read()
		if ret == True:
			farmes_list.append(frame)
		else:
			break
		

	print(f'length of the frame list is= {len(farmes_list)}')
	i = 0
	new_frame = list()
	for img in farmes_list:
		try:
			frame = img
			# Open image in bwDir - The searched image
			searchedImageBw = np.array(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
			# Open image to be compared
			inx = i
			if inx != len(farmes_list):
				cmpImage = np.array(cv2.cvtColor(farmes_list[inx+1], cv2.COLOR_BGR2GRAY))
				rms = sqrt(mean_squared_error(searchedImageBw, cmpImage))
				#print(f'rms= {rms}')
				if rms>3:
					#farmes_list.remove(frame)
					new_frame.append(frame)


		except Exception as e:
			#print(e)
			#tb.print_exc()
			pass
		i = i+1
	   

	print(f'length of the frame list is= {len(new_frame)}')

	pil_frames = [ Image.fromarray(img) for img in new_frame]
	bytesio_object = frame_gif(pil_frames)
	#ig.save(bytesio_object, path = "videotogif.gif")
	
	return bytesio_object
