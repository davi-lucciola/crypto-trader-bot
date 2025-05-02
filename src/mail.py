import os
import smtplib
from dataclasses import dataclass
from email.message import Message


@dataclass
class MailException(Exception):
    message: str


SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_PORT = os.getenv('SMTP_PORT')
SENDER_EMAIL = os.getenv('EMAIL')
SENDER_PASSWORD = os.getenv('EMAIL_PASSWORD')


def send_email(email: str, subject: str, message: str):
    try:
        body = Message()
        body['From'] = SENDER_EMAIL
        body['To'] =  email
        body['Subject'] = subject
        body.add_header('Content-Type', 'text/html')
        body.set_payload(message)

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, email, body.as_string())
    except:
        raise MailException('Houve um error ao tentar enviar email.')
