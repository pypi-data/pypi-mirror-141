import glob
from PIL import Image
from io import BytesIO


def make_gif(frame_folder,duration = 400, loop = 0):
	frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*")]
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

# if __name__ == "__main__":
#     bytesio_object= make_gif("../test")
    
#     with open("pil_image.gif", "wb") as f:
#     	f.write(bytesio_object.getbuffer())
#     frames = [Image.open(image) for image in glob.glob(f"{'../test'}/*")]
#     bytesio_object = frame_gif(frames)
#     with open("pil_image1.gif", "wb") as f:
#     	f.write(bytesio_object.getbuffer())