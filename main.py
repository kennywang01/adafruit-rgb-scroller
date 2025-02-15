import time
from python.samples.samplebase import SampleBase
from python.rgbmatrix import graphics
from client import AwsClient
from parser import parse_emoji_text
from PIL import Image
import json
import cv2

EMOJI_TEXT_SPACING = 2

class ImageScroller(SampleBase):
    def __init__(self, *args, **kwargs):
        super(ImageScroller, self).__init__(*args, **kwargs)
        self.client = AwsClient()

    def run(self):
        text = self.client.get_text()
        drawings = parse_emoji_text(text)
        canvas = self.matrix.CreateFrameCanvas()
        xpos = canvas.width

        while True:
            # display content
            canvas.Clear()
            for drawing in drawings:
                drawing.draw(canvas, xpos)

            # length is sum of lengths of text and emojis altogether, and space between emoji and text
            total_len = sum([drawing.length for drawing in drawings]) + EMOJI_TEXT_SPACING*(len(drawings)-1)

            # scroll content left
            xpos -= 1

            # if fallen off screen, go back to right side
            if (xpos + total_len < 0):
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
