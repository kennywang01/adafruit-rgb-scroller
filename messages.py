def read_messages():
    with open("messages.txt", "r", encoding='utf-8') as f:
        messages = f.readlines()
    return [m.strip() for m in messages]

if __name__ == "__main__":
    print(read_messages())