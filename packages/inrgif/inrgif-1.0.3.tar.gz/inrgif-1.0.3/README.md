# pygif
A Python package to make gif from images and videos

## Usage

Following methods can be utilized to make gif

```
from inrgif import images_to_gif, video_to_gif
import glob
from PIL import Image
#from video to gif..
obj = video_to_gif.make_gif(video_path="videoplayback.mp4",duration = 400, loop = 0 )
images_to_gif.save(obj,"video.gif")

#from folder all images.
#here folder name is test
bytesio_object= images_to_gif.make_gif(frame_folder="test",duration = 400, loop = 0)
images_to_gif.save(bytesio_object,"folder.gif")

#from PIL objects to gif..
frames = [Image.open(image) for image in glob.glob(f"{'test'}/*")]
bytesio_object = images_to_gif.frame_gif(frames=frames,duration = 400, loop = 0)
images_to_gif.save(bytesio_object,"frames.gif")

```

To uninstall execute following..

```
pip uninstall inrgif

```