import base64
from io import BytesIO
import time
from python.samples.samplebase import SampleBase
from PIL import Image
import json
import cv2
import np

with open("emojis.json","r") as emojis_file:
    emojis = json.load(emojis_file)

base64_string = emojis["U+1F600"].partition("data:image/png;base64,")[2]

class ImageScroller(SampleBase):
    def __init__(self, *args, **kwargs):
        super(ImageScroller, self).__init__(*args, **kwargs)

    def run(self):
        image_data = base64.b64decode(base64_string)
        image_stream = BytesIO(image_data)
        image = Image.open(image_stream).convert('RGB')
        cv2_im = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        cv2_im[np.where(cv2_im[:, :, 3] == 0)] = (0, 0, 0, 255)
        final_im = Image.fromarray(cv2_im)
        final_im.resize((self.matrix.width, self.matrix.height), Image.ANTIALIAS)

        double_buffer = self.matrix.CreateFrameCanvas()
        img_width, img_height = image.size

        # let's scroll
        xpos = 0
        while True:
            xpos += 1
            if (xpos > img_width):
                xpos = 0

            double_buffer.SetImage(image, -xpos)
            double_buffer.SetImage(image, -xpos + img_width)

            double_buffer = self.matrix.SwapOnVSync(double_buffer)
            time.sleep(0.01)

# Main function
# e.g. call with
#  sudo ./image-scroller.py --chain=4
# if you have a chain of four
if __name__ == "__main__":
    image_scroller = ImageScroller()
    if (not image_scroller.process()):
        image_scroller.print_help()
