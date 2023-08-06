# pygif
A Python package to make gif from images and videos

## Usage

Following methods can be utilized to make gif

```
from inrgif.inrgif import images_to_gif, video_to_gif
import glob
from PIL import Image
#from video..
obj = video_to_gif.make_gif("videoplayback.mp4")
images_to_gif.save(obj,"video.gif")

#from folder all images.
#here folder name is test
bytesio_object= images_to_gif.make_gif("test")
images_to_gif.save(bytesio_object,"folder.gif")

#from objects
frames = [Image.open(image) for image in glob.glob(f"{'test'}/*")]
bytesio_object = images_to_gif.frame_gif(frames)
images_to_gif.save(bytesio_object,"frames.gif")

```

To uninstall execute following..

```
pip uninstall geosky-1.0.0

```