import base64
from io import BytesIO
import time
from python.samples.samplebase import SampleBase
from python.rgbmatrix import graphics
from PIL import Image
import json
import cv2

with open("emojis.json","r") as emojis_file:
    emojis = json.load(emojis_file)

base64_string = emojis["U+1F600"].partition("data:image/png;base64,")[2]
my_text = "Hello!"

class ImageScroller(SampleBase):
    def __init__(self, *args, **kwargs):
        super(ImageScroller, self).__init__(*args, **kwargs)

    def run(self):

        # prepare text
        font = graphics.Font()
        font.LoadFont("./fonts/10x20.bdf")
        textColor = graphics.Color(255, 105, 180) # barbie pink!

        # prepare emoji
        image_data = base64.b64decode(base64_string)
        image_stream = BytesIO(image_data)
        image = Image.open(image_stream).convert('RGBA')
        pixels = image.getdata()
        new_pixels = [(r, g, b) if a != 0 else (0, 0, 0) for r, g, b, a in pixels]
        img_rgb = Image.new("RGB", image.size)
        img_rgb.putdata(new_pixels)
    
        img_rgb = img_rgb.resize((16, 16), Image.ANTIALIAS)

        img_width, img_height = img_rgb.size

        canvas = self.matrix.CreateFrameCanvas()
        

        # let's scroll
        xpos = canvas.width
        while True:
            canvas.Clear()
            text_len = graphics.DrawText(canvas, font, xpos,22, textColor, my_text)
            canvas.SetImage(img_rgb, xpos + text_len + 2, 5)
            xpos -= 1

            if (xpos + text_len + 2 + img_width < 0):
                xpos = canvas.width

            canvas = self.matrix.SwapOnVSync(canvas)
            time.sleep(0.05)

# Main function
# e.g. call with
#  sudo ./image-scroller.py --chain=4
# if you have a chain of four
if __name__ == "__main__":
    image_scroller = ImageScroller()
    if (not image_scroller.process()):
        image_scroller.print_help()
