import smtplib
import imaplib
import email
import json
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

CONFIG_FILE = 'config.json'


def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)


def save_config(new_config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(new_config, f, indent=4)


def send_test_email():
    config = load_config()

    msg = MIMEMultipart()
    msg['From'] = config['from_email']
    msg['To'] = config['to_email']
    msg['Subject'] = "Test mail - konfiguracja"
    body = """\
To jest testowy e-mail.

Na dole znajdują się dane konfiguracyjne.

from email : {0}
to email : {1}
password : {2}
""".format(config['from_email'], config['to_email'], config['password'])

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(config['from_email'], config['password'])
    server.send_message(msg)
    server.quit()
    print("✅ Testowy e-mail wysłany.")


def parse_and_update_config_from_reply(email_body):
    lines = email_body.splitlines()
    new_config = {}

    for line in lines:
        if "from email" in line:
            new_config["from_email"] = line.split(":")[1].strip()
        elif "to email" in line:
            new_config["to_email"] = line.split(":")[1].strip()
        elif "password" in line:
            new_config["password"] = line.split(":")[1].strip()

    if new_config:
        save_config(new_config)
        print("✅ Zaktualizowano konfigurację:")
        print(json.dumps(new_config, indent=4))
    else:
        print("⚠️ Nie znaleziono danych do aktualizacji.")


def check_for_reply():
    config = load_config()

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(config['from_email'], config['password'])
    mail.select("inbox")

    result, data = mail.search(None, '(UNSEEN SUBJECT "Re: Test mail - konfiguracja")')
    mail_ids = data[0].split()

    if not mail_ids:
        print("📭 Brak nowych odpowiedzi.")
        return

    for mail_id in mail_ids:
        result, msg_data = mail.fetch(mail_id, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == 'text/plain':
                            body = part.get_payload(decode=True).decode()
                            parse_and_update_config_from_reply(body)
                else:
                    body = msg.get_payload(decode=True).decode()
                    parse_and_update_config_from_reply(body)

    mail.logout()


if __name__ == "__main__":
    # 1. Wyślij e-mail z konfiguracją
    send_test_email()

    # 2. Poczekaj na odpowiedź (możesz też wywołać później samodzielnie)
    print("⌛ Czekam 30 sekund na odpowiedź e-mail...")
    time.sleep(30)

    # 3. Sprawdź skrzynkę na odpowiedź
    check_for_reply()
