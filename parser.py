import emoji
from drawings import TextDrawing, EmojiDrawing
import functools
import operator
import re

def tokenize(text):
    # tokenize text, whitespace, and emojis
    whitespace_re = re.compile(r'(\S+)')
    split_emoji = emoji.get_emoji_regexp().split(text)
    split_whitespace = [list(whitespace_re.split(substr)) for substr in split_emoji]
    tokens = functools.reduce(operator.concat, split_whitespace)
    return [t for t in tokens if t]  # ignore empty strings

def parse_emoji_text(text):
    tokens = tokenize(text)
    drawings = []

    for i,t in enumerate(tokens):
        if emoji.is_emoji(t):
        # collect all unicode chars which make up emoji
            emoji_unicode_chars = []

            for char in t:
                emoji_unicode_chars.append(f"U+{ord(char):04X}")

            emoji_unicode_text = " ".join(emoji_unicode_chars)
            emoji_drawing = EmojiDrawing(emoji_unicode_text)
            drawings.append(emoji_drawing)

        else:
            text_drawing = TextDrawing(t)
            drawings.append(text_drawing)
        
    return drawings

if __name__ == "__main__":
    print(tokenize("😍Hello 👪  🇲🇶world!"))