def read_messages():
    with open("messages.txt", "r", encoding='utf-8') as f:
        messages = f.readlines()
    return [m.strip() for m in messages]

if __name__ == "__main__":
    # validate messages
    import emoji
    import json
    import re
    import functools
    import operator
    with open("emojis.json","r") as emojis_file:
        emoji_images = json.load(emojis_file)
    messages_text = read_messages()

    def parse_emoji_text(text):
        # tokenize text, whitespace, and emojis
        whitespace_re = re.compile(r'(\S+)')
        split_emoji = emoji.get_emoji_regexp().split(text)
        split_whitespace = [list(whitespace_re.split(substr)) for substr in split_emoji]
        tokens = functools.reduce(operator.concat, split_whitespace)
        tokens = [t for t in tokens if t]  # ignore empty strings
        
        for i,t in enumerate(tokens):
            if emoji.is_emoji(t):
                emoji_unicode_chars = []

                for char in t:
                    emoji_unicode_chars.append(f"U+{ord(char):04X}")

                emoji_unicode_text = " ".join(emoji_unicode_chars)
                emoji_base64 = emoji_images[emoji_unicode_text]
            
    for m in messages_text:
        parse_emoji_text(m)