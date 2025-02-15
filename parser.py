import emoji
from drawings import TextDrawing, EmojiDrawing

def parse_emoji_text(text):
    split_text = emoji.get_emoji_regexp().split(text)
    drawings = []

    for i,t in enumerate(split_text):
        if not t: # skip empty strings
            continue

        elif emoji.is_emoji(t):
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
