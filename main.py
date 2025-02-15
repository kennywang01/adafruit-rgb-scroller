import time
from collections import deque
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
            spacing = 0

            for drawing in drawings:
                drawing.set_xpos(xpos + spacing)

                # check if drawing is in frame
                spill_left = drawing.xpos < 0
                spill_right = drawing.xpos > canvas.width
                in_frame = not (spill_left or spill_right)

                if in_frame:
                    drawing.draw(canvas)
                    spacing += drawing.length + EMOJI_TEXT_SPACING
                elif spill_right:
                    # we don't need to look at rest of drawings out of frame
                    break


            # length is sum of lengths of text and emojis altogether, and space between emoji and text
            # total_len = sum([drawing.length for drawing in in_frame_drawings]) + EMOJI_TEXT_SPACING*(len(drawings)-1)

            # scroll content left
            xpos -= 1

            # if last drawing spill left, go back to right side
            if (drawings[-1].xpos or canvas.width) + (drawing[-1].length or 1) < 0:
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
