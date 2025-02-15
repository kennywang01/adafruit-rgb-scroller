from abc import ABC, abstractmethod
from python.rgbmatrix import graphics
import json
import base64
from PIL import Image
from io import BytesIO

# y pos constant so content scrolls through middle
IMAGE_Y_POS = 6
TEXT_Y_POS = 22

# more constants for consistent visuals
EMOJI_DIMENSION = 16
FONT_COLOR = graphics.Color(255, 105, 180) # hot pink!

with open("emojis.json","r") as emojis_file:
    emoji_images = json.load(emojis_file)

class Drawing(ABC):
    length: int
    xpos: int

    @abstractmethod
    def __init__(self, content):
        pass
    
    @abstractmethod
    def draw(self, canvas):
        pass
    
    def set_xpos(self, xpos):
        self.xpos = xpos

class TextDrawing(Drawing):

    def  __init__(self, content):
        self.text = content
        self.length = None # length is given by graphics driver
        self.xpos = None

    def draw(self, canvas):
        font = graphics.Font()
        font.LoadFont("./fonts/10x20.bdf")
        self.length = graphics.DrawText(canvas, font, self.xpos, TEXT_Y_POS, FONT_COLOR, self.text)

class EmojiDrawing(Drawing):

    def __init__(self, content):
        # content must be unicode string and valid key for emojis.json
        base64_string = emoji_images[content].partition("data:image/png;base64,")[2]
        image_data = base64.b64decode(base64_string)
        image_stream = BytesIO(image_data)
        image = Image.open(image_stream).convert('RGBA')
        pixels = image.getdata()
        new_pixels = [(r, g, b) if a != 0 else (0, 0, 0) for r, g, b, a in pixels]
        img_rgb = Image.new("RGB", image.size)
        img_rgb.putdata(new_pixels)
        img_rgb = img_rgb.resize((EMOJI_DIMENSION, EMOJI_DIMENSION), Image.ANTIALIAS)

        self.emoji = img_rgb
        self.length = EMOJI_DIMENSION
        self.xpos = None

    def draw(self, canvas):
        canvas.SetImage(self.emoji, self.xpos, IMAGE_Y_POS)